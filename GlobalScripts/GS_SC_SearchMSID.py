SESP_Models_Cont = Product.GetContainerByName('SC_SESP Models')
SESP_Models_Hid_Cont = Product.GetContainerByName('SC_SESP Models Hidden')
SearchText = Product.Attr('SC_MSID_Search_Field').GetValue()
SESP_Models_Cont.Clear()
if SearchText == "" or SearchText == None:
    for row in SESP_Models_Hid_Cont.Rows:
        i = SESP_Models_Cont.AddNewRow(False)
        i['MSID'] = row['MSID']
        i['System_Name'] = row['System_Name']
        i['System_Number'] = row['System_Number']
        i['Platform'] = row['Platform']
        i['Model#'] = row['Model#']
        i['Description'] = row['Description']
        i['Qty'] = row['Qty']
        i['UnitPrice'] = row['UnitPrice']
        i['Price'] = row['Price']
else:
    for row in SESP_Models_Hid_Cont.Rows:
        if SearchText.lower() in row['MSID'].lower():
            i = SESP_Models_Cont.AddNewRow(False)
            i['MSID'] = row['MSID']
            i['System_Name'] = row['System_Name']
            i['System_Number'] = row['System_Number']
            i['Platform'] = row['Platform']
            i['Model#'] = row['Model#']
            i['Description'] = row['Description']
            i['Qty'] = row['Qty']
            i['UnitPrice'] = row['UnitPrice']
            i['Price'] = row['Price']
SESP_Models_Cont.Calculate()
#SESP_Models_Hid_Cont.Calculate()