from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

def is_valid_url(url):
    try:
        response = requests.head(url, timeout=0.5)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def get_numbers_from_url(url):
    try:
        response = requests.get(url, timeout=0.5)
        if response.status_code == 200:
            data = response.json()
            return data.get("numbers", [])
        else:
            return []
    except requests.exceptions.RequestException:
        return []

@app.route('/numbers', methods=['GET'])
def get_merged_numbers():
    input_urls = request.args.getlist('url')
    merged_numbers = list()

    for url in input_urls:
        if is_valid_url(url):
            numbers = get_numbers_from_url(url)
            merged_numbers.extend(numbers)

    response_data = {"numbers": sorted(list(set(merged_numbers)))}
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(port=8008)


