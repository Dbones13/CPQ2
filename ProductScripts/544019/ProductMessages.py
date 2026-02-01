Product.Attr('Incomplete_Flag').AssignValue('')
def populateMessage(message):
	if Product.Messages.Contains(message):
		Product.Attr('Incomplete_Flag').AssignValue('1')
		return
	#Product.Messages.Add(message)
	Product.Attr('Incomplete_Flag').AssignValue('1')
	Product.Attr('Product_Message').AssignValue(message)

packageContainerName = "K&E Configuration"
packageContainer = Product.GetContainerByName(packageContainerName).Rows
if packageContainer.Count>0:
	product = packageContainer[0].Product
	ModelNumber=product.PartNumber
	Query="Select Attribute_Name,Attribute_Value_Code,Dependency_Attribute_Name,Dependency_Attribute_Value_Code,message,Dependency_Attribute_Name_2,Dependency_Attribute_Value_Code_2 from KE_PACKAGE_PART_QTY_MAPPING where Package_Model_Number  ='"+ModelNumber+"' and message <> ''"
	messages=SqlHelper.GetList(Query)

	for message in messages:
		attrName = message.Attribute_Name
		if Product.Attr(attrName).GetValue() == message.Attribute_Value_Code:
			if message.Dependency_Attribute_Name != '' and message.Dependency_Attribute_Name_2 == '':
				if Product.Attr(message.Dependency_Attribute_Name).GetValue() == message.Dependency_Attribute_Value_Code:
					populateMessage(message.message)
			elif message.Dependency_Attribute_Name != '' and message.Dependency_Attribute_Name_2 != '':
				if Product.Attr(message.Dependency_Attribute_Name).GetValue() == message.Dependency_Attribute_Value_Code and Product.Attr(message.Dependency_Attribute_Name_2).GetValue() == message.Dependency_Attribute_Value_Code_2:
					populateMessage(message.message)

			else:
				populateMessage(message.message)
part = Product.Attr("K&E Selected Model").GetValue()
if part!='':
	ProductData=SqlHelper.GetFirst("Select PRODUCT_NAME from products where PRODUCT_CATALOG_CODE  ='"+part+"' and PRODUCT_ACTIVE = 'True'")
	Trace.Write("KE_Part_Number="+str(part.strip().encode('unicode_escape')))
	Trace.Write("KE_Part_Name="+str(ProductData.PRODUCT_NAME.strip().encode('unicode_escape')))
	Product.Attr('KE_Part_Number').AssignValue(str(part.strip().encode('unicode_escape')))
	Product.Attr('KE_Part_Name').AssignValue(str(ProductData.PRODUCT_NAME.strip().encode('unicode_escape')))