from flask import Blueprint, jsonify, request
from flask_mail import Message
from . import db, storage, mail
from .models import Images
from .counter import count_flower
from .estimator import estimate_yield


api = Blueprint("api", __name__)


@api.route("/")
def debug():
    return jsonify("Running"), 201


@api.route("/add_task", methods=["POST"])
def add_task():
    task_info = request.get_json()

    userid = task_info["userid"]
    path = task_info["path"]
    name = task_info["name"]

    # Add record in database
    new_task = Images(userid=userid, path=path, name=name)
    db.session.add(new_task)
    db.session.commit()
    # taskid = new_task.id

    # Processing
    image_url = storage.child(path + name).get_url(None)
    result = count_flower(image_url)
    # result = 1

    # Update database
    # setattr(new_task, "result", "processed")
    new_task.processed = True
    new_task.result = result
    db.session.commit()

    return jsonify(
        {
            "id": new_task.id,
            "path": path,
            "name": name,
            "processed": True,
            "result": result,
        }
    )
    # return jsonify({"status": "success"}), 201


# @api.route("/process_tasks/<userid>")
# def process_tasks(userid):
#     return jsonify({"status": "done"}), 201


@api.route("/report", methods=["POST"])
def get_report():
    batch_info = request.get_json()
    userid = batch_info["userid"]
    email = batch_info["email"]
    path = batch_info["path"]
    task_list = Images.query.filter_by(userid=userid).filter_by(path=path).all()

    results = []
    for task in task_list:
        results.append(task.result)

    estimate = estimate_yield(results)

    msg = Message(subject="Report", recipients=[email])
    msg.html = f"<b> Hello Test </b><p>The result is {estimate}</p>"
    mail.send(msg)

    return jsonify({"results": results, "sum": estimate}), 201


@api.route("/results/<userid>")
def results(userid):
    if userid == "admin":
        task_list = Images.query.all()
    else:
        task_list = Images.query.filter_by(userid=userid).all()

    results = []
    for task in task_list:
        results.append(
            {
                "path": task.path,
                "name": task.name,
                "processed": task.processed,
                "result": task.result,
            }
        )
    return jsonify({"results": results}), 201


@api.route("/reset", methods=["POST"])
def reset_database():
    admin_info = request.get_json()
    username = admin_info["username"]
    password = admin_info["password"]
    if (username == "admin") and (password == "reset"):
        Images.query.delete()
        # db.session.query(Model).delete()
        db.session.commit()

    return jsonify("success"), 201
