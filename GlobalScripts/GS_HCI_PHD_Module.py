from System import DateTime
integrationTestingLst=['Install and Configure Software','Configure and load PHD tag definitions','Configure/setup RDIs','Configure ERP and other interfaces','Define and test virtual tag calculations','Define user profiles and tag security','Implement TagSync','Configure USM Software','Configure USM Monitor Items','Configure USM Condition Items','Configure USM Historised Monitor Items','Test RDIs and tag collection, correct errors','Internal application integration testing']
def copyDeliverable(cont,ChangedCell):
    for row in cont.Rows:
        if row.RowIndex==ChangedCell.RowIndex:
            row['Hidden_lable']=str(ChangedCell.NewValue)
def additiolDeliverableTotal(cont):
    finalHrs=0
    for row in cont.Rows:
        if row['Hidden_lable']!='Total':
            finalHrs+=float(row['Final Hrs'])
        else:
            row['Final Hrs']=str(finalHrs)
            row.Calculate()

def negValChec(cont,ChangedCell):
    for row in cont.Rows:
        if row.RowIndex==ChangedCell.RowIndex:
            row[ChangedCell.ColumnName]=str(ChangedCell.OldValue)

def getCurrencyFactor(fromCurr,toCurr):
    query = SqlHelper.GetFirst("select Exchange_Rate from Currency_ExchangeRate_Mapping where From_Currency = '{}' and To_Currency = '{}'".format(fromCurr,toCurr))
    factor=1
    if query:
        factor=query.Exchange_Rate
    return factor

def getECSalesOrg(Execution_County):
    salesorg_details = SqlHelper.GetFirst("SELECT Execution_Country_Sales_Org, Currency FROM NEW_EXECUTION_COUNTRY_SALES_ORG_MAPPING WHERE Execution_County = '{}'".format(Execution_County))
    return salesorg_details.Execution_Country_Sales_Org if salesorg_details else "1109"

def getLaborCost(Execution_Country,partNumber,executionYear,quoteCurreny):
    cost=0
    Execution_Country_Sales_Org=getECSalesOrg(Execution_Country) if Execution_Country!='' else ''
    res = SqlHelper.GetFirst("Select Cost_CurrentMonth_Year1,Cost_CurrentMonth_Year2,Cost_CurrentMonth_Year3,Cost_CurrentMonth_Year4,Cost_Currency_Code from HPS_LABOR_COST_DATA where Sales_Org = '{0}' and Part_Number in ('{1}')".format(Execution_Country_Sales_Org,partNumber))
    if res:
        if executionYear == str(DateTime.Now.Year):
            cost=res.Cost_CurrentMonth_Year1
        elif executionYear == str(DateTime.Now.Year + 1):
            cost=res.Cost_CurrentMonth_Year2
        elif executionYear == str(DateTime.Now.Year + 2):
            cost=res.Cost_CurrentMonth_Year3
        elif executionYear == str(DateTime.Now.Year + 3):
            cost=res.Cost_CurrentMonth_Year4
        factor=getCurrencyFactor(res.Cost_Currency_Code,quoteCurreny)
        cost=cost*float(factor)
    return cost
    
def getInflationRate(salesOrg,lob):
    query = "Select * from YOY_INFLATION_RATE where salesOrg = '{0}' and LOB = '{1}'".format(salesOrg,lob)
    res = SqlHelper.GetFirst(query)
    return res


def getCalculateListPrice(salesOrg,listPrice,executionYear):
    res = (getInflationRate(salesOrg,'HCI'))
    price=0
    if res is not None:
        inflationRate = res.Inflation_Rate
        inflationRate2 = res.Inflation_Rate_Year2
        inflationRate3 = res.Inflation_Rate_Year3
    else:
        inflationRate = 0.0
        inflationRate2 = 0.0
        inflationRate3 = 0.0
    if executionYear == str(DateTime.Now.Year):
        price=listPrice
    elif executionYear == str(DateTime.Now.Year + 1):
        price=listPrice*(1+float(inflationRate))
    elif executionYear == str(DateTime.Now.Year + 2):
        price=listPrice*(1+float(inflationRate))*(1+float(inflationRate2))
    elif executionYear == str(DateTime.Now.Year + 3):
        price=listPrice*(1+float(inflationRate))*(1+float(inflationRate2))*(1+float(inflationRate3))
    if price:
        return price
    return 0
    
def getEACCost(partNumber,currency):
    res = SqlHelper.GetFirst("Select EAC_Value,Currency from Labor_GES_EAC_Value where GES_Service_Material = '{}'".format(partNumber))
    EACCost = float(res.EAC_Value) if res else 0
    EACCurr = res.Currency if res else currency
    currFactor = getCurrencyFactor(EACCurr,currency)
    EACCost= EACCost *float(currFactor)
    return EACCost

def getW2WFactor(partNumber):
    getW2WFactor = SqlHelper.GetFirst("SELECT WTWMarkupFactorEstimated,GES_Service_Material FROM Labor_GES_WTW_Markup_Factor where GES_Service_Material='{}' ".format(partNumber))
    W2WFactor=getW2WFactor.WTWMarkupFactorEstimated if getW2WFactor else 0
    return float(W2WFactor)