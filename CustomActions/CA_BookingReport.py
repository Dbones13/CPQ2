from GS_CalculateTotals import getWriteInProductType
import GS_Booking_report

def getProductLineMap(groupingKey):
    plDict = dict()
    ptPlMap = dict()
    guidPartNumberMap = dict()
    srvModulePriceMap = dict()
    writeInProductTypes = getWriteInProductType(Quote)
    chinaDataDict = GS_Booking_report.getChinaDataDict()
    indiaDataDict = GS_Booking_report.getIndiaDataDict()
    for item in Quote.Items:
        guidPartNumberMap[item.QuoteItemGuid] = item.PartNumber if item.ProductName not in ('Generic System','Winest Labor Import') else item.ProductName
        if item[groupingKey].Value == "":
            continue
        plDict[item.PartNumber] = item[groupingKey].Value
        productType = item.ProductTypeName
        if item.ProductTypeName == "Write-In":
            productType = writeInProductTypes.get(item.PartNumber, item.ProductTypeName)
            if productType.upper() == 'PRE-SALES':
                productType = 'PRE-SALES'
        ptData = ptPlMap.get(productType, {"totalCost": 0, "totalSell": 0, "totalWTW": 0})
        plData = ptData.get(item[groupingKey].Value, dict())
        plData["quoteSellPrice"] = plData.get("quoteSellPrice", 0) + float(item.ExtendedAmount)
        plData["cost"] = plData.get("cost", 0) + float(item.ExtendedCost)
        if Quote.GetCustomField('Booking LOB').Content == 'CCC':
            if Quote.GetCustomField('Booking Country').Content.lower() == 'united states':
                plData["wtw"] = plData.get("wtw", 0) + float(item.QI_ExtendedWTWCost.Value) 
            elif Quote.GetCustomField('Booking Country').Content.lower() == 'brazil':
                plData["wtw"] = plData.get("wtw", 0) + (float(item.ExtendedAmount)*float(0.80)) 
            else:
                plData["wtw"] = plData.get("wtw", 0) + (float(item.ExtendedAmount)*float(0.85)) 
        else:
            plData["wtw"] = 0
        plData["productLineDesc"] = (item[groupingKey+"Desc"].Value).encode("ASCII", "ignore")
        chinaData = chinaDataDict.get(item[groupingKey].Value)
        if chinaData:
            plData.update(chinaData)
        indiaData = indiaDataDict.get(item[groupingKey].Value)
        if indiaData:
            plData.update(indiaData)
        ptData[item[groupingKey].Value] = plData
        ptData["totalCost"] += float(item.ExtendedCost)
        ptData["totalSell"] += float(item.ExtendedAmount)
        if Quote.GetCustomField('Booking LOB').Content == 'CCC':
            if Quote.GetCustomField('Booking Country').Content.lower() == 'united states':
                ptData["totalWTW"] += float(item.QI_ExtendedWTWCost.Value)
            elif Quote.GetCustomField('Booking Country').Content.lower() == 'brazil':
                ptData["totalWTW"] += (float(item.ExtendedAmount)*float(0.80)) 
            else:
                ptData["totalWTW"] += (float(item.ExtendedAmount)*float(0.85)) 
        else:
            ptData["totalWTW"] = 0
        ptPlMap[productType] = ptData
        try:
            guid_partnumber = guidPartNumberMap[item.ParentItemGuid]
        except:
            guid_partnumber=''
        if item.ParentItemGuid and guid_partnumber in ("OPM","EBR","ELCN","Orion Console","Project Management","TPS_to_EXP","TCMI","EHPM/EHPMX/ C300PM","C200_Migration","EHPM_HART_IO","CB_EC_Upgrade_to_C300_UHIO","FSC to SM","FSC to SM Audit","LM_ELMM_ControlEdge_PLC","xPM to C300 Migration","CD Actuator I-F Upgrade","XP10 Actuator Upgrade","Graphics Migration","Generic System Migration","Trace Software","3rd Party PLC to ControlEdge PLC/UOC","QCS RAE Upgrade","CWS RAE Upgrade","TPA/PMD Migration","FSC to SM IO Migration","FSC to SM IO Audit","ELEPIU ControlEdge RTU Migration Engineering","Virtualization System","ASSESSMENT","SMX","Cyber Generic System","MSS","PCN","CYBER_APP_CNTRL","LCN","IAA","PHD_Labor","Uniformance_Insight_Labor","AFM_Labor","HCI_LABOR","HCI_EDM"):
            modName = guidPartNumberMap[item.ParentItemGuid]
            srvModulePriceMap[(modName, item.PartNumber)] = item.NetPrice
        if item.ParentItemGuid and guid_partnumber in ("FDM Upgrade 1","FDM Upgrade 2","FDM Upgrade 3"):
            srvModulePriceMap[('FDM Upgrade', item.PartNumber)] = item.NetPrice
        if item.ParentItemGuid and guid_partnumber in ("C200_Migration"):
            srvModulePriceMap[('C200 Migration', item.PartNumber)] = item.NetPrice
        if item.ParentItemGuid and guid_partnumber in ("PRJT","PMD","FDM System","ControlEdge RTU System","PLC","UOC","CN900","HS","Virtualization","3rd Party Devices/Systems Interface (SCADA)","eServer System","ARO, RESS & ERG System","Digital Video Manager","ESDC","Simulation System","MXProLine","Experion Enterprise System","C300 System","Experion MX","PlantCruise","HC900","VFD","Measurement IQ","SM ESD","SM FGS","SM BMS","SM HIPPS","TM","MasterLogic-50 Generic","MasterLogic-200 Generic","Experion LX Generic","Fire and Gas Consultancy Service","Industrial Security (Access Control)","Liquid MeterSuite Engineering - C300 Functions","MeterSuite Engineering - MSC Functions","MS Analyser System Engineering","Public Address General Alarm System","PRMS Skid Engineering","Tank Gauging Engineering","Gas MeterSuite Engineering - C300 Functions","One Wireless System","Fire Detection & Alarm Engineering","Metering Skid Engineering","Process Safety Workbench Engineering","PCD","Generic System","Winest Labor Import"):
            modName = item.ParentItemGuid
            srvModulePriceMap[(modName, item.PartNumber)] = item.NetPrice
    return plDict, ptPlMap, srvModulePriceMap

