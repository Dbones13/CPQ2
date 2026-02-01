def getDefaultAnswer():
	query = "select * from KE_QUE_DEFAULT (NOLOCK)"
	res = SqlHelper.GetList(query)
	d = dict()
	for r in res:
		d[r.Attribute_Name] = r.Default
	return d

def getMigQueMapping(product_key):
	query = "select * from MIGRATION_MODULE_QUE_MAP (NOLOCK) where product_key = '{}'".format(product_key)
	res = SqlHelper.GetList(query)

	resDict = dict()
	for r in res:
		rDict = resDict.get(r.Module_Key,dict())
		rDict[r.Module_Question] = r.Migration_Question
		resDict[r.Module_Key] = rDict
	return resDict

def migQueValue(name, que, attrValues, defaults):
	migrationQuestion = que.get(name)
	Trace.Write("migrationQuestion name:"+str(type(attrValues.get(migrationQuestion,''))))
	if migrationQuestion is not None:
		return attrValues.get(migrationQuestion,'').lower() if str(type(attrValues.get(migrationQuestion,''))) != "<type 'list'>" else ""
	defaultAns = defaults.get(name)
	if defaultAns is not None:
		return defaultAns.lower()

def npCanBeadded(row, attrValues, queDict, defaults):
	Trace.Write("row.Attribute_Value_Code.lower() == "+str(row.Attribute_Value_Code.lower()))
	if row.Attribute_Name and migQueValue(row.Attribute_Name, queDict, attrValues, defaults) != row.Attribute_Value_Code.lower():
		return False
	if row.Dependency_Attribute_Name and migQueValue(row.Dependency_Attribute_Name, queDict, attrValues, defaults) != row.Dependency_Attribute_Value_Code.lower():
		return False
	if row.Dependency_Attribute_Name_2 and migQueValue(row.Dependency_Attribute_Name_2, queDict, attrValues, defaults) != row.Dependency_Attribute_Value_Code_2.lower():
		return False
	return True

def getNonPricingPartNonDefl(row, attrValues, queDict, defaults):
	part = ''
	if npCanBeadded(row, attrValues, queDict, defaults):
		part = row.Child_Products
	return part

def getproductsystemID(partnumber):
	ProductData = SqlHelper.GetFirst("Select SYSTEM_ID, PRODUCT_NAME from products where PRODUCT_CATALOG_CODE  ='"+partnumber+"' and PRODUCT_ACTIVE = 'True'")
	return ProductData

def populateContainer(product , Quantity, parentModule, partnumbercont, ModelNumber):
	productsystemID=getproductsystemID(product.Child_Products)
	partrow = partnumbercont.Rows.GetByColumnName('Part_Number',product.Child_Products ) if partnumbercont else ''
	oldqty = 0
	rowKEPrd=''
	if partrow:
		rowKEPrd = partrow['KE_Part_Number'] if partrow['KE_Part_Number'] else ''
	if (not partrow or (rowKEPrd == '' or rowKEPrd != ModelNumber))and productsystemID :
		partrow=partnumbercont.AddNewRow(productsystemID.SYSTEM_ID,False)
	elif not productsystemID:
		return
	else:
		oldqty = int(partrow['ItemQuantity']) if partrow['ItemQuantity'] else 0
	quantity = int(product.Quantity) * int(Quantity) 
	partrow["Part_Number"]=product.Child_Products
	partrow["ItemQuantity"]=str(quantity + oldqty)
	partrow["Part_Name"]=productsystemID.PRODUCT_NAME
	partrow["Parent_Module"]=parentModule
	partrow["KE_Part_Number"]=ModelNumber
	if partrow.Product.Attributes.GetByName("ItemQuantity") is not None:
		partrow.Product.Attributes.GetByName("ItemQuantity").AssignValue(str(quantity))
		Trace.Write("ItemQuantity "+str(partrow.Product.Attributes.GetByName("ItemQuantity").GetValue()))
	if partrow.Product.Attributes.GetByName("PricingNeeded") is not None:
		partrow.Product.Attributes.GetByName("PricingNeeded").AssignValue(product.Pricing)
		Trace.Write("PricingNeeded "+str(partrow.Product.Attributes.GetByName("PricingNeeded").GetValue()))
	partrow.ApplyProductChanges()

