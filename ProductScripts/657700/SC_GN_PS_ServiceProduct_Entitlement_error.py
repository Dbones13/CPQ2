if Product.Name != "Service Contract Products":
    Entitlements = Product.GetContainerByName('SC_GN_AT_Product_Entitlement_Cont')
    ServiceProduct = Product.GetContainerByName('SC_GN_AT_Service_Product_Cont')
    opt_ent_cont = Product.GetContainerByName('SC_GN_AT_Optional_Ent_Cont')
    flag = 0
    msg = ''
    SP_list = []
    ent_list = []
    for SP_row in ServiceProduct.Rows:
        if SP_row.IsSelected == True:
            SP_list.append(str(SP_row['Service_Product']))
    for ent_row in Entitlements.Rows:
            ent_list.append(str(ent_row['Service_Product']))
    #Trace.Write("ServiceProduct--->"+(ServiceProduct)+"  flag--->"+str(flag))
    '''if SP_list != '':
        if opt_ent_cont.Rows.Count:
            for ent_row in opt_ent_cont.Rows:
                if ent_row['Service_Product'] in SP_list and ent_row.IsSelected:
                    flag = 0
        else:
            flag = 0'''
    for data in SP_list:
        if data not in ent_list:
            Trace.Write('data-->'+str(data))
            flag = 1
            break
    Trace.Write("ent_list--->"+str(ent_list)+"  SP_list--->"+str(SP_list))
    Trace.Write('msg-->'+str(msg))
    if flag:
        msg = "Selected service product must have atleast one entitlement." + "<br>"
        Trace.Write("Selected service product must have atleast one entitlement.")
    Trace.Write('msg-->'+str(msg))
    Product.Attr("SC_GN_AT_Error_Message").AssignValue(msg)