cont = Product.GetContainerByName("SM_RG_ATEX Compliance_and_Enclosure_Type_Cont")
if cont.Rows.Count > 0:
    enclosure = Product.GetContainerByName("SM_RG_ATEX Compliance_and_Enclosure_Type_Cont").Rows[0].GetColumnByName("Enclosure_Type").DisplayValue
    if enclosure == "Universal Safety Cab-1.3M":
        identifier_modifier = Product.GetContainerByName("SM_RG_Universal_Safety_Cabinet_1.3M_Cont").Rows[0].GetColumnByName("Specify_Identifier_Modifier_for_SM_SC_Universal_Safety_Cabinet").DisplayValue
        if identifier_modifier == "Yes":
            ui_string = Product.GetContainerByName("SM_RG_Universal_Safety_Cabinet_1.3M_Cont").Rows[0].GetColumnByName("UI_Identifier_Modifier_for_SM_SC_Universal_Safety_Cabinet").Value
            if len(ui_string) >= 20:
                modifier_new = ui_string[0:5]+ui_string[7:19]+ui_string[5:7]+ui_string[19:]
                Product.GetContainerByName("SM_RG_Universal_Safety_Cabinet_1.3M_Cont").Rows[0].SetColumnValue('Identifier_Modifier_for_SM_SC_Universal_Safety_Cabinet',modifier_new)