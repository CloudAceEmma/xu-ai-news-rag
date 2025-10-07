import os
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader, PyPDFLoader, UnstructuredExcelLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from backend.services.embedding import LlamaServerEmbeddings
from backend.models import db, Document
from backend.config import Config
from backend.auth.routes import get_current_user_id

def get_user_faiss_index_path(user_id):
    """Constructs the path for a user's FAISS index."""
    return os.path.join(Config.FAISS_INDEX_PATH, f"user_{user_id}")

def add_document_to_kb(file_path, document_type, source=None, tags=None):
    """
    Adds a document to the knowledge base: loads, chunks, embeds,
    and stores it in a user-specific FAISS vector store.
    """
    user_id = get_current_user_id()
    if not user_id:
        raise ValueError("User identity not found in JWT token.")

    # 1. Load the document
    if document_type == 'txt':
        loader = TextLoader(file_path)
    elif document_type == 'pdf':
        loader = PyPDFLoader(file_path)
    elif document_type == 'xlsx':
        loader = UnstructuredExcelLoader(file_path)
    else:
        raise ValueError(f"Unsupported document type: {document_type}")
    
    documents = loader.load()

    # 2. Chunk the document
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = text_splitter.split_documents(documents)
    
    # 3. Create vector embeddings
    embeddings = LlamaServerEmbeddings()

    # 4. Store in FAISS vector store
    index_path = get_user_faiss_index_path(user_id)
    
    if os.path.exists(index_path):
        # Load existing vector store and add new documents
        vector_store = FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)
        vector_store.add_documents(docs)
    else:
        # Create a new vector store
        vector_store = FAISS.from_documents(docs, embeddings)

    vector_store.save_local(index_path)

    # 5. Save metadata to database
    new_doc = Document(
        user_id=user_id,
        file_path=file_path,
        document_type=document_type,
        source=source,
        tags=tags
    )
    db.session.add(new_doc)
    db.session.commit()
    
    return new_doc

def delete_document_from_kb(doc_id):
    """
    Deletes a document from the knowledge base.
    Note: This only deletes the metadata. The vectors in FAISS are not removed
    to avoid complexity. A full implementation would require rebuilding the index.
    """
    doc = Document.query.get(doc_id)
    if not doc:
        return False
    
    # For simplicity, we only delete the metadata and the file.
    # A robust implementation would also remove the corresponding vectors from FAISS.
    if os.path.exists(doc.file_path):
        os.remove(doc.file_path)
        
    db.session.delete(doc)
    db.session.commit()
    return True

def update_document_metadata(doc_id, source=None, tags=None):
    """Updates the metadata of a document."""
    doc = Document.query.get(doc_id)
    if not doc:
        return None
    
    if source is not None:
        doc.source = source
    if tags is not None:
        doc.tags = tags
        
    db.session.commit()
    return doc
