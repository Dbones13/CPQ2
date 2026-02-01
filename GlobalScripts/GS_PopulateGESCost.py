from System import DateTime
Product = Product

def getContainer(Name):
    return Product.GetContainerByName(Name)

def getCfValue(Name):
    return Quote.GetCustomField(Name).Content

def setAttrValue(Name,value):
    Product.Attr(Name).AssignValue(value)

def getFloat(Var):
    if Var:
        return float(Var)
    return 0

def getDefaultExecutionYear():
    executionYear = str(DateTime.Now.Year)
    yearsList = []
    currentYear = DateTime.Now.Year
    i = 0
    while i < 4:
        year = currentYear + i
        yearsList.append(year)
        i += 1
    #Trace.Write(str(yearsList))
    if getCfValue("EGAP_Contract_Start_Date") != '':
        year = UserPersonalizationHelper.CovertToDate(getCfValue("EGAP_Contract_Start_Date")).Year
        if year in yearsList:
            executionYear = year
        else:
            executionYear = yearsList[-1] if len(yearsList) > 0 else str(DateTime.Now.Year)
    return executionYear

def setproductMessage(material,deliverable,cost,listPrice):
    if cost:
        setAttrValue("Product_Message","Part Number '{0}' is not allowed due to missing Cost for the deliverable '{1}'".format(material,deliverable))
    if listPrice:
        setAttrValue("Product_Message","Part Number '{0}' is not allowed due to missing List Price for the deliverable '{1}'".format(material,deliverable))

def checkCostAndPrice(container):
    productIncomplete = False
    for row in getContainer(container).Rows:
        setAttrValue("Incomplete_Flag","")
        cost = False
        listPrice = False
        if row["GES_Eng_Percentage_Split"] not in ('0','') and row["Final_Hrs"] not in ('','0.0'):
            if row["GES_Regional_Cost"] in ('0',''):
                cost = True
                setproductMessage(row["GES_Eng"],row["Deliverable"],cost,listPrice)
                setAttrValue("Incomplete_Flag","1")
                productIncomplete = True
                return productIncomplete
            if row["GES_ListPrice"] in ('0',''):
                listPrice = True
                setproductMessage(row["GES_Eng"],row["Deliverable"],cost,listPrice)
                setAttrValue("Incomplete_Flag","1")
                productIncomplete = True
                return productIncomplete
        if row["FO_Eng_Percentage_Split"] not in ('0','') and row["Final_Hrs"] not in ('','0.0'):
            if row["Regional_Cost"] in ('0',''):
                cost = True
                setproductMessage(row["FO_Eng"],row["Deliverable"],cost,listPrice)
                setAttrValue("Incomplete_Flag","1")
                productIncomplete = True
                return productIncomplete
            if row["FO_ListPrice"] in ('0',''):
                listPrice = True
                setproductMessage(row["FO_Eng"],row["Deliverable"],cost,listPrice)
                setAttrValue("Incomplete_Flag","1")
                productIncomplete = True
                return productIncomplete
    return productIncomplete


def getPartsCost():
    partsCost = dict()
    foPartNumberCon = getContainer("MSID_Labor_FO_Part_Number")
    for row in foPartNumberCon.Rows:
        if row["GES_Part_Number"]:
            partsCost[row["GES_Part_Number"]] = row["Cost"]
        else:
            partsCost[row["FO_Part_Number"]] = row["Cost"]
    #Trace.Write(str(partsCost))
    return partsCost

def getPartsListPrice():
    partsListPrice = dict()
    foPartNumberCon = getContainer("MSID_Labor_FO_Part_Number")
    for row in foPartNumberCon.Rows:
        if row["GES_Part_Number"]:
            partsListPrice[row["GES_Part_Number"]] = row["ListPrice"]
        else:
            partsListPrice[row["FO_Part_Number"]] = row["ListPrice"]
    #Trace.Write(str(partsListPrice))
    return partsListPrice

