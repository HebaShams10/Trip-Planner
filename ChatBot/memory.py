from langchain_community.chat_message_histories import ChatMessageHistory

chat_history = ChatMessageHistory()

def load_memory(user_input):
    return {
        "question": user_input,
        "chat_history": chat_history.messages
    }