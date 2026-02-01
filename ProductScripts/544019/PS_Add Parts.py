packageContainerName = "K&E Configuration"
pricingContainerName = "Pricing Parts"
nonPricingContainerName = "Non Pricing Parts"

packageContainer = Product.GetContainerByName(packageContainerName).Rows
partnumbercont = Product.GetContainerByName(pricingContainerName)
nonPricingCont = Product.GetContainerByName(nonPricingContainerName)

def populateContainer(product , Quantity):
	if(product.Pricing == 'Yes'):
		partrow=partnumbercont.AddNewRow(product.Child_Products,False)
	else:
		partrow=nonPricingCont.AddNewRow(product.Child_Products,False)
	partrow["Part_Number"]=product.Child_Products
	partrow["ItemQuantity"]=product.Quantity
	partrow["Part_Name"]=product.PRODUCT_NAME
	partrow["PLSG"] = product.PLSG
	partrow["PLSG Description"] = product.PLSGDesc
	if partrow.Product.Attributes.GetByName("ItemQuantity") is not None:
		partrow.Product.Attributes.GetByName("ItemQuantity").AssignValue(str(product.Quantity))
	if partrow.Product.Attributes.GetByName("PricingNeeded") is not None:
		partrow.Product.Attributes.GetByName("PricingNeeded").AssignValue(product.Pricing)
#    partrow.Product.ApplyRules() #CXCPQ-70447: Commented ApplyRules on 11/7/2023
	partrow.ApplyProductChanges()

partnumbercont.Rows.Clear()
nonPricingCont.Rows.Clear()
Product.AllowAttr(packageContainerName)
Product.AllowAttr(pricingContainerName)
Product.AllowAttr(nonPricingContainerName)
if packageContainer.Count>0:
	product = packageContainer[0].Product
	ModelNumber=product.PartNumber
	quantity = 1
	Query="Select TOP 500 PRODUCT_NAME , PLSG,PLSGDesc,Child_Products,DefaultPart,Quantity,Pricing,Attribute_Name,Attribute_Value_Code,Dependency_Attribute_Name,Dependency_Attribute_Value_Code,Dependency_Attribute_Name_2,Dependency_Attribute_Value_Code_2 from KE_PACKAGE_PART_QTY_MAPPING join products on PRODUCT_CATALOG_CODE = Child_Products join HPS_PRODUCTS_MASTER hps on Child_Products = hps.PartNumber where Package_Model_Number  ='"+ModelNumber+"' and IS_Model_name <> 'Y' and Child_Products <> '' ORDER BY Child_Products"
	ChildProductData=SqlHelper.GetList(Query)
	for childProduct in ChildProductData:
		if childProduct.DefaultPart == 'Y':
			populateContainer(childProduct,quantity)
		else:
			for attr in Product.Attributes:
				if attr.Name == childProduct.Attribute_Name and attr.GetValue() == childProduct.Attribute_Value_Code and childProduct.Dependency_Attribute_Name == '':
					populateContainer(childProduct,quantity)
				elif attr.Name == childProduct.Attribute_Name and attr.GetValue() == childProduct.Attribute_Value_Code and childProduct.Dependency_Attribute_Name != '' and childProduct.Dependency_Attribute_Name_2 == '':
					if Product.Attr(childProduct.Dependency_Attribute_Name).GetValue() == childProduct.Dependency_Attribute_Value_Code:
						populateContainer(childProduct,quantity)
				elif attr.Name == childProduct.Attribute_Name and attr.GetValue() == childProduct.Attribute_Value_Code and childProduct.Dependency_Attribute_Name != '' and childProduct.Dependency_Attribute_Name_2 != '':
					if Product.Attr(childProduct.Dependency_Attribute_Name).GetValue() == childProduct.Dependency_Attribute_Value_Code and Product.Attr(childProduct.Dependency_Attribute_Name_2).GetValue() == childProduct.Dependency_Attribute_Value_Code_2:
						populateContainer(childProduct,quantity)