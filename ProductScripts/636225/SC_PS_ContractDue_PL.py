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
#contractDuration1 = contract.split(' ')[0]
if contractDuration == "":
    contractDuration = 0
if contractDuration=='0.10':
    contractDuration = int(m.ceil(float(contractDuration)))
    Product.Attr('SC_Contract_Duration').AssignValue(str(contractDuration))
elif float(contractDuration) < 0.5 or float(contractDuration) > 3:
    if float(contractDuration) > 3:
        incompleteMessage = "Contract Duration greater than 3 years not allowed."
    else:
        incompleteMessage = "Contract Duration less than 6 months not allowed."
    Product.Attr('SC_Digital_Prime_Contract_invalid').AssignValue(incompleteMessage)
else:
    contractDuration = int(m.ceil(float(contractDuration)))
    #contractYears = str(contractDuration)+" year"
    Product.Attr('SC_Contract_Duration').AssignValue(str(contractDuration))
    Product.Attr('SC_Digital_Prime_Contract_invalid').AssignValue('')

#renewal duration logic
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

Product.Attr('SC_Renewal_check').AssignValue('1')
ContDur = Product.Attr('SC_Contract_Duration').GetValue()

if float(ContDur) > 3:
    Product.Attr('SC_Contract_Duration').AssignValue('3')
Trace.Write("ContDur PS_PopulateRenewalfromNew" + str (ContDur))