import os
import asyncio
import cognee
from dotenv import load_dotenv
load_dotenv()

async def prune_and_add_data():
    await cognee.prune.prune_data()
    await cognee.prune.prune_system(metadata=True)

    data_dir = os.path.join(os.path.dirname(__file__), "data")
    for filename in os.listdir(data_dir):
        if filename.endswith(".txt"):
            file_path = os.path.join(data_dir, filename)
            with open(file_path, "r") as f:
                content = f.read()
                await cognee.add(content)
    await cognee.cognify()

async def main():
    from cognee.api.v1.config import config
    
    config.data_root_directory(
        os.path.join(os.path.dirname(__file__), "../.cognee/data_storage")
    )

    config.system_root_directory(
        os.path.join(os.path.dirname(__file__), "../.cognee/system")
    )

    # await prune_and_add_data()
    result = await cognee.search("How many contracts do we have?")
    print(result)
    return

if __name__ == "__main__":
    asyncio.run(main())