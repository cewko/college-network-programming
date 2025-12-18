import asyncio
import random


async def async_worker(task_id: int) -> None:
    work_time = random.uniform(0.1, 3)

    print(f"Task {task_id} started.")

    try:
        await asyncio.sleep(work_time)
        print(f"Task {task_id} finished after {work_time:.2f} secs")
    except asyncio.CancelledError:
        print(f"Task {task_id} failed due to timeout ({work_time:.2f} secs)")
        raise


async def run_with_timeout(task_number: int = 5, timeout: float = 2) -> None:
    tasks = [async_worker(i) for i in range(1, task_number + 1)]
    all_tasks = asyncio.gather(*tasks, return_exceptions=True)

    try:
        await asyncio.wait_for(all_tasks, timeout=timeout)
        print("All tasks have been successfully completed")
    except asyncio.TimeoutError:
        print(f"Timeout")
        all_tasks.cancel()

        try:
            await all_tasks
        except asyncio.CancelledError:
            pass

    
async def main():
    await run_with_timeout()


if __name__ == "__main__":
    asyncio.run(main())
