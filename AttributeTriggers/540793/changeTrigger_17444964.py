a=Product.Attr('SC_LSS_Scope_Selection_Button').GetValue().split(', ')
SC_LSS_Models_Summary_Cont=Product.GetContainerByName('SC_LSS_Models_Summary_Cont')
SC_LSS_Models_Summary_Cont_Hidden=Product.GetContainerByName('SC_LSS_Models_Summary_Cont_Hidden')
SC_LSS_Models_Summary_Cont.Clear()
for row in SC_LSS_Models_Summary_Cont_Hidden.Rows:
    if row['Comments'] in a :
        i = SC_LSS_Models_Summary_Cont.AddNewRow()
        i['Model'] = row['Model']
        i['Description'] = row['Description']
        i['Previous_Year_Quantity'] = row['PY_Quantity']
        i['Renewal_Quantity'] = row['CY_Quantity']
        i['Previous Year Unit List Price'] = row['PY_UnitPrice']
        i['Previous Year List Price'] = row['PY_ListPrice']
        i['Previous Year Unit Cost price']=row['PY_UnitCost']
        i['Previous Year Cost Price']=row['PY_CostPrice']
        i['Honeywell List Price Per unit'] = row['CY_UnitPrice']
        i['Honeywell List Price'] = row['CY_ListPrice']
        i['Current Year Unit Cost Price'] = row['CY_UnitCost']
        i['Current Year Cost Price']=row['CY_CostPrice']
        i['Scope Reduction Quantity']=row['SR_Quantity']
        i['Scope Addition Quantity']=row['SA_Quantity']
        i['Comments']=row['Comments']