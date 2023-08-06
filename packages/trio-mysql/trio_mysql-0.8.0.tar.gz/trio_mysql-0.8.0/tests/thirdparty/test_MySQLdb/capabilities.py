""" Script to test database capabilities and the DB-API interface
    for functionality and memory leaks.

    Adapted from a script by M-A Lemburg.

"""
import sys
import pytest
from time import time
from tests import base

class DatabaseTest(base.TrioMySQLTestCase):

    db_module = None
    connect_args = ()
    connect_kwargs = dict(use_unicode=True, charset="utf8", binary_prefix=True)
    create_table_extra = "ENGINE=INNODB CHARACTER SET UTF8"
    rows = 10
    debug = False

    async def setUp(self):
        db = self.db_module.connect(*self.connect_args, **self.connect_kwargs)
        await db.connect()
        self.connection = db
        self.cursor = db.cursor()
        self.BLOBText = ''.join([chr(i) for i in range(256)] * 100);
        self.BLOBUText = "".join(chr(i) for i in range(16834))
        data = bytearray(range(256)) * 16
        self.BLOBBinary = self.db_module.Binary(data)

    leak_test = True

    async def tearDown(self):
        try:
            if self.leak_test:
                import gc
                del self.cursor
                orphans = gc.collect()
                self.assertFalse(orphans, "%d orphaned objects found after deleting cursor" % orphans)

                del self.connection
                orphans = gc.collect()
                self.assertFalse(orphans, "%d orphaned objects found after deleting connection" % orphans)
        finally:
            await self.connection.aclose()

    async def table_exists(self, name):
        try:
            await self.cursor.execute('select * from %s where 1=0' % name)
        except Exception:
            return False
        else:
            return True

    def quote_identifier(self, ident):
        return '"%s"' % ident

    async def new_table_name(self):
        i = id(self.cursor)
        while True:
            name = self.quote_identifier('tb%08x' % i)
            if not await self.table_exists(name):
                return name
            i = i + 1

    async def create_table(self, columndefs):

        """ Create a table using a list of column definitions given in
            columndefs.

            generator must be a function taking arguments (row_number,
            col_number) returning a suitable data object for insertion
            into the table.

        """
        self.table = await self.new_table_name()
        await self.cursor.execute('CREATE TABLE %s (%s) %s' %
                            (self.table,
                             ',\n'.join(columndefs),
                             self.create_table_extra))

    async def check_data_integrity(self, columndefs, generator):
        # insert
        await self.create_table(columndefs)
        insert_statement = ('INSERT INTO %s VALUES (%s)' %
                            (self.table,
                             ','.join(['%s'] * len(columndefs))))
        data = [ [ generator(i,j) for j in range(len(columndefs)) ]
                 for i in range(self.rows) ]
        if self.debug:
            print(data)
        await self.cursor.executemany(insert_statement, data)
        await self.connection.commit()
        # verify
        await self.cursor.execute('select * from %s' % self.table)
        l = await self.cursor.fetchall()
        if self.debug:
            print(l)
        self.assertEqual(len(l), self.rows)
        try:
            for i in range(self.rows):
                for j in range(len(columndefs)):
                    self.assertEqual(l[i][j], generator(i,j))
        finally:
            if not self.debug:
                await self.cursor.execute('drop table %s' % (self.table))

    @pytest.mark.trio
    async def test_transactions(self, set_me_up):
        await set_me_up(self)
        columndefs = ( 'col1 INT', 'col2 VARCHAR(255)')
        def generator(row, col):
            if col == 0: return row
            else: return ('%i' % (row%10))*255
        await self.create_table(columndefs)
        insert_statement = ('INSERT INTO %s VALUES (%s)' %
                            (self.table,
                             ','.join(['%s'] * len(columndefs))))
        data = [ [ generator(i,j) for j in range(len(columndefs)) ]
                 for i in range(self.rows) ]
        await self.cursor.executemany(insert_statement, data)
        # verify
        await self.connection.commit()
        await self.cursor.execute('select * from %s' % self.table)
        l = await self.cursor.fetchall()
        self.assertEqual(len(l), self.rows)
        for i in range(self.rows):
            for j in range(len(columndefs)):
                self.assertEqual(l[i][j], generator(i,j))
        delete_statement = 'delete from %s where col1=%%s' % self.table
        await self.cursor.execute(delete_statement, (0,))
        await self.cursor.execute('select col1 from %s where col1=%s' % \
                            (self.table, 0))
        l = await self.cursor.fetchall()
        self.assertFalse(l, "DELETE didn't work")
        await self.connection.rollback()
        await self.cursor.execute('select col1 from %s where col1=%s' % \
                            (self.table, 0))
        l = await self.cursor.fetchall()
        self.assertTrue(len(l) == 1, "ROLLBACK didn't work")
        await self.cursor.execute('drop table %s' % (self.table))

    @pytest.mark.trio
    async def test_truncation(self, set_me_up):
        await set_me_up(self)
        columndefs = ( 'col1 INT', 'col2 VARCHAR(255)')
        def generator(row, col):
            if col == 0: return row
            else: return ('%i' % (row%10))*((255-self.rows//2)+row)
        await self.create_table(columndefs)
        insert_statement = ('INSERT INTO %s VALUES (%s)' %
                            (self.table,
                             ','.join(['%s'] * len(columndefs))))

        try:
            await self.cursor.execute(insert_statement, (0, '0'*256))
        except Warning:
            if self.debug: print(self.cursor.messages)
        except self.connection.DataError:
            pass
        else:
            self.fail("Over-long column did not generate warnings/exception with single insert")

        await self.connection.rollback()

        try:
            for i in range(self.rows):
                data = []
                for j in range(len(columndefs)):
                    data.append(generator(i,j))
                await self.cursor.execute(insert_statement,tuple(data))
        except Warning:
            if self.debug: print(self.cursor.messages)
        except self.connection.DataError:
            pass
        else:
            self.fail("Over-long columns did not generate warnings/exception with execute()")

        await self.connection.rollback()

        try:
            data = [ [ generator(i,j) for j in range(len(columndefs)) ]
                     for i in range(self.rows) ]
            await self.cursor.executemany(insert_statement, data)
        except Warning:
            if self.debug: print(self.cursor.messages)
        except self.connection.DataError:
            pass
        else:
            self.fail("Over-long columns did not generate warnings/exception with executemany()")

        await self.connection.rollback()
        await self.cursor.execute('drop table %s' % (self.table))

    @pytest.mark.trio
    async def test_CHAR(self, set_me_up):
        await set_me_up(self)
        # Character data
        def generator(row,col):
            return ('%i' % ((row+col) % 10)) * 255
        await self.check_data_integrity(
            ('col1 char(255)','col2 char(255)'),
            generator)

    @pytest.mark.trio
    async def test_INT(self, set_me_up):
        await set_me_up(self)
        # Number data
        def generator(row,col):
            return row*row
        await self.check_data_integrity(
            ('col1 INT',),
            generator)

    @pytest.mark.trio
    async def test_DECIMAL(self, set_me_up):
        await set_me_up(self)
        # DECIMAL
        def generator(row,col):
            from decimal import Decimal
            return Decimal("%d.%02d" % (row, col))
        await self.check_data_integrity(
            ('col1 DECIMAL(5,2)',),
            generator)

    @pytest.mark.trio
    async def test_DATE(self, set_me_up):
        await set_me_up(self)
        ticks = time()
        def generator(row,col):
            return self.db_module.DateFromTicks(ticks+row*86400-col*1313)
        await self.check_data_integrity(
                 ('col1 DATE',),
                 generator)

    @pytest.mark.trio
    async def test_TIME(self, set_me_up):
        await set_me_up(self)
        ticks = time()
        def generator(row,col):
            return self.db_module.TimeFromTicks(ticks+row*86400-col*1313)
        await self.check_data_integrity(
                 ('col1 TIME',),
                 generator)

    @pytest.mark.trio
    async def test_DATETIME(self, set_me_up):
        await set_me_up(self)
        ticks = time()
        def generator(row,col):
            return self.db_module.TimestampFromTicks(ticks+row*86400-col*1313)
        await self.check_data_integrity(
                 ('col1 DATETIME',),
                 generator)

    @pytest.mark.trio
    async def test_TIMESTAMP(self, set_me_up):
        await set_me_up(self)
        ticks = time()
        def generator(row,col):
            return self.db_module.TimestampFromTicks(ticks+row*86400-col*1313)
        await self.check_data_integrity(
                 ('col1 TIMESTAMP',),
                 generator)

    @pytest.mark.trio
    async def test_fractional_TIMESTAMP(self, set_me_up):
        await set_me_up(self)
        ticks = time()
        def generator(row,col):
            return self.db_module.TimestampFromTicks(ticks+row*86400-col*1313+row*0.7*col/3.0)
        await self.check_data_integrity(
                 ('col1 TIMESTAMP',),
                 generator)

    @pytest.mark.trio
    async def test_LONG(self, set_me_up):
        await set_me_up(self)
        def generator(row,col):
            if col == 0:
                return row
            else:
                return self.BLOBUText # 'BLOB Text ' * 1024
        await self.check_data_integrity(
                 ('col1 INT', 'col2 LONG'),
                 generator)

    @pytest.mark.trio
    async def test_TEXT(self, set_me_up):
        await set_me_up(self)
        def generator(row,col):
            if col == 0:
                return row
            else:
                return self.BLOBUText[:5192] # 'BLOB Text ' * 1024
        await self.check_data_integrity(
                 ('col1 INT', 'col2 TEXT'),
                 generator)

    @pytest.mark.trio
    async def test_LONG_BYTE(self, set_me_up):
        await set_me_up(self)
        def generator(row,col):
            if col == 0:
                return row
            else:
                return self.BLOBBinary # 'BLOB\000Binary ' * 1024
        await self.check_data_integrity(
                 ('col1 INT','col2 LONG BYTE'),
                 generator)

    @pytest.mark.trio
    async def test_BLOB(self, set_me_up):
        await set_me_up(self)
        def generator(row,col):
            if col == 0:
                return row
            else:
                return self.BLOBBinary # 'BLOB\000Binary ' * 1024
        await self.check_data_integrity(
                 ('col1 INT','col2 BLOB'),
                 generator)
