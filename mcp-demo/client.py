# client.py: plays the part of an AI app (the "host")
import asyncio
import sys
import argparse

from mcp import Client, StdioServerParameters

# Start mcp_server.py and talk to it, the way Claude Desktop or Cursor would
server = StdioServerParameters(command=sys.executable, args=["mcp_server.py"])
parser = argparse.ArgumentParser()
parser.add_argument("--tool", choices=["classify_iris", "iris_probabilities"], default="iris_probabilities")
parser.add_argument("--measurements", type=float, nargs=4, default=[6.0, 2.7, 5.1, 1.6])
options = parser.parse_args()


async def main():
    async with Client(server) as client:
        # 1. Discovery: ask the server what tools it has
        result = await client.list_tools()
        for tool in result.tools:
            print("Tool:", tool.name)
            print("Description:", " ".join((tool.description or "").split()))
            print("Inputs:", ", ".join(
                f"{name} ({definition['type']})"
                for name, definition in tool.input_schema["properties"].items()
            ))
            print()

        # 2. Use a tool, as an AI app would after reading the descriptions
        answer = await client.call_tool(
            options.tool,
            dict(zip(["sepal_length", "sepal_width", "petal_length", "petal_width"], options.measurements)),
        )
        if answer.is_error:
            raise RuntimeError(answer.content[0].text)
        print("Called:", options.tool)
        print(answer.content[0].text)


asyncio.run(main())
