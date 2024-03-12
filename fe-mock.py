import aiohttp
import asyncio
import time

# Define your API endpoint
url = "http://localhost:8080/inference"

# Create a list of JSON payloads
payloads = [
    {
        "header": ">Q8TF40|EUKARYA|NO_SP|0",
        "sequence": "MAPTLFQKLFSKRTGLGAPGRDARDPDCGFSWPLPEFDPSQIRLIVYQDCERRGRNVLFDSSVKRRNEDI",
        "threshold": 0.6
    }
    # Add more payloads as needed
]*100

async def send_request(session, payload):
    start_time = time.time()
    async with session.post(url, json=payload) as response:
        elapsed_time = time.time() - start_time
        if response.status == 200:
            print(f"Request successful: {await response.text()} (Time: {elapsed_time:.2f} seconds)")
        else:
            print(f"Request failed with status code {response.status}: {await response.text()}")

async def main():
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*[send_request(session, payload) for payload in payloads])

if __name__ == "__main__":
    asyncio.run(main())