# coding: utf-8
import datetime
import json
import time
import warnings

import pytest

from trio_mysql import util
import trio_mysql.cursors
from tests import base
from trio_mysql.err import ProgrammingError


__all__ = ["TestConversion", "TestCursor", "TestBulkInserts"]


class TestConversion(base.TrioMySQLTestCase):
    @pytest.mark.trio
    async def test_datatypes(self, set_me_up):
        await set_me_up(self)
        """ test every data type """
        conn = self.connections[0]
        c = conn.cursor()
        await c.execute("create table test_datatypes (b bit, i int, l bigint, f real, s varchar(32), u varchar(32), bb blob, d date, dt datetime, ts timestamp, td time, t time, st datetime)")
        try:
            # insert values

            v = (True, -3, 123456789012, 5.7, "hello'\" world", u"Espa\xc3\xb1ol", "binary\x00data".encode(conn.charset), datetime.date(1988,2,2), datetime.datetime(2014, 5, 15, 7, 45, 57), datetime.timedelta(5,6), datetime.time(16,32), time.localtime())
            await c.execute("insert into test_datatypes (b,i,l,f,s,u,bb,d,dt,td,t,st) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", v)
            await c.execute("select b,i,l,f,s,u,bb,d,dt,td,t,st from test_datatypes")
            r = await c.fetchone()
            self.assertEqual(util.int2byte(1), r[0])
            self.assertEqual(v[1:10], r[1:10])
            self.assertEqual(datetime.timedelta(0, 60 * (v[10].hour * 60 + v[10].minute)), r[10])
            self.assertEqual(datetime.datetime(*v[-1][:6]), r[-1])

            await c.execute("delete from test_datatypes")

            # check nulls
            await c.execute("insert into test_datatypes (b,i,l,f,s,u,bb,d,dt,td,t,st) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", [None] * 12)
            await c.execute("select b,i,l,f,s,u,bb,d,dt,td,t,st from test_datatypes")
            r = await c.fetchone()
            self.assertEqual(tuple([None] * 12), r)

            await c.execute("delete from test_datatypes")

            # check sequences type
            for seq_type in (tuple, list, set, frozenset):
                await c.execute("insert into test_datatypes (i, l) values (2,4), (6,8), (10,12)")
                seq = seq_type([2,6])
                await c.execute("select l from test_datatypes where i in %s order by i", (seq,))
                r = await c.fetchall()
                self.assertEqual(((4,),(8,)), r)
                await c.execute("delete from test_datatypes")

        finally:
            await c.execute("drop table test_datatypes")

    @pytest.mark.trio
    async def test_dict(self, set_me_up):
        await set_me_up(self)
        """ test dict escaping """
        conn = self.connections[0]
        c = conn.cursor()
        await c.execute("create table test_dict (a integer, b integer, c integer)")
        try:
            await c.execute("insert into test_dict (a,b,c) values (%(a)s, %(b)s, %(c)s)", {"a":1,"b":2,"c":3})
            await c.execute("select a,b,c from test_dict")
            self.assertEqual((1,2,3), await c.fetchone())
        finally:
            await c.execute("drop table test_dict")

    @pytest.mark.trio
    async def test_string(self, set_me_up):
        await set_me_up(self)
        conn = self.connections[0]
        c = conn.cursor()
        await c.execute("create table test_dict (a text)")
        test_value = "I am a test string"
        try:
            await c.execute("insert into test_dict (a) values (%s)", test_value)
            await c.execute("select a from test_dict")
            self.assertEqual((test_value,), await c.fetchone())
        finally:
            await c.execute("drop table test_dict")

    @pytest.mark.trio
    async def test_integer(self, set_me_up):
        await set_me_up(self)
        conn = self.connections[0]
        c = conn.cursor()
        await c.execute("create table test_dict (a integer)")
        test_value = 12345
        try:
            await c.execute("insert into test_dict (a) values (%s)", test_value)
            await c.execute("select a from test_dict")
            self.assertEqual((test_value,), await c.fetchone())
        finally:
            await c.execute("drop table test_dict")

    @pytest.mark.trio
    async def test_binary(self, set_me_up):
        await set_me_up(self)
        """test binary data"""
        data = bytes(bytearray(range(255)))
        conn = self.connections[0]
        await self.safe_create_table(
            conn, "test_binary", "create table test_binary (b binary(255))")

        async with conn.cursor() as c:
            await c.execute("insert into test_binary (b) values (%s)", (data,))
            await c.execute("select b from test_binary")
            self.assertEqual(data, (await c.fetchone())[0])

    @pytest.mark.trio
    async def test_blob(self, set_me_up):
        await set_me_up(self)
        """test blob data"""
        data = bytes(bytearray(range(256)) * 4)
        conn = self.connections[0]
        await self.safe_create_table(
            conn, "test_blob", "create table test_blob (b blob)")

        async with conn.cursor() as c:
            await c.execute("insert into test_blob (b) values (%s)", (data,))
            await c.execute("select b from test_blob")
            self.assertEqual(data, (await c.fetchone())[0])

    @pytest.mark.trio
    async def test_untyped(self, set_me_up):
        await set_me_up(self)
        """ test conversion of null, empty string """
        conn = self.connections[0]
        c = conn.cursor()
        await c.execute("select null,''")
        self.assertEqual((None,u''), await c.fetchone())
        await c.execute("select '',null")
        self.assertEqual((u'',None), await c.fetchone())

    @pytest.mark.trio
    async def test_timedelta(self, set_me_up):
        await set_me_up(self)
        """ test timedelta conversion """
        conn = self.connections[0]
        c = conn.cursor()
        await c.execute("select time('12:30'), time('23:12:59'), time('23:12:59.05100'), time('-12:30'), time('-23:12:59'), time('-23:12:59.05100'), time('-00:30')")
        self.assertEqual((datetime.timedelta(0, 45000),
                          datetime.timedelta(0, 83579),
                          datetime.timedelta(0, 83579, 51000),
                          -datetime.timedelta(0, 45000),
                          -datetime.timedelta(0, 83579),
                          -datetime.timedelta(0, 83579, 51000),
                          -datetime.timedelta(0, 1800)),
                         await c.fetchone())

    @pytest.mark.xfail(raises=base.SkipTest)
    @pytest.mark.trio
    async def test_datetime_microseconds(self, set_me_up):
        await set_me_up(self)
        """ test datetime conversion w microseconds"""

        conn = self.connections[0]
        if not self.mysql_server_is(conn, (5, 6, 4)):
            raise base.SkipTest("target backend does not support microseconds")
        c = conn.cursor()
        dt = datetime.datetime(2013, 11, 12, 9, 9, 9, 123450)
        await c.execute("create table test_datetime (id int, ts datetime(6))")
        try:
            await c.execute(
                "insert into test_datetime values (%s, %s)",
                (1, dt)
            )
            await c.execute("select ts from test_datetime")
            self.assertEqual((dt,), c.fetchone())
        finally:
            await c.execute("drop table test_datetime")


