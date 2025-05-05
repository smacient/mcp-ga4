import asyncio
import os
import logging


from gemini_utilities.stdio_chat_loop import MCPClient

# current_dir = os.path.dirname(__file__)
# server_file_path = os.path.join(current_dir, "ga4_server.py")


async def test():
    print("Async event loop test passed!")


logging.basicConfig(level=logging.INFO)


async def handle_request_with_retry(client, retries=3, delay=5):
    # Resolve server file path dynamically
    server_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "ga4_server.py"))

    for attempt in range(retries):
        try:
            logging.info(f"Attempt {attempt + 1} to connect to server: {server_file_path}")
            await client.connect_to_server(server_file_path)
            logging.info("Connected successfully!")
            await client.chat_loop()
            return  # Exit once connected successfully
        except Exception as e:
            if "503" in str(e):
                logging.warning(f"Error: {e}. Retrying in {delay * (2 ** attempt)} seconds...")
                await asyncio.sleep(delay * (2 ** attempt))  # Exponential backoff
            else:
                logging.error(f"Critical error occurred: {e}")
                raise
    logging.error("All retry attempts failed. Please try again later.")


async def main():
    """Main function to start the MCP client."""
    print("Starting Gemini_client...")

    client = MCPClient()
    try:
        await handle_request_with_retry(client=client)
    except Exception as e:
        print(f"Error occurred during connection: {e}")
    finally:
        print("Cleaning up resources...")
        await client.clean_up()


if __name__ == "__main__":
    # run the function with asyncio event loop
    asyncio.run(test())

    asyncio.run(main())
    #  uv run localserver/gemini_client.py
    # acc 140900748
    # prop 256742771

