import re
from openai import OpenAI
from utility import download_document, preprocess_call_log, clean_facts
import shared_variables


# Business Logic
def start_processing_data(question, document_links):
    shared_variables.processing = True
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
    system_prompt = "You are a function which takes a [question] and a [call logs] string array as input, and analyze each [call log] in sequence to determine the concrete facts to the [question] and write as bullet points. Do not focus on delayed or on hold decisions or 'not' type of decisions, focus solely on the concrete decisions. Do not add additional text as it can break the code reading the function output. While processing each [call log] in sequence, make sure you update facts about the same feature. For example, call log 1 fact: '-The team has decided to go with pink theme.', call log 2 fact: '-The team has decided to add purple theme.' should be updated to the fact: '-The team has decided to go with pink and purple theme'. Avoid two facts per line example fact: '-The team has decided on a subscription-based pricing model at $100 per month, with a 30-day free trial.' should be two facts: '-The team has decided on a subscription-based pricing model at $100 per month' \n '-The team has decided on a 30-day free trial.'"

    for i, document in enumerate(downloaded_documents, start=1):
        call_log = preprocess_call_log(document.decode("utf-8"))
        call_log_prompt += f"[call log {i}]:\n {call_log}\n"

    # handle case where call log may be empty
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
            temperature=0.2,
        )

        content = completion.choices[0].message.content
        points = content.split("\n- ")
        shared_variables.g_facts = clean_facts(points)
        shared_variables.processing = False
    else:
        shared_variables.g_facts = []
        shared_variables.processing = False
