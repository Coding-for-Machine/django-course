import os
from dotenv import load_dotenv
import asyncio
from lessons.models import TestCase
import aiohttp
# .env faylini yuklash
load_dotenv()

DOCKER_API = os.getenv("DOCKER_BACKEND_API")

async def format_code_push(user_code, test_case):
    if user_code and test_case:



