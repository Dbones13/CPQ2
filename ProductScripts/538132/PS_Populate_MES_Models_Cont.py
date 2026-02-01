SC_Product_Type = Product.Attr('SC_Product_Type').GetValue()
if SC_Product_Type == 'New':
    modelScopeCont = Product.GetContainerByName('SC_MES_Models_Scope')
    scopeCont = Product.GetContainerByName('SC_MES_Models')
    scopeContHidden = Product.GetContainerByName('SC_MES_Models_Hidden')
    scopeContHidden.Rows.Clear()
    serprod_lictype = {"MES Batch Maintenance Services":"Term","MES Batch Services Term":"Perpetual"}
    serviceproduct = Product.Attr("SC_MES_Service_Product").GetValue()
    SearchText = Product.Attr('SC_MES_Search_Model').GetValue()


    if SearchText == "" or SearchText == None:
        scopeCont.Rows.Clear()

    if modelScopeCont.Rows.Count:
        for row in modelScopeCont.Rows:
            mesmodel = row['MES Models']
            mesquery = SqlHelper.GetFirst("select MES_Model,License_Type from SC_MES_Models where MES_Model='{}'".format(mesmodel))
            if mesquery is not None:
                if serviceproduct in serprod_lictype.keys():
                    if mesquery.License_Type == serprod_lictype[serviceproduct] and row['Quantity'] not in ("","0") and row['Unit_Price'] not in ("","0.00","0"):
                        scopeContRowHidden = scopeContHidden.AddNewRow(False)
                        scopeContRowHidden['MES Models'] = mesmodel
                        scopeContRowHidden['Description'] = row['Description']
                        scopeContRowHidden['Quantity'] = row['Quantity']
                        scopeContRowHidden['Unit Price'] = row['Unit_Price']
                        scopeContRowHidden['List Price'] = row['List_Price']
                        scopeContRowHidden.Calculate()
                        if SearchText == "" or SearchText == None:
                            scopeContRow = scopeCont.AddNewRow(False)
                            scopeContRow['MES Models'] = mesmodel
                            scopeContRow['Description'] = row['Description']
                            scopeContRow['Quantity'] = row['Quantity']
                            scopeContRow['Unit Price'] = scopeContRowHidden['Unit Price']
                            scopeContRow['List Price'] = scopeContRowHidden['List Price']
                            scopeContRow.Calculate
        scopeContHidden.Calculate()
        scopeCont.Calculate()

