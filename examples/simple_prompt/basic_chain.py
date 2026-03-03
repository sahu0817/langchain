from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

llm = ChatOpenAI(model="gpt-4o-mini")

prompt = ChatPromptTemplate.from_template(
    "Answer concisely: {question}"
)
chain = prompt | llm

# Every call becomes a traced run in LangSmith
resp = chain.invoke({"question": "What is Kafka used for?"})
print(resp.content)
