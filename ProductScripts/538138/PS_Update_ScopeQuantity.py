if Product.Attr('SC_Product_Type').GetValue() == "Renewal":
    summary_cont = Product.GetContainerByName("SC_Labor_Summary_Container")
    if summary_cont.Rows.Count:
        for row in summary_cont.Rows:
            row['PY_Deliverables_Hours'] = '0' if row['PY_Deliverables_Hours'] == '' else row['PY_Deliverables_Hours']
            row['Renewal_Year_Deliverables_Hours'] = '0' if row['Renewal_Year_Deliverables_Hours'] == '' else row['Renewal_Year_Deliverables_Hours']
            row['BurdenRate'] = '0' if row['BurdenRate'] == '' else row['BurdenRate']
            row['Contigency_Cost'] = '0' if row['Contigency_Cost'] == '' else row['Contigency_Cost']
            SC_Renewal_check = row.Product.Attr('SC_Renewal_check').GetValue()
            if True:#SC_Renewal_check == '2' or SC_Renewal_check == '3' or SC_Renewal_check == '4':
                row['Final_Total_Cost_Price'] = str(float(row['Renewal_Year_Deliverables_Hours']) * float(row['BurdenRate']) + float(row['Contigency_Cost']))
                if float(row['PY_Deliverables_Hours']) > float(row['Renewal_Year_Deliverables_Hours']):
                    row['Scope_Reduction_Quantity'] = str(float(row['Renewal_Year_Deliverables_Hours']) - float(row['PY_Deliverables_Hours']))
                    row['Scope_Addition_Quantity'] = '0'
                    row['Comments'] = 'Scope Reduction'
                elif float(row['PY_Deliverables_Hours']) < float(row['Renewal_Year_Deliverables_Hours']):
                    row['Scope_Addition_Quantity'] = str(float(row['Renewal_Year_Deliverables_Hours']) - float(row['PY_Deliverables_Hours']))
                    row['Scope_Reduction_Quantity'] = '0'
                    row['Comments'] = 'Scope Addition'
                else:
                    row['Comments'] = 'No Scope Change'
                    row['Scope_Reduction_Quantity'] = '0'
                    row['Scope_Addition_Quantity'] = '0'
                row.Product.Attr('SC_Renewal_check').AssignValue('1')
            elif SC_Renewal_check == '3' or SC_Renewal_check == '4' or SC_Renewal_check == '2':
                row['Final_Total_Cost_Price'] = str(float(row['Renewal_Year_Deliverables_Hours']) * float(row['BurdenRate']) + float(row['Contigency_Cost']))
                row.Product.Attr('SC_Renewal_check').AssignValue('1')
else:
	summary_cont = Product.GetContainerByName("SC_Labor_Summary_Container")
	if summary_cont.Rows.Count:
		for row in summary_cont.Rows:
			row['Final_Total_Cost_Price'] = str(float(row['Deliverable_Hours']) * float(row['BurdenRate'])) if row['Deliverable_Hours'] and float(row['Deliverable_Hours']) > 0 and row['BurdenRate'] and float(row['BurdenRate']) > 0 else '0'