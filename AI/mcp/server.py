from mcp.server.fastmcp import FastMCP

mcp = FastMCP("first-mcp")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

@mcp.tool()
def greet(name: str) -> str:
    """Greet a person."""
    return f"Hello {name}!"
    
if __name__ == "__main__":
    mcp.run(transport="streamable-http")