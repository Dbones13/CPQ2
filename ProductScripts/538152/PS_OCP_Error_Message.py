Courses_OCP = Product.GetContainerByName('SC_WEP_Courses_OCP')
OCP_entitlement = Product.GetContainerByName('SC_WEP_Entitlement_OCP')
err_msg6 = ""
flag = False
course_flag = False

if Courses_OCP.Rows.Count:
    for row in Courses_OCP.Rows:
        if Product.Attr('SC_Product_Type').GetValue() == "New":
            if row["Effort_Loading"] not in ("","0","0.00","0.0"):
                course_flag = True
                break
        elif Product.Attr('SC_Product_Type').GetValue() == "Renewal":
            if row["CY_EffortLoading"] not in ("","0","0.00","0.0"):
                course_flag = True
                break
    if course_flag == True:
        for row in OCP_entitlement.Rows:
            if row.IsSelected == True:
                flag = True
                break
        if flag == False:
            err_msg6 = "Please select minimum one optional entitlement (OCP)" + "<br>"
ErrorMsg = err_msg6
Product.Attr("SC_WEP_OCP_Error").AssignValue(ErrorMsg)