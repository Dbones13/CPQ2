if True:
    SummaryContHidden = Product.GetContainerByName('SC_RC_Honeywell_Scope_Summary_Pricing_Hidden')
    HW_Summary_Cont = Product.GetContainerByName('SC_Honeywell_Scope_Summary_Pricing')
    HW_Summary_Cont.Rows.Clear()
    x = Product.Attr("SC_HDP_RC_Selection").SelectedValues
    if SummaryContHidden.Rows.Count:
        for row in SummaryContHidden.Rows:
            for i in x:
                if i.Display == row["Comments"]:
                    HW_summary_row = HW_Summary_Cont.AddNewRow(False)
                    HW_summary_row['Description'] = row['Description']
                    HW_summary_row['Quantity'] = row['Quantity']
                    HW_summary_row['PY_Quantity'] = row['PY_Quantity']
                    HW_summary_row['PY_UnitPrice'] = row['PY_UnitPrice']
                    HW_summary_row['PY_ListPrice'] = row['PY_ListPrice']
                    HW_summary_row['HW_ListPrice'] = row['HW_ListPrice']
                    HW_summary_row['SR_Quantity'] = row['SR_Quantity']
                    HW_summary_row['SA_Quantity'] = row['SA_Quantity']
                    HW_summary_row['R_Quantity'] = row['Quantity']
                    HW_summary_row['Comments'] = row['Comments']
                    HW_summary_row.Calculate()
            HW_Summary_Cont.Calculate()