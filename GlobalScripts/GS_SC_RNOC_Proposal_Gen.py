import re
def parseDate(TagParserQuote, Quote, fieldName):
	y = TagParserQuote.ParseString("<*CTX( Quote.CustomField({}).Format(yyyy))*>".format(fieldName))
	m = TagParserQuote.ParseString("<*CTX( Quote.CustomField({}).Format(MM))*>".format(fieldName))
	d = TagParserQuote.ParseString("<*CTX( Quote.CustomField({}).Format(dd))*>".format(fieldName))
	return int(y), int(m), int(d)
def RNOC_Renewal(Quote,TagParserQuote):
	from datetime import datetime
	fieldName= 'SC_CF_CURANNDELSTDT'
	table = Quote.QuoteTables["QT_KeyValueTable"]
	prevQuote = Quote.GetCustomField('SC_CF_PREVIOUS_QUOTE_NO').Content
	#currentStDate =  Quote.GetCustomField('SC_CF_CURANNDELSTDT').Content
	y1,m1,d1 =  parseDate(TagParserQuote, Quote, fieldName)
	QuoteType = Quote.GetCustomField('Quote Type').Content
	#currentStDate=datetime.strptime(currentStDate,'%d/%M/%y')
	StartYear=y1
	RNOC_SP=RenewalSP=PrevYrSP=0
	DiffSP = 0
	RNOC_PRV_SP = 0
	RNOC_Total = 'No'
	PSt_Dt=''
	PEt_Dt=''
	PPo=''
	cont_duration=Quote.GetCustomField("SC_CF_CONTRACTDURYR").Content if Quote.GetCustomField("SC_CF_CONTRACTDURYR").Content !='' else 0
	if Quote.GetCustomField("SC_CF_IS_CONTRACT_EXTENSION").Content=="True": # added logic for EXTENSION quote
		cont_duration= '1.0 years'
	term=Quote.GetCustomField("SC_CF_Term_duration_Months").Content if Quote.GetCustomField("SC_CF_Term_duration_Months").Content !='' else 0
	Trace.Write(term)
	yr = int(term)/12 if int(term)/12 > 0 else 1
	year ="Year-"+str(yr)
	if len(prevQuote) > 0 :
		Trace.Write(prevQuote)
		from GS_SC_GetQuoteData import CL_QuoteHandler
		QuoteHandler = CL_QuoteHandler(prevQuote)
		prevQValue=QuoteHandler.GetFieldValues(['SC_CF_CURANNDELSTDT','SC_CF_CURANNDELENDT','PONumber'])
		for values in prevQValue:
			if values.Name == 'SC_CF_CURANNDELSTDT':
				PSt_Dt = values.Value
			if values.Name == 'SC_CF_CURANNDELENDT':
				PEt_Dt = values.Value
			if values.Name == 'PONumber':
				PPo = values.Value
	if len(prevQuote) > 0 or (prevQuote)=='':
		INV_FREQUENCY=Quote.GetCustomField("SC_CF_INV_FREQUENCY").Content
		B_Amount =PrevYrSP= 0
		Trace.Write(cont_duration)
		for items in Quote.MainItems:
			if cont_duration =='1.0 years':
				if items.PartNumber =='Service Contract':
					RenewalSP=round(items.ExtendedAmount,2)
					PrevYrSP=round(items.QI_SC_Previous_Year_Sell_Price.Value,2)
					DiffSP = round(RenewalSP - PrevYrSP,2)	
			if cont_duration !='1.0 years' and items.PartNumber == year:
				text =items.QI_SC_SellPrice.Value if items.QI_SC_SellPrice.Value !='' else 0
				pattern = r"[0-9]+.?[0-9]*"
				ab = re.findall(pattern,text)
				numb= str(ab[0]+"."+ab[1])
				RenewalSP=round(float(numb.replace(',', '')),2)
				PrevYrSP=round(items.QI_SC_Previous_Year_Sell_Price.Value,2)
				DiffSP = round(RenewalSP - PrevYrSP,2)
			if items.PartNumber == 'Service Contract':
				Renewal=round(items.ExtendedAmount,2)
				if INV_FREQUENCY in ["Yearly","Adhoc"]:
					B_Amount = Renewal
				elif INV_FREQUENCY in ["Semi-Annual"]:
					B_Amount = round(Renewal/2.0,2)
				elif INV_FREQUENCY in ["Quarterly"]:
					B_Amount = round(Renewal/4.0,2)
				elif INV_FREQUENCY in ["Monthly"]:
					B_Amount = round(Renewal/12.0,2)
				elif INV_FREQUENCY in ["Every 4 months"]:
					B_Amount = round(Renewal/3.0,2)
				elif INV_FREQUENCY in ["Every 4 weeks"]:
					B_Amount = round(Renewal/13.0,2)
				elif INV_FREQUENCY in ["Bi-Monthly"]:
					B_Amount = round(Renewal/6.0,2)
		row = table.AddNewRow()
		row["Type"] = "RNOC"
		row["Service_Name"] = "RNOC_DATES"
		row["Identifier1"] = B_Amount
		row["Identifier2"] = PSt_Dt
		row["Identifier3"] = PEt_Dt
		row["Identifier4"] = RenewalSP
		row["Identifier5"] = PrevYrSP
		row["Identifier6"] = DiffSP
		row["Identifier7"] = PPo
		row["Identifier8"] = StartYear
		for rows in table.Rows:
			if rows['Type'] =='Entitlement':
				for record in filter(lambda y : y.PartNumber in ("SESP" , "Service Product", "Enabled Services", "MES Performix", "Third Party Services") and y.RolledUpQuoteItem.startswith("1.1"), Quote.MainItems):
					if record.PartNumber == 'Third Party Services' :
						Desc = record.PartNumber
					else:
						Desc = record.Description
					if Desc == rows['Identifier3'] :
						rows['Identifier8']= str(round(record.ExtendedAmount,2))
						rows['ProductQnt']= str(record.Quantity)
						qnt =str(record.Quantity)
						ID =rows.Id
						Trace.Write("Id>>>>>> : "+str(ID))
						if qnt == '0' and QuoteType== "Contract Renewal":
							table.DeleteRow(ID)
						Trace.Write("Test : "+str(rows['ProductQnt']))
						rows['Identifier9']= str(round(record.QI_SC_Previous_Year_Sell_Price.Value,2))
						RNOC_SP = RNOC_SP + record.ExtendedAmount
						if qnt == '0' and QuoteType== "Contract Renewal":
							RNOC_PRV_SP = RNOC_PRV_SP + 0
						else:
							RNOC_PRV_SP = RNOC_PRV_SP + record.QI_SC_Previous_Year_Sell_Price.Value
						RNOC_Total = 'Yes'
		if RNOC_Total == 'Yes':
			row = table.AddNewRow()
			row["Type"] = "RNOC_SP_TOTAL"
			row["Price"] = str(round(RNOC_SP,2))
			row["Identifier10"] = str(round(RNOC_PRV_SP,2))
			table.Save()
#ab=RNOC_Renewal(Quote,TagParserQuote)