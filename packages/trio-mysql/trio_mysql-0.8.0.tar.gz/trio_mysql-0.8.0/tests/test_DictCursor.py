from tests import base
import trio_mysql.cursors
import pytest

import datetime
import warnings


class TestDictCursor(base.TrioMySQLTestCase):
    bob = {'name': 'bob', 'age': 21, 'DOB': datetime.datetime(1990, 2, 6, 23, 4, 56)}
    jim = {'name': 'jim', 'age': 56, 'DOB': datetime.datetime(1955, 5, 9, 13, 12, 45)}
    fred = {'name': 'fred', 'age': 100, 'DOB': datetime.datetime(1911, 9, 12, 1, 1, 1)}

    cursor_type = trio_mysql.cursors.DictCursor
    conn = None

    async def setUp(self):
        await super().setUp()
        self.conn = conn = self.connections[0]
        c = conn.cursor(self.cursor_type)

        # create a table ane some data to query
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore")
            await c.execute("drop table if exists dictcursor")
            # include in filterwarnings since for unbuffered dict cursor warning for lack of table
            # will only be propagated at start of next execute() call
            await c.execute("""CREATE TABLE dictcursor (name char(20), age int , DOB datetime)""")
        data = [("bob", 21, "1990-02-06 23:04:56"),
                ("jim", 56, "1955-05-09 13:12:45"),
                ("fred", 100, "1911-09-12 01:01:01")]
        await c.executemany("insert into dictcursor values (%s,%s,%s)", data)

    async def tearDown(self):
        if self.conn is not None:
            async with self.conn.cursor() as c:
                await c.execute("drop table dictcursor")
        await super().tearDown()

    async def _ensure_cursor_expired(self, cursor):
        pass

    @pytest.mark.trio
    async def test_DictCursor(self, set_me_up):
        await set_me_up(self)
        bob, jim, fred = self.bob.copy(), self.jim.copy(), self.fred.copy()
        #all assert test compare to the structure as would come out from MySQLdb
        conn = self.conn
        c = conn.cursor(self.cursor_type)

        # try an update which should return no rows
        await c.execute("update dictcursor set age=20 where name='bob'")
        bob['age'] = 20
        # pull back the single row dict for bob and check
        await c.execute("SELECT * from dictcursor where name='bob'")
        r = await c.fetchone()
        self.assertEqual(bob, r, "fetchone via DictCursor failed")
        await self._ensure_cursor_expired(c)

        # same again, but via fetchall => tuple)
        await c.execute("SELECT * from dictcursor where name='bob'")
        r = await c.fetchall()
        self.assertEqual([bob], r, "fetch a 1 row result via fetchall failed via DictCursor")
        # same test again but iterate over the
        await c.execute("SELECT * from dictcursor where name='bob'")
        async for r in c:
            self.assertEqual(bob, r, "fetch a 1 row result via iteration failed via DictCursor")
        # get all 3 row via fetchall
        await c.execute("SELECT * from dictcursor")
        r = await c.fetchall()
        self.assertEqual([bob,jim,fred], r, "fetchall failed via DictCursor")
        #same test again but do a list comprehension
        await c.execute("SELECT * from dictcursor")
        r = []
        async for res in c:
            r.append(res)
        self.assertEqual([bob,jim,fred], r, "DictCursor should be iterable")
        # get all 2 row via fetchmany
        await c.execute("SELECT * from dictcursor")
        r = await c.fetchmany(2)
        self.assertEqual([bob, jim], r, "fetchmany failed via DictCursor")
        await self._ensure_cursor_expired(c)

    @pytest.mark.trio
    async def test_custom_dict(self, set_me_up):
        await set_me_up(self)
        class MyDict(dict): pass

        class MyDictCursor(self.cursor_type):
            dict_type = MyDict

        keys = ['name', 'age', 'DOB']
        bob = MyDict([(k, self.bob[k]) for k in keys])
        jim = MyDict([(k, self.jim[k]) for k in keys])
        fred = MyDict([(k, self.fred[k]) for k in keys])

        cur = self.conn.cursor(MyDictCursor)
        await cur.execute("SELECT * FROM dictcursor WHERE name='bob'")
        r = await cur.fetchone()
        self.assertEqual(bob, r, "fetchone() returns MyDictCursor")
        await self._ensure_cursor_expired(cur)

        await cur.execute("SELECT * FROM dictcursor")
        r = await cur.fetchall()
        self.assertEqual([bob, jim, fred], r,
                         "fetchall failed via MyDictCursor")

        await cur.execute("SELECT * FROM dictcursor")
        r = []
        async for res in cur:
            r.append(res)
        self.assertEqual([bob, jim, fred], r,
                         "list failed via MyDictCursor")

        await cur.execute("SELECT * FROM dictcursor")
        r = await cur.fetchmany(2)
        self.assertEqual([bob, jim], r,
                         "list failed via MyDictCursor")
        await self._ensure_cursor_expired(cur)


class TestSSDictCursor(TestDictCursor):
    cursor_type = trio_mysql.cursors.SSDictCursor

    async def _ensure_cursor_expired(self, cursor):
        await cursor.fetchall()

