import math

class Global:

    controller = None

    JSONDateTime = '%Y-%m-%d %H:%M:%S'
    
    # Show debug messages
    debug = True

    @classmethod
    def formatCurrency(amount, symbol="\xa3"):
        negative = amount < 0
        negativeStr = ""
        if negative:
            amount = -amount
            negativeStr = "-"
        decimal = amount % 100
        print decimal
        whole = (amount - decimal)/100

        if decimal < 10:
            decimal = "0" + str(decimal)
        return negativeStr + str(symbol) + str(whole) + "." + str(decimal)