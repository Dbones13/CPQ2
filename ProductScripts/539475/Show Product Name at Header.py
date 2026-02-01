Experion_Group_Cont = Product.GetContainerByName('Experion_HS_Cont')
if Experion_Group_Cont.Rows.Count > 0:
    for row in Experion_Group_Cont.Rows:
        Experion_Grp_Name = row.Product.Attr('Experion_Group_Name').GetValue()
        if str(row["Experion HS Group Name"]) != Experion_Grp_Name:
            row.Product.Attr('Experion_Group_Name').AssignValue(str(row["Experion HS Group Name"]))
            #row.ApplyProductChanges()
#Experion_Group_Cont.Calculate()