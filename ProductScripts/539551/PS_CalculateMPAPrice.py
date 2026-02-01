def getContainer(product,Name):
    return product.GetContainerByName(Name)

def getFloat(Var):
    if Var:
        return float(Var)
    return 0

def getSalesOrg(country):
    query = SqlHelper.GetFirst("select Execution_Country_Sales_Org from EXECUTION_COUNTRY_SALES_ORG_MAPPING where Execution_County = '{}'".format(country))
    if query is not None:
        #Trace.Write("SalesOrg = " + query.Execution_Country_Sales_Org)
        return query.Execution_Country_Sales_Org

def currencyCOnversion(Price):
    quoteCurrency = Quote.SelectedMarket.CurrencyCode
    priceWithConversion = dict()
    if Price:
        for key in Price:
            Trace.Write(Price[key]["stdcurrency"])
            query = SqlHelper.GetFirst("select Exchange_Rate from Currency_ExchangeRate_Mapping where From_Currency = '{}' and To_Currency = '{}'".format(Price[key]["stdcurrency"],quoteCurrency))
            if query is not None:
                priceWithConversion[key] = getFloat(Price[key]["price"]) * getFloat(query.Exchange_Rate)
            else:
                priceWithConversion[key] = getFloat(Price[key]["price"])
    #Trace.Write(str(priceWithConversion))
    return priceWithConversion

def getMPAPrice(salesOrg,partNumber,honeywellRef,totalManHours):
    mpaPrice = dict()
    if honeywellRef == "1-CUN51UZ":
        query = "SELECT Unit_MPA_Price,Currency,Service_Material FROM GES_MPA_PRICE WHERE SalesOrg = '{0}' and cast(Minimum_MH as float) <= {1} and cast(Maximum_MH as float)> {2} and  Service_Material = '{3}'  and HoneywellRef = '1-CUN51UZ'".format(salesOrg,totalManHours,totalManHours,partNumber)
        res = SqlHelper.GetFirst(query)
        if res is not None and res.Unit_MPA_Price:
            mpaPrice[res.Service_Material] = {"price": res.Unit_MPA_Price,"stdcurrency": res.Currency}
        Trace.Write(str(mpaPrice))
        unitMPAPrice = currencyCOnversion(mpaPrice)
        if partNumber in unitMPAPrice and unitMPAPrice[partNumber]:
            return getFloat(unitMPAPrice[partNumber])
        return 0
    elif honeywellRef == "1-E2E9KXP":
        query = "SELECT Unit_MPA_Price,Currency,Service_Material FROM GES_MPA_PRICE WHERE SalesOrg = '{0}' and  Service_Material = '{1}' and HoneywellRef = '1-E2E9KXP'".format(salesOrg,partNumber)
        res = SqlHelper.GetFirst(query)
        if res is not None and res.Unit_MPA_Price:
            mpaPrice[res.Service_Material] = {"price": res.Unit_MPA_Price,"stdcurrency": res.Currency}
        Trace.Write(str(mpaPrice))
        unitMPAPrice = currencyCOnversion(mpaPrice)
        if partNumber in unitMPAPrice and unitMPAPrice[partNumber]:
            return getFloat(unitMPAPrice[partNumber])
        return 0
    elif honeywellRef == "1-AG39TBN":
        query = "SELECT Unit_MPA_Price,Currency,Service_Material FROM GES_MPA_PRICE WHERE SalesOrg = '{0}' and  Service_Material = '{1}' and HoneywellRef = '1-AG39TBN'".format(salesOrg,partNumber)
        res = SqlHelper.GetFirst(query)
        if res is not None and res.Unit_MPA_Price:
            mpaPrice[res.Service_Material] = {"price": res.Unit_MPA_Price,"stdcurrency": res.Currency}
        Trace.Write(str(mpaPrice))
        unitMPAPrice = currencyCOnversion(mpaPrice)
        if partNumber in unitMPAPrice and unitMPAPrice[partNumber]:
            return getFloat(unitMPAPrice[partNumber])
        return 0

