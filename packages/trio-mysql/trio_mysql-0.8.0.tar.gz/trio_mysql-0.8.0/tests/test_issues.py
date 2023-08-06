import datetime
import time
import warnings
import sys

import trio_mysql
from trio_mysql import cursors
from tests import base
import pytest

try:
    import imp
    reload = imp.reload
except AttributeError:
    pass


__all__ = ["TestOldIssues", "TestNewIssues", "TestGitHubIssues"]

class TestOldIssues(base.TrioMySQLTestCase):
    @pytest.mark.trio
    async def test_issue_3(self, set_me_up):
        await set_me_up(self)
        """ undefined methods datetime_or_None, date_or_None """
        conn = self.connections[0]
        c = conn.cursor()
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore")
            await c.execute("drop table if exists issue3")
        await c.execute("create table issue3 (d date, t time, dt datetime, ts timestamp)")
        try:
            await c.execute("insert into issue3 (d, t, dt, ts) values (%s,%s,%s,%s)", (None, None, None, None))
            await c.execute("select d from issue3")
            self.assertEqual(None, (await c.fetchone())[0])
            await c.execute("select t from issue3")
            self.assertEqual(None, (await c.fetchone())[0])
            await c.execute("select dt from issue3")
            self.assertEqual(None, (await c.fetchone())[0])
            await c.execute("select ts from issue3")
            self.assertTrue(isinstance((await c.fetchone())[0], datetime.datetime))
        finally:
            await c.execute("drop table issue3")

    @pytest.mark.trio
    async def test_issue_4(self, set_me_up):
        await set_me_up(self)
        """ can't retrieve TIMESTAMP fields """
        conn = self.connections[0]
        c = conn.cursor()
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore")
            await c.execute("drop table if exists issue4")
        await c.execute("create table issue4 (ts timestamp)")
        try:
            await c.execute("insert into issue4 (ts) values (now())")
            await c.execute("select ts from issue4")
            self.assertTrue(isinstance((await c.fetchone())[0], datetime.datetime))
        finally:
            await c.execute("drop table issue4")

    @pytest.mark.trio
    async def test_issue_5(self, set_me_up):
        await set_me_up(self)
        """ query on information_schema.tables fails """
        con = self.connections[0]
        cur = con.cursor()
        await cur.execute("select * from information_schema.tables")

    @pytest.mark.trio
    async def test_issue_6(self, set_me_up):
        await set_me_up(self)
        """ exception: TypeError: ord() expected a character, but string of length 0 found """
        # ToDo: this test requires access to db 'mysql'.
        kwargs = self.databases[0].copy()
        kwargs['db'] = "mysql"
        conn = trio_mysql.connect(**kwargs)
        await conn.connect()
        c = conn.cursor()
        await c.execute("select * from user")
        await conn.aclose()

    @pytest.mark.trio
    async def test_issue_8(self, set_me_up):
        await set_me_up(self)
        """ Primary Key and Index error when selecting data """
        conn = self.connections[0]
        c = conn.cursor()
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore")
            await c.execute("drop table if exists test")
        await c.execute("""CREATE TABLE `test` (`station` int(10) NOT NULL DEFAULT '0', `dh`
datetime NOT NULL DEFAULT '2015-01-01 00:00:00', `echeance` int(1) NOT NULL
DEFAULT '0', `me` double DEFAULT NULL, `mo` double DEFAULT NULL, PRIMARY
KEY (`station`,`dh`,`echeance`)) ENGINE=MyISAM DEFAULT CHARSET=latin1;""")
        try:
            self.assertEqual(0, await c.execute("SELECT * FROM test"))
            await c.execute("ALTER TABLE `test` ADD INDEX `idx_station` (`station`)")
            self.assertEqual(0, await c.execute("SELECT * FROM test"))
        finally:
            await c.execute("drop table test")

    @pytest.mark.trio
    async def test_issue_9(self, set_me_up):
        await set_me_up(self)
        """ sets DeprecationWarning in Python 2.6 """
        try:
            reload(trio_mysql)
        except DeprecationWarning:
            self.fail()

    @pytest.mark.trio
    async def test_issue_13(self, set_me_up):
        await set_me_up(self)
        """ can't handle large result fields """
        conn = self.connections[0]
        cur = conn.cursor()
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore")
            await cur.execute("drop table if exists issue13")
        try:
            await cur.execute("create table issue13 (t text)")
            # ticket says 18k
            size = 18*1024
            await cur.execute("insert into issue13 (t) values (%s)", ("x" * size,))
            await cur.execute("select t from issue13")
            # use assertTrue so that obscenely huge error messages don't print
            r = (await cur.fetchone())[0]
            self.assertTrue("x" * size == r)
        finally:
            await cur.execute("drop table issue13")

    @pytest.mark.trio
    async def test_issue_15(self, set_me_up):
        await set_me_up(self)
        """ query should be expanded before perform character encoding """
        conn = self.connections[0]
        c = conn.cursor()
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore")
            await c.execute("drop table if exists issue15")
        await c.execute("create table issue15 (t varchar(32))")
        try:
            await c.execute("insert into issue15 (t) values (%s)", (u'\xe4\xf6\xfc',))
            await c.execute("select t from issue15")
            self.assertEqual(u'\xe4\xf6\xfc', (await c.fetchone())[0])
        finally:
            await c.execute("drop table issue15")

    @pytest.mark.trio
    async def test_issue_16(self, set_me_up):
        await set_me_up(self)
        """ Patch for string and tuple escaping """
        conn = self.connections[0]
        c = conn.cursor()
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore")
            await c.execute("drop table if exists issue16")
        await c.execute("create table issue16 (name varchar(32) primary key, email varchar(32))")
        try:
            await c.execute("insert into issue16 (name, email) values ('pete', 'floydophone')")
            await c.execute("select email from issue16 where name=%s", ("pete",))
            self.assertEqual("floydophone", (await c.fetchone())[0])
        finally:
            await c.execute("drop table issue16")

    @pytest.mark.skip("test_issue_17() requires a custom, legacy MySQL configuration and will not be run.")
    @pytest.mark.trio
    async def test_issue_17(self, set_me_up):
        await set_me_up(self)
        """could not connect mysql use passwod"""
        conn = self.connections[0]
        host = self.databases[0]["host"]
        db = self.databases[0]["db"]
        c = conn.cursor()

        # grant access to a table to a user with a password
        try:
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore")
                await c.execute("drop table if exists issue17")
            await c.execute("create table issue17 (x varchar(32) primary key)")
            await c.execute("insert into issue17 (x) values ('hello, world!')")
            await c.execute("grant all privileges on %s.issue17 to 'issue17user'@'%%' identified by '1234'" % db)
            await conn.commit()

            conn2 = trio_mysql.connect(host=host, user="issue17user", passwd="1234", db=db)
            c2 = conn2.cursor()
            await c2.execute("select x from issue17")
            self.assertEqual("hello, world!", (await c2.fetchone())[0])
        finally:
            await c.execute("drop table issue17")

