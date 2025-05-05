import os
import logging
from dotenv import load_dotenv
from typing import Optional

from aioconsole import ainput

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.messages import AIMessage, HumanMessage

from openai_utilities.system_input import system_instruction

# Load environment variables
load_dotenv()
logger = logging.getLogger(__name__)


class MCPClient:
    def __init__(self):
        self.session: Optional[ClientSession] = None
        self.server_params: Optional[StdioServerParameters] = None
        self.sys_query: str = system_instruction

        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            raise ValueError("OPENAI_API_KEY not found. Please add it to your .env file.")

        self.llm = ChatOpenAI(
            model="gpt-4o",
            temperature=0.0,
            max_retries=2,
            api_key=openai_api_key
        )

    async def connect_to_server(self, server_file_path: str):
        command = "python" if server_file_path.endswith(".py") else "node"
        logger.info(f"Using command: {command} for server: {server_file_path}")
        self.server_params = StdioServerParameters(command=command, args=[server_file_path])

    def build_agent_executor(self, tools):
        """Use an AgentExecutor instead of direct LangGraph for simpler setup"""
        # Create prompt
        prompt = ChatPromptTemplate.from_messages([
            ("system", self.sys_query),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        # Create agent
        agent = create_tool_calling_agent(self.llm, tools, prompt)
        
        # Create executor
        agent_executor = AgentExecutor(
            agent=agent,
            tools=tools,
            verbose=True,
            return_intermediate_steps=True
        )
        
        return agent_executor

    async def run_agent(self):
        async with stdio_client(self.server_params) as (read, write):
            async with ClientSession(read, write) as session:
                self.session = session
                await self.session.initialize()

                tools = await load_mcp_tools(self.session)
                logger.info(f"\nLoaded tools: {[tool.name for tool in tools]}")

                agent_executor = self.build_agent_executor(tools)
                chat_history = []

                while True:
                    print("\nMCP client active! Type \u001b[31m quit \u001b[0m to exit.")
                    query = await ainput("\nQuery: ")
                    if query.lower() == "quit":
                        print("Shutting down MCP client...")
                        break

                    try:
                        # Use AgentExecutor's direct invocation
                        result = await agent_executor.ainvoke({
                            "input": query,
                            "chat_history": chat_history
                        })
                        
                        # Process result
                        if "output" in result:
                            formatted_output = result["output"]
                            print(f"\nGemini: \u001b[32m{formatted_output}\u001b[0m")
                            
                            # Add to chat history
                            chat_history.append(HumanMessage(content=query))
                            chat_history.append(AIMessage(content=formatted_output))
                        else:
                            print("\n\u001b[31mNo output in result\u001b[0m")
                            
                    except Exception as e:
                        logger.error(f"\n\u001b[31mError during agent processing: {e}\u001b[0m", exc_info=True)