def getSespBgpDataDict():
    results = SqlHelper.GetList("SELECT * FROM SESP_BGP_DATA")
    res = dict()
    for result in results:
        res[result.Product_Line] =  result.SESP_BGP
    return res
def getCurrencyFactor(quote):
    quoteCurrency = quote.GetCustomField("Currency").Content
    functionalCurrency = quote.GetCustomField("Functional Currency of Entity").Content
    currencyFactor = 1.00
    if quoteCurrency and functionalCurrency and quoteCurrency != functionalCurrency:
        currencyFactorToUSD = float(SqlHelper.GetFirst("SELECT Exchange_Rate FROM CURRENCY_EXCHANGERATE_MAPPING WHERE From_Currency = '{}' AND To_Currency = 'USD'".format(quoteCurrency)).Exchange_Rate)
        currencyFactorFromUSD = float(SqlHelper.GetFirst("SELECT Exchange_Rate FROM CURRENCY_EXCHANGERATE_MAPPING WHERE From_Currency = 'USD' AND To_Currency = '{}'".format(functionalCurrency)).Exchange_Rate)
        currencyFactor = currencyFactorToUSD * currencyFactorFromUSD
    quote.GetCustomField("ConversionRateBR").Content = str(currencyFactor)
    return currencyFactor
def setDiscountIndex(quote):
    specialPriceFlag = False
    disCounter = 0
    salesArea = quote.GetCustomField("Sales Area").Content
    if salesArea in ["623P", "624P"]:
        disCounter = 0
    elif salesArea == "876P" or (salesArea == "588P" and not specialPriceFlag):
        disCounter = 1
    elif salesArea == "588P"  and specialPriceFlag:
        disCounter = 2
    return disCounter
