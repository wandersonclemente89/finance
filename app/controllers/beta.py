from app import app
from flask import request, jsonify
from finance.calculation import Beta


@app.route('/stock/beta', methods=["POST"])
def stock_beta():
    req_data = request.get_json()
    stock_list = req_data['stock']
    return jsonify(
        stockBeta=Beta.stock_beta(stock_list)
    )
