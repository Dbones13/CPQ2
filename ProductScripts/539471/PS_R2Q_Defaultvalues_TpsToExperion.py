estCon = Product.GetContainerByName('TPS_EX_Station_Conversion_EST')

# Define default values in a dictionary
default_values = {
    'TPS_EX_Computer_Adapter_Kit': 'No',
    'TPS_EX_Hardware': 'Dell T5860XL',
    'TPS_EX_Future_Mounting_Furniture': 'Desktop',
    'TPS_EX_RPS_Type': 'None',
    'TPS_EX_Keyboard_Type': 'None',
    'TPS_EX_Quad_Display': 'Yes'
}

for row in estCon.Rows:
    for attr, default in default_values.items():
        current_value = row[attr]
        if current_value == '':
            if attr == 'TPS_EX_Hardware':
                row.SetColumnValue(attr, default)
            else:
                row.GetColumnByName(attr).SetAttributeValue(default)
                
convcon = Product.GetContainerByName('TPS_EX_Conversion_ACET_EAPP')
for row in convcon.Rows:
    if row['TPS_EX_Conversion_ACET_EAPP_Type'] == 'APP to ACE-T':
        if row['TPS_EX_Conversion_ACET_EAPP_Server_Hardware'] == '':
            row.SetColumnValue('TPS_EX_Conversion_ACET_EAPP_Server_Hardware','HP DL 320 G11')
    if row['TPS_EX_Conversion_ACET_EAPP_Type'] == 'APP to EAPP':
        if row['TPS_EX_Conversion_ACET_EAPP_Server_Hardware'] == '':
            row.SetColumnValue('TPS_EX_Conversion_ACET_EAPP_Server_Hardware','DELL T550 STD TPM')