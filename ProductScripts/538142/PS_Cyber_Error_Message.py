SC_Product_Type = Product.Attr('SC_Product_Type').GetValue()
if SC_Product_Type == 'New':
    Cyberscope = Product.GetContainerByName("SC_Cyber_Models_Scope_Cont")
    from CPQ_SF_SC_Modules import CL_SC_Modules
    class_contact_modules = CL_SC_Modules(Quote, TagParserQuote, None, Session)
    AccountName = Quote.GetCustomField('Account Name').Content
    AccountSite = Quote.GetCustomField('Account Site').Content
    MSIDTable=class_contact_modules.get_site_assets(AccountName, AccountSite)
    Valid_Asset=['']
    for Assets in MSIDTable.records:
        Valid_Asset.append(str(Assets.Name))
    err_msg_1 = ""
    err_msg_2 = ""
    err_msg_3 = ""
    err_msg_4 = ""
    err_msg_5 = ""
    err_msg_6 = ""


    if Cyberscope.Rows.Count > 0:
        for row in Cyberscope.Rows:
            if row['Asset No'] not in Valid_Asset:
                err_msg_1+= "Asset is not Valid:" + str(row.RowIndex+1) + "<br>"
            if row['Quantity'] == "0":
                err_msg_2+= "Quantity is invalid on row:" + str(row.RowIndex+1) + "<br>"
            if row['Description'] == str(''):
                err_msg_3 += "Description is blank:" + str(row.RowIndex+1) + "<br>"
            if row['Unit_List_Price'] == "0" or  row['Unit_List_Price'] == "":
                err_msg_4 += "List Price is not valid:" + str(row.RowIndex+1) + "<br>"
            if  row['Unit_Cost_Price'] == "0" or row['Unit_Cost_Price'] == "":
                err_msg_5 += "Cost Price is not valid:" + str(row.RowIndex+1) + "<br>"
            if row['Model'] == str(''):
                err_msg_6 += "Model is blank" + str(row.RowIndex+1) + "<br>"


    ErrorMsg = err_msg_1 + err_msg_2 + err_msg_3 + err_msg_4 + err_msg_5 + err_msg_6
    Product.Attr("SC_Cyber_Error_Message").AssignValue(ErrorMsg)
elif SC_Product_Type == 'Renewal':
    Cyberscope = Product.GetContainerByName("SC_Cyber_Models_Scope_Cont")
    from CPQ_SF_SC_Modules import CL_SC_Modules
    class_contact_modules = CL_SC_Modules(Quote, TagParserQuote, None, Session)
    AccountName = Quote.GetCustomField('Account Name').Content
    AccountSite = Quote.GetCustomField('Account Site').Content
    MSIDTable=class_contact_modules.get_site_assets(AccountName, AccountSite)
    Valid_Asset=['']
    for Assets in MSIDTable.records:
        Valid_Asset.append(str(Assets.Name))
    err_msg_1 = ""
    err_msg_2 = ""
    err_msg_3 = ""
    err_msg_4 = ""
    err_msg_5 = ""
    err_msg_6 = ""


    if Cyberscope.Rows.Count > 0:
        for row in Cyberscope.Rows:
            if row['PY_Quantity'] == '0':
                if row['Asset No'] not in Valid_Asset:
                    err_msg_1+= "Asset is not Valid:" + str(row.RowIndex+1) + "<br>"
                if row['Renewal_Quantity'] == "0" and row['PY_Quantity'] == "0" :
                    err_msg_2+= "Quantity is invalid on row:" + str(row.RowIndex+1) + "<br>"
                if row['Description'] == str(''):
                    err_msg_3 += "Description is blank:" + str(row.RowIndex+1) + "<br>"
                if (row['CY_ListPrice'] == "0" or  row['CY_ListPrice'] == ""):
                    err_msg_4 += "List Price is not valid:" + str(row.RowIndex+1) + "<br>"
                if (row['CY_CostPrice'] == "0" or  row['CY_CostPrice'] == ""):
                    err_msg_5 += "Cost Price is not valid:" + str(row.RowIndex+1) + "<br>"
                if row['Model_Number'] == str(''):
                    err_msg_6 += "Model is blank" + str(row.RowIndex+1) + "<br>"


    ErrorMsg = err_msg_1 + err_msg_2 + err_msg_3 + err_msg_4 + err_msg_5 + err_msg_6
    Product.Attr("SC_Cyber_Error_Message").AssignValue(ErrorMsg)