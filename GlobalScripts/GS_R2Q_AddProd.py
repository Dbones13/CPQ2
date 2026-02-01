"""def extract_product_data(): 
    mainProductAttrsDict = {}
    containerDict = {}
    firstLevelProductAttrs = {}
    firstLevelContAttr = {}
    firstLevelContAttrlist = []
    secondlevelAttrs = {}
    secondLevelContAttr = {}
    secondLevelContAttrlist = [] 

    for attr in Product.Attributes:
        if Product.Attr(attr.Name).GetValue() == '':
            continue

        if attr.DisplayType != 'Container':
            mainProductAttrsDict[attr.Name] = Product.Attr(attr.Name).GetValue()

        else:
            contName = Product.GetContainerByName(attr.Name).Rows
            if contName.Count > 0:
                rowlist = []

                for colNames in contName:
                    columnValues = {}
                    for col in colNames.Columns:
                        columnValues[col.Name] = colNames[col.Name]
                    rowlist.append(columnValues)
                    containerDict[attr.Name] = rowlist
                    # First Level Attribute Details 
                    if colNames.Product:
                        for fl_attrs in colNames.Product.Attributes:
                            if colNames.Product.Attr(fl_attrs.Name).GetValue() == '':
                                continue

                            if fl_attrs.DisplayType != 'Container':
                                firstLevelProductAttrs[fl_attrs.Name] = colNames.Product.Attr(fl_attrs.Name).GetValue()

                            else:
                                fl_ContName = colNames.Product.GetContainerByName(fl_attrs.Name)
                                if fl_ContName.Rows.Count > 0:
                                    fl_containerName = fl_ContName.Rows.Item[0].Columns
                                    for fl_colNames in fl_ContName.Rows:
                                        firstLevelContAttr[fl_attrs.Name] = [colval.Name +'||'+fl_colNames[colval.Name] for colval in fl_containerName]
                                        firstLevelContAttrlist.append(firstLevelContAttr)
                                        # Second Level Attribute Details
                                        if fl_colNames.Product:
                                            for sl_attrs in fl_colNames.Product.Attributes:
                                                if fl_colNames.Product.Attr(sl_attrs.Name).GetValue() == '':
                                                    continue

                                                if sl_attrs.DisplayType != 'Container':
                                                    secondlevelAttrs[sl_attrs.Name] = fl_colNames.Product.Attr(sl_attrs.Name).GetValue()

                                                else:
                                                    sl_ContName = fl_colNames.Product.GetContainerByName(sl_attrs.Name)
                                                    if sl_ContName.Rows.Count > 0:
                                                        sl_containerName = sl_ContName.Rows.Item[0].Columns
                                                        for sl_colNames in sl_ContName.Rows:
                                                            secondLevelContAttr[sl_ContName.Name] = [colval.Name +'||'+sl_colNames[colval.Name] for colval in sl_containerName]
                                                            secondLevelContAttrlist.append(secondLevelContAttr)


    Session['MainProdData'] = mainProductAttrsDict
    Session['productData'] = containerDict
    Session['C300SystemAttrs'] = firstLevelProductAttrs
    Session['C300SystemCont'] = firstLevelContAttrlist
    Session['C300ControlGroupAttrs'] = secondlevelAttrs
    Session['C300ControlGroupCont'] = secondLevelContAttrlist


saveAction = Quote.GetCustomField("R2Q_Save").Content
isR2Qquote = True if Quote.GetCustomField("isR2QRequest").Content else False
if isR2Qquote and saveAction != 'Save':
    extract_product_data()"""
def extractProductContainer(attrName, product):
	containerList = []
	containerProductList = []
	containerRows = product.GetContainerByName(attrName).Rows
	if containerRows.Count > 0:
		for contanierRow in containerRows:
			contanierRowDict = {}
			for col in contanierRow.Columns:
				contanierRowDict[col.Name] = contanierRow[col.Name]
			containerList.append(contanierRowDict)
			if contanierRow.Product and attrName not in ['R2Q_Project_Questions_Cont']:
				selectAttributedict_level = {}
				extractProductAttributes(selectAttributedict_level, contanierRow.Product)
				containerProductList.append(selectAttributedict_level)
	return [containerList , containerProductList]


def extractProductAttributes(attributedict, product):
	for attr in product.Attributes:
		if attr.DisplayType == 'Container' and attr.Name not in attributedict:
			attributedict[attr.Name] = extractProductContainer(attr.Name, product)
		else:
			if product.Attr(attr.Name).GetValue() != '' and attr.Name not in attributedict:
				attributedict[attr.Name] = product.Attr(attr.Name).GetValue()


saveAction = Quote.GetCustomField("R2Q_Save").Content
isR2Qquote = True if Quote.GetCustomField("isR2QRequest").Content else False
if isR2Qquote and saveAction != 'Save':
	selectAttributedict = {}
	extractProductAttributes(selectAttributedict,Product)
	Session['SelectedAttsData'] = selectAttributedict
	Log.Info("SelectedAttsData====> " +str(Session['SelectedAttsData']))