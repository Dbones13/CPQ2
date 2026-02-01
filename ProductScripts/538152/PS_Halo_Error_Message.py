Halo_valid = Product.GetContainerByName('SC_WEP_Models_Scope_Halo')
Halo_entitlement = Product.GetContainerByName('SC_WEP_Entitlement_Halo')
flag = False
err_msg = ""
err_msg2 = ""
err_msg3 = ""
err_msg6 = ""
if Halo_valid.Rows.Count:
    for row in Halo_valid.Rows:
        haloquery = SqlHelper.GetFirst("select WEP_Model from SC_WEP_Models where WEP_Model='{}' and TAB='HALO'".format(row["Model"]))
        if haloquery is None:
            err_msg += "Invalid Model" + "(row:"+ str(row.RowIndex+1) + ")"+ "in Halo tab" + "<br>"
        if row['Description'] == "":
            err_msg2 += "Description is Blank" + "(row:"+ str(row.RowIndex+1) + ")"+ "in Halo tab" + "<br>"
        if Product.Attr('SC_Product_Type').GetValue() == "New":
            if row['Quantity'] in ("","0"):
                err_msg3 += "zero Quantity" + "(row:"+ str(row.RowIndex+1) + ")"+ "in Halo tab" + "<br>"
        '''elif Product.Attr('SC_Product_Type').GetValue() == "Renewal":
            if row['PY_Quantity'] == '0':
                if row['CY_Quantity'] in ("","0"):
                    err_msg3 += "zero Quantity" + "(row:"+ str(row.RowIndex+1) + ")"+ "in Halo tab" + "<br>"'''
    for row in Halo_entitlement.Rows:
        if row.IsSelected == True:
            flag = True
            break
    if flag == False:
        err_msg6 = "Please select minimum one optional entitlement (Halo)" + "<br>"
ErrorMsg = err_msg + err_msg2 + err_msg3 + err_msg6
Product.Attr("SC_WEP_Halo_Error").AssignValue(ErrorMsg)