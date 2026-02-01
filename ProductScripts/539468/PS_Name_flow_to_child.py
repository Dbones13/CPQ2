eserver_cont = Product.GetContainerByName('ES_Group')
if eserver_cont.Rows.Count > 0:
    for row in eserver_cont.Rows:
        flag = "false"
        eServer_name = row.Product.Attr('eServer_name').GetValue()
        mobile_name = row.Product.Attr('eServer_mobile_group').GetValue()

        if str(row['eServer_System_Group_Name']) != eServer_name:
            row.Product.Attr('eServer_name').AssignValue(str(row["eServer_System_Group_Name"]))
            flag = "true"

        if Product.Attr('Enterprise_flag_check').GetValue() == "True":
            attList = ["Enterprise_Groups_list","cluster1","cluster2","cluster3","cluster4","cluster5","cluster6","cluster7","cluster8","cluster9","cluster10"]
            for attribute in attList:
                if Product.Attr(attribute).GetValue() != row.Product.Attr(attribute).GetValue():
                    row.Product.Attr(attribute).AssignValue(Product.Attr(attribute).GetValue())
                    flag = "true"

        if str(row['Mobile_Server']) != mobile_name:
            row.Product.Attr('eServer_mobile_group').AssignValue(str(row["Mobile_Server"]))
            flag = "true"

        if flag == "true":
            row.ApplyProductChanges()
            row.Product.ApplyRules()