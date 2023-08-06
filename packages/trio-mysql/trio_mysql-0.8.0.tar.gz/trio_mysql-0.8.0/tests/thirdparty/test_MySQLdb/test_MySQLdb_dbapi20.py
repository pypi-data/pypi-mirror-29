import pytest

from tests.thirdparty.test_MySQLdb import dbapi20
import trio_mysql
from tests import base


class Test_MySQLdb(dbapi20.TestDatabaseAPI20):
    driver = trio_mysql
    connect_args = ()
    connect_kw_args = base.TrioMySQLTestCase.databases[0].copy()
    connect_kw_args.update(dict(read_default_file='~/.my.cnf',
                                charset='utf8',
                                sql_mode="ANSI,STRICT_TRANS_TABLES,TRADITIONAL"))

    def test_setoutputsize(self): pass
    def test_setoutputsize_basic(self): pass
    def test_nextset(self): pass

    """The tests on fetchone and fetchall and rowcount bogusly
    test for an exception if the statement cannot return a
    result set. MySQL always returns a result set; it's just that
    some things return empty result sets."""

    @pytest.mark.trio
    async def test_fetchall(self, set_me_up):
        await set_me_up(self)
        con = await self._connect()
        try:
            cur = con.cursor()
            # cursor.fetchall should raise an Error if called
            # without executing a query that may return rows (such
            # as a select)
            with pytest.raises(self.driver.Error):
                await cur.fetchall()

            await self.executeDDL1(cur)
            for sql in self._populate():
                await cur.execute(sql)

            # cursor.fetchall should raise an Error if called
            # after executing a a statement that cannot return rows
##             self.assertRaises(self.driver.Error,cur.fetchall)

            await cur.execute('select name from %sbooze' % self.table_prefix)
            rows = await cur.fetchall()
            self.assertTrue(cur.rowcount in (-1,len(self.samples)))
            self.assertEqual(len(rows),len(self.samples),
                'cursor.fetchall did not retrieve all rows'
                )
            rows = [r[0] for r in rows]
            rows.sort()
            for i in range(0,len(self.samples)):
                self.assertEqual(rows[i],self.samples[i],
                'cursor.fetchall retrieved incorrect rows'
                )
            rows = await cur.fetchall()
            self.assertEqual(
                len(rows),0,
                'cursor.fetchall should return an empty list if called '
                'after the whole result set has been fetched'
                )
            self.assertTrue(cur.rowcount in (-1,len(self.samples)))

            await self.executeDDL2(cur)
            await cur.execute('select name from %sbarflys' % self.table_prefix)
            rows = await cur.fetchall()
            self.assertTrue(cur.rowcount in (-1,0))
            self.assertEqual(len(rows),0,
                'cursor.fetchall should return an empty list if '
                'a select query returns no rows'
                )

        finally:
            await con.aclose()

    @pytest.mark.trio
    async def test_fetchone(self, set_me_up):
        await set_me_up(self)
        con = await self._connect()
        try:
            cur = con.cursor()

            # cursor.fetchone should raise an Error if called before
            # executing a select-type query
            with pytest.raises(self.driver.Error):
                await cur.fetchone()

            # cursor.fetchone should raise an Error if called after
            # executing a query that cannnot return rows
            await self.executeDDL1(cur)
##             self.assertRaises(self.driver.Error,cur.fetchone)

            await cur.execute('select name from %sbooze' % self.table_prefix)
            self.assertEqual(await cur.fetchone(),None,
                'cursor.fetchone should return None if a query retrieves '
                'no rows'
                )
            self.assertTrue(cur.rowcount in (-1,0))

            # cursor.fetchone should raise an Error if called after
            # executing a query that cannnot return rows
            await cur.execute("insert into %sbooze values ('Victoria Bitter')" % (
                self.table_prefix
                ))
##             self.assertRaises(self.driver.Error,await cur.fetchone)

            await cur.execute('select name from %sbooze' % self.table_prefix)
            r = await cur.fetchone()
            self.assertEqual(len(r),1,
                'cursor.fetchone should have retrieved a single row'
                )
            self.assertEqual(r[0],'Victoria Bitter',
                'cursor.fetchone retrieved incorrect data'
                )
##             self.assertEqual(await cur.fetchone(),None,
##                 'cursor.fetchone should return None if no more rows available'
##                 )
            self.assertTrue(cur.rowcount in (-1,1))
        finally:
            await con.aclose()

    # Same complaint as for fetchall and fetchone
    @pytest.mark.trio
    async def test_rowcount(self, set_me_up):
        await set_me_up(self)
        con = await self._connect()
        try:
            cur = con.cursor()
            await self.executeDDL1(cur)
##             self.assertEqual(cur.rowcount,-1,
##                 'cursor.rowcount should be -1 after executing no-result '
##                 'statements'
##                 )
            await cur.execute("insert into %sbooze values ('Victoria Bitter')" % (
                self.table_prefix
                ))
##             self.assertTrue(cur.rowcount in (-1,1),
##                 'cursor.rowcount should == number or rows inserted, or '
##                 'set to -1 after executing an insert statement'
##                 )
            await cur.execute("select name from %sbooze" % self.table_prefix)
            self.assertTrue(cur.rowcount in (-1,1),
                'cursor.rowcount should == number of rows returned, or '
                'set to -1 after executing a select statement'
                )
            await self.executeDDL2(cur)
##             self.assertEqual(cur.rowcount,-1,
##                 'cursor.rowcount not being reset to -1 after executing '
##                 'no-result statements'
##                 )
        finally:
            await con.aclose()

    @pytest.mark.trio
    async def test_callproc(self, set_me_up):
        await set_me_up(self)
        pass # performed in test_MySQL_capabilities

    async def help_nextset_setUp(self,cur):
        ''' Should create a procedure called deleteme
            that returns two result sets, first the
            number of rows in booze then "name from booze"
        '''
        sql="""
           create procedure deleteme()
           begin
               select count(*) from %(tp)sbooze;
               select name from %(tp)sbooze;
           end
        """ % dict(tp=self.table_prefix)
        await cur.execute(sql)

    async def help_nextset_tearDown(self,cur):
        'If cleaning up is needed after nextSetTest'
        await cur.execute("drop procedure deleteme")

    @pytest.mark.trio
    async def test_nextset(self, set_me_up):
        await set_me_up(self)
        from warnings import warn
        con = await self._connect()
        try:
            cur = con.cursor()
            if not hasattr(cur,'nextset'):
                return

            try:
                await self.executeDDL1(cur)
                sql=self._populate()
                for sql in self._populate():
                    await cur.execute(sql)

                await self.help_nextset_setUp(cur)

                await cur.callproc('deleteme')
                numberofrows=await cur.fetchone()
                assert numberofrows[0]== len(self.samples)
                assert await cur.nextset()
                names=await cur.fetchall()
                assert len(names) == len(self.samples)
                s=await cur.nextset()
                if s:
                    empty = await cur.fetchall()
                    self.assertEqual(len(empty), 0,
                                      "non-empty result set after other result sets")
                    #warn("Incompatibility: MySQL returns an empty result set for the CALL itself",
                    #     Warning)
                #assert s == None,'No more return sets, should return None'
            finally:
                await self.help_nextset_tearDown(cur)

        finally:
            await con.aclose()
