import re
import util
from vendor import Vendor
from taxRate import TaxRate

def predict(receipt):

    ## predict vendor
    vendor = Vendor(receipt.rawText, receipt.lines)
    vendor.run()
    receipt.prediction['vendor'] = vendor._result

    ## predict tax rate
    taxRate = TaxRate(receipt.rawText, receipt.lines)
    taxRate.run()
    receipt.prediction['tax_rate'] = taxRate._result

    ## predict total price
    totalPrice = findTotalPrice(receipt.rawText)
    receipt.prediction['total_price'] = totalPrice
    ## predict currency
    currency = findCurrency(receipt.rawText)
    receipt.prediction['currency'] = currency
    ## predict date
    date = findDate(receipt.rawText, receipt.lines)
    receipt.prediction['date'] = date
    ## predict address
    address = findAddress(receipt.linesText, receipt.lines)
    receipt.prediction['address'] = address
    ## predict procuts
    products = findProducts(receipt.rawText, receipt.lines)
    receipt.prediction['products'] = products

def findCurrency(text):
    for currency in util.currencyList:
        m = re.findall(r"\b" + currency  + r"\b", text)
        if m:
            return m[0]
    for currency in util.currencyList:
        m = re.findall(currency, text)
        if m:
            return m[0]
    return None

def findTotalPrice(text):
    m = re.findall(r'[0-9]+\.[0-9]{2}', text)
    if m:
        biggest = 0
        for potential_price in m:
            try:
                potential_price = float(potential_price)
                if potential_price > biggest:
                        biggest = potential_price
            except:
                continue
        if biggest > 0:
             return biggest
    m = re.findall(r'(?<=TOTAL\s)(\w+)', text)
    if m:
        return m[0]
    return None

def findDate(text, lines):
   m = re.findall(r'[0-9]{4}[-|.|\s|\\][0-9]{2}[-|.|\s|\\][0-9]{2}', text)
   if m:
        return m[0]
   m = re.findall(r'[0-9]{2}[-|.|\s|\\][0-9]{2}[-|.|\s|\\][0-9]{4}', text)
   if m:
        return m[0]
   for month in util.months:
        m = re.findall(r'[0-9]{2}\s?' + month + r'\s?[\']?[0-9]{2}', text, flags=re.IGNORECASE)
        if m:
            return m[0]
   return None

def findAddress(text, lines):
    ## GASTRIKEGATAN 1 113 22 STOCHOLM type \p{L}*\s[0-9]+\s[0-9]{3}\s[0-9]{2}\s\p{L}*
    m = re.findall(r'\b[\w]*\b \b[\w]*\b \b[\w]*\b\s[0-9]+\s\n?\s?[0-9]{3}\s[0-9]{2}\s\b[\w]*\b', text, flags=re.UNICODE)
    if m:
        return re.sub(r'\n', '', m[0])
    m = re.findall(r'\b[\w]*\b \b[\w]*\b\s[0-9]+\s\n?\s?[0-9]{3}\s[0-9]{2}\s\b[\w]*\b', text, flags=re.UNICODE)
    if m:
        return re.sub(r'\n', '', m[0])
    m = re.findall(r'\b[\w]*\b\s[0-9]+\s\n?\s?[0-9]{3}\s[0-9]{2}\s\b[\w]*\b', text, flags=re.UNICODE)
    if m:
        return re.sub(r'\n', '', m[0])
    ## GASTRIKEGATAN 1 11322 STOCHOLM type \p{L}*\s[0-9]+\s[0-9]{3}\s[0-9]{2}\s\p{L}*
    m = re.findall(r'\b[\w]*\b \b[\w]*\b \b[\w]*\b\s[0-9]+\s[0-9]{5}\s\b[\w]*\b', text, flags=re.UNICODE)
    if m:
        return re.sub(r'\n', '', m[0])
    m = re.findall(r'\b[\w]*\b \b[\w]*\b\s[0-9]+\s[0-9]{5}\s\b[\w]*\b', text, flags=re.UNICODE)
    if m:
        return re.sub(r'\n', '', m[0])
    m = re.findall(r'\b[\w]*\b\s[0-9]+\s[0-9]{5}\s\b[\w]*\b', text, flags=re.UNICODE)
    if m:
        return re.sub(r'\n', '', m[0])
    ## GASTRIKEGATAN 1 SE-113 22 STOCHOLM type \p{L}*\s[0-9]+\s[0-9]{3}\s[0-9]{2}\s\p{L}*
    m = re.findall(r'\b[\w]*\b\s[0-9]+\s[SE-]?\s?[0-9]{3}\s[0-9]{2}\s\b[\w]*\b', text, flags=re.UNICODE)
    if m:
        return re.sub(r'\n', '', m[0])
    return None
  

def findProducts(text, lines):
    return None
