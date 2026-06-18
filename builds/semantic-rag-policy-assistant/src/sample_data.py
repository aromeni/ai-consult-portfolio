"""Sample data and paths for the Semantic RAG Policy Assistant."""

import os

DOCS_DIR = os.path.join(
    os.path.dirname(__file__), "..", "data", "synthetic_documents"
)

DEMO_QUERIES = [
    "Can staff enter learner data into AI tools?",
    "What are the safeguarding rules for AI use?",
    "How should staff check AI-generated outputs?",
    "What is the data minimisation requirement?",
    "When should staff ask a manager before using AI?",
]

DEMO_CHUNK_SIZE = 500
DEMO_OVERLAP = 100

PLANNED_PHASES = [
    ("Phase 1", "Document loading, chunking, keyword search, app scaffold"),
    ("Phase 2", "Chunking Explorer — configurable word chunking, section strategy, validation"),
    ("Phase 3", "Local embeddings — sentence-transformers/all-MiniLM-L6-v2, 384-dim vectors"),
    ("Phase 4", "FAISS vector index — IndexFlatIP (cosine) and IndexFlatL2, save/load"),
    ("Phase 5", "Semantic search — query embedding, FAISS retrieval, ranked results"),
    ("Phase 6", "RAG Q&A — intent detection, grounded answers, evidence summary, download"),
    ("Phase 7", "Retrieval comparison — keyword vs semantic, overlap detection, insight"),
    ("Phase 8", "Mini Answer Report — 10-section Markdown report, reviewer notes, download"),
]
