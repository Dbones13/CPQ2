# ================================================================================================
# Component: PLC System -> PLC Control Group -> PLC Remote Group ....
# Author: Ashok Kandi
# Purpose: This is used to create a inherit the attributes from parent product.
# Date: 02/10/2022
# ================================================================================================
PLC_Common_Questions_Cont = Product.GetContainerByName('PLC_Common_Questions_Cont')
if PLC_Common_Questions_Cont.Rows.Count == 1:
    PLC_Shielded_Terminal_Strip = PLC_Common_Questions_Cont.Rows[0].GetColumnByName('PLC_Shielded_Terminal_Strip').Value
    PLC_IO_Spare = PLC_Common_Questions_Cont.Rows[0].GetColumnByName('PLC_IO_Spare').Value
    PLC_IO_Slot_Spare = PLC_Common_Questions_Cont.Rows[0].GetColumnByName('PLC_IO_Slot_Spare').Value
    PLC_IO_Filler_Module = PLC_Common_Questions_Cont.Rows[0].GetColumnByName('PLC_IO_Filler_Module').Value

    Product.Attr('PLC_Shielded_Terminal_Strip').AssignValue(PLC_Shielded_Terminal_Strip)
    Product.Attr('PLC_IO_Spare').AssignValue(PLC_IO_Spare)
    Product.Attr('PLC_IO_Slot_Spare').AssignValue(PLC_IO_Slot_Spare)
    Product.Attr('PLC_IO_Filler_Module').AssignValue(PLC_IO_Filler_Module)

PLC_Software_Question_Cont = Product.GetContainerByName('PLC_Software_Question_Cont')
if PLC_Software_Question_Cont.Rows.Count == 1:
    PLC_Software_Release = PLC_Software_Question_Cont.Rows[0].GetColumnByName('PLC_Software_Release').Value
    PLC_Cabinet_Mounting = PLC_Software_Question_Cont.Rows[0].GetColumnByName('PLC_Cabinet_Required_Racks_Mounting').Value
    Product.Attr('PLC_Software_Release').AssignValue(PLC_Software_Release)
    Product.Attr('PLC_Cabinet_Required_Racks_Mounting').AssignValue(PLC_Cabinet_Mounting)

CE_SystemGroup_Cont = Product.GetContainerByName('PLC_ControlGroup_Cont')
if CE_SystemGroup_Cont.Rows.Count == 0:
    newRow = CE_SystemGroup_Cont.AddNewRow('Control_Group_cpq', False)
    newRow.ApplyProductChanges()

PLC_ControlGroup_Cont = Product.GetContainerByName('PLC_ControlGroup_Cont')
if PLC_ControlGroup_Cont.Rows.Count > 0:
    for row in PLC_ControlGroup_Cont.Rows:
        PLC_CG_Name = row.Product.Attr('PLC_CG_Name').GetValue()
        if str(row["Control Group Name"]) != PLC_CG_Name:
            row.Product.Attr('PLC_CG_Name').AssignValue(str(row["Control Group Name"]))
            row.ApplyProductChanges()
PLC_ControlGroup_Cont.Calculate()