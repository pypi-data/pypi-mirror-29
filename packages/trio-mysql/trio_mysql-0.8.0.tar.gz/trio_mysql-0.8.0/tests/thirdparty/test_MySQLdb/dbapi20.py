''' Python DB API 2.0 driver compliance unit test suite.

    This software is Public Domain and may be used without restrictions.

 "Now we have booze and barflies entering the discussion, plus rumours of
  DBAs on drugs... and I won't tell you what flashes through my mind each
  time I read the subject line with 'Anal Compliance' in it.  All around
  this is turning out to be a thoroughly unwholesome unit test."

    -- Ian Bicking
'''

__rcs_id__  = '$Id$'
__version__ = '$Revision$'[11:-2]
__author__ = 'Stuart Bishop <zen@shangri-la.dropbear.id.au>'

import time
import pytest
from tests import base

# $Log$
# Revision 1.1.2.1  2006/02/25 03:44:32  adustman
# Generic DB-API unit test module
#
# Revision 1.10  2003/10/09 03:14:14  zenzen
# Add test for DB API 2.0 optional extension, where database exceptions
# are exposed as attributes on the Connection object.
#
# Revision 1.9  2003/08/13 01:16:36  zenzen
# Minor tweak from Stefan Fleiter
#
# Revision 1.8  2003/04/10 00:13:25  zenzen
# Changes, as per suggestions by M.-A. Lemburg
# - Add a table prefix, to ensure namespace collisions can always be avoided
#
# Revision 1.7  2003/02/26 23:33:37  zenzen
# Break out DDL into helper functions, as per request by David Rushby
#
# Revision 1.6  2003/02/21 03:04:33  zenzen
# Stuff from Henrik Ekelund:
#     added test_None
#     added test_nextset & hooks
#
# Revision 1.5  2003/02/17 22:08:43  zenzen
# Implement suggestions and code from Henrik Eklund - test that cursor.arraysize
# defaults to 1 & generic cursor.callproc test added
#
# Revision 1.4  2003/02/15 00:16:33  zenzen
# Changes, as per suggestions and bug reports by M.-A. Lemburg,
# Matthew T. Kromer, Federico Di Gregorio and Daniel Dittmar
# - Class renamed
# - Now a subclass of TestCase, to avoid requiring the driver stub
#   to use multiple inheritance
# - Reversed the polarity of buggy test in test_description
# - Test exception heirarchy correctly
# - self.populate is now self._populate(), so if a driver stub
#   overrides self.ddl1 this change propogates
# - VARCHAR columns now have a width, which will hopefully make the
#   DDL even more portible (this will be reversed if it causes more problems)
# - cursor.rowcount being checked after various execute and fetchXXX methods
# - Check for fetchall and fetchmany returning empty lists after results
#   are exhausted (already checking for empty lists if select retrieved
#   nothing
# - Fix bugs in test_setoutputsize_basic and test_setinputsizes
#

