#CXCPQ-46820: GS_Populate_WS_Table script used to load FP VC products and corresponding Accessories/spare parts into the WS_Table Quote table. 
#This script called from custom action while generating the proposal document.
#Loads both BASE/Optional items into the WS_table and field ItemType to distinguish them
#Business asked to insert all non-VAS WriteIns into this table to display  in BOM tab.

def populateQuoteTableRow(table , dataDict , row = None):
	if not row:
		row = table.AddNewRow()
	for key , value in dataDict.items():
		row[key] = value


def populateWSTable(Quote):
	if Quote.GetCustomField('Booking LOB').Content == "PMC":
		wstable = Quote.QuoteTables["WS_Table"]
		wstable.Rows.Clear()
		#wstable.Save()
		wsrow={}
		
		#doc_row_index = 1
		#read quote items when item is added to quote and check if item is present in  table PMC_FP_Products
		for qitem in Quote.MainItems:
			lv_spareFlag=qitem["QI_SparePartsFlag"].Value
			if lv_spareFlag == "Spare Part":
				fpquery = SqlHelper.GetFirst("SELECT 1 as flag FROM PMC_FP_Products(nolock) WHERE PARTNUMBER = '{}'".format(qitem["QI_ParentVcModel"].Value))
			else: 
				fpquery = SqlHelper.GetFirst("SELECT 1 as flag FROM PMC_FP_Products(nolock) WHERE PARTNUMBER = '{}'".format(qitem.PartNumber))
				
			#if quote item is a FP product then populate quote table - WS table
			if fpquery:#If FP VC product or Spare
				wsrow["Item_Guid"]=qitem.QuoteItemGuid
				wsrow["ItemNumberSr"]=qitem.RolledUpQuoteItem #doc_row_index
				wsrow["PartNumber"]=qitem.PartNumber
				wsrow["ItemDescription"]=qitem.Description
				wsrow["Codes"]=qitem.QI_ExtendedDescription.Value
				#To Populate Plant
				plsg_data = SqlHelper.GetFirst("SELECT PLSG FROM HPS_PRODUCTS_MASTER(nolock) WHERE  PartNumber = '{}'".format(qitem.PartNumber))
				if plsg_data:
					coi_data = SqlHelper.GetFirst("SELECT Country_of_Origin FROM QT__Country_of_Origin(nolock) WHERE Product_Line_Sub_Group = '{}'".format(plsg_data.PLSG))
				if coi_data:
					fp_plant = SqlHelper.GetFirst("SELECT Plant FROM COUNTRY_OF_ORIGIN_PLSG_MAPPING WHERE VC_Model = '{}' and Country_of_Origin = '{}'".format(qitem.PartNumber, coi_data.Country_of_Origin))
					if fp_plant:
						wsrow["Plant"]=fp_plant.Plant
				
				wsrow["Product_Line"]=qitem["QI_ProductLineDesc"].Value
				wsrow["ItemType"] = "Base" if qitem.ItemType == 0 else "Optional"
				wsrow["Quantity"]=qitem.Quantity
				wsrow["ListPrice"]=qitem.ExtendedListPrice
				wsrow["UnitPrice"]=qitem.ListPrice
				
				if lv_spareFlag != "Spare Part":#FP VC Product
					wsrow["ModelCode"]=qitem["QI_FME"].Value
					if qitem.QI_Ace_Quote_Number.Value: # ACE Quote
						wsrow["Special_Quote_1"]=qitem.QI_Ace_Quote_Number.Value
					yspec_query = SqlHelper.GetList("SELECT Yspecial_Quote FROM QT__Yspecial_Selection(nolock)  WHERE CartItemGUID='{}'".format(qitem.QuoteItemGuid))
					
					if yspec_query is not None: # Yspecials
						ypsec =[]
						dic = {'1':"Special_Quote_1",'2':"Special_Quote_2",'3':"Special_Quote_3",'4':"Special_Quote_4"}
						wsrow["Special_Quote_1"] = ''
						wsrow["Special_Quote_2"] = ''
						wsrow["Special_Quote_3"] = ''
						wsrow["Special_Quote_4"] = ''
						wsrow["Special_Quote_n"] = ''
						for i in yspec_query:
							ypsec.append(i.Yspecial_Quote)
					Trace.Write('Yspec_List' +str(ypsec[:]))
					for i in range(1,len(ypsec)+1):
						if i < 5:#Upto 5 yspecials added to the table
							wsrow[dic[str(i)]]=ypsec[i-1]
						else:
							wsrow["Special_Quote_n"] += ypsec[i-1] + ','
				
					wsrow["FPSpare"]="No"
				else: #FP VC product spare part
					wsrow["ModelCode"]=''#qitem.PartNumber #CXCPQ-46820:Modelcode should be populated only for VC products. Other cases it should be blank
					wsrow["FPSpare"]="Yes"
				wsrow["Surcharge_Price"]=qitem["QI_Tariff_Amount"].Value
				wsrow["Total_Sell_Price"]=qitem["QI_Sell_Price_Inc_Tariff"].Value
				populateQuoteTableRow(wstable,wsrow)
				#doc_row_index += 1
			else:
				wrquery = SqlHelper.GetFirst("SELECT Description from WriteInProducts(nolock) where Product = '{}' and VASProduct!='Yes' ".format(qitem.PartNumber))
				if wrquery: #Non-VAS writeins
					wsrow["Item_Guid"]=qitem.QuoteItemGuid
					wsrow["ItemNumberSr"]=qitem.RolledUpQuoteItem 
					wsrow["PartNumber"]=qitem.PartNumber
					wsrow["ItemDescription"]=qitem.QI_ExtendedDescription.Value #qitem.Description #CXCPQ-46820:For WriteIns extended description should be populated in Item desc field.
					wsrow["Codes"]=qitem.QI_ExtendedDescription.Value
					wsrow["Product_Line"]=qitem["QI_ProductLineDesc"].Value
					wsrow["ItemType"] = "Base" if qitem.ItemType == 0 else "Optional"
					wsrow["Quantity"]=qitem.Quantity
					wsrow["ListPrice"]=qitem.ExtendedListPrice
					wsrow["UnitPrice"]=qitem.ListPrice
					wsrow["FPSpare"]="No"
					wsrow["ModelCode"]=''
					wsrow["Surcharge_Price"]=qitem["QI_Tariff_Amount"].Value
					wsrow["Total_Sell_Price"]=qitem["QI_Sell_Price_Inc_Tariff"].Value
					populateQuoteTableRow(wstable,wsrow)
			wstable.Save()