def populateMPAPrice(row):
    if row["GES_Eng_Percentage_Split"] not in ('0.00','') and row["Final_Hrs"] not in ('','0'):
        Trace.Write("inside")
        salesOrg = getSalesOrg(row["Execution_Country"])
        gesMPAPrice = getMPAPrice(salesOrg,row["GES_Eng"],honeywellRef,totalManHours)
        Trace.Write("gesMPAPrice-->"+str(gesMPAPrice))
        if gesMPAPrice:
            MPAPrice = round(getFloat(gesMPAPrice),2)
            gesFinalHours = round(getFloat(row["Final_Hrs"]) * getFloat(row["GES_Eng_Percentage_Split"]) / 100)
            row["GES_MPA_Price"] = str(MPAPrice * gesFinalHours)
        else:
            row["GES_MPA_Price"] = "0"
    else:
        row["GES_MPA_Price"] = "0"
    if row["FO_Eng_Percentage_Split"] not in ('0.00','') and row["Final_Hrs"] not in ('','0'):
        salesOrg = getSalesOrg(row["Execution_Country"])
        foMPAPrice = getMPAPrice(salesOrg,row["FO_Eng"],honeywellRef,totalManHours)
        Trace.Write("foMPAPrice----->"+str(foMPAPrice))
        if foMPAPrice:
            MPAPrice = round(getFloat(foMPAPrice),2)
            foFinalHours = round(getFloat(row["Final_Hrs"]) * getFloat(row["FO_Eng_Percentage_Split"]) / 100)
            row["FO_MPA_Price"] = str(MPAPrice * foFinalHours)
        else:
            row["FO_MPA_Price"] = "0"
    else:
        row["FO_MPA_Price"] = "0"

honeywellRef = Quote.GetCustomField('MPA Honeywell Ref').Content
#honeywellRef = "1-CUN51UZ"
containers = ['MSID_Labor_OPM_Engineering','MSID_Labor_LCN_One_Time_Upgrade_Engineering','MSID_Labor_EBR_Con','MSID_Labor_ELCN_Con','MSID_Labor_Orion_Console_Con','MSID_Labor_EHPM_C300PM_Con','MSID_Labor_TPS_TO_EXPERION_Con','MSID_Labor_TCMI_Con','MSID_Labor_EHPM_HART_IO_Con','MSID_Labor_C200_Migration_Con','MSID_Labor_CB-EC_Upgrade_to_C300-UHIO_con','MSID_Labor_xPM_to_C300_Migration_Con','MSID_Labor_FDM_Upgrade_Con','MSID_Labor_FSC_to_SM_con','MSID_Labor_FSC_to_SM_audit_Con','MSID_Labor_LM_to_ELMM_Con','MSID_Labor_XP10_Actuator_Upgrade_con','MSID_Labor_Graphics_Migration_con','MSID_Labor_CD_Actuator_con','MSID_Labor_FSCtoSM_IO_con','3rd_Party_PLC_UOC_Labor','MSID_Labor_Project_Management','MSID_Labor_CWS_RAE_Upgrade_con','MSID_Labor_Virtualization_con','MSID_Labor_QCS_RAE_Upgrade_con','MSID_Labor_TPA_con','MSID_Labor_FSC_to_SM_IO_Audit_Con','MSID_Labor_Generic_System1_Cont','MSID_Labor_Generic_System2_Cont','MSID_Labor_Generic_System3_Cont','MSID_Labor_Generic_System4_Cont','MSID_Labor_Generic_System5_Cont','MSID_Labor_ELEPIU_con']
totalManHours = 0

msidContainer = Product.GetContainerByName("CONT_Migration_MSID_Selection")
if msidContainer:
    for row in msidContainer.Rows:
        msidProduct = row.Product
        for container in containers:
            for row in getContainer(msidProduct,container).Rows:
                if row["Deliverable"] == 'Total':
                    totalManHours = totalManHours + float(row['Final_Hrs'])
                    break
        Trace.Write("totalManHours--->"+str(totalManHours))
#totalManHours = 500
#containers = ['MSID_Labor_OPM_Engineering','MSID_Labor_LCN_One_Time_Upgrade_Engineering','MSID_Labor_Project_Management','MSID_Additional_Custom_Deliverables']

msidContainer = Product.GetContainerByName("CONT_Migration_MSID_Selection")
if msidContainer:
    for Row in msidContainer.Rows:
        msidProduct = Row.Product
        for container in containers:
            for row in getContainer(msidProduct,container).Rows:
                if row["Deliverable"] not in ('Total','Off-Site','On-Site'):
                    populateMPAPrice(row)
                getContainer(msidProduct,container).Calculate()