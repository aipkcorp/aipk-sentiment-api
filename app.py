from flask import Flask, request, jsonify
from transformers import pipeline
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

classifier = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")

@app.route('/')
def home():
    return 'AIPK 감정 분석 서버 실행 중입니다.'

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        text = data.get("text", "")
        if not text:
            return jsonify({"error": "No text provided"}), 400

        result = classifier(text)[0]
        label = result['label']
        score = round(float(result['score']), 3)
        emotion = "긍정" if "4" in label or "5" in label else "부정"

        return jsonify({
            "emotion": emotion,
            "score": score,
            "raw_label": label
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run()