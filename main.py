import json
import threading
import shared_variables
from contract import GetQuestionAndFactsResponse
from processing import start_processing_data
from dotenv import load_dotenv
from flask import Flask, request, jsonify

# Loading API credentials
load_dotenv()

# global and shared variables
global g_question
g_question = ""
shared_variables.init()

# Flask Server
app = Flask(__name__)

# Endpoints
@app.route("/submit_question_and_documents", methods=["POST"])
def submit_question_and_documents():
    global g_question
    data = request.get_json()
    question = data.get("question")
    document_links = data.get("documents")
    g_question = question
    thread = threading.Thread(
        target=start_processing_data, args=(question, document_links)
    )
    thread.start()
    return jsonify({"message": "Request received successfully"}), 200


@app.route("/get_question_and_facts", methods=["GET"])
def get_question_and_facts():
    global g_question
    response = ""

    if shared_variables.processing:
        response = GetQuestionAndFactsResponse(
            question=g_question, facts=[], status="processing"
        )
    else:
        response = GetQuestionAndFactsResponse(
            question=g_question, facts=shared_variables.g_facts, status="done"
        )

    return app.response_class(
        response=json.dumps(response.to_dict(), sort_keys=False),
        status=200,
        mimetype="application/json",
    )


if __name__ == "__main__":
    app.run(debug=False)