def populateLaborRows(quote, srvModulePriceMap, sespBgpDict,plDict):
    global totalIndiaTP
    global totalChinaTP
    global totalChinaTP2
    subtotalIndiaTP,subtotalChinaTP,subtotalChinaTP2 = 0,0,0
    currencyFactor = getCurrencyFactor(quote)
    laborData = GS_Booking_report.getMigrationLaborData(quote, srvModulePriceMap,plDict)
    disCounter = setDiscountIndex(quote)
    discountPer = 0
    total_hour ,total_cost ,total_sell= 0,0,0
    if not laborData:
        Trace.Write("No Labor Data!")
    table = quote.QuoteTables["QT_Booking_Report"]
    for network, networkData in laborData.items():
        newRow_outer = table.AddNewRow()
        newRow_outer["Product_Line_Description"] = network
        for execName, plDataDict in networkData.items():
            for pl, plData in plDataDict.items():
                newRow = table.AddNewRow()
                newRow["Product_Line"] = pl
                newRow["Product_Line_Description"] = execName
                newRow["Sell_Price"] = plData.get("quoteSellPrice", 0)
                newRow["Hrs"] = plData.get("hrs", 0)
                newRow["Cost"] = plData.get("cost", 0)
                newRow["Company_Code_Sell"] = float(plData.get("quoteSellPrice", 0) * currencyFactor)
                newRow["Company_Code_Cost"] = float(plData.get("cost", 0) * currencyFactor)
                newRow["CCC_Standard_Cost"] = float(plData.get("cost", 0)) if Quote.GetCustomField('Booking LOB').Content == 'CCC' else int(0)
                newRow["CCC_COST_Booking_Country"] = (float(plData.get("cost", 0)) if Quote.GetCustomField('Booking LOB').Content == 'CCC' else int(0))*currencyFactor
                if str(plData["quoteSellPrice"]) not in ('0','0.00','0.0'):
                    newRow["CCC_Margin"] = ((float(plData.get("quoteSellPrice", 0)) - float(float(plData.get("cost", 0)) if Quote.GetCustomField('Booking LOB').Content == 'CCC' else int(0)))/float(plData.get("quoteSellPrice", 0)))*100
                newRow["China_TP_Discount"] = "Not Discounted" if plData.get("China_S1_Discount",0) in (0,"0", "","N/A") else "Discounted"
                newRow["China_TP_Discount2"] = "Not Discounted" if plData.get("China_S2_Discount",0) in (0,"0", "","N/A") else "Discounted"
                newRow["Order_Product_Type"] = "Honeywell Labor"
                newRow["Order_SAP_Network_Name"] = network
                try:
                    disCounter = setDiscountIndex(quote)
                    disCounter = disCounter if "," in (plData.get("China_S1_Discount","0")) else 0
                    discountPer =  (plData.get("China_S1_Discount","0").split(",")[disCounter])  if ((plData.get("China_S1_Discount","0").split(",")[disCounter])) != "N/A" else 0
                    newRow["China_TP"] = ((100 - float(discountPer) ) * float(plData["cost"]))/100
                except Exception as e:
                    Log.Info("China_TP:: Exception: {}".format(str(e)))
                    pass
                try:
                    disCounter = setDiscountIndex(quote)
                    disCounter = disCounter if "," in (plData.get("China_S2_Discount","0")) else 0
                    discountPer = (plData.get("China_S2_Discount","0").split(",")[disCounter])  if  ((plData.get("China_S2_Discount","0").split(",")[disCounter])) != "N/A" else 0
                    newRow["China_TP2"] = ((100 - float(discountPer) ) * float(plData["cost"]))/100
                except Exception as e:
                    Log.Info("China_TP2:: Exception: {}".format(str(e)))
                    pass
                pl = pl.Split('-')[0]
                newRow["India_SESP_BGP"] = sespBgpDict.get(pl,"Ignore")
                newRow["India_TP_Discount"] = "Not Discounted" if plData.get("India_Discount_Percent",0) in (0,"0", "","N/A") else "Discounted"
                try:
                    newRow["India_TP"] = ((100 - float(plData.get("India_Discount_Percent","0"))) * float(plData["cost"]))/100
                    totalIndiaTP +=  float(newRow["India_TP"]) if newRow["India_TP"] not in (0,"0", "","N/A") else 0
                    totalChinaTP +=  float(newRow["China_TP"]) if newRow["China_TP"] not in (0,"0", "","N/A") else 0
                    totalChinaTP2 +=  float(newRow["China_TP2"]) if newRow["China_TP2"] not in (0,"0", "","N/A") else 0
                    subtotalIndiaTP +=  float(newRow["India_TP"]) if newRow["India_TP"] not in (0,"0", "","N/A") else 0
                    subtotalChinaTP +=  float(newRow["China_TP"]) if newRow["China_TP"] not in (0,"0", "","N/A") else 0
                    subtotalChinaTP2 +=  float(newRow["China_TP2"]) if newRow["China_TP2"] not in (0,"0", "","N/A") else 0
                except Exception as e:
                    Log.Info("China_TP2:: Exception: {}".format(str(e)))
                    pass
                total_hour += float(newRow["Hrs"])
                total_cost += float(newRow["Cost"])
                total_sell += float(newRow["Sell_Price"])
        newRow_outer["India_TP"] = subtotalIndiaTP
        newRow_outer["China_TP"] = subtotalChinaTP
        newRow_outer["China_TP2"] = subtotalChinaTP2
    return total_hour,total_cost,total_sell
def indiaBookingReportData(SG):
    results = SqlHelper.GetFirst("SELECT Discount_Percent FROM BOOKINGREPORT_INDIA where SG like '{0}%'".format(SG))
    if results:
        return results.Discount_Percent
    else:
        return 0

def chinaBookingReportData(SG):
    results = SqlHelper.GetFirst("SELECT China_S1_Discount,China_S2_Discount FROM BOOKINGREPORT_CHINA where PL like '{0}%'".format(SG))
    if results:
        discount1 = results.China_S1_Discount
        discount2 = results.China_S2_Discount
        return discount1,discount2
    else:
        return 0, 0
