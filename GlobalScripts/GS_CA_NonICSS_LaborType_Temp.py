#CA_NonICSS_LaborType_Temp Start
def getFloat_prjt(Var):
    if Var:
        return float(Var)
    return 0
def addValues(totalDict , partNumber,key, value):
    partDict = totalDict.get(partNumber,dict())
    partDict[key] = getFloat_prjt(partDict.get(key , 0)) + getFloat_prjt(value)
    totalDict[partNumber] = partDict
def populateLaborTypeTable2(labotTypeTable,laborTypeTableData):
    addRow = labotTypeTable.AddNewRow()
    addRow["Labor_Type"] = "Total"
    addRow["IsHeader"] = "Yes"
    for laborType in laborTypes:
        addRow = labotTypeTable.AddNewRow()
        addRow["Labor_Type"] = laborType
        addRow["IsHeader"] = "Yes"
        typeData = laborTypeTableData.get(laborType,'')
        if typeData:
            addRow["Hours"] = typeData.get("Hours",0)
            addRow["Total_Cost"] = typeData.get("Total_Cost",0)
            addRow["Total_Sell_Price"] = typeData.get("Total_Sell_Price",0)
def getExecutionCountry(Quote):
    marketCode = Quote.SelectedMarket.MarketCode
    salesOrg = marketCode.partition('_')[0]
    currency = marketCode.partition('_')[2]
    query = SqlHelper.GetFirst("select Execution_County from NEW_EXECUTION_COUNTRY_SALES_ORG_MAPPING where Sales_Area = '{}' and Currency = '{}'".format(salesOrg,currency))
    if query is not None:
        return query.Execution_County
def rowtotal(row):
    Split1=getFloat_prjt(row["FO Eng 1 % Split"])
    Split2=getFloat_prjt(row["FO Eng 2 % Split"])
    Total_split=Split1+Split2
    return Total_split
def ges_split(row):
    return row["GES Eng % Split"]
def rowtotal2(row):
    Split2=getFloat_prjt(row["FO Eng 2 % Split"])
    return Split2
def rowtotal1(row):
    Split1=getFloat_prjt(row["FO Eng 1 % Split"])
    return Split1
def Fototal(row):
    return row["FO Eng % Split"]
def populateLaborTypeTable1(labotTypeTable,item,laborTypeDict,sellPriceDict):
    addRow = labotTypeTable.AddNewRow()
    addRow["Labor_Type"] = "Total"
    addRow["System"] = item.PartNumber
    addRow["Quote_Item_GuId"] = item.QuoteItemGuid
    addRow["IsHeader"] = "No"
    for laborType in laborTypes:
        addRow = labotTypeTable.AddNewRow()
        addRow["Labor_Type"] = laborType
        addRow["IsHeader"] = "No"
        typeData = laborTypeDict.get(laborType,'')
        if typeData:
            addRow["Hours"] = typeData.get("Hours",0)
            addRow["Total_Cost"] = typeData.get("Total Cost",0)
            addRow["Total_Sell_Price"] = sellPriceDict.get(laborType,0)
            addRow["Quote_Item_GuId"] = item.QuoteItemGuid
def getItemData(item):
    systemgroupData = dict()
    for module in item.Children:
        partData = systemgroupData.get(module.PartNumber,dict())
        for part in module.Children:
            if part.ProductTypeName.lower() == "honeywell labor":
                partData[part.PartNumber] = str(part.NetPrice)
        systemgroupData[module.PartNumber] = partData
    return systemgroupData
