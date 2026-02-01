#to filter MSID from MSID container:
mesmodel = Product.GetContainerByName('SC_MES_Models')
mesmodelhidden = Product.GetContainerByName('SC_MES_Models_Hidden')
SearchText = Product.Attr('SC_MES_Search_Model').GetValue()
mesmodel.Clear()
if SearchText == "" or SearchText == None:
    for row in mesmodelhidden.Rows:
        i = mesmodel.AddNewRow(False)
        i['MES Models'] = row['MES Models']
        i['Description'] = row['Description']
        i['Quantity'] = row['Quantity']
        i['Unit Price'] = row['Unit Price']
        i['List Price'] = row['List Price']
else:
    for row in mesmodelhidden.Rows:
        if SearchText.lower() in row['MES Models'].lower():
            i = mesmodel.AddNewRow(False)
            i['MES Models'] = row['MES Models']
            i['Description'] = row['Description']
            i['Quantity'] = row['Quantity']
            i['Unit Price'] = row['Unit Price']
            i['List Price'] = row['List Price']
mesmodel.Calculate()