class TestCursor(base.TrioMySQLTestCase):
    # this test case does not work quite right yet, however,
    # we substitute in None for the erroneous field which is
    # compatible with the DB-API 2.0 spec and has not broken
    # any unit tests for anything we've tried.

    #def test_description(self):
    #    """ test description attribute """
    #    # result is from MySQLdb module
    #    r = (('Host', 254, 11, 60, 60, 0, 0),
    #         ('User', 254, 16, 16, 16, 0, 0),
    #         ('Password', 254, 41, 41, 41, 0, 0),
    #         ('Select_priv', 254, 1, 1, 1, 0, 0),
    #         ('Insert_priv', 254, 1, 1, 1, 0, 0),
    #         ('Update_priv', 254, 1, 1, 1, 0, 0),
    #         ('Delete_priv', 254, 1, 1, 1, 0, 0),
    #         ('Create_priv', 254, 1, 1, 1, 0, 0),
    #         ('Drop_priv', 254, 1, 1, 1, 0, 0),
    #         ('Reload_priv', 254, 1, 1, 1, 0, 0),
    #         ('Shutdown_priv', 254, 1, 1, 1, 0, 0),
    #         ('Process_priv', 254, 1, 1, 1, 0, 0),
    #         ('File_priv', 254, 1, 1, 1, 0, 0),
    #         ('Grant_priv', 254, 1, 1, 1, 0, 0),
    #         ('References_priv', 254, 1, 1, 1, 0, 0),
    #         ('Index_priv', 254, 1, 1, 1, 0, 0),
    #         ('Alter_priv', 254, 1, 1, 1, 0, 0),
    #         ('Show_db_priv', 254, 1, 1, 1, 0, 0),
    #         ('Super_priv', 254, 1, 1, 1, 0, 0),
    #         ('Create_tmp_table_priv', 254, 1, 1, 1, 0, 0),
    #         ('Lock_tables_priv', 254, 1, 1, 1, 0, 0),
    #         ('Execute_priv', 254, 1, 1, 1, 0, 0),
    #         ('Repl_slave_priv', 254, 1, 1, 1, 0, 0),
    #         ('Repl_client_priv', 254, 1, 1, 1, 0, 0),
    #         ('Create_view_priv', 254, 1, 1, 1, 0, 0),
    #         ('Show_view_priv', 254, 1, 1, 1, 0, 0),
    #         ('Create_routine_priv', 254, 1, 1, 1, 0, 0),
    #         ('Alter_routine_priv', 254, 1, 1, 1, 0, 0),
    #         ('Create_user_priv', 254, 1, 1, 1, 0, 0),
    #         ('Event_priv', 254, 1, 1, 1, 0, 0),
    #         ('Trigger_priv', 254, 1, 1, 1, 0, 0),
    #         ('ssl_type', 254, 0, 9, 9, 0, 0),
    #         ('ssl_cipher', 252, 0, 65535, 65535, 0, 0),
    #         ('x509_issuer', 252, 0, 65535, 65535, 0, 0),
    #         ('x509_subject', 252, 0, 65535, 65535, 0, 0),
    #         ('max_questions', 3, 1, 11, 11, 0, 0),
    #         ('max_updates', 3, 1, 11, 11, 0, 0),
    #         ('max_connections', 3, 1, 11, 11, 0, 0),
    #         ('max_user_connections', 3, 1, 11, 11, 0, 0))
    #    conn = self.connections[0]
    #    c = conn.cursor()
    #    await c.execute("select * from mysql.user")
    #
    #    self.assertEqual(r, c.description)

    @pytest.mark.trio
    async def test_fetch_no_result(self, set_me_up):
        await set_me_up(self)
        """ test a fetchone() with no rows """
        conn = self.connections[0]
        c = conn.cursor()
        await c.execute("create table test_nr (b varchar(32))")
        try:
            data = "trio_mysql"
            await c.execute("insert into test_nr (b) values (%s)", (data,))
            self.assertEqual(None, await c.fetchone())
        finally:
            await c.execute("drop table test_nr")

    @pytest.mark.trio
    async def test_aggregates(self, set_me_up):
        await set_me_up(self)
        """ test aggregate functions """
        conn = self.connections[0]
        c = conn.cursor()
        try:
            await c.execute('create table test_aggregates (i integer)')
            for i in range(0, 10):
                await c.execute('insert into test_aggregates (i) values (%s)', (i,))
            await c.execute('select sum(i) from test_aggregates')
            r, = await c.fetchone()
            self.assertEqual(sum(range(0,10)), r)
        finally:
            await c.execute('drop table test_aggregates')

    @pytest.mark.trio
    async def test_single_tuple(self, set_me_up):
        await set_me_up(self)
        """ test a single tuple """
        conn = self.connections[0]
        c = conn.cursor()
        await self.safe_create_table(
            conn, 'mystuff',
            "create table mystuff (id integer primary key)")
        await c.execute("insert into mystuff (id) values (1)")
        await c.execute("insert into mystuff (id) values (2)")
        await c.execute("select id from mystuff where id in %s", ((1,),))
        self.assertEqual([(1,)], list(await c.fetchall()))
        await c.aclose()

    @pytest.mark.xfail(raises=base.SkipTest)
    @pytest.mark.trio
    async def test_json(self, set_me_up):
        await set_me_up(self)
        args = self.databases[0].copy()
        args["charset"] = "utf8mb4"
        conn = trio_mysql.connect(**args)
        await conn.connect()
        if not self.mysql_server_is(conn, (5, 7, 0)):
            raise base.SkipTest("JSON type is not supported on MySQL <= 5.6")

        await self.safe_create_table(conn, "test_json", """\
create table test_json (
    id int not null,
    json JSON not null,
    primary key (id)
);""")
        cur = conn.cursor()

        json_str = u'{"hello": "こんにちは"}'
        await cur.execute("INSERT INTO test_json (id, `json`) values (42, %s)", (json_str,))
        await cur.execute("SELECT `json` from `test_json` WHERE `id`=42")
        res = (await cur.fetchone())[0]
        self.assertEqual(json.loads(res), json.loads(json_str))

        await cur.execute("SELECT CAST(%s AS JSON) AS x", (json_str,))
        res = (await cur.fetchone())[0]
        self.assertEqual(json.loads(res), json.loads(json_str))
        await conn.aclose()


