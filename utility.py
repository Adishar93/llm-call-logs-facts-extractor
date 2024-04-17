import re
import requests


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


# Remove leading or trailing symbols except fullstop at the end
def clean_facts(points):
    return [
        re.sub(r"^[^\w\s]*|[^\w\s]*[^.]$", "", point).strip()
        for point in points
        if point.strip()
    ]
