import datetime
import sys
import time
import trio
import trio_mysql
import pytest
import socket
from tests import base


class TempUser:
    def __init__(self, c, user, db, auth=None, authdata=None, password=None):
        self._c = c
        self._user = user
        self._password = password
        self._auth = auth
        self._authdata = authdata
        self._db = db

    async def __aenter__(self):
        create = "CREATE USER " + self._user
        if password is not None:
            create += " IDENTIFIED BY '%s'" % self._password
        elif auth is not None:
            create += " IDENTIFIED WITH %s" % self._auth
            if authdata is not None:
                create += " AS '%s'" % self._authdata

        try:
            await c.execute(create)
            self._created = True
        except trio_mysql.err.InternalError:
            # already exists - TODO need to check the same plugin applies
            self._created = False
        try:
            await c.execute("GRANT SELECT ON %s.* TO %s" % (db, user))
            self._grant = True
        except trio_mysql.err.InternalError:
            self._grant = False

        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        if self._grant:
            await self._c.execute("REVOKE SELECT ON %s.* FROM %s" % (self._db, self._user))
        if self._created:
            await self._c.execute("DROP USER %s" % self._user)

async def _get_plugins(db):
    async with trio_mysql.connect(**db) as conn:
        async with conn.cursor() as curs:
            await curs.execute("SHOW PLUGINS")
            res = await curs.fetchall()
            return res

def get_plugins(db):
    return trio.run(_get_plugins,db)