class TestNewIssues(base.TrioMySQLTestCase):
    @pytest.mark.trio
    async def test_issue_34(self, set_me_up):
        await set_me_up(self)
        try:
            c = trio_mysql.connect(host="localhost", port=1237, user="root")
            await c.connect()
            self.fail()
        except trio_mysql.OperationalError as e:
            self.assertEqual(2003, e.args[0])

    @pytest.mark.trio
    async def test_issue_33(self, set_me_up):
        await set_me_up(self)
        conn = trio_mysql.connect(charset="utf8", **self.databases[0])
        await conn.connect()
        await self.safe_create_table(conn, u'hei\xdfe',
                               u'create table hei\xdfe (name varchar(32))')
        c = conn.cursor()
        await c.execute(u"insert into hei\xdfe (name) values ('Pi\xdfata')")
        await c.execute(u"select name from hei\xdfe")
        self.assertEqual(u"Pi\xdfata", (await c.fetchone())[0])

    @pytest.mark.skip("This test requires manual intervention")
    @pytest.mark.trio
    async def test_issue_35(self, set_me_up):
        await set_me_up(self)
        conn = self.connections[0]
        c = conn.cursor()
        print("sudo killall -9 mysqld within the next 10 seconds")
        try:
            await c.execute("select sleep(10)")
            self.fail()
        except trio_mysql.OperationalError as e:
            self.assertEqual(2013, e.args[0])

    @pytest.mark.trio
    async def test_issue_36(self, set_me_up):
        await set_me_up(self)
        # connection 0 is super user, connection 1 isn't
        conn = self.connections[1]
        await conn.connect()
        c = conn.cursor()
        await c.execute("show processlist")
        kill_id = None
        for row in await c.fetchall():
            id = row[0]
            info = row[7]
            if info == "show processlist":
                kill_id = id
                break
        self.assertEqual(kill_id, conn.thread_id())
        # now nuke the connection
        await self.connections[0].kill(kill_id)
        # make sure this connection has broken
        try:
            await c.execute("show tables")
            self.fail()
        except Exception:
            pass
        await c.aclose()
        await conn.aclose()

        # check the process list from the other connection
        try:
            # Wait since Travis-CI sometimes fail this test.
            time.sleep(0.1)

            c = self.connections[0].cursor()
            await c.execute("show processlist")
            ids = [row[0] for row in await c.fetchall()]
            self.assertFalse(kill_id in ids)
        finally:
            del self.connections[1]

    @pytest.mark.trio
    async def test_issue_37(self, set_me_up):
        await set_me_up(self)
        conn = self.connections[0]
        c = conn.cursor()
        self.assertEqual(1, await c.execute("SELECT @foo"))
        self.assertEqual((None,), await c.fetchone())
        self.assertEqual(0, await c.execute("SET @foo = 'bar'"))
        await c.execute("set @foo = 'bar'")

    @pytest.mark.trio
    async def test_issue_38(self, set_me_up):
        await set_me_up(self)
        conn = self.connections[0]
        c = conn.cursor()
        datum = "a" * 1024 * 1023 # reduced size for most default mysql installs

        try:
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore")
                await c.execute("drop table if exists issue38")
            await c.execute("create table issue38 (id integer, data mediumblob)")
            await c.execute("insert into issue38 values (1, %s)", (datum,))
        finally:
            await c.execute("drop table issue38")

    async def disabled_test_issue_54(self):
        conn = self.connections[0]
        c = conn.cursor()
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore")
            await c.execute("drop table if exists issue54")
        big_sql = "select * from issue54 where "
        big_sql += " and ".join("%d=%d" % (i,i) for i in range(0, 100000))

        try:
            await c.execute("create table issue54 (id integer primary key)")
            await c.execute("insert into issue54 (id) values (7)")
            await c.execute(big_sql)
            self.assertEqual(7, (await c.fetchone())[0])
        finally:
            await c.execute("drop table issue54")

