# An LLM application to 
- Creates a langchain agent 
- Creates a context with MCP tool calling
- Enriches the prompt  and invoke a LLM
- Observe the trace in Langsmith

## Env Variables
```
> . ./set.env
> env | egrep "LANGCHAIN|OPENAI"
OPENAI_API_KEY=sk-svcacct-**************
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=my-app
LANGCHAIN_API_KEY=lsv2_sk_***************
```
## Run the Python Program
```
> python3 ./langchain_mcp.py
The order 'ORD-1001' belongs to the customer Alice and has a total amount of $42.50.
```
## Observe the trace in LangSmith
[![Check Table](../images/langchain_mcp.png)]()
