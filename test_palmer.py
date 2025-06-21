import asyncio
from src.palmer_ai.core import PalmerAICore

async def main():
    palmer = PalmerAICore()
    result = await palmer.analyze_with_love({"name": "Test Company"})
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
