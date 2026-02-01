# ================================================================================================
# Component: UOC System
# Author: Ashok Kandi
# Purpose: This is used to create add row in a control group container.
# Date: 02/10/2022
# ================================================================================================
CE_SystemGroup_Cont = Product.GetContainerByName('UOC_ControlGroup_Cont')
if CE_SystemGroup_Cont.Rows.Count == 0:
    newRow = CE_SystemGroup_Cont.AddNewRow('UOC_Control_Group_cpq', False)
    newRow.ApplyProductChanges()

UOC_Common_Questions_Cont = Product.GetContainerByName('UOC_Common_Questions_Cont')
if UOC_Common_Questions_Cont.Rows.Count == 1:
    UOC_Shielded_Terminal_Strip = UOC_Common_Questions_Cont.Rows[0].GetColumnByName('UOC_Shielded_Terminal_Strip').Value
    UOC_IO_Spare = UOC_Common_Questions_Cont.Rows[0].GetColumnByName('UOC_IO_Spare').Value
    UOC_IO_Slot_Spare = UOC_Common_Questions_Cont.Rows[0].GetColumnByName('UOC_IO_Slot_Spare').Value
    UOC_IO_Filler_Module = UOC_Common_Questions_Cont.Rows[0].GetColumnByName('UOC_IO_Filler_Module').Value
    Cabinet_Required_Racks_Mounting = UOC_Common_Questions_Cont.Rows[0].GetColumnByName('UOC_Cabinet_Required_Racks_Mounting').Value
    UOC_Exp_PKS_software_release = UOC_Common_Questions_Cont.Rows[0].GetColumnByName('UOC_Exp_PKS_software_release').Value

    Product.Attr('UOC_Shielded_Terminal_Strip').AssignValue(UOC_Shielded_Terminal_Strip)
    Product.Attr('UOC_IO_Spare').AssignValue(UOC_IO_Spare)
    Product.Attr('UOC_IO_Slot_Spare').AssignValue(UOC_IO_Slot_Spare)
    Product.Attr('UOC_IO_Filler_Module').AssignValue(UOC_IO_Filler_Module)
    Product.Attr('Cabinet_Required_Racks_Mounting').AssignValue(Cabinet_Required_Racks_Mounting)
    Product.Attr('Controledge_Exp_PKS_software_release').AssignValue(UOC_Exp_PKS_software_release)

CE_SystemGroup_Cont = Product.GetContainerByName('UOC_ControlGroup_Cont')
if CE_SystemGroup_Cont.Rows.Count == 0:
    newRow = CE_SystemGroup_Cont.AddNewRow('UOC_Control_Group_cpq', False)
    newRow.ApplyProductChanges()

PLC_ControlGroup_Cont = Product.GetContainerByName('UOC_ControlGroup_Cont')
if PLC_ControlGroup_Cont.Rows.Count > 0:
    for row in PLC_ControlGroup_Cont.Rows:
        PLC_CG_Name = row.Product.Attr('UOC_CG_Name').GetValue()
        if str(row["Control Group Name"]) != PLC_CG_Name:
            row.Product.Attr('UOC_CG_Name').AssignValue(str(row["Control Group Name"]))
            row.ApplyProductChanges()
PLC_ControlGroup_Cont.Calculate()