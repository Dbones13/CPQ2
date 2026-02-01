if Product.Attr('SC_Product_Type').GetValue() =="Renewal":
    sespmodel=Product.GetContainerByName("SC_Models_Scope_Renewal")
    sespModelHidden = Product.GetContainerByName('SC_Models_Scope_Renewal_Hidden')
    m = []
    msid = []
    for row in sespModelHidden.Rows:
        if row['Renewal Quantity'] == row['Quantity'] == '0':
            m.append(row.RowIndex)
            if row['MSIDs'] not in msid:
                msid.append(row['MSIDs'])
    m.reverse()
    for i in m:
        sespModelHidden.DeleteRow(i)

    #Clean UI container and align as per search criteria
    SearchText = Product.Attr('SC_MSID_Search_Sope_Selection').GetValue()
    sespmodel.Clear()
    for row in sespModelHidden.Rows:
        if SearchText == "" or SearchText == None or SearchText.lower() in row['MSIDs'].lower():
            i = sespmodel.AddNewRow(False)
            i['Asset Validation Line Item Number']=row['Asset Validation Line Item Number']
            i['MSIDs'] = row['MSIDs']
            i['System_Name'] = row['System_Name']
            i['System_Number'] = row['System_Number']
            i['Platform'] = row['Platform']
            i['SESP_Models'] = row['SESP_Models']
            i['Description'] = row['Description']
            i['Quantity'] = row['Quantity']
            i['Previous Year Unit Price'] = row['Previous Year Unit Price']
            i['Previous Year List Price'] = row['Previous Year List Price']
            i['Renewal Quantity']=row['Renewal Quantity']
            i['Comments']=row['Comments']
            i['Difference']=row['Difference']
            i['HiddenRowIndex'] = str(row.RowIndex)


    #enabled services checkbox is selected - begin
    es = Product.Attr('EnableSelection_SESP').SelectedValue
    if es and len(msid):
        rowIndex = []
        cont = Product.GetContainerByName('Asset_details_ServiceProd')
        for row in cont.Rows:
            if row['MSID'] in msid:
                rowIndex.append(row.RowIndex)
        rowIndex.reverse()
        for i in rowIndex:
            cont.DeleteRow(i)
        if len(rowIndex):
            cont.Calculate()
    #enabled services checkbox is selected - end
    ScriptExecutor.Execute('PS_SESPModelRenewal_Errors')
    Product.Attr('SC_Product_Status').AssignValue("0")