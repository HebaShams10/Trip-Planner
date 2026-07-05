from langchain_core.output_parsers import StrOutputParser
from ChatBot.prompt import prompt
from ChatBot.llm import llm

class ChatChain:
    def __init__(self):
        self.chain = (prompt | llm | StrOutputParser())
    def invoke(self, payload, config=None):
        return self.chain.invoke(payload, config=config)
    async def ainvoke(self, payload, config=None):
        return await self.chain.ainvoke(payload, config=config)