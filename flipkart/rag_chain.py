from langchain_groq  import ChatGroq
from langchain_ollama import ChatOllama

# For langchain 0.3.x, imports are in langchain_core
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory

# Import chain creation utilities
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from flipkart.config import Config

class RAGChainBuilder:
    def __init__(self, vector_store):
        self.vector_store = vector_store
        self.config = Config()
        
        # Choose model based on configuration
        if self.config.USE_OLLAMA:
            self.model = ChatOllama(
                model = self.config.OLLAMA_MODEL, 
                base_url = self.config.OLLAMA_BASE_URL, 
                temperature = 0.2
            )
        else:
            self.model = ChatGroq(
                api_key = self.config.GROQ_API_KEY,
                model = self.config.GROQ_MODEL,
                temperature = 0.2
            )
        
        self.history_Store = {} #it will store all our history for different sessions.

    def _get_history(self, session_id:str)->BaseChatMessageHistory:
        if session_id not in self.history_Store:
            self.history_Store[session_id] = ChatMessageHistory()
        return self.history_Store[session_id]

    def build_chain(self):
        retriever = self.vector_store.as_retriever(search_kwargs={"k":3})

        # Combined prompt for RAG with history
        qa_prompt = ChatPromptTemplate.from_messages([
            ("system", """You're an e-commerce bot for Flipkart answering product queries using customer reviews.

IMPORTANT RULES:
1. ALWAYS mention specific product names from the reviews
2. Quote actual customer feedback and experiences
3. Highlight pros and cons based on real reviews
4. Be specific - avoid generic answers
5. If multiple products match, compare them by name

CONTEXT (Product Reviews):
{context}"""),
            MessagesPlaceholder(variable_name="chat_history"), 
            ("human", "{input}")
        ])

        # Create RAG chain using LCEL (LangChain Expression Language)
        def format_docs(docs):
            formatted = []
            for doc in docs:
                product_name = doc.metadata.get("product_name", "Unknown Product")
                formatted.append(f"Product: {product_name}\nReview: {doc.page_content}")
            return "\n\n---\n\n".join(formatted)

        rag_chain = (
            {
                "context": lambda x: format_docs(retriever.invoke(x["input"])),
                "input": lambda x: x["input"],
                "chat_history": lambda x: x.get("chat_history", [])
            }
            | qa_prompt
            | self.model
            | StrOutputParser()
        )

        # Wrap with message history
        return RunnableWithMessageHistory(
            rag_chain,
            self._get_history,
            input_messages_key="input",
            history_messages_key="chat_history"
        )