def getSellPriceData(laboHours,item):
    fo_partNumber_Mapping = {
"SYS LE-Eng": "HPS_SYS_LE1_P350",
"SYS LE-Design Eng" : "HPS_SYS_LE1_P345",
"SYS LE-Sr Design Eng" : "HPS_SYS_LE1_P310",
"SYS LE-Lead Eng"  : "HPS_SYS_LE1_P305",
"SYS LE-Prin Proj Eng" : "HPS_SYS_LE1_P300",
"SYS SSE-Eng" : "HPS_SYS_SSE_P350",
"SYS SSE-Design Eng":"HPS_SYS_SSE_P345",
"SYS SSE-Sr Design Eng":"HPS_SYS_SSE_P310",
"SYS SSE-Lead Eng":"HPS_SYS_SSE_P305",
"SYS SSE-Prin Proj Eng":"HPS_SYS_SSE_P300",
"SYS CPA-Eng":"HPS_SYS_CPA_P350",
"SYS CPA-Design Eng":"HPS_SYS_CPA_P345",
"SYS CPA-Sr Design Eng":"HPS_SYS_CPA_P310",
"SYS CPA-Lead Eng":"HPS_SYS_CPA_P305",
"SYS CPA-Prin Proj Eng":"HPS_SYS_CPA_P300",
"SYS SNC-Eng":"HPS_SYS_SNC_P350",
"SYS SNC-Design Eng":"HPS_SYS_SNC_P345",
"SYS SNC-Sr Design Eng":"HPS_SYS_SNC_P310",
"SYS SNC-Lead Eng":"HPS_SYS_SNC_P305",
"SYS FIE-Eng":"HPS_SYS_FIE_P350",
"SYS FIE-Design Eng":"HPS_SYS_FIE_P345",
"SYS FIE-Sr Design Eng":"HPS_SYS_FIE_P310",
"SYS FIE-Lead Eng":"HPS_SYS_FIE_P305",
"HPS_GES_P350F_CN":"HPS_GES_P350F_CN",
"HPS_GES_P350B_CN":"HPS_GES_P350B_CN",
"HPS_GES_P350F_UZ":"HPS_GES_P350F_UZ",
"HPS_GES_P350B_UZ":"HPS_GES_P350B_UZ",
"HPS_GES_P350F_RO":"HPS_GES_P350F_RO",
"HPS_GES_P350B_RO":"HPS_GES_P350B_RO",
"HPS_GES_P350F_IN":"HPS_GES_P350F_IN",
"HPS_GES_P350B_IN":"HPS_GES_P350B_IN",
"SYS BPA-Eng":"HPS_SYS_BPA_P350",
"HPS_SYS_BPA_P350":"HPS_SYS_BPA_P350",
"SYS BPA-Design Eng":"HPS_SYS_BPA_P345",
"HPS_SYS_BPA_P345":"HPS_SYS_BPA_P345",
"SYS BPA-Sr Design Eng":"HPS_SYS_BPA_P310",
"HPS_SYS_BPA_P310":"HPS_SYS_BPA_P310",
"SYS BPA-Lead Eng":"HPS_SYS_BPA_P305",
"HPS_SYS_BPA_P305":"HPS_SYS_BPA_P305",
"SYS BPA-Prin Proj Eng":"HPS_SYS_BPA_P300",
"HPS_SYS_BPA_P300":"HPS_SYS_BPA_P300",
"SYS HMI-Eng":"HPS_SYS_HMI_P350",
"HPS_SYS_HMI_P350":"HPS_SYS_HMI_P350",
"SYS HMI-Design Eng":"HPS_SYS_HMI_P345",
"HPS_SYS_HMI_P345":"HPS_SYS_HMI_P345",
"SYS HMI-Sr Design Eng":"HPS_SYS_HMI_P310",
"HPS_SYS_HMI_P310":"HPS_SYS_HMI_P310",
"SYS HMI-Lead Eng":"HPS_SYS_HMI_P305",
"HPS_SYS_HMI_P305":"HPS_SYS_HMI_P305",
"SYS HMI-Prin Proj Eng":"HPS_SYS_HMI_P300",
"HPS_SYS_HMI_P300":"HPS_SYS_HMI_P300",
"SYS SHE-Eng":"HPS_SYS_SHE_P350",
"HPS_SYS_SHE_P350":"HPS_SYS_SHE_P350",
"SYS SHE-Design Eng":"HPS_SYS_SHE_P345",
"HPS_SYS_SHE_P345":"HPS_SYS_SHE_P345",
"SYS SHE-Sr Design Eng":"HPS_SYS_SHE_P310",
"HPS_SYS_SHE_P310":"HPS_SYS_SHE_P310",
"SYS SHE-Lead Eng":"HPS_SYS_SHE_P305",
"HPS_SYS_SHE_P305":"HPS_SYS_SHE_P305",
"SYS SHE-Prin Proj Eng":"HPS_SYS_SHE_P300",
"HPS_SYS_SHE_P300":"HPS_SYS_SHE_P300",
"SYS SII-Eng":"HPS_SYS_SII_P350",
"HPS_SYS_SII_P350":"HPS_SYS_SII_P350",
"SYS SII-Design Eng":"HPS_SYS_SII_P345",
"HPS_SYS_SII_P345":"HPS_SYS_SII_P345",
"SYS SII-Sr Design Eng":"HPS_SYS_SII_P310",
"HPS_SYS_SII_P310":"HPS_SYS_SII_P310",
"SYS SII-Lead Eng":"HPS_SYS_SII_P305",
"HPS_SYS_SII_P305":"HPS_SYS_SII_P305",
"SYS SII-Prin Proj Eng":"HPS_SYS_SII_P300",
"HPS_SYS_SII_P300":"HPS_SYS_SII_P300",
"SYS SNC-Prin Proj Eng":"HPS_SYS_SNC_P300",
"HPS_SYS_SNC_P300":"HPS_SYS_SNC_P300",
"SYS FIE-Prin ProjEng":"HPS_SYS_FIE_P300",
"HPS_SYS_FIE_P300":"HPS_SYS_FIE_P300",
"SYS GES HMI Eng-FO-UZ":"HPS_GES_P335F_UZ",
"HPS_GES_P335F_UZ":"HPS_GES_P335F_UZ",
"SYS GES HMI Eng-FO-RO":"HPS_GES_P335F_RO",
"HPS_GES_P335F_RO":"HPS_GES_P335F_RO",
"SYS GES HMI Eng-FO-IN":"HPS_GES_P335F_IN",
"HPS_GES_P335F_IN":"HPS_GES_P335F_IN",
"SYS GES HMI Eng-FO-CN":"HPS_GES_P335F_CN",
"HPS_GES_P335F_CN":"HPS_GES_P335F_CN",
"SYS GES HMI Eng-BO-UZ":"HPS_GES_P335B_UZ",
"HPS_GES_P335B_UZ":"HPS_GES_P335B_UZ",
"SYS GES HMI Eng-BO-RO":"HPS_GES_P335B_RO",
"HPS_GES_P335B_RO":"HPS_GES_P335B_RO",
"SYS GES HMI Eng-BO-IN":"HPS_GES_P335B_IN",
"HPS_GES_P335B_IN":"HPS_GES_P335B_IN",
"SYS GES HMI Eng-BO-CN":"HPS_GES_P335B_CN",
"HPS_GES_P335B_CN":"HPS_GES_P335B_CN",
"SYS GES Eng-FO-UZ":"HPS_GES_P350F_UZ",
"HPS_GES_P350F_UZ":"HPS_GES_P350F_UZ",
"SYS GES Eng-BO-UZ":"HPS_GES_P350B_UZ",
"HPS_GES_P350B_UZ":"HPS_GES_P350B_UZ",
"SYS GES Eng-FO-RO":"HPS_GES_P350F_RO",
"HPS_GES_P350F_RO":"HPS_GES_P350F_RO",
"SYS GES Eng-BO-RO":"HPS_GES_P350B_RO",
"HPS_GES_P350B_RO":"HPS_GES_P350B_RO",
"SYS GES Eng-FO-IN":"HPS_GES_P350F_IN",
"HPS_GES_P350F_IN":"HPS_GES_P350F_IN",
"SYS GES Eng-BO-IN":"HPS_GES_P350B_IN",
"HPS_GES_P350B_IN":"HPS_GES_P350B_IN",
"SYS GES Eng-FO-CN":"HPS_GES_P350F_CN",
"HPS_GES_P350F_CN":"HPS_GES_P350F_CN",
"SYS GES Eng-BO-CN":"HPS_GES_P350B_CN",
"HPS_SYS_LE1_P350":"HPS_SYS_LE1_P350",
"HPS_SYS_LE1_P345":"HPS_SYS_LE1_P345",
"HPS_SYS_LE1_P310":"HPS_SYS_LE1_P310",
"HPS_SYS_LE1_P305":"HPS_SYS_LE1_P305",
"HPS_SYS_LE1_P300":"HPS_SYS_LE1_P300",
"HPS_SYS_SSE_P350":"HPS_SYS_SSE_P350",
"HPS_SYS_SSE_P345":"HPS_SYS_SSE_P345",
"HPS_SYS_SSE_P310":"HPS_SYS_SSE_P310",
"HPS_SYS_SSE_P305":"HPS_SYS_SSE_P305",
"HPS_SYS_SSE_P300":"HPS_SYS_SSE_P300",
"HPS_SYS_CPA_P350":"HPS_SYS_CPA_P350",
"HPS_SYS_CPA_P345":"HPS_SYS_CPA_P345",
"HPS_SYS_CPA_P310":"HPS_SYS_CPA_P310",
"HPS_SYS_CPA_P305":"HPS_SYS_CPA_P305",
"HPS_SYS_CPA_P300":"HPS_SYS_CPA_P300",
"HPS_SYS_SNC_P350":"HPS_SYS_SNC_P350",
"HPS_SYS_SNC_P345":"HPS_SYS_SNC_P345",
"HPS_SYS_SNC_P310":"HPS_SYS_SNC_P310",
"HPS_SYS_SNC_P305":"HPS_SYS_SNC_P305",
"HPS_SYS_FIE_P350":"HPS_SYS_FIE_P350",
"HPS_SYS_FIE_P345":"HPS_SYS_FIE_P345",
"HPS_SYS_FIE_P310":"HPS_SYS_FIE_P310",
"HPS_SYS_FIE_P305":"HPS_SYS_FIE_P305",
"HPS_GES_P350F_CN":"HPS_GES_P350F_CN",
"HPS_GES_P350B_CN":"HPS_GES_P350B_CN",
"HPS_GES_P350F_UZ":"HPS_GES_P350F_UZ",
"HPS_GES_P350B_UZ":"HPS_GES_P350B_UZ",
"HPS_GES_P350F_RO":"HPS_GES_P350F_RO",
"HPS_GES_P350B_RO":"HPS_GES_P350B_RO",
"HPS_GES_P350F_IN":"HPS_GES_P350F_IN",
"HPS_GES_P350B_IN" :"HPS_GES_P350B_IN",
"HPS_GES_P350F_EG":"HPS_GES_P350F_EG",
"HPS_GES_P350B_EG" :"HPS_GES_P350B_EG",
"HPS_GES_P335B_EG":"HPS_GES_P335B_EG",
"HPS_GES_P335F_EG":"HPS_GES_P335F_EG",
"SYS GES HMI Eng-FO-EG":"HPS_GES_P335F_EG",
"SYS GES HMI Eng-BO-EG":"HPS_GES_P335B_EG",
"SYS GES Eng-BO-EG":"HPS_GES_P350B_EG",
"SYS GES Eng-FO-EG":"HPS_GES_P350F_EG"
}
    sellPriceDict = dict()
    itemSellPriceData = itemData.get(item.PartNumber,'')
    for laboType,product in laboHours.items():
        sellPrice = 0
        for prodName, partNum in product.items():
            if itemSellPriceData:
                for part,hour in partNum.items():
                     if prodName == item.ProductName and part and itemSellPriceData.get(fo_partNumber_Mapping[part],'') != '':
                        sellPrice += getFloat_prjt(hour) * getFloat_prjt(itemSellPriceData.get(fo_partNumber_Mapping[part],''))
        sellPriceDict[laboType] = sellPrice
    return sellPriceDict
