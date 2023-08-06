#!/usr/bin/env python
import trio
import trio_mysql

async def main():
    async with trio_mysql.connect(host='localhost', port=3306, user='root', passwd='', db='mysql') as conn:
        async with conn.cursor() as cur:

            await cur.execute("SELECT Host,User FROM user")
            print(cur.description)

            print()

            async for row in cur:
                print(row)

