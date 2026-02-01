Checkproduct = Product.ParseString('<*CTX(Product.RootProduct.PartNumber)*>')
if Quote.GetCustomField("isR2QRequest").Content == 'Yes' and Checkproduct == 'Migration':
    columns_to_set = [
        ('UOC_Ethernet_Switch_Type', 'Multi Mode')
    ]
    if Product.GetContainerByName('UOC_CG_Controller_Rack_Cont').Rows.Count:
        for column_name, attribute_value in columns_to_set:
            Product.GetContainerByName('UOC_CG_Controller_Rack_Cont').Rows[0].GetColumnByName(column_name).SetAttributeValue(attribute_value)
            if column_name == 'UOC_Ethernet_Switch_Type':
                Product.GetContainerByName('UOC_CG_Controller_Rack_Cont').Rows[0].GetColumnByName(column_name).Value = 'MultiMode'
        row = Product.GetContainerByName('UOC_CG_Controller_Rack_Cont').Rows[0]
        powersupply= row.Product.Attr('UOC_Power_Supply').GetValue()
        if powersupply =="Non Redundant":
            attribute = row.GetColumnByName("UOC_Power_Status_Mod_Redundant_Supply").ReferencingAttribute
            for value in attribute.Values:
                if value.Display in ('Yes'):
                    value.Allowed = False