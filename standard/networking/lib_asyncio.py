#!/usr/bin/env python3

# ASYNCIO
# From Python 3.4 but it dynamically changes

import asyncio
import shutil
import os

import aiohttp
import aiofiles
import requests

URLS = [
    'https://pl.wikipedia.org/wiki/Wiki',
    'https://docs.python.org/3/',
    'https://pypi.org/',
    'https://twitter.com/?lang=pl',
    'https://docs.aiohttp.org/en/stable/index.html',
    'https://www.google.com/',
]


async def get_and_save_async(url: str, session: aiohttp.ClientSession, i: int) -> None:
    async with session.get(url) as response:
        result = await response.text()

    async with aiofiles.open(f'trash/a{i}.txt', 'w') as file:
        await file.write(result)


async def run_async_version() -> None:
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*[get_and_save_async(url, session, i) for i, url in enumerate(URLS)])


# ------------------


def get_and_save_sync(url: str, session: requests.Session, i: int) -> None:
    result = session.get(url).text

    with open(f'trash/s{i}.txt', 'w') as file:
        file.write(result)


def run_sync_version() -> None:
    with requests.Session() as session:
        for i, url in enumerate(URLS):
            get_and_save_sync(url, session, i)


# --------------------


async def lock_test(secs: int, lock: asyncio.Lock) -> None:
    async with lock:
        print('IN CS', secs)
        await asyncio.sleep(secs)
        print('OUT CS', secs)


async def lock_version() -> None:
    lock = asyncio.Lock()
    await asyncio.gather(lock_test(4, lock), lock_test(8, lock))


if __name__ == "__main__":
    import time

    if not os.path.isdir('trash'):
        os.makedirs('trash')

    start = time.perf_counter()
    asyncio.run(run_async_version())
    elapsed = time.perf_counter() - start
    print(f"Async completed in {elapsed:0.3f} seconds.")

    start = time.perf_counter()
    run_sync_version()
    elapsed = time.perf_counter() - start
    print(f"Sync completed in {elapsed:0.3f} seconds.")

    asyncio.run(lock_version())

    # Clean trash
    shutil.rmtree('./trash/')
    os.makedirs('trash')
