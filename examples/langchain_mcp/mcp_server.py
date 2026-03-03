# mcp_server.py
from fastmcp import FastMCP  # adjust import if your fastmcp version differs
from mcp_backend import lookup_order

mcp = FastMCP("orders-demo")

@mcp.tool("lookupByKey")
def lookup_by_key(table: str, key: str) -> str:
    """
    FastMCP tool that wraps our core lookup_order() logic.
    """
    return lookup_order(table, key)

if __name__ == "__main__":
    # Runs the MCP server (typically speaking stdio / http / sse depending
    # on your FastMCP configuration / CLI flags).
    mcp.run()
