from app import app
from flask import request, jsonify
from finance.calculation import CashFlow

@app.route('/stock/price', methods=["POST"])
def stock_price():
    req_data = request.get_json()
    stock = req_data['stock']
    erp = req_data['equityRiskPremium']
    riskFreeTax = req_data['riskFreeTax']
    freeCashFlow = req_data['freeCashFlow']
    payout = req_data['payout']
    roe = req_data['roe']
    costOfThirdPartiesCapital = req_data['costOfThirdPartiesCapital']
    percentageOfThirdPartiesCapital = req_data['percentageOfThirdPartiesCapital']
    indebtedness = req_data['indebtedness']
    g = req_data['g']
    numberOfYears = req_data['numberOfYears']
    numberOfStocks = req_data['numberOfStocks']
    resp = CashFlow.fdc(stock, erp, riskFreeTax, freeCashFlow, payout, roe, costOfThirdPartiesCapital,
                           percentageOfThirdPartiesCapital, g, numberOfYears, numberOfStocks, indebtedness)
    return jsonify(
        fairPrice=resp[0],
        capm=resp[1],
        wacc=resp[2],
        actualPrice=resp[3],
        discount=resp[4]
    )