from taskiq_redis import RedisStreamBroker

import asyncio
import dotenv
import os

dotenv.load_dotenv()

broker = RedisStreamBroker(url=os.getenv("REDIS_URL"))


@broker.task
async def work_hard(name: str):
    await asyncio.sleep(2)
    print(f"good job, {name}!")


if __name__ == "__main__":

    async def run():
        task = await work_hard.kiq("bro")
        print(task.task_id)

    asyncio.run(run())
