import os
import asyncio
import logging
import traceback

from openai_utilities.server_connect import MCPClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def test():
    print("Async event loop test passed!")


async def handle_request_with_retry(client, retries=3, delay=5):
    server_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "ga4_server.py"))

    if not os.path.exists(server_file_path):
        logger.error(f"Server file not found at {server_file_path}")
        return

    for attempt in range(retries):
        try:
            logger.info(f"Attempt {attempt + 1} to connect to server: {server_file_path}")
            await client.connect_to_server(server_file_path)
            logger.info("Connected successfully!")
            await client.run_agent()
            return
        except Exception as e:
            if "503" in str(e):
                logger.warning(f"Server error: {e}. Retrying in {delay * (2 ** attempt)} seconds...")
                await asyncio.sleep(delay * (2 ** attempt))  # Exponential backoff
            else:
                logger.error(f"Critical error: {e}")
                raise

    logger.error("All retry attempts failed. Please try again later.")


async def main():
    logger.info("Starting MCP client...")
    client = MCPClient()
    try:
        await handle_request_with_retry(client)
    except Exception as e:
        logger.error(f"Unhandled error: {e}")
        traceback.print_exc()


if __name__ == "__main__":
    # run the function with asyncio event loop
    asyncio.run(test())

    asyncio.run(main())

    #  uv run localserver/openai_new.py localserver/ga4_server.py
    # 256742771