def populateQuoteTable(quote, ptPlMap, srvModulePriceMap, sespBgpDict,plDict):
    global totalIndiaTP
    global totalChinaTP
    global totalChinaTP2
    currencyFactor = getCurrencyFactor(quote)
    totalQuoteSellPrice, totalQuoteCostPrice, totalQuote_CCC_CostPrice= 0.00, 0.00, 0.00
    totalQuoteHours, totalQuoteMargin = 0, 0
    headerList = []
    discountPer = 0
    disCounter = setDiscountIndex(quote)
    table = quote.QuoteTables["QT_Booking_Report"]
    table.Rows.Clear()
    headerOrder = [
        "PRE-SALES",
        "Honeywell Material",
        "Honeywell Software",
        "Honeywell Labor",
        "Third-Party Material",
        "Third-Party Labor",
        "Other"
    ]
    for header in headerOrder:

        subtotalIndiaTP,subtotalChinaTP,subtotalChinaTP2 = 0,0,0
        data = ptPlMap.get(header)
        if not data:
            continue
        totalQuoteSellPrice += data["totalSell"]
        totalQuoteCostPrice += data["totalCost"]
        totalQuote_CCC_CostPrice += float(data["totalWTW"]) if Quote.GetCustomField('Booking LOB').Content == 'CCC' and header in("Honeywell Material","Honeywell Software") else float(data["totalCost"]) if Quote.GetCustomField('Booking LOB').Content == 'CCC' else int(0)
        margin = round((data["totalSell"] - data["totalCost"] )/ data["totalSell"] if (data["totalSell"] != 0 and data["totalSell"] != '') else 0, 4)
        newRow_outer = table.AddNewRow()
        newRow_outer["Product_Type"] = (
            "Honeywell Hardware" if header == "Honeywell Material" else header
        )
        newRow_outer["Sell_Price"] = data["totalSell"]
        newRow_outer["Cost"] = data["totalCost"]
        newRow_outer["Margin"] = margin
        newRow_outer["Company_Code_Sell"] = float(data["totalSell"] * currencyFactor)
        newRow_outer["Company_Code_Cost"] = float(data["totalCost"] * currencyFactor)
        newRow_outer["CCC_Standard_Cost"] = float(data["totalWTW"]) if Quote.GetCustomField('Booking LOB').Content == 'CCC' and header in("Honeywell Material","Honeywell Software") else float(data["totalCost"]) if Quote.GetCustomField('Booking LOB').Content == 'CCC' else int(0)
        newRow_outer["CCC_COST_Booking_Country"] = (float(data["totalWTW"]) if Quote.GetCustomField('Booking LOB').Content == 'CCC' and header in("Honeywell Material","Honeywell Software") else float(data["totalCost"]) if Quote.GetCustomField('Booking LOB').Content == 'CCC' else int(0))*currencyFactor
        if str(data["totalSell"]) not in ('0','0.00','0.0'):
            newRow_outer["CCC_Margin"] = ((float(data["totalSell"]) - float(float(data["totalWTW"]) if Quote.GetCustomField('Booking LOB').Content == 'CCC' and header in("Honeywell Material","Honeywell Software") else float(data["totalCost"]) if Quote.GetCustomField('Booking LOB').Content == 'CCC' else int(0)))/float(data["totalSell"]))*100
        if header == "Honeywell Labor":
            total_hrs,tot_cost,tot_sell=populateLaborRows(quote, srvModulePriceMap,sespBgpDict,plDict)
            if total_hrs:
                newRow_outer["Hrs"] = total_hrs
                continue
            if tot_cost:
                newRow_outer["Cost"] = tot_cost
            if tot_sell:
                newRow_outer["Sell_Price"] = tot_sell
        for pl, plData in data.items():
            if pl == "totalCost" or pl == "totalSell" or pl == "totalWTW":
                continue
            newRow = table.AddNewRow()
            newRow["Product_Line"] = pl
            newRow["Product_Line_Description"] =  str(plData["productLineDesc"])
            newRow["Sell_Price"] = plData["quoteSellPrice"]
            newRow["Cost"] = plData["cost"]
            newRow["Company_Code_Sell"] = float(plData["quoteSellPrice"] * currencyFactor)
            newRow["Company_Code_Cost"] = float(plData["cost"] * currencyFactor)
            newRow["CCC_Standard_Cost"] = float(plData.get("wtw",0)) if Quote.GetCustomField('Booking LOB').Content == 'CCC' and header in("Honeywell Material","Honeywell Software") else float(plData["cost"]) if Quote.GetCustomField('Booking LOB').Content == 'CCC' else int(0)
            newRow["CCC_COST_Booking_Country"] = (float(plData.get("wtw",0)) if Quote.GetCustomField('Booking LOB').Content == 'CCC' and header in("Honeywell Material","Honeywell Software") else float(plData["cost"]) if Quote.GetCustomField('Booking LOB').Content == 'CCC' else int(0))*currencyFactor
            if str(plData["quoteSellPrice"]) not in ('0','0.00','0.0'):
                newRow["CCC_Margin"] = ((float(plData["quoteSellPrice"]) - float(float(plData.get("wtw",0)) if Quote.GetCustomField('Booking LOB').Content == 'CCC' and header in("Honeywell Material","Honeywell Software") else float(plData["cost"]) if Quote.GetCustomField('Booking LOB').Content == 'CCC' else int(0)))/float(plData["quoteSellPrice"]))*100
            newRow["SESP_BGP"] = sespBgpDict.get(pl,"Ignore")
            newRow["SESP_BGP2"] = sespBgpDict.get(pl,"Ignore")
            newRow["China_TP_Discount"] = "Not Discounted" if plData.get("China_S1_Discount",0) in (0,"0", "","N/A") else "Discounted"
            newRow["China_TP_Discount2"] = "Not Discounted" if plData.get("China_S2_Discount",0) in (0,"0", "","N/A") else "Discounted"
            try:
                disCounter = setDiscountIndex(quote)
                disCounter = disCounter if "," in (plData.get("China_S1_Discount","0")) else 0
                discountPer = (plData.get("China_S1_Discount","0").split(",")[disCounter]) if  ((plData.get("China_S1_Discount","0").split(",")[disCounter])) != "N/A" else 0
                newRow["China_TP"] = ((100 - float(discountPer) ) * float(plData["cost"]))/100
            except:
                pass
            try:
                disCounter = setDiscountIndex(quote)
                disCounter = disCounter if "," in (plData.get("China_S2_Discount","0")) else 0
                discountPer = (plData.get("China_S2_Discount","0").split(",")[disCounter]) if  ((plData.get("China_S2_Discount","0").split(",")[disCounter])) != "N/A" else 0
                newRow["China_TP2"] = ((100 - float(discountPer) ) * float(plData["cost"]))/100
            except:
                pass
            pl = pl.Split('-')[0]
            newRow["India_SESP_BGP"] = sespBgpDict.get(pl,"Ignore")
            newRow["India_TP_Discount"] = "Not Discounted" if plData.get("India_Discount_Percent",0) in (0,"0", "","N/A") else "Discounted"
            try:
                newRow["India_TP"] = ((100 - float(plData.get("India_Discount_Percent","0"))) * float(plData["cost"]))/100
                totalIndiaTP +=  float(newRow["India_TP"]) if newRow["India_TP"] not in (0,"0", "","N/A") else 0
                totalChinaTP +=  float(newRow["China_TP"]) if newRow["China_TP"] not in (0,"0", "","N/A") else 0
                totalChinaTP2 +=  float(newRow["China_TP2"]) if newRow["China_TP2"] not in (0,"0", "","N/A") else 0
                subtotalIndiaTP +=  float(newRow["India_TP"]) if newRow["India_TP"] not in (0,"0", "","N/A") else 0
                subtotalChinaTP +=  float(newRow["China_TP"]) if newRow["China_TP"] not in (0,"0", "","N/A") else 0
                subtotalChinaTP2 +=  float(newRow["China_TP2"]) if newRow["China_TP2"] not in (0,"0", "","N/A") else 0
            except:
                pass
        newRow_outer["India_TP"] = subtotalIndiaTP
        newRow_outer["China_TP"] = subtotalChinaTP
        newRow_outer["China_TP2"] = subtotalChinaTP2
    for productType in ptPlMap:
        headerList.append(productType)
    for header in headerList:
        if header not in headerOrder and header != 'Standard Warranty' :
            subtotalIndiaTP,subtotalChinaTP,subtotalChinaTP2 = 0,0,0
            data = ptPlMap.get(header)
            if not data:
                continue
            totalQuoteSellPrice += data["totalSell"]
            totalQuoteCostPrice += data["totalCost"]
            totalQuote_CCC_CostPrice += float(data["totalWTW"]) if Quote.GetCustomField('Booking LOB').Content == 'CCC' and header in("Honeywell Material","Honeywell Software") else float(data["totalCost"]) if Quote.GetCustomField('Booking LOB').Content == 'CCC' else int(0)
            margin = round((data["totalSell"] - data["totalCost"] )/ data["totalSell"] if (data["totalSell"] != 0 and data["totalSell"] != '') else 0, 4)
            newRow_outer = table.AddNewRow()
            newRow_outer["Product_Type"] = header
            newRow_outer["Sell_Price"] = data["totalSell"]
            newRow_outer["Cost"] = data["totalCost"]
            newRow_outer["Margin"] = margin
            newRow_outer["Company_Code_Sell"] = float(data["totalSell"] * currencyFactor)
            newRow_outer["Company_Code_Cost"] = float(data["totalCost"] * currencyFactor)
            newRow_outer["CCC_Standard_Cost"] = float(data["totalWTW"]) if Quote.GetCustomField('Booking LOB').Content == 'CCC' and header in("Honeywell Material","Honeywell Software") else float(data["totalCost"]) if Quote.GetCustomField('Booking LOB').Content == 'CCC' else int(0)
            newRow_outer["CCC_COST_Booking_Country"] = (float(data["totalWTW"]) if Quote.GetCustomField('Booking LOB').Content == 'CCC' and header in("Honeywell Material","Honeywell Software") else float(data["totalCost"]) if Quote.GetCustomField('Booking LOB').Content == 'CCC' else int(0))* currencyFactor
            if str(data["totalSell"]) not in ('0','0.00','0.0'):
                newRow_outer["CCC_Margin"] = ((float(data["totalSell"]) - (float(data["totalWTW"]) if Quote.GetCustomField('Booking LOB').Content == 'CCC' and header in("Honeywell Material","Honeywell Software") else float(data["totalCost"]) if Quote.GetCustomField('Booking LOB').Content == 'CCC' else int(0)))/float(data["totalSell"]))*100
            for pl, plData in data.items():
                if pl == "totalCost" or pl == "totalSell" or pl == "totalWTW":
                    continue
                newRow = table.AddNewRow()
                newRow["Product_Line"] = pl
                newRow["Product_Line_Description"] =  str(plData["productLineDesc"])
                newRow["Sell_Price"] = plData["quoteSellPrice"]
                newRow["Cost"] = plData["cost"]
                newRow["Company_Code_Sell"] = float(plData["quoteSellPrice"] * currencyFactor)
                newRow["Company_Code_Cost"] = float(plData["cost"] * currencyFactor)
                newRow["CCC_Standard_Cost"] = float(plData.get("wtw",0)) if Quote.GetCustomField('Booking LOB').Content == 'CCC' and header in("Honeywell Material","Honeywell Software") else float(plData["cost"]) if Quote.GetCustomField('Booking LOB').Content == 'CCC' else int(0)
                newRow["CCC_COST_Booking_Country"] = (float(plData.get("wtw",0)) if Quote.GetCustomField('Booking LOB').Content == 'CCC' and header in("Honeywell Material","Honeywell Software") else float(plData["cost"]) if Quote.GetCustomField('Booking LOB').Content == 'CCC' else int(0))*currencyFactor
                if str(plData["quoteSellPrice"]) not in ('0','0.00','0.0'):
                    newRow["CCC_Margin"] = ((float(plData["quoteSellPrice"]) - (float(plData.get("wtw",0)) if Quote.GetCustomField('Booking LOB').Content == 'CCC' and header in("Honeywell Material","Honeywell Software") else float(plData["cost"]) if Quote.GetCustomField('Booking LOB').Content == 'CCC' else int(0)))/ float(plData["quoteSellPrice"]))*100
                newRow["SESP_BGP"] = sespBgpDict.get(pl,"Ignore")
                newRow["SESP_BGP2"] = sespBgpDict.get(pl,"Ignore")
                newRow["China_TP_Discount"] = "Not Discounted" if plData.get("China_S1_Discount",0) in (0,"0", "","N/A") else "Discounted"
                newRow["China_TP_Discount2"] = "Not Discounted" if plData.get("China_S2_Discount",0) in (0,"0", "","N/A") else "Discounted"
                try:
                    disCounter = setDiscountIndex(quote)
                    disCounter = disCounter if "," in (plData.get("China_S1_Discount","0")) else 0
                    discountPer = (plData.get("China_S1_Discount","0").split(",")[disCounter]) if ((plData.get("China_S1_Discount","0").split(",")[disCounter])) != "N/A" else 0
                    newRow["China_TP"] = ((100 - float(discountPer) ) * float(plData["cost"]))/100
                except:
                    pass
                try:
                    disCounter = setDiscountIndex(quote)
                    disCounter = disCounter if "," in (plData.get("China_S2_Discount","0")) else 0
                    discountPer = (plData.get("China_S2_Discount","0").split(",")[disCounter]) if ((plData.get("China_S2_Discount","0").split(",")[disCounter])) != "N/A" else 0
                    newRow["China_TP2"] = ((100 - float(discountPer) ) * float(plData["cost"]))/100
                except:
                    pass
                pl = pl.Split('-')[0]
                newRow["India_SESP_BGP"] = sespBgpDict.get(pl,"Ignore")
                newRow["India_TP_Discount"] = "Not Discounted" if plData.get("India_Discount_Percent",0) in (0,"0", "","N/A") else "Discounted"
                try:
                    newRow["India_TP"] = ((100 - float(plData.get("India_Discount_Percent","0"))) * float(plData["cost"]))/100
                    totalIndiaTP +=  float(newRow["India_TP"]) if newRow["India_TP"] not in (0,"0", "","N/A") else 0
                    totalChinaTP +=  float(newRow["China_TP"]) if newRow["China_TP"] not in (0,"0", "","N/A") else 0
                    totalChinaTP2 +=  float(newRow["China_TP2"]) if newRow["China_TP2"] not in (0,"0", "","N/A") else 0
                    subtotalIndiaTP +=  float(newRow["India_TP"]) if newRow["India_TP"] not in (0,"0", "","N/A") else 0
                    subtotalChinaTP +=  float(newRow["China_TP"]) if newRow["China_TP"] not in (0,"0", "","N/A") else 0
                    subtotalChinaTP2 +=  float(newRow["China_TP2"]) if newRow["China_TP2"] not in (0,"0", "","N/A") else 0
                except:
                    pass
            newRow_outer["India_TP"] = subtotalIndiaTP
            newRow_outer["China_TP"] = subtotalChinaTP
            newRow_outer["China_TP2"] = subtotalChinaTP2
    margin_buckets = round((totalQuoteSellPrice - totalQuoteCostPrice  )/ totalQuoteSellPrice if (totalQuoteSellPrice != 0 and totalQuoteSellPrice != '') else 0 , 4)
    newRow = table.AddNewRow()
    header = 'Total(6 Cost Buckets)'
    newRow = table.AddNewRow()
    newRow["Product_Type"] = header
    newRow["Sell_Price"] = totalQuoteSellPrice
    newRow["Cost"] = totalQuoteCostPrice
    newRow["Margin"] = margin_buckets
    newRow["Company_Code_Sell"] = float(totalQuoteSellPrice * currencyFactor)
    newRow["Company_Code_Cost"] = float(totalQuoteCostPrice* currencyFactor)
    newRow["CCC_Standard_Cost"] = float(totalQuote_CCC_CostPrice)
    newRow["CCC_COST_Booking_Country"] = float(totalQuote_CCC_CostPrice* currencyFactor)
    if str(totalQuoteSellPrice) not in ('0','0.00','0.0'):
        newRow["CCC_Margin"] = ((float(totalQuoteSellPrice) - float(totalQuote_CCC_CostPrice))/float(totalQuoteSellPrice)) * 100
    stdWarrantyCost = 0
    margin_sw=0
    newRow = table.AddNewRow()
    for header in ["Standard Warranty"]:
        subtotalIndiaTP,subtotalChinaTP,subtotalChinaTP2 = 0,0,0
        data = ptPlMap.get(header)
        if not data:
            continue
        margin_sw = round((data["totalSell"] - data["totalCost"] )/ data["totalSell"] if (data["totalSell"] != 0 and data["totalSell"] != '') else 0, 4)
        newRow_outer = table.AddNewRow()
        newRow_outer["Product_Type"] = header
        newRow_outer["Sell_Price"] = data["totalSell"]
        newRow_outer["Cost"] = data["totalCost"]
        newRow_outer["Margin"] = margin_sw
        newRow_outer["Company_Code_Sell"] = float(data["totalSell"] * currencyFactor)
        newRow_outer["Company_Code_Cost"] = float(data["totalCost"] * currencyFactor)
        newRow_outer["CCC_Standard_Cost"] = float(data["totalWTW"]) if Quote.GetCustomField('Booking LOB').Content == 'CCC' and header in("Honeywell Material","Honeywell Software") else float(data["totalCost"]) if Quote.GetCustomField('Booking LOB').Content == 'CCC' else int(0)
        newRow_outer["CCC_COST_Booking_Country"] = (float(data["totalWTW"]) if Quote.GetCustomField('Booking LOB').Content == 'CCC' and header in("Honeywell Material","Honeywell Software") else float(data["totalCost"]) if Quote.GetCustomField('Booking LOB').Content == 'CCC' else int(0))* currencyFactor
        if str(data["totalSell"]) not in ('0','0.00','0.0'):
            newRow_outer["CCC_Margin"] = ((float(data["totalSell"]) - (float(data["totalWTW"]) if Quote.GetCustomField('Booking LOB').Content == 'CCC' and header in("Honeywell Material","Honeywell Software") else float(data["totalCost"]) if Quote.GetCustomField('Booking LOB').Content == 'CCC' else int(0)))/float(data["totalSell"]))*100
        for pl, plData in data.items():
            if pl == "totalCost" or pl == "totalSell" or pl == "totalWTW":
                continue
            newRow = table.AddNewRow()
            newRow["Product_Line"] = pl
            newRow["Product_Line_Description"] =  str(plData["productLineDesc"])
            newRow["Sell_Price"] = plData["quoteSellPrice"]
            newRow["Cost"] = plData["cost"]
            newRow["CCC_Standard_Cost"] = plData.get("wtw",0) if Quote.GetCustomField('Booking LOB').Content == 'CCC' and header in("Honeywell Material","Honeywell Software") else plData.get("cost",0) if Quote.GetCustomField('Booking LOB').Content == 'CCC' else int(0)
            newRow["CCC_COST_Booking_Country"] = float(plData.get("wtw",0) if Quote.GetCustomField('Booking LOB').Content == 'CCC' and header in("Honeywell Material","Honeywell Software") else plData.get("cost",0) if Quote.GetCustomField('Booking LOB').Content == 'CCC' else int(0))*100
            if str(plData["quoteSellPrice"]) not in ('0','0.00','0.0'):
                newRow["CCC_Margin"] = ((float(plData["quoteSellPrice"]) - (plData.get("wtw",0) if Quote.GetCustomField('Booking LOB').Content == 'CCC' and header in("Honeywell Material","Honeywell Software") else plData.get("cost",0) if Quote.GetCustomField('Booking LOB').Content == 'CCC' else int(0)))/float(plData["quoteSellPrice"]))*100
            newRow["SESP_BGP"] = sespBgpDict.get(pl,"Ignore")
            newRow["SESP_BGP2"] = sespBgpDict.get(pl,"Ignore")
            newRow["India_SESP_BGP"] = sespBgpDict.get(pl,"Ignore")
            newRow["India_TP"] = ((100 - float(plData.get("India_Discount_Percent","0"))) * float(plData["cost"]))/100
            try:
                disCounter = setDiscountIndex(quote)
                disCounter = disCounter if "," in (plData.get("China_S1_Discount","0")) else 0
                discountPer = (plData.get("China_S1_Discount","0").split(",")[disCounter])  if  ((plData.get("China_S1_Discount","0").split(",")[disCounter])) != "N/A" else 0
                newRow["China_TP"] = ((100 - float(discountPer) ) * float(plData["cost"]))/100
            except:
                pass
            try:
                disCounter = setDiscountIndex(quote)
                disCounter = disCounter if "," in (plData.get("China_S2_Discount","0")) else 0
                discountPer = (plData.get("China_S2_Discount","0").split(",")[disCounter])  if  ((plData.get("China_S2_Discount","0").split(",")[disCounter])) != "N/A" else 0
                newRow["China_TP2"] = ((100 - float(discountPer) ) * float(plData["cost"]))/100
            except:
                pass
            totalIndiaTP +=  float(newRow["India_TP"]) if newRow["India_TP"] not in (0,"0", "","N/A") else 0
            totalChinaTP +=  float(newRow["China_TP"]) if newRow["China_TP"] not in (0,"0", "","N/A") else 0
            totalChinaTP2 +=  float(newRow["China_TP2"]) if newRow["China_TP2"] not in (0,"0", "","N/A") else 0
            subtotalIndiaTP +=  float(newRow["India_TP"]) if newRow["India_TP"] not in (0,"0", "","N/A") else 0
            subtotalChinaTP +=  float(newRow["China_TP"]) if newRow["China_TP"] not in (0,"0", "","N/A") else 0
            subtotalChinaTP2 +=  float(newRow["China_TP2"]) if newRow["China_TP2"] not in (0,"0", "","N/A") else 0
            indiaTPDiscount =  indiaBookingReportData(pl)
            chinaTPDiscount1,chinaTPDiscount2 = chinaBookingReportData(pl)
            newRow["India_TP_Discount"] = "Not Discounted" if indiaTPDiscount in (0,"0", "","N/A") else "Discounted"
            newRow["China_TP_Discount"] = "Not Discounted" if chinaTPDiscount1 in (0,"0", "","N/A") else "Discounted"
            newRow["China_TP_Discount2"] = "Not Discounted" if chinaTPDiscount2 in (0,"0", "","N/A") else "Discounted"
            stdWarrantyCost += float(plData["cost"])
        newRow_outer["India_TP"] = subtotalIndiaTP
        newRow_outer["China_TP"] = subtotalChinaTP
        newRow_outer["China_TP2"] = subtotalChinaTP2
    newRow = table.AddNewRow()
    #margin = round((totalQuoteSellPrice - (totalQuoteCostPrice + stdWarrantyCost) )/ totalQuoteSellPrice if (totalQuoteSellPrice != 0 and totalQuoteSellPrice != '') else 0 , 4)
    header = 'Project Total (Including Standard Warranty & Pre-Sales)'
    newRow = table.AddNewRow()
    newRow["Product_Type"] = header
    if data:
        totalSell=data["totalSell"]
    else:
        totalSell=0
    totalQuoteSellPrice += totalSell
    totalQuoteCostPrice += stdWarrantyCost
    newRow["Sell_Price"] = totalQuoteSellPrice
    newRow["Cost"] = totalQuoteCostPrice
    newRow["CCC_Standard_Cost"] = float(totalQuote_CCC_CostPrice)
    newRow["CCC_COST_Booking_Country"] = float(totalQuote_CCC_CostPrice* currencyFactor)
    if str(totalQuoteSellPrice) not in ('0','0.00','0.0'):
        newRow["CCC_Margin"] = ((float(totalQuoteSellPrice) - float(totalQuote_CCC_CostPrice))/float(totalQuoteSellPrice)) * 100
    margin_total = round((totalQuoteSellPrice - (totalQuoteCostPrice) )/ totalQuoteSellPrice if (totalQuoteSellPrice != 0 and totalQuoteSellPrice != '') else 0 , 4)
    newRow["Margin"] = margin_total
    newRow["Company_Code_Sell"] = float((totalQuoteSellPrice) * currencyFactor)
    newRow["Company_Code_Cost"] = float((totalQuoteCostPrice) * currencyFactor)
    newRow["India_TP"] = float(totalIndiaTP)
    newRow["China_TP"] = float(totalChinaTP)
    newRow["China_TP2"] = float(totalChinaTP2)
    newRow["China_Discounted_TP_Margin"] = float((totalQuoteSellPrice - totalChinaTP )/totalQuoteSellPrice) if (totalQuoteSellPrice != 0 and totalQuoteSellPrice != '') else 0
    newRow["China_Discounted_TP_Margin_2"] = float((totalQuoteSellPrice - totalChinaTP2 )/totalQuoteSellPrice) if (totalQuoteSellPrice != 0 and totalQuoteSellPrice != '') else 0
    newRow["India_Discounted_TP_Margin"] = float((totalQuoteSellPrice -totalIndiaTP )/totalQuoteSellPrice) if (totalQuoteSellPrice != 0 and totalQuoteSellPrice != '') else 0
    table.Save()
totalIndiaTP = 0.00
totalChinaTP = 0.00
totalChinaTP2 = 0.00
groupingKey = "QI_ProductLine" if Quote.GetCustomField('Booking Country').Content not in ['china','india','taiwan','hong kong','India'] else "QI_PLSG"
plDict, ptPlMap, srvModulePriceMap = getProductLineMap(groupingKey)
sespBgpDict = getSespBgpDataDict()
populateQuoteTable(Quote, ptPlMap, srvModulePriceMap, sespBgpDict,plDict)
try:
    getcnt = SqlHelper.GetFirst("select count(PartNumber) as cnt from items where cartID = '"+str(Quote.CompositeNumber)+"'  and PartNumber in ('HCI_EDM','HCI_Labor_config') ")
    if(int(getcnt.cnt) >0):
        ScriptExecutor.Execute('GS_HCI_Firm_and_Budgetary_Report')
except:
    Log.Info("HCI Doc report error ")