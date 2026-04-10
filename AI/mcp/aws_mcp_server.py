from mcp.server.fastmcp import FastMCP
import boto3
from botocore.exceptions import ClientError
from datetime import datetime

mcp = FastMCP("aws-mcp-demo")

s3 = boto3.client("s3",region_name="ap-south-1")
ce = boto3.client("ce", region_name="ap-south-1")

@mcp.tool()
def get_s3_file(bucket: str, key: str) -> str:
    """Read a text file from S3 and return its contents.key means file name"""

    response = s3.get_object(Bucket=bucket,Key=key)
    content  = response['Body'].read().decode("utf-8")

    return content
@mcp.tool()
def get_aws_costs(start_date: str, end_date: str) -> str:
    """
    Get total AWS unblended cost between two dates.
    Date format: YYYY-MM-DD
    Note: end_date is exclusive in AWS Cost Explorer.
    Example: start_date=2026-03-01, end_date=2026-04-01
    """
    try:
        response = ce.get_cost_and_usage(
            TimePeriod={
                "Start": start_date,
                "End": end_date
            },
            Granularity="MONTHLY",
            Metrics=["UnblendedCost"]
        )

        results = response.get("ResultsByTime", [])
        if not results:
            return "No cost data found for the given period."

        amount = results[0]["Total"]["UnblendedCost"]["Amount"]
        unit = results[0]["Total"]["UnblendedCost"]["Unit"]

        return f"Total AWS cost from {start_date} to {end_date} is {amount} {unit}."

    except ClientError as e:
        return f"AWS error: {str(e)}"
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def greet(name:str) ->str:
    """greet the name"""
    return f"Hello {name}! MCP is working with AWS."

@mcp.tool()
def get_aws_costs_by_service(start_date: str, end_date: str) -> str:
    """
    Get AWS cost grouped by service for a given period.

    Date format: YYYY-MM-DD
    Example:
    start_date = 2026-03-01
    end_date   = 2026-04-01

    Note: end_date is exclusive.
    """
    try:
        datetime.strptime(start_date, "%Y-%m-%d")
        datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        return "Date must be in YYYY-MM-DD format. Example: 2026-03-01"

    try:
        response = ce.get_cost_and_usage(
            TimePeriod={
                "Start": start_date,
                "End": end_date
            },
            Granularity="MONTHLY",
            Metrics=["UnblendedCost"],
            GroupBy=[
                {
                    "Type": "DIMENSION",
                    "Key": "SERVICE"
                }
            ]
        )

        results = response.get("ResultsByTime", [])
        if not results:
            return "No cost data found for the given period."

        groups = results[0].get("Groups", [])
        if not groups:
            return "No service-wise cost data found."

        lines = [f"AWS cost by service from {start_date} to {end_date}:"]
        for group in groups:
            service_name = group["Keys"][0]
            amount = group["Metrics"]["UnblendedCost"]["Amount"]
            unit = group["Metrics"]["UnblendedCost"]["Unit"]
            lines.append(f"- {service_name}: {amount} {unit}")

        return "\n".join(lines)

    except ClientError as e:
        return f"AWS error: {str(e)}"
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    mcp.run(transport="streamable-http")