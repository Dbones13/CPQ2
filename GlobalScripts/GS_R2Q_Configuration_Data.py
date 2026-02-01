def getAvtiveProductAtt(productID, productName, tabs):
	AttQuery="""Select t.Id, t.Tabs, t.Name from (SELECT [Id] = [PRODUCT_ATTRIBUTES].[PA_ID]
						,[Name] = [ATTRIBUTE_DEFN].[STANDARD_ATTRIBUTE_NAME]
						,STUFF((
							select distinct ',' + [sys_ProductTabs].[TAB_NAME] from [sys_ProductTabs]
							inner join TAB_PRODUCTS on [TAB_PRODUCTS].TAB_CODE=[sys_ProductTabs].TAB_CODE 
							inner join PAT_SCHEMA on [TAB_PRODUCTS].TAB_PROD_ID = [PAT_SCHEMA].TAB_PROD_ID
							where [TAB_PRODUCTS].PRODUCT_ID = [PRODUCT_ATTRIBUTES].PRODUCT_ID and [PRODUCT_ATTRIBUTES].STANDARD_ATTRIBUTE_CODE = [PAT_SCHEMA].STANDARD_ATTRIBUTE_CODE
							FOR XML PATH('')), 1, 1, '') as Tabs FROM [PRODUCT_ATTRIBUTES] 
					INNER JOIN [ATTRIBUTE_DEFN] on [ATTRIBUTE_DEFN].[STANDARD_ATTRIBUTE_CODE] =  [PRODUCT_ATTRIBUTES].[STANDARD_ATTRIBUTE_CODE]
					INNER JOIN [ATT_DISPLAY_DEFN] on [PRODUCT_ATTRIBUTES].ATT_DISPLAY = [ATT_DISPLAY_DEFN].ATT_DISPLAY
					left outer join (SELECT distinct stdCode STANDARD_ATTRIBUTE_CODE FROM attrTrigger where product_id={pID}) HasTrigger on [PRODUCT_ATTRIBUTES].STANDARD_ATTRIBUTE_CODE = HasTrigger.STANDARD_ATTRIBUTE_CODE
				WHERE  [PRODUCT_ATTRIBUTES].PRODUCT_ID = {pID}) t where exists (select 1 from STRING_SPLIT(t.Tabs, ',') as value where value.value in {filterTabs})""".format(pID = productID, filterTabs = str(tuple(tabs)).replace(',)',')'))
	aData = SqlHelper.GetList(AttQuery)
	return { arow.Name : arow.Tabs for arow in aData}

def getCustomAttributes(productName, product):
	pData = SqlHelper.GetList("Select * from R2Q_COMPARISON_TABLE where ProductName = '{}' or ProductName = 'General'".format(productName))
	inAtt, exAtt, conAtt, prdTabs = [], [], {}, {"exName": [], "inName": []}
	for prow in pData:
		if prow.ObjectType.lower() == 'tab':
			if prow.IncludeName: prdTabs['inName'].append(prow.IncludeName.lower())
			elif prow.ExlcudeName: prdTabs['exName'].append(prow.ExlcudeName.lower())
		else:
			if prow.IsCondition != '1':
				if prow.IncludeName: inAtt.append(prow.IncludeName)
				elif prow.ExlcudeName: exAtt.append(prow.ExlcudeName)
			else:
				inAtt.append(prow.IncludeName) if product.ParseString(prow.ConditionFormula) == "1" else exAtt.append(prow.IncludeName)
			if prow.ObjectType.lower() == 'container' and prow.IncludeName: conAtt[prow.IncludeName] = prow
	return set(inAtt), set(exAtt), conAtt, prdTabs

def getProductTabs(product, inAtt, exAtt, all = False):
	return [tab.Name for tab in product.Tabs if (tab.Visible or all or tab.Name.lower() in inAtt) and tab.Name.lower() not in exAtt]