class TestGitHubIssues(base.TrioMySQLTestCase):
    @pytest.mark.trio
    async def test_issue_66(self, set_me_up):
        await set_me_up(self)
        """ 'Connection' object has no attribute 'insert_id' """
        conn = self.connections[0]
        c = conn.cursor()
        self.assertEqual(0, conn.insert_id())
        try:
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore")
                await c.execute("drop table if exists issue66")
            await c.execute("create table issue66 (id integer primary key auto_increment, x integer)")
            await c.execute("insert into issue66 (x) values (1)")
            await c.execute("insert into issue66 (x) values (1)")
            self.assertEqual(2, conn.insert_id())
        finally:
            await c.execute("drop table issue66")

    @pytest.mark.trio
    async def test_issue_79(self, set_me_up):
        await set_me_up(self)
        """ Duplicate field overwrites the previous one in the result of DictCursor """
        conn = self.connections[0]
        c = conn.cursor(trio_mysql.cursors.DictCursor)

        with warnings.catch_warnings():
            warnings.filterwarnings("ignore")
            await c.execute("drop table if exists a")
            await c.execute("drop table if exists b")
        await c.execute("""CREATE TABLE a (id int, value int)""")
        await c.execute("""CREATE TABLE b (id int, value int)""")

        a=(1,11)
        b=(1,22)
        try:
            await c.execute("insert into a values (%s, %s)", a)
            await c.execute("insert into b values (%s, %s)", b)

            await c.execute("SELECT * FROM a inner join b on a.id = b.id")
            r = (await c.fetchall())[0]
            self.assertEqual(r['id'], 1)
            self.assertEqual(r['value'], 11)
            self.assertEqual(r['b.value'], 22)
        finally:
            await c.execute("drop table a")
            await c.execute("drop table b")

    @pytest.mark.trio
    async def test_issue_95(self, set_me_up):
        await set_me_up(self)
        """ Leftover trailing OK packet for "CALL my_sp" queries """
        conn = self.connections[0]
        cur = conn.cursor()
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore")
            await cur.execute("DROP PROCEDURE IF EXISTS `foo`")
        await cur.execute("""CREATE PROCEDURE `foo` ()
        BEGIN
            SELECT 1;
        END""")
        try:
            await cur.execute("""CALL foo()""")
            await cur.execute("""SELECT 1""")
            self.assertEqual((await cur.fetchone())[0], 1)
        finally:
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore")
                await cur.execute("DROP PROCEDURE IF EXISTS `foo`")

    @pytest.mark.trio
    async def test_issue_114(self, set_me_up):
        await set_me_up(self)
        """ autocommit is not set after reconnecting with ping() """
        conn = trio_mysql.connect(charset="utf8", **self.databases[0])
        await conn.connect()
        await conn.autocommit(False)
        c = conn.cursor()
        await c.execute("""select @@autocommit;""")
        self.assertFalse((await c.fetchone())[0])
        await conn.aclose()
        await conn.ping()
        await c.execute("""select @@autocommit;""")
        self.assertFalse((await c.fetchone())[0])
        await conn.aclose()

        # Ensure autocommit() is still working
        conn = trio_mysql.connect(charset="utf8", **self.databases[0])
        await conn.connect()
        c = conn.cursor()
        await c.execute("""select @@autocommit;""")
        self.assertFalse((await c.fetchone())[0])
        await conn.aclose()
        await conn.ping()
        await conn.autocommit(True)
        await c.execute("""select @@autocommit;""")
        self.assertTrue((await c.fetchone())[0])
        await conn.aclose()

    @pytest.mark.trio
    async def test_issue_175(self, set_me_up):
        await set_me_up(self)
        """ The number of fields returned by server is read in wrong way """
        conn = self.connections[0]
        cur = conn.cursor()
        for length in (200, 300):
            columns = ', '.join('c{0} integer'.format(i) for i in range(length))
            sql = 'create table test_field_count ({0})'.format(columns)
            try:
                await cur.execute(sql)
                await cur.execute('select * from test_field_count')
                assert len(cur.description) == length
            finally:
                with warnings.catch_warnings():
                    warnings.filterwarnings("ignore")
                    await cur.execute('drop table if exists test_field_count')

    @pytest.mark.trio
    async def test_issue_321(self, set_me_up):
        await set_me_up(self)
        """ Test iterable as query argument. """
        conn = trio_mysql.connect(charset="utf8", **self.databases[0])
        await conn.connect()
        await self.safe_create_table(
            conn, "issue321",
            "create table issue321 (value_1 varchar(1), value_2 varchar(1))")

        sql_insert = "insert into issue321 (value_1, value_2) values (%s, %s)"
        sql_dict_insert = ("insert into issue321 (value_1, value_2) "
                           "values (%(value_1)s, %(value_2)s)")
        sql_select = ("select * from issue321 where "
                      "value_1 in %s and value_2=%s")
        data = [
            [(u"a", ), u"\u0430"],
            [[u"b"], u"\u0430"],
            {"value_1": [[u"c"]], "value_2": u"\u0430"}
        ]
        cur = conn.cursor()
        self.assertEqual(await cur.execute(sql_insert, data[0]), 1)
        self.assertEqual(await cur.execute(sql_insert, data[1]), 1)
        self.assertEqual(await cur.execute(sql_dict_insert, data[2]), 1)
        self.assertEqual(
            await cur.execute(sql_select, [(u"a", u"b", u"c"), u"\u0430"]), 3)
        self.assertEqual(await cur.fetchone(), (u"a", u"\u0430"))
        self.assertEqual(await cur.fetchone(), (u"b", u"\u0430"))
        self.assertEqual(await cur.fetchone(), (u"c", u"\u0430"))

    @pytest.mark.trio
    async def test_issue_364(self, set_me_up):
        await set_me_up(self)
        """ Test mixed unicode/binary arguments in executemany. """
        conn = trio_mysql.connect(charset="utf8", **self.databases[0])
        await conn.connect()
        await self.safe_create_table(
            conn, "issue364",
            "create table issue364 (value_1 binary(3), value_2 varchar(3)) "
            "engine=InnoDB default charset=utf8")

        sql = "insert into issue364 (value_1, value_2) values (_binary %s, %s)"
        usql = u"insert into issue364 (value_1, value_2) values (_binary %s, %s)"
        values = [trio_mysql.Binary(b"\x00\xff\x00"), u"\xe4\xf6\xfc"]

        # test single insert and select
        cur = conn.cursor()
        await cur.execute(sql, args=values)
        await cur.execute("select * from issue364")
        self.assertEqual(await cur.fetchone(), tuple(values))

        # test single insert unicode query
        await cur.execute(usql, args=values)

        # test multi insert and select
        await cur.executemany(sql, args=(values, values, values))
        await cur.execute("select * from issue364")
        for row in await cur.fetchall():
            self.assertEqual(row, tuple(values))

        # test multi insert with unicode query
        await cur.executemany(usql, args=(values, values, values))

    @pytest.mark.trio
    async def test_issue_363(self, set_me_up):
        await set_me_up(self)
        """ Test binary / geometry types. """
        conn = trio_mysql.connect(charset="utf8", **self.databases[0])
        await conn.connect()
        await self.safe_create_table(
            conn, "issue363",
            "CREATE TABLE issue363 ( "
            "id INTEGER PRIMARY KEY, geom LINESTRING NOT NULL, "
            "SPATIAL KEY geom (geom)) "
            "ENGINE=MyISAM default charset=utf8")

        cur = conn.cursor()
        query = ("INSERT INTO issue363 (id, geom) VALUES"
                 "(1998, GeomFromText('LINESTRING(1.1 1.1,2.2 2.2)'))")
        # From MySQL 5.7, ST_GeomFromText is added and GeomFromText is deprecated.
        if self.mysql_server_is(conn, (5, 7, 0)):
            with self.assertWarns(trio_mysql.err.Warning) as cm:
                await cur.execute(query)
        else:
            await cur.execute(query)

        # select WKT
        query = "SELECT AsText(geom) FROM issue363"
        if self.mysql_server_is(conn, (5, 7, 0)):
            with self.assertWarns(trio_mysql.err.Warning) as cm:
                await cur.execute(query)
        else:
            await cur.execute(query)
        row = await cur.fetchone()
        self.assertEqual(row, ("LINESTRING(1.1 1.1,2.2 2.2)", ))

        # select WKB
        query = "SELECT AsBinary(geom) FROM issue363"
        if self.mysql_server_is(conn, (5, 7, 0)):
            with self.assertWarns(trio_mysql.err.Warning) as cm:
                await cur.execute(query)
        else:
            await cur.execute(query)
        row = await cur.fetchone()
        self.assertEqual(row,
                         (b"\x01\x02\x00\x00\x00\x02\x00\x00\x00"
                          b"\x9a\x99\x99\x99\x99\x99\xf1?"
                          b"\x9a\x99\x99\x99\x99\x99\xf1?"
                          b"\x9a\x99\x99\x99\x99\x99\x01@"
                          b"\x9a\x99\x99\x99\x99\x99\x01@", ))

        # select internal binary
        await cur.execute("SELECT geom FROM issue363")
        row = await cur.fetchone()
        # don't assert the exact internal binary value, as it could
        # vary across implementations
        self.assertTrue(isinstance(row[0], bytes))

    @pytest.mark.trio
    async def test_issue_491(self, set_me_up):
        await set_me_up(self)
        """ Test warning propagation """
        conn = trio_mysql.connect(charset="utf8", **self.databases[0])
        await conn.connect()

        with warnings.catch_warnings():
            # Ignore all warnings other than trio_mysql generated ones
            warnings.simplefilter("ignore")
            warnings.simplefilter("error", category=trio_mysql.Warning)

            # verify for both buffered and unbuffered cursor types
            for cursor_class in (cursors.Cursor, cursors.SSCursor):
                c = conn.cursor(cursor_class)
                try:
                    await c.execute("SELECT CAST('124b' AS SIGNED)")
                    await c.fetchall()
                except trio_mysql.Warning as e:
                    # Warnings should have errorcode and string message, just like exceptions
                    self.assertEqual(len(e.args), 2)
                    self.assertEqual(e.args[0], 1292)
                    self.assertTrue(isinstance(e.args[1], str))
                else:
                    self.fail("Should raise Warning")
                finally:
                    await c.aclose()
