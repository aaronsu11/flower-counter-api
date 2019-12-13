from flask import Blueprint, jsonify, request
from datetime import datetime
from . import db, storage
from .models import Images, Parameters
from .counter import counterWrapper
from .summarizer import summarize
from .messager import email_message


api = Blueprint("api", __name__)


@api.route("/")
def serverCheck():
    """Return a friendly HTTP greeting."""
    return "Server Running"


@api.route("/algorithm_test")
def algorithmTest():
    # Processing
    image_url = storage.child("test.jpg").get_url(None)
    result, message = counterWrapper(image_url)
    return f"Result: {result}, Status: {message}"


# Only use when first run -> init or potentially reset database
@api.route("/create_table", methods=["POST"])
def debug():
    admin_info = request.get_json()
    username = admin_info["username"]
    password = admin_info["password"]
    message = ""
    if (username == "admin") and (password == "db_init"):
        db.create_all()
        message = "Init Successful"
    else:
        message = "Init Fail"
    return jsonify(message), 201


@api.route("/add_task", methods=["POST"])
def add_task():
    task_info = request.get_json()

    userid = task_info["userid"]
    batchid = task_info["batchid"]
    path = task_info["path"]
    label = task_info["label"]
    vineyard = task_info["vineyard"]
    block = task_info["block"]
    date = task_info["date"]
    date = datetime.strptime(date, "%Y-%m-%d").date()
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
    new_task = Images(
        userid=userid,
        batchid=batchid,
        path=path,
        vineyard=vineyard,
        block=block,
        date=date,
        name=name,
    )
    db.session.add(new_task)
    db.session.commit()

    # Processing
    image_url = storage.child(path + name).get_url(None)
    result, error_msg = counterWrapper(image_url)
    # result = 1

    params = Parameters.query.filter_by(label=label).first()
    if params:
        slope = float(params.slope)
        intercept = float(params.intercept)
        message = "model found"
        # slope = 100
        # intercept = 0
    else:
        slope = 1
        intercept = 0
        message = "model not exists"

    estimate = result * slope + intercept

    # Update database
    # setattr(new_task, "result", "processed")
    new_task.status = "processed"
    new_task.result = float(result)
    new_task.estimate = float(estimate)
    db.session.commit()

    return jsonify(
        {"id": new_task.id, "result": result, "message": message, "estimate": estimate}
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
        results.append(float(task.result))

    summary = summarize(results)

    if sendEmail:
        summary["batch_info"] = batch_info
        email_message(summary)

    return jsonify({"summary": summary}), 201


@api.route("/list", methods=["POST"])
def get_list():
    request_info = request.get_json()
    userid = request_info["userid"]
    filter_type = request_info["type"]
    filter_content = request_info["content"]
    filter_content_extra = request_info["content_extra"]

    if filter_type == "vineyardls":
        section_list = (
            db.session.query(Images.vineyard).filter_by(userid=userid).distinct()
        )
    elif filter_type == "datels":
        section_list = (
            db.session.query(Images.date)
            .filter_by(userid=userid)
            .filter_by(vineyard=filter_content)
            .distinct()
        )
    elif filter_type == "blockls":
        section_list = (
            db.session.query(Images.block)
            .filter_by(userid=userid)
            .filter_by(vineyard=filter_content)
            .distinct()
        )
    elif filter_type == "date":
        task_list = (
            Images.query.filter_by(userid=userid)
            .filter_by(status="processed")
            .filter_by(vineyard=filter_content)
            .filter_by(date=filter_content_extra)
        )
    elif filter_type == "block":
        task_list = (
            Images.query.filter_by(userid=userid)
            .filter_by(vineyard=filter_content)
            .filter_by(block=filter_content_extra)
        )
    else:
        return jsonify("Invalid Filter Type")
    # else:
    #     task_list = Images.query.filter_by(userid=userid).filter(
    #         Images.path.contains(filter_content)
    #     )

    records = []

    if filter_content_extra:
        estimates = []
        for task in task_list:
            estimates.append(float(task.estimate))
            records.append(
                {"name": task.name, "path": task.path, "estimate": float(task.estimate)}
            )
        summary = summarize(estimates)
        return jsonify({"summary": summary, "records": records}), 201
    else:
        for section in section_list:
            records.append(section[0])
        return jsonify({"summary": None, "records": records}), 201


@api.route("/results/<userid>")
def results(userid):
    if userid == "admin":
        task_list = Images.query.all()
    else:
        task_list = Images.query.filter_by(userid=userid).all()

    results = []
    for task in task_list:
        results.append(
            {"name": task.name, "status": task.status, "result": float(task.result)}
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