def getExecutionCountry():
    marketCode = Quote.SelectedMarket.MarketCode
    salesOrg = Quote.GetCustomField('Sales Area').Content
    #query = SqlHelper.GetFirst("select Execution_County from EXECUTION_COUNTRY_SALES_ORG_MAPPING where Execution_Country_Sales_Org = '{}'".format(salesOrg))
    #Update for Defect CXCPQ-27359
    currency = Quote.GetCustomField('Currency').Content
    query = SqlHelper.GetFirst("select Execution_County from NEW_EXECUTION_COUNTRY_SALES_ORG_MAPPING where Sales_Area = '{}' and Currency = '{}'".format(salesOrg,currency))
    if query is not None:
        return query.Execution_County

def getSalesOrg(country):
    query = SqlHelper.GetFirst("select Execution_Country_Sales_Org from EXECUTION_COUNTRY_SALES_ORG_MAPPING where Execution_County = '{}'".format(country))
    if query is not None:
        #Trace.Write("SalesOrg = " + query.Execution_Country_Sales_Org)
        return query.Execution_Country_Sales_Org

def getInflationRate(salesOrg):
    LOB = Quote.GetCustomField("Booking LOB").Content
    query = "Select * from YOY_INFLATION_RATE where salesOrg = '{0}' and LOB = '{1}'".format(salesOrg,LOB)
    res = SqlHelper.GetFirst(query)
    return res

def getCalculateListPrice(power,partnumber):
    salesOrg = Quote.GetCustomField("Sales Area").Content
    res = (getInflationRate(salesOrg))
    price = getFloat(partsListPrice.get(partnumber,0))
    if power == 1 and res is not None:
        inflationRate1 = res.Inflation_Rate
        price = (getFloat(partsListPrice.get(partnumber,0)) * getFloat((1 + inflationRate1 )))
    elif power == 2 and res is not None:
        inflationRate1 = res.Inflation_Rate
        inflationRate2 = res.Inflation_Rate_Year2
        price = (getFloat(partsListPrice.get(partnumber,0)) * getFloat((1 + inflationRate1 ))* getFloat((1 + inflationRate2 )))
    elif power == 2 and res is not None:
        inflationRate1 = res.Inflation_Rate
        inflationRate2 = res.Inflation_Rate_Year2
        inflationRate3 = res.Inflation_Rate_Year3
        price = (getFloat(partsListPrice.get(partnumber,0)) * getFloat((1 + inflationRate1 ))* getFloat((1 + inflationRate2 ))* getFloat((1 + inflationRate3 )))
    if price:
        return price
    return 0

def laborCostWithCOnversion(laborcostParts):
    quoteCurrency = Quote.SelectedMarket.CurrencyCode
    costWithConversion = dict()
    if laborcostParts:
        for key in laborcostParts:
            Trace.Write(laborcostParts[key]["stdcurrency"])
            query = SqlHelper.GetFirst("select Exchange_Rate from Currency_ExchangeRate_Mapping where From_Currency = '{}' and To_Currency = '{}'".format(laborcostParts[key]["stdcurrency"],quoteCurrency))
            if query is not None:
                costWithConversion[key] = getFloat(laborcostParts[key]["cost"]) * getFloat(query.Exchange_Rate)
            else:
                factor = 1.00
                query1 = SqlHelper.GetFirst("select Exchange_Rate from Currency_ExchangeRate_Mapping where From_Currency = '{}' and To_Currency = '{}'".format(laborcostParts[key]["stdcurrency"],'USD'))
                if query1 is not None:
                    factor = factor * getFloat(query1.Exchange_Rate)
                    queryUSD = SqlHelper.GetFirst("select Exchange_Rate from Currency_ExchangeRate_Mapping where From_Currency = '{}' and To_Currency = '{}'".format('USD',quoteCurrency))
                    if queryUSD is not None:
                        factor = factor * getFloat(queryUSD.Exchange_Rate)
                    else:
                        factor = 1.00
                costWithConversion[key] = getFloat(laborcostParts[key]["cost"]) * factor
    #Trace.Write("cost conversion")
    #Trace.Write(str(costWithConversion))
    return costWithConversion

