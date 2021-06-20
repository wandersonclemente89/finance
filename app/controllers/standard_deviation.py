from app import app
from flask import request, jsonify
from finance.calculation import StandardDeviation


@app.route('/stock/risk', methods=["POST"])
def standard_deviation():
    req_data = request.get_json()
    stock_list = req_data['stockList']
    start_date = req_data['startDate']
    return jsonify(
        stockRisk=StandardDeviation.standard_deviation(stock_list, start_date)
    )


@app.route('/portfolio/risk', methods=["POST"])
def portfolio_risk():
    req_data = request.get_json()
    stock_list = req_data['stockList']
    start_date = req_data['startDate']
    return jsonify(
        portfolioRisk=StandardDeviation.portfolio_risk(stock_list, start_date)
    )

