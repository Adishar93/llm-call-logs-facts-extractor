import re
import json
import requests
import threading
from flask import Flask, request, jsonify
from openai import OpenAI

app = Flask(__name__)

processing = False
g_question = ""
g_facts = []


# Utility functions
def download_document(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.content
        else:
            return None
    except Exception as e:
        print("Error downloading document:", e)
        return None


def preprocess_call_log(call_log):
    lines = call_log.split("\n")
    processed_lines = []
    timestamp_pattern = re.compile(
        r"^\d{2}:\d{2}:\d{2},\d{3}\s+-->\s+\d{2}:\d{2}:\d{2},\d{3}$"
    )
    for line in lines:
        if timestamp_pattern.match(line.strip()):
            continue  # Skip lines with timestamp
        processed_lines.append(line.strip())
    return "\n".join(processed_lines)


# Business Logic
def start_processing_data(question, document_links):
    global processing, g_facts
    processing = True
    downloaded_documents = []

    for doc_url in document_links:
        doc_url = doc_url.strip("<>")
        document = download_document(doc_url)
        if document:
            downloaded_documents.append(document)
        else:
            print("Failed to download document from:", doc_url)

    question_prompt = f"[question]: {question}\n"
    call_log_prompt = ""
    system_prompt = "You are a function which takes a [question] and a [call logs] string array as input, and analyze each [call log] in sequence to determine the concrete facts to the [question] and write as bullet points. Do not focus on delayed or on hold decisions, focus solely on the concrete decisions. Do not add additional text as it can break the code reading the function output. While processing each [call log] in sequence, make sure you combine facts about the same topic. For example, call log 1 fact: -decided to go with pink theme, call log 2 fact: -decided to add purple theme -> should be combined into -decided to give pink and purple theme."

    for i, document in enumerate(downloaded_documents, start=1):
        call_log = preprocess_call_log(document.decode("utf-8"))
        call_log_prompt += f"[call log {i}]:\n {call_log}\n"
    
    #handle case where call log may be empty
    if call_log_prompt:
      client = OpenAI()
      completion = client.chat.completions.create(
          model="gpt-4-turbo",
          max_tokens=100,
          messages=[
              {
                  "role": "system",
                  "content": system_prompt,
              },
              {"role": "user", "content": question_prompt + call_log_prompt},
          ],
      )

      # print(completion.choices[0].message)
      content = completion.choices[0].message.content
      points = content.split("\n- ")
      # Remove empty strings and "-" from each point
      g_facts = [point.strip().replace("-", "") for point in points if point.strip()]
      processing = False
    else:
      g_facts = []
      processing = False


# Flask API Endpoints
class GetQuestionAndFactsResponse:
    def __init__(self, question, facts, status):
        self.question = question
        self.facts = facts
        self.status = status

    def to_dict(self):
        return {"question": self.question, "facts": self.facts, "status": self.status}


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
    global processing, g_question, g_facts
    response = ""

    if processing:
        response = GetQuestionAndFactsResponse(
            question=g_question, facts=[], status="processing"
        )
    else:
        response = GetQuestionAndFactsResponse(
            question=g_question, facts=g_facts, status="done"
        )

    return app.response_class(
        response=json.dumps(response.to_dict(), sort_keys=False),
        status=200,
        mimetype="application/json",
    )


if __name__ == "__main__":
    app.run(debug=True)

# from openai import OpenAI
# client = OpenAI()
# completion = client.chat.completions.create(
#   model="gpt-4-turbo",
#   max_tokens = 100,
#   messages=[
#     {"role": "system", "content": "You are a function which takes a [question] and a [call logs] string array as input, and analyze each [call log] in sequence to determine the concrete facts to the [question] and write as bullet points. Do not focus on delayed or on hold decisions, focus solely on the concrete decisions. Do not additional text as it can break the code reading the function output. While processing each [call log] in sequence, make sure you combine facts about the same topic. For example, call log 1 fact: -decided to go with pink theme, call log 2 fact: -decided to add purple theme -> should be combined into -decided to give pink and purple theme. "},
#     {"role": "user", "content": '''[Question]: What are our product design decisions?
#      [Call Log 1]:
#      1
# 00:01:11,430 --> 00:01:40,520
# John: Hello, everybody. Let's start with the product design discussion. I think we should go with a modular design for our product. It will allow us to easily add or remove features as needed.

# 2
# 00:01:41,450 --> 00:01:49,190
# Sara: I agree with John. A modular design will provide us with the flexibility we need. Also, I suggest we use a responsive design to ensure our product works well on all devices. Finally, I think we should use websockets to improve latency and provide real-time updates.

# 3
# 00:01:49,340 --> 00:01:50,040
# Mike: Sounds good to me. I also propose we use a dark theme for the user interface. It's trendy and reduces eye strain for users. Let's hold off on the websockets for now since it's a little bit too much work.
#      [Call Log 2]:
#      1
# 00:01:11,430 --> 00:01:40,520
# John: After giving it some more thought, I believe we should also consider a light theme option for the user interface. This will cater to users who prefer a brighter interface.

# 2
# 00:01:41,450 --> 00:01:49,190
# Sara: That's a great idea, John. A light theme will provide an alternative to users who find the dark theme too intense.

# 3
# 00:01:49,340 --> 00:01:50,040
# Mike: I'm on board with that.
# '''}
#   ]
# )

# print(completion.choices[0].message)
