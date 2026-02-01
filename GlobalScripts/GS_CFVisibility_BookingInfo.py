'''
New Script is created to manage the visibility of custom fields within the "BOOKING INFO" tab
replacing GS_Custom Field Visibilty
'''
from GS_CommonModule import getCFValue,hideCF,getCF,showCF

fieldsToHideShow = ['AM Name','Backlog Flag','Booking Account','Booking Info Business Model','Booking Info Milestone Category','Contractor/ Partner(C/P)','Drop Shipment','End User','Estimator Name','Exchange Rate','PO Amount','Project Comments','Project Owner Name','Quote and Po Currency','Quote Sell price','SAP Project Number','Legacy CRM ID_Booking Info Tab','Account Siebel Id','Opportunity Siebel Id']

if getCFValue(Quote, "Booking LOB") == 'CCC':
	fieldsToHideShow.remove('Exchange Rate')
for field in fieldsToHideShow:
	hideCF(getCF(Quote , field))
if getCFValue(Quote, "Quote Type") in ('Projects','Parts and Spot'):
	showCF(getCF(Quote,"Project Owner Name"))
if getCFValue(Quote, "Booking LOB") != "PMC":
	hideCF(getCF(Quote,"ApprovedControlNumber"))
elif getCFValue(Quote, "Booking LOB") == "PMC" :
	hideCF(getCF(Quote,"ProfitCentre"))
	hideCF(getCF(Quote,"Profit Centre Description"))
if getCFValue(Quote, "Quote Type") == "Projects" and Quote.GetCustomField("Booking Country").Content.upper() == "UNITED STATES":
	showCF(getCF(Quote,"CF_US_TAX1"))
	showCF(getCF(Quote,"CF_US_TAX2"))
else:
	hideCF(getCF(Quote,"CF_US_TAX1"))
	hideCF(getCF(Quote,"CF_US_TAX2"))

'''if Quote.OrderStatus.Name == 'Preparing':
	Quote.GetCustomField("Quote Expiration Date").Content = TagParserQuote.ParseString("<*CTX(Date.AddDays(1000))*>") if getCFValue(Quote , "Quote Type") == 'Projects' else TagParserQuote.ParseString("<*CTX(Date.AddDays(30))*>")
	if getCFValue(Quote, "Booking LOB") == 'CCC':
		res = SqlHelper.GetFirst("SELECT Exchange_Rate FROM CURRENCY_EXCHANGERATE_MAPPING_CCC WHERE From_Currency = 'USD' AND To_Currency = '"+str(Quote.GetCustomField('Currency').Content)+"'")
	else:
		res = SqlHelper.GetFirst("SELECT Exchange_Rate FROM Currency_ExchangeRate_Mapping WHERE From_Currency = 'USD' AND To_Currency = '"+str(Quote.GetCustomField('Currency').Content)+"'")
	Quote.GetCustomField('Exchange Rate').Content = res.Exchange_Rate'''