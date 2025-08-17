import os
from typing import Optional
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_ollama import ChatOllama
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from openai import OpenAI


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
        
        if not documents:
            print("No documents found in search-folder")
            return None

        print(f"Loaded {len(documents)} documents")
        
        # Add document IDs
        for i, doc in enumerate(documents):
            doc.metadata["doc_id"] = i
            
        # Split documents into chunks
        text_splitter = CharacterTextSplitter(
            chunk_size=1500,
            chunk_overlap=280
        )
        chunks = text_splitter.split_documents(documents)
        print(f"Split into {len(chunks)} chunks")

        # Create embeddings and vectorstore
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        return FAISS.from_documents(chunks, embedding=embeddings)
        
    except Exception as e:
        print(f"Error initializing vector store: {str(e)}")
        return None


def initialize_conversation_chain(vectorstore):
    """Initialize the conversation chain with the given vectorstore."""
    try:
        if vectorstore is None:
            return None
            
        llm = ChatOllama(
            model="gemma3:4b",
            temperature=0.7
        )
        memory = ConversationBufferMemory(
            memory_key='chat_history', 
            return_messages=True
        )
        retriever = vectorstore.as_retriever()
        
        conversation_chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=retriever,
            memory=memory
        )
        return conversation_chain
    except Exception as e:
        print(f"Error initializing conversation chain: {str(e)}")
        return None


# Initialize vector store
vectorstore = initialize_vector_store()

# Initialize conversation chain
conversation_chain = initialize_conversation_chain(vectorstore)


def find_bugs_in_code():
    """Find bugs in the codebase by querying the LLM with a specific prompt."""
    # Re-initialize if needed
    global conversation_chain, vectorstore
    
    if conversation_chain is None:
        # Try to re-initialize vector store and conversation chain
        vectorstore = initialize_vector_store()
        conversation_chain = initialize_conversation_chain(vectorstore)
        
        if conversation_chain is None:
            return "Error: Conversation chain not initialized. Please check the setup and ensure Ollama is running with the required model."
    
    # Specific prompt for bug finding
    bug_prompt = (
        "Analyze all the code in the provided codebase and identify any bugs, "
        "errors, or potential issues. Focus only on actual bugs and problems. "
        "If you find any bugs, list them clearly. If there are no bugs or nothing "
        "is wrong in the code, simply respond with 'All OK'. Do not make up bugs "
        "that don't exist."
    )
    
    try:
        result = conversation_chain.invoke({"question": bug_prompt})
        return result["answer"]
    except Exception as e:
        return f"Error: {str(e)}"
