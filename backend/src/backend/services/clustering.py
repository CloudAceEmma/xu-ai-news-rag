from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from backend.models import Document
import numpy as np

def generate_cluster_report(user_id, n_clusters=5):
    """
    Generates a cluster report for a user's documents using TF-IDF and K-Means.
    """
    docs = Document.query.filter_by(user_id=user_id).all()
    if not docs or len(docs) < n_clusters:
        return {"error": "Not enough documents to generate a cluster report."}

    # For simplicity, we'll read the content from the files.
    # A more optimized approach would be to store content in the database or a cache.
    doc_contents = []
    for doc in docs:
        try:
            with open(doc.file_path, 'r', encoding='utf-8') as f:
                doc_contents.append(f.read())
        except Exception as e:
            print(f"Could not read file {doc.file_path}: {e}")
            # Skip files that can't be read
            continue

    if not doc_contents or len(doc_contents) < n_clusters:
        return {"error": "Not enough readable documents to generate a cluster report."}

    # Vectorize the documents
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(doc_contents)

    # Perform clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    kmeans.fit(X)

    # Get top terms per cluster
    order_centroids = kmeans.cluster_centers_.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names_out()
    
    report = {}
    for i in range(n_clusters):
        top_terms = [terms[ind] for ind in order_centroids[i, :10]]
        report[f"Cluster {i+1}"] = top_terms
        
    return report
