import numpy as np
import numpy_financial as npf
from datetime import date, datetime
from pandas_datareader import data as wb
import matplotlib.pyplot as plt
import pandas as pd


class ReturnOfInvestment:

    @staticmethod
    def stock_return(stock, start_date, mean_type):
        data = wb.DataReader(stock, data_source='yahoo', start=start_date)

        if mean_type == 'S':
            data['simple_return'] = (data['Adj Close'] / data['Adj Close'].shift(1)) - 1
            # Média de retorno diário
            # avg_daily=data['simple_return'].mean()
            # Média de retorno anual
            avg_annual = data['simple_return'].mean() * 250
            # Gráfico
            # data['simple_return'].plot(figsize=(8, 5))
            # plt.show()
        elif mean_type == 'L':
            data['log_return'] = np.log(data['Adj Close'] / data['Adj Close'].shift(1))
            # Média de retorno diário
            # avg_daily=data['log_return'].mean()
            # Média de retorno anual
            avg_annual = data['log_return'].mean() * 250
            # Gráfico
            # data['log_return'].plot(figsize=(8, 5))
            # plt.show()
        else:
            print('Invalid mean type! \n please choose either \'S\' or \'L\'.')
            return

        return str(round(avg_annual, 5) * 100) + '%'

    @staticmethod
    def equity_return(stock, erp, ipca):
        beta = Beta.stock_beta(stock)
        ri = ipca + (float(beta)) * (erp - ipca)
        return str(round((ri * 100), 2)) + '%'

    @staticmethod
    def equity_int_return(stock, erp, riskFreeTax):
        beta = Beta.stock_beta(stock)
        ri = riskFreeTax + (float(beta)) * (erp - riskFreeTax)
        return ri

    @staticmethod
    def stock_portfolio_return(dict_of_stocks, start_date):
        data = pd.DataFrame()
        total_number_of_stocks = 0
        weights = []

        for stock in dict_of_stocks:
            total_number_of_stocks += dict_of_stocks[stock]
            data[stock] = wb.DataReader(stock, data_source='yahoo', start=start_date)['Adj Close']

        # (data / data.iloc[0] * 100).plot(figsize=(15, 6))
        # plt.show()

        for stock in dict_of_stocks:
            weights.append(dict_of_stocks[stock] / total_number_of_stocks)

        annual_return = ((data / data.shift(1)) - 1).mean() * 250
        t = float(np.dot(annual_return, np.array(weights)))
        return str(round(t, 5) * 100) + '%'

    @staticmethod
    def stock_index_comparison(list_of_stocks, start_date):
        data = pd.DataFrame()
        for stock in list_of_stocks:
            data[stock] = wb.DataReader(stock, data_source='yahoo', start=start_date)['Adj Close']

        (data / data.iloc[0] * 100).plot(figsize=(15, 6))
        plt.show()


class StandardDeviation:

    @staticmethod
    def standard_deviation(list_of_stocks, start_date):
        data = pd.DataFrame()
        for stock in list_of_stocks:
            data[stock] = wb.DataReader(stock, data_source='yahoo', start=start_date)['Adj Close']

        daily_avg = np.log(data / data.shift(1))
        std = daily_avg[list_of_stocks].std() * pow(250, 0.5)
        # mean = daily_avg[list_of_stocks].mean() * 250
        return str(round(std, 4) * 100)

    @staticmethod
    def correlation(list_of_stocks, start_date):
        data = pd.DataFrame()
        for stock in list_of_stocks:
            data[stock] = wb.DataReader(stock, data_source='yahoo', start=start_date)['Adj Close']

        daily_avg = np.log(data / data.shift(1))
        corr = daily_avg.corr()
        return corr

    @staticmethod
    def portfolio_risk(dict_of_stocks, start_date):
        data = pd.DataFrame()
        total_number_of_stocks = 0
        weights = []

        for stock in dict_of_stocks:
            total_number_of_stocks += dict_of_stocks[stock]
            data[stock] = wb.DataReader(stock, data_source='yahoo', start=start_date)['Adj Close']

        for stock in dict_of_stocks:
            weights.append(dict_of_stocks[stock] / total_number_of_stocks)

        daily_avg = np.log(data / data.shift(1))
        pfolio_var = (np.dot(np.array(weights).T, np.dot(daily_avg.cov() * 250, weights)))
        pfolio_vol = pow(pfolio_var, 0.5)

        return str(round(pfolio_var, 5)), str(round(pfolio_vol, 5) * 100) + '%'


class Beta:

    @staticmethod
    def stock_beta(stock):
        data = pd.DataFrame()
        list_of_stocks = [stock, '^BVSP']

        current_date = date.today().strftime('%Y-%m-%d')
        current_year = current_date.split('-')[0]

        start_date = datetime(int(current_year) - 5, 1, 1).strftime('%Y-%m-%d')
        end_date = datetime(int(current_year), 12, 31).strftime('%Y-%m-%d')

        for stock in list_of_stocks:
            data[stock] = wb.get_data_yahoo(stock, interval='mo', start=start_date, end=end_date)['Adj Close']

        sec_return = np.log(data / data.shift(1))
        cov = sec_return.cov() * 12
        cov_with_market = cov.iloc[0, 1]
        market_var = sec_return['^BVSP'].var() * 12

        return str(round((cov_with_market / market_var), 2))


class CashFlow:

    @staticmethod
    def fdc(stock, erp, risk_free_tax, free_cash_flow, payout, roe, cost_of_third_parties_capital,
            percentage_of_third_parties_capital, g, number_of_years, numberOfStocks, indebtedness):

        print('======== capm =============')
        capm = ReturnOfInvestment.equity_int_return(stock, erp, risk_free_tax)

        capm_str = str(round(capm*100, 2))+'%'
        print(capm_str)

        print('======== wacc =============')
        wacc = ((1 - percentage_of_third_parties_capital) * capm) + (percentage_of_third_parties_capital
                                                                     * (cost_of_third_parties_capital * 0.65))
        wacc_str = str(round(wacc*100, 2))+'%'
        print(wacc_str)

        print('======== cash_flows =============')
        cash_flows = [free_cash_flow]
        tax = (1 - payout) * roe
        for year in range(1, number_of_years):
            cash_flows.append(cash_flows[year-1]*(1 + tax))
        print(cash_flows)

        print('======== Perpetual growth rate =============')
        perpetual_growth_amount = cash_flows[number_of_years - 1] / (wacc - g)
        print(perpetual_growth_amount)

        fair_price = (((npf.npv(wacc, cash_flows) + perpetual_growth_amount) - indebtedness) / numberOfStocks)
        actual_stock_price = wb.get_data_yahoo(stock)['Adj Close'].tail(1).iloc[0]
        discount = 1 - actual_stock_price/fair_price

        return [round(fair_price, 2), capm_str, wacc_str, round(actual_stock_price, 2), str(round(discount*100, 2))+'%']
