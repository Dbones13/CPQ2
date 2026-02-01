PrdList = Product.Attr('MSID_PRDCHOICES').Values
rank_map_r2q = {'FDM Upgrade 1': 18, 'FDM Upgrade 2': 19, 'FDM Upgrade 3': 20}
hide_prd_r2q = {'Trace Software'} #'Virtualization System',
isR2Q = Quote.GetCustomField('isR2QRequest').Content
for i in PrdList:
    if i.Display in rank_map_r2q and isR2Q == 'Yes':
        i.Rank = rank_map_r2q[i.Display]
    if i.Display in hide_prd_r2q and isR2Q != 'Yes':
        i.Allowed = False
'''if isR2Q == 'Yes':
    from GS_R2Q_Product_Attribute_ContColms import MigrationProductsAttributesContainerColumns as gesLoc
    pole = Quote.GetCustomField('R2Q_Booking_Pole').Content #Quote.GetCustomField('Pole').Content
    Product.Attr('MSID_GES_Location').SelectValue(gesLoc.ges_location.get(pole))'''