def calculateTotals(labotTypeTable,item):
    if labotTypeTable.Rows.Count > 0:
        totalHours = 0
        totalcost = 0
        totalSellPrice = 0
        for row in labotTypeTable.Rows:
            if row["Quote_Item_GuId"] == item.QuoteItemGuid:
                totalHours += getFloat_prjt(row["Hours"])
                totalcost += getFloat_prjt(row["Total_Cost"])
                totalSellPrice += getFloat_prjt(row["Total_Sell_Price"])
        for row in labotTypeTable.Rows:
            if row["Quote_Item_GuId"] == item.QuoteItemGuid:
                if row["Labor_Type"] == "Total":
                    row["Hours"] = totalHours
                    row["Total_Cost"] = totalcost
                    row["Total_Sell_Price"] = totalSellPrice
                else:
                    row["Percentage"] = str(format(round((getFloat_prjt(row["Hours"]) / totalHours) * 100,2),".2f")) if  totalHours > 0 else 0
                    row["Percentage"] = str(row["Percentage"])+str("%")
            elif row["Labor_Type"] != "Total" and row["Quote_Item_GuId"] == "":
                row["Percentage"] = str(format(round((getFloat_prjt(row["Hours"]) / totalHours) * 100,2),".2f")) if  totalHours > 0 else 0
                row["Percentage"] = str(row["Percentage"])+str("%")

