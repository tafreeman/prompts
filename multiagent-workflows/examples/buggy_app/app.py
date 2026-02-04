from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/contact", methods=["POST"])
def contact():
    data = request.json
    message = data.get("message", "")

    # Bug: This crashes if message contains non-ascii characters because we try to encode it as ascii
    # for some legacy processing reason
    processed_message = message.encode("ascii")

    return jsonify({"status": "received", "length": len(processed_message)})


if __name__ == "__main__":
    app.run(debug=True)
