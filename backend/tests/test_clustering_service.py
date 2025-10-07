import os
from unittest.mock import patch
from backend.services.clustering import generate_cluster_report
from backend.models import db, Document, User

def test_generate_cluster_report(app):
    """Test the cluster report generation service."""
    with app.app_context():
        # Setup a user and some documents
        user = User(username="cluster_user", password_hash="test")
        db.session.add(user)
        db.session.commit()

        # Create dummy files
        os.makedirs("test_docs", exist_ok=True)
        doc1_path = "test_docs/doc1.txt"
        doc2_path = "test_docs/doc2.txt"
        with open(doc1_path, "w") as f:
            f.write("This is a document about python and data science.")
        with open(doc2_path, "w") as f:
            f.write("This document discusses machine learning and python.")

        doc1 = Document(user_id=user.id, file_path=doc1_path, document_type="txt")
        doc2 = Document(user_id=user.id, file_path=doc2_path, document_type="txt")
        db.session.add_all([doc1, doc2])
        db.session.commit()

        # Generate the report
        report = generate_cluster_report(user.id, n_clusters=2)
        
        assert "Cluster 1" in report
        assert "Cluster 2" in report
        assert "python" in report["Cluster 1"] or "python" in report["Cluster 2"]

        # Clean up dummy files
        os.remove(doc1_path)
        os.remove(doc2_path)
        os.rmdir("test_docs")

def test_generate_cluster_report_not_enough_documents(app):
    """Test cluster report generation with insufficient documents."""
    with app.app_context():
        user = User(username="cluster_user_2", password_hash="test")
        db.session.add(user)
        db.session.commit()

        report = generate_cluster_report(user.id, n_clusters=5)
        assert "error" in report
        assert "Not enough documents" in report["error"]
