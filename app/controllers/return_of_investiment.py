from app import app
from flask import request, jsonify
from finance.calculation import ReturnOfInvestment


@app.route('/stock/roi', methods=["POST"])
def stock_return():
    req_data = request.get_json()
    stock = req_data['stock']
    start_date = req_data['startDate']
    mean_type = req_data['meanType']
    return jsonify(
        historicalReturn=ReturnOfInvestment.stock_return(stock, start_date, mean_type)
    )


@app.route('/portfolio/roi', methods=["POST"])
def stock_portfolio_return():
    req_data = request.get_json()
    stock_list = req_data['stockList']
    start_date = req_data['startDate']
    return jsonify(
        historicalReturn=ReturnOfInvestment.stock_portfolio_return(stock_list, start_date)
    )

@app.route('/stock/capm', methods=["POST"])
def equity_return():
    req_data = request.get_json()
    stock = req_data['stock']
    erp = req_data['equityRiskPremium']
    ipca = req_data['riskFreeTax']
    return jsonify(
        expectedEquityReturn=ReturnOfInvestment.equity_return(stock, erp, ipca)
    )
