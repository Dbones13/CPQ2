TNA_valid = Product.GetContainerByName('SC_WEP_Models_Scope_TNA')
TNA_entitlement = Product.GetContainerByName('SC_WEP_Entitlement_TNA')
Sys_Sel_valid = Product.GetContainerByName('SC_WEP_System_Selection_TNA')
flag = False
sys_flag = False
err_msg = ""
err_msg2 = ""
err_msg3 = ""
err_msg6 = ""
if TNA_valid.Rows.Count:
    for row in TNA_valid.Rows:
        tnaquery = SqlHelper.GetFirst("select WEP_Model from SC_WEP_Models where WEP_Model='{}' and TAB='TNA'".format(row["Model"]))
        if tnaquery is None:
            err_msg += "Invalid Model" + "(row:"+ str(row.RowIndex+1) + ")"+ "in TNA tab" + "<br>"
        if row['Description'] == "":
            err_msg2 += "Description is Blank" + "(row:"+ str(row.RowIndex+1) + ")"+ "in TNA tab" + "<br>"
        if Product.Attr('SC_Product_Type').GetValue() == "New":
            if row['Quantity'] in ("","0"):
                err_msg3 += "zero Quantity" + "(row:"+ str(row.RowIndex+1) + ")"+ "in TNA tab" + "<br>"
        '''elif Product.Attr('SC_Product_Type').GetValue() == "Renewal":
            if row['PY_Quantity'] == '0':
                if row['CY_Quantity'] in ("","0"):
                    err_msg3 += "zero Quantity" + "(row:"+ str(row.RowIndex+1) + ")"+ "in TNA tab" + "<br>"'''
    for row in TNA_entitlement.Rows:
        if row.IsSelected == True:
            flag = True
            break
    if flag == False:
        err_msg6 = "Please select minimum one optional entitlement (TNA)" + "<br>"
if Sys_Sel_valid.Rows.Count:
    for row in Sys_Sel_valid.Rows:
        if Product.Attr('SC_Product_Type').GetValue() == "New":
            if row["User_Count"] != "" and row["User_Count"] != "0":
                sys_flag = True
                break
        elif Product.Attr('SC_Product_Type').GetValue() == "Renewal":
            if row["CY_UserCount"] != "" and row["CY_UserCount"] != "0":
                sys_flag = True
                break
    if sys_flag == True:
        for row in TNA_entitlement.Rows:
            if row.IsSelected == True:
                flag = True
                break
        if flag == False:
            err_msg6 = "Please select minimum one optional entitlement (TNA)" + "<br>"
ErrorMsg = err_msg + err_msg2 + err_msg3 + err_msg6
Product.Attr("SC_WEP_TNA_Error").AssignValue(ErrorMsg)