class TestAuthentication(base.TrioMySQLTestCase):

    socket_auth = False
    socket_found = False
    two_questions_found = False
    three_attempts_found = False
    pam_found = False
    mysql_old_password_found = False
    sha256_password_found = False

    import os
    osuser = os.environ.get('USER')

    # socket auth requires the current user and for the connection to be a socket
    # rest do grants @localhost due to incomplete logic - TODO change to @% then
    db = base.TrioMySQLTestCase.databases[0].copy()

    socket_auth = db.get('unix_socket') is not None \
                  and db.get('host') in ('localhost', '127.0.0.1')

    cur = get_plugins(db)
    del db['user']
    for r in cur:
        if (r[1], r[2]) !=  (u'ACTIVE', u'AUTHENTICATION'):
            continue
        if r[3] ==  u'auth_socket.so':
            socket_plugin_name = r[0]
            socket_found = True
        elif r[3] ==  u'dialog_examples.so':
            if r[0] == 'two_questions':
                two_questions_found =  True
            elif r[0] == 'three_attempts':
                three_attempts_found =  True
        elif r[0] ==  u'pam':
            pam_found = True
            pam_plugin_name = r[3].split('.')[0]
            if pam_plugin_name == 'auth_pam':
                pam_plugin_name = 'pam'
            # MySQL: authentication_pam
            # https://dev.mysql.com/doc/refman/5.5/en/pam-authentication-plugin.html

            # MariaDB: pam
            # https://mariadb.com/kb/en/mariadb/pam-authentication-plugin/

            # Names differ but functionality is close
        elif r[0] ==  u'mysql_old_password':
            mysql_old_password_found = True
        elif r[0] ==  u'sha256_password':
            sha256_password_found = True
        #else:
        #    print("plugin: %r" % r[0])

    @pytest.mark.trio
    async def test_plugin(self, set_me_up):
        await set_me_up(self)
        # Bit of an assumption that the current user is a native password
        self.assertEqual('mysql_native_password', self.connections[0]._auth_plugin_name)

    @pytest.mark.xfail(raises=base.SkipTest)
    @pytest.mark.skipif(not socket_auth, reason="connection to unix_socket required")
    @pytest.mark.skipif(socket_found, reason="socket plugin already installed")
    @pytest.mark.trio
    async def testSocketAuthInstallPlugin(self, set_me_up):
        await set_me_up(self)
        # needs plugin. lets install it.
        cur = self.connections[0].cursor()
        try:
            await cur.execute("install plugin auth_socket soname 'auth_socket.so'")
            TestAuthentication.socket_found = True
            self.socket_plugin_name = 'auth_socket'
            await self.realtestSocketAuth()
        except trio_mysql.err.InternalError:
            try:
                await cur.execute("install soname 'auth_socket'")
                TestAuthentication.socket_found = True
                self.socket_plugin_name = 'unix_socket'
                await self.realtestSocketAuth()
            except trio_mysql.err.InternalError:
                TestAuthentication.socket_found = False
                raise base.SkipTest('we couldn\'t install the socket plugin')
        finally:
            if TestAuthentication.socket_found:
                await cur.execute("uninstall plugin %s" % self.socket_plugin_name)

    @pytest.mark.skipif(not socket_auth, reason="connection to unix_socket required")
    @pytest.mark.skipif(not socket_found, reason="no socket plugin")
    @pytest.mark.trio
    async def testSocketAuth(self, set_me_up):
        await set_me_up(self)
        await self.realtestSocketAuth()

    async def realtestSocketAuth(self):
        async with TempUser(self.connections[0].cursor(), TestAuthentication.osuser + '@localhost',
                      self.databases[0]['db'], self.socket_plugin_name) as u:
            c = trio_mysql.connect(user=TestAuthentication.osuser, **self.db)
            await c.connect()
            await c.aclose()

    class Dialog(object):
        fail=False

        def __init__(self, con):
            self.fail=TestAuthentication.Dialog.fail
            pass

        async def prompt(self, echo, prompt):
            if self.fail:
               self.fail=False
               return b'bad guess at a password'
            return self.m.get(prompt)

    class DialogHandler(object):

        def __init__(self, con):
            self.con=con

        async def authenticate(self, pkt):
            while True:
                flag = pkt.read_uint8()
                echo = (flag & 0x06) == 0x02
                last = (flag & 0x01) == 0x01
                prompt = pkt.read_all()

                if prompt == b'Password, please:':
                    await self.con.write_packet(b'stillnotverysecret\0')
                else:
                    await self.con.write_packet(b'no idea what to do with this prompt\0')
                pkt = self.con._read_packet()
                pkt.check_error()
                if pkt.is_ok_packet() or last:
                    break
            return pkt

    class DefectiveHandler(object):
        def __init__(self, con):
            self.con=con


    @pytest.mark.xfail(raises=base.SkipTest)
    @pytest.mark.skipif(not socket_auth, reason="connection to unix_socket required")
    @pytest.mark.skipif(two_questions_found, reason="two_questions plugin already installed")
    @pytest.mark.trio
    async def testDialogAuthTwoQuestionsInstallPlugin(self, set_me_up):
        await set_me_up(self)
        # needs plugin. lets install it.
        cur = self.connections[0].cursor()
        try:
            await cur.execute("install plugin two_questions soname 'dialog_examples.so'")
            TestAuthentication.two_questions_found = True
            await self.realTestDialogAuthTwoQuestions()
        except trio_mysql.err.InternalError:
            raise base.SkipTest('we couldn\'t install the two_questions plugin')
        finally:
            if TestAuthentication.two_questions_found:
                await cur.execute("uninstall plugin two_questions")

    @pytest.mark.skipif(not socket_auth, reason="connection to unix_socket required")
    @pytest.mark.skipif(not two_questions_found, reason="no two questions auth plugin")
    @pytest.mark.trio
    async def testDialogAuthTwoQuestions(self, set_me_up):
        await set_me_up(self)
        await self.realTestDialogAuthTwoQuestions()

    async def realTestDialogAuthTwoQuestions(self):
        TestAuthentication.Dialog.fail=False
        TestAuthentication.Dialog.m = {b'Password, please:': b'notverysecret',
                                       b'Are you sure ?': b'yes, of course'}
        async with TempUser(self.connections[0].cursor(), 'trio_mysql_2q@localhost',
                      self.databases[0]['db'], 'two_questions', 'notverysecret') as u:
            with self.assertRaises(trio_mysql.err.OperationalError):
                c = trio_mysql.connect(user='trio_mysql_2q', **self.db)
                await c.connect()
            c = trio_mysql.connect(user='trio_mysql_2q', auth_plugin_map={b'dialog': TestAuthentication.Dialog}, **self.db)
            await c.connect()
            await c.aclose()

    @pytest.mark.xfail(raises=base.SkipTest)
    @pytest.mark.skipif(not socket_auth, reason="connection to unix_socket required")
    @pytest.mark.skipif(three_attempts_found, reason="three_attempts plugin already installed")
    @pytest.mark.trio
    async def testDialogAuthThreeAttemptsQuestionsInstallPlugin(self, set_me_up):
        await set_me_up(self)
        # needs plugin. lets install it.
        cur = self.connections[0].cursor()
        try:
            await cur.execute("install plugin three_attempts soname 'dialog_examples.so'")
            TestAuthentication.three_attempts_found = True
            await self.realTestDialogAuthThreeAttempts()
        except trio_mysql.err.InternalError:
            raise base.SkipTest('we couldn\'t install the three_attempts plugin')
        finally:
            if TestAuthentication.three_attempts_found:
                await cur.execute("uninstall plugin three_attempts")

    @pytest.mark.skipif(not socket_auth, reason="connection to unix_socket required")
    @pytest.mark.skipif(not three_attempts_found, reason="no three attempts plugin")
    @pytest.mark.trio
    async def testDialogAuthThreeAttempts(self, set_me_up):
        await set_me_up(self)
        await self.realTestDialogAuthThreeAttempts()

    async def realTestDialogAuthThreeAttempts(self):
        TestAuthentication.Dialog.m = {b'Password, please:': b'stillnotverysecret'}
        TestAuthentication.Dialog.fail=True   # fail just once. We've got three attempts after all
        async with TempUser(self.connections[0].cursor(), 'trio_mysql_3a@localhost',
                      self.databases[0]['db'], 'three_attempts', 'stillnotverysecret') as u:
            c = trio_mysql.connect(user='trio_mysql_3a', auth_plugin_map={b'dialog': TestAuthentication.Dialog}, **self.db)
            await c.connect()
            await c.aclose()
            c = trio_mysql.connect(user='trio_mysql_3a', auth_plugin_map={b'dialog': TestAuthentication.DialogHandler}, **self.db)
            await c.connect()
            await c.aclose()
            with self.assertRaises(trio_mysql.err.OperationalError):
                c = trio_mysql.connect(user='trio_mysql_3a', auth_plugin_map={b'dialog': object}, **self.db)

            with self.assertRaises(trio_mysql.err.OperationalError):
                c = trio_mysql.connect(user='trio_mysql_3a', auth_plugin_map={b'dialog': TestAuthentication.DefectiveHandler}, **self.db)
                await c.connect()
                await c.aclose()
            with self.assertRaises(trio_mysql.err.OperationalError):
                c = trio_mysql.connect(user='trio_mysql_3a', auth_plugin_map={b'notdialogplugin': TestAuthentication.Dialog}, **self.db)
                await c.connect()
                await c.aclose()
            TestAuthentication.Dialog.m = {b'Password, please:': b'I do not know'}
            with self.assertRaises(trio_mysql.err.OperationalError):
                c = trio_mysql.connect(user='trio_mysql_3a', auth_plugin_map={b'dialog': TestAuthentication.Dialog}, **self.db)
                await c.connect()
                await c.aclose()
            TestAuthentication.Dialog.m = {b'Password, please:': None}
            with self.assertRaises(trio_mysql.err.OperationalError):
                c = trio_mysql.connect(user='trio_mysql_3a', auth_plugin_map={b'dialog': TestAuthentication.Dialog}, **self.db)
                await c.connect()
                await c.aclose()

    @pytest.mark.xfail(raises=base.SkipTest)
    @pytest.mark.skipif(not socket_auth, reason="connection to unix_socket required")
    @pytest.mark.skipif(pam_found,reason= "pam plugin already installed")
    @pytest.mark.skipif(os.environ.get('PASSWORD') is None, reason="PASSWORD env var required")
    @pytest.mark.skipif(os.environ.get('PAMSERVICE') is None, reason="PAMSERVICE env var required")
    @pytest.mark.trio
    async def testPamAuthInstallPlugin(self, set_me_up):
        await set_me_up(self)
        # needs plugin. lets install it.
        cur = self.connections[0].cursor()
        try:
            await cur.execute("install plugin pam soname 'auth_pam.so'")
            TestAuthentication.pam_found = True
            await self.realTestPamAuth()
        except trio_mysql.err.InternalError:
            raise base.SkipTest('we couldn\'t install the auth_pam plugin')
        finally:
            if TestAuthentication.pam_found:
                await cur.execute("uninstall plugin pam")


    @pytest.mark.skipif(not socket_auth, reason="connection to unix_socket required")
    @pytest.mark.skipif(not pam_found, reason="no pam plugin")
    @pytest.mark.skipif(os.environ.get('PASSWORD') is None, reason="PASSWORD env var required")
    @pytest.mark.skipif(os.environ.get('PAMSERVICE') is None, reason="PAMSERVICE env var required")
    @pytest.mark.trio
    async def testPamAuth(self, set_me_up):
        await set_me_up(self)
        await self.realTestPamAuth()

    async def realTestPamAuth(self):
        db = self.db.copy()
        import os
        db['password'] = os.environ.get('PASSWORD')
        cur = self.connections[0].cursor()
        try:
            await cur.execute('show grants for ' + TestAuthentication.osuser + '@localhost')
            grants = (await cur.fetchone())[0]
            await cur.execute('drop user ' + TestAuthentication.osuser + '@localhost')
        except trio_mysql.OperationalError as e:
            # assuming the user doesn't exist which is ok too
            self.assertEqual(1045, e.args[0])
            grants = None
        async with TempUser(cur, TestAuthentication.osuser + '@localhost',
                      self.databases[0]['db'], 'pam', os.environ.get('PAMSERVICE')) as u:
            try:
                c = trio_mysql.connect(user=TestAuthentication.osuser, **db)
                await c.connect()
                db['password'] = 'very bad guess at password'
                with self.assertRaises(trio_mysql.err.OperationalError):
                    cc = trio_mysql.connect(user=TestAuthentication.osuser,
                                    auth_plugin_map={b'mysql_cleartext_password': TestAuthentication.DefectiveHandler},
                                    **self.db)
                    await cc.connect()
            except trio_mysql.OperationalError as e:
                self.assertEqual(1045, e.args[0])
                # we had 'bad guess at password' work with pam. Well at least we get a permission denied here
                with self.assertRaises(trio_mysql.err.OperationalError):
                    cc = trio_mysql.connect(user=TestAuthentication.osuser,
                                    auth_plugin_map={b'mysql_cleartext_password': TestAuthentication.DefectiveHandler},
                                    **self.db)
                    await cc.connect()
        if grants:
            # recreate the user
            await cur.execute(grants)

    # select old_password("crummy p\tassword");
    #| old_password("crummy p\tassword") |
    #| 2a01785203b08770                  |
    @pytest.mark.xfail(raises=base.SkipTest)
    @pytest.mark.skipif(not socket_auth, reason="connection to unix_socket required")
    @pytest.mark.skipif(not mysql_old_password_found, reason="no mysql_old_password plugin")
    @pytest.mark.trio
    async def testMySQLOldPasswordAuth(self, set_me_up):
        await set_me_up(self)
        if self.mysql_server_is(self.connections[0], (5, 7, 0)):
            raise base.SkipTest('Old passwords aren\'t supported in 5.7')
        # trio_mysql.err.OperationalError: (1045, "Access denied for user 'old_pass_user'@'localhost' (using password: YES)")
        # from login in MySQL-5.6
        if self.mysql_server_is(self.connections[0], (5, 6, 0)):
            raise base.SkipTest('Old passwords don\'t authenticate in 5.6')
        db = self.db.copy()
        db['password'] = "crummy p\tassword"
        with self.connections[0] as c:
            # deprecated in 5.6
            if sys.version_info[0:2] >= (3,2) and self.mysql_server_is(self.connections[0], (5, 6, 0)):
                with self.assertWarns(trio_mysql.err.Warning) as cm:
                    await c.execute("SELECT OLD_PASSWORD('%s')" % db['password'])
            else:
                await c.execute("SELECT OLD_PASSWORD('%s')" % db['password'])
            v = (await c.fetchone())[0]
            self.assertEqual(v, '2a01785203b08770')
            # only works in MariaDB and MySQL-5.6 - can't separate out by version
            #if self.mysql_server_is(self.connections[0], (5, 5, 0)):
            #    with TempUser(c, 'old_pass_user@localhost',
            #                  self.databases[0]['db'], 'mysql_old_password', '2a01785203b08770') as u:
            #        c = trio_mysql.connect(user='old_pass_user', **db)
            #        await c.connect()
            #        cur = c.cursor()
            #        await cur.execute("SELECT VERSION()")
            await c.execute("SELECT @@secure_auth")
            secure_auth_setting = (await c.fetchone())[0]
            await c.execute('set old_passwords=1')
            # trio_mysql.err.Warning: 'pre-4.1 password hash' is deprecated and will be removed in a future release. Please use post-4.1 password hash instead
            if sys.version_info[0:2] >= (3,2) and self.mysql_server_is(self.connections[0], (5, 6, 0)):
                with self.assertWarns(trio_mysql.err.Warning) as cm:
                    await c.execute('set global secure_auth=0')
            else:
                await c.execute('set global secure_auth=0')
            async with TempUser(c, 'old_pass_user@localhost',
                          self.databases[0]['db'], password=db['password']) as u:
                cc = trio_mysql.connect(user='old_pass_user', **db)
                await cc.connect()
                cur = cc.cursor()
                await cur.execute("SELECT VERSION()")
                await cc.aclose()
            await c.execute('set global secure_auth=%r' % secure_auth_setting)

    @pytest.mark.skipif(not socket_auth, reason="connection to unix_socket required")
    @pytest.mark.skipif(not sha256_password_found, reason="no sha256 password authentication plugin found")
    @pytest.mark.trio
    async def testAuthSHA256(self, set_me_up):
        await set_me_up(self)
        c = self.connections[0].cursor()
        async with TempUser(c, 'trio_mysql_sha256@localhost',
                      self.databases[0]['db'], 'sha256_password') as u:
            if self.mysql_server_is(self.connections[0], (5, 7, 0)):
                await c.execute("SET PASSWORD FOR 'trio_mysql_sha256'@'localhost' ='Sh@256Pa33'")
            else:
                await c.execute('SET old_passwords = 2')
                await c.execute("SET PASSWORD FOR 'trio_mysql_sha256'@'localhost' = PASSWORD('Sh@256Pa33')")
            db = self.db.copy()
            db['password'] = "Sh@256Pa33"
            # not implemented yet so thows error
            with self.assertRaises(trio_mysql.err.OperationalError):
                c = trio_mysql.connect(user='trio_mysql_256', **db)
                await c.connect()

