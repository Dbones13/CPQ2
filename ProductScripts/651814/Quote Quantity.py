fme_parts = ['AS-PHDRDIS','AS-PHDAS','AS-UNPHDES','AS-PHDRDIM','AS-PHDAM','AS-UNPHDEM','AS-UPSAS','AS-UPSBS','AS-UPSDS','AS-UNSGHTS']
no_of_configuration = Product.Attr("Number_Of_Configurations_EDM").GetValue()
def delete_items():
	for i in Quote.MainItems:
		if (i.PartNumber in fme_parts and i.QI_VCProducts.Value == ' ') or (i.PartNumber in fme_parts and i.QI_VCProducts.Value == no_of_configuration) :
			i.Delete()

def populatePartsInChild(product, container):
	hostquery = SqlHelper.GetFirst("Select HostName from CT_HOSTNAME where Domain in (select tenant_name from tenant_environments where is_current_environment = 1)")
	host = hostquery.HostName
	#lineItemContainer = product.GetContainerByName("MSID_Added_Parts_Common_Container")
	lineItemContainer = product.GetContainerByName("Trace_Software_Added_Parts_Common_Container")
	lineItemContainer.Clear()
	for row in container.Rows:
		#if row["fme"]:
		#	delete_items(row["PartNumber"])
		qty = row["Quantity"] if row["Quantity"] else 0
		adj = int(row["Adj Quantity"]) if row["Adj Quantity"] else 0
		final_qty = int(qty) + adj
		prod = SqlHelper.GetFirst("select PRODUCT_ID from products where PRODUCT_CATALOG_CODE='{}'".format(str(row["PartNumber"])))
		if prod and row["fme"]=="" and final_qty > 0 and row["PartNumber"] not in fme_parts:
			Trace.Write("-finall->"+str(prod.PRODUCT_ID)+"-->"+str(qty)+"-->"+str(adj))
			childRow = lineItemContainer.AddNewRow(False)
			childRow["PartNumber"] = row["PartNumber"]
			childRow["Quantity"] = str(final_qty)
			childRow["PLSG"] = row["PLSG"]
			childRow["PartDescription"] = row["PartDescription"]
			childRow["plsgDescription"] = row["plsgDescription"]
			childRow["Comments"] = row["Comments"]

	lineItemContainer.Calculate()
	for row in lineItemContainer.Rows:
		row.IsSelected = True
		row.Calculate()
		updateChildAttributes(row)
	lineItemContainer.Calculate()

def updateChildAttributes(row):
	if not row.Product:
		return
	for attr in filter(lambda a : a.DisplayType != "Container", row.Product.Attributes):
		if attr.Name == "ItemQuantity":
			attr.AssignValue(row["Quantity"])
	row.ApplyProductChanges()

def thirdPartyWriteIn():
	if Product.Attr('Trace_Software_Do_you_need_hardware').GetValue() == 'Yes':
		thirdPartHWIncluded = [i for i in Product.GetContainerByName('HCI_Thrid_Party_Hardware').Rows if str(i['Qty'])!='' and str(i['Qty'])!='0']
		writeInProductQuery = SqlHelper.GetFirst("SELECT Product, UnitofMeasure,PRODUCTLINE, PRODUCTLINEDESCRIPTION, PRODUCTLINESUBGROUPDESCRIPTION, PRODUCTLINESUBGROUP FROM WRITEINPRODUCTS (nolock) WHERE Category = 'Common' AND Product = 'Write-In Third Party Hardware & Software' ")
		WriteInCont = Product.GetContainerByName("HCI_PHD_WriteInCont")
		for HW in thirdPartHWIncluded:
			if str(HW['Third_Party_Hardware']) == 'Total Number of Servers':
				break
			newRow = WriteInCont.AddNewRow(True)
			newRow['ProductName'] = writeInProductQuery.Product
			newRow.Product.Attr('Selected_WriteIn').AssignValue(HW['Third_Party_Hardware'])
			newRow.Product.Attr('Unit of Measure').AssignValue(writeInProductQuery.UnitofMeasure)
			newRow['PartNumber'] = HW['Third_Party_Hardware']
			newRow['UOM'] = writeInProductQuery.UnitofMeasure
			newRow.Product.Attr('Cost').AssignValue(HW['Cost']) if HW['Cost'] else 0
			newRow.Product.Attr('Price').AssignValue(HW['Price']) if HW['Price'] else 0
			newRow.Product.Attr('Extended Description').AssignValue(str(HW['Extended_Description']))
			newRow.Product.Attr('ItemQuantity').AssignValue(str(HW['Qty']))
			newRow.Product.Attr('Product Line').AssignValue(writeInProductQuery.PRODUCTLINE)
			newRow.Product.Attr('Product Line Description').AssignValue(writeInProductQuery.PRODUCTLINEDESCRIPTION)
			newRow.Product.Attr('Product line sub group').AssignValue(writeInProductQuery.PRODUCTLINESUBGROUP)
			newRow.Product.Attr('PLSG description').AssignValue(writeInProductQuery.PRODUCTLINESUBGROUPDESCRIPTION)
			newRow['Cost'] = HW['Cost'] if HW['Cost'] else '0'
			newRow['Price'] = HW['Price'] if HW['Price'] else '0'
			newRow.ApplyProductChanges()
			newRow.Calculate()

