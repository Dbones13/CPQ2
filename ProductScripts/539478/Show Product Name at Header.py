HC900_Group_Cont = Product.GetContainerByName('HC900_Cont')
if HC900_Group_Cont.Rows.Count > 0:
    for row in HC900_Group_Cont.Rows:
        HC900_Grp_Name = row.Product.Attr('HC900_Group_Name').GetValue()
        if str(row["HC900 Group Name"]) != HC900_Grp_Name:
            row.Product.Attr('HC900_Group_Name').AssignValue(str(row["HC900 Group Name"]))
            row.ApplyProductChanges()
HC900_Group_Cont.Calculate()
isR2Qquote = True if Quote.GetCustomField("isR2QRequest").Content else False
if isR2Qquote:
	Product.DisallowAttrValues('HC900_Ges_Location_Labour', "GES Egypt")