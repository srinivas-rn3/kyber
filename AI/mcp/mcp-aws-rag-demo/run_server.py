from mcp.server.fastmcp import FastMCP
from app.tools.aws_costs import get_aws_costs_by_service
from app.tools.s3_tools import list_s3_files
from app.tools.dynamodb_tools import get_dynamodb_item
from app.tools.rag_tools import search_documents
from app.tools.sequence_tools import run_demo_sequence

mcp = FastMCP("aws-rag-demo")

mcp.tool()(get_aws_costs_by_service)
mcp.tool()(list_s3_files)
mcp.tool()(get_dynamodb_item)
mcp.tool()(search_documents)
mcp.tool()(run_demo_sequence)

if __name__ == "__main__":
    mcp.run()