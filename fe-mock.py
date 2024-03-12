import aiohttp
import asyncio
import time
import sys
import numpy as np

n = int(sys.argv[1]) if len(sys.argv) > 1 else 100

# Define your API endpoint
url = "http://localhost:8080/inference"

data = None
with open("./data/examples.fasta") as f:
    data = f.read()
    data = data.split(">")
    data = [d for d in data if d]
    data = [{ 'header': ">"+d.split("\n")[0], 'sequence': d.split("\n")[1] } for d in data]

# Create a list of JSON payloads
if not data:
    payloads = [
        {
            "header": ">EUKARYA",
            "sequence": "MAPTLFQKLFSKRTGLGAPGRDARDPDCGFSWPLPEFDPSQIRLIVYQDCERRGRNVLFDSSVKRRNEDI",
        }
        # Add more payloads as needed
    ]*n
else:
    payloads = np.random.choice(data, n)

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