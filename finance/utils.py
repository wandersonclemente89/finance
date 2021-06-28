import yfinance as yf
from numpy import mean


class Utils:

    def free_cash_flow(stock):
        ticker = yf.Ticker(stock)
        cashFlowArrayData = ticker.cashflow.loc[['Total Cash From Operating Activities', 'Capital Expenditures'],
                                                [True, True, True, True]].to_numpy()
        freeCashFlowArray = cashFlowArrayData[0] + cashFlowArrayData[1]

        freeCashFlowGrowthArray = []
        for x in range(1, freeCashFlowArray.size):
            freeCashFlowGrowthArray.append((freeCashFlowArray[x - 1] - freeCashFlowArray[x]) / freeCashFlowArray[x])

        avg = mean(freeCashFlowGrowthArray)

        return [freeCashFlowArray[0], avg]
