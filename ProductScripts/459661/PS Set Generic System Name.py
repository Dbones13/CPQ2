Generic_System_Cont = Product.GetContainerByName('PMC_Generic_System_Cont')
if Generic_System_Cont.Rows.Count > 0:
    for row in Generic_System_Cont.Rows:
        GS_Name = row.Product.Attr('Generic_System_Group_Name').GetValue()
        if str(row["Generic System Name"]) != GS_Name:
            row.Product.Attr('Generic_System_Group_Name').AssignValue(str(row["Generic System Name"]))
            row.ApplyProductChanges()
Generic_System_Cont.Calculate()