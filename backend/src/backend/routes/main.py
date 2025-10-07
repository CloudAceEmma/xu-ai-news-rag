from flask import Blueprint, request, jsonify
import os
from datetime import datetime
from werkzeug.utils import secure_filename
from backend.auth.routes import token_required, get_current_user_id
from backend.services.knowledge_base import (
    add_document_to_kb,
    delete_document_from_kb,
    update_document_metadata
)
from backend.models import Document
from backend.services.search import perform_search, generate_keyword_report
from backend.services.clustering import generate_cluster_report
from backend.services.feeds import add_rss_feed, get_user_feeds, delete_rss_feed
from backend.config import Config

main_bp = Blueprint('main', __name__)
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'xlsx'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main_bp.route('/documents', methods=['POST'])
@token_required
def upload_document(current_user):
    if 'file' not in request.files:
        return jsonify({"msg": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"msg": "No selected file"}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
        
        document_type = filename.rsplit('.', 1)[1].lower()
        source = request.form.get('source')
        tags = request.form.get('tags')

        add_document_to_kb(current_user.id, file_path, document_type, source, tags)
        
        return jsonify({"msg": "File uploaded and processed successfully"}), 201
    return jsonify({"msg": "File type not allowed"}), 400

from datetime import datetime

# ... (imports remain the same)

# ... (file handling functions remain the same)

# ... (upload_document remains the same)

@main_bp.route('/documents', methods=['GET'])
@token_required
def get_documents(current_user):
    query = Document.query.filter_by(user_id=current_user.id)
    
    # Filtering
    doc_type = request.args.get('type')
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')

    if doc_type:
        query = query.filter(Document.document_type == doc_type)
    
    if start_date_str:
        try:
            start_date = datetime.fromisoformat(start_date_str)
            query = query.filter(Document.uploaded_at >= start_date)
        except ValueError:
            return jsonify({"msg": "Invalid start_date format. Use ISO format."}), 400

    if end_date_str:
        try:
            end_date = datetime.fromisoformat(end_date_str)
            query = query.filter(Document.uploaded_at <= end_date)
        except ValueError:
            return jsonify({"msg": "Invalid end_date format. Use ISO format."}), 400

    documents = query.all()
    return jsonify([{
        "id": doc.id,
        "file_path": doc.file_path,
        "document_type": doc.document_type,
        "source": doc.source,
        "tags": doc.tags,
        "uploaded_at": doc.uploaded_at.isoformat()
    } for doc in documents]), 200

@main_bp.route('/documents/<int:doc_id>', methods=['DELETE'])
@token_required
def delete_document(current_user, doc_id):
    if delete_document_from_kb(doc_id):
        return jsonify({"msg": "Document deleted"}), 200
    return jsonify({"msg": "Document not found"}), 404

@main_bp.route('/documents/<int:doc_id>', methods=['PUT'])
@token_required
def update_document(current_user, doc_id):
    data = request.get_json()
    doc = update_document_metadata(doc_id, data.get('source'), data.get('tags'))
    if doc:
        return jsonify({"msg": "Document updated"}), 200
    return jsonify({"msg": "Document not found"}), 404

@main_bp.route('/documents/batch_delete', methods=['POST'])
@token_required
def batch_delete_documents(current_user):
    data = request.get_json()
    doc_ids = data.get('ids')

    if not doc_ids or not isinstance(doc_ids, list):
        return jsonify({"msg": "Invalid request. 'ids' must be a list of document IDs."}), 400

    # Ensure the user can only delete their own documents
    docs_to_delete = Document.query.filter(Document.user_id == current_user.id, Document.id.in_(doc_ids)).all()
    
    if not docs_to_delete:
        return jsonify({"msg": "No matching documents found to delete."}), 404

    for doc in docs_to_delete:
        delete_document_from_kb(doc.id)
    
    return jsonify({"msg": f"Successfully deleted {len(docs_to_delete)} documents."}), 200

@main_bp.route('/search', methods=['POST'])
@token_required
def search(current_user):
    query = request.json.get('query')
    if not query:
        return jsonify({"error": "Query is required"}), 400
    
    result = perform_search(current_user.id, query)
    return jsonify(result)

@main_bp.route('/report/keywords', methods=['GET'])
@token_required
def keywords_report(current_user):
    report = generate_keyword_report(current_user.id)
    return jsonify(report)

@main_bp.route('/report/clustering', methods=['GET'])
@token_required
def clustering_report(current_user):
    report = generate_cluster_report(current_user.id)
    return jsonify(report)

@main_bp.route('/feeds', methods=['POST'])
@token_required
def add_feed(current_user):
    url = request.json.get('url')
    if not url:
        return jsonify({"error": "URL is required"}), 400
    
    feed = add_rss_feed(current_user.id, url)
    if feed:
        return jsonify({"id": feed.id, "url": feed.url}), 201
    return jsonify({"error": "Failed to add feed"}), 500

@main_bp.route('/feeds', methods=['GET'])
@token_required
def get_feeds(current_user):
    feeds = get_user_feeds(current_user.id)
    return jsonify([{"id": f.id, "url": f.url} for f in feeds])

@main_bp.route('/feeds/<int:feed_id>', methods=['DELETE'])
@token_required
def delete_feed(current_user, feed_id):
    if delete_rss_feed(current_user.id, feed_id):
        return jsonify({"message": "Feed deleted"}), 200
    return jsonify({"error": "Feed not found or permission denied"}), 404