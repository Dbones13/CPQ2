import math
#---------------------------------------------------------------------------------------------------------
# story: CXCPQ-63377
# Description:Commercial Info Tab, multiyear related Cost and Sell Price escalation input fields for BOM and Labor would #             be visible when Quote Type is Projects and Booking Lob is 'PAS/LSS'
#----------------------------------------------------------------------------------------------------------
# Date 			Name				  Comment
# 11-09-2023	Ankit Chouhan		  Initial Creation
# 29-09-2023    Ankit Chouhan         Added changes for Defaulting value (0) for YOY and BOM custom Fields
from datetime import date
def numOfDays(date1, date2):
    return (date2-date1).days
def parseDate(TagParserQuote, Quote, fieldName):
    y = TagParserQuote.ParseString("<*CTX( Quote.CustomField({}).Format(yyyy))*>".format(fieldName))
    m = TagParserQuote.ParseString("<*CTX( Quote.CustomField({}).Format(MM))*>".format(fieldName))
    d = TagParserQuote.ParseString("<*CTX( Quote.CustomField({}).Format(dd))*>".format(fieldName))
    return int(y), int(m), int(d)
cf_contractStartDate = Quote.GetCustomField('EGAP_Contract_Start_Date')
cf_contractEndDate = Quote.GetCustomField('EGAP_Contract_End_Date')
Years = 0
if Quote.GetCustomField('Quote Type').Content=='Projects':
    if Quote.GetCustomField('CF_Multiyear_Project').Content == "Yes":
        if cf_contractStartDate.Content.strip() != '' and cf_contractEndDate.Content.strip() != '':
            y1, m1, d1 = parseDate(TagParserQuote, Quote, 'EGAP_Contract_Start_Date')
            y2, m2, d2 = parseDate(TagParserQuote, Quote, 'EGAP_Contract_End_Date')
            date1 = date(y1, m1, d1)
            date2 = date(y2, m2, d2)
            d = float(numOfDays(date1, date2)) #days calculation
            Years = int(math.ceil(d/365)) #year Calculation
            labor_int = 0
            labor = Quote.GetCustomField('CF_Cost_and_Sell_percent').Content
            if labor != "":
                labor_int = int(labor)
            Quote.GetCustomField('CF_Starting_Year').Editable = True
            Trace.Write(Years)
            if Years < 4 or  labor_int == 0:
                Quote.GetCustomField('CF_Starting_Year').Content=None
                Quote.GetCustomField('CF_Starting_Year').Editable = False
            elif Years > 10:
                    Quote.CustomFields.AllowValuesByValueCodes('CF_Starting_Year', '4', '5', '6', '7', '8', '9', '10')
                    Quote.GetCustomField('CF_Starting_Year').Editable = True
            else:
                Quote.CustomFields.DisallowValuesByValueCodes('CF_Starting_Year', '4', '5', '6', '7', '8', '9', '10')
                while Years>=4:
                    Quote.CustomFields.AllowValuesByValueCodes('CF_Starting_Year',str(Years))
                    Years -= 1
        else:
            Quote.GetCustomField('CF_Starting_Year').Content=None
            Quote.GetCustomField('CF_Starting_Year').Editable = False
    else:
        Quote.GetCustomField('CF_Starting_Year').Content=None
        Quote.GetCustomField('CF_Cost_and_Sell_percent').Content='0'
        Quote.GetCustomField('CF_Cost_percent').Content='0'
        Quote.GetCustomField('CF_Sell_Price').Content='0'