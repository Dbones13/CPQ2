import GS_PasC300CG_DocumnetIOGenerater,GS_PasC300RG_DocumnetIOGenerater
import GS_C300_PASDocument_data1, GS_PasC300RG_IO_Documnet_1
def populateC300proposal(Quote, C300Item, guid):
	QT_Table = Quote.QuoteTables["PAS_Document_Data"]
	cont_req=''
	field_bus1=''
	Eternt_intfce1=''
	Profi_bus1=''
	joined_UM_value=''
	control_req=[]
	field_bus=[]
	Profi_bus=[]
	Eternt_intfce=[]
	UM_value =[]
	C300CGIO=0
	C300PMIO=0
	C300RGIO=0
	LST_CG_GUID = None
	CGn = {
		"C300 System" : 0
	}

	#for level 2
	newRow = QT_Table.AddNewRow()
	sys_name = C300Item.ProductName
	newRow["System_Name"] = sys_name
	sys_name_guid = C300Item.QuoteItemGuid
	newRow["System_Item_GUID"] = sys_name_guid
	sys_grp = guid[C300Item.ParentItemGuid]
	newRow["System_Group"] = sys_grp
	sys_grp_guid = C300Item.ParentItemGuid
	newRow["System_Grp_GUID"] = sys_grp_guid
	newRow["RolledUpQuoteItem"] = C300Item.RolledUpQuoteItem
	contr = C300Item.SelectedAttributes.GetContainerByName('Series_C_Control_Groups_Cont')
	if contr:
		for row in contr.Rows:
			#Trace.Write('Series_c control group details')
			if row["controler_required"]:
				if row["controler_required"] == 'C300 CEE':
					control_req.append(str(row["controler_required"])+'_NonHive')
				else:
					control_req.append(str(row["controler_required"]))
			if row["SerC_CG_Foundation_Fieldbus_Interface_required"]:
				field_bus.append(str(row["SerC_CG_Foundation_Fieldbus_Interface_required"]))
			if row["SerC_GC_Profibus_Gateway_Interface"]:
				Profi_bus.append(str(row["SerC_GC_Profibus_Gateway_Interface"]))
			if row["SerC_CG_Ethernet_Interface"]:
				Eternt_intfce.append(str(row["SerC_CG_Ethernet_Interface"]))
			if row["Uni_marshling"]:
				UM_value.append(str(row["Uni_marshling"]))
			C300CGIO += int(row['total_family_CG_ios_doc']) if row['total_family_CG_ios_doc']!='' else 0
			C300PMIO += int(row['pmio_ios']) if row['pmio_ios']!='' else 0
			C300PMIO += int(row['ethernet_ios']) if row['ethernet_ios']!='' else 0
			C300PMIO += int(row['turbo_ios']) if row['turbo_ios']!='' else 0
			C300PMIO += int(row['Total_Sumof_FF_IOs']) if row['Total_Sumof_FF_IOs']!='' else 0
			C300PMIO += int(row['Total_Profibus_Red_NonRed_IOs']) if row['Total_Profibus_Red_NonRed_IOs']!='' else 0
			C300RGIO += int(row['Total RG Local Io Proposal']) if row['Total RG Local Io Proposal']!='' else 0
		expectedResult = str(C300CGIO)
		expectedResult1 = str(C300PMIO)
		expectedResult2 = str(C300RGIO)
		newRow['C300FMIO'] = expectedResult
		newRow['C300PMIO'] = expectedResult1
		newRow['C300RGIO'] = expectedResult2

	for Item in C300Item.Children:
		#for level 3
		if Item.ProductName == "Series-C Control Group":
			newRow = QT_Table.AddNewRow()
			newRow["CG_Name"] = Item.PartNumber
			newRow["CG_Item_GUID"] = Item.QuoteItemGuid
			newRow["System_Name"] = sys_name
			newRow["System_Item_GUID"] = sys_name_guid
			newRow["System_Group"] = sys_grp
			newRow["System_Grp_GUID"] = sys_grp_guid
			newRow["RolledUpQuoteItem"] = Item.RolledUpQuoteItem
			if LST_CG_GUID == Item.ParentItemGuid and newRow["CG_Name"] != '':
				CGn[Item.ProductName] += int(1)
				newRow["CG_No"] = str(CGn[Item.ProductName])
			elif newRow["CG_Name"] != '':
				CGn = {"C300 System" : 0}
				CGn[Item.ProductName] = 1
				newRow["CG_No"] = str(CGn[Item.ProductName])
				LST_CG_GUID = Item.ParentItemGuid
			
			LIO_CNT = 0
			ioSum=GS_C300_PASDocument_data1.populateC300Data1(Quote,Item)
			ioSum1=GS_PasC300CG_DocumnetIOGenerater.populateC300Data2(Quote,Item)
			ioSum.pop(0)
			ioSum1.pop(0) #calculation started from index 1
			expectedResult = [str(d) for d in ioSum]
			expectedResult1 = [str(a) for a in ioSum1]
			#Trace.Write("Expected Result CG: "+str(expectedResult))
			#Trace.Write("Expected Result SubCG: "+str(expectedResult1))
			newRow['CG'] = "|".join(expectedResult)
			newRow['SUBCG'] = "|".join(expectedResult1)
			newRow['Local_IO']= LIO_CNT

			#for level 4
			n = 0 
			RIO_CNT = 0
			for rg in Item.Children:
				if rg.ProductName == "Series-C Remote Group":
					n += 1
					rgIoSum=GS_PasC300RG_DocumnetIOGenerater.populateC300Data2(Quote,rg)
					rgIoSum1=GS_PasC300RG_IO_Documnet_1.populateC300RGData1(Quote,rg)
					rgIoSum.pop(0) #calculation started from index 1
					rgIoSum1.pop(0)
					expectedResult = [str(d) for d in rgIoSum]
					expectedResult1 = [str(a) for a in rgIoSum1]
					#Trace.Write("Expected Result RG: "+str(expectedResult))
					newRow['RG'+str(n)] = "|".join(expectedResult1)
					newRow['SubRG'+str(n)] = "|".join(expectedResult)
					newRow['Remote_IO'] = RIO_CNT
					newRow['Remote_Qty'] = str(n)
					if n == 1:
						newRow['RGNames'] = rg.PartNumber
					else:
						newRow['RGNames'] = newRow['RGNames'] + "|" + rg.PartNumber

	QT_Table.Save()

	cont_req="<br>".join(control_req)
	Quote.GetCustomField("C300_Attribute_value").Content= cont_req if cont_req else ""
	field_bus1="<br>".join(field_bus)
	Quote.GetCustomField("Field_bus_value").Content= field_bus1 if field_bus1 else ""
	Eternt_intfce1="<br>".join(Eternt_intfce)
	Quote.GetCustomField("Eternt_intfce_value").Content= Eternt_intfce1 if Eternt_intfce1 else ""
	Profi_bus1="<br>".join(Profi_bus)
	Quote.GetCustomField("Profi_bus_value").Content= Profi_bus1 if Profi_bus1 else ""
	joined_UM_value="<br>".join(UM_value)
	Quote.GetCustomField("universal_marshalling_value").Content= joined_UM_value if joined_UM_value else ""