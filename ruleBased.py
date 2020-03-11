import re
import util
from vendor import Vendor
from taxRate import TaxRate
from totalPrice import TotalPrice
from date import Date
from currency import Currency
from address import Address
from products import Products

def predict(receipt):

    ## predict vendor
    vendor = Vendor(receipt.rawText, receipt.lines)
    vendor.run()
    receipt.ruleBasedPrediction['vendor'] = vendor._result

    ## predict tax rate
    taxRate = TaxRate(receipt.rawText, receipt.lines, receipt.graph, receipt.words)
    taxRate.run()
    receipt.ruleBasedPrediction['tax_rate'] = taxRate._result

    ## predict total price
    totalPrice = TotalPrice(receipt.rawText, receipt.lines)
    totalPrice.run()
    receipt.ruleBasedPrediction['total_price'] = totalPrice._result

    ## predict date
    date = Date(receipt.rawText, receipt.lines)
    date.run()
    receipt.ruleBasedPrediction['date'] = date._result
    
    ## predict currency
    currency = Currency(receipt.rawText)
    currency.run()
    receipt.ruleBasedPrediction['currency'] = currency._result

    ## predict address
    address = Address(receipt.linesText)
    address.run()
    receipt.ruleBasedPrediction['address'] = address._result

    ## predict products
    products = Products(receipt.rawText)
    products.run()
    receipt.ruleBasedPrediction['products'] = products._result