def getNonPricingParts(part_list, parentModule, partnumbercont, attributeValueDict):
	keTbl = 'KE_Package_Part_Qty_Mapping'
	query = "select Distinct Package_Model_Number from "+keTbl+" (NOLOCK) WHERE Package_Model_Number in ('{0}')"
	query = query.format("','".join(part_list))
	res = SqlHelper.GetList(query)
	if res:
		for r in res:
			ModelNumber = r.Package_Model_Number
			quantity = 1
			BaseQuery="Select Child_Products,DefaultPart,Quantity,Pricing,Attribute_Name,Attribute_Value_Code,Dependency_Attribute_Name,Dependency_Attribute_Value_Code,Dependency_Attribute_Name_2,Dependency_Attribute_Value_Code_2 from "+keTbl+" (NOLOCK)  join products on PRODUCT_CATALOG_CODE = Child_Products join HPS_PRODUCTS_MASTER hps on Child_Products = hps.PartNumber where Package_Model_Number  ='"+ModelNumber+"' and Pricing = 'No' and Child_Products <> ''"
			ChildProductData=SqlHelper.GetList(BaseQuery)
			if ChildProductData:
				for childProduct in ChildProductData:
					if childProduct.DefaultPart == 'Y':
						populateContainer(childProduct,quantity, parentModule, partnumbercont, ModelNumber)
					else:
						defaults = getDefaultAnswer()
						queDict = getMigQueMapping(parentModule)
						np_cond = getNonPricingPartNonDefl(childProduct, attributeValueDict, queDict.get(ModelNumber,queDict.get("",dict())), defaults)
						if np_cond != '':
							populateContainer(childProduct,quantity, parentModule, partnumbercont, ModelNumber)

def getKENonPrcPart_standalone(ModelNumber):
	nonPricingParts = set()
	nonPricingQty = dict()
	query = "select * from KE_QUE_DEFAULT"
	res = SqlHelper.GetList(query)
	defaults = dict()
	for r in res:
		defaults[r.Attribute_Name] = r.Default
	
	BaseQuery="Select Child_Products,DefaultPart,Quantity,Pricing,Attribute_Name,Attribute_Value_Code,Dependency_Attribute_Name,Dependency_Attribute_Value_Code,Dependency_Attribute_Name_2,Dependency_Attribute_Value_Code_2 from KE_Package_Part_Qty_Mapping (NOLOCK) join products on PRODUCT_CATALOG_CODE = Child_Products join HPS_PRODUCTS_MASTER hps on Child_Products = hps.PartNumber where Package_Model_Number  ='"+ModelNumber+"' and Pricing = 'No' and Child_Products <> ''"
	ChildProductData=SqlHelper.GetList(BaseQuery)
	if ChildProductData:
		for childProduct in ChildProductData:
			if childProduct.DefaultPart == 'Y':
				nonPricingParts.add(childProduct.Child_Products)
				nonPricingQty[childProduct.Child_Products] = childProduct.Quantity
			else:
				if (defaults.get(childProduct.Attribute_Name) if defaults.get(childProduct.Attribute_Name) is not None else '') == childProduct.Attribute_Value_Code and childProduct.Dependency_Attribute_Name == '':
					nonPricingParts.add(childProduct.Child_Products)
					nonPricingQty[childProduct.Child_Products] = childProduct.Quantity
				elif (defaults.get(childProduct.Attribute_Name) if defaults.get(childProduct.Attribute_Name) is not None else '') == childProduct.Attribute_Value_Code and childProduct.Dependency_Attribute_Name != '' and childProduct.Dependency_Attribute_Name_2 == '':
					if (defaults.get(childProduct.Dependency_Attribute_Name) if defaults.get(childProduct.Dependency_Attribute_Name) is not None else '') == childProduct.Dependency_Attribute_Value_Code:
						nonPricingParts.add(childProduct.Child_Products)
						nonPricingQty[childProduct.Child_Products] = childProduct.Quantity
				elif (defaults.get(childProduct.Attribute_Name) if defaults.get(childProduct.Attribute_Name) is not None else '') == childProduct.Attribute_Value_Code and childProduct.Dependency_Attribute_Name != '' and childProduct.Dependency_Attribute_Name_2 != '':
					if (defaults.get(childProduct.Dependency_Attribute_Name) if defaults.get(childProduct.Dependency_Attribute_Name) is not None else '') == childProduct.Dependency_Attribute_Value_Code and (defaults.get(childProduct.Dependency_Attribute_Name_2) if defaults.get(childProduct.Dependency_Attribute_Name_2) is not None else '') == childProduct.Dependency_Attribute_Value_Code_2:
						nonPricingParts.add(childProduct.Child_Products)
						nonPricingQty[childProduct.Child_Products] = childProduct.Quantity
	return nonPricingParts, nonPricingQty