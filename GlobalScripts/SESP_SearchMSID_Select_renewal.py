SESP_Models_Cont_Renewal = Product.GetContainerByName('SC_Models_Scope_Renewal')
SESP_Models_Hid_Cont_Renewal = Product.GetContainerByName('SC_Models_Scope_Renewal_Hidden')
SearchText = Product.Attr('SC_MSID_Search_Sope_Selection').GetValue()
SESP_Models_Cont_Renewal.Clear()
#SESP_Models_Hid_Cont_Renewal.Rows.
if SearchText == "" or SearchText == None:
    for row in SESP_Models_Hid_Cont_Renewal.Rows:
        i = SESP_Models_Cont_Renewal.AddNewRow(False)
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
else:
    for row in SESP_Models_Hid_Cont_Renewal.Rows:
        Trace.Write(SearchText)
        if SearchText.lower() in row['MSIDs'].lower():
            i = SESP_Models_Cont_Renewal.AddNewRow(False)
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
            i['Difference']=row['Difference']
            i['Comments']=row['Comments']
            i['HiddenRowIndex'] = str(row.RowIndex)
#SESP_Models_Cont_Renewal.Calculate()
#SESP_Models_Hid_Cont_Renewal.Calculate()