def getFopartsCost(salesOrg,partNumber,executionYear):
    query = "Select * from HPS_LABOR_COST_DATA where Sales_Org = '{0}' and Part_Number in ('{1}')".format(salesOrg,partNumber)
    res = SqlHelper.GetList(query)
    foCost = dict()
    for i in res:
        if executionYear == str(DateTime.Now.Year):
            foCost[i.Part_Number] = {"cost":i.Cost_CurrentMonth_Year1,"stdcurrency":i.Cost_Currency_Code}
        elif executionYear == str(DateTime.Now.Year + 1):
            foCost[i.Part_Number] = {"cost":i.Cost_CurrentMonth_Year2,"stdcurrency":i.Cost_Currency_Code}
        elif executionYear == str(DateTime.Now.Year + 2):
            foCost[i.Part_Number] = {"cost":i.Cost_CurrentMonth_Year3,"stdcurrency":i.Cost_Currency_Code}
        elif executionYear == str(DateTime.Now.Year + 3):
            foCost[i.Part_Number] = {"cost":i.Cost_CurrentMonth_Year4,"stdcurrency":i.Cost_Currency_Code}
    Trace.Write(str(foCost))
    foCostWithConversion = laborCostWithCOnversion(foCost)
    return foCostWithConversion

def getTPandEACValueSapParts(salesOrg,partNumber,executionYear):
    query = "Select lc.*,eac.EAC_Value,eac.Currency from HPS_LABOR_COST_DATA lc join Labor_GES_EAC_Value eac on lc.Part_Number = eac.GES_Service_Material where Sales_Org = '{0}' and Part_Number in ('{1}')".format(salesOrg, partNumber)
    res = SqlHelper.GetList(query)
    gesTP = dict()
    gesEAC = dict()
    for i in res:
        if executionYear == str(DateTime.Now.Year):
            gesTP[i.Part_Number] = {"cost":i.Cost_CurrentMonth_Year1,"stdcurrency":i.Cost_Currency_Code}
            gesEAC[i.Part_Number] = {"cost":i.EAC_Value,"stdcurrency":i.Currency}
        elif executionYear == str(DateTime.Now.Year + 1):
            gesTP[i.Part_Number] = {"cost":i.Cost_CurrentMonth_Year2,"stdcurrency":i.Cost_Currency_Code}
            gesEAC[i.Part_Number] = {"cost":i.EAC_Value,"stdcurrency":i.Currency}
        elif executionYear == str(DateTime.Now.Year + 2):
            gesTP[i.Part_Number] = {"cost":i.Cost_CurrentMonth_Year3,"stdcurrency":i.Cost_Currency_Code}
            gesEAC[i.Part_Number] = {"cost":i.EAC_Value,"stdcurrency":i.Currency}
        elif executionYear == str(DateTime.Now.Year + 3):
            gesTP[i.Part_Number] = {"cost":i.Cost_CurrentMonth_Year4,"stdcurrency":i.Cost_Currency_Code}
            gesEAC[i.Part_Number] = {"cost":i.EAC_Value,"stdcurrency":i.Currency}
    #Trace.Write(str(gesTP))
    #Trace.Write(str(gesEAC))
    tpWithConversion = laborCostWithCOnversion(gesTP)
    eacWithConversion = laborCostWithCOnversion(gesEAC)
    return tpWithConversion,eacWithConversion

