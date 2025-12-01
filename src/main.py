import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from .discord_bot import run_bot
from .db import init_db

async def main():
    init_db()
    scheduler = AsyncIOScheduler()
    scheduler.start()
    await run_bot()

if __name__ == "__main__":
    asyncio.run(main())
