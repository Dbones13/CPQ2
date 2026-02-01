def setAttrValue(Name,value):
    Product.Attr(Name).AssignValue(value)

def getCfValue(Name):
    return Quote.GetCustomField(Name).Content

exeYearsRange =  set([DateTime.Now.Year +i for i in range(4)])

if getCfValue("EGAP_Contract_Start_Date") != '' and getCfValue("EGAP_Contract_End_Date") != '':
    contractStartYear = UserPersonalizationHelper.CovertToDate( getCfValue("EGAP_Contract_Start_Date")).Year
    contractEndYear = UserPersonalizationHelper.CovertToDate(getCfValue("EGAP_Contract_End_Date")).Year
    year = int(Product.Attr('Generic4_Execution_Year').GetValue())
    setAttrValue("Generic4_Message",'')
    if len(str(year)) < 4 or year < DateTime.Now.Year or year not in exeYearsRange:
        setAttrValue("Generic4_Message",'User is allowed to enter current + next 3 years in 20XX format (e.g. 2023, 2025 etc)')
        setAttrValue("Generic4_Execution_Year",'')
    else:
        if year <= contractEndYear and year >= contractStartYear:
            container =  Product.GetContainerByName("MSID_Labor_Generic_System4_Cont")
            for row in container.Rows:
                if row["Deliverable"] not in ('Total','Off-Site','On-Site') and row.IsSelected:
                    row["Execution_Year"] = str(year)
                    row.IsSelected = False
            setAttrValue("Generic4_Execution_Year",'')
            ScriptExecutor.Execute('PS_PopulateGESCost')
        else:
            setAttrValue("Generic4_Message",'Execution Year should be in between the Contract start date and Contract end date')
            setAttrValue("Generic4_Execution_Year",'')
else:
    year = int(Product.Attr('Generic4_Execution_Year').GetValue())
    setAttrValue("Generic4_Message",'')
    if year not in exeYearsRange:
        setAttrValue("Generic4_Message",'User is allowed to enter current + next 3 years in 20XX format (e.g. 2023, 2025 etc)')
        setAttrValue("Generic4_Execution_Year",'')
    else:
        container =  Product.GetContainerByName("MSID_Labor_Generic_System4_Cont")
        for row in container.Rows:
            if row["Deliverable"] not in ('Total','Off-Site','On-Site') and row.IsSelected:
                row["Execution_Year"] = str(year)
                row.IsSelected = False
        setAttrValue("Generic4_Execution_Year",'')
        ScriptExecutor.Execute('PS_PopulateGESCost')