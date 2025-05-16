from flask import Flask, request, jsonify
import openai
import os
import json

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/")
def index():
    return "AIPK 감정 분석 API 서버입니다."

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "텍스트가 필요합니다."}), 400

    prompt = f"""
    다음 문장을 감정적으로 분석해서 0.0부터 1.0 사이의 점수(score)를 매기고, 
    그에 맞는 위로 멘트(sentiment)를 함께 작성해주세요. 
    아래 형식의 JSON으로만 응답해 주세요:

    {{
        "score": (0.0 ~ 1.0 숫자),
        "sentiment": "위로 멘트"
    }}

    문장: "{data['text']}"
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        result = response.choices[0].message.content.strip()

        # GPT 응답을 JSON으로 파싱
        result_json = json.loads(result)

        return jsonify(result_json)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
