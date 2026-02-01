if Product.Attr('SC_Product_Type').GetValue() == "New":
    p1p2valid = Product.GetContainerByName("SC_P1P2_Parts_Details")
    err_msg = ""
    err_msg_2 = ""

    if p1p2valid.Rows.Count > 0:
        for row in p1p2valid.Rows:
            if row['Qty'] == "0" or row['Qty'] == "":
                if row['Replacement_Status'] == "Direct replacement":
                    pass
                else:
                    err_msg += "Qty is invalid on row:" + str(row.RowIndex+1) + "<br>"
            query = SqlHelper.GetFirst("select PartNumber from HPS_PRODUCTS_MASTER where PartNumber = '{}'".format(row['Part_Number']))
            if query is None:
                err_msg_2 += "PartNumber Model is invalid on row:" + str(row.RowIndex+1) + "<br>"

    ErrorMsg = err_msg + err_msg_2
    Product.Attr("Error_Message").AssignValue(ErrorMsg)

elif Product.Attr('SC_Product_Type').GetValue() == "Renewal":
    p1p2valid = Product.GetContainerByName("SC_P1P2_Parts_Details")
    err_msg = ""
    err_msg_2 = ""

    if p1p2valid.Rows.Count > 0:
        for row in p1p2valid.Rows:
            if row['PY_Quantity'] == "0" or row['PY_Quantity'] == "":
                if row['CY_Quantity'] == "0" or row['CY_Quantity'] == "":
                    if row['Replacement_Status'] == "Direct replacement" and row['Service_Product'] == "Parts Holding P2":
                        pass
                    else:
                        err_msg += "Qty is invalid on row:" + str(row.RowIndex+1) + "<br>"
            query = SqlHelper.GetFirst("select PartNumber from HPS_PRODUCTS_MASTER where PartNumber = '{}'".format(row['Part_Number']))
            if query is None:
                err_msg_2 += "PartNumber Model is invalid on row:" + str(row.RowIndex+1) + "<br>"

    ErrorMsg = err_msg + err_msg_2
    Product.Attr("Error_Message").AssignValue(ErrorMsg)