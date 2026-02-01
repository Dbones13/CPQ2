Subscription_OM = Product.GetContainerByName('SC_WEP_Subscription_Price_OM')
Add_on_Fees_OM = Product.GetContainerByName('SC_WEP_Add_On_Fees_OM')
OM_entitlement = Product.GetContainerByName('SC_WEP_Entitlement_OM')
err_msg6 = ""
flag = False
sub_flag = False
add_flag = False

if Subscription_OM.Rows.Count:
    for row in Subscription_OM.Rows:
        if Product.Attr('SC_Product_Type').GetValue() == 'New':
            if row["User_Count"] != "" and row["User_Count"] != "0":
                sub_flag = True
                break
        elif Product.Attr('SC_Product_Type').GetValue() == 'Renewal':
            if row["CY_UserCount"] != "" and row["CY_UserCount"] != "0":
                sub_flag = True
                break
    if sub_flag == True:
        for row in OM_entitlement.Rows:
            if row.IsSelected == True:
                flag = True
                break
        if flag == False:
            err_msg6 = "Please select minimum one optional entitlement (O and M)" + "<br>"
if Add_on_Fees_OM.Rows.Count:
    for row in Add_on_Fees_OM.Rows:
        if Product.Attr('SC_Product_Type').GetValue() == 'New':
            if row["Subscription_Price_USD"] != "" and row["Subscription_Price_USD"] != "0":
                add_flag = True
                break
        '''elif Product.Attr('SC_Product_Type').GetValue() == 'Renewal':
            if row["CY_SubscriptionPrice_USD"] != "" and row["CY_SubscriptionPrice_USD"] != "0":
                add_flag = True
                break'''
    if add_flag == True:
        for row in OM_entitlement.Rows:
            if row.IsSelected == True:
                flag = True
                break
        if flag == False:
            err_msg6 = "Please select minimum one optional entitlement (O and M)" + "<br>"
ErrorMsg = err_msg6
Product.Attr("SC_WEP_OM_Error").AssignValue(ErrorMsg)