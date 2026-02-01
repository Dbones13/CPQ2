Product.Attr('SC_Product_Status').AssignValue('1')
if Product.Name == 'Local Support Standby':
    m = Product.GetContainerByName('SC_LSS_Models_Summary_Cont')
    m.Rows.Clear()
    h = Product.GetContainerByName('SC_LSS_Models_Summary_Cont_Hidden')
    h.Rows.Clear()
    am = Product.GetContainerByName('SC_Local_Support_Standby_validModel')
if Product.Attr('SC_Product_Type').GetValue() is not None and Product.Attr('SC_Product_Type').GetValue() != 'Renewal':
    if Product.Name == 'Local Support Standby':
        for i in am.Rows:
            row = m.AddNewRow(False)
            rowh = h.AddNewRow(False)
            rowh['Model'] = row['Model'] = i['Model']
            rowh['Description'] = row['Description'] = i['Description']
            rowh['Hidden_List_Price'] = rowh['List_Price'] = row['List_Price'] = i['List Price']
            rowh['Hidden_Cost_Price'] = rowh['Cost_Price'] = row['Cost_Price'] = i['Cost Price']
            rowh['Quantity'] = row['Quantity'] = i['Quantity']
        else:
            m.Calculate()
if Product.Attr('SC_Product_Type').GetValue() is not None and Product.Attr('SC_Product_Type').GetValue() == 'Renewal' and Product.Name == 'Local Support Standby':
    ComparisonSummary = Product.GetContainerByName('ComparisonSummary')
    PreviousYearSellPrice = 0
    py_discount1 = 0
    for comrows in ComparisonSummary.Rows:
        py_discount1 = comrows['PY_Discount_SFDC'] if comrows['PY_Discount_SFDC']  else 0
    for i in am.Rows:
        row = m.AddNewRow(False)
        rowh = h.AddNewRow(False)
        rowh['Model'] = row['Model'] = i['Model']
        rowh['Description'] = row['Description'] = i['Description']
        rowh['PY_Quantity'] = row['Previous_Year_Quantity'] = i['Previous Year Quantity'] if i['Previous Year Quantity'] else '0'
        rowh['CY_Quantity'] = row['Renewal_Quantity'] = i['Renewal Quantity'] if i['Renewal Quantity'] else '0'
        rowh['PY_UnitPrice'] = row['Previous Year Unit List Price'] = i['Previous Year Unit List Price'] if i['Previous Year Unit List Price'] else '0'
        rowh['PY_ListPrice'] = row['Previous Year List Price'] = i['Previous Year List Price'] if i['Previous Year List Price'] else '0'
        rowh['PY_UnitCost'] = row['Previous Year Unit Cost price'] = i['Previous Year Unit Cost price'] if i['Previous Year Unit Cost price'] else '0'
        rowh['PY_CostPrice'] = row['Previous Year Cost price'] = i['Previous Year Cost price'] if i['Previous Year Cost price'] else '0'
        rowh['CY_UnitPrice'] = row['Honeywell List Price Per Unit'] = i['Honeywell List Price Per Unit']
        rowh['CY_ListPrice'] = row['Honeywell List Price'] = i['Honeywell List Price']
        rowh['CY_UnitCost'] = row['Current Year Unit Cost Price'] = i['Current Year Unit Cost Price']
        rowh['Hidden_Cost_Price'] = rowh['CY_CostPrice'] = row['Current Year Cost Price'] = i['Current Year Cost Price']
        rowh['Comments'] = row['Comments'] = i['Comment']
        if i['Previous Year Quantity'] !='' and i['Renewal Quantity'] !='':
            if i['Previous Year Quantity'] > i['Renewal Quantity']:
                rowh['SR_Quantity'] = row['Scope Reduction Quantity'] = str(int(i['Renewal Quantity'])-int(i['Previous Year Quantity']))
            elif i['Previous Year Quantity'] < i['Renewal Quantity']:
                rowh['SA_Quantity'] = row['Scope Addition Quantity'] = str(int(i['Renewal Quantity'])- int(i['Previous Year Quantity']))
        rowh['SA_Price'] = str(float(row['Honeywell List Price Per Unit']) * int(row['Scope Addition Quantity'])) if row['Scope Addition Quantity'] else "0"
        rowh['SR_Price'] =  str(float(row['Previous Year Unit List Price']) * int(row['Scope Reduction Quantity'])) if row['Scope Reduction Quantity'] else "0"
        if Product.Attr('SC_Pricing_Escalation').GetValue() == "Yes":
            rowh['Hidden_List_Price'] = rowh['List_Price'] = str(float(rowh['SR_Price']) + float(rowh['SA_Price']) + float(rowh['PY_ListPrice']))
            rowh['Escalation_Price'] = str(float(rowh['CY_Quantity'])*float(rowh['PY_ListPrice'])/float(rowh['PY_Quantity'])) if rowh['PY_Quantity'] not in ('','0') else '0'
        else:
            rowh['Hidden_List_Price'] = rowh['List_Price'] = str(row['Honeywell List Price'])
            rowh['Escalation_Price'] = '0'
        rowh.Calculate()
        PreviousYearSellPrice = float(rowh["PY_ListPrice"]) - (float(rowh["PY_ListPrice"]) * float(py_discount1))
        rowh['PY_SellPrice'] = str(PreviousYearSellPrice)
        rowh['LY_Discount'] = str(py_discount1)
    # Defect CXCPQ-101901
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