def getTPandEACValueNonSapParts(partNumber,executionYear):
    query = "Select lc.*,eac.EAC_Value,eac.Currency from HPS_LABOR_COST_DATA lc join Labor_GES_EAC_Value eac on lc.Part_Number = eac.GES_Service_Material where Sales_Org = '' and Part_Number in ('{}')".format(partNumber)
    res = SqlHelper.GetList(query)
    gesTP = dict()
    gesEAC = dict()
    for i in res:
        if executionYear == str(DateTime.Now.Year):
            gesTP[i.Part_Number] = {"cost":i.Cost_CurrentMonth_Year1,"stdcurrency":i.Cost_Currency_Code}
            gesEAC[i.Part_Number] = {"cost":i.EAC_Value,"stdcurrency":i.Currency}
        elif executionYear == str(DateTime.Now.Year + 1):
            gesTP[i.Part_Number] = {"cost":i.Cost_CurrentMonth_Year2,"stdcurrency":i.Cost_Currency_Code}
            gesEAC[i.Part_Number] = {"cost":i.EAC_Value,"stdcurrency":i.Currency}
        elif executionYear == str(DateTime.Now.Year + 2):
            gesTP[i.Part_Number] = {"cost":i.Cost_CurrentMonth_Year3,"stdcurrency":i.Cost_Currency_Code}
            gesEAC[i.Part_Number] = {"cost":i.EAC_Value,"stdcurrency":i.Currency}
        elif executionYear == str(DateTime.Now.Year + 3):
            Trace.Write("non sap 2025")
            gesTP[i.Part_Number] = {"cost":i.Cost_CurrentMonth_Year4,"stdcurrency":i.Cost_Currency_Code}
            gesEAC[i.Part_Number] = {"cost":i.EAC_Value,"stdcurrency":i.Currency}

    #Trace.Write(str(gesTP))
    #Trace.Write(str(gesEAC))
    tpWithConversion = laborCostWithCOnversion(gesTP)
    eacWithConversion = laborCostWithCOnversion(gesEAC)
    return tpWithConversion,eacWithConversion