class TestConnection(base.TrioMySQLTestCase):

    @pytest.mark.trio
    async def test_utf8mb4(self, set_me_up):
        await set_me_up(self)
        """This test requires MySQL >= 5.5"""
        arg = self.databases[0].copy()
        arg['charset'] = 'utf8mb4'
        conn = trio_mysql.connect(**arg)
        await conn.connect()
        await conn.aclose()

    @pytest.mark.trio
    async def test_largedata(self, set_me_up):
        await set_me_up(self)
        """Large query and response (>=16MB)"""
        cur = self.connections[0].cursor()
        await cur.execute("SELECT @@max_allowed_packet")
        if (await cur.fetchone())[0] < 16*1024*1024 + 10:
            print("Set max_allowed_packet to bigger than 17MB")
            return
        t = 'a' * (16*1024*1024)
        await cur.execute("SELECT '" + t + "'")
        assert (await cur.fetchone())[0] == t

    @pytest.mark.trio
    async def test_autocommit(self, set_me_up):
        await set_me_up(self)
        con = self.connections[0]
        self.assertFalse(con.get_autocommit())

        cur = con.cursor()
        await cur.execute("SET AUTOCOMMIT=1")
        self.assertTrue(con.get_autocommit())

        await con.autocommit(False)
        self.assertFalse(con.get_autocommit())
        await cur.execute("SELECT @@AUTOCOMMIT")
        assert (await cur.fetchone())[0] == 0

    @pytest.mark.trio
    async def test_select_db(self, set_me_up):
        await set_me_up(self)
        con = self.connections[0]
        current_db = self.databases[0]['db']
        other_db = self.databases[1]['db']

        cur = con.cursor()
        await cur.execute('SELECT database()')
        assert (await cur.fetchone())[0] == current_db

        await con.select_db(other_db)
        await cur.execute('SELECT database()')
        assert (await cur.fetchone())[0] == other_db

    @pytest.mark.trio
    async def test_connection_gone_away(self, set_me_up):
        await set_me_up(self)
        """
        http://dev.mysql.com/doc/refman/5.0/en/gone-away.html
        http://dev.mysql.com/doc/refman/5.0/en/error-messages-client.html#error_cr_server_gone_error
        """
        con = self.connections[0]
        cur = con.cursor()
        await cur.execute("SET wait_timeout=1")
        time.sleep(2)
        with pytest.raises(trio_mysql.OperationalError) as cm:
            await cur.execute("SELECT 1+1")
        # error may occur while reading, not writing because of socket buffer.
        #self.assertEqual(cm.exception.args[0], 2006)
        self.assertIn(cm.value.args[0], (2006, 2013))

    @pytest.mark.trio
    async def test_init_command(self, set_me_up):
        await set_me_up(self)
        conn = trio_mysql.connect(
            #init_command='SELECT "bar"; SELECT "baz"',
            init_command='SELECT "bar"',
            **self.databases[0]
        )
        await conn.connect()
        c = conn.cursor()
        await c.execute('select "foobar";')
        self.assertEqual(('foobar',), await c.fetchone())
        await conn.aclose()
        with self.assertRaises(trio_mysql.err.Error):
            await conn.ping(reconnect=False)

    @pytest.mark.trio
    async def test_read_default_group(self, set_me_up):
        await set_me_up(self)
        conn = trio_mysql.connect(
            read_default_group='client',
            **self.databases[0]
        )
        self.assertFalse(conn.open)
        await conn.connect()
        self.assertTrue(conn.open)
        await conn.aclose()

    @pytest.mark.trio
    async def test_context(self, set_me_up):
        await set_me_up(self)
        c = trio_mysql.connect(**self.databases[0])
        await c.connect()
        with self.assertRaises(ValueError):
            async with c as cur:
                await cur.execute('create table if not exists test ( a int )')
                await c.begin()
                await cur.execute('insert into test values ((1))')
                raise ValueError('pseudo abort')
                await c.commit() # never executed
        await c.aclose()

        c = trio_mysql.connect(**self.databases[0])
        await c.connect()
        async with c as cur:
            await cur.execute('select count(*) from test')
            self.assertEqual(0, (await cur.fetchone())[0])
            await cur.execute('insert into test values ((1))')
            await c.commit() # otherwise we may deadlock
        async with c as cur:
            await cur.execute('select count(*) from test')
            self.assertEqual(1, (await cur.fetchone())[0])
            await cur.execute('drop table test')

    @pytest.mark.trio
    async def test_set_charset(self, set_me_up):
        await set_me_up(self)
        c = trio_mysql.connect(**self.databases[0])
        await c.connect()
        await c.set_charset('utf8')
        await c.aclose()
        # TODO validate setting here

    @pytest.mark.trio
    async def test_defer_connect(self, set_me_up):
        await set_me_up(self)
        for db in self.databases:
            d = db.copy()
            try:
                sock = trio.socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                await sock.connect(d['unix_socket'])
            except KeyError:
                sock = await trio.open_tcp_stream \
                                (d.get('host', 'localhost'), d.get('port', 3306))
            for k in ['unix_socket', 'host', 'port']:
                try:
                    del d[k]
                except KeyError:
                    pass

            c = trio_mysql.connect(**d)
            self.assertFalse(c.open)
            await c.connect(sock)
            await c.aclose()
            await sock.aclose()

    @pytest.mark.skipif(sys.version_info[0:2] < (3,2), reason="required py-3.2")
    @pytest.mark.trio
    async def test_no_delay_warning(self, set_me_up):
        await set_me_up(self)
        current_db = self.databases[0].copy()
        current_db['no_delay'] =  True
        with self.assertWarns(DeprecationWarning) as cm:
            conn = trio_mysql.connect(**current_db)
            await conn.connect()
            await conn.aclose()