def getFinalHours(container,product):
	for row in container.Rows:
		TotalFOEngsplit=rowtotal(row)
		TotalFOEngsplit1=rowtotal1(row)
		TotalFOEngsplit2=rowtotal2(row)
		gesplit = ges_split(row)
		excecutionCountry=getExecutionCountry(Quote)
		if row["Execution Country"]== excecutionCountry and row["Final Hrs"] not in ('',"0") and (TotalFOEngsplit1 != '0' or TotalFOEngsplit2 != '0'):
			addValues(laborTypeDict,"Front Office Labor","Hours",round(getFloat_prjt(row["Final Hrs"]) * getFloat_prjt(TotalFOEngsplit1) / 100)+round(getFloat_prjt(row["Final Hrs"]) * getFloat_prjt(TotalFOEngsplit2) / 100))
			addValues(laborTypeDict,"Front Office Labor","Total Cost",round(getFloat_prjt(row["FO_Regional_Cost"]),2))
			addValues(laboHours["Front Office Labor"], product, row["FO Eng 1"],round(getFloat_prjt(row["Final Hrs"]) * getFloat_prjt(TotalFOEngsplit1) / 100))
			addValues(laboHours["Front Office Labor"], product, row["FO Eng 2"],round(getFloat_prjt(row["Final Hrs"]) * getFloat_prjt(TotalFOEngsplit2) / 100))
		elif row["Final Hrs"] not in ('',"0") and TotalFOEngsplit != '0':
			addValues(laborTypeDict,"Intercompany Labor","Hours",round(getFloat_prjt(row["Final Hrs"]) * getFloat_prjt(TotalFOEngsplit1) / 100)+round(getFloat_prjt(row["Final Hrs"]) * getFloat_prjt(TotalFOEngsplit2) / 100))
			addValues(laborTypeDict,"Intercompany Labor","Total Cost",round(getFloat_prjt(row["FO_Regional_Cost"]),2))
			addValues(laboHours["Intercompany Labor"], product, row["FO Eng 1"],round(getFloat_prjt(row["Final Hrs"]) * getFloat_prjt(TotalFOEngsplit1) / 100))
			addValues(laboHours["Intercompany Labor"], product, row["FO Eng 2"],round(getFloat_prjt(row["Final Hrs"]) * getFloat_prjt(TotalFOEngsplit2) / 100))
		if row["Final Hrs"] not in ('',"0") and row["GES Eng"] != '' and row["GES Eng % Split"] != '0':
			GES_Eng=row["GES Eng"]
			if GES_Eng in ('HPS_GES_P350B_IN','HPS_GES_P350B_CN','HPS_GES_P350B_RO','HPS_GES_P350B_UZ','HPS_GES_P335B_IN','HPS_GES_P335B_CN','HPS_GES_P335B_RO','HPS_GES_P335B_UZ','HPS_GES_P215B_IN','HPS_GES_P215B_CN','HPS_GES_P215B_RO','HPS_GES_P215B_UZ','HPS_GES_P350B_EG','HPS_GES_P335B_EG'):
				addValues(laborTypeDict,"GES Back -office Labor","Hours",round(getFloat_prjt(row["Final Hrs"]) * getFloat_prjt(gesplit) / 100))
				addValues(laborTypeDict,"GES Back -office Labor","Total Cost",round(getFloat_prjt(row["GES_Regional_Cost"]),2))
				addValues(laboHours["GES Back -office Labor"], product, row["GES Eng"],round(getFloat_prjt(row["Final Hrs"]) * getFloat_prjt(gesplit) / 100))
			elif GES_Eng in ('HPS_GES_P350F_IN','HPS_GES_P350F_CN','HPS_GES_P350F_RO','HPS_GES_P350F_UZ','HPS_GES_P215F_CN','HPS_GES_P215F_IN','HPS_GES_P215F_RO','HPS_GES_P215F_UZ','HPS_GES_P335F_CN','HPS_GES_P335F_IN','HPS_GES_P335F_RO','HPS_GES_P335F_UZ','HPS_GES_P350F_EG','HPS_GES_P335F_EG'):
				addValues(laborTypeDict,"GES On-site Labor","Hours",round(getFloat_prjt(row["Final Hrs"]) * getFloat_prjt(gesplit) / 100))
				addValues(laborTypeDict,"GES On-site Labor","Total Cost",round(getFloat_prjt(row["GES_Regional_Cost"]),2))
				addValues(laboHours["GES On-site Labor"], product, row["GES Eng"],round(getFloat_prjt(row["Final Hrs"]) * getFloat_prjt(gesplit) / 100))
			elif item.ProductTypeName =="Honeywell Labor" and txt.startswith("SVC-") and not txt.startswith("HPS_SYS_") :
				addFinalHours_prjt(laborHours, "Front Office Labor", round(getFloat_prjt(item.Quantity)))
