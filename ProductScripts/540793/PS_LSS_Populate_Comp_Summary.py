tabs = [tab.Name for tab in Product.Tabs if tab.IsSelected]
if 'Scope Summary' in tabs:
	value = "0"
	PY_ListPrice_HW = 0
	PY_ListPrice_Support = 0
	PreviousYearListPrice =0.0
	SC_Product_Type = Product.Attr('SC_Product_Type').GetValue()
	if SC_Product_Type == 'Renewal':
		HW_Cont = Product.GetContainerByName('SC_Local_Support_Standby_validModel')
		if HW_Cont.Rows.Count:
			for row in HW_Cont.Rows:
				if Product.Name in ['Local Support Standby'] and row['Previous Year List Price']:
					PreviousYearListPrice += float(row['Previous Year List Price'])
			if PreviousYearListPrice == 0.0:
				value = "1"
			else:
				PY_ListPrice_HW = str(PreviousYearListPrice)
				Trace.Write(PY_ListPrice_HW)
		ComparisonSummary = Product.GetContainerByName("ComparisonSummary")
		if ComparisonSummary.Rows.Count:
			for row in ComparisonSummary.Rows:
				if row['Service_Product']:
					if value == "1":
						row['Configured_PY_List_Price'] = row['PY_List_Price_SFDC']
						row['Configured_PY_Sell_Price'] = row['PY_Sell_Price_SFDC']
					else:
						row['Configured_PY_List_Price'] = str(PY_ListPrice_HW)
						row['Configured_PY_Sell_Price'] = str(float(row['Configured_PY_List_Price']) - (float(row['Configured_PY_List_Price']) * float(row['PY_Discount_SFDC']))) if row['PY_Discount_SFDC'] else str(float(row['Configured_PY_List_Price']))
				Trace.Write("row['Configured_PY_List_Price']" +str(row['Configured_PY_List_Price']))
				if row['Configured_PY_List_Price'] == "0":
					row['Configured_PY_List_Price'] = row['PY_List_Price_SFDC']
					row['Configured_PY_Sell_Price'] = row['PY_Sell_Price_SFDC']
				row.Calculate()
			ComparisonSummary.Calculate()