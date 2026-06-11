import os
import random

from flask import Flask, jsonify
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)

# prometheus_flask_exporter tự động:
# - tạo endpoint /metrics
# - đếm số request
# - đo thời gian xử lý request
# - gắn nhãn method, status, endpoint
PrometheusMetrics(app)

# ERROR_RATE dùng để giả lập lỗi.
# Ví dụ:
#   ERROR_RATE=0   => không cố tình tạo lỗi
#   ERROR_RATE=0.5 => khoảng 50% request trả về HTTP 500
ERR = float(os.getenv("ERROR_RATE", "0"))

# VERSION dùng để phân biệt version app khi canary.
# Ví dụ v1 là bản cũ, v2 là bản mới.
VER = os.getenv("VERSION", "v1")

@app.get("/")
def index():
    if random.random() < ERR:
        return jsonify(error="injected", version=VER), 500

    return jsonify(ok=True, version=VER), 200

@app.get("/healthz")
def healthz():
    return "ok", 200