def updateWriteInCont():
	BookingLOB = 'HCP'
	WriteInCont = Product.GetContainerByName("HCI_PHD_WriteInCont")
	PHDProduct = Product.Attr("HCI_PHD_Product").SelectedValue.Display
	BGPSupport = float(Product.Attr("HCI_PHD_BGP_SUPPORT").GetValue() or 0)
	WriteIn_ItemsDict = {}
	SupportWriteIns = list(range(1,int(BGPSupport)+1,1))
	writeInProductQuery = SqlHelper.GetList("SELECT Product, WRITEINS_DESC, UnitofMeasure,PRODUCTLINE, PRODUCTLINEDESCRIPTION, PRODUCTLINESUBGROUPDESCRIPTION, PRODUCTLINESUBGROUP FROM WRITEINPRODUCTS (nolock) JOIN CT_SW_HW_WRITEINS(NOLOCK) ON Product = WRITEINS  WHERE Category = '" + BookingLOB + "' AND PRODUCTNAME = '"+str(PHDProduct)+"' ")
	if int(BGPSupport)>0:
		for i in SupportWriteIns:
			for writeIn in writeInProductQuery:
				key =str(writeIn.WRITEINS_DESC).replace(' Yr', ' '+str(i)+'Yr')

				WriteIn_ItemsDict[str(writeIn.WRITEINS_DESC).replace(' Yr', ' '+str(i)+'Yr')] = [str(writeIn.Product),writeIn.UnitofMeasure,writeIn.PRODUCTLINE,writeIn.PRODUCTLINEDESCRIPTION,writeIn.PRODUCTLINESUBGROUP,writeIn.PRODUCTLINESUBGROUPDESCRIPTION]
				#for key,value in WriteIn_ItemsDict.items():
				newRow = WriteInCont.AddNewRow(True)
				Trace.Write('key--'+str(key))
				newRow['ProductName'] = writeIn.Product
				newRow.Product.Attr('Selected_WriteIn').AssignValue(key)
				newRow.Product.Attr('Unit of Measure').AssignValue(writeIn.UnitofMeasure)
				#newRow.Product.Attr('Product Line').AssignValue(str(value[4]).split('-')[0])
				#newRow.Product.Attr('Product Line Description').AssignValue(value[5])
				#newRow.Product.Attr('Product line sub group').AssignValue(value[4])
				#newRow.Product.Attr('PLSG description').AssignValue(value[5])
				newRow['PartNumber'] = key
				newRow['UOM'] = writeIn.UnitofMeasure
				newRow.Product.Attr('Extended Description').AssignValue(key)
				newRow.Product.Attr('ItemQuantity').AssignValue("1")
				newRow.ApplyProductChanges()
				newRow.Calculate()

WriteInCont = Product.GetContainerByName("HCI_PHD_WriteInCont")
WriteInCont.Rows.Clear()
updateWriteInCont()
thirdPartyWriteIn()
controw = Product.GetContainerByName('HCI_PHD_PartSummary_Cont')
populatePartsInChild(Product, controw)
delete_items()

FME_Valid_Parts = Product.GetContainerByName("FME_Valid_Parts")
FME_Valid_Parts.Clear()
for i in Product.GetContainerByName("HCI_PHD_PartSummary_Cont").Rows:
	if i["fme"]:
		vp = FME_Valid_Parts.AddNewRow(True)
		vp["Part Number"] = str(i["PartNumber"])
		vp["FME"] = str(i["fme"])
		vp["ExtendedDescription"] = "t"
		vp["Quantity"] = "1"
		vp["Ace Quote Reference Number"] = "1"
		vp["Ace Quote Description"] = "desc"
		vp["Unit List Price"] = "0"