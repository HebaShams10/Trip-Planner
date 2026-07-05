from langchain_groq import ChatGroq
from ChatBot import config

def get_llm():
    return ChatGroq(
        api_key=config.GROQ_API_KEY,
        model=config.model_name,
        temperature=config.temperature,
        max_tokens=config.max_tokens,
        request_timeout=config.timeout_s
    )

llm = get_llm()