ccr_cont = Product.GetContainerByName('Scada_CCR_Unit_Cont')
if ccr_cont.Rows.Count > 0:
    for row in ccr_cont.Rows:
        ccr_name = row.Product.Attr('CCR_group_name').GetValue()
        if str(row['Unit_Location']) != ccr_name:
            row.Product.Attr('CCR_group_name').AssignValue(str(row["Unit_Location"]))
            row.ApplyProductChanges()