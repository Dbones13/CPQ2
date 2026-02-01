try:
	if Product.Attr('SC_Product_Type').GetValue() is not None and Product.Attr('SC_Product_Type').GetValue() != 'Renewal':
		if Product.Name == 'Hardware Warranty' or Product.Name == 'Hardware Refresh':
			m = Product.GetContainerByName('HWOS_Model Scope_3party_ScopeSummary')
			m.Rows.Clear()
			am = Product.GetContainerByName('HWOS_Model Scope_3party')
			for i in am.Rows:
				row = m.AddNewRow(False)
				row['Asset'] = i['Asset']
				row['3rd Party Model'] = i['3rd Party Model']
				row['Description'] = i['Description']
				row['Ext Cost'] = i['Ext Cost']
				row['List Price'] = i['List Price']
				row['Quantity'] = i['Quantity']
			else:
				m.Calculate()
		if Product.Name == 'Hardware Refresh':
			setDefaultValues = SqlHelper.GetList("select ServiceProduct, Entitlement from CT_SC_ENTITLEMENTS_DATA where IsMandatory = 'True' and ServiceProduct = '{}'".format('Hardware Refresh'))
			o = Product.GetContainerByName('HWOS_Entitlement_Optional')
			o.Rows.Clear()
			e = Product.GetContainerByName('HWOS_Entitlement')
			for i in setDefaultValues:
				row = o.AddNewRow(False)
				row['Include'] = 'Mandatory'
				row['Entitlement'] = i.Entitlement
			else:
				o.Calculate()
			for i in e.Rows:
				if i.IsSelected:
					row = o.AddNewRow(False)
					row['Include'] = 'Optional'
					row['Entitlement'] = i['Entitlement']
			else:
				o.Calculate()

		if Product.Name == 'Hardware Warranty':
			setDefaultValues = SqlHelper.GetList("select ServiceProduct, Entitlement from CT_SC_ENTITLEMENTS_DATA where IsMandatory = 'True' and ServiceProduct = '{}'".format('Hardware Warranty'))
			o = Product.GetContainerByName('HWOS_Entitlement_Optional')
			o.Rows.Clear()
			e = Product.GetContainerByName('HWOS_Entitlement')
			for i in setDefaultValues:
				row = o.AddNewRow(False)
				row['Include'] = 'Mandatory'
				row['Entitlement'] = i.Entitlement
			else:
				o.Calculate()
			for i in e.Rows:
				if i.IsSelected:
					row = o.AddNewRow(False)
					row['Include'] = 'Optional'
					row['Entitlement'] = i['Entitlement']
			else:
				o.Calculate()

		if Product.Name == 'Workforce Excellence Program' or Product.Name == 'Trace':
			o = Product.GetContainerByName('HWOS_Entitlement_Optional')
			o.Rows.Clear()
			e = Product.GetContainerByName('HWOS_Entitlement')
			for i in e.Rows:
				row = o.AddNewRow(False)
				if i.IsSelected:
					row['Include'] = 'Mandatory'
				else:
					row['Include'] = "Optional"
				row['Entitlement'] = i['Entitlement']
			else:
				o.Calculate()
			m = Product.GetContainerByName('HWOS_Model Scope_3party_ScopeSummary')
			m.Rows.Clear()
			am = Product.GetContainerByName('HWOS_Model Scope_3party')
			for i in am.Rows:
				row = m.AddNewRow(False)
				row['Service Product'] = row['Service Product']
				row['3rd Party Model'] = i['3rd Party Model']
				row['Description'] = i['Description']
				row['Ext Cost'] = i['Ext Cost']
				row['Unit Cost'] = i['Unit Cost']
				row['Unit List Price'] = i['Unit List Price']
				row['List Price'] = i['List Price']
				row['Quantity'] = i['Quantity']
			else:
				m.Calculate()
		if arg.NameOfCurrentTab == "Scope Summary" and Product.Name == "Training":
			en_Cont = Product.GetContainerByName('HWOS_Entitlement').Rows
			en_Sum_Cont = Product.GetContainerByName('HWOS_3rdParty_Training_Entitlements_Summary')
			en_Sum_Cont.Clear()
			for enRow in en_Cont:
				EntitleRow = en_Sum_Cont.AddNewRow(False)
				EntitleRow["Service Product"] = "Training"
				EntitleRow["Entitlement"] = enRow["Entitlement"]
			valid_Cont = Product.GetContainerByName('HWOS_Model Scope_3party_Training').Rows
			valid_Sum_Cont = Product.GetContainerByName('HWOS_3rdParty_Training_Summary')
			valid_Sum_Cont.Clear()
			for validRow in valid_Cont:
				summaryRow = valid_Sum_Cont.AddNewRow(False)
				summaryRow["Models"] = validRow["Standard Models"]
				summaryRow["Quantity"] = validRow["Quantity"]
				summaryRow["List Price"] = validRow["List Price"]
				summaryRow["Cost"] = validRow["Cost"]
except Exception as e:
	Trace.Write('Exception in honeywell other service product script name - UpdateScopeSummaryDetails')
