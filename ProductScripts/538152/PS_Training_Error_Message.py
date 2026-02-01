Training_valid = Product.GetContainerByName('SC_WEP_Models_Scope_Training')
Training_entitlement = Product.GetContainerByName('SC_WEP_Entitlement_Training')
TC_valid = Product.GetContainerByName('SC_WEP_Configurable_Models_Training')
flag = False
err_msg = ""
err_msg2 = ""
err_msg3 = ""
err_msg6 = ""
c_err_msg1 = ""
c_err_msg2 = ""
c_err_msg3 = ""
c_err_msg4 = ""
c_err_msg5 = ""
if Training_valid.Rows.Count:
    for row in Training_valid.Rows:
        trainingquery = SqlHelper.GetFirst("select WEP_Model from SC_WEP_Models where WEP_Model='{}' and TAB='Training'".format(row["Model"]))
        if trainingquery is None:
            err_msg += "Invalid Model" + "(row:"+ str(row.RowIndex+1) + ")"+ "in Training tab" + "<br>"
        if row['Description'] == "":
            err_msg2 += "Description is Blank" + "(row:"+ str(row.RowIndex+1) + ")"+ "in Training tab" + "<br>"
        if Product.Attr('SC_Product_Type').GetValue() == "New":
            if row['Quantity'] in ("","0"):
                err_msg3 += "zero Quantity" + "(row:"+ str(row.RowIndex+1) + ")"+ "in Training tab" + "<br>"
        '''elif Product.Attr('SC_Product_Type').GetValue() == "Renewal":
            if row['PY_Quantity'] in ("","0"):
                if row['CY_Quantity'] in ("","0"):
                    err_msg3 += "zero Quantity" + "(row:"+ str(row.RowIndex+1) + ")"+ "in Training tab" + "<br>"'''
    for row in Training_entitlement.Rows:
        if row.IsSelected == True:
            flag = True
            break
    if flag == False:
        err_msg6 = "Please select minimum one optional entitlement (Training)" + "<br>"
if TC_valid.Rows.Count:
    for row in TC_valid.Rows:
        if row['Model'] == "":
            c_err_msg1 += "Model is Blank" + "(row:"+ str(row.RowIndex+1) + ")"+ "in Training tab in configurable container" + "<br>"
        if row['Description'] == "":
            c_err_msg2 += "Description is Blank" + "(row:"+ str(row.RowIndex+1) + ")"+ "in Training tab in configurable container" + "<br>"
        if Product.Attr('SC_Product_Type').GetValue() == "New":
            if row['Quantity'] in ("","0"):
                c_err_msg3 += "zero Quantity" + "(row:"+ str(row.RowIndex+1) + ")"+ "in Training tab in configurable container" + "<br>"
            if row['Unit_Price'] in ("","0"):
                c_err_msg4 += "Zero Unit Price" + "(row:"+ str(row.RowIndex+1) + ")"+ "in Training tab in configurable container" + "<br>"
            if row['Unit_Cost'] in ("","0"):
                c_err_msg5 += "Zero Unit Cost" + "(row:"+ str(row.RowIndex+1) + ")"+ "in Training tab in configurable container" + "<br>"
        if Product.Attr('SC_Product_Type').GetValue() == "Renewal":
            if Product.Attr('SC_ScopeRemoval_Training').GetValue() != "Training":
                if row['CY_UnitPrice'] in ("","0"):
                    c_err_msg4 += "Zero Unit Price" + "(row:"+ str(row.RowIndex+1) + ")"+ "in Training tab in configurable container" + "<br>"
                if row['CY_UnitCost'] in ("","0"):
                    c_err_msg5 += "Zero Unit Cost" + "(row:"+ str(row.RowIndex+1) + ")"+ "in Training tab in configurable container" + "<br>"
    for row in Training_entitlement.Rows:
        if row.IsSelected == True:
            flag = True
            break
    if flag == False:
        err_msg6 = "Please select minimum one optional entitlement (Training)" + "<br>"
ErrorMsg = err_msg + err_msg2 + err_msg3 + err_msg6 + c_err_msg1 + c_err_msg2 + c_err_msg3 + c_err_msg4 + c_err_msg5
Product.Attr("SC_WEP_Training_Error").AssignValue(ErrorMsg)