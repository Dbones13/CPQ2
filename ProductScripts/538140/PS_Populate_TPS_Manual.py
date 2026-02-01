SC_Product_Type = Product.Attr('SC_Product_Type').GetValue()
if SC_Product_Type == 'New':
    TPS_valid = Product.GetContainerByName('SC_TPS_Models_Scope')
    err_msg = ""
    err_msg2 = ""
    Product.Attr("Error_Message").AssignValue('')
    if TPS_valid.Rows.Count:
        for row in TPS_valid.Rows:
            if row['3rd_Party_Models'] == "" or row['Description'] == "":
                err_msg += "3rd Party Models and description is mandatory for all added models " + "(row:"+ str(row.RowIndex+1) + ")"+ "<br>"
            if row['Quantity'] in ("","0") or row['Unit_Price'] in ("","0") or row['UNIT_COST'] in ("","0"):
                Trace.Write('fdf')
                err_msg2 += "Quantity, Unit List Price and Unit Cost are mandatory for all added models " + "(row:"+ str(row.RowIndex+1) + ")" + "<br>"
    ErrorMsg = err_msg + err_msg2
    Product.Attr("Error_Message").AssignValue(ErrorMsg)
elif SC_Product_Type == 'Renewal':
    TPS_valid = Product.GetContainerByName('SC_TPS_Models_Scope')
    err_msg = ""
    err_msg2 = ""
    Product.Attr("Error_Message").AssignValue('')
    if TPS_valid.Rows.Count:
        for row in TPS_valid.Rows:
            if row['3rd_Party_Models'] == "" or row['Description'] == "":
                    err_msg += "3rd Party Models and description is mandatory for all added models " + "(row:"+ str(row.RowIndex+1) + ")"+ "<br>"
                    Trace.Write('checkingthere'+str(err_msg))
            '''if row['PY_Quantity'] == '0':
                if row['Renewal_Quantity'] in ("","0") or row['HW_UnitPrice'] in ("","0") or row['CY_Unit_Cost_Price'] in ("","0"):
                    Trace.Write('fdf')
                    err_msg2 += "Renewal Quantity, Unit List Price and Unit Cost are mandatory for all added models " + "(row:"+ str(row.RowIndex+1) + ")" + "<br>"'''
        ErrorMsg = err_msg + err_msg2
        Product.Attr("Error_Message").AssignValue(ErrorMsg)