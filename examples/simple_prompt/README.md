# A basic python program to chain a prompt to an LLM call and observe the traces in Langsmith
- Env Var Settings
- Run the python Program
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
> python3 ./basic_chain.py
Kafka is used for building real-time data pipelines and streaming applications. It allows for the processing and analyzing of high-throughput data streams, enabling the integration of data from multiple sources and facilitating event-driven architectures.
```
## Observe the trace in LangSmith
[![Check Table](../images/basic_chain.png)]()
