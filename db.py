import aiopg
import os

pool = None


async def connect():
    global pool
    if not pool:
        dsn = os.getenv("DB_DSN")
        pool = await aiopg.create_pool(dsn)


async def disconn():
    if pool:
        pool.close()
        await pool.wait_closed()


if __name__ == "__main__":
    import asyncio
    import dotenv

    dotenv.load_dotenv()

    async def run():
        await connect()
        async with pool.acquire() as conn:
            curs = await conn.cursor()
            await curs.execute("SELECT 42")
            async for row in curs:
                print(row)
        await disconn()

    asyncio.run(run())
