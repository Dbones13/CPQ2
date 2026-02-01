labCont = Product.GetContainerByName("SC_Labor_Summary_Container")
X = 0
for row in labCont.Rows:

    if row['Lumpsum'] == "Y":

        if row.Product.Attr('SC_Labor_Service_Product').GetValue() == '' or row.Product.Attr('SC_Labor_Entitlement').GetValue() == '':
            X = 1
    if row['Lumpsum'] == "N":
        if row.Product.Attr('SC_Labor_Service_Product').GetValue() == '' or row.Product.Attr('SC_Labor_Entitlement').GetValue() == ''or row.Product.Attr('SC_Labor_Resource_Type').GetValue() == '':
            X = 2
Product.Attr('SC_Labor_errormsg').AssignValue(str(X))