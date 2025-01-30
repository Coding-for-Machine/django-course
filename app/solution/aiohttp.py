import aiohttp
import asyncio


API_URL = ""

"""
data = {
    "code": "def add():",
    "language": "python"
}
"""
async def post_code(url: str,  data=None):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data) as response:
            if response.status==200:
                return await respone.json()
            else:
                return await resonse.status, response.text



if __name__ in "__main__":
    asyncio.run(post_code(API_URL))
