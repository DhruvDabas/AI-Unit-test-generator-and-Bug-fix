import os
import glob
from openai import OpenAI
import gradio as gr
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.chat_models import ChatOllama
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

# Constants
OLLAMA_API = "http://localhost:11434/api/chat"
HEADERS = {"Content-Type": "application/json"}
MODEL = "gemma3:4b"

# Initialize OpenAI client for Ollama
openai_client = OpenAI(base_url='http://localhost:11434/v1', api_key='ollama')

def initialize_vector_store():
    """Initialize the vector store with documents from search-folder."""
    try:
        
        if not os.path.exists("search-folder"):
            print("search-folder does not exist")
            return None
            
        
        loader = DirectoryLoader(
            "search-folder", 
            glob="**/*", 
            loader_cls=TextLoader, 
            loader_kwargs={'encoding': 'utf-8'},
            show_progress=True,
            use_multithreading=True
        )
        documents = loader.load()
        
        
        for i, doc in enumerate(documents):
            doc.metadata["doc_id"] = i
            
        if not documents:
            print("No documents found in search-folder")
            return None

        print(f"Loaded {len(documents)} documents")
        
        # Split documents into chunks
        text_splitter = CharacterTextSplitter(chunk_size=1500, chunk_overlap=280)
        chunks = text_splitter.split_documents(documents)
        
        print(f"Split into {len(chunks)} chunks")

        # Create embeddings
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        # Create vectorstore
        vectorstore = FAISS.from_documents(chunks, embedding=embeddings)
        return vectorstore
    except Exception as e:
        print(f"Error initializing vector store: {str(e)}")
        return None





vectorstore = initialize_vector_store()

# chat if convo chain is successful
conversation_chain = None
if vectorstore:
    try:
        llm = ChatOllama(model="gemma3:4b", temperature=0.7)
        memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
        retriever = vectorstore.as_retriever()
        conversation_chain = ConversationalRetrievalChain.from_llm(
            llm=llm, 
            retriever=retriever, 
            memory=memory
        )
    except Exception as e:
        print(f"Error initializing conversation chain: {str(e)}")

def chat_with_llm(message, history):



    if conversation_chain is None:
        return "Error: Conversation chain not initialized. Please check the setup."
    
    try:
        result = conversation_chain.invoke({"question": message})
        return result["answer"]
    except Exception as e:
        return f"Error: {str(e)}"