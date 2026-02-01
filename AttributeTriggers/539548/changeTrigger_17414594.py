if Quote.GetCustomField("isR2QRequest").Content == 'Yes':
    from GS_R2Q_Product_Attribute_ContColms import MigrationProductsAttributesContainerColumns as gesLoc
    
    product = Product.Attr('MSID_PRDCHOICES').GetValue()
    product_list = [item.strip() for item in product.split(",")]
    if "xPM to C300 Migration" in product_list:
        Product.Attr('MSID_Is_Site_Acceptance_Test_Required').SelectValue('None')
    elif "ELCN" in product_list:
        Product.Attr('MSID_Is_Site_Acceptance_Test_Required').SelectValue('No')
    
    if Product.GetContainerByName('CONT_MSID_SUBPRD').Rows.Count == 0 or Product.GetContainerByName('CONT_MSID_SUBPRD').Rows.Count == 1:
        pole = Quote.GetCustomField('R2Q_Booking_Pole').Content #Quote.GetCustomField('Pole').Content
        Product.Attr('MSID_GES_Location').SelectValue(gesLoc.ges_location.get(pole))

    Product.Attr('MSID_Active_Service_Contract').SelectValue('No') #Quote.GetCustomField("Entitlement").Content != 'No SESP'
    if product == 'LM to ELMM ControlEdge PLC' or Quote.GetCustomField("Entitlement").Content != '' or Quote.GetCustomField('Check_LSS_Rec_Count').Content == 'True':
        Product.Attr('MSID_Active_Service_Contract').SelectValue('Yes')