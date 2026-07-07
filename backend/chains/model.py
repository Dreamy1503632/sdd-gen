from langchain_groq import ChatGroq
from langchain_openai import AzureChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

# Check required environment variables
required_keys = [
    "GROQ_API_KEY",
    "AZURE_OPENAI_API_KEY",
    "AZURE_OPENAI_ENDPOINT"
]

for key in required_keys:
    if not os.getenv(key):
        raise ValueError(f"{key} is not set in environment variables")


G_llm = ChatGroq(
    temperature=0,
    model_name="openai/gpt-oss-120b"
)


llm = AzureChatOpenAI(
    azure_deployment="gpt-35-turbo",
    api_version="2024-08-01-preview",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)


if __name__ == "__main__":
    response = llm.invoke("What is the capital of France?")
    print(response)