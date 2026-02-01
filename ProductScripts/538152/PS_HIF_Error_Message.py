HIF_valid = Product.GetContainerByName('SC_WEP_Models_Scope_HIF')
HIF_entitlement = Product.GetContainerByName('SC_WEP_Entitlement_HIF')
flag = False
err_msg = ""
err_msg2 = ""
err_msg3 = ""
err_msg4 = ""
err_msg5 = ""
err_msg6 = ""
if HIF_valid.Rows.Count:
    for row in HIF_valid.Rows:
        if row['Model'] == "":
            err_msg += "Model is Blank" + "(row:"+ str(row.RowIndex+1) + ")"+ "in HIF tab" + "<br>"
        if row['Description'] == "":
            err_msg2 += "Description is Blank" + "(row:"+ str(row.RowIndex+1) + ")"+ "in HIF tab" + "<br>"
        if Product.Attr('SC_Product_Type').GetValue() == "New":
            if row['Quantity'] in ("","0"):
                err_msg3 += "zero Quantity" + "(row:"+ str(row.RowIndex+1) + ")"+ "in HIF tab" + "<br>"
            if row['Unit_Price'] in ("","0"):
                err_msg4 += "Zero Unit Price" + "(row:"+ str(row.RowIndex+1) + ")"+ "in HIF tab" + "<br>"
            if row['Unit_Cost'] in ("","0"):
                err_msg5 += "Zero Unit Cost" + "(row:"+ str(row.RowIndex+1) + ")"+ "in HIF tab" + "<br>"
        elif Product.Attr('SC_Product_Type').GetValue() == "Renewal":
            '''if row['PY_Quantity'] in ("","0"):
                if row['CY_Quantity'] in ("","0"):
                    err_msg3 += "zero Quantity" + "(row:"+ str(row.RowIndex+1) + ")"+ "in HIF tab" + "<br>"'''
            if Product.Attr('SC_ScopeRemoval').GetValue() != "Workforce Excellence Program":
                if row['CY_UnitPrice'] in ("","0"):
                    err_msg4 += "Zero Unit Price" + "(row:"+ str(row.RowIndex+1) + ")"+ "in HIF tab" + "<br>"
                if row['CY_UnitCost'] in ("","0"):
                    err_msg5 += "Zero Unit Cost" + "(row:"+ str(row.RowIndex+1) + ")"+ "in HIF tab" + "<br>"
    for row in HIF_entitlement.Rows:
        if row.IsSelected == True:
            flag = True
            break
    if flag == False:
        err_msg6 = "Please select minimum one optional entitlement (HIF)" + "<br>"
ErrorMsg = err_msg + err_msg2 + err_msg3 + err_msg4 + err_msg5 + err_msg6
Product.Attr("SC_WEP_HIF_Error").AssignValue(ErrorMsg)