if SC_Product_Type == 'Renewal':
    modelScopeCont = Product.GetContainerByName('SC_MES_Models_Scope')
    scopeCont = Product.GetContainerByName('SC_MES_Models')
    scopeContHidden = Product.GetContainerByName('SC_MES_Models_Hidden')
    serviceproduct = Product.Attr("SC_MES_Service_Product").GetValue()
    comparisonCont = Product.GetContainerByName('ComparisonSummary')
    scopeContHidden.Rows.Clear()
    scopeCont.Rows.Clear()

    comparisonCont = Product.GetContainerByName('ComparisonSummary')
    compDict = {}
    if comparisonCont.Rows.Count:
        for compRow in comparisonCont.Rows:
            compDict[compRow["Service_Product"]] = compRow["PY_Discount_SFDC"] if compRow["PY_Discount_SFDC"] else '0'

    if modelScopeCont.Rows.Count:
        for row in modelScopeCont.Rows:
            scopeContRowHidden = scopeContHidden.AddNewRow(False)
            scopeContRowHidden['MES Models'] = row['MES Models']
            scopeContRowHidden['Description'] = row['Description']
            scopeContRowHidden['Quantity'] = row['Renewal_Quantity']
            scopeContRowHidden['Unit Price'] = row['HW_UnitPrice']
            scopeContRowHidden['PY_Quantity'] = row['PY_Quantity']
            scopeContRowHidden['Renewal_Quantity'] = row['Renewal_Quantity']
            scopeContRowHidden['PY_UnitPrice'] = row['PY_UnitPrice']
            scopeContRowHidden['PY_ListPrice'] = row['PY_ListPrice']
            scopeContRowHidden['HW_UnitPrice'] = row['HW_UnitPrice']
            scopeContRowHidden.Calculate()
            if int(row['Renewal_Quantity']) > int(row['PY_Quantity']):
                scopeContRowHidden['SR_Quantity'] = '0'
                scopeContRowHidden['SA_Quantity'] = str(int(row['Renewal_Quantity'])-int(row['PY_Quantity']))
                scopeContRowHidden['Comments'] = "Scope Addition"
            elif int(row['Renewal_Quantity']) < int(row['PY_Quantity']):
                scopeContRowHidden['SR_Quantity'] = str(int(row['Renewal_Quantity'])-int(row['PY_Quantity']))
                scopeContRowHidden['SA_Quantity'] = '0'
                scopeContRowHidden['Comments'] = "Scope Reduction"
            else:
                scopeContRowHidden['SR_Quantity'] = '0'
                scopeContRowHidden['SA_Quantity'] = '0'
                scopeContRowHidden['Comments'] = "No Scope Change"
            scopeContRowHidden['SR_Price'] = str(float(row['PY_UnitPrice'])*float(scopeContRowHidden['SR_Quantity']))
            scopeContRowHidden['SA_Price'] = str(float(row['HW_UnitPrice'])*float(scopeContRowHidden['SA_Quantity']))
            if Product.Attr('SC_Pricing_Escalation').GetValue() == "Yes":
                if int(row['Renewal_Quantity']) > int(row['PY_Quantity']):
                    scopeContRowHidden['Escalation_Price'] = str(float(row['PY_Quantity'])*float(row['PY_UnitPrice']))
                    scopeContRowHidden['List Price'] = str((float(row['PY_Quantity'])*float(row['PY_UnitPrice'])) + ((int(row['Renewal_Quantity']) - int(row['PY_Quantity']))*float(row['HW_UnitPrice'])))
                else:
                    scopeContRowHidden['Escalation_Price'] = str(float(row['Renewal_Quantity'])*float(row['PY_UnitPrice']))
                    scopeContRowHidden['List Price'] = str(float(row['Renewal_Quantity'])*float(row['PY_UnitPrice']))
            else:
                scopeContRowHidden['Escalation_Price'] = '0'
                scopeContRowHidden['List Price'] = row['HW_ListPrice']
            py_discount = float(compDict.get(serviceproduct,0))
            scopeContRowHidden["PY_Discount"] = str(py_discount * 100)
            scopeContRowHidden["PY_SellPrice"] = str(float(scopeContRowHidden['PY_ListPrice']) - (float(scopeContRowHidden['PY_ListPrice']) * py_discount))
            scopeContRowHidden.Calculate()
        scopeContHidden.Calculate()

    x = Product.Attr("SC_MES_RC_Selection").SelectedValues
    if scopeContHidden.Rows.Count:
        for row in scopeContHidden.Rows:
            for i in x:
                if i.Display == row["Comments"]:
                    scopeContRow = scopeCont.AddNewRow(False)
                    scopeContRow['MES Models'] = row['MES Models']
                    scopeContRow['Description'] = row['Description']
                    scopeContRow['Quantity'] = row['Quantity']
                    scopeContRow['Unit Price'] = row['HW_UnitPrice']
                    scopeContRow['PY_Quantity'] = row['PY_Quantity']
                    scopeContRow['Renewal_Quantity'] = row['Quantity']
                    scopeContRow['PY_UnitPrice'] = row['PY_UnitPrice']
                    scopeContRow['PY_ListPrice'] = row['PY_ListPrice']
                    scopeContRow['HW_UnitPrice'] = row['HW_UnitPrice']
                    scopeContRow['SR_Quantity'] = row['SR_Quantity']
                    scopeContRow['SA_Quantity'] = row['SA_Quantity']
                    scopeContRow['Comments'] = row['Comments']
                    scopeContRow['List Price'] = row['List Price']
                    scopeContRow.Calculate()
        scopeCont.Calculate()