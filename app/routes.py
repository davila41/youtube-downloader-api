from flask import Blueprint, request, jsonify, send_file
from app.downloader import download_video

bp = Blueprint("api", __name__)

@bp.route("/download", methods=["POST"])
def download():
    data = request.get_json()
    url = data.get("url")
    format_type = data.get("format", "mp3").lower()

    if not url:
        return jsonify({"error": "URL não fornecida"}), 400

    try:
        filepath = download_video(url, format_type)
        return send_file(filepath, as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
