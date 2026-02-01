dis_dict = dict()
cont = Product.GetContainerByName("Discount Bulk Upload Container")
scenario = Product.Attr('Discount Bulk Upload Type').SelectedValue.ValueCode
for row in cont.Rows:
	if row[scenario] != '':
		dis_dict[row[scenario]] = row['Discount in %']

if dis_dict:
	for Item in Quote.Items:
		if Item.QI_ProductLine.Value != '' and Item.QI_ProductLine.Value in dis_dict.Keys:
			Item.QI_Additional_Discount_Percent.Value = dis_dict[Item.QI_ProductLine.Value]
		elif Item.QI_PLSG.Value != '' and Item.QI_PLSG.Value in dis_dict.Keys:
			Item.QI_Additional_Discount_Percent.Value = dis_dict[Item.QI_PLSG.Value]
Quote.Calculate()