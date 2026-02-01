ss_cont = Product.GetContainerByName('SS_Group')
if ss_cont.Rows.Count > 0:
    for row in ss_cont.Rows:
        Simulation_System1 = row.Product.Attr('Simulation_System_name').GetValue()
        if str(row['Simulation_System_Group_Name']) != Simulation_System1:
            row.Product.Attr('Simulation_System_name').AssignValue(str(row["Simulation_System_Group_Name"]))
            row.ApplyProductChanges()