class TestBulkInserts(base.TrioMySQLTestCase):

    cursor_type = trio_mysql.cursors.DictCursor

    async def setUp(self):
        await super().setUp()
        self.conn = conn = self.connections[0]
        c = conn.cursor(self.cursor_type)

        # create a table ane some data to query
        await self.safe_create_table(conn, 'bulkinsert', """\
CREATE TABLE bulkinsert
(
id int(11),
name char(20),
age int,
height int,
PRIMARY KEY (id)
)
""")

    async def _verify_records(self, data):
        conn = self.connections[0]
        cursor = conn.cursor()
        await cursor.execute("SELECT id, name, age, height from bulkinsert")
        result = await cursor.fetchall()
        self.assertEqual(sorted(data), sorted(result))

    @pytest.mark.trio
    async def test_bulk_insert(self, set_me_up):
        await set_me_up(self)
        conn = self.connections[0]
        cursor = conn.cursor()

        data = [(0, "bob", 21, 123), (1, "jim", 56, 45), (2, "fred", 100, 180)]
        await cursor.executemany("insert into bulkinsert (id, name, age, height) "
                           "values (%s,%s,%s,%s)", data)
        self.assertEqual(
            cursor._last_executed, bytearray(
            b"insert into bulkinsert (id, name, age, height) values "
            b"(0,'bob',21,123),(1,'jim',56,45),(2,'fred',100,180)"))
        await cursor.execute('commit')
        await self._verify_records(data)

    @pytest.mark.trio
    async def test_bulk_insert_multiline_statement(self, set_me_up):
        await set_me_up(self)
        conn = self.connections[0]
        cursor = conn.cursor()
        data = [(0, "bob", 21, 123), (1, "jim", 56, 45), (2, "fred", 100, 180)]
        await cursor.executemany("""insert
into bulkinsert (id, name,
age, height)
values (%s,
%s , %s,
%s )
 """, data)
        self.assertEqual(cursor._last_executed.strip(), bytearray(b"""insert
into bulkinsert (id, name,
age, height)
values (0,
'bob' , 21,
123 ),(1,
'jim' , 56,
45 ),(2,
'fred' , 100,
180 )"""))
        await cursor.execute('commit')
        await self._verify_records(data)

    @pytest.mark.trio
    async def test_bulk_insert_single_record(self, set_me_up):
        await set_me_up(self)
        conn = self.connections[0]
        cursor = conn.cursor()
        data = [(0, "bob", 21, 123)]
        await cursor.executemany("insert into bulkinsert (id, name, age, height) "
                           "values (%s,%s,%s,%s)", data)
        await cursor.execute('commit')
        await self._verify_records(data)

    @pytest.mark.trio
    async def test_issue_288(self, set_me_up):
        await set_me_up(self)
        """executemany should work with "insert ... on update" """
        conn = self.connections[0]
        cursor = conn.cursor()
        data = [(0, "bob", 21, 123), (1, "jim", 56, 45), (2, "fred", 100, 180)]
        await cursor.executemany("""insert
into bulkinsert (id, name,
age, height)
values (%s,
%s , %s,
%s ) on duplicate key update
age = values(age)
 """, data)
        self.assertEqual(cursor._last_executed.strip(), bytearray(b"""insert
into bulkinsert (id, name,
age, height)
values (0,
'bob' , 21,
123 ),(1,
'jim' , 56,
45 ),(2,
'fred' , 100,
180 ) on duplicate key update
age = values(age)"""))
        await cursor.execute('commit')
        await self._verify_records(data)

    @pytest.mark.trio
    async def test_warnings(self, set_me_up):
        await set_me_up(self)
        con = self.connections[0]
        cur = con.cursor()
        with warnings.catch_warnings(record=True) as ws:
            warnings.simplefilter("always")
            await cur.execute("drop table if exists no_exists_table")
        self.assertEqual(len(ws), 1)
        self.assertEqual(ws[0].category, trio_mysql.Warning, vars(ws[0]))
        if u"no_exists_table" not in str(ws[0].message):
            self.fail("'no_exists_table' not in %s" % (str(ws[0].message),))
