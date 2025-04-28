import asyncio
import nest_asyncio
from mcp import ClientSession
from mcp.client.sse import sse_client

nest_asyncio.apply()  # Needed to run interactive python sessions

"""
Make sure:
1. The server is running before running this script.
2. The server is configured to use SSE transport.
3. The server is listening on port 8000.

To run the server:
uv run cloud-server.py
"""


async def main():
    # Connect to the server using SSE
    async with sse_client("http://localhost:8000/sse") as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            # Initialize the connection
            await session.initialize()

            # List available tools
            tools_result = await session.list_tools()
            print("Available tools:")
            for tool in tools_result.tools:
                print(f"  - {tool.name}: {tool.description}")

            while True:
                # Get user input for tool name
                tool_name = input("\nEnter the name of the tool you want to use (or 'exit' to quit): ")
                if tool_name.lower() in ["exit", "quit"]:
                    print("Ending the session...")
                    break

                # Fetch the expected input schema for the selected tool
                try:
                    tool_info = next((tool for tool in tools_result.tools if tool.name == tool_name), None)
                    if not tool_info:
                        print(f"Tool '{tool_name}' not found. Please try again.")
                        continue

                    print(f"\nExpected keys for '{tool_name}':")
                    for param in tool_info.input_schema.fields:
                        print(f"  - {param.name}: {param.description}")

                except Exception as e:
                    print(f"\nError fetching tool information for '{tool_name}': {e}")
                    continue

                # Get user input for arguments
                print("\nSpecify arguments for the tool (key=value, separated by commas):")
                args_input = input("Arguments: ")

                # Parse arguments into a dictionary
                try:
                    arguments = {}
                    if args_input.strip():
                        for pair in args_input.split(","):
                            key, value = pair.split("=")
                            arguments[key.strip()] = value.strip()

                    # Call the specified tool with provided arguments
                    result = await session.call_tool(tool_name, arguments=arguments)
                    print(f"\nTool Response:\n{result.content[0].text}")

                except Exception as e:
                    print(f"\nError calling tool '{tool_name}' with arguments: {arguments}")
                    print(f"Details: {e}")

if __name__ == "__main__":
    asyncio.run(main())
