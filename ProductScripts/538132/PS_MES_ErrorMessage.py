SC_Product_Type = Product.Attr('SC_Product_Type').GetValue()
if SC_Product_Type == 'New':
    messcope = Product.GetContainerByName("SC_MES_Models_Scope")
    err_msg = ""
    err_msg_1 = ""
    err_msg_2 = ""
    err_msg_3 = ""

    serprod_lictype = {"MES Batch Maintenance Services":"Term","MES Batch Services Term":"Perpetual"}
    serviceproduct = Product.Attr("SC_MES_Service_Product").GetValue()

    if messcope.Rows.Count > 0:
        for row in messcope.Rows:
            if row['Quantity'] == "0" or row['Quantity'] == "":
                err_msg += "Quantity is invalid on row:" + str(row.RowIndex+1) + "<br>"
            mesquery = SqlHelper.GetFirst("select MES_Model,License_Type from SC_MES_Models where MES_Model='{}'".format(row["MES Models"]))
            if row['Description'] == "":
                err_msg_1 += "Blank Description:" + str(row.RowIndex+1) + "<br>"
            if mesquery is None:
                err_msg_2 += "MES Model is invalid on row:" + str(row.RowIndex+1) + "<br>"
            else:
                 if serviceproduct in serprod_lictype.keys():
                    if mesquery.License_Type != serprod_lictype[serviceproduct]:
                        err_msg_3 += "MES Model is not associated with Service Product on row:" + str(row.RowIndex+1) + "<br>"

    ErrorMsg = err_msg + err_msg_1 + err_msg_2 + err_msg_3
    Product.Attr("Error_Message").AssignValue(ErrorMsg)

elif SC_Product_Type == 'Renewal':
    messcope = Product.GetContainerByName("SC_MES_Models_Scope")
    err_msg = ""
    err_msg_1 = ""
    err_msg_2 = ""
    err_msg_3 = ""

    serprod_lictype = {"MES Batch Maintenance Services":"Term","MES Batch Services Term":"Perpetual"}
    serviceproduct = Product.Attr("SC_MES_Service_Product").GetValue()

    if messcope.Rows.Count > 0:
        for row in messcope.Rows:
            '''if row['PY_Quantity'] == "0":
                if row['Renewal_Quantity'] == "0" or row['Renewal_Quantity'] == "":
                    err_msg += "Quantity is invalid on row:" + str(row.RowIndex+1) + "<br>"'''
            mesquery = SqlHelper.GetFirst("select MES_Model,License_Type from SC_MES_Models where MES_Model='{}'".format(row["MES Models"]))
            if row['Description'] == "":
                err_msg_1 += "Blank Description:" + str(row.RowIndex+1) + "<br>"
            if mesquery is None:
                err_msg_2 += "MES Model is invalid on row:" + str(row.RowIndex+1) + "<br>"
            else:
                 if serviceproduct in serprod_lictype.keys():
                    if mesquery.License_Type != serprod_lictype[serviceproduct]:
                        err_msg_3 += "MES Model is not associated with Service Product on row:" + str(row.RowIndex+1) + "<br>"

    ErrorMsg = err_msg + err_msg_1 + err_msg_2 + err_msg_3
    Product.Attr("Error_Message").AssignValue(ErrorMsg)