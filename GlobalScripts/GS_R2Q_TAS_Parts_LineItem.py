from GS_Curr_ExchRate_Mod import fn_get_curr_exchrate
import GS_APIGEE_Integration_Util
import re
excel_Url, header = GS_APIGEE_Integration_Util.GetR2QAPIGEEAuthDetails()

def insert_parts_summary(child_product,exchange_rate):
	tas_parts = child_product.GetContainerByName('TAS_MODULE_PARTS_SUMMARY')
	writein_parts = child_product.GetContainerByName('WriteInProduct')
	tas_parts.Rows.Clear()
	writein_parts.Rows.Clear()
	for item in parts_list:
		if item["Part"] and "Write-In" not in str(item["Part"]):
			childRow = tas_parts.AddNewRow()
			childRow["Part_Number"] = str(item["Part"])
			childRow["Quantity"] = str(item["Quantity"])
			childRow["Description"] = item['Description']
			#Log.Info("isnnd--"+str(item["Part"]))
		elif item["Part"] and "Write-In" in str(item["Part"]):
			containerRow = writein_parts.AddNewRow('WriteIn_cpq', False)
			containerRow["Selected_WriteIn"] = str(item["Part"])
			containerRow["WriteInProducts"] = str(item["Part"])
			containerRow["Price"] = str(float(item['ListPrice']) * float(exchange_rate))
			containerRow["Cost"] = str(float(item['CostPrice']) * float(exchange_rate))
			containerRow["ItemQuantity"] = str(item['Quantity'])
			containerRow["ExtendedDescription"] = item['Description']
			containerRow.Product.Attributes.GetByName("Writein_Category").SelectValue('Common')
			containerRow.Product.Attributes.GetByName("Selected_WriteIn").AssignValue(str(containerRow["Selected_WriteIn"]))
			containerRow.Product.Attributes.GetByName("ItemQuantity").AssignValue(str(containerRow["ItemQuantity"]))
			containerRow.Product.Attributes.GetByName("Extended Description").AssignValue(containerRow["ExtendedDescription"])
			containerRow.Product.Attributes.GetByName("Price").AssignValue(str(containerRow["Price"]))
			containerRow.Product.Attributes.GetByName("cost").AssignValue(str(containerRow["Cost"]))
			containerRow.Product.Attributes.GetByName("Unit of Measure").AssignValue('EA')
	#Log.Info("part--"+str(tas_parts.Rows.Count))
	#writein_parts.MakeAllRowsSelected()
	#tas_parts.MakeAllRowsSelected()
	for row in writein_parts.Rows:
		row.IsSelected = True
	for row in tas_parts.Rows:
		row.IsSelected = True
		#Log.Info("inin--")
	if containerRow:
		child_product.ApplyRules()
		containerRow.ApplyProductChanges()
		writein_parts.Calculate()


try:
	Log.Info('GS_R2Q_TAS_Parts_LineItem Param-->>'+JsonHelper.Serialize(Param))
	param = eval(JsonHelper.Serialize(Param).replace('null', '""'))
	Log.Info('GS_R2Q_TAS_Parts_LineItem Param Payload-->>'+str(param["TASList"]))
	QuoteNumber = str(param["CPQQuoteNumber"])
	action_name = str(param["ActionName"])
	prd_name = action_name.replace("_TAGBIT","")
	parts_list = param["TASList"]
	non_cpq_items = ''

	APIGEE_Credentials = SqlHelper.GetFirst("Select Value from HPS_INTEGRATION_PARAMS Where [Key]='APIGEE_Credentials'").Value
	APIGEE_R2Q_URL = SqlHelper.GetFirst("Select Value from HPS_INTEGRATION_PARAMS Where [Key]='APIGEE_URL'").Value
	tokenUrl = "{}/v2/oauth/accesstoken".format(APIGEE_R2Q_URL)
	responseToken=AuthorizedRestClient.GetClientCredentialsGrantOAuthToken(APIGEE_Credentials,tokenUrl)
	Req_Token = "{} {}".format(responseToken["token_type"], responseToken["access_token"])
	Url="https://it.api-beta.honeywell.com/cpq/r2q/sfdc/v1/cpqtor2q/tas/generate-part-summary"
	header = {"Content-Type" : "application/json","Authorization" : "{}".format(Req_Token),"HON-Org-Id" : "PMT-HPS" }
	
	if parts_list:
		Quote = QuoteHelper.Edit(QuoteNumber)
		Quote_Currency = Quote.GetCustomField("SC_CF_CURRENCY").Content
		exchange_rate = fn_get_curr_exchrate("USD", Quote_Currency)
		for item in Quote.MainItems:
			if prd_name in ('Small Volume Prover', 'Skid and Instruments', 'Operator Training'):
				if item.ProductName == 'New / Expansion Project':
					product = item.EditConfiguration()
					system_cont_rows = product.GetContainerByName('TAS_NON_CPQ_ITEMS')
					for child_row in system_cont_rows.Rows:
						for child_attr in child_row.Product.Attributes:
							child_product = child_attr.Product
							if child_product.Name == str(prd_name):
								#Log.Info("isnnd--prd_name")
								#insert_parts_summary(child_product)
								#child_product.ApplyRules()
								non_cpq_items = child_product
							break
					if non_cpq_items:
						insert_parts_summary(non_cpq_items,exchange_rate)
						child_row.ApplyProductChanges()
						non_cpq_items.ApplyRules()
						system_cont_rows.Calculate()
					#product.ApplyRules()
					product.UpdateQuote()
					break
			else:
				if item.ProductName == 'System Group':
					product = item.EditConfiguration()
					system_cont_rows = product.GetContainerByName('CE_System_Cont').Rows
					for child_row in system_cont_rows:
						for child_attr in child_row.Product.Attributes:
							child_product = child_attr.Product
							if child_product.Name == str(prd_name):
								#Log.Info("isnnd--prd_name")
								insert_parts_summary(child_product,exchange_rate)
								child_product.ApplyRules()
							break
					#product.ApplyRules()
					product.UpdateQuote()
					break



	final_request_body ={'QuoteNumber':str(QuoteNumber),'UserName':str(User.UserName),'CartId':str(Quote.QuoteId),'Module':'TAS','RevisionNumber': str(Quote.RevisionNumber),'Action':'Update','Status':'Success','Action_List':[{'ActionName':str(action_name),'ScriptName':'GS_R2Q_TAS_SUMMARY'}]}
	res = RestClient.Post(excel_Url, RestClient.SerializeToJson(str(final_request_body)),header)
	Log.Info("GS_R2Q_TAS_Parts_LineItem---sucess")

except Exception as ex:
	Log.Info("except--GS_R2Q_TAS_Parts_LineItem Error-->>"+str(ex))
	final_request_body={'QuoteNumber':str(Quote.CompositeNumber),'CartId':str(Quote.QuoteId),'RevisionNumber': str(Quote.RevisionNumber),'UserName':str(User.UserName),'Module':'TAS','Action':'Update','Status':'Fail','Action_List':[{'ActionName':str(param["ActionName"]),'ScriptName':'GS_R2Q_TAS_SUMMARY','ErrorMessage':str(ex)}]}
	RestClient.Post(excel_Url, RestClient.SerializeToJson(str(final_request_body)),header)
