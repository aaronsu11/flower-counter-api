from flask import Blueprint, jsonify, request
from . import db, storage
from .models import Images
from .counter import count_flower
from .summarizer import summarize
from .messager import email_message


api = Blueprint("api", __name__)

# Only use when first run -> init or potentially reset database
@api.route("/create_table", methods=["POST"])
def debug():
    admin_info = request.get_json()
    username = admin_info["username"]
    password = admin_info["password"]
    if (username == "admin") and (password == "db_init"):
        db.create_all()
    return jsonify("Init Successful"), 201


@api.route("/add_task", methods=["POST"])
def add_task():
    task_info = request.get_json()

    userid = task_info["userid"]
    batchid = task_info["batchid"]
    path = task_info["path"]
    name = task_info["name"]

    # Delete duplicate records
    old_tasks = (
        db.session.query(Images)
        .filter_by(userid=userid)
        .filter_by(path=path)
        .filter_by(name=name)
        # .order_by(Images.id.desc())
        # .first()
    )

    for task in old_tasks:
        if task.status != "deleted":
            task.status = "deleted"
    db.session.commit()

    # Add record in database
    new_task = Images(userid=userid, batchid=batchid, path=path, name=name)
    db.session.add(new_task)
    db.session.commit()
    # taskid = new_task.id

    # Processing
    image_url = storage.child(path + name).get_url(None)
    result = count_flower(image_url)
    # result = 1

    # Update database
    # setattr(new_task, "result", "processed")
    new_task.status = "processed"
    new_task.result = result
    db.session.commit()

    return jsonify(
        {
            "id": new_task.id,
            "batchid": batchid,
            "path": path,
            "name": name,
            "result": result,
        }
    )
    # return jsonify({"status": "success"}), 201


@api.route("/report", methods=["POST"])
def get_report():
    batch_info = request.get_json()
    userid = batch_info["userid"]
    batchid = batch_info["batchid"]
    email = batch_info["email"]
    date = batch_info["date"]
    variety = batch_info["variety"]
    el_stage = batch_info["el_stage"]
    vineyard = batch_info["vineyard"]
    block_id = batch_info["block_id"]
    sendEmail = batch_info["sendEmail"]
    # path = batch_info["path"]
    if userid == 0:
        path = f"images/{userid}/{email}/{vineyard}/{block_id}/{variety}@{el_stage}/{date}/"
    else:
        path = f"images/{userid}/{vineyard}/{block_id}/{variety}@{el_stage}/{date}/"

    if batchid:
        task_list = (
            Images.query.filter_by(userid=userid).filter_by(batchid=batchid).all()
        )
    else:
        task_list = Images.query.filter_by(userid=userid).filter_by(path=path).all()

    results = []
    for task in task_list:
        results.append(task.result)

    summary = summarize(results)

    if sendEmail:
        summary["batch_info"] = batch_info
        email_message(summary)

    return jsonify({"summary": summary}), 201


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
