import asyncio
import nest_asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

nest_asyncio.apply()  # Needed to run interactive Python sessions


async def main():
    # Define server parameters
    server_params = StdioServerParameters(
        command="python",  # The command to run your server
        args=["server.py"],  # Arguments to the command
    )
    try:
        # Connect to the server
        async with stdio_client(server_params) as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as session:
                # Initialize the connection
                await session.initialize()

                # List available tools
                tools_result = await session.list_tools()
                print("Available tools:")
                for tool in tools_result.tools:
                    print(f"  - {tool.name}: {tool.description}")

                # Loop for user interaction
                while True:
                    # Get the tool name from the user
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

    except Exception as e:
        print(f"Unable to connect to server: {e}")

if __name__ == "__main__":
    asyncio.run(main())