def readContainerData(product, att, conAtt):
	cont = product.GetContainerByName(str(att.Name))
	RowName = conAtt[str(att.Name)].RowName + ' ' if str(att.Name) in conAtt else ''
	RowIndexList = conAtt[str(att.Name)].IncludeRowIndex.split(',') if str(att.Name) in conAtt and conAtt[str(att.Name)].IncludeRowIndex else []
	exColumnNames = conAtt[str(att.Name)].ExlcudeColumnName.split(',') if str(att.Name) in conAtt and conAtt[str(att.Name)].ExlcudeColumnName else []
	defaultValues = eval(conAtt[str(att.Name)].DefaultValues) if str(att.Name) in conAtt and conAtt[str(att.Name)].DefaultValues else {}
	validCols = [col.Name for col in cont.Rows[0].Columns if product.ParseString('<*CTX( Container({0}).Column({1}).GetPermission() )*>'.format(att.Name,col.Name)) != "Hidden" and col.Name not in exColumnNames] if cont.Rows.Count>0 else []
	return {"Name": att.Name, "Label": product.ParseString(att.LabelFormula), "Value": ([getProductAttributes(row.Product) if att.IsLineItem and row.Product else {RowName + str(row.RowIndex+1) : [{"Name": col.Name, "Label": col.HeaderLabel, "Value": str(row.IsSelected) if col.DisplayType == "SelectorCheckBox" else col.Value  if col.Value not in [None, ''] else col.DisplayValue if col.DisplayValue else defaultValues.get(col.Name, '') if col.DisplayType == "DropDown" else str(int(float(row[col.Name]))) if col.DataType == "Number" and col.DecimalPlaces == 0 and row[col.Name] not in [None, ''] else row[col.Name]} for col in row.Columns if col.Name in validCols]} for row in cont.Rows if (str(row.RowIndex+1) in RowIndexList or not RowIndexList)])}

def isNumberLike(value):
	try:
		float(value)
		return True
	except:
		return False

def getProductAttributes(product):
	inAtt, exAtt, conAtt, prdTabs = getCustomAttributes(product.Name, product)
	pAtt = getAvtiveProductAtt(product.Id, product.Name, getProductTabs(product, prdTabs['inName'], prdTabs['exName']))
	prdData = [readContainerData(product, att, conAtt) if att.DisplayType == 'Container'else {"Name": att.Name, "Label": product.ParseString(att.LabelFormula), "Value": (str(int(float(att.GetValue()))) if isNumberLike(att.GetValue()) and float(att.GetValue()).is_integer() else att.GetValue())} for att in product.Attributes if ("{}".format(att.Name) in pAtt.Keys and att.Allowed == True and str(att.Access) != 'Hidden' and att.DisplayType != 'DisplayOnlyText' and "{}".format(att.Name) not in exAtt) or "{}".format(att.Name) in inAtt]
	return {"Product" : {"Name":product.Name, "Attributes": prdData}}

def saveProductAttributes(Quote, product):
	Quote.SetGlobal('r2qcompare', JsonHelper.Serialize(getProductAttributes(product)))


def generateTableRows(Attributes, prdName, cprdName, AttData):
	cAttData = []
	for item in Attributes:
		if isinstance(item["Value"], list):
			for vitem in item["Value"]:
				if "Product" in vitem:
					generateTableRows(vitem["Product"]["Attributes"],cprdName, vitem["Product"]["Name"], cAttData)
				else:
					for citem in vitem:
						AttData.append({"pName" : prdName, "cName" : cprdName, "Name" : item["Label"] if item["Label"] and item["Label"] not in ["<!-- -->"] else item["Name"], "Label" : "Row Number", "Value" : citem })
						cnt = len(AttData)
						generateTableRows(vitem[citem], prdName, cprdName, AttData)
						if cnt == len(AttData):
							AttData.pop()
		else:
			AttData.append({"pName" : prdName, "cName" : cprdName, "Name" : item["Name"], "Label" : item["Label"], "Value" : item["Value"] }) if item["Value"] and item["Value"] not in ('0', '0.0', '0.00') else ''
	AttData.extend(cAttData)
	return AttData

def getHTMLDataTable(Quote):
	html = """<table class='fiori3-table fiori3-products-list-table table table-hover' id='r2Q_compatability_table'>
		<thead>
		<tr>
			<th style="Width:80%" class='d-none'>Parent Product</th>
			<th style="Width:100%" >Product Name</th>
			<th style="Width:100%" >Attribute Name</th>
			<th style="Width:100%" >Attribute Label</th>
			<th style="Width:100%" >Attribute Value</th>
		</tr>
		</thead>
		<tbody>"""
	pdData = Quote.GetGlobal('r2qcompare')
	if pdData:
		pdData = eval(pdData.replace('null', '""'))
		tData=generateTableRows(pdData["Product"]["Attributes"], "Quote", pdData["Product"]["Name"], [])
		for trow in tData:
			html += "      <tr>
"
			html += "        <td class='d-none'>{}</td>
".format(trow["pName"])
			html += "        <td>{}</td>
".format(trow["cName"])
			html += "        <td>{}</td>
".format(trow["Name"])
			html += "        <td>{}</td>
".format(trow["Label"])
			html += '        <td style="text-align: left;">{}</td>
'.format(str(trow["Value"].encode("ascii", "replace").replace('?','')))
			html += "      </tr>
"
	html += """    </tbody>
	</table>"""
	return html