def populateGESCost(row,defaultExecutionYear):
    if row["GES_Eng_Percentage_Split"] not in ('0','') and row["Final_Hrs"] not in ('','0.0'):
        if row["Execution_Country"] == excecutionCountry and row["Execution_Year"] == defaultExecutionYear:
            regionalCost = round(getFloat(partsCost.get(row["GES_Eng"],0)),2)
            gesFinalHours = round(getFloat(row["Final_Hrs"]) * getFloat(row["GES_Eng_Percentage_Split"]) / 100)
            row["GES_Regional_Cost"] = str(regionalCost * gesFinalHours)
        else:
            if row["GES_Eng"].endswith("_CN") or row["GES_Eng"].endswith("_UZ"):
                gesTPSap,gesEAC1Sap = getTPandEACValueNonSapParts(row["GES_Eng"],row["Execution_Year"])
                #Trace.Write(str(gesTPSap))
                #Trace.Write(str(gesEAC1Sap))
                if row["GES_Eng"] in gesTPSap and gesTPSap[row["GES_Eng"]]:
                    regionalCost = getFloat(gesTPSap.get(row["GES_Eng"],0)) + getFloat(gesEAC1Sap.get(row["GES_Eng"],0))
                    gesFinalHours = round(getFloat(row["Final_Hrs"]) * getFloat(row["GES_Eng_Percentage_Split"]) / 100)
                    row["GES_Regional_Cost"] = str(round(regionalCost,2) * gesFinalHours)
                else:
                    row["GES_Regional_Cost"] = "0"
            elif row["GES_Eng"].endswith("_IN") or row["GES_Eng"].endswith("_RO"):
                #Trace.Write("country same year change IN")
                salesOrg = getSalesOrg(row["Execution_Country"])
                #Trace.Write("salesOrg = " + str(salesOrg))
                gesTPSap,gesEAC1Sap = getTPandEACValueSapParts(salesOrg,row["GES_Eng"],row["Execution_Year"])
                #Trace.Write(str(gesTPSap))
                #Trace.Write(str(gesEAC1Sap))
                if row["GES_Eng"] in gesTPSap and gesTPSap[row["GES_Eng"]]:
                    regionalCost = getFloat(gesTPSap.get(row["GES_Eng"],0)) + getFloat(gesEAC1Sap.get(row["GES_Eng"],0))
                    gesFinalHours = round(getFloat(row["Final_Hrs"]) * getFloat(row["GES_Eng_Percentage_Split"]) / 100)
                    row["GES_Regional_Cost"] = str(round(regionalCost,2) * gesFinalHours)
                else:
                    row["GES_Regional_Cost"] = "0"
    else:
        row["GES_Regional_Cost"] = "0"
    if row["FO_Eng_Percentage_Split"] not in ('0','') and row["Final_Hrs"] not in ('','0.0'):
        if row["Execution_Country"] == bookingCountry:
            if row["Execution_Year"] == defaultExecutionYear:
                regionalCost = round(getFloat(partsCost.get(row["FO_Eng"],0)),2)
                foFinalHours = round(getFloat(row["Final_Hrs"]) * getFloat(row["FO_Eng_Percentage_Split"]) / 100)
                row["Regional_Cost"] = str(regionalCost * foFinalHours)
                row["FOUnitWTWCost"] = str(row["Regional_Cost"])
            else:
                salesOrg = getSalesOrg(row["Execution_Country"])
                foPartsCost = getFopartsCost(salesOrg,row["FO_Eng"],row["Execution_Year"])
                Trace.Write(str(foPartsCost))
                if row["FO_Eng"] in foPartsCost and foPartsCost[row["FO_Eng"]]:
                    regionalCost = round(getFloat(foPartsCost.get(row["FO_Eng"],0)),2)
                    foFinalHours = round(getFloat(row["Final_Hrs"]) * getFloat(row["FO_Eng_Percentage_Split"]) / 100)
                    row["Regional_Cost"] = str(regionalCost * foFinalHours)
                    row["FOUnitWTWCost"] = str(row["Regional_Cost"])
                else:
                    row["Regional_Cost"] = "0"
                    row["FOUnitWTWCost"] = "0"
        else:
            salesOrg = getSalesOrg(row["Execution_Country"])
            foPartsCost = getFopartsCost(salesOrg,row["FO_Eng"],row["Execution_Year"])
            Trace.Write(str(foPartsCost))
            if row["FO_Eng"] in foPartsCost and foPartsCost[row["FO_Eng"]]:
                regionalCost = round(getFloat(foPartsCost.get(row["FO_Eng"],0)),2) + ((round(getFloat(foPartsCost.get(row["FO_Eng"],0)),2) * 10) / 100)
                foFinalHours = round(( getFloat(row["Final_Hrs"]) * getFloat(row["FO_Eng_Percentage_Split"]) / 100))
                #Trace.Write("regionalCost = " + str(regionalCost))
                row["Regional_Cost"] = str(regionalCost * foFinalHours)
                row["FOUnitWTWCost"] = str(getFloat(row["Regional_Cost"]) / (1 + 0.1))
            else:
                row["Regional_Cost"] = "0"
                row["FOUnitWTWCost"] = "0"
    else:
        row["Regional_Cost"] = "0"
        row["FOUnitWTWCost"] = "0"

