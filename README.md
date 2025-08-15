# AI-Powered Unit Test Generator & Bug Finder using Gradio, FAISS, and Frontier LLMs

**Coder AI** is an intelligent developer assistant that helps you **understand**, **debug**, and **improve** your codebase.  
It combines **code parsing**, **semantic search**, and **LLM reasoning** to answer questions, detect bugs, generate tests, and suggest refactors — all through an intuitive **Gradio web UI**.

---

##  Key Capabilities

- **Natural Language Code Q&A** – Ask questions about any function, class, or module in your repo.
- **Bug Detection & Analysis** – Identify logic errors and security vulnerabilities using static analysis + AI reasoning.
- **Automated Unit Test Generation** – Create **PyTest** or **Jest** test files for untested code paths.
- **Code Refactoring Suggestions** – Improve readability, maintainability, and performance.

---

##  How It Works

1. **Repo Ingestion** – Parse source files into functions/classes using **Tree-sitter**.
2. **Embedding & Indexing** – Store code embeddings in **FAISS** for fast semantic search.
3. **RAG Pipeline** – Retrieve relevant code and feed it to a **frontier LLM** for analysis and generation.
4. **Interactive UI** – Use the **Gradio interface** to upload repos, ask questions, and receive actionable insights.

---
