#PS_CalculateMPAPrice
def getContainer(product,Name):
	return product.GetContainerByName(Name)

def getFloat(Var):
	if Var:
		return float(Var)
	return 0

def getSalesOrg(country):
	query = SqlHelper.GetFirst("select Execution_Country_Sales_Org from EXECUTION_COUNTRY_SALES_ORG_MAPPING (NOLOCK) where Execution_County = '{}'".format(country))
	if query is not None:
		#Trace.Write("SalesOrg = " + query.Execution_Country_Sales_Org)
		return query.Execution_Country_Sales_Org

def currencyCOnversion(Price):
	quoteCurrency = Quote.SelectedMarket.CurrencyCode
	priceWithConversion = dict()
	if Price:
		for key in Price:
			Trace.Write(Price[key]["stdcurrency"])
			query = SqlHelper.GetFirst("select Exchange_Rate from Currency_ExchangeRate_Mapping (NOLOCK) where From_Currency = '{}' and To_Currency = '{}'".format(Price[key]["stdcurrency"],quoteCurrency))
			if query is not None:
				priceWithConversion[key] = getFloat(Price[key]["price"]) * getFloat(query.Exchange_Rate)
			else:
				priceWithConversion[key] = getFloat(Price[key]["price"])
	#Trace.Write(str(priceWithConversion))
	return priceWithConversion

def getMPAPrice(salesOrg,partNumber,honeywellRef,totalManHours):
	mpaPrice = dict()
	query = ""
	if honeywellRef == "1-CUN51UZ":
		query = "SELECT Unit_MPA_Price,Currency,Service_Material FROM GES_MPA_PRICE (NOLOCK) WHERE SalesOrg = '{0}' and cast(Minimum_MH as float) <= {1} and cast(Maximum_MH as float)> {1} and  Service_Material = '{2}'  and HoneywellRef = '{3}'".format(salesOrg,totalManHours,partNumber,honeywellRef)
	elif honeywellRef in ("1-E2E9KXP", "1-AG39TBN"):
		query = "SELECT Unit_MPA_Price,Currency,Service_Material FROM GES_MPA_PRICE WHERE SalesOrg = '{0}' and  Service_Material = '{1}' and HoneywellRef = '{2}'".format(salesOrg,partNumber,honeywellRef)
	res = SqlHelper.GetFirst(query)
	if res is not None and res.Unit_MPA_Price:
		mpaPrice[res.Service_Material] = {"price": res.Unit_MPA_Price,"stdcurrency": res.Currency}
	Trace.Write(str(mpaPrice))
	unitMPAPrice = currencyCOnversion(mpaPrice)
	if partNumber in unitMPAPrice and unitMPAPrice[partNumber]:
		return getFloat(unitMPAPrice[partNumber])
	return 0

def populateMPAPrice(row):
	if row["GES_Eng_Percentage_Split"] not in ('0.00','') and row["Final_Hrs"] not in ('','0'):
		salesOrg = getSalesOrg(row["Execution_Country"])
		gesMPAPrice = getMPAPrice(salesOrg,row["GES_Eng"],honeywellRef,totalManHours)
		Trace.Write(str(gesMPAPrice))
		if gesMPAPrice:
			MPAPrice = round(getFloat(gesMPAPrice),2)
			gesFinalHours = round(getFloat(row["Final_Hrs"]) * getFloat(row["GES_Eng_Percentage_Split"]) / 100)
			row["GES_MPA_Price"] = str(MPAPrice * gesFinalHours)
		else:
			row["GES_MPA_Price"] = "0"
	else:
		row["GES_MPA_Price"] = "0"
	if row["FO_Eng_Percentage_Split"] not in ('0.00','') and row["Final_Hrs"] not in ('','0'):
		salesOrg = getSalesOrg(row["Execution_Country"])
		foMPAPrice = getMPAPrice(salesOrg,row["FO_Eng"],honeywellRef,totalManHours)
		Trace.Write(str(foMPAPrice))
		if foMPAPrice:
			MPAPrice = round(getFloat(foMPAPrice),2)
			foFinalHours = round(getFloat(row["Final_Hrs"]) * getFloat(row["FO_Eng_Percentage_Split"]) / 100)
			row["FO_MPA_Price"] = str(MPAPrice * foFinalHours)
		else:
			row["FO_MPA_Price"] = "0"
	else:
		row["FO_MPA_Price"] = "0"

honeywellRef = Quote.GetCustomField('MPA Honeywell Ref').Content
containers = ['Trace_Software_Labor_con','Trace_Project_Management_Labor_con']
totalManHours = 0

for container in containers:
	for row in Product.GetContainerByName(container).Rows:
		if row["Deliverable"] == 'Total':
			totalManHours = totalManHours + float(row['Final_Hrs'])
			break

for item in Quote.MainItems:
    totalManHours = totalManHours + int(item["QI_Local_Labor"].Value) + int(item["QI_Cross_Border_Labor"].Value) + int(item["QI_GES_Work_GES_Location"].Value) + int(item["QI_GES_Work_Non_GES_Location"].Value)
Trace.Write(totalManHours)

for container in containers:
	for row in Product.GetContainerByName(container).Rows:
		if row["Deliverable"] not in ('Total','Off-Site','On-Site'):
			populateMPAPrice(row)
		Product.GetContainerByName(container).Calculate()