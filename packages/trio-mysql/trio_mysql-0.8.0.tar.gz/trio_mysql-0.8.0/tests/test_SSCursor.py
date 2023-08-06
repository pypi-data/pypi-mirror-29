import sys
import pytest

from tests import base
import trio_mysql.cursors

class TestSSCursor(base.TrioMySQLTestCase):
    @pytest.mark.trio
    async def test_SSCursor(self, set_me_up):
        await set_me_up(self)
        affected_rows = None # was: 18446744073709551615

        conn = self.connections[0]
        data = [
            ('America', '', 'America/Jamaica'),
            ('America', '', 'America/Los_Angeles'),
            ('America', '', 'America/Lima'),
            ('America', '', 'America/New_York'),
            ('America', '', 'America/Menominee'),
            ('America', '', 'America/Havana'),
            ('America', '', 'America/El_Salvador'),
            ('America', '', 'America/Costa_Rica'),
            ('America', '', 'America/Denver'),
            ('America', '', 'America/Detroit'),]

        try:
            cursor = conn.cursor(trio_mysql.cursors.SSCursor)

            # Create table
            await cursor.execute(('CREATE TABLE tz_data ('
                'region VARCHAR(64),'
                'zone VARCHAR(64),'
                'name VARCHAR(64))'))

            await conn.begin()
            # Test INSERT
            for i in data:
                await cursor.execute('INSERT INTO tz_data VALUES (%s, %s, %s)', i)
                self.assertEqual(conn.affected_rows(), 1, 'affected_rows does not match')
            await conn.commit()

            # Test fetchone()
            iter = 0
            await cursor.execute('SELECT * FROM tz_data')
            while True:
                row = await cursor.fetchone()
                if row is None:
                    break
                iter += 1

                # Test cursor.rowcount
                self.assertEqual(cursor.rowcount, affected_rows,
                    'cursor.rowcount != %s' % (str(affected_rows)))

                # Test cursor.rownumber
                self.assertEqual(cursor.rownumber, iter,
                    'cursor.rowcount != %s' % (str(iter)))

                # Test row came out the same as it went in
                self.assertEqual((row in data), True,
                    'Row not found in source data')

            # Test fetchall
            await cursor.execute('SELECT * FROM tz_data')
            self.assertEqual(len(await cursor.fetchall()), len(data),
                'fetchall failed. Number of rows does not match')

            # Test fetchmany
            await cursor.execute('SELECT * FROM tz_data')
            self.assertEqual(len(await cursor.fetchmany(2)), 2,
                'fetchmany failed. Number of rows does not match')

            # So MySQLdb won't throw "Commands out of sync"
            while True:
                res = await cursor.fetchone()
                if res is None:
                    break

            # Test update, affected_rows()
            await cursor.execute('UPDATE tz_data SET zone = %s', ['Foo'])
            await conn.commit()
            self.assertEqual(cursor.rowcount, len(data),
                'Update failed. affected_rows != %s' % (str(len(data))))

            # Test executemany
            await cursor.executemany('INSERT INTO tz_data VALUES (%s, %s, %s)', data)
            self.assertEqual(cursor.rowcount, len(data),
                'executemany failed. cursor.rowcount != %s' % (str(len(data))))

            # Test multiple datasets
            ## DOES NOT WORK
            if False:
                await cursor.execute('SELECT 1; SELECT 2; SELECT 3')
                self.assertListEqual(list(cursor), [(1, )])
                assert await cursor.nextset()
                self.assertListEqual(list(cursor), [(2, )])
                assert await cursor.nextset()
                self.assertListEqual(list(cursor), [(3, )])
                assert not await cursor.nextset()

        finally:
            await cursor.execute('DROP TABLE tz_data')
            await cursor.aclose()

__all__ = ["TestSSCursor"]

