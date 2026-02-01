count = 0
cont = Product.GetContainerByName('CE_System_Cont').Rows
for i in cont:
	Trace.Write(i['Product Name'])
	if i['Product Name'] == 'Experion Enterprise System':
		eeproduct = i.Product
		count+=eeproduct.GetContainerByName('Experion_Enterprise_Cont').Rows.Count
Product.Attr('Experion_EnterpriseGroup_Cont_count').AssignValue(str(count))