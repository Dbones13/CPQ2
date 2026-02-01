isR2Qquote = True if Quote.GetCustomField("isR2QRequest").Content else False
if not isR2Qquote:
    def getContainer(product,Name):
        return product.GetContainerByName(Name)

    def getFloat(Var):
        if Var:
            return float(Var)
        return 0

    def addFinalHours(totalDict, key, value):
        totalDict[key] = getFloat(totalDict.get(key, 0)) + getFloat(value)

    def getExecutionCountry():
        marketCode = Quote.SelectedMarket.MarketCode
        # salesOrg = marketCode.partition('_')[0]
        #query = SqlHelper.GetFirst("select Execution_County from EXECUTION_COUNTRY_SALES_ORG_MAPPING where Execution_Country_Sales_Org = '{}'".format(salesOrg))
        #Update for Defect CXCPQ-27359
        # currency = marketCode.partition('_')[2]
        salesOrg = Quote.GetCustomField('Sales Area').Content
        currency = Quote.GetCustomField('Currency').Content
        query = SqlHelper.GetFirst("select Execution_County from NEW_EXECUTION_COUNTRY_SALES_ORG_MAPPING where Sales_Area = '{}' and Currency = '{}'".format(salesOrg,currency))
        if query is not None:
            return query.Execution_County

    def getFinalHours(msidProduct,container):
        for row in getContainer(msidProduct,container).Rows:
            if row["Deliverable"] not in ('Off-Site','On-Site','Total'):
                if row["Execution_Country"] == excecutionCountry and row["Final_Hrs"] not in ('',"0") and row["FO_Eng"] != '' and row["FO_Eng_Percentage_Split"] != '0':
                    addFinalHours(laboHours, "Local Labor", round(getFloat(row["Final_Hrs"]) * getFloat(row["FO_Eng_Percentage_Split"]) / 100))
                elif row["Final_Hrs"] not in ('',"0") and row["FO_Eng"] != '' and row["FO_Eng_Percentage_Split"] != '0':
                    addFinalHours(laboHours, "Cross Border Labor", round(getFloat(row["Final_Hrs"]) * getFloat(row["FO_Eng_Percentage_Split"]) / 100))
                if row["Final_Hrs"] not in ('',"0") and row["GES_Eng"] != '' and row["GES_Eng_Percentage_Split"] != '0':
                    if row["GES_Eng"] in ('SVC_GES_P350B_IN','SVC_GES_P350B_CN','SVC_GES_P350B_RO','SVC_GES_P350B_UZ','SVC_GES_P350B_EG','SVC_GES_P215B_IN','SVC_GES_P215B_CN','SVC_GES_P215B_RO','SVC_GES_P215B_UZ'):
                        addFinalHours(laboHours, "GES - Work @ GES Location", round(getFloat(row["Final_Hrs"]) * getFloat(row["GES_Eng_Percentage_Split"]) / 100))
                    elif row["GES_Eng"] in ('SVC_GES_P350F_IN','SVC_GES_P350F_CN','SVC_GES_P350F_RO','SVC_GES_P350F_UZ','SVC_GES_P350F_EG','SVC_GES_P215F_IN','SVC_GES_P215F_CN','SVC_GES_P215F_RO','SVC_GES_P215F_UZ'):
                        addFinalHours(laboHours, "GES - Work @ Non GES Location", round(getFloat(row["Final_Hrs"]) * getFloat(row["GES_Eng_Percentage_Split"]) / 100))

    laboHours = dict()
    excecutionCountry = getExecutionCountry()
    laborFields = ['Local Labor','Cross Border Labor','GES - Work @ GES Location','GES - Work @ Non GES Location','Total GES Hours','Total Labor']
    getFinalHours(Product,"Trace_Software_Labor_con")
    getFinalHours(Product,"Trace_Project_Management_Labor_con")
    totalLabor1 = laboHours.get("Local Labor",0) + laboHours.get("Cross Border Labor",0) + laboHours.get("GES - Work @ GES Location",0) + laboHours.get("GES - Work @ Non GES Location",0)
    Trace.Write(totalLabor1)
    #To Populate QuoteItemCustom Fields
    Local_Labor = laboHours.get("Local Labor",0)
    Cross_Border_Labor = laboHours.get("Cross Border Labor",0)
    GES_Location = laboHours.get("GES - Work @ GES Location",0)
    Non_GES_Location = laboHours.get("GES - Work @ Non GES Location",0)
    items = arg.QuoteItemCollection
    for item in items:
        if item.ProductName == "Trace Software":
            item["QI_Local_Labor"].Value = Local_Labor
            item["QI_Cross_Border_Labor"].Value = Cross_Border_Labor
            item["QI_GES_Work_GES_Location"].Value = GES_Location
            item["QI_GES_Work_Non_GES_Location"].Value = Non_GES_Location
            break

    Quote.Calculate(1)