# A custom type and function to escape it
class Foo(object):
    value = "bar"


def escape_foo(x, d):
    return x.value


class TestEscape(base.TrioMySQLTestCase):
    @pytest.mark.trio
    async def test_escape_string(self, set_me_up):
        await set_me_up(self)
        con = self.connections[0]
        cur = con.cursor()

        self.assertEqual(con.escape("foo'bar"), "'foo\\'bar'")
        # added NO_AUTO_CREATE_USER as not including it in 5.7 generates warnings
        await cur.execute("SET sql_mode='NO_BACKSLASH_ESCAPES,NO_AUTO_CREATE_USER'")
        self.assertEqual(con.escape("foo'bar"), "'foo''bar'")

    @pytest.mark.trio
    async def test_escape_builtin_encoders(self, set_me_up):
        await set_me_up(self)
        con = self.connections[0]
        cur = con.cursor()

        val = datetime.datetime(2012, 3, 4, 5, 6)
        self.assertEqual(con.escape(val, con.encoders), "'2012-03-04 05:06:00'")

    @pytest.mark.trio
    async def test_escape_custom_object(self, set_me_up):
        await set_me_up(self)
        con = self.connections[0]
        cur = con.cursor()

        mapping = {Foo: escape_foo}
        self.assertEqual(con.escape(Foo(), mapping), "bar")

    @pytest.mark.trio
    async def test_escape_fallback_encoder(self, set_me_up):
        await set_me_up(self)
        con = self.connections[0]
        cur = con.cursor()

        class Custom(str):
            pass

        mapping = {str: trio_mysql.escape_string}
        self.assertEqual(con.escape(Custom('foobar'), mapping), "'foobar'")

    @pytest.mark.trio
    async def test_escape_no_default(self, set_me_up):
        await set_me_up(self)
        con = self.connections[0]
        cur = con.cursor()

        self.assertRaises(TypeError, con.escape, 42, {})

    @pytest.mark.trio
    async def test_escape_dict_value(self, set_me_up):
        await set_me_up(self)
        con = self.connections[0]
        cur = con.cursor()

        mapping = con.encoders.copy()
        mapping[Foo] = escape_foo
        self.assertEqual(con.escape({'foo': Foo()}, mapping), {'foo': "bar"})

    @pytest.mark.trio
    async def test_escape_list_item(self, set_me_up):
        await set_me_up(self)
        con = self.connections[0]
        cur = con.cursor()

        mapping = con.encoders.copy()
        mapping[Foo] = escape_foo
        self.assertEqual(con.escape([Foo()], mapping), "(bar)")

    @pytest.mark.skip("we don't have multiselect")
    @pytest.mark.trio
    async def test_previous_cursor_not_closed(self, set_me_up):
        await set_me_up(self)
        con = self.connections[0]
        cur1 = con.cursor()
        await cur1.execute("SELECT 1; SELECT 2")
        cur2 = con.cursor()
        await cur2.execute("SELECT 3")
        assert (await cur2.fetchone())[0] == 3

    @pytest.mark.skip("we don't have multiselect")
    @pytest.mark.trio
    async def test_commit_during_multi_result(self, set_me_up):
        await set_me_up(self)
        con = self.connections[0]
        cur = con.cursor()
        await cur.execute("SELECT 1; SELECT 2")
        await con.commit()
        await cur.execute("SELECT 3")
        assert (await cur.fetchone())[0] == 3
