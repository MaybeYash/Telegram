from flask import Flask, render_template, request, jsonify
import requests
from datetime import datetime

app = Flask(__name__, template_folder="../templates")

def get_creation_date(id: int) -> str:
    url = "https://restore-access.indream.app/regdate"
    headers = {
        "accept": "*/*",
        "content-type": "application/x-www-form-urlencoded",
        "user-agent": "Nicegram/92 CFNetwork/1390 Darwin/22.0.0",
        "x-api-key": "e758fb28-79be-4d1c-af6b-066633ded128",
        "accept-language": "en-US,en;q=0.9"
    }
    data = {"telegramId": id}
    response = requests.post(url, headers=headers, json=data).json()
    if 'data' in response and 'date' in response['data']:
        return response['data']['date']
    return "N/A"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_join_date', methods=['POST'])
def get_join_date():
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        join_date = get_creation_date(user_id)
        if join_date == "N/A":
            return jsonify({"message": "Could not retrieve your join date."}), 400
        join_year, join_month = map(int, join_date.split('-'))
        join_date_obj = datetime(join_year, join_month, 1)
        now = datetime.now()
        diff_years = now.year - join_date_obj.year
        diff_months = now.month - join_date_obj.month
        if diff_months < 0:
            diff_years -= 1
            diff_months += 12
        if diff_years > 0:
            message = f"You Joined Telegram Approximately {diff_years} year{'s' if diff_years > 1 else ''} and {diff_months} month{'s' if diff_months > 1 else ''} ago!"
        else:
            message = f"You Joined Telegram Approximately {diff_months} month{'s' if diff_months > 1 else ''} ago!"
        return jsonify({"message": message})
    except Exception as e:
        return jsonify({"message": str(e)}), 500

app = app
