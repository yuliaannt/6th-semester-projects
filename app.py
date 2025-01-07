from flask import Flask, render_template, request, jsonify

import response_generator

# from waitress import serve

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/get")
def get_bot_response():
    message = request.args.get("msg")
    print(f"Message received: {message}")  # debuging
    response = ""
    if message:
        response = response_generator.generate_response(message)
        print(f"Response generated: {response}")  # debbuging
        return str(response)
    else:
        return "Missing Data!"


if __name__ == "__main__":
    app.run()

    # serve(app, host="mongodb://localhost", port=27017)
