import asyncio
import aiohttp
from aiohttp import ClientSession
import json
from typing import List, Optional

# List of API URLs
api_urls: List[str] = [
    "https://api.example.com/endpoint1",
    "https://api.example.com/endpoint2",
    # ... add all 100,000 URLs here
]

CONCURRENT_REQUESTS = 100
BATCH_SIZE = 500
OUTPUT_FILE = "responses.json"

# Function to perform an API call
async def fetch(session: ClientSession, url: str) -> Optional[str]:
    try:
        async with session.get(url) as response:
            return await response.text()
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

# Main function to manage API calls
async def run(urls: List[str]) -> None:
    tasks: List[asyncio.Task] = []
    sem = asyncio.Semaphore(CONCURRENT_REQUESTS)
    responses: List[Optional[str]] = []

    async with ClientSession() as session:
        for idx, url in enumerate(urls):
            task = asyncio.create_task(bound_fetch(sem, session, url, responses))
            tasks.append(task)

            # Process responses in batches
            if (idx + 1) % BATCH_SIZE == 0:
                await asyncio.gather(*tasks)
                write_responses_to_file(responses)
                responses.clear()
                tasks = []

        # Process any remaining tasks
        if tasks:
            await asyncio.gather(*tasks)
            write_responses_to_file(responses)
            responses.clear()

# Function to write responses to a file
def write_responses_to_file(responses: List[Optional[str]]) -> None:
    with open(OUTPUT_FILE, "a") as file:
        for response in responses:
            if response is not None:
                file.write(json.dumps(response) + "\n")

# Function to limit concurrent connections
async def bound_fetch(sem: asyncio.Semaphore, session: ClientSession, url: str, responses: List[Optional[str]]) -> None:
    async with sem:
        response = await fetch(session, url)
        if response is not None:
            responses.append(response)

# Execute the API calls
if __name__ == "__main__":
    asyncio.run(run(api_urls))
