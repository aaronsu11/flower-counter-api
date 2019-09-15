from flask import Blueprint, jsonify

api = Blueprint("api", __name__)


@api.route("/add_task", methods=["POST"])
def add_task():
    return jsonify({"status": "success"}), 201


@api.route("/process_tasks")
def process_tasks():
    return jsonify({"status": "done"}), 201


@api.route("/results")
def results():
    return jsonify({"results": []}), 201

