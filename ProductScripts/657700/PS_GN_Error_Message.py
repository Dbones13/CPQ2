SC_Product_Type = Product.Attr('SC_Product_Type').GetValue()
if SC_Product_Type == 'New':
	Cyberscope = Product.GetContainerByName("SC_GN_AT_Models_Scope_Cont")
	validModelCont = Product.GetContainerByName("SC_GN_AT_Models_Scope_Cont")
	inValidModelCont = Product.GetContainerByName("SC_GN_AT_Invalid_Cont")
	Service = Product.GetContainerByName('SC_GN_AT_Service_Product_Cont')
	#from CPQ_SF_SC_Modules import CL_SC_Modules
	#class_contact_modules = CL_SC_Modules(Quote, TagParserQuote, None, Session)
	#AccountName = Quote.GetCustomField('Account Name').Content
	#AccountSite = Quote.GetCustomField('Account Site').Content
	#MSIDTable=class_contact_modules.get_site_assets(AccountName, AccountSite)
	#Valid_Asset=['']
	#for Assets in MSIDTable.records:
		#Valid_Asset.append(str(Assets.Name))
	err_msg_1 = ""
	err_msg_2 = ""
	err_msg_3 = ""
	err_msg_4 = ""
	err_msg_5 = ""
	err_msg_6 = ""

	SP_list = []
	ErrorMsg = ''
	Product.Attr("SC_GN_AT_Error_Message").AssignValue(ErrorMsg)
	for SP_row in Service.Rows:
		if SP_row.IsSelected == True:
			SP_list.append(str(SP_row['Service_Product']))
	
	if Cyberscope.Rows.Count > 0:
		for row in Cyberscope.Rows:
			#if row['Asset No'] not in Valid_Asset:
				#err_msg_1+= "Asset is not Valid:" + str(row.RowIndex+1) + "<br>"
			if row['Quantity'] == "0":
				err_msg_2+= "Quantity is invalid on row:" + str(row.RowIndex+1) + "<br>"
			if row['Description'] == str(''):
				err_msg_3 += "Description is blank:" + str(row.RowIndex+1) + "<br>"
			if row['Unit_List_Price'] == "0" or  row['Unit_List_Price'] == "":
				err_msg_4 += "List Price is not valid:" + str(row.RowIndex+1) + "<br>"
			if  row['Unit_Cost_Price'] == "0" or row['Unit_Cost_Price'] == "":
				err_msg_5 += "Cost Price is not valid:" + str(row.RowIndex+1) + "<br>"
			if row['Model'] == str(''):
				err_msg_6 += "Model is blank" + str(row.RowIndex+1) + "<br>"
		Serv_Prod = []
		Valid_SP_Asset = []
		def populateInValidCont():
			row = inValidModelCont.AddNewRow(False)
			row["Asset No"] = Asset
			row["Service_Product"] = SP
			row["Description"] = Desc
			row["Quantity"] = Qty
			row["Reason"] = reason
			row["Model"]=Model
		if validModelCont.Rows.Count:
			for row in validModelCont.Rows:
				Serv_Prod.append(row["Service_Product"])
				if row["Service_Product"] != "" and row["Asset No"] != "" and row["Model"] != "":
					Valid_SP_Asset.append(str(row["Service_Product"])+"|"+str(row["Asset No"])+"|"+str(row["Model"]))
					
		#Checking for Qty
			Qty = row['Quantity']
			SP = row['Service_Product']
			Asset = row['Asset No']
			Desc = row['Description']
			Model = row['Model']
			if str(Qty).isalpha():
				Qty='0'
			elif str(Qty)=="":
				Qty='0'
			key = str(SP)+"|"+str(Asset)+"|"+str(Model)

		#Checking for valid Asset
			reason = ""
			#if SP != "" and Asset != "" and Model != "" and key in Valid_SP_Asset:
				#reason+='Duplicate Entry'
			if Model=="":
				reason += 'Invalid Model number (CPQ)''<br>'
			if Desc=="":
				reason += 'Model Description is blank''<br>'
			if str(Qty)=="0" or (float(Qty) <= 0 or float(Qty)>1):
				reason += 'Invalid Quantity''<br>'
			if SP not in SP_list:
				reason += 'Invalid Selected Service Product''<br>'
			#if Asset not in Valid_Asset and Asset.strip() != "":
				#reason += 'Invalid Asset Number''<br>'
			#if float(CP) <= 0:
				#reason += 'Invalid Cost Price''<br>'
			#if float(LP) <= 0:
				#reason += 'Invalid List Price''<br>'
			#Trace.Write("reason-->NEW"+str(reason)+"; "+"SP-->"+str(SP))
			if reason != "": #and SP not in Serv_Prod:
				populateInValidCont()
				key1 = str(SP)+"|"+str(Asset)+"|"+str(Model)
				if key1 not in Valid_SP_Asset:
					Valid_SP_Asset.append(key1)
	ErrorMsg = err_msg_1 + err_msg_2 + err_msg_3 + err_msg_4 + err_msg_5 + err_msg_6
	Trace.Write('Test' + str(ErrorMsg))
	Product.Attr("SC_GN_AT_Error_Message").AssignValue(ErrorMsg)
	

elif SC_Product_Type == 'Renewal':
	Cyberscope = Product.GetContainerByName("SC_GN_AT_Models_Scope_Cont")
	from CPQ_SF_SC_Modules import CL_SC_Modules
	class_contact_modules = CL_SC_Modules(Quote, TagParserQuote, None, Session)
	AccountName = Quote.GetCustomField('Account Name').Content
	AccountSite = Quote.GetCustomField('Account Site').Content
	MSIDTable=class_contact_modules.get_site_assets(AccountName, AccountSite)
	Valid_Asset=['']
	for Assets in MSIDTable.records:
		Valid_Asset.append(str(Assets.Name))
	err_msg_1 = ""
	err_msg_2 = ""
	err_msg_3 = ""
	err_msg_4 = ""
	err_msg_5 = ""
	err_msg_6 = ""


	if Cyberscope.Rows.Count > 0:
		for row in Cyberscope.Rows:
			if row['PY_Quantity'] == '0':
				#if row['Asset No'] not in Valid_Asset:
					#err_msg_1+= "Asset is not Valid:" + str(row.RowIndex+1) + "<br>"
				if row['Renewal_Quantity'] == "0" and row['PY_Quantity'] == "0" :
					err_msg_2+= "Quantity is invalid on row:" + str(row.RowIndex+1) + "<br>"
				if row['Description'] == str(''):
					err_msg_3 += "Description is blank:" + str(row.RowIndex+1) + "<br>"
				if (row['CY_ListPrice'] == "0" or  row['CY_ListPrice'] == ""):
					err_msg_4 += "List Price is not valid:" + str(row.RowIndex+1) + "<br>"
				if (row['CY_CostPrice'] == "0" or  row['CY_CostPrice'] == ""):
					err_msg_5 += "Cost Price is not valid:" + str(row.RowIndex+1) + "<br>"
				if row['Model_Number'] == str(''):
					err_msg_6 += "Model is blank" + str(row.RowIndex+1) + "<br>"


	ErrorMsg = err_msg_1 + err_msg_2 + err_msg_3 + err_msg_4 + err_msg_5 + err_msg_6
	Product.Attr("SC_GN_AT_Error_Message").AssignValue(ErrorMsg)