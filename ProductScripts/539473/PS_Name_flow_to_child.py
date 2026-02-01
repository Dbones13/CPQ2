esdc_cont = Product.GetContainerByName('ESDC_Group')

if esdc_cont.Rows.Count > 0:
    for row in esdc_cont.Rows:
        flag = "false"
        esdc_name = row.Product.Attr('Electrical_Substation_Data_Collector_Name').GetValue()
        if str(row['Electrical_Substation_Data_Collector_Group_Name']) != esdc_name:
            row.Product.Attr('Electrical_Substation_Data_Collector_Name').AssignValue(str(row["Electrical_Substation_Data_Collector_Group_Name"]))
            flag = "true"
        if Product.Attr('Enterprise_flag_check').GetValue() == "True":
            attList = ["Enterprise_Groups_list","cluster1","cluster2","cluster3","cluster4","cluster5","cluster6","cluster7","cluster8","cluster9","cluster10"]
            for attribute in attList:
                if Product.Attr(attribute).GetValue() != row.Product.Attr(attribute).GetValue():
                    row.Product.Attr(attribute).AssignValue(Product.Attr(attribute).GetValue())
                    flag = "true"
        if flag == "true":
            row.ApplyProductChanges()
            #row.Product.ApplyRules()