import pytest

import warnings

from tests import base
import trio_mysql.cursors

class CursorTest(base.TrioMySQLTestCase):
    async def setUp(self):
        await super().setUp()

        conn = self.connections[0]
        await conn.connect()
        await self.safe_create_table(
            conn,
            "test", "create table test (data varchar(10))",
        )
        cursor = conn.cursor()
        await cursor.execute(
            "insert into test (data) values "
            "('row1'), ('row2'), ('row3'), ('row4'), ('row5')")
        await cursor.aclose()
        self.test_connection = trio_mysql.connect(**self.databases[0])
        await self.test_connection.connect()
        self.addCleanup(self.test_connection.aclose)

    @pytest.mark.trio
    async def test_cleanup_rows_unbuffered(self, set_me_up):
        await set_me_up(self)
        conn = self.test_connection
        cursor = conn.cursor(trio_mysql.cursors.SSCursor)

        await cursor.execute("select * from test as t1, test as t2")
        for counter, row in enumerate(cursor):
            if counter > 10:
                break

        del cursor
        self.safe_gc_collect()

        c2 = conn.cursor()

        await c2.execute("select 1")
        assert await c2.fetchone() == (1,)
        assert await c2.fetchone() is None

    @pytest.mark.trio
    async def test_cleanup_rows_buffered(self, set_me_up):
        await set_me_up(self)
        conn = self.test_connection
        cursor = conn.cursor(trio_mysql.cursors.Cursor)

        await cursor.execute("select * from test as t1, test as t2")
        for counter, row in enumerate(cursor):
            if counter > 10:
                break

        del cursor
        self.safe_gc_collect()

        c2 = conn.cursor()

        await c2.execute("select 1")

        assert await c2.fetchone() == (1,)
        assert await c2.fetchone() is None

    @pytest.mark.trio
    async def test_executemany(self, set_me_up):
        await set_me_up(self)
        conn = self.test_connection
        cursor = conn.cursor(trio_mysql.cursors.Cursor)

        m = trio_mysql.cursors.RE_INSERT_VALUES.match("INSERT INTO TEST (ID, NAME) VALUES (%s, %s)")
        self.assertIsNotNone(m, 'error parse %s')
        self.assertEqual(m.group(3), '', 'group 3 not blank, bug in RE_INSERT_VALUES?')

        m = trio_mysql.cursors.RE_INSERT_VALUES.match("INSERT INTO TEST (ID, NAME) VALUES (%(id)s, %(name)s)")
        self.assertIsNotNone(m, 'error parse %(name)s')
        self.assertEqual(m.group(3), '', 'group 3 not blank, bug in RE_INSERT_VALUES?')

        m = trio_mysql.cursors.RE_INSERT_VALUES.match("INSERT INTO TEST (ID, NAME) VALUES (%(id_name)s, %(name)s)")
        self.assertIsNotNone(m, 'error parse %(id_name)s')
        self.assertEqual(m.group(3), '', 'group 3 not blank, bug in RE_INSERT_VALUES?')

        m = trio_mysql.cursors.RE_INSERT_VALUES.match("INSERT INTO TEST (ID, NAME) VALUES (%(id_name)s, %(name)s) ON duplicate update")
        self.assertIsNotNone(m, 'error parse %(id_name)s')
        self.assertEqual(m.group(3), ' ON duplicate update', 'group 3 not ON duplicate update, bug in RE_INSERT_VALUES?')

        m = trio_mysql.cursors.RE_INSERT_VALUES.match("INSERT INTO bloup(foo, bar)VALUES(%s, %s)")
        assert m is not None

        # cursor._executed must bee "insert into test (data) values (0),(1),(2),(3),(4),(5),(6),(7),(8),(9)"
        # list args
        data = range(10)
        await cursor.executemany("insert into test (data) values (%s)", data)
        self.assertTrue(cursor._executed.endswith(b",(7),(8),(9)"), 'execute many with %s not in one query')

        # dict args
        data_dict = [{'data': i} for i in range(10)]
        await cursor.executemany("insert into test (data) values (%(data)s)", data_dict)
        self.assertTrue(cursor._executed.endswith(b",(7),(8),(9)"), 'execute many with %(data)s not in one query')

        # %% in column set
        await cursor.execute("""\
            CREATE TABLE percent_test (
                `A%` INTEGER,
                `B%` INTEGER)""")
        try:
            q = "INSERT INTO percent_test (`A%%`, `B%%`) VALUES (%s, %s)"
            self.assertIsNotNone(trio_mysql.cursors.RE_INSERT_VALUES.match(q))
            await cursor.executemany(q, [(3, 4), (5, 6)])
            self.assertTrue(cursor._executed.endswith(b"(3, 4),(5, 6)"), "executemany with %% not in one query")
        finally:
            await cursor.execute("DROP TABLE IF EXISTS percent_test")