class TestDatabaseAPI20(base.TrioMySQLTestCase):
    ''' Test a database self.driver for DB API 2.0 compatibility.
        This implementation tests Gadfly, but the TestCase
        is structured so that other self.drivers can subclass this
        test case to ensure compiliance with the DB-API. It is
        expected that this TestCase may be expanded in the future
        if ambiguities or edge conditions are discovered.

        The 'Optional Extensions' are not yet being tested.

        self.drivers should subclass this test, overriding setUp, tearDown,
        self.driver, connect_args and connect_kw_args. Class specification
        should be as follows:

        import dbapi20
        class mytest(dbapi20.DatabaseAPI20Test):
           [...]

        Don't 'import DatabaseAPI20Test from dbapi20', or you will
        confuse the unit tester - just 'import dbapi20'.
    '''

    # The self.driver module. This should be the module where the 'connect'
    # method is to be found
    driver = None
    connect_args = () # List of arguments to pass to connect
    connect_kw_args = {} # Keyword arguments for connect
    table_prefix = 'dbapi20test_' # If you need to specify a prefix for tables

    ddl1 = 'create table %sbooze (name varchar(20))' % table_prefix
    ddl2 = 'create table %sbarflys (name varchar(20))' % table_prefix
    xddl1 = 'drop table %sbooze' % table_prefix
    xddl2 = 'drop table %sbarflys' % table_prefix

    lowerfunc = 'lower' # Name of stored procedure to convert string->lowercase

    # Some drivers may need to override these helpers, for example adding
    # a 'commit' after the execute.
    async def executeDDL1(self,cursor):
        await cursor.execute(self.ddl1)

    async def executeDDL2(self,cursor):
        await cursor.execute(self.ddl2)

    async def setUp(self):
        ''' self.drivers should override this method to perform required setup
            if any is necessary, such as creating the database.
        '''
        pass

    async def tearDown(self):
        ''' self.drivers should override this method to perform required cleanup
            if any is necessary, such as deleting the test database.
            The default drops the tables that may be created.
        '''
        con = await self._connect()
        try:
            cur = con.cursor()
            for ddl in (self.xddl1,self.xddl2):
                try:
                    await cur.execute(ddl)
                    await con.commit()
                except self.driver.Error:
                    # Assume table didn't exist. Other tests will check if
                    # execute is busted.
                    pass
        finally:
            await con.aclose()

    async def _connect(self):
        try:
            res = self.driver.connect(
                *self.connect_args,**self.connect_kw_args
                )
            await res.connect()
            return res
        except AttributeError:
            self.fail("No connect method found in self.driver module")

    @pytest.mark.trio
    async def test_connect(self, set_me_up):
        await set_me_up(self)
        con = await self._connect()
        await con.aclose()

    @pytest.mark.trio
    async def test_apilevel(self, set_me_up):
        await set_me_up(self)
        try:
            # Must exist
            apilevel = self.driver.apilevel
            # Must equal 2.0
            self.assertEqual(apilevel,'2.0')
        except AttributeError:
            self.fail("Driver doesn't define apilevel")

    @pytest.mark.trio
    async def test_threadsafety(self, set_me_up):
        await set_me_up(self)
        try:
            # Must exist
            threadsafety = self.driver.threadsafety
            # Must be a valid value
            self.assertTrue(threadsafety in (0,1,2,3))
        except AttributeError:
            self.fail("Driver doesn't define threadsafety")

    @pytest.mark.trio
    async def test_paramstyle(self, set_me_up):
        await set_me_up(self)
        try:
            # Must exist
            paramstyle = self.driver.paramstyle
            # Must be a valid value
            self.assertTrue(paramstyle in (
                'qmark','numeric','named','format','pyformat'
                ))
        except AttributeError:
            self.fail("Driver doesn't define paramstyle")

    @pytest.mark.trio
    async def test_Exceptions(self, set_me_up):
        await set_me_up(self)
        # Make sure required exceptions exist, and are in the
        # defined heirarchy.
        self.assertTrue(issubclass(self.driver.Warning,Exception))
        self.assertTrue(issubclass(self.driver.Error,Exception))
        self.assertTrue(
            issubclass(self.driver.InterfaceError,self.driver.Error)
            )
        self.assertTrue(
            issubclass(self.driver.DatabaseError,self.driver.Error)
            )
        self.assertTrue(
            issubclass(self.driver.OperationalError,self.driver.Error)
            )
        self.assertTrue(
            issubclass(self.driver.IntegrityError,self.driver.Error)
            )
        self.assertTrue(
            issubclass(self.driver.InternalError,self.driver.Error)
            )
        self.assertTrue(
            issubclass(self.driver.ProgrammingError,self.driver.Error)
            )
        self.assertTrue(
            issubclass(self.driver.NotSupportedError,self.driver.Error)
            )

    @pytest.mark.trio
    async def test_ExceptionsAsConnectionAttributes(self, set_me_up):
        await set_me_up(self)
        # OPTIONAL EXTENSION
        # Test for the optional DB API 2.0 extension, where the exceptions
        # are exposed as attributes on the Connection object
        # I figure this optional extension will be implemented by any
        # driver author who is using this test suite, so it is enabled
        # by default.
        con = await self._connect()
        drv = self.driver
        self.assertTrue(con.Warning is drv.Warning)
        self.assertTrue(con.Error is drv.Error)
        self.assertTrue(con.InterfaceError is drv.InterfaceError)
        self.assertTrue(con.DatabaseError is drv.DatabaseError)
        self.assertTrue(con.OperationalError is drv.OperationalError)
        self.assertTrue(con.IntegrityError is drv.IntegrityError)
        self.assertTrue(con.InternalError is drv.InternalError)
        self.assertTrue(con.ProgrammingError is drv.ProgrammingError)
        self.assertTrue(con.NotSupportedError is drv.NotSupportedError)


    @pytest.mark.trio
    async def test_commit(self, set_me_up):
        await set_me_up(self)
        con = await self._connect()
        try:
            # Commit must work, even if it doesn't do anything
            await con.commit()
        finally:
            await con.aclose()

    @pytest.mark.trio
    async def test_rollback(self, set_me_up):
        await set_me_up(self)
        con = await self._connect()
        # If rollback is defined, it should either work or throw
        # the documented exception
        if hasattr(con,'rollback'):
            try:
                await con.rollback()
            except self.driver.NotSupportedError:
                pass
        await con.aclose()

    @pytest.mark.trio
    async def test_cursor(self, set_me_up):
        await set_me_up(self)
        con = await self._connect()
        try:
            cur = con.cursor()
        finally:
            await con.aclose()

    @pytest.mark.trio
    async def test_cursor_isolation(self, set_me_up):
        await set_me_up(self)
        con = await self._connect()
        try:
            # Make sure cursors created from the same connection have
            # the documented transaction isolation level
            cur1 = con.cursor()
            cur2 = con.cursor()
            await self.executeDDL1(cur1)
            await cur1.execute("insert into %sbooze values ('Victoria Bitter')" % (
                self.table_prefix
                ))
            await cur2.execute("select name from %sbooze" % self.table_prefix)
            booze = await cur2.fetchall()
            self.assertEqual(len(booze),1)
            self.assertEqual(len(booze[0]),1)
            self.assertEqual(booze[0][0],'Victoria Bitter')
        finally:
            await con.aclose()

    @pytest.mark.trio
    async def test_description(self, set_me_up):
        await set_me_up(self)
        con = await self._connect()
        try:
            cur = con.cursor()
            await self.executeDDL1(cur)
            self.assertEqual(cur.description,None,
                'cursor.description should be none after executing a '
                'statement that can return no rows (such as DDL)'
                )
            await cur.execute('select name from %sbooze' % self.table_prefix)
            self.assertEqual(len(cur.description),1,
                'cursor.description describes too many columns'
                )
            self.assertEqual(len(cur.description[0]),7,
                'cursor.description[x] tuples must have 7 elements'
                )
            self.assertEqual(cur.description[0][0].lower(),'name',
                'cursor.description[x][0] must return column name'
                )
            self.assertEqual(cur.description[0][1],self.driver.STRING,
                'cursor.description[x][1] must return column type. Got %r'
                    % cur.description[0][1]
                )

            # Make sure self.description gets reset
            await self.executeDDL2(cur)
            self.assertEqual(cur.description,None,
                'cursor.description not being set to None when executing '
                'no-result statements (eg. DDL)'
                )
        finally:
            await con.aclose()

    @pytest.mark.trio
    async def test_rowcount(self, set_me_up):
        await set_me_up(self)
        con = await self._connect()
        try:
            cur = con.cursor()
            await self.executeDDL1(cur)
            self.assertEqual(cur.rowcount,-1,
                'cursor.rowcount should be -1 after executing no-result '
                'statements'
                )
            await cur.execute("insert into %sbooze values ('Victoria Bitter')" % (
                self.table_prefix
                ))
            self.assertTrue(cur.rowcount in (-1,1),
                'cursor.rowcount should == number or rows inserted, or '
                'set to -1 after executing an insert statement'
                )
            await cur.execute("select name from %sbooze" % self.table_prefix)
            self.assertTrue(cur.rowcount in (-1,1),
                'cursor.rowcount should == number of rows returned, or '
                'set to -1 after executing a select statement'
                )
            await self.executeDDL2(cur)
            self.assertEqual(cur.rowcount,-1,
                'cursor.rowcount not being reset to -1 after executing '
                'no-result statements'
                )
        finally:
            await con.aclose()

    lower_func = 'lower'
    @pytest.mark.trio
    async def test_callproc(self, set_me_up):
        await set_me_up(self)
        con = await self._connect()
        try:
            cur = con.cursor()
            if self.lower_func and hasattr(cur,'callproc'):
                r = await cur.callproc(self.lower_func,('FOO',))
                self.assertEqual(len(r),1)
                self.assertEqual(r[0],'FOO')
                r = await cur.fetchall()
                self.assertEqual(len(r),1,'callproc produced no result set')
                self.assertEqual(len(r[0]),1,
                    'callproc produced invalid result set'
                    )
                self.assertEqual(r[0][0],'foo',
                    'callproc produced invalid results'
                    )
        finally:
            await con.aclose()

    @pytest.mark.trio
    async def test_close(self, set_me_up):
        await set_me_up(self)
        con = await self._connect()
        try:
            cur = con.cursor()
        finally:
            await con.aclose()

        # cursor.execute should raise an Error if called after connection
        # closed
        with pytest.raises(self.driver.Error):
            await self.executeDDL1(cur)

        # connection.commit should raise an Error if called after connection'
        # closed.'
        with pytest.raises(self.driver.Error):
            await con.commit()

        # connection.close should raise an Error if called more than once
        # except that Trio doesn't do that, closing should be idempotent
        #with pytest.raises(self.driver.Error):
        #    await con.aclose()

    @pytest.mark.trio
    async def test_execute(self, set_me_up):
        await set_me_up(self)
        con = await self._connect()
        try:
            cur = con.cursor()
            await self._paraminsert(cur)
        finally:
            await con.aclose()

    async def _paraminsert(self,cur):
        await self.executeDDL1(cur)
        await cur.execute("insert into %sbooze values ('Victoria Bitter')" % (
            self.table_prefix
            ))
        self.assertTrue(cur.rowcount in (-1,1))

        if self.driver.paramstyle == 'qmark':
            await cur.execute(
                'insert into %sbooze values (?)' % self.table_prefix,
                ("Cooper's",)
                )
        elif self.driver.paramstyle == 'numeric':
            await cur.execute(
                'insert into %sbooze values (:1)' % self.table_prefix,
                ("Cooper's",)
                )
        elif self.driver.paramstyle == 'named':
            await cur.execute(
                'insert into %sbooze values (:beer)' % self.table_prefix,
                {'beer':"Cooper's"}
                )
        elif self.driver.paramstyle == 'format':
            await cur.execute(
                'insert into %sbooze values (%%s)' % self.table_prefix,
                ("Cooper's",)
                )
        elif self.driver.paramstyle == 'pyformat':
            await cur.execute(
                'insert into %sbooze values (%%(beer)s)' % self.table_prefix,
                {'beer':"Cooper's"}
                )
        else:
            self.fail('Invalid paramstyle')
        self.assertTrue(cur.rowcount in (-1,1))

        await cur.execute('select name from %sbooze' % self.table_prefix)
        res = await cur.fetchall()
        self.assertEqual(len(res),2,'cursor.fetchall returned too few rows')
        beers = [res[0][0],res[1][0]]
        beers.sort()
        self.assertEqual(beers[0],"Cooper's",
            'cursor.fetchall retrieved incorrect data, or data inserted '
            'incorrectly'
            )
        self.assertEqual(beers[1],"Victoria Bitter",
            'cursor.fetchall retrieved incorrect data, or data inserted '
            'incorrectly'
            )

    @pytest.mark.trio
    async def test_executemany(self, set_me_up):
        await set_me_up(self)
        con = await self._connect()
        try:
            cur = con.cursor()
            await self.executeDDL1(cur)
            largs = [ ("Cooper's",) , ("Boag's",) ]
            margs = [ {'beer': "Cooper's"}, {'beer': "Boag's"} ]
            if self.driver.paramstyle == 'qmark':
                await cur.executemany(
                    'insert into %sbooze values (?)' % self.table_prefix,
                    largs
                    )
            elif self.driver.paramstyle == 'numeric':
                await cur.executemany(
                    'insert into %sbooze values (:1)' % self.table_prefix,
                    largs
                    )
            elif self.driver.paramstyle == 'named':
                await cur.executemany(
                    'insert into %sbooze values (:beer)' % self.table_prefix,
                    margs
                    )
            elif self.driver.paramstyle == 'format':
                await cur.executemany(
                    'insert into %sbooze values (%%s)' % self.table_prefix,
                    largs
                    )
            elif self.driver.paramstyle == 'pyformat':
                await cur.executemany(
                    'insert into %sbooze values (%%(beer)s)' % (
                        self.table_prefix
                        ),
                    margs
                    )
            else:
                self.fail('Unknown paramstyle')
            self.assertTrue(cur.rowcount in (-1,2),
                'insert using cursor.executemany set cursor.rowcount to '
                'incorrect value %r' % cur.rowcount
                )
            await cur.execute('select name from %sbooze' % self.table_prefix)
            res = await cur.fetchall()
            self.assertEqual(len(res),2,
                'cursor.fetchall retrieved incorrect number of rows'
                )
            beers = [res[0][0],res[1][0]]
            beers.sort()
            self.assertEqual(beers[0],"Boag's",'incorrect data retrieved')
            self.assertEqual(beers[1],"Cooper's",'incorrect data retrieved')
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
            with pytest.raises(self.driver.Error):
                await cur.fetchone()

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
            with pytest.raises(self.driver.Error):
                await cur.fetchone()

            await cur.execute('select name from %sbooze' % self.table_prefix)
            r = await cur.fetchone()
            self.assertEqual(len(r),1,
                'cursor.fetchone should have retrieved a single row'
                )
            self.assertEqual(r[0],'Victoria Bitter',
                'cursor.fetchone retrieved incorrect data'
                )
            self.assertEqual(await cur.fetchone(),None,
                'cursor.fetchone should return None if no more rows available'
                )
            self.assertTrue(cur.rowcount in (-1,1))
        finally:
            await con.aclose()

    samples = [
        'Carlton Cold',
        'Carlton Draft',
        'Mountain Goat',
        'Redback',
        'Victoria Bitter',
        'XXXX'
        ]

    def _populate(self):
        ''' Return a list of sql commands to setup the DB for the fetch
            tests.
        '''
        populate = [
            "insert into %sbooze values ('%s')" % (self.table_prefix,s)
                for s in self.samples
            ]
        return populate

    @pytest.mark.trio
    async def test_fetchmany(self, set_me_up):
        await set_me_up(self)
        con = await self._connect()
        try:
            cur = con.cursor()

            # cursor.fetchmany should raise an Error if called without
            #issuing a query
            with pytest.raises(self.driver.Error):
                await cur.fetchmany(4)

            await self.executeDDL1(cur)
            for sql in self._populate():
                await cur.execute(sql)

            await cur.execute('select name from %sbooze' % self.table_prefix)
            r = await cur.fetchmany()
            self.assertEqual(len(r),1,
                'cursor.fetchmany retrieved incorrect number of rows, '
                'default of arraysize is one.'
                )
            cur.arraysize=10
            r = await cur.fetchmany(3) # Should get 3 rows
            self.assertEqual(len(r),3,
                'cursor.fetchmany retrieved incorrect number of rows'
                )
            r = await cur.fetchmany(4) # Should get 2 more
            self.assertEqual(len(r),2,
                'cursor.fetchmany retrieved incorrect number of rows'
                )
            r = await cur.fetchmany(4) # Should be an empty sequence
            self.assertEqual(len(r),0,
                'cursor.fetchmany should return an empty sequence after '
                'results are exhausted'
            )
            self.assertTrue(cur.rowcount in (-1,6))

            # Same as above, using cursor.arraysize
            cur.arraysize=4
            await cur.execute('select name from %sbooze' % self.table_prefix)
            r = await cur.fetchmany() # Should get 4 rows
            self.assertEqual(len(r),4,
                'cursor.arraysize not being honoured by fetchmany'
                )
            r = await cur.fetchmany() # Should get 2 more
            self.assertEqual(len(r),2)
            r = await cur.fetchmany() # Should be an empty sequence
            self.assertEqual(len(r),0)
            self.assertTrue(cur.rowcount in (-1,6))

            cur.arraysize=6
            await cur.execute('select name from %sbooze' % self.table_prefix)
            rows = await cur.fetchmany() # Should get all rows
            self.assertTrue(cur.rowcount in (-1,6))
            self.assertEqual(len(rows),6)
            self.assertEqual(len(rows),6)
            rows = [r[0] for r in rows]
            rows.sort()

            # Make sure we get the right data back out
            for i in range(0,6):
                self.assertEqual(rows[i],self.samples[i],
                    'incorrect data retrieved by cursor.fetchmany'
                    )

            rows = await cur.fetchmany() # Should return an empty list
            self.assertEqual(len(rows),0,
                'cursor.fetchmany should return an empty sequence if '
                'called after the whole result set has been fetched'
                )
            self.assertTrue(cur.rowcount in (-1,6))

            await self.executeDDL2(cur)
            await cur.execute('select name from %sbarflys' % self.table_prefix)
            r = await cur.fetchmany() # Should get empty sequence
            self.assertEqual(len(r),0,
                'cursor.fetchmany should return an empty sequence if '
                'query retrieved no rows'
                )
            self.assertTrue(cur.rowcount in (-1,0))

        finally:
            await con.aclose()

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
            with pytest.raises(self.driver.Error):
                await cur.fetchall()

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
    async def test_mixedfetch(self, set_me_up):
        await set_me_up(self)
        con = await self._connect()
        try:
            cur = con.cursor()
            await self.executeDDL1(cur)
            for sql in self._populate():
                await cur.execute(sql)

            await cur.execute('select name from %sbooze' % self.table_prefix)
            rows1  = await cur.fetchone()
            rows23 = await cur.fetchmany(2)
            rows4  = await cur.fetchone()
            rows56 = await cur.fetchall()
            self.assertTrue(cur.rowcount in (-1,6))
            self.assertEqual(len(rows23),2,
                'fetchmany returned incorrect number of rows'
                )
            self.assertEqual(len(rows56),2,
                'fetchall returned incorrect number of rows'
                )

            rows = [rows1[0]]
            rows.extend([rows23[0][0],rows23[1][0]])
            rows.append(rows4[0])
            rows.extend([rows56[0][0],rows56[1][0]])
            rows.sort()
            for i in range(0,len(self.samples)):
                self.assertEqual(rows[i],self.samples[i],
                    'incorrect data retrieved or inserted'
                    )
        finally:
            await con.aclose()

    def help_nextset_setUp(self,cur):
        ''' Should create a procedure called deleteme
            that returns two result sets, first the
            number of rows in booze then "name from booze"
        '''
        raise NotImplementedError('Helper not implemented')
        #sql="""
        #    create procedure deleteme as
        #    begin
        #        select count(*) from booze
        #        select name from booze
        #    end
        #"""
        #await cur.execute(sql)

    def help_nextset_tearDown(self,cur):
        'If cleaning up is needed after nextSetTest'
        raise NotImplementedError('Helper not implemented')
        #await cur.execute("drop procedure deleteme")

    @pytest.mark.trio
    async def test_nextset(self, set_me_up):
        await set_me_up(self)
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

                self.help_nextset_setUp(cur)

                await cur.callproc('deleteme')
                numberofrows=await cur.fetchone()
                assert numberofrows[0]== len(self.samples)
                assert await cur.nextset()
                names=await cur.fetchall()
                assert len(names) == len(self.samples)
                s=await cur.nextset()
                assert s == None,'No more return sets, should return None'
            finally:
                self.help_nextset_tearDown(cur)

        finally:
            await con.aclose()

    @pytest.mark.trio
    async def test_nextset(self, set_me_up):
        await set_me_up(self)
        raise NotImplementedError('Drivers need to override this test')

    @pytest.mark.trio
    async def test_arraysize(self, set_me_up):
        await set_me_up(self)
        # Not much here - rest of the tests for this are in test_fetchmany
        con = await self._connect()
        try:
            cur = con.cursor()
            self.assertTrue(hasattr(cur,'arraysize'),
                'cursor.arraysize must be defined'
                )
        finally:
            await con.aclose()

    @pytest.mark.trio
    async def test_setinputsizes(self, set_me_up):
        await set_me_up(self)
        con = await self._connect()
        try:
            cur = con.cursor()
            cur.setinputsizes( (25,) )
            await self._paraminsert(cur) # Make sure cursor still works
        finally:
            await con.aclose()

    @pytest.mark.trio
    async def test_setoutputsize_basic(self, set_me_up):
        await set_me_up(self)
        # Basic test is to make sure setoutputsize doesn't blow up
        con = await self._connect()
        try:
            cur = con.cursor()
            cur.setoutputsize(1000)
            cur.setoutputsize(2000,0)
            await self._paraminsert(cur) # Make sure the cursor still works
        finally:
            await con.aclose()

    @pytest.mark.trio
    async def test_setoutputsize(self, set_me_up):
        await set_me_up(self)
        # Real test for setoutputsize is driver dependant
        raise NotImplementedError('Driver need to override this test')

    @pytest.mark.trio
    async def test_None(self, set_me_up):
        await set_me_up(self)
        con = await self._connect()
        try:
            cur = con.cursor()
            await self.executeDDL1(cur)
            await cur.execute('insert into %sbooze values (NULL)' % self.table_prefix)
            await cur.execute('select name from %sbooze' % self.table_prefix)
            r = await cur.fetchall()
            self.assertEqual(len(r),1)
            self.assertEqual(len(r[0]),1)
            self.assertEqual(r[0][0],None,'NULL value not returned as None')
        finally:
            await con.aclose()

    @pytest.mark.trio
    async def test_Date(self, set_me_up):
        await set_me_up(self)
        d1 = self.driver.Date(2002,12,25)
        d2 = self.driver.DateFromTicks(time.mktime((2002,12,25,0,0,0,0,0,0)))
        # Can we assume this? API doesn't specify, but it seems implied
        # self.assertEqual(str(d1),str(d2))

    @pytest.mark.trio
    async def test_Time(self, set_me_up):
        await set_me_up(self)
        t1 = self.driver.Time(13,45,30)
        t2 = self.driver.TimeFromTicks(time.mktime((2001,1,1,13,45,30,0,0,0)))
        # Can we assume this? API doesn't specify, but it seems implied
        # self.assertEqual(str(t1),str(t2))

    @pytest.mark.trio
    async def test_Timestamp(self, set_me_up):
        await set_me_up(self)
        t1 = self.driver.Timestamp(2002,12,25,13,45,30)
        t2 = self.driver.TimestampFromTicks(
            time.mktime((2002,12,25,13,45,30,0,0,0))
            )
        # Can we assume this? API doesn't specify, but it seems implied
        # self.assertEqual(str(t1),str(t2))

    @pytest.mark.trio
    async def test_Binary(self, set_me_up):
        await set_me_up(self)
        b = self.driver.Binary(b'Something')
        b = self.driver.Binary(b'')

    @pytest.mark.trio
    async def test_STRING(self, set_me_up):
        await set_me_up(self)
        self.assertTrue(hasattr(self.driver,'STRING'),
            'module.STRING must be defined'
            )

    @pytest.mark.trio
    async def test_BINARY(self, set_me_up):
        await set_me_up(self)
        self.assertTrue(hasattr(self.driver,'BINARY'),
            'module.BINARY must be defined.'
            )

    @pytest.mark.trio
    async def test_NUMBER(self, set_me_up):
        await set_me_up(self)
        self.assertTrue(hasattr(self.driver,'NUMBER'),
            'module.NUMBER must be defined.'
            )

    @pytest.mark.trio
    async def test_DATETIME(self, set_me_up):
        await set_me_up(self)
        self.assertTrue(hasattr(self.driver,'DATETIME'),
            'module.DATETIME must be defined.'
            )

    @pytest.mark.trio
    async def test_ROWID(self, set_me_up):
        await set_me_up(self)
        self.assertTrue(hasattr(self.driver,'ROWID'),
            'module.ROWID must be defined.'
            )
