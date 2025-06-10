import asyncio
import nest_asyncio
import logging
from mcp import ClientSession
from mcp.client.sse import sse_client

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

nest_asyncio.apply()  # Needed to run interactive python

"""
Make sure:
1. The server is running before running this script.
2. The server is configured to use SSE transport.
3. The server is listening on port 8000.

To run the server:
uv run server2.py
"""

async def main():
    try:
        logger.debug("Starting client")
        # Connect to the server using SSE
        logger.debug("Connecting to server at http://localhost:8000/sse")
        async with sse_client("http://localhost:8000/sse") as (read_stream, write_stream):
            logger.debug("Connected to server")
            async with ClientSession(read_stream, write_stream) as session:
                # Initialize the connection
                logger.debug("Initializing session")
                await session.initialize()
                logger.debug("Session initialized")

                # List available tools
                logger.debug("Listing available tools")
                tools_result = await session.list_tools()
                print("Available tools:")
                for tool in tools_result.tools:
                    print(f"  - {tool.name}: {tool.description}")

                # Call our Weather tool
                logger.debug("Calling get_alerts tool for CA")
                result = await session.call_tool("get_alerts", arguments={"state":"CA"})
                print(f"The weather alerts are = {result.content[0].text}")
                logger.debug("Tool call completed")

    except Exception as e:
        logger.error(f"Error in client: {str(e)}", exc_info=True)
        raise

if __name__ == "__main__":
    try:
        logger.debug("Starting main execution")
        asyncio.run(main())
    except Exception as e:
        logger.error(f"Error in main execution: {str(e)}", exc_info=True)
        raise