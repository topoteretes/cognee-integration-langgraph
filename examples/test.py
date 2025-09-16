import os
import asyncio
import cognee
from dotenv import load_dotenv

load_dotenv()

async def main():
    from cognee.api.v1.config import config
    
    config.data_root_directory(
        os.path.join(os.path.dirname(__file__), "../.cognee/data_storage")
    )

    config.system_root_directory(
        os.path.join(os.path.dirname(__file__), "../.cognee/system")
    )

    await cognee.add("Virtus Pro is a software development company that specializes in building custom software solutions for businesses.")
    await cognee.cognify()

    await cognee.visualize_graph()
    return

if __name__ == "__main__":
    asyncio.run(main())