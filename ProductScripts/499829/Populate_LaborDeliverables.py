isR2Qquote = True if Quote.GetCustomField("isR2QRequest").Content else False
if not isR2Qquote:
    import math as m

    from System import DateTime

    def getContainer(Name):
        return Product.GetContainerByName(Name)

    def getCfValue(Name):
        return Quote.GetCustomField(Name).Content

    def getAttrValue(Name):
        return Product.Attr(Name).GetValue()

    def getFloat(Var):
        if Var:
            return float(Var)
        return 0

    def calculateFinalHours1(row,oldCalHrs):
        if getFloat(oldCalHrs) == getFloat(row["Calculated_Hrs"]):
            return str(round(getFloat(row["Final_Hrs"])))
        else:
            return str(round(getFloat(row["Calculated_Hrs"]) * getFloat(row["Adjustment_Productivity"])))

    def reCalAdj(row,oldCalHrs):
        if getFloat(oldCalHrs) != getFloat(row["Calculated_Hrs"]):
            return "1"
        else:
            return row["Adjustment_Productivity"]

    def getTotalEngHours(container):
        totalFinalHours = 0
        for row in getContainer(container).Rows:
            if row["Deliverable"] == "Total":
                totalFinalHours += getFloat(row["Final_Hrs"])
        return totalFinalHours

    def calculateTotals(container):
        totalOffSiteHrs = 0
        totalOnSiteHrs = 0
        totalOffSiteFinalHrs = 0
        totalOnSiteFinalHrs = 0
        totalCalculatedHrs = 0
        totalFinalHrs = 0
        for row in container.Rows:
            if row["Deliverable_Type"] in ("Offsite","Off-Site"):
                #if row["Calculated_Hrs"] != "0":
                totalOffSiteHrs = totalOffSiteHrs + getFloat(row["Calculated_Hrs"])
                totalOffSiteFinalHrs = totalOffSiteFinalHrs + getFloat(row["Final_Hrs"])
            elif row["Deliverable_Type"] in ("Onsite","On-Site"):
                #if row["Calculated_Hrs"] != "0":
                totalOnSiteHrs = totalOnSiteHrs + getFloat(row["Calculated_Hrs"])
                totalOnSiteFinalHrs = totalOnSiteFinalHrs + getFloat(row["Final_Hrs"])
            totalCalculatedHrs = totalOffSiteHrs + totalOnSiteHrs
            totalFinalHrs = totalOffSiteFinalHrs + totalOnSiteFinalHrs
        for row in container.Rows:
            if row["Deliverable"] == "Off-Site":
                row["Calculated_Hrs"] = str(totalOffSiteHrs)
                row["Final_Hrs"] = str(totalOffSiteFinalHrs)
            elif row["Deliverable"] == "On-Site":
                row["Calculated_Hrs"] = str(totalOnSiteHrs)
                row["Final_Hrs"] = str(totalOnSiteFinalHrs)
            elif row["Deliverable"] == "Total":
                row["Calculated_Hrs"] = str(totalCalculatedHrs)
                row["Final_Hrs"] = str(totalFinalHrs)
        container.Calculate()

    def getDefaultExecutionYear():
        executionYear = str(DateTime.Now.Year)
        yearsList = []
        currentYear = DateTime.Now.Year
        i = 0
        while i < 4:
            year = currentYear + i
            yearsList.append(year)
            i += 1
        if getCfValue("EGAP_Contract_Start_Date") != '':
            year = UserPersonalizationHelper.CovertToDate(getCfValue("EGAP_Contract_Start_Date")).Year
            if year in yearsList:
                executionYear = year
            else:
                executionYear = yearsList[-1] if len(yearsList) > 0 else str(DateTime.Now.Year)
        return executionYear

    def checkForMPACustomer():
        PricePlanPresent = False
        query = TagParserQuote.ParseString("select * from MPA_PRICE_PLAN_MAPPING where Honeywell_Ref = '<*CTX(Quote.CustomField(MPA Honeywell Ref))*>' and Price_Plan_Status= 'Active' and Price_Plan_Parts_Discount = 'Y' and Price_Plan_Start_Date < '<*CTX( Date.Format(MM/dd/yyyy) )*>' and Price_Plan_End_Date > '<*CTX( Date.Format(MM/dd/yyyy) )*>'")
        res = SqlHelper.GetList(query)
        if res and len(res) > 0:
            PricePlanPresent = True
        return PricePlanPresent

    def getExecutionCountry():
        marketCode = Quote.SelectedMarket.MarketCode
        # salesOrg = marketCode.partition('_')[0]
        #Updated logic for Defect 27359
        # currency = marketCode.partition('_')[2]
        salesOrg = Quote.GetCustomField('Sales Area').Content
        currency = Quote.GetCustomField('Currency').Content
        query = SqlHelper.GetFirst("select Execution_County from NEW_EXECUTION_COUNTRY_SALES_ORG_MAPPING where Sales_Area = '{}' and Currency = '{}'".format(salesOrg,currency))
        #query = SqlHelper.GetFirst("select Execution_County from EXECUTION_COUNTRY_SALES_ORG_MAPPING where Execution_Country_Sales_Org = '{}'".format(salesOrg))
        if query is not None:
            return query.Execution_County

    def migrationDDSCheck(elcnUpgradeNew):
        sum = 0
        rowIndex = 0
        for row in elcnUpgradeNew.Rows:
            if rowIndex < 2:
                for column in row.Columns:
                    if row[column.Name] != '':
                        sum += int(row[column.Name])
            rowIndex += 1
        if sum > 0:
            return sum
        else:
            return 0

    def populatelLabCon(LabCon,AdjustmentProductivity,mpaAvailable,activeServiceContract,contractType,modulename):
        if LabCon.Rows.Count == 0:
            excecutionCountry = getExecutionCountry()
            queryData = SqlHelper.GetList("select * from LABOR_DELIVERABLES where Product_Module = '{}'and Contract = '{}'".format(modulename,contractType))
            row = LabCon.AddNewRow(False)
            row["Deliverable"] = "Total"
            row = LabCon.AddNewRow(False)
            row["Deliverable"] = "Off-Site"
            if queryData is not None:
                for entry in queryData:
                    if Product.ParseString(entry.Deliverable_Type) == "Offsite":
                        row = LabCon.AddNewRow(False)
                        row["Deliverable"] = entry.Deliverables
                        row["Deliverable_Type"] = "Offsite"
                        row["Adjustment_Productivity"] = AdjustmentProductivity
                        row["Execution_Year"] = str(executionYear)
                        row["FO_Eng"] = entry.FO_Eng
                        if getAttrValue("Trace_software_GES_Location") != 'None':
                            row["FO_Eng_Percentage_Split"] = Product.ParseString(entry.FO_Eng_Split)
                            row["GES_Eng_Percentage_Split"] = Product.ParseString(entry.GES_Eng_Split)
                            row["GES_Eng"] = "SVC_GES_P350B_{}".format(TagParserProduct.ParseString('<*ValueCode(Trace_software_GES_Location)*>'))
                        else:
                            row["FO_Eng_Percentage_Split"] = "100"
                            row["GES_Eng_Percentage_Split"] = "0"
                        if excecutionCountry:
                            row["Execution_Country"] = excecutionCountry
                row = LabCon.AddNewRow(False)
                row["Deliverable"] = "On-Site"
                for entry in queryData:
                    if Product.ParseString(entry.Deliverable_Type) == "Onsite":
                        row = LabCon.AddNewRow(False)
                        row["Deliverable"] = entry.Deliverables
                        row["Deliverable_Type"] = "Onsite"
                        row["Adjustment_Productivity"] = AdjustmentProductivity
                        row["Execution_Year"] = str(executionYear)
                        row["FO_Eng"] = entry.FO_Eng
                        if getAttrValue("Trace_software_GES_Location") != 'None':
                            row["FO_Eng_Percentage_Split"] = Product.ParseString(entry.FO_Eng_Split)
                            row["GES_Eng_Percentage_Split"] = Product.ParseString(entry.GES_Eng_Split)
                            row["GES_Eng"] = "SVC_GES_P350F_{}".format(TagParserProduct.ParseString('<*ValueCode(Trace_software_GES_Location)*>'))
                        else:
                            row["FO_Eng_Percentage_Split"] = "100"
                            row["GES_Eng_Percentage_Split"] = "0"
                        if excecutionCountry:
                            row["Execution_Country"] = excecutionCountry
                        
    def populateprojectManagementCon(projectManagementCon,pmAdjustmentProductivity,mpaAvailable,activeServiceContract):
        if projectManagementCon.Rows.Count == 0:
            excecutionCountry = getExecutionCountry()
            queryData = SqlHelper.GetList("select * from LABOR_DELIVERABLES where Product_Module = 'PM'")
            row = projectManagementCon.AddNewRow(False)
            row["Deliverable"] = "Total"
            if queryData is not None:
                for entry in queryData:
                    if entry.Deliverable_Type == "Offsite":
                        row = projectManagementCon.AddNewRow(False)
                        row["Deliverable"] = entry.Deliverables
                        row["Adjustment_Productivity"] = pmAdjustmentProductivity
                        row["Deliverable_Flag"] = entry.Deliverable_Flag
                        row["Deliverable_Type"] = entry.Deliverable_Type
                        row["FO_Eng_Percentage_Split"] = "100"
                        row["GES_Eng_Percentage_Split"] = "0"
                        if row["Deliverable_Flag"] == "PM":
                            if mpaAvailable or activeServiceContract == "Yes":
                                row["FO_Eng"] = "SVC-PMGT-ST"
                            else:
                                row["FO_Eng"] = "SVC-PMGT-ST-NC"
                        elif row["Deliverable_Flag"] == "PA":
                            if mpaAvailable or activeServiceContract == "Yes":
                                row["FO_Eng"] = "SVC-PADM-ST"
                            else:
                                row["FO_Eng"] = "SVC-PADM-ST-NC"
                        row["Execution_Year"] = str(executionYear)
                        if getAttrValue("Trace_software_GES_Location") != 'None':
                            row["GES_Eng"] = "SVC_GES_P215B_{}".format(TagParserProduct.ParseString('<*ValueCode(Trace_software_GES_Location)*>'))
                        if excecutionCountry:
                            row["Execution_Country"] = excecutionCountry

    if Product.Attr('Trace_Software_Scope_Choices').GetValue() in ['LABOR', 'HW/SW/LABOR']:
        excecutionCountry = getExecutionCountry()
        executionYear = getDefaultExecutionYear()
        foPartNumberCon = getContainer("MSID_Labor_FO_Part_Number")
        traceCon = getContainer("Trace_Software_Labor_con")
        projectManagementCon = getContainer("Trace_Project_Management_Labor_con")

        traceProductivity =getAttrValue("Trace_Software_Adjustment_Productivity")
        pmAdjustmentProductivity = getAttrValue("PM_Adjustment_Productivity")

        mpaAvailable = checkForMPACustomer()
        activeServiceContract = getAttrValue("Trace_software_Active_Service_Contract")
        if activeServiceContract == 'Yes' or mpaAvailable:
            contractType = "Contract"
        else:
            contractType = "Non-Contract"

        if foPartNumberCon.Rows.Count == 0:
            ScriptExecutor.Execute('PopulatePartNumberContainer')

        populatelLabCon( traceCon,traceProductivity,mpaAvailable,activeServiceContract,contractType,"Trace Software")
        populateprojectManagementCon(projectManagementCon,pmAdjustmentProductivity,mpaAvailable,activeServiceContract) 

        con = getContainer('Trace_Software_License_Configuration_transpose')
        conrow = con.Rows[0]
        var_2 = conrow['Trace_Software_L4_Trace_Server_Option']
        var_1 = Product.Attr('Trace_Software_Number_of_Tags').GetValue()
        var_3 = Product.Attr('Trace_Software_Is_this_a_customized_installation').GetValue()
        var_4 = Product.Attr('Trace_Software_Architecture_drawing_update').GetValue()

        Drawing_update = 0
        Drawing_update += 4.00 if(var_4 == "Yes") else 0

        Installation = 0
        if var_1 == "<=50000":
            if var_2 =="Yes":
                Installation = 32.00
            else:
                Installation = 24.00
        else:
            if var_2 =="Yes":
                Installation = 40.00
            else:
                Installation = 32.00

        if var_3 == "Yes":
            Installation = Installation + 8.00

        if traceCon.Rows.Count > 0:
            for row in traceCon.Rows:
                oldCalHrs = row["Calculated_Hrs"]
                if row["Deliverable"] == "Trace Existing Drawings Updates":
                    row["Calculated_Hrs"] = str(Drawing_update)
                    row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
                    row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
                elif row["Deliverable"] == "Trace Installation":
                    row["Calculated_Hrs"] = str(Installation)
                    row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
                    row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
            calculateTotals(traceCon)


        EngHours = getTotalEngHours("Trace_Software_Labor_con") 

        pmOtherActivities = 0
        if EngHours > 0:
            pmOtherActivities = 24
        else:
            pmOtherActivities = 0

        paOtherActivities = 0
        if EngHours > 0:
            paOtherActivities = 8
        else:
            paOtherActivities = 0

        paMonthlyProjectManagement = 0
        if EngHours <= 160 :
            paMonthlyProjectManagement = 0
        else:
            paMonthlyProjectManagement = 16

        pmEngineeringManagement = 0
        if EngHours <= 160:
            pmEngineeringManagement = 0
        elif EngHours > 160 and EngHours <= 2000:
            pmEngineeringManagement = round((EngHours -160) * 0.1)
        else:
            pmEngineeringManagement = 176 + round((EngHours - 2000 -160) * 0.05)

        if projectManagementCon.Rows.Count > 0:
            for row in projectManagementCon.Rows:
                oldCalHrs = row["Calculated_Hrs"]
                if row["Deliverable"] == "PM Engineering Management":
                    row["Calculated_Hrs"] = str(pmEngineeringManagement)
                    row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
                    row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
                elif row["Deliverable"] == "PM Other activities":
                    row["Calculated_Hrs"] = str(pmOtherActivities)
                    row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
                    row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
                elif row["Deliverable"] == "PA Monthly Project Management":
                    row["Calculated_Hrs"] = str(paMonthlyProjectManagement)
                    row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
                    row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
                elif row["Deliverable"] == "PA Other activities":
                    row["Calculated_Hrs"] = str(paOtherActivities)
                    row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
                    row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
            calculateTotals(projectManagementCon)