import GS_APIGEE_Integration_Util
from GS_Curr_ExchRate_Mod import fn_get_curr_exchrate

def addOrUpdateWriteIn(attr_Name, qty):
	writeInProductQuery = SqlHelper.GetFirst("SELECT WRITEIN_NAME, EXTENDED_DESCRIPTION, UNIT_LIST_PRICE, UNIT_REGIONAL_COST, AREA FROM R2Q_THIRD_PARTY_WRITEINS (nolock) WHERE R2Q_ATTRIBUTE_NAME = '" + attr_Name + "' ")
	if writeInProductQuery:
		Quote_Currency = Quote.GetCustomField("SC_CF_CURRENCY").Content
		exchange_rate = fn_get_curr_exchrate("USD", Quote_Currency)
		Log.Info("exchange rate ==> "+str(exchange_rate))
		containerRow = WriteinProdCont.AddNewRow('WriteIn_cpq', False)
		containerRow.GetColumnByName('Category').SetAttributeValue('Common')
		containerRow["Selected_WriteIn"]     = str(writeInProductQuery.WRITEIN_NAME)
		containerRow["WriteInProducts"]     = str(writeInProductQuery.EXTENDED_DESCRIPTION)
		containerRow["Price"] = str(float(writeInProductQuery.UNIT_LIST_PRICE) * exchange_rate)
		containerRow["Cost"] = str(float(writeInProductQuery.UNIT_REGIONAL_COST) * exchange_rate)
		# containerRow["Price"] = str(writeInProductQuery.UNIT_LIST_PRICE)
		# containerRow["Cost"] = str(writeInProductQuery.UNIT_REGIONAL_COST)
		containerRow["ItemQuantity"]        = str(qty)
		containerRow["ExtendedDescription"]         = str(writeInProductQuery.EXTENDED_DESCRIPTION)
		containerRow["Area"] = str(writeInProductQuery.AREA)
		if str(writeInProductQuery.WRITEIN_NAME) == "Write-In Third Party Hardware":
			containerRow.Product.Attributes.GetByName("Unit of Measure").SelectValue('EA')
		containerRow.Product.Attributes.GetByName("Writein_Category").SelectValue('Common')
		containerRow.Product.Attributes.GetByName("Selected_WriteIn").AssignValue(str(containerRow["Selected_WriteIn"]))
		containerRow.Product.Attributes.GetByName("ItemQuantity").AssignValue(str(containerRow["ItemQuantity"]))
		containerRow.Product.Attributes.GetByName("Extended Description").AssignValue(containerRow["ExtendedDescription"])
		containerRow.Product.Attributes.GetByName("Price").AssignValue(str(containerRow["Price"]))
		containerRow.Product.Attributes.GetByName("cost").AssignValue(str(containerRow["Cost"]))
		containerRow.Product.Attributes.GetByName('LCM_WriteIn_Area').AssignValue(str(containerRow["Area"]))
		containerRow.Product.ApplyRules()
		containerRow.ApplyProductChanges()
		containerRow.Calculate()

