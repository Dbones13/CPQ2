import math as m
from datetime import datetime
from datetime import date

def numOfDays(date1, date2):
    return (date2-date1).days
'''
Contract Duration logic
'''
contract = Quote.GetCustomField('SC_CF_CONTRACTDURYR').Content
contractDuration = contract.split(' ')[0]
Product.Attr('SC_Contract_Duration').AssignValue(str(contractDuration))

Trace.Write("Nileshttest " + str(contractDuration))

#renewal duration logic
'''
def parseDate(TagParserQuote, Quote, fieldName):
    if Quote.GetCustomField(fieldName).Content != "":
        y = UserPersonalizationHelper.CovertToDate(Quote.GetCustomField(fieldName).Content).Year # .Day
        m = UserPersonalizationHelper.CovertToDate(Quote.GetCustomField(fieldName).Content).Month
        d = UserPersonalizationHelper.CovertToDate(Quote.GetCustomField(fieldName).Content).Day
    return int(y), int(m), int(d)

y2, m2, d2 = parseDate(TagParserQuote, Quote, 'SC_CF_CURANNDELENDT')
date2 = date(y2, m2, d2)
current_datetime = date.today()

d = float(numOfDays(current_datetime, date2))
d = int(d/365)
Trace.Write(d)
Product.Attr('SC_Contract_Duration').AssignValue(str(d))
'''