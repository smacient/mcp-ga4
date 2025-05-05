# MCP Server For Google Analytics 4

This is a Model Context Protocol (MCP) server with tools to retrieve information from Google analytics 4 cloud server. It integrates easily with claude desktop and gives helpful business intelligence feedback based on your data

## Setup Steps

1.  ## Initialize the project 
    #### launch CMD where you want to keep your project, and clone the repo, enter project folder
```bash
    git clone https://github.com/smacient/mcp-ga4.git
    cd mcp-ga4
```

2.  ## Create virtual environment and activate it
```bash
    uv venv
    .venv\Scripts\activate
  ```

3.  ## Install dependencies:
```bash
    uv sync
```

4.  ## Setup environment
- set up your goggle account credentials and download the json file. rename it credentials.json
- create a `.env` file inside the `localserver` folder
- add the correct path to your google credentials in the env file

    `GOOGLE_APPLICATION_CREDENTIALS="C:\\Users\\path to\\credentials.json"`


## Features

The server implements the following features:

### Tools
- `get_report`: retrieve your GA4 report based on required metrics, dimension and timeframe and give a detailed summary and insight based on the data
- `get_realtime_report`: retrieve your GA4 report realtime report based on required metrics, dimension and timeframe and give a detailed summary and insight based on the data
- `compare_report_metrics`: retrieve your GA4 report for two periods based on required metrics, dimension and give a comparative report and insight based on the data
- `get_report_with_order`: retrieve your GA4 report report based on required metrics, dimension and timeframe, rank it based on specified metrics and give a detailed summary and insight based on the data
- `list_all_properties`: retrieve your GA4 properties available in the current user
- `list_all_accounts`: retrieve your GA4 account information, which it uses to get other information

## Running the Server

#### To run on terminal

To run the server with the MCP Inspector for development:
```bash
uv run mcp dev localserver/ga4_server.py
```

To run the with openai client: 

update the .env
  ```ENV
    GOOGLE_APPLICATION_CREDENTIALS="C:\\Users\\`path to`\\credentials.json"
    OPENAI_API_KEY="add your openai api key"
  ```
run command
```bash
uv run mcp localserver/openai_client.py
```

To run the with gemini client: 

update the .env
  ```ENV
    GOOGLE_APPLICATION_CREDENTIALS="C:\\Users\\`path to`\\credentials.json"
    GEMINI_API_KEY="add your gemini api key"
  ```
run command
```bash
uv run mcp localserver/gemini_client.py
```

#### To run on Claude desktop

To install the server in Claude desktop app:
```bash
uv run mcp install localserver/ga4_server.py
```
Set up the configuration properly
- go to claude desktop.
- click settings, go to developer and click on edit config
- open the config file with sublime text
- add the env section as the one shown below.
- edit the claude configuration file to look like the one below. add the paths needed. remove `path to` and add the correct path

```JSON
{
  "mcpServers": {
    "Google Analytics 4": {
      "command": "uv",
      "args": [
        "run",
        "--with",
        "mcp[cli]",
        "mcp",
        "run",
        "C:\\Users\\`path to`\\Gemini-Agent-MCP\\src\\gemini_server_sample.py"
      ],
      "env": {
        "VIRTUAL_ENV": "C:\\Users\\`path to`\\Gemini-Agent-MCPmcp_ga4\\.venv",
        "PATH": "C:\\Users\\`path to`\\Gemini-Agent-MCP\\.venv\\Scripts;${PATH}",
        "GOOGLE_APPLICATION_CREDENTIALS": "C:\\Users\\`path to`\\credentials.json"
      }
    }
  }
}

```

 End claude in task manager and restart it. Your tools will be visible on the chat interface.

 Ask Claude to get your GA4 information and accept the popup permit to use the tools required.
