import GS_APIGEE_Integration_Util
excel_Url, header = GS_APIGEE_Integration_Util.GetR2QAPIGEEAuthDetails()
try:
	Log.Info('GS_R2Q_Virtualization_Mapping Param-->>'+JsonHelper.Serialize(Param))
	param = eval(JsonHelper.Serialize(Param).replace('null', '""'))
	Log.Info('GS_R2Q_Virtualization_Mapping Param QuoteNumber-->>'+str(param["CPQQuoteNumber"]))
	Log.Info('GS_R2Q_Virtualization_Mapping Param Payload-->>'+str(param["VrtList"]))
	QuoteNumber = str(param["CPQQuoteNumber"])
	Quote = QuoteHelper.Edit(QuoteNumber)
	Quote.SetGlobal('VrtMappingFlag', 'True')
	Quote.SetGlobal('Virtualization_Mapping_Param', str(param))
	Log.Info('GS_R2Q_Virtualization_Mapping Param-->> Started with QuoteLines: {}'.format(Quote.Items.Count))
	for item in Quote.MainItems:
		if item.ProductName  == 'MSID_New':
			product = item.EditConfiguration()
			selectedProducts = product.GetContainerByName('CONT_MSID_SUBPRD')
			for selectedRow in selectedProducts.Rows:
				if selectedRow['Selected_Products'] == 'Virtualization System Migration':
					for child_attr in selectedRow.Product.Attributes:
						Log.Info("Virtualization System Migration--insind--")
						#selectedRow.Product.ParseString('<* ExecuteScript(VRT_Mapping, {}) *>'.format(str(param["VrtList"])))
						ScriptExecutor.ExecuteGlobal('VRT_CHECKING',{'msidproduct':child_attr.Product,'vrt_list':param})
						child_attr.Product.ApplyRules()
						break
						#child_attr.ApplyProductChanges()
						'''if selectedRow.Product.GetContainerByName("Virtualization_partsummary_cont").Rows.Count > 0:
							
							for vrtParts in selectedRow.Product.GetContainerByName("Virtualization_partsummary_cont").Rows:
								MSID_Virtualisation = product.GetContainerByName("MSID_Virtualization_Added_Parts_Common_Container").AddNewRow(False)
								MSID_Virtualisation ['PartNumber'] = vrtParts['partnumber']
								MSID_Virtualisation ['Quantity'] = vrtParts['CE_Part_Qty']
								MSID_Virtualisation ['PartDescription'] = vrtParts['CE_Part_Description']
								MSID_Virtualisation ['Adj Quantity'] = vrtParts['CE_Adj_Quantity']
								MSID_Virtualisation ['Final Quantity'] = vrtParts['CE_Final_Quantity']
								MSID_Virtualisation ['Comments'] = vrtParts['CE_Comments']
								Log.Info('GS_R2Q_Virtualization_Mapping parts = '+str(MSID_Virtualisation ['PartNumber']))
							#selectedRow.Product.GetContainerByName("Virtualization_partsummary_cont").Rows.Clear()'''
					selectedRow.Product.ApplyRules()
					Log.Info("attributevalueafterapplyrules"+str(selectedRow.Product.Attr('Virtualization_Number_of_R640XL_Standard_Servers').GetValue()))
					selectedRow.ApplyProductChanges()
			product.UpdateQuote()
			break
	#Quote.Reconfigure()
	Quote.SetGlobal('VrtMappingFlag', '')
	Log.Info('GS_R2Q_Virtualization_Mapping Param-->> Success: {}'.format(Quote.Items.Count))
	vrt_request_body={'QuoteNumber':str(Quote.CompositeNumber),'UserName':str(User.UserName),'CartId':str(Quote.QuoteId),'Module':'Migration','RevisionNumber': str(Quote.RevisionNumber),'Action':'Update','Status':'Success','Action_List':[{'ActionName':'Virtualization System','ScriptName':'GS_R2Q_VirtualizationSystem_Parts'}]}
	res = RestClient.Post(excel_Url, RestClient.SerializeToJson(str(vrt_request_body)),header)
	Log.Info('GS_R2Q_Virtualization_Mapping =>> Req: {} -- Res: {}'.format(vrt_request_body, res))
except Exception as ex:
	Log.Info('GS_R2Q_Virtualization_Mapping Error-->>'+str(ex))
	vrt_request_body={'QuoteNumber':str(Quote.CompositeNumber),'UserName':str(User.UserName),'CartId':str(Quote.QuoteId),'Module':'Migration','RevisionNumber': str(Quote.RevisionNumber),'Action':'Update','Status':'Fail','Action_List':[{'ActionName':'Virtualization System','ScriptName':'GS_R2Q_VirtualizationSystem_Parts','ErrorMessage':str(ex)}]}
	res = RestClient.Post(excel_Url, RestClient.SerializeToJson(str(vrt_request_body)),header)
	Log.Info('GS_R2Q_Virtualization_Mapping =>> Req: {} -- Res: {}'.format(vrt_request_body, res))