Log.Info('GS_R2Q_AddWriteIn Param-->>'+str(Param))
excel_Url, header = GS_APIGEE_Integration_Util.GetR2QAPIGEEAuthDetails()
try:
	QuoteNumber = Param.QuoteNumber
	Quote = QuoteHelper.Edit(QuoteNumber)
	if Quote.ContainsAnyProduct('Project_cpq'):
		attribute = ''
		for item in Quote.MainItems:
			if item.PartNumber == 'PRJT R2Q':
				#Product = item.EditConfiguration()
				isR2Qquote = True if Quote.GetCustomField("R2QFlag").Content else False
				if isR2Qquote and Quote.GetCustomField('R2Q_Save').Content == 'Submit':
					Log.Info("Addwritein call..")
					ProductsData = eval(Quote.GetGlobal('R2Qdata'))
					total_stations = total_servers = 0
					if ProductsData:
						for key, values in ProductsData.items():
							if values and len(values) > 0 and key == 'R2Q CE_System_Cont':
								order_products = {"Experion":[]}
								for indx, selected_Product_order in enumerate(values[0]):
									if selected_Product_order['Selected_Products'] ==  'R2Q Experion Enterprise System':
										order_products["Experion"] = values[1][indx]

						stations = ['CMS Flex Station Qty 0_60', 'DMS Flex Station Qty 0_60', 'Flex Station Qty (0-60)', 'Additional Stations']
						#ebr = ['Experion Backup & Restore (Experion Server)', 'Experion Backup & Restore (Flex Station ES-F)']
						qty_dict = {'ESD_FGS_Aux_PanelsConsoles':0, 'Colour A4 printer': 0, 'B_W_A3_printer': 0, 'Colour_A3_printer': 0,'L3 Switch Required (0-10)': 0, 'Network_Firewall_Required': 0,'PDB Cabinet (0-50)': 0, 'GPS NTP Server System (0-1)': 0, 'Laptop (0-50)': 0}
						sections = {'Server Furniture (0-50)':0, 'Station Furniture (0-200)':0}
						if order_products["Experion"]:
							getWriteinPrd = SqlHelper.GetFirst("SELECT PA.PRODUCT_ID, PA.PRODUCT_NAME FROM products PA INNER JOIN product_versions PV ON PV.product_id = PA.PRODUCT_ID WHERE PA.PRODUCT_NAME = 'Write-in Products' AND PV.is_active = 'True'")
							WriteinPrd_Id = int(getWriteinPrd.PRODUCT_ID)
							WriteinProduct = ProductHelper.CreateProduct(WriteinPrd_Id)
							WriteinProdCont = WriteinProduct.GetContainerByName('WriteInProduct')
							for attrname, attrvalue in order_products['Experion'].items():
								if attrname == 'Experion_Enterprise_Cont' and attrvalue[1]:
									attribute = attrvalue[1][0]
									total_stations += sum(int(attribute[attr]) for attr in stations if attr in attribute)
									#total_servers += sum(1 for attr in ebr if (attr in attribute and attribute[attr] == "Yes"))
									if 'Experion Backup & Restore (Experion Server)' in attribute:
										total_servers += 1 if (attribute['Experion Backup & Restore (Experion Server)'] == "Yes") else 0
									if 'Server Redundancy Requirement?' in attribute:
										total_servers += 2 if (attribute["Server Redundancy Requirement?"] == "Redundant") else 1
									if "Additional Servers" in attribute:
										total_servers += int(attribute["Additional Servers"])
									sections["Server Furniture (0-50)"] = total_servers if "Server Furniture (0-50)" in attribute else 0
									sections["Station Furniture (0-200)"] = total_stations if "Station Furniture (0-200)" in attribute else 0
									if qty_dict:
										for attr,val in qty_dict.items():
											if attr in attribute:
												qty_dict[attr] = attribute[attr]
							if sections:
								for attr_name, qty in sections.items():
									if attribute and (attribute[attr_name] == "Yes" or attribute[attr_name] > 0) and int(qty) > 0:
										addOrUpdateWriteIn(attr_name,qty)
							if qty_dict:
								for attr_name, qty in qty_dict.items():
									if int(qty) > 0:
										addOrUpdateWriteIn(attr_name,qty)

							WriteinProdCont.MakeAllRowsSelected()
							WriteinProdCont.Calculate()
							WriteinProduct.AddToQuote()
							Quote.Save(False)
	Log.Info('GS_R2Q_AddWriteIn Success-->>')
	final_request_body={'QuoteNumber':str(Param.QuoteNumber),'CartId':str(Param.CartId),'RevisionNumber': str(Param.RevisionNumber),'UserName':str(User.UserName),'Module':'New/Expansion','Action':'Update','Status':'Success','Action_List':[{'ActionName':'WriteIn','ScriptName':'GS_R2Q_AddWriteIn'}]}
	RestClient.Post(excel_Url, RestClient.SerializeToJson(str(final_request_body)),header)
except Exception as ex:
	Log.Info('GS_R2Q_AddWriteIn Fail-->>'+str(ex))
	final_request_body={'QuoteNumber':str(Param.QuoteNumber),'CartId':str(Param.CartId),'RevisionNumber': str(Param.RevisionNumber),'UserName':str(User.UserName),'Module':'New/Expansion','Action':'Update','Status':'Fail','Action_List':[{'ActionName':'WriteIn','ScriptName':'GS_R2Q_AddWriteIn','ErrorMessage':str(ex)}]}
	RestClient.Post(excel_Url, RestClient.SerializeToJson(str(final_request_body)),header)