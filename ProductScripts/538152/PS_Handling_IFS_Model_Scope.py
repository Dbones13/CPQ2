models= []
m = []

modelScopeCont = Product.GetContainerByName('SC_WEP_Models_Scope_IFS')
invalidCont = Product.GetContainerByName('SC_WEP_Invalid_Models_IFS')

if modelScopeCont.Rows.Count:
    for row in modelScopeCont.Rows:
        model = row['Model']
        ifsquery = SqlHelper.GetFirst("select WEP_Model from SC_WEP_Models where WEP_Model='{}' and TAB='IFS'".format(model))
        if ifsquery is not None:
            if model in models:
                m.append(row.RowIndex)
                invalidrow = invalidCont.AddNewRow()
                invalidrow['Model'] = row['Model']
                invalidrow['Description'] = row['Description']
                if Product.Attr('SC_Product_Type').GetValue() == "New":
                    invalidrow['Quantity'] = row['Quantity']
                elif Product.Attr('SC_Product_Type').GetValue() == "Renewal":
                    invalidrow['Quantity'] = row['CY_Quantity']
                invalidrow['Reason'] = "Duplicate Entry"
            else:
                models.append(model)
        else:
            m.append(row.RowIndex)
            invalidrow = invalidCont.AddNewRow()
            invalidrow['Model'] = row['Model']
            invalidrow['Description'] = row['Description']
            if Product.Attr('SC_Product_Type').GetValue() == "New":
                invalidrow['Quantity'] = row['Quantity']
            elif Product.Attr('SC_Product_Type').GetValue() == "Renewal":
                invalidrow['Quantity'] = row['CY_Quantity']
            invalidrow['Reason'] = "Invalid Model number (CPQ)"

m.reverse()
for i in m:
    modelScopeCont.DeleteRow(i)
    modelScopeCont.Calculate()