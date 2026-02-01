SC_Product_Type = Product.Attr('SC_Product_Type').GetValue()
if SC_Product_Type == 'New':
    tabs = [tab.Name for tab in Product.Tabs if tab.IsSelected]
    if 'Scope Summary' in tabs:
        model_summary = Product.GetContainerByName("SC_Experion_Models_Summary")
        hiddenCont = Product.GetContainerByName('SC_Experion_Models_Hidden')
        hiddenCont.Rows.Clear()
        model_summary.Rows.Clear()

        model_scope = Product.GetContainerByName('SC_Experion_Models_Scope')

        if model_scope.Rows.Count:
            for row in model_scope.Rows:
                if (row["MSIDs"] != '') and (row["List_Price"] not in ['', '0.00','0']) and (row["Cost_Price"] not in ['', '0.00','0']):
                    row["Hidden_Quantity"] = row["Quantity"]
                    row["Hidden_ListPrice"] = row["List_Price"]
                    row["Hidden_CostPrice"] = row["Cost_Price"]
                    sRow = model_summary.AddNewRow(False)
                    sRow["MSIDs"] = row["MSIDs"]
                    sRow["Description"] = row["Description"]
                    sRow["Quantity"] = row["Quantity"]
                    sRow["List_Price"] = row["List_Price"]
                    sRow["Cost_Price"] = row["Cost_Price"]
                    hRow = hiddenCont.AddNewRow(False)
                    hRow["MSIDs"] = row["MSIDs"]
                    hRow["Description"] = row["Description"]
                    hRow["Quantity"] = row["Quantity"]
                    hRow["List_Price"] = row["List_Price"]
                    hRow["Cost_Price"] = row["Cost_Price"]
            hiddenCont.Calculate()
elif SC_Product_Type == 'Renewal':
    modelScopeCont = Product.GetContainerByName('SC_Experion_Models_Scope')
    summaryCont = Product.GetContainerByName('SC_Experion_Models_Summary')
    hiddenCont = Product.GetContainerByName('SC_Experion_Models_Hidden')
    serviceproduct = Product.Attr("SC_Exp_Ext_Supp_RQUP_summary").GetValue()
    hiddenCont.Rows.Clear()
    summaryCont.Rows.Clear()

    comparisonCont = Product.GetContainerByName('ComparisonSummary')
    compDict = {}
    if comparisonCont.Rows.Count:
        for compRow in comparisonCont.Rows:
            compDict[compRow["Service_Product"]] = compRow["PY_Discount_SFDC"] if compRow["PY_Discount_SFDC"] else '0'

    if modelScopeCont.Rows.Count:
        for row in modelScopeCont.Rows:
            scopeContRowHidden = hiddenCont.AddNewRow(False)
            scopeContRowHidden['MSIDs'] = row['MSIDs']
            scopeContRowHidden['Description'] = row['Description']
            scopeContRowHidden['PY_Quantity'] = row['PY_Quantity']
            scopeContRowHidden['Renewal_Quantity'] = row['Renewal_Quantity']
            scopeContRowHidden['PY_ListPrice'] = row['PY_ListPrice']
            scopeContRowHidden['PY_CostPrice'] = row['PY_CostPrice']
            scopeContRowHidden['HW_ListPrice'] = row['HW_ListPrice']
            #scopeContRowHidden['List_Price'] = row['HW_ListPrice']
            scopeContRowHidden['Cost_Price'] = row['Cost_Price']
            scopeContRowHidden['SR_Price'] = row['SR_Price'] if row['SR_Price'] != '' else '0'
            scopeContRowHidden['SA_Price'] = row['SA_Price'] if row['SA_Price'] != '' else '0'
            scopeContRowHidden['Comment'] = row['Comment']
            #scopeContRowHidden['PY_SellPrice'] = row['PY_SellPrice']
            #scopeContRowHidden['LY_Discount'] = row['LY_Discount']
            Trace.Write("Renewal_Quantity: "+str(row['Renewal_Quantity']))
            Trace.Write("PY_Quantity: "+str(row['PY_Quantity']))
            row['SR_Price'] = row['SR_Price'] if row['SR_Price'] != '' else '0'
            row['SA_Price'] = row['SA_Price'] if row['SA_Price'] != '' else '0'
            if Product.Attr('SC_Pricing_Escalation').GetValue() == "Yes":
                if float(row['Renewal_Quantity']) > float(row['PY_Quantity']):
                    scopeContRowHidden['List_Price'] = str(float(row['PY_ListPrice'])+float(row['SR_Price'])+float(row['SA_Price']))
                    scopeContRowHidden['Escalation_Price'] = str(float(row['PY_ListPrice']) - float(row['SR_Price']))
                    #scopeContRowHidden['List_Price'] = str(float(row['PY_ListPrice']) + (float(row['Renewal_Quantity']) - float(row['PY_Quantity'])))
                    #scopeContRowHidden['Escalation_Price'] = str(float(row['PY_Quantity'])*float(row['PY_ListPrice']))
                else:
                    scopeContRowHidden['List_Price'] = str(float(row['PY_ListPrice'])+float(row['SR_Price'])+float(row['SA_Price']))
                    scopeContRowHidden['Escalation_Price'] = str(float(row['PY_ListPrice']) - float(row['SR_Price']))
                    #scopeContRowHidden['List_Price'] = str(float(row['Renewal_Quantity'])*(float(row['PY_Quantity'])*(float(row['PY_ListPrice'])/float(row['PY_Quantity']) if row['PY_Quantity'] != '' else '0')))
                    #scopeContRowHidden['Escalation_Price'] = str(float(row['Renewal_Quantity'])*(float(row['PY_Quantity'])*(float(row['PY_ListPrice'])/float(row['PY_Quantity']) if row['PY_Quantity'] != '' else '0')))
            else:
                scopeContRowHidden['List_Price'] = str(row['HW_ListPrice'])
                scopeContRowHidden['Escalation_Price'] = '0'
            py_discount = float(compDict.get(serviceproduct,0))
            scopeContRowHidden["LY_Discount"] = str(py_discount * 100)
            scopeContRowHidden["PY_SellPrice"] = str(float(scopeContRowHidden['PY_ListPrice']) - (float(scopeContRowHidden['PY_ListPrice']) * py_discount))
            scopeContRowHidden.Calculate()
        hiddenCont.Calculate()

    x = Product.Attr("SC_Experion_RC_Selection").SelectedValues
    if hiddenCont.Rows.Count:
        for row in hiddenCont.Rows:
            for i in x:
                if i.Display == row["Comment"]:
                    summaryContRow = summaryCont.AddNewRow(False)
                    summaryContRow['MSIDs'] = row['MSIDs']
                    summaryContRow['Description'] = row['Description']
                    summaryContRow['PY_Quantity'] = row['PY_Quantity']
                    summaryContRow['Renewal_Quantity'] = row['Renewal_Quantity']
                    summaryContRow['PY_ListPrice'] = row['PY_ListPrice']
                    summaryContRow['PY_CostPrice'] = row['PY_CostPrice']
                    summaryContRow['HW_ListPrice'] = row['HW_ListPrice']
                    summaryContRow['Cost_Price'] = row['Cost_Price']
                    summaryContRow['SR_Price'] = row['SR_Price']
                    summaryContRow['SA_Price'] = row['SA_Price']
                    summaryContRow['Comment'] = row['Comment']
                    summaryContRow.Calculate()
                summaryCont.Calculate()