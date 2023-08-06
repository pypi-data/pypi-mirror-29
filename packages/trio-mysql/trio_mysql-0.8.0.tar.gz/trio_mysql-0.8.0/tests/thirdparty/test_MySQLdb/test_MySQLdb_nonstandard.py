import pytest

import sys

import trio_mysql
_mysql = trio_mysql
from trio_mysql.constants import FIELD_TYPE
from tests import base


class TestDBAPISet(base.FakeUnittestcase):
    def test_set_equality(self):
        self.assertTrue(trio_mysql.STRING == trio_mysql.STRING)

    def test_set_inequality(self):
        self.assertTrue(trio_mysql.STRING != trio_mysql.NUMBER)

    def test_set_equality_membership(self):
        self.assertTrue(FIELD_TYPE.VAR_STRING == trio_mysql.STRING)

    def test_set_inequality_membership(self):
        self.assertTrue(FIELD_TYPE.DATE != trio_mysql.STRING)


class TestCoreModule(base.FakeUnittestcase):
    """Core _mysql module features."""

    async def test_NULL(self):
        """Should have a NULL constant."""
        self.assertEqual(_mysql.NULL, 'NULL')

    async def test_version(self):
        """Version information sanity."""
        self.assertTrue(isinstance(_mysql.__version__, str))

        self.assertTrue(isinstance(_mysql.version_info, tuple))
        self.assertEqual(len(_mysql.version_info), 5)

    async def test_client_info(self):
        self.assertTrue(isinstance(_mysql.get_client_info(), str))

    async def test_thread_safe(self):
        self.assertTrue(isinstance(_mysql.thread_safe(), int))


class TestCoreAPI(base.TrioMySQLTestCase):
    """Test _mysql interaction internals."""

    async def setUp(self):
        kwargs = base.TrioMySQLTestCase.databases[0].copy()
        kwargs["read_default_file"] = "~/.my.cnf"
        self.conn = _mysql.connect(**kwargs)
        await self.conn.connect()

    async def tearDown(self):
        await self.conn.aclose()

    @pytest.mark.skip("We don't think about threads")
    def test_thread_id(self):
        tid = self.conn.thread_id()
        self.assertTrue(isinstance(tid, int),
                        "thread_id didn't return an integral value.")

        self.assertRaises(TypeError, self.conn.thread_id, ('evil',),
                          "thread_id shouldn't accept arguments.")

    @pytest.mark.trio
    async def test_affected_rows(self, set_me_up):
        await set_me_up(self)
        self.assertEqual(self.conn.affected_rows(), 0,
                          "Should return 0 before we do anything.")


    #def test_debug(self):
        ## FIXME Only actually tests if you lack SUPER
        #self.assertRaises(trio_mysql.OperationalError,
                          #self.conn.dump_debug_info)

    @pytest.mark.trio
    async def test_charset_name(self, set_me_up):
        await set_me_up(self)
        self.assertTrue(isinstance(self.conn.character_set_name(), str),
                        "Should return a string.")

    @pytest.mark.trio
    async def test_host_info(self, set_me_up):
        await set_me_up(self)
        assert isinstance(self.conn.get_host_info(), str), "should return a string"

    @pytest.mark.trio
    async def test_proto_info(self, set_me_up):
        await set_me_up(self)
        self.assertTrue(isinstance(self.conn.get_proto_info(), int),
                        "Should return an int.")

    @pytest.mark.trio
    async def test_server_info(self, set_me_up):
        await set_me_up(self)
        if sys.version_info[0] == 2:
            self.assertTrue(isinstance(self.conn.get_server_info(), str),
                            "Should return an str.")
        else:
            self.assertTrue(isinstance(self.conn.get_server_info(), str),
                            "Should return an str.")
