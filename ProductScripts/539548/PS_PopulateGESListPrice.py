def getContainer(Name):
    return Product.GetContainerByName(Name)

def getFloat(Var):
    if Var:
        return float(Var)
    return 0

def getGESListPrice():
    gespartslistPrice = dict()
    foPartNumberCon = getContainer("MSID_Labor_FO_Part_Number")
    for row in foPartNumberCon.Rows:
        if row["GES_Part_Number"]:
            gespartslistPrice[row["GES_Part_Number"]] = row["ListPrice"]
    #Trace.Write(str(gespartsCost))
    return gespartslistPrice

def getSalesOrg(country):
    query = SqlHelper.GetFirst("select Execution_Country_Sales_Org from EXECUTION_COUNTRY_SALES_ORG_MAPPING where Execution_County = '{}'".format(country))
    if query is not None:
        #Trace.Write("SalesOrg = " + query.Execution_Country_Sales_Org)
        return query.Execution_Country_Sales_Org

def getInflationRate(salesOrg):
    LOB = Quote.GetCustomField("Booking LOB").Content
    query = "Select * from YOY_INFLATION_RATE where salesOrg = '{0}' and LOB = '{1}'".format(salesOrg,LOB)
    res = SqlHelper.GetFirst(query)
    if res is not None:
        return res
    return 0

def getCalculateListPrice(power):
    salesOrg = getSalesOrg(row["Execution_Country"])
    res = getInflationRate(salesOrg)
    if power == 1:
        inflationRate1 = res.Inflation_Rate
        price = (getFloat(gespartslistPrice.get(row["GES_Eng"],0)) * getFloat(1 + getFloat(inflationRate1 )))
    elif power == 2 :
        inflationRate1 = res.Inflation_Rate
        inflationRate2 = res.Inflation_Rate_Year2
        price = (getFloat(gespartslistPrice.get(row["GES_Eng"],0)) * getFloat(1 + getFloat(inflationRate1)) * getFloat(1 + getFloat(inflationRate2)))
    elif power == 3:
        inflationRate1 = res.Inflation_Rate
        inflationRate2 = res.Inflation_Rate_Year2
        inflationRate3 = res.Inflation_Rate_Year3
        price = (getFloat(gespartslistPrice.get(row["GES_Eng"],0)) * getFloat(1 + getFloat(inflationRate1)) * getFloat(1 + getFloat(inflationRate2)) * getFloat(1 + getFloat(inflationRate3)))
    if price:
        Trace.Write(price)
        return price
    return 0

def populateGESListPrice(row):
    if row["GES_Eng_Percentage_Split"] not in ('0','') and row["Final_Hrs"] not in ('','0.0'):
        if row["Execution_Year"] == "2022":
            Trace.Write("check")
            row["GES_ListPrice"] = str(gespartslistPrice.get(row["GES_Eng"],0))
        elif row["Execution_Year"] == "2023":
            power = 1
            row["GES_ListPrice"] = str(getCalculateListPrice(power))
        elif row["Execution_Year"] == "2024":
            power = 2
            row["GES_ListPrice"] = str(getCalculateListPrice(power))
        elif row["Execution_Year"] == "2025":
            power = 3
            row["GES_ListPrice"] = str(getCalculateListPrice(power))

gespartslistPrice = getGESListPrice()
Trace.Write(str(gespartslistPrice))

containers = ['MSID_Labor_OPM_Engineering','MSID_Labor_LCN_One_Time_Upgrade_Engineering','MSID_Labor_Project_Management','MSID_Additional_Custom_Deliverables']

for container in containers:
    for row in getContainer(container).Rows:
        populateGESListPrice(row)
    getContainer(container).Calculate()