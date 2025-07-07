from dotenv import load_dotenv
import google.generativeai as genai
from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client
from typing import List
import asyncio
import nest_asyncio
import json
import os

nest_asyncio.apply()

load_dotenv()

class MCP_ChatBot:

    def __init__(self):
        # Initialize session and client objects
        self.session: ClientSession = None
        # Configure Gemini API
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            raise ValueError("Please set GOOGLE_API_KEY environment variable")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        self.chat = self.model.start_chat(history=[])
        self.available_tools: List[dict] = []

    async def process_query(self, query):
        # Add user message to chat
        self.chat.send_message(query)
        
        # Get response from Gemini
        response = self.chat.last
        
        # Handle response
        if hasattr(response, 'text'):
            print(response.text)
        elif hasattr(response, 'candidates') and response.candidates:
            candidate = response.candidates[0]
            if hasattr(candidate, 'content') and candidate.content:
                content = candidate.content
                if hasattr(content, 'parts') and content.parts:
                    for part in content.parts:
                        if hasattr(part, 'text'):
                            print(part.text)
                        elif hasattr(part, 'function_call'):
                            # Handle function call
                            function_call = part.function_call
                            tool_name = function_call.name
                            
                            # Parse function arguments
                            try:
                                tool_args = json.loads(function_call.args) if function_call.args else {}
                                print(f"Calling tool {tool_name} with args {tool_args}")
                                
                                # Call the tool through MCP session
                                result = await self.session.call_tool(tool_name, arguments=tool_args)
                                
                                # Send tool result back to Gemini
                                tool_result = {
                                    "role": "function",
                                    "name": tool_name,
                                    "content": result.content
                                }
                                
                                # Add tool result to chat and get new response
                                self.chat.send_message(json.dumps(tool_result))
                                final_response = self.chat.last
                                
                                if hasattr(final_response, 'text'):
                                    print(final_response.text)
                                else:
                                    print("Tool execution completed")
                                    
                            except Exception as e:
                                print(f"Error calling tool {tool_name}: {e}")
                                # Send error back to Gemini
                                error_result = {
                                    "role": "function",
                                    "name": tool_name,
                                    "content": f"Error: {str(e)}"
                                }
                                self.chat.send_message(json.dumps(error_result))
                                final_response = self.chat.last
                                if hasattr(final_response, 'text'):
                                    print(final_response.text)

    async def chat_loop(self):
        """Run an interactive chat loop"""
        print("\nMCP Chatbot with Gemini Started!")
        print("Type your queries or 'quit' to exit.")
        
        while True:
            try:
                query = input("\nQuery: ").strip()
        
                if query.lower() == 'quit':
                    break
                    
                await self.process_query(query)
                print("\n")
                    
            except Exception as e:
                print(f"\nError: {str(e)}")
    
    async def connect_to_server_and_run(self):
        # Create server parameters for stdio connection
        server_params = StdioServerParameters(
            command="uv",  # Executable
            args=["run", "research_server.py"],  # Optional command line arguments
            env=None,  # Optional environment variables
        )
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                self.session = session
                # Initialize the connection
                await session.initialize()
    
                # List available tools
                response = await session.list_tools()
                
                tools = response.tools
                print("\nConnected to server with tools:", [tool.name for tool in tools])
                

                
                # Configure Gemini with tools using the correct format
                try:
                    # Create tools in the exact format Gemini expects
                    gemini_tools = []
                    for tool in response.tools:
                        if tool.name == "search_papers":
                            gemini_tools.append({
                                "function_declarations": [{
                                    "name": "search_papers",
                                    "description": "Search for papers on arXiv based on a topic and store their information.",
                                    "parameters": {
                                        "type": "object",
                                        "properties": {
                                            "topic": {
                                                "type": "string",
                                                "description": "The topic to search for"
                                            },
                                            "max_results": {
                                                "type": "number",
                                                "description": "Maximum number of results to retrieve (default: 5)"
                                            }
                                        },
                                        "required": ["topic"]
                                    }
                                }]
                            })
                        elif tool.name == "extract_info":
                            gemini_tools.append({
                                "function_declarations": [{
                                    "name": "extract_info",
                                    "description": "Search for information about a specific paper across all topic directories.",
                                    "parameters": {
                                        "type": "object",
                                        "properties": {
                                            "paper_id": {
                                                "type": "string",
                                                "description": "The ID of the paper to look for"
                                            }
                                        },
                                        "required": ["paper_id"]
                                    }
                                }]
                            })
                    
                    self.model = genai.GenerativeModel('gemini-2.5-flash', tools=gemini_tools)
                    self.chat = self.model.start_chat(history=[])
                    print("Successfully configured Gemini with tools!")
                    
                except Exception as e:
                    print(f"Error configuring Gemini with tools: {e}")
                    print("Falling back to basic model without tools...")
                    self.model = genai.GenerativeModel('gemini-2.5-flash')
                    self.chat = self.model.start_chat(history=[])
                    print("Using basic Gemini model without function calling")
    
                await self.chat_loop()


async def main():
    chatbot = MCP_ChatBot()
    await chatbot.connect_to_server_and_run()
  

if __name__ == "__main__":
    asyncio.run(main())