if Quote.GetCustomField("isR2QRequest").Content == 'Yes':
    from GS_R2Q_Product_Attribute_ContColms import MigrationProductsAttributesContainerColumns as PRD
    Product.DisallowAttrValues('MSID_PRDCHOICES', *PRD.prdChoicesList)