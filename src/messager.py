from flask_mail import Message
from flask import render_template
from . import mail


def email_message(summary):
    email = summary["batch_info"]["email"]
    vineyard = summary["batch_info"]["vineyard"]
    block_name = summary["batch_info"]["block_id"]
    msg = Message(
        subject=f"Results for Vineyard {vineyard}, Block {block_name} from UNSW Flower Counting System ",
        recipients=[email],
        reply_to="vyepproject@gmail.com",
    )
    # msg.html = f"<b> Hello Test </b><p>The result is {MEAN}</p>"
    msg.html = render_template("email.html", summary=summary)
    mail.send(msg)
    return summary