def populateGESListPrice(row):
    if row["GES_Eng_Percentage_Split"] not in ('0','') and row["Final_Hrs"] not in ('','0.0'):
        if row["Execution_Year"] == str(DateTime.Now.Year):
            #Trace.Write("check")
            row["GES_ListPrice"] = str(round(getFloat(partsListPrice.get(row["GES_Eng"],0)),2) * round(getFloat(row["Final_Hrs"]) * getFloat(row["GES_Eng_Percentage_Split"]) / 100))
        elif row["Execution_Year"] == str(DateTime.Now.Year + 1):
            power = 1
            row["GES_ListPrice"] = str(round(getCalculateListPrice(power,row["GES_Eng"]),2) * round(getFloat(row["Final_Hrs"]) * getFloat(row["GES_Eng_Percentage_Split"]) / 100))
        elif row["Execution_Year"] == str(DateTime.Now.Year + 2):
            power = 2
            row["GES_ListPrice"] = str(round(getCalculateListPrice(power,row["GES_Eng"]),2) * round(getFloat(row["Final_Hrs"]) * getFloat(row["GES_Eng_Percentage_Split"]) / 100))
        elif row["Execution_Year"] == str(DateTime.Now.Year + 3):
            power = 3
            row["GES_ListPrice"] = str(round(getCalculateListPrice(power,row["GES_Eng"]),2) * round(getFloat(row["Final_Hrs"]) * getFloat(row["GES_Eng_Percentage_Split"]) / 100))
    else:
        row["GES_ListPrice"] = "0"
    if row["FO_Eng_Percentage_Split"] not in ('0','') and row["Final_Hrs"] not in ('','0.0'):
        if row["Execution_Year"] == str(DateTime.Now.Year):
            row["FO_ListPrice"] = str(round(getFloat(partsListPrice.get(row["FO_Eng"],0)),2) * round(( getFloat(row["Final_Hrs"]) * getFloat(row["FO_Eng_Percentage_Split"]) / 100)) )
        elif row["Execution_Year"] == str(DateTime.Now.Year + 1):
            power = 1
            row["FO_ListPrice"] = str(round(getCalculateListPrice(power,row["FO_Eng"]),2) * round(getFloat(row["Final_Hrs"]) * getFloat(row["FO_Eng_Percentage_Split"]) / 100))
        elif row["Execution_Year"] == str(DateTime.Now.Year + 2):
            power = 2
            row["FO_ListPrice"] = str(round(getCalculateListPrice(power,row["FO_Eng"]),2) * round(getFloat(row["Final_Hrs"]) * getFloat(row["FO_Eng_Percentage_Split"]) / 100))
        elif row["Execution_Year"] == str(DateTime.Now.Year + 3):
            power = 3
            row["FO_ListPrice"] = str(round(getCalculateListPrice(power,row["FO_Eng"]),2) * round(getFloat(row["Final_Hrs"]) * getFloat(row["FO_Eng_Percentage_Split"]) / 100))
    else:
        row["FO_ListPrice"] = "0"

partsListPrice = getPartsListPrice()
#Trace.Write(str(partsListPrice))
excecutionCountry = getExecutionCountry()
bookingCountry = getCfValue("Booking Country").title()
defaultExecutionYear = str(getDefaultExecutionYear())
partsCost = getPartsCost()

containers = ['MSID_Labor_OPM_Engineering','MSID_Labor_LCN_One_Time_Upgrade_Engineering','MSID_Labor_EBR_Con','MSID_Labor_ELCN_Con','MSID_Labor_Orion_Console_Con','MSID_Labor_EHPM_C300PM_Con','MSID_Labor_TPS_TO_EXPERION_Con','MSID_Labor_TCMI_Con','MSID_Labor_Project_Management','MSID_Additional_Custom_Deliverables','MSID_Labor_FDM_Upgrade_Con','MSID_Labor_EHPM_HART_IO_Con', 'MSID_Labor_C200_Migration_Con','MSID_Labor_CB-EC_Upgrade_to_C300-UHIO_con','MSID_Labor_FSC_to_SM_con','MSID_Labor_FSC_to_SM_audit_Con','MSID_Labor_xPM_to_C300_Migration_Con','MSID_Labor_LM_to_ELMM_Con','MSID_Labor_XP10_Actuator_Upgrade_con','MSID_Labor_Graphics_Migration_con','MSID_Labor_CD_Actuator_con','MSID_Labor_ELEPIU_con']

for container in containers:
    for row in getContainer(container).Rows:
        if row["Deliverable"] not in ('Total','Off-Site','On-Site'):
            populateGESListPrice(row)
            populateGESCost(row,defaultExecutionYear)
        getContainer(container).Calculate()

for container in containers:
    if container != "MSID_Additional_Custom_Deliverables":
        productIncomplete = checkCostAndPrice(container)
        if productIncomplete:
            break