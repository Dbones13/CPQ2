SC_Product_Type = Product.Attr('SC_Product_Type').GetValue()
if SC_Product_Type == 'New':
    Model_cont = Product.GetContainerByName('SC_Experion_Models_Scope')
    err_msg = ""
    err_msg2 = ""
    err_msg3 = ""

    if Model_cont.Rows.Count:
        for row in Model_cont.Rows:
            if row['MSIDs'] == "":
                err_msg += "Please enter MSID" + "(row:"+ str(row.RowIndex+1) + ")"+ "<br>"
            if row['List_Price'] in ("","0"):
                err_msg2 += "Please enter List Price" + "(row:"+ str(row.RowIndex+1) + ")" + "<br>"
            if row['Cost_Price'] in ("","0"):
                err_msg3 += "Please enter Cost Price" + "(row:"+ str(row.RowIndex+1) + ")" + "<br>"
    ErrorMsg = err_msg + err_msg2 + err_msg3
    Product.Attr("Error_Message").AssignValue(ErrorMsg)
if SC_Product_Type == 'Renewal':
    Model_cont = Product.GetContainerByName('SC_Experion_Models_Scope')
    err_msg = ""
    err_msg2 = ""
    err_msg3 = ""

    if Model_cont.Rows.Count:
        for row in Model_cont.Rows:
            if row['MSIDs'] == "":
                err_msg += "Please enter MSID" + "(row:"+ str(row.RowIndex+1) + ")"+ "<br>"
            if Product.Attr('SC_ScopeRemoval').GetValue() in ['',"False"]:
                if row['HW_ListPrice'] in ("","0"):
                    err_msg2 += "Please enter List Price" + "(row:"+ str(row.RowIndex+1) + ")" + "<br>"
                if row['Cost_Price'] in ("","0"):
                    err_msg3 += "Please enter Cost Price" + "(row:"+ str(row.RowIndex+1) + ")" + "<br>"
    ErrorMsg = err_msg + err_msg2 + err_msg3
    Product.Attr("Error_Message").AssignValue(ErrorMsg)