from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# ✅ 환경변수에 저장된 OpenAI API 키 불러오기
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        data = request.get_json()
        user_text = data.get("text", "")

        if not user_text:
            return jsonify({"error": "No input text provided."}), 400

        # GPT에게 감정 점수 및 위로 메시지를 생성하도록 요청
        prompt = f"""
        너는 감정 분석을 수행하는 AI야. 사용자의 문장을 분석해서 감정 점수를 0.0~1.0 사이로 판단하고,
        해당 감정에 어울리는 위로 메시지를 작성해. 다음 형식의 JSON으로 출력해:
        {{"score": float, "sentiment": "string"}}

        예시 입력: "아 진짜 너무 힘들고 우울해"
        예시 출력: {{"score": 0.87, "sentiment": "많이 힘들었죠. 당신의 마음을 이해해요."}}

        이제 다음 문장을 분석해줘:
        문장: "{user_text}"
        """

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "너는 감정 분석기 역할을 해."},
                {"role": "user", "content": prompt}
            ]
        )

        reply = response['choices'][0]['message']['content']

        # JSON 형식 파싱
        result = eval(reply.strip())

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

