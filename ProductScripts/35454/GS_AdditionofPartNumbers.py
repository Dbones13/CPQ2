# ModelNumber=Product.PartNumber
# partnumbercont = Product.GetContainerByName("Non Pricing Parts")
# if partnumbercont:
# 	partnumbercont.Rows.Clear()

# def getproductsystemID(partnumber):
#     ProductData=SqlHelper.GetFirst("Select SYSTEM_ID,PRODUCT_NAME from products where PRODUCT_CATALOG_CODE  ='"+partnumber+"' and PRODUCT_ACTIVE = 'True'")
#     return ProductData

# def populateContainer(product , Quantity):
#     productsystemID=getproductsystemID(product.Child_Products)
#     partrow=partnumbercont.AddNewRow(productsystemID.SYSTEM_ID,False)
#     quantity = int(product.Quantity) * int(Quantity)
#     partrow["Part_Number"]=product.Child_Products
#     partrow["ItemQuantity"]=str(quantity)
#     partrow["Part_Name"]=productsystemID.PRODUCT_NAME
#     if partrow.Product.Attributes.GetByName("ItemQuantity") is not None:
#         partrow.Product.Attributes.GetByName("ItemQuantity").AssignValue(str(quantity))
#         Trace.Write("ItemQuantity "+str(partrow.Product.Attributes.GetByName("ItemQuantity").GetValue()))
#     if partrow.Product.Attributes.GetByName("PricingNeeded") is not None:
#         partrow.Product.Attributes.GetByName("PricingNeeded").AssignValue(product.Pricing)
#         Trace.Write("PricingNeeded "+str(partrow.Product.Attributes.GetByName("PricingNeeded").GetValue()))
#     partrow.Product.ApplyRules()
#     partrow.ApplyProductChanges()

# quantity = 1
# BaseQuery="Select Child_Products,DefaultPart,Quantity,Pricing,Attribute_Name,Attribute_Value_Code,Dependency_Attribute_Name,Dependency_Attribute_Value_Code,Dependency_Attribute_Name_2,Dependency_Attribute_Value_Code_2 from KE_PACKAGE_PART_QTY_MAPPING where Package_Model_Number  ='"+ModelNumber+"' and Pricing = 'No' and Child_Products <> ''"
# ChildProductData=SqlHelper.GetList(BaseQuery)
# for childProduct in ChildProductData:
#     if childProduct.DefaultPart == 'Y':
#         populateContainer(childProduct,quantity)
#     else:
#         for attr in Product.Attributes:
#             if attr.Name == childProduct.Attribute_Name and attr.GetValue() == childProduct.Attribute_Value_Code and childProduct.Dependency_Attribute_Name == '':
#                 populateContainer(childProduct,quantity)
#             elif attr.Name == childProduct.Attribute_Name and attr.GetValue() == childProduct.Attribute_Value_Code and childProduct.Dependency_Attribute_Name != '' and childProduct.Dependency_Attribute_Name_2 == '':
#                 if Product.Attr(childProduct.Dependency_Attribute_Name).GetValue() == childProduct.Dependency_Attribute_Value_Code:
#                     populateContainer(childProduct,quantity)
#             elif attr.Name == childProduct.Attribute_Name and attr.GetValue() == childProduct.Attribute_Value_Code and childProduct.Dependency_Attribute_Name != '' and childProduct.Dependency_Attribute_Name_2 != '':
#                 if Product.Attr(childProduct.Dependency_Attribute_Name).GetValue() == childProduct.Dependency_Attribute_Value_Code and Product.Attr(childProduct.Dependency_Attribute_Name_2).GetValue() == childProduct.Dependency_Attribute_Value_Code_2:
#                     populateContainer(childProduct,quantity)