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
        folders = glob.glob("search-folder/*")
        text_loader_kwargs = {'encoding': 'utf-8'}
        documents = []

        for folder in folders:
            doc_type = os.path.basename(folder)
            loader = DirectoryLoader(folder, glob="**/*.md", loader_cls=TextLoader, loader_kwargs=text_loader_kwargs)
            folder_docs = loader.load()
            for doc in folder_docs:
                doc.metadata["doc_type"] = doc_type
                documents.append(doc)

        if not documents:
            print("No documents found in search-folder")
            return None

        text_splitter = CharacterTextSplitter(chunk_size=1500, chunk_overlap=280)
        chunks = text_splitter.split_documents(documents)

        doc_types = set(chunk.metadata['doc_type'] for chunk in chunks)
        print(f"Document types found: {', '.join(doc_types)}")

        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        db_name = "vector_db"
        if os.path.exists(db_name):
            try:
                FAISS(persist_directory=db_name, embedding_function=embeddings).delete_collection()
            except:
                pass  # Ignore errors in deleting old collection

        vectorstore = FAISS.from_documents(chunks, embedding=embeddings)
        return vectorstore
    except Exception as e:
        print(f"Error initializing vector store: {str(e)}")
        return None

# Initialize vector store
vectorstore = initialize_vector_store()

# Initialize conversation chain if vector store was created successfully
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
    """
    Chat with the LLM using the vector store for context.
    
    Args:
        message (str): User's message
        history (list): Chat history
        
    Returns:
        str: LLM response
    """
    if conversation_chain is None:
        return "Error: Conversation chain not initialized. Please check the setup."
    
    try:
        result = conversation_chain.invoke({"question": message})
        return result["answer"]
    except Exception as e:
        return f"Error: {str(e)}"