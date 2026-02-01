if Product.Name != "Service Contract Products":
    ServiceProduct = Product.GetContainerByName('SC_GN_AT_Service_Product_Cont') 
    opt_ent_cont = Product.GetContainerByName('SC_GN_AT_Optional_Ent_Cont')
    flag = 1
    msg = ''
    #Trace.Write("ServiceProduct--->"+(ServiceProduct)+"  flag--->"+str(flag))
    if ServiceProduct != '':
        if opt_ent_cont.Rows.Count:
            for ent_row in opt_ent_cont.Rows:
                if ent_row['Service_Product'] in ServiceProduct and ent_row.IsSelected:
                    flag = 0
        else:
            flag = 0
    if flag:
        msg = "Selected service product must have atleast one entitlement." + "<br>"
        Trace.Write("Selected service product must have atleast one entitlement.")
    Product.Attr("SC_Cyber_Error_Message").AssignValue(msg)