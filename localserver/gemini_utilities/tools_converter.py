# import genai tool handler
from google.genai.types import Tool, FunctionDeclaration

# import shema cleaning function
from gemini_utilities.clean_schema import tool_schema_handler


def convert_mcp_tools_to_gemini(mcp_tools):
    """convert mcp tools definition to the correct format for Gemini ai function calling

    Args:
        mcp_tools (list): list of mcp tools objct with name, description, and inputSchema

    Returns:
        List: list of Gemini tool object with properly formatted function declaration
    """
    gemini_tools = []
    print("cleaning tool properties")
    for tool in mcp_tools:
        # ensure schema input is a valid JSON schema

        parameters = tool_schema_handler(tool.inputSchema)
        # create a function declaration
        function_declaration = FunctionDeclaration(
            name=tool.name,
            description=tool.description,
            parameters=parameters
        )
        # wrap the declaration in a tool object
        gemini_tool = Tool(function_declarations=[function_declaration])
        gemini_tools.append(gemini_tool)

    return gemini_tools
