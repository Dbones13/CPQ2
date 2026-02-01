RTU_ControlGroup_Cont = Product.GetContainerByName('RTU_ControlGroup_Cont')
RTU_Software_Labor_Container = Product.GetContainerByName('RTU_Software_Labor_Container1')
if RTU_ControlGroup_Cont.Rows.Count == 0:
    newRow = RTU_ControlGroup_Cont.AddNewRow('RTU_Group_cpq', False)
    newRow.ApplyProductChanges()
if RTU_Software_Labor_Container.Rows.Count == 1:
    cabinet_mounting = RTU_Software_Labor_Container.Rows[0].GetColumnByName('RTU_Cabinet_Required_Racks_Mounting').Value

    Product.Attr('RTU_Cabinet_Required_Racks_Mounting').AssignValue(cabinet_mounting)

site_voltage = Product.Attr('CE_Site_Voltage').GetValue()
cabinet_mounting = Product.Attr('RTU_Cabinet_Required_Racks_Mounting').GetValue()
if RTU_ControlGroup_Cont.Rows.Count > 0:
    for row in RTU_ControlGroup_Cont.Rows:
        RTU_CG_Name = row.Product.Attr('RTU_CG_Name').GetValue()
        row["CE_Site_Voltage"] = site_voltage
        if str(row["Control Group Name"]) != RTU_CG_Name:
            row.Product.Attr('RTU_CG_Name').AssignValue(str(row["Control Group Name"]))
        row.Product.Attr("RTU_CG_Index").AssignValue(str(row.RowIndex))
        row.Product.Attr('CE_Site_Voltage').AssignValue(str(row["CE_Site_Voltage"]))
        row.ApplyProductChanges()
    RTU_ControlGroup_Cont.Calculate()