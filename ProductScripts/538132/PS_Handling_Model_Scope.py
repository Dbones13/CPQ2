SC_Product_Type = Product.Attr('SC_Product_Type').GetValue()
if SC_Product_Type == 'New':
    serprod_lictype = {"MES Batch Maintenance Services":"Term","MES Batch Services Term":"Perpetual"}
    serviceproduct = Product.Attr("SC_MES_Service_Product").GetValue()
    m= []
    list_index = 0
    to_be_added = {}

    modelScopeCont = Product.GetContainerByName('SC_MES_Models_Scope')
    invalidCont = Product.GetContainerByName('SC_MES_Invalid_Models')

    if modelScopeCont.Rows.Count:
        for row in modelScopeCont.Rows:
            mesmodel = row['MES Models']
            mesquery = SqlHelper.GetFirst("select MES_Model,License_Type from SC_MES_Models where MES_Model='{}'".format(mesmodel))
            if mesquery is not None:
                if serviceproduct in serprod_lictype.keys():
                    if mesquery.License_Type != serprod_lictype[serviceproduct]:
                        m.append(row.RowIndex)
                        invalidrow = invalidCont.AddNewRow()
                        invalidrow['MES Models'] = row['MES Models']
                        invalidrow['Description'] = row['Description']
                        invalidrow['Quantity'] = row['Quantity']
                        invalidrow['Reason'] = "Part is not associated with Service Product"
            else:
                m.append(row.RowIndex)
                invalidrow = invalidCont.AddNewRow()
                invalidrow['MES Models'] = row['MES Models']
                invalidrow['Description'] = row['Description']
                invalidrow['Quantity'] = row['Quantity']
                invalidrow['Reason'] = "Invalid Model number (CPQ)"

    m.reverse()
    for i in m:
        modelScopeCont.DeleteRow(i)
        modelScopeCont.Calculate()

elif SC_Product_Type == 'Renewal':
    serprod_lictype = {"MES Batch Maintenance Services":"Term","MES Batch Services Term":"Perpetual"}
    serviceproduct = Product.Attr("SC_MES_Service_Product").GetValue()
    m= []
    list_index = 0
    to_be_added = {}

    modelScopeCont = Product.GetContainerByName('SC_MES_Models_Scope')
    invalidCont = Product.GetContainerByName('SC_MES_Invalid_Models')

    if modelScopeCont.Rows.Count:
        for row in modelScopeCont.Rows:
            mesmodel = row['MES Models']
            mesquery = SqlHelper.GetFirst("select MES_Model,License_Type from SC_MES_Models where MES_Model='{}'".format(mesmodel))
            if mesquery is not None:
                if serviceproduct in serprod_lictype.keys():
                    if mesquery.License_Type != serprod_lictype[serviceproduct]:
                        m.append(row.RowIndex)
                        invalidrow = invalidCont.AddNewRow()
                        invalidrow['MES Models'] = row['MES Models']
                        invalidrow['Description'] = row['Description']
                        invalidrow['Renewal_Quantity'] = row['Renewal_Quantity'] if row['Renewal_Quantity'] else "0"
                        invalidrow['PY_Quantity'] = row['PY_Quantity']
                        invalidrow['Reason'] = "Part is not associated with Service Product"
            else:
                m.append(row.RowIndex)
                invalidrow = invalidCont.AddNewRow()
                invalidrow['MES Models'] = row['MES Models']
                invalidrow['Description'] = row['Description']
                invalidrow['Renewal_Quantity'] = row['Renewal_Quantity'] if row['Renewal_Quantity'] else "0"
                invalidrow['PY_Quantity'] = row['PY_Quantity']
                invalidrow['Reason'] = "Invalid Model number (CPQ)"

    m.reverse()
    for i in m:
        modelScopeCont.DeleteRow(i)
        modelScopeCont.Calculate()