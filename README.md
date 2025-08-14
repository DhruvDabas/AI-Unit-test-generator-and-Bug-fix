# AI-Unit-test-generator-and-Bug-fix

**Automated Unit Test Generator & Bug Finder using Express.js, FAISS, and Frontier LLMs**

CodeGuard AI helps developers **understand, debug, and improve** their codebase.  
It can:
- Answer questions about any function/class in the repo
- Find potential bugs using static analysis + AI reasoning
- Generate unit tests for missing coverage
- Suggest code refactors

---

## 🚀 Features
- **Repo Ingestion**: Parse source code into functions/classes and store embeddings in FAISS.
- **AI Code Q&A**: Ask natural language questions about the code.
- **Bug Detection**: Identify potential logic/security issues.
- **Unit Test Generation**: Create PyTest/Jest test files automatically.

---

## 🏗 Tech Stack
**Backend:**
- Node.js + Express.js
- LangChain.js (RAG orchestration)
- FAISS (vector database)
- Tree-sitter (code parsing)
- OpenAI / HuggingFace APIs (embeddings + reasoning)


# Create .env file
cp .env.example .env
