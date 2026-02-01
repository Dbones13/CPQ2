from CPQ_SF_SC_Modules import CL_SC_Modules
class_contact_modules = CL_SC_Modules(Quote, TagParserQuote, None, Session)
AccountName = Quote.GetCustomField('Account Name').Content
AccountId = Quote.GetCustomField('AccountId').Content
sitesApiResponse = class_contact_modules.get_sitesByID(AccountId)
accountSitesList = []
if sitesApiResponse:
    if sitesApiResponse and str(sitesApiResponse).Contains('totalSize') and sitesApiResponse.totalSize > 0:
        accountSitesList = [str(st.Id) for st in sitesApiResponse.records]
MSIDTable=class_contact_modules.get_siteID_assets(AccountId, accountSitesList, None, True if sitesApiResponse else False)
err_msg_1 = ""
err_msg_2 = ""
err_msg_3 = ""
err_msg_4 = ""
err_msg_5 = ""
err_msg_6 = ""
ErrorMsg = ""
Valid_Asset=[]
for Assets in MSIDTable.records:
	Valid_Asset.append(str(Assets.Name))
a=Product.Attr('SC_Product_Type').GetValue()
Trace.Write(a)
if a=="Renewal":
	messcope = Product.GetContainerByName("SC_BGP_Models_Scope_Cont")
	if messcope.Rows.Count > 0:
		for row in messcope.Rows:
			if row['Asset No'] not in Valid_Asset:
				err_msg_1+= "Asset No not available: " + str(row.RowIndex+1) + "<br>"
			if row['Description'] == str(''):
				err_msg_3 += "Service product with Blank Description" + str(row.RowIndex+1) + "<br>"
			if row["Service_Product"] not in Product.Attr('SC_ScopeRemoval').GetValue():
				if row['Renewal_Quantity'] != "1":
					err_msg_2+= "Invalid Quantity:" + str(row.RowIndex+1) + "<br>"
				if row['Current_Year_List_Price'] == "0.00" or	 row['Current_Year_List_Price'] == "" or row['Current_Year_List_Price'] == "0":
					err_msg_4 += "Invalid Price:" + str(row.RowIndex+1) + "<br>"
				if row['Current_Year_Cost_Price'] == "0.00" or	 row['Current_Year_Cost_Price'] == "" or row['Current_Year_Cost_Price'] == "0":
					err_msg_5 += "Invalid Cost:" + str(row.RowIndex+1) + "<br>"
			if row['Model_Number'] == "0.00" or	 row['Model_Number'] == "":
				err_msg_6 += "Service product with Blank Model Number:" + str(row.RowIndex+1) + "<br>"
		ErrorMsg = err_msg_1 + err_msg_2 + err_msg_3 + err_msg_4 + err_msg_5 + err_msg_6
	#else:
		#ErrorMsg = "The model scope table is empty"
else:
	messcope = Product.GetContainerByName("SC_BGP_Models_Scope_Cont")
	if messcope.Rows.Count > 0:
		for row in messcope.Rows:
			if row['Asset No'] not in Valid_Asset:
				err_msg_1+= "Asset No not available " + str(row.RowIndex+1) + "<br>"
			if row['Quantity'] != "1":
				err_msg_2+= "Quantity is invalid on row:" + str(row.RowIndex+1) + "<br>"
			if row['Description'] == str(''):
				err_msg_3 += "Description is blank:" + str(row.RowIndex+1) + "<br>"
			if row['Unit_List_Price'] == "0" or	 row['Unit_List_Price'] == "":
				err_msg_4 += "List Price is not valid:" + str(row.RowIndex+1) + "<br>"
			if	row['Unit_Cost_Price'] == "0" or row['Unit_Cost_Price'] == "":
				err_msg_5 += "Cost Price is not valid:" + str(row.RowIndex+1) + "<br>"
		ErrorMsg = err_msg_1 + err_msg_2 + err_msg_3 + err_msg_4 + err_msg_5
	#else:
		#ErrorMsg = "The model scope table is empty"
Product.Attr("SC_BGP_Error_Message").AssignValue(ErrorMsg)