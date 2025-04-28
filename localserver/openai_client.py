import asyncio
from langchain_openai import ChatOpenAI  # Import OpenAI integration
from mcp_use import MCPAgent, MCPClient
import os

from dotenv import load_dotenv
# Load environment variables from .env
load_dotenv()
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
# Ensure OpenAI key is loaded
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")


async def run_memory_chat():
    """Run a chat using MCPAgent's built-in conversation memory."""
    # Load environment variables for API keys
    # load_dotenv()
    # os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")  # Ensure OpenAI key is loaded

    # Config file path - change this to your config file if applicable
    config_file = "localserver/ga4_server.json"

    print(f"Using configuration file: {config_file}")

    # Ensure the file exists before proceeding
    if not os.path.exists(config_file):
        raise FileNotFoundError(f"Configuration file not found at: {config_file}")

    # config_file = os.getenv("GA4_CONFIG_PATH")

    print("Initializing chat...")

    # Create MCP client and agent with memory enabled
    client = MCPClient.from_config_file(config_file)
    llm = ChatOpenAI(model="gpt-4", temperature=0.7)  # Use OpenAI's GPT model

    # Create agent with memory_enabled=True
    agent = MCPAgent(
        llm=llm,
        client=client,
        max_steps=15,
        memory_enabled=True,  # Enable built-in conversation memory
    )

    try:
        # Main chat loop
        while True:
            # print guide
            print("\n===== Interactive MCP Chat =====")
            print("Type 'exit' or 'quit' to end the conversation")
            print("Type 'clear' to clear conversation history")
            print("==================================\n")
            # Get user input
            user_input = input("\nYou: ")

            # Check for exit command
            if user_input.lower() in ["exit", "quit"]:
                print("Ending conversation...")
                break

            # Check for clear history command
            if user_input.lower() == "clear":
                agent.clear_conversation_history()
                print("Conversation history cleared.")
                continue

            # Get response from agent
            print("\nAssistant: ", end="", flush=True)

            try:
                # Run the agent with the user input (memory handling is automatic)
                response = await agent.run(user_input)
                print(response)

            except Exception as e:
                print(f"\nError: {e}")

    finally:
        # Clean up
        if client and client.sessions:
            await client.close_all_sessions()

if __name__ == "__main__":
    asyncio.run(run_memory_chat())
