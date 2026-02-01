fdm_cont = Product.GetContainerByName('FDM_System_Group_Cont')

if fdm_cont.Rows.Count > 0:
    for row in fdm_cont.Rows:
        flag = "false"
        if Product.Attr('Enterprise_flag_check').GetValue() == "True":
            attList = ["Enterprise_Groups_list","cluster1","cluster2","cluster3","cluster4","cluster5","cluster6","cluster7","cluster8","cluster9","cluster10"]
            for attribute in attList:
                if Product.Attr(attribute).GetValue() != row.Product.Attr(attribute).GetValue():
                    row.Product.Attr(attribute).AssignValue(Product.Attr(attribute).GetValue())
                    flag = "true"
        if flag == "true":
            row.ApplyProductChanges()
            row.Product.ApplyRules()