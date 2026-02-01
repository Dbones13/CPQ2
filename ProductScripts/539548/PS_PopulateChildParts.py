if Session["Product Loading"] != True:
	isR2Qquote = True if Quote.GetCustomField("isR2QRequest").Content else False
	if not isR2Qquote:
		import math
		import GS_MigrationPartsUtil_New_MSID as mpu
		import GS_MigrationPartsUtil_2_New_MSID as mpu2
		import GS_MigrationPartsUtil_3_New_MSID as mpu3
		import GS_MigrationPartsUtil_5_New_MSID as mpu5
		import GS_MigrationPartsUtil_6_New_MSID as mpu6
		import GS_MigrationPartsUtil_8_New_MSID as mpu8

		globalQueDict = dict()
		def log_dict(dictionary):
			Log.Write(RestClient.SerializeToJson(dictionary))

		def getContainer(product, containerName):
			return product.GetContainerByName(containerName)

		def getAttributeValue(product,attribute_name):
			return product.Attr(attribute_name).GetValue()

		def getAttrValue(name, partNumber, prodName):
			queDict = globalQueDict.get(prodName)
			if not queDict:
				return

			que = queDict.get(partNumber)
			if que is None:
				return

			migrationQuestion = que.get(name)
			if migrationQuestion is not None:
				return attributeValueDict.get(migrationQuestion)

		def populatePartsInChild(productRow, container):
			product = productRow.Product
			virlist=[]
			productname=product.Name
			lineItemContainer = product.GetContainerByName("MSID_Added_Parts_Common_Container")
			if productname =='Virtualization System Migration':
				vircont = product.GetContainerByName("Virtualization_partsummary_cont")
				for i in vircont.Rows:
					virlist.append(i['partnumber'])
			#lineItemContainer.Clear()
			products_to_execute = []
			partQtyMap = {}
			rowsToDelete = []

			for row in container.Rows:
				qty = row["Final Quantity"] if row["Final Quantity"] else 0
				if float(qty):
					partQtyMap[row["PartNumber"] ]= qty

			for li_row in lineItemContainer.Rows:
				pn = li_row["PartNumber"]
				newQTY =  partQtyMap.get(pn,0)
				if newQTY:
					li_row["Quantity"] = str(newQTY)
					del partQtyMap[pn]
				else:
					if li_row["IsChildRow"] != "Yes":
						rowsToDelete.append(li_row.RowIndex)

			for part,qty in partQtyMap.items():
				if part in virlist:
					continue
				else:
					childRow = lineItemContainer.AddNewRow()
					childRow["PartNumber"] = part
					childRow["Quantity"] = str(qty)
					Log.Info("part number-> " +str(part)+ "quantity " +str(qty))
					Log.Info('childRow["PartNumber"] = ' + str(part) + ' childRow["Quantity"] = ' + str(childRow["Quantity"]))
					childRow.IsSelected = True
					if not childRow.Product:
						continue
					for attr in filter(lambda a : a.DisplayType != "Container", childRow.Product.Attributes):
						if attr.Name == "ItemQuantity":
							attr.AssignValue(childRow["Quantity"])
							continue
						value = getAttrValue(attr.Name, childRow.Product.PartNumber, productRow.Product.Name)
						if value:
							value = value[0] if type(value) == type([]) else value
							if attr.DisplayType == "FreeInputNoMatching":
								attr.AssignValue(value)
								continue
							attr.SelectValue(value)
					products_to_execute.append(childRow.Product)

			for rowIndex in rowsToDelete[::-1]:
				lineItemContainer.DeleteRow(rowIndex)
			lineItemContainer.Calculate()
			productRow.ApplyProductChanges()

		def populateChildPartForMSID(product):
			partContainers, contProductMap = mpu6.getChildContainerMap()
			productContainer = product.GetContainerByName("CONT_MSID_SUBPRD")
			for container in partContainers:
				if container == "MSID_Virtualization_Added_Parts_Common_Container":
					#productContainerVirt = product.GetContainerByName("MSID_Product_Container_Virtualization_hidden")
					contVirt = product.GetContainerByName("MSID_Virtualization_Added_Parts_Common_Container")
					productRowVirt = productContainer.Rows.GetByColumnName("Selected_Products", "Virtualization System Migration")
					if not productRowVirt:
						productRowVirt = productContainer.Rows.GetByColumnName("Selected_Products", "Virtualization System")
						if not productRowVirt:
							continue
					populatePartsInChild(productRowVirt, contVirt)
				else:
					cont = product.GetContainerByName(container)
					genSysContainers = {"MSID_GS1_Added_Parts_Common_Container": "Generic System 1",
										"MSID_GS2_Added_Parts_Common_Container": "Generic System 2",
										"MSID_GS3_Added_Parts_Common_Container": "Generic System 3",
										"MSID_GS4_Added_Parts_Common_Container": "Generic System 4",
										"MSID_GS5_Added_Parts_Common_Container": "Generic System 5"}
					if container in genSysContainers:
						productRow = productContainer.Rows.GetByColumnName("Product Name", genSysContainers[container])
					else:
						productRow = productContainer.Rows.GetByColumnName("Selected_Products", contProductMap[container])
					if not productRow:
						continue
					populatePartsInChild(productRow, cont)
					if contProductMap[container] == "FSC to SM":
						productContainerfsc = product.GetContainerByName("MSID_Product_Container_FSC_hidden")
						contfsc = product.GetContainerByName("MSID_FSC_to_SM_audit_Added_Parts_Common_Container")
						productRowfsc = productContainerfsc.Rows.GetByColumnName("Product Name", "FSC to SM Audit")
						populatePartsInChild(productRowfsc, contfsc)
					if contProductMap[container] == "FSC to SM IO Migration":
						productContainerfscio = product.GetContainerByName("MSID_Product_Container_FSC_IO_hidden")
						contfscio = product.GetContainerByName("MSID_FSCtoSM_IO_audit_Added_Parts_Common_Container")
						productRowfsc = productContainerfscio.Rows.GetByColumnName("Product Name", "FSC to SM IO Audit")
						#if productRowfsc == None:
							#productRowfsc ="FSC to SM IO Audit"
						populatePartsInChild(productRowfsc, contfscio)

		def getFloat(v):
			if v:
				return float(v)
			return 0

		msidContainer = getContainer(Product, "CONT_MSID_SUBPRD")
		for row in msidContainer.Rows:
			msidProduct = row.Product
			populateChildPartForMSID(Product) #Containe is not added 
			if row["Selected_Products"] == "Orion Console":
				mpu.populateWriteIns(msidProduct)
			if row["Selected_Products"] == "FSC to SM":
				mpu.populateWriteInsFSC(msidProduct)
			if row["Selected_Products"] == "TPS to Experion":
				mpu2.populateWriteInsTPS(msidProduct)
			if row["Selected_Products"] == "LM to ELMM ControlEdge PLC":
				mpu5.populateWriteInsLM(msidProduct)
			if row["Selected_Products"] == "CD Actuator I-F Upgrade":
				mpu2.populateWriteInsCDActuatorIFUpgrade(msidProduct)
			if row["Selected_Products"] == "CWS RAE Upgrade":
				if Product.Attr("Scope").GetValue() != ["LABOR"]:
					mpu3.populateWriteInsCWSRAEUpgrade(msidProduct,Quote)
			if row["Selected_Products"] == "TPA/PMD Migration":
				mpu8.populateWriteInsTPAPMD(msidProduct)
			if row["Selected_Products"] == "C200 Migration":
				mpu.populateWriteInsC200(msidProduct)
			if row["Selected_Products"] == "OPM":
				mpu2.populateWriteInsOPM(msidProduct)
			if row["Selected_Products"] == "CB-EC Upgrade to C300-UHIO":
				mpu8.populateCBECwritein(msidProduct)