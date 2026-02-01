c300_cont = Product.GetContainerByName('Series_C_Control_Groups_Cont')

if c300_cont.Rows.Count > 0:
    for row in c300_cont.Rows:
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