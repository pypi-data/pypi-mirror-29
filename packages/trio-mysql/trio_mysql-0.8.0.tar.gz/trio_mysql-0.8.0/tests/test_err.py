import pytest

from trio_mysql import err
from tests import base


__all__ = ["TestRaiseException"]


class TestRaiseException(base.FakeUnittestcase):

    def test_raise_mysql_exception(self):
        data = b"\xff\x15\x04Access denied"
        with self.assertRaises(err.OperationalError) as cm:
            err.raise_mysql_exception(data)
        self.assertEqual(cm.value.args, (1045, 'Access denied'))

    def test_raise_mysql_exception_client_protocol_41(self):
        data = b"\xff\x15\x04#28000Access denied"
        with self.assertRaises(err.OperationalError) as cm:
            err.raise_mysql_exception(data)
        self.assertEqual(cm.value.args, (1045, 'Access denied'))
