gesloc = Product.Attr('MSID_GES_Location').GetValue()
if gesloc:
    Product.GetContainerByName('UOC_Labor_Details').Rows[0].SetColumnValue('UOC_Ges_Location_Labour',str(gesloc))