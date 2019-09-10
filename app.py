from flask import Flask, request, redirect

app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        return "Got it!"
        # return redirect('/')
    else:
        return "Hello, World !"


@app.route("/home/<int:id>")
def home(id):
    return "Home Page"


if __name__ == "__main__":
    app.run(debug=True)
