Here is the complete architectural breakdown for your **Multi-Agent Git Analyzer**, designed to be a formal blueprint for your implementation.

---

## 1. High-Level Design (HLD)

The system follows a decoupled, containerized architecture split into three core layers: **Ingestion**, **Storage/Retrieval**, and **Serving**.

```
                                  +-----------------------+
                                  |   React Frontend      |
                                  +-----------+-----------+
                                              | (HTTP / WebSockets)
                                              v
                                  +-----------+-----------+
                                  |    FastAPI Backend    |
                                  +-----+-----------+-----+
                                        |           |
       +--------------------------------+           +------------------+
       | (Triggers Git Clone)                                          | (Queries Engine)
       v                                                               v
+------+----------------+       +-------------------+       +----------+----------+
|  Ingestion Engine     | ----> | Text Splitter     | ----> | LangChain Orchestrator|
|  (GitPython / Bash)   |       | (AST / Language)  |       | (Agent A & Agent B) |
+-----------------------+       +---------+---------+       +----------+----------+
                                          |                            |
                                          | (Generates Embeddings)     | (Vector Search)
                                          v                            v
                                +---------+---------+        +---------+---------+
                                |  Embedding Model  | ---->  | Vector DB         |
                                |  (HuggingFace)    |        | (ChromaDB)        |
                                +-------------------+        +-------------------+

```

### Component Breakdown

* **User Interface (UI):** A single-page application where users input a GitHub URL and interact with the AI chat agent.
* **API Gateway & Server:** An asynchronous FastAPI server managing asynchronous background tasks (for repository parsing) and real-time token streaming.
* **Data Pipeline:** A worker process that downloads the codebase, strips out non-essential files, parses the structural files, chunks them, and stores their representations.
* **Vector Engine:** A specialized spatial database optimized for storing high-dimensional mathematical representations (embeddings) of code chunks to enable fast semantic lookups.
* **Multi-Agent Coordinator:** The execution environment that loops user input through specialized tool-using agents before generating a finalized response.

---

## 2. Low-Level Design (LLD)

### Data Ingestion Sequence

```
[User] -> (Submit URL) -> [FastAPI] -> (Trigger Task) -> [GitWorker]
                                                             |
   +---------------------------------------------------------+
   v
[Clone Repo] -> [Filter Extensions] -> [AST Code Splitter] -> [Generate Vectors] -> [Save to ChromaDB]

```

### Core System Modules & Class Signatures

#### A. Ingestion & Document Processor

```python
class RepoIngestionEngine:
    def __init__(self, repo_url: str, storage_path: str):
        self.repo_url = repo_url
        self.storage_path = storage_path
        
    def clone_repository(self) -> bool:
        """Clones the remote repo using GitPython, returns true on success."""
        pass

    def filter_and_load_files(self) -> list[dict]:
        """Traverses directory; filters for valid extensions (.py, .js, .ts, .go, .java).
        Returns raw file contents and metadata paths."""
        pass

```

#### B. Semantic Chunking Layer

```python
class CodeSemanticSplitter:
    def __init__(self, language: str, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.language = language
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk_source_code(self, raw_documents: list[dict]) -> list[object]:
        """Applies RecursiveCharacterTextSplitter.from_language to split 
        by semantic code boundaries (functions, classes)."""
        pass

```

#### C. Vector Storage Connection

```python
class VectorStoreManager:
    def __init__(self, collection_name: str, embedding_model_name: str):
        self.client = None # Initialize ChromaDB client
        self.embed_fn = None # Initialize HuggingFace Embeddings
        
    def index_documents(self, chunks: list[object]) -> bool:
        """Computes embeddings and batches injection into Vector Database."""
        pass
        
    def get_retriever(self):
        """Returns a vector store retriever interface for the AI agents."""
        pass

```

#### D. Multi-Agent Reasoning Execution

```python
class MultiAgentOrchestrator:
    def __init__(self, retriever_tool):
        self.llm = None # Initialize Ollama (Gemma) or OpenAI client
        self.tools = [retriever_tool]
        
    def initialize_agent_executor(self):
        """Creates the LangChain ReAct agent equipped with search tools and system prompts."""
        pass
        
    async def stream_analysis(self, query: str):
        """Asynchronously streams generated response tokens back to the WebSocket wrapper."""
        yield token

```

---

## 3. Step-by-Step Implementation Instructions

### Step 1: Initialize Project Structure

Set up a clean monorepo architecture:

```text
git-analyzer/
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py            # FastAPI Application entry point
│   │   ├── core/              # Ingestion, Splitter, Vector logic
│   │   └── agents/            # LangChain Agent definitions
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   ├── src/                   # React Components (Chat, Dash, Hooks)
│   ├── package.json
│   └── Dockerfile
│
└── docker-compose.yml

```

### Step 2: Build the Python Ingestion Script

* Install core dependencies: `pip install fastapi langchain langchain-community chromadb gitpython sentence-transformers uvicorn`.
* Implement `RepoIngestionEngine` using `git.Repo.clone_from()`.
* Use `langchain_text_splitters.Language` enumeration to correctly segment blocks according to the specific source language.

### Step 3: Configure Vector Store & LLM Pipeline

* Use a lightweight local embedding model like `all-MiniLM-L6-v2` via HuggingFace inside your vector manager.
* Set up a local instance of **Ollama** running **Gemma** or configure your remote API keys.
* Define system prompt parameters instructing Agent A to prioritize structural files (e.g., configurations, routing files, main controllers) during initial scans.

### Step 4: Develop Frontend Interface

* Set up a React app using Vite.
* Implement a stateful chat interface that establishes a persistent standard JavaScript native `WebSocket` connection to `ws://localhost:8000/api/v1/chat`.
* Append incoming message fragments seamlessly into the viewport array to mimic real-time typing generation.

### Step 5: Containerize via Docker Compose

Write a multi-container routing definition mapping environment context variables so the frontend knows exactly where to find the exposed gateway APIs:

```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    volumes:
      - ./backend:/app
      - repo_storage:/tmp/repos
    environment:
      - VECTOR_DB_DIR=/tmp/chroma

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend

volumes:
  repo_storage:

```

---

## 4. Curated Documentation & Resource Directory

To successfully write this code from scratch, rely heavily on these primary reference sources:

### Core Frameworks

* **FastAPI Documentation:** [fastapi.tiangolo.com](https://fastapi.tiangolo.com/) (Focus on *Background Tasks* and *WebSockets*).
* **LangChain Expression Language (LCEL):** [python.langchain.com](https://python.langchain.com/) (Focus on *Vector stores*, *Code Text Splitter*, and *Agents*).

### Data & Vector Infrastructure

* **ChromaDB Reference:** [docs.trychroma.com](https://docs.trychroma.com/) (Focus on local persistent client storage).
* **GitPython Docs:** [gitpython.readthedocs.io](https://gitpython.readthedocs.io/) (Focus on programmatic clone operations).

### Models & Framework Integration

* **Ollama API Integration:** [github.com/ollama/ollama](https://github.com/ollama/ollama) (For downloading and orchestrating your LLM locally).
* **HuggingFace Embeddings:** [huggingface.co/sentence-transformers/all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) (The standard model used for indexing code context fragments).
