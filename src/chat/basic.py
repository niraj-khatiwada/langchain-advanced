from langchain_openai import ChatOpenAI
from langchain.globals import set_debug
import os
from dotenv import load_dotenv
from langchain_core.prompts.chat import ChatPromptTemplate

load_dotenv(override=True)
set_debug(True)

OPEN_AI_BASE_URL = os.getenv("OPEN_AI_BASE_URL")
OPEN_AI_API_KEY = os.getenv("OPEN_AI_API_KEY")


llm = ChatOpenAI(
    base_url=OPEN_AI_BASE_URL,
    api_key=OPEN_AI_API_KEY,
)

prompt_template = ChatPromptTemplate(
    messages=[
        (
            "system",
            "Always greet in English language even if question was asked in different language",
        ),
        ("human", "{input}"),
    ],
)

# Langchain common expression
chain = prompt_template | llm

res = chain.invoke(
    input=prompt_template.format_messages(
        input="नमस्ते",
    )
)

print(res.text())
