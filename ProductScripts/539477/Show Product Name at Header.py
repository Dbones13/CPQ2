PlantCruise_Group_Cont = Product.GetContainerByName('PlantCruise_Cont')
if PlantCruise_Group_Cont.Rows.Count > 0:
    for row in PlantCruise_Group_Cont.Rows:
        PlantCruise_Grp_Name = row.Product.Attr('PlantCruise_Group_Name').GetValue()
        if str(row["PlantCruise Group Name"]) != PlantCruise_Grp_Name:
            row.Product.Attr('PlantCruise_Group_Name').AssignValue(str(row["PlantCruise Group Name"]))
            row.ApplyProductChanges()
PlantCruise_Group_Cont.Calculate()