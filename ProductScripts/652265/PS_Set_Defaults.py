Product.Attr('Winest Import Name').AssignValue('Winest Labor Import')

container = Product.GetContainerByName('Winest IO Container')
if container.Rows.Count == 0:
	container.AddNewRow()

updateFlag = False
container = Product.GetContainerByName('Winest Additional Labor Container')
if container.Rows.Count == 0:
	updateFlag = True
	newRow = container.AddNewRow()

if updateFlag:
	import datetime
	salesArea = TagParserQuote.ParseString('<* QuoteProperty (Sales Area) *>')
	marketCode = TagParserQuote.ParseString('<* MCODE *>')
	salesOrg = marketCode.partition('_')[0]
	currency = marketCode.partition('_')[2]
	query = SqlHelper.GetFirst("select Execution_County from NEW_EXECUTION_COUNTRY_SALES_ORG_MAPPING where Sales_Area = '{}' and Currency = '{}'".format(salesOrg,currency))

	current_year = datetime.datetime.now().year
	if Quote:
		if Quote.GetCustomField('EGAP_Contract_Start_Date').Content != "": #If there is a Contract Start Date in the quote:
			c_start_date = Quote.GetCustomField('EGAP_Contract_Start_Date').Content
			contract_start = int("20"+c_start_date[-2:])
			if contract_start > current_year+3: #Maxes out at 3 years in the future. Can't go beyond that.
				contract_start = current_year+3
		else:
			contract_start = current_year
	else:
		contract_start = current_year

	if salesArea != "" and query:
		newRow['Execution Country'] = query.Execution_County
	newRow['Execution Year'] = str(contract_start)
	newRow.Calculate()
	container.Calculate()
	#ScriptExecutor.Execute('PS_Refresh_Labor_Containers_Data')