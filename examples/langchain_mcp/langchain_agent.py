# langchain_agent.py
from pydantic import BaseModel, Field

from langchain_core.tools import StructuredTool
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent

from mcp_backend import lookup_order

class LookupOrderInput(BaseModel):
    table: str = Field(description="Logical table name, e.g. 'orders'")
    key: str = Field(description="Primary key of the order, e.g. 'ORD-1001'")

lookup_order_tool = StructuredTool.from_function(
    name="lookup_order",
    description=(
        "Look up an order by primary key from the 'orders' table and return JSON."
    ),
    func=lookup_order,
    args_schema=LookupOrderInput,
)

def build_agent():
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)  # or your model
    tools = [lookup_order_tool]

    return create_agent(
        llm,
        tools=tools,
        system_prompt="You are an assistant that helps inspect orders.",
        debug=True,  # verbose execution
    )

if __name__ == "__main__":
    agent = build_agent()

    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": (
                        "Use the lookup_order tool to fetch order 'ORD-1001' "
                        "from the 'orders' table and summarize it."
                    ),
                }
            ]
        }
    )
    # New API returns state with "messages"; last message is the final reply
    messages = result.get("messages", [])
    if messages:
        last = messages[-1]
        content = getattr(last, "content", str(last))
        print(content)
    else:
        print(result)