def getFinaladdHours(container,product):
	for row in container.Rows:
		TotalFOEngsplit=Fototal(row)
		excecutionCountry=getExecutionCountry(Quote)
		if row["Execution Country"]== excecutionCountry and row["Final Hrs"] not in ('',"0") and TotalFOEngsplit != '0':
			addValues(laborTypeDict,"Front Office Labor","Hours",round(getFloat_prjt(row["Final Hrs"]) * getFloat_prjt(TotalFOEngsplit) / 100))
			addValues(laborTypeDict,"Front Office Labor","Total Cost",round(getFloat_prjt(row["FO_Regional_Cost"]),2))
			addValues(laboHours["Front Office Labor"], product, row["FO Eng"],round(getFloat_prjt(row["Final Hrs"]) * getFloat_prjt(TotalFOEngsplit) / 100))
		elif row["Final Hrs"] not in ('',"0") and TotalFOEngsplit != '0':
			addValues(laborTypeDict,"Intercompany Labor","Hours",round(getFloat_prjt(row["Final Hrs"]) * getFloat_prjt(TotalFOEngsplit) / 100))
			addValues(laborTypeDict,"Intercompany Labor","Total Cost",round(getFloat_prjt(row["FO_Regional_Cost"]),2))
			addValues(laboHours["Intercompany Labor"], product, row["FO Eng"],round(getFloat_prjt(row["Final Hrs"]) * getFloat_prjt(TotalFOEngsplit) / 100))
		if row["Final Hrs"] not in ('',"0") and row["GES Eng"] != '' and row["GES Eng % Split"] != '0':
			GES_Eng=row["GES Eng"]
			if GES_Eng in ('HPS_GES_P350B_IN','HPS_GES_P350B_CN','HPS_GES_P350B_RO','HPS_GES_P350B_UZ','HPS_GES_P335B_IN','HPS_GES_P335B_CN','HPS_GES_P335B_RO','HPS_GES_P335B_UZ','HPS_GES_P215B_IN','HPS_GES_P215B_CN','HPS_GES_P215B_RO','HPS_GES_P215B_UZ','HPS_GES_P350B_EG','HPS_GES_P335B_EG'):
				addValues(laborTypeDict,"GES Back -office Labor","Hours",round(getFloat_prjt(row["Final Hrs"]) * getFloat_prjt(row["GES Eng % Split"]) / 100))
				addValues(laborTypeDict,"GES Back -office Labor","Total Cost",round(getFloat_prjt(row["GES_Regional_Cost"]),2))
				addValues(laboHours["GES Back -office Labor"], product, row["GES Eng"],round(getFloat_prjt(row["Final Hrs"]) * getFloat_prjt(row["GES Eng % Split"]) / 100))
			elif GES_Eng in ('HPS_GES_P350F_IN','HPS_GES_P350F_CN','HPS_GES_P350F_RO','HPS_GES_P350F_UZ','HPS_GES_P215F_CN','HPS_GES_P215F_IN','HPS_GES_P215F_RO','HPS_GES_P215F_UZ','HPS_GES_P335F_CN','HPS_GES_P335F_IN','HPS_GES_P335F_RO','HPS_GES_P335F_UZ','HPS_GES_P350F_EG','HPS_GES_P335F_EG'):
				addValues(laborTypeDict,"GES On-site Labor","Hours",round(getFloat_prjt(row["Final Hrs"]) * getFloat_prjt(row["GES Eng % Split"]) / 100))
				addValues(laborTypeDict,"GES On-site Labor","Total Cost",round(getFloat_prjt(row["GES_Regional_Cost"]),2))
				addValues(laboHours["GES On-site Labor"], product, row["GES Eng"],round(getFloat_prjt(row["Final Hrs"]) * getFloat_prjt(row["GES Eng % Split"]) / 100))
			elif item.ProductTypeName =="Honeywell Labor" and txt.startswith("SVC-") and not txt.startswith("HPS_SYS_") :
				addFinalHours_prjt(laborHours, "Front Office Labor", round(getFloat_prjt(item.Quantity)))
