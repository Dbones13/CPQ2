import GS_APIGEE_Integration_Util
from GS_Curr_ExchRate_Mod import fn_get_curr_exchrate

excel_Url, header = GS_APIGEE_Integration_Util.GetR2QAPIGEEAuthDetails()
try:
	Log.Info('R2Q Marshalling API =>> Payload: {}'.format(str(JsonHelper.Serialize(Param).encode("ascii", "replace").replace('?','')).strip()))
	param = eval(str(JsonHelper.Serialize(Param).encode("ascii", "replace").replace('?','')).strip().replace('null', '""'))

	QuoteNumber = param['CPQQuoteNumber']
	Quote = QuoteHelper.Edit(QuoteNumber)
	Quote_Currency = Quote.GetCustomField("SC_CF_CURRENCY").Content
	exchange_rate = fn_get_curr_exchrate("USD", Quote_Currency)
	if Quote.ContainsAnyProduct('Project_cpq'):
		for item in Quote.MainItems:
			if item.PartNumber == 'PRJT R2Q':
				Product = item.EditConfiguration()
				WriteinProdCont = Product.GetContainerByName('WriteInProduct')
	res2 = param['DataTableObject']
	if res2 and len(res2) > 0 and 'Failure' not in res2:
		marshalling_cabinet_counts = {
			'DCS Marshalling': "",
			'ESD Marshalling': "",
			'FGS Marshalling': ""
		}
		isValid =False
		for itemdet in res2:
			isValid =True
			containerRow = WriteinProdCont.AddNewRow(False)
			#Log.Write('check - 1 = WriteinProdCont '+str(itemdet['Part/Model #']))
			containerRow.GetColumnByName('Category').SetAttributeValue('Common')
			containerRow["Selected_WriteIn"] = str(itemdet['Part/Model #'])
			containerRow["WriteInProducts"] = str(itemdet['Part/Model #'])
			containerRow["Price"] = str(itemdet['Unit List Price'])
			containerRow["Cost"] = str(itemdet['Unit Regional Cost'])
			containerRow["ItemQuantity"] = str(itemdet['Quantity'])
			containerRow['Area'] = str(itemdet['Area'])
			containerRow["ExtendedDescription"]= itemdet['Extended Description']
			if itemdet['Extended Description'].startswith('TS8 Cabinet Base'):
				if 'C300' in param.get('ActionName', '').split('_')[0]:
					Quote.GetCustomField('C300 Cabinet Count').Content = str(int(Quote.GetCustomField('C300 Cabinet Count').Content if Quote.GetCustomField('C300 Cabinet Count').Content else 0) + int(itemdet['Quantity']))
				if 'R2Q Safety Manager ESD' in param.get('ActionName', '').split('_')[0] and param.get('productLine', '') =='ESD':
					Log.Write('SM ESD-->>'+str(itemdet['Part/Model #'])+"-->>"+str(itemdet['Quantity']))
					Quote.GetCustomField('SM ESD Cabinet Count').Content = str(int(Quote.GetCustomField('SM ESD Cabinet Count').Content if Quote.GetCustomField('SM ESD Cabinet Count').Content else 0) + int(itemdet['Quantity']))
				if param.get('productLine', '') =='FGS':
					Log.Write('SM FGS-->>'+str(itemdet['Part/Model #'])+"-->>"+str(itemdet['Quantity']))
					Quote.GetCustomField('SM FGS Cabinet Count').Content = str(int(Quote.GetCustomField('SM FGS Cabinet Count').Content if Quote.GetCustomField('SM FGS Cabinet Count').Content else 0) + int(itemdet['Quantity']))
				area = str(itemdet['Area'])
				if area in marshalling_cabinet_counts:
					marshalling_cabinet_counts[area] = str(itemdet['Quantity'])
		if any(marshalling_cabinet_counts.values()):
			for systemCont in Product.GetContainerByName('R2Q CE_System_Cont').Rows:
				if systemCont['Selected_Products'] == "R2Q C300 System" and marshalling_cabinet_counts['DCS Marshalling']:
					systemCont.Product.Attr('C300_Marshalling_cabinet_count (0-500)').AssignValue(marshalling_cabinet_counts['DCS Marshalling'])
				if systemCont['Selected_Products'] in ("R2Q Safety Manager ESD", "R2Q Safety Manager FGS"):
					if systemCont['Selected_Products'] == param.get('ActionName', '').split('_')[0]:
						for laborCont in systemCont.Product.GetContainerByName('SM_Labor_Cont').Rows:
							if marshalling_cabinet_counts['ESD Marshalling']:
								laborCont['Marshalling_cabinet_count'] = marshalling_cabinet_counts['ESD Marshalling']
							if marshalling_cabinet_counts['FGS Marshalling']:
								laborCont['Marshalling_cabinet_count'] = marshalling_cabinet_counts['FGS Marshalling']
		if isValid and WriteinProdCont.Rows.Count > 0:
			#WriteinProdCont = Product.GetContainerByName('WriteInProduct').Rows.Clear()
			getWriteinPrd = SqlHelper.GetFirst("SELECT PA.PRODUCT_ID, PA.PRODUCT_NAME FROM products PA INNER JOIN product_versions PV ON PV.product_id = PA.PRODUCT_ID WHERE PA.PRODUCT_NAME = 'Write-in Products' AND PV.is_active = 'True'")
			WriteinPrd_Id = int(getWriteinPrd.PRODUCT_ID)
			WriteinProdContainer = ProductHelper.CreateProduct(WriteinPrd_Id)
			WriteinProdContitems = WriteinProdContainer.GetContainerByName('WriteInProduct').Rows.Clear()
			WriteinProdContitems = WriteinProdContainer.GetContainerByName('WriteInProduct')

			for itemdet in res2:
				is_duplicate = False
				for existing_row in WriteinProdContitems.Rows:
					if ((existing_row["ExtendedDescription"]).strip() == itemdet['Extended Description'].strip() and
						str(existing_row["ItemQuantity"]).strip() == str(itemdet["Quantity"]).strip() and str(existing_row["Area"]).strip() == str(itemdet["Area"]).strip()):
						is_duplicate = True
						break

				if is_duplicate:
					continue
				containerRow = WriteinProdContitems.AddNewRow('WriteIn_cpq', False)
				containerRow.GetColumnByName('Category').SetAttributeValue('Common')
				#Log.Write('inside = '+str(itemdet['Selected_WriteIn']))
				containerRow["Selected_WriteIn"] = str(itemdet['Part/Model #'])
				containerRow["WriteInProducts"] = str(itemdet['Part/Model #'])
				containerRow["Price"] = str(float(itemdet['Unit List Price']) * exchange_rate)
				containerRow["Cost"] = str(float(itemdet['Unit Regional Cost']) * exchange_rate)
				containerRow["ItemQuantity"] = str(itemdet['Quantity'])
				containerRow['Area'] = str(itemdet['Area'])
				containerRow["ExtendedDescription"] = itemdet['Extended Description']
				containerRow.Product.Attributes.GetByName("Writein_Category").SelectValue('Common')
				containerRow.Product.Attributes.GetByName("Selected_WriteIn").AssignValue(str(containerRow["Selected_WriteIn"]))
				containerRow.Product.Attributes.GetByName("ItemQuantity").AssignValue(str(containerRow["ItemQuantity"]))
				containerRow.Product.Attributes.GetByName("Extended Description").AssignValue(containerRow["ExtendedDescription"])
				containerRow.Product.Attributes.GetByName("Price").AssignValue(str(containerRow["Price"]))
				containerRow.Product.Attributes.GetByName("cost").AssignValue(str(containerRow["Cost"]))
				containerRow.Product.Attributes.GetByName('LCM_WriteIn_Area').AssignValue(str(containerRow["Area"]))
				containerRow.Product.ApplyRules()
				containerRow.ApplyProductChanges()
			WriteinProdContitems.MakeAllRowsSelected()
			WriteinProdContitems.Calculate()
			WriteinProdContainer.AddToQuote()
			Quote.Save(False)
	Log.Info('GS_R2QPRJT_PS_Marshalling_Async Success-->>')
	final_request_body={'QuoteNumber':str(param.get('CPQQuoteNumber', '')),'CartId':str(Quote.QuoteId),'RevisionNumber': str(Quote.RevisionNumber),'UserName':str(User.UserName),'Module':'New/Expansion','Action':'Update','Status':'Success','Action_List':[{'ActionName':str(param.get('ActionName', '')),'ScriptName':'GS_R2QPRJT_PS_Marshalling_Async'}]}
	RestClient.Post(excel_Url, RestClient.SerializeToJson(str(final_request_body)),header)
	Log.Info('GS_R2QPRJT_PS_Marshalling success payload '+str(final_request_body)+'= excel_Url = '+str(excel_Url)+' = header '+str(header))
except Exception as ex:
	Log.Info('GS_R2QPRJT_PS_Marshalling_Async Error-->>'+str(ex))
	final_request_body={'QuoteNumber':str(param.get('CPQQuoteNumber', '')),'CartId':str(Quote.QuoteId),'RevisionNumber': str(Quote.RevisionNumber),'UserName':str(User.UserName),'Module':'New/Expansion','Action':'Update','Status':'Fail','Action_List':[{'ActionName':str(param.get('ActionName', '')),'ScriptName':'GS_R2QPRJT_PS_Marshalling_Async','ErrorMessage':str(ex)}]}
	RestClient.Post(excel_Url, RestClient.SerializeToJson(str(final_request_body)),header)
