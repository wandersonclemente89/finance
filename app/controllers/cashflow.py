from app import app
from flask import request, jsonify
from finance.calculation import CashFlow


@app.route('/stock/price', methods=["POST"])
def stock_price():
    req_data = request.get_json()
    stock = req_data['stock']
    erp = req_data['equityRiskPremium']
    riskFreeTax = req_data['riskFreeTax']
    roe = req_data['roe']
    costOfThirdPartiesCapital = req_data['costOfThirdPartiesCapital']
    percentageOfThirdPartiesCapital = req_data['percentageOfThirdPartiesCapital']
    netDebt = req_data['netDebt']
    g = req_data['g']
    numberOfYears = req_data['numberOfYears']
    numberOfStocks = req_data['numberOfStocks']
    resp = CashFlow.fdc(stock, erp, riskFreeTax, roe, costOfThirdPartiesCapital,
                        percentageOfThirdPartiesCapital, g, numberOfYears, numberOfStocks, netDebt)
    return jsonify(
        fairPrice=resp[0],
        capm=resp[1],
        wacc=resp[2],
        actualPrice=resp[3],
        discount=resp[4]
    )