try:
    excecutionCountry = getExecutionCountry(Quote)
    laborTypes = ['Front Office Labor','Intercompany Labor','GES Back -office Labor','GES On-site Labor']
    labotTypeTable = Quote.QuoteTables["Sys_Grp_Level_labor_type"]
    labotTypeTable.Rows.Clear()
    product_name=["One Wireless System","Tank Gauging Engineering","Public Address General Alarm System","PRMS Skid Engineering","Metering Skid Engineering", "Fire Detection & Alarm Engineering","MS Analyser System Engineering","Gas MeterSuite Engineering - C300 Functions","Liquid MeterSuite Engineering - C300 Functions","Industrial Security (Access Control)","MeterSuite Engineering - MSC Functions"]
    conNames = {
                "System Group" : "CE_System_Cont",
                "PRMS Skid Engineering" : "PRMS_Engineering_Labor_Container",
                "MS Analyser System Engineering" : "MS_ASE_Engineering_Labor_Container",
                "Fire Detection & Alarm Engineering": "FDA_Engineering_Labor_Container",
                "Public Address General Alarm System": "PAGA_Labor_Container",
                "Industrial Security (Access Control)": "IS_Labor_Container",
                "Tank Gauging Engineering": "TGE_Engineering_Labor_Container",
                "Gas MeterSuite Engineering - C300 Functions": "Gas_MeterSuite_Engineering_Labor_Container",
                "Liquid MeterSuite Engineering - C300 Functions" : "LMS_Labor_Container",
                "MeterSuite Engineering - MSC Functions": "MSC_Engineering_Labor_Container",
                "One Wireless System": "OWS_Engineering_Labor_Container",
                "Metering Skid Engineering": "MSE_Engineering_Labor_Container"
                }
    adtnl_Containers = {
                "One Wireless System":"OWS_Additional_Labour_Container",
                "Industrial Security (Access Control)":"IS_Additional_Labor_Container",
                "Public Address General Alarm System":"PAGA_Additional_Labour_Container",
                "Fire Detection & Alarm Engineering":"FDA_Additional_Labor_Container",
                "MeterSuite Engineering - MSC Functions":"MSC_Additional_Labour_Container",
                "Liquid MeterSuite Engineering - C300 Functions":"LMS_Additional_Labor_Container",
                "Gas MeterSuite Engineering - C300 Functions":"Gas_MeterSuite_Additional_Labor_Container",
                "MS Analyser System Engineering":"MS_ASE_Additional_Labour_Container",
                "PRMS Skid Engineering":"PRMS_Additional_Labor_Container",
                "Metering Skid Engineering":"MSE_Additional_Labor_Container",
                "Tank Gauging Engineering":"TGE_Additional_Labour_Container"
                }
    for item in Quote.MainItems:
        if item.ProductName == "System Group":
            laborTypeDict = dict()
            laboHours = dict()
            laboHours["Front Office Labor"] = dict()
            laboHours["Intercompany Labor"] = dict()
            laboHours["GES Back -office Labor"] = dict()
            laboHours["GES On-site Labor"] = dict()
            sellPriceDict = {}
            itemData = getItemData(item)
            sysdict = {'Front Office Labor':0,'Intercompany Labor':0,'GES Back -office Labor':0,'GES On-site Labor':0}
            for prod in item.Children:
                if prod.ProductName in product_name:
                    con = prod.SelectedAttributes.GetContainerByName(conNames[prod.ProductName])
                    Addcon = prod.SelectedAttributes.GetContainerByName(adtnl_Containers[prod.ProductName])
                    getFinalHours(con,prod.ProductName)
                    getFinaladdHours(Addcon,prod.ProductName)
                    sellPriceDict = getSellPriceData(laboHours,prod)
                    for i in sellPriceDict.keys():
                        sysdict[i] += sellPriceDict[i]
            if sysdict:
                populateLaborTypeTable1(labotTypeTable,item,laborTypeDict,sysdict)
                calculateTotals(labotTypeTable,item)
    laborTypeTableData = dict()
    for row in labotTypeTable.Rows:
        if row["Labor_Type"] != "Total":
            addValues(laborTypeTableData,row["Labor_Type"],"Hours",row["Hours"])
            addValues(laborTypeTableData,row["Labor_Type"],"Total_Cost",row["Total_Cost"])
            addValues(laborTypeTableData,row["Labor_Type"],"Total_Sell_Price",row["Total_Sell_Price"])
    headerlabotTypeTable = Quote.QuoteTables["Quote_Level_Labor_Type"]
    headerlabotTypeTable.Rows.Clear()
    populateLaborTypeTable2(headerlabotTypeTable,laborTypeTableData)

    if headerlabotTypeTable.Rows.Count > 0:
        totalHours = 0
        totalcost = 0
        totalSellPrice = 0
        for row in headerlabotTypeTable.Rows:
            if row["IsHeader"] == "Yes":
                totalHours += getFloat_prjt(row["Hours"])
                totalcost += getFloat_prjt(row["Total_Cost"])
                totalSellPrice += getFloat_prjt(row["Total_Sell_Price"])
        for row in headerlabotTypeTable.Rows:
            if row["IsHeader"] == "Yes":
                if row["Labor_Type"] == "Total":
                    row["Hours"] = totalHours
                    row["Total_Cost"] = totalcost
                    row["Total_Sell_Price"] = totalSellPrice
                else:
                    row["Percentage"] = str(format(round((getFloat_prjt(row["Hours"]) / totalHours) * 100,2),".2f")) if  totalHours > 0 else 0
                    row["Percentage"] = str(row["Percentage"])+str("%")
    labotTypeTable.Save()
    headerlabotTypeTable.Save()
except Exception as e:
    Log.Write("Non ICSS"+str(e))
#CA_NonICSS_LaborType_Temp end
#CA_NonICSS_ServicematerialType_Temp excuation Start
ScriptExecutor.Execute('GS_CA_NonICSS_ServicematerialType_Temp')
#CA_NonICSS_ServicematerialType_Temp excuation end