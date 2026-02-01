models= []
m = []

modelScopeCont = Product.GetContainerByName('SC_WEP_Models_Scope_TNA')
invalidCont = Product.GetContainerByName('SC_WEP_Invalid_Models_TNA')

if modelScopeCont.Rows.Count:
    for row in modelScopeCont.Rows:
        model = row['Model']
        tnaquery = SqlHelper.GetFirst("select WEP_Model from SC_WEP_Models where WEP_Model='{}' and TAB='TNA'".format(model))
        if tnaquery is not None:
            if model in models:
                m.append(row.RowIndex)
                invalidrow = invalidCont.AddNewRow()
                invalidrow['Model'] = row['Model']
                invalidrow['Description'] = row['Description']
                invalidrow['Quantity'] = row['Quantity']
                invalidrow['Reason'] = "Duplicate Entry"
            else:
                models.append(model)
        else:
            m.append(row.RowIndex)
            invalidrow = invalidCont.AddNewRow()
            invalidrow['Model'] = row['Model']
            invalidrow['Description'] = row['Description']
            invalidrow['Quantity'] = row['Quantity']
            invalidrow['Reason'] = "Invalid Model number (CPQ)"

m.reverse()
for i in m:
    modelScopeCont.DeleteRow(i)
    modelScopeCont.Calculate()