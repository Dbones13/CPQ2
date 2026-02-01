def cab_plc_uoc(Item, Quote, cab_count_no, cab_count_yes):
    container_mapping = {
    "UOC Control Group": ("UOC_CG_Cabinet_Cont", "UOC_CG_PartSummary_Cont"),
    "UOC Remote Group": ("UOC_RG_Cabinet_Cont", "UOC_RG_PartSummary_Cont"),
    "CE PLC Control Group": ("PLC_CG_Cabinet_Cont", "PLC_CG_PartSummary_LI_Cont"),
    "CE PLC Remote Group": ("PLC_RG_Cabinet_Cont", "PLC_RG_PartSummary_LI_Cont"),
}
    for item in Quote.Items:
        if item.ProductName in container_mapping:
            cabinet_cont_name, part_summary_cont_name = container_mapping[item.ProductName]
            cabinet_rows = item.SelectedAttributes.GetContainerByName(cabinet_cont_name)
            if cabinet_rows:
                attr_containers = cabinet_rows.Rows[0].Columns
                for column in attr_containers:
                    if column.Name in ('UOC_Integrated_Marshalling_Cabinet', 'PLC_Integrated_Marshalling_Cabinet'):
                        parts = item.SelectedAttributes.GetContainerByName(part_summary_cont_name)
                        if parts:
                            for part in parts.Rows:
                                if part['CE_Part_Number'] in ('CC-CBDS01', 'CC-CBDD01'):
                                    qty = int(part['CE_Part_Qty'])
                                    if column.Value == 'Yes':
                                        cab_count_yes += qty
                                    elif column.Value == 'No':
                                        cab_count_no += qty
    if Item.ProductName == "ControlEdge UOC System":
        Quote.GetCustomField("R2Q_UOC_CabinetCount").Content=str(cab_count_yes)+"|"+str(cab_count_no)
    elif Item.ProductName == "ControlEdge PLC System":
        Quote.GetCustomField("R2Q_PLC_CabinetCount").Content=str(cab_count_yes)+"|"+str(cab_count_no)