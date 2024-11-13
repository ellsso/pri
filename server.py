from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

# MongoDB 설정
client = MongoClient("mongodb://localhost:27017/")
db = client["motionSensorDB"]
collection = db["motionData"]

@app.route("/api/motion-data", methods=["POST"])
def save_motion_data():
    data = request.json.get("motionData", [])
    if data:
        # 데이터에 타임스탬프 추가
        for entry in data:
            entry["received_at"] = datetime.utcnow()  # 수신 시간 추가
        
        # MongoDB에 데이터 저장
        collection.insert_many(data)
        return jsonify({"status": "success", "message": "Data saved"}), 200
    
    return jsonify({"status": "error", "message": "No data received"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
