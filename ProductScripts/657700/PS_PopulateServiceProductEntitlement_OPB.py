prev_quote = Quote.GetCustomField("SC_CF_Parent_Quote_Number_Link").Content
active_contract = Quote.GetCustomField("SC_CF_Parent_Contract_Number_Link").Content
SPList = []
serviceProduct = ""
Service = Product.GetContainerByName('SC_GN_AT_Service_Product_Cont')
				
entitle_list = []
if Product.Attr('SC_Product_Type').GetValue() == "Renewal":
		opt_ent_cont = Product.GetContainerByName('SC_GN_AT_Optional_Ent_Cont')
		opt_ent_cont.Rows.Clear()
		from CPQ_SF_SC_Modules import CL_SC_Modules
		Contract_Number = Quote.GetCustomField("SC_CF_Parent_Contract_Number_Link").Content
		class_contact_modules = CL_SC_Modules(Quote, TagParserQuote, None,Session)
		resp = class_contact_modules.get_ContractRenewalLineItem_Data(Contract_Number)
		Trace.Write('Response-->'+str(resp))
		for record in resp["records"]:
				product_name = str(record["Service_Product_Name__c"])
				entitlement_name = str(record["Name"])
				entitle_list.append(entitlement_name)
				entitlement_query = SqlHelper.GetFirst("Select Product_Type,ServiceProduct,Entitlement,IsMandatory from CT_SC_ENTITLEMENTS_DATA where Module_Name = 'Generic Module' and ServiceProduct = '{}'".format(product_name))
				if entitlement_query is not None:
						serviceProduct = product_name
						selected_val= Product.Attr('SC_GN_AT_Product_Family').SelectedValue
						if not selected_val:
								Product.Attr('SC_GN_AT_Product_Family').SelectDisplayValue(entitlement_query.Product_Type)
								rowidx = Product.GetContainerByName('SC_GN_AT_Service_Product_Cont').Rows.GetByColumnName('Service_Product', product_name).RowIndex if Product.GetContainerByName('SC_GN_AT_Service_Product_Cont').Rows.GetByColumnName('Service_Product', product_name) else -1
								if rowidx != -1:
									Product.GetContainerByName('SC_GN_AT_Service_Product_Cont').MakeRowSelected(rowidx, False)
						else:
								rowidx = Product.GetContainerByName('SC_GN_AT_Service_Product_Cont').Rows.GetByColumnName('Service_Product', product_name).RowIndex if Product.GetContainerByName('SC_GN_AT_Service_Product_Cont').Rows.GetByColumnName('Service_Product', product_name) else -1
								if rowidx != -1:
									Product.GetContainerByName('SC_GN_AT_Service_Product_Cont').MakeRowSelected(rowidx, False)
						Product.GetContainerByName('SC_GN_AT_Service_Product_Cont').Calculate()
		S = []
		for SP_row in Service.Rows:
			SP_row.IsSelected == True
			S.append(str(SP_row['Service_Product']))
		Trace.Write(str(S))
		for SP in S:
			listt = SqlHelper.GetList("select Distinct Entitlement from CT_SC_ENTITLEMENTS_DATA where IsMandatory = 'False' and Module_Name = 'Generic Module' and ServiceProduct = '{}' ".format(SP))
			for row in listt:
				i = opt_ent_cont.AddNewRow()
				i['Service_Product'] = str(SP)
				i['Optional_Entitlement'] = row.Entitlement
				if row.Entitlement in entitle_list:
					i.IsSelected = True
			Product.Attr('SC_OPB_Check_SP_Ent').AssignValue('1')