IFS_valid = Product.GetContainerByName('SC_WEP_Models_Scope_IFS')
IFS_entitlement = Product.GetContainerByName('SC_WEP_Entitlement_IFS')
flag = False
err_msg = ""
err_msg2 = ""
err_msg3 = ""
err_msg6 = ""
if IFS_valid.Rows.Count:
    for row in IFS_valid.Rows:
        ifsquery = SqlHelper.GetFirst("select WEP_Model from SC_WEP_Models where WEP_Model='{}' and TAB='IFS'".format(row["Model"]))
        if ifsquery is None:
            err_msg += "Invalid Model" + "(row:"+ str(row.RowIndex+1) + ")"+ "in IFS tab" + "<br>"
        if row['Description'] == "":
            err_msg2 += "Description is Blank" + "(row:"+ str(row.RowIndex+1) + ")"+ "in IFS tab" + "<br>"
        if Product.Attr('SC_Product_Type').GetValue() == "New":
            if row['Quantity'] in ("","0"):
                err_msg3 += "zero Quantity" + "(row:"+ str(row.RowIndex+1) + ")"+ "in IFS tab" + "<br>"
        '''elif Product.Attr('SC_Product_Type').GetValue() == "Renewal":
            if row['PY_Quantity'] == '0':
                if row['CY_Quantity'] in ("","0"):
                    err_msg3 += "zero Quantity" + "(row:"+ str(row.RowIndex+1) + ")"+ "in IFS tab" + "<br>"'''
    for row in IFS_entitlement.Rows:
        if row.IsSelected == True:
            flag = True
            break
    if flag == False:
        err_msg6 = "Please select minimum one optional entitlement (IFS)" + "<br>"
ErrorMsg = err_msg + err_msg2 + err_msg3 + err_msg6
Product.Attr("SC_WEP_IFS_Error").AssignValue(ErrorMsg)