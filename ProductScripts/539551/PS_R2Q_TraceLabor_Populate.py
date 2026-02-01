isR2Qquote = True if Quote.GetCustomField("isR2QRequest").Content else False
if isR2Qquote:
    import math as m

    from System import DateTime

    def getContainer(Name):
        return Product.GetContainerByName(Name)

    def getCfValue(Name):
        return Quote.GetCustomField(Name).Content

    def getAttrValue(Product,Name):
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
        query = TagParserQuote.ParseString("select * from MPA_PRICE_PLAN_MAPPING where Honeywell_Ref = '<*CTX(Quote.CustomField(MPA Honeywell Ref))*>' and  Honeywell_Ref ! = '' and Price_Plan_Status= 'Active' and Price_Plan_Parts_Discount = 'Y' and Price_Plan_Start_Date < '<*CTX( Date.Format(MM/dd/yyyy) )*>' and Price_Plan_End_Date > '<*CTX( Date.Format(MM/dd/yyyy) )*>'")
        res = SqlHelper.GetList(query)
        if res and len(res) > 0:
            PricePlanPresent = True
        return PricePlanPresent

    def getExecutionCountry():
        marketCode = Quote.SelectedMarket.MarketCode
        #salesOrg = marketCode.partition('_')[0]
        #Updated logic for Defect 27359
        #currency = marketCode.partition('_')[2]
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

    def populatelLabCon(msidproduct,LabCon,AdjustmentProductivity,mpaAvailable,activeServiceContract,contractType,modulename,GES_Valuecode):
        #LabCon = msidproduct.LabCon
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
                        if getAttrValue(msidproduct,"MSID_GES_Location") != 'None':
                            row["FO_Eng_Percentage_Split"] = Product.ParseString(entry.FO_Eng_Split)
                            row["GES_Eng_Percentage_Split"] = Product.ParseString(entry.GES_Eng_Split)
                            row["GES_Eng"] = "SVC_GES_P350B_{}".format(GES_Valuecode)
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
                        if getAttrValue(msidproduct,"MSID_GES_Location") != 'None':
                            row["FO_Eng_Percentage_Split"] = Product.ParseString(entry.FO_Eng_Split)
                            row["GES_Eng_Percentage_Split"] = Product.ParseString(entry.GES_Eng_Split)
                            row["GES_Eng"] = "SVC_GES_P350F_{}".format(GES_Valuecode)
                        else:
                            row["FO_Eng_Percentage_Split"] = "100"
                            row["GES_Eng_Percentage_Split"] = "0"
                        if excecutionCountry:
                            row["Execution_Country"] = excecutionCountry
    excecutionCountry = getExecutionCountry()
    executionYear = getDefaultExecutionYear()
    mpaAvailable = checkForMPACustomer()

    migration_new_cont = Product.GetContainerByName('CONT_Migration_MSID_Selection')
    for MigrationNew in migration_new_cont.Rows: 
        foPartNumberCon = MigrationNew.Product.GetContainerByName("MSID_Labor_FO_Part_Number")
        traceCon = MigrationNew.Product.GetContainerByName("Trace_Software_Labor_con")
        
        traceProductivity =getAttrValue(MigrationNew.Product,"Trace_Software_Adjustment_Productivity")
        activeServiceContract = getAttrValue(MigrationNew.Product,"MSID_Active_Service_Contract")
        if activeServiceContract == 'Yes' or mpaAvailable:
            contractType = "Contract"
        else:
            contractType = "Non-Contract"
        msidCont = MigrationNew.Product.GetContainerByName("CONT_MSID_SUBPRD")
        msidproduct = MigrationNew.Product
        for row in msidCont.Rows:
            Product = row.Product
            
            selectedProducts = row["Selected_Products"]
            if selectedProducts == 'Trace Software':
                    
                if selectedProducts == 'Trace Software' and foPartNumberCon.Rows.Count == 0:
                        ScriptExecutor.Execute('R2Q_Trace_PopulatePartNumber')
                GES_location =MigrationNew.Product.Attr('MSID_GES_Location').GetValue() if MigrationNew.Product.Attr('MSID_GES_Location').GetValue() != 'None' else ''
                GES_Valuecode=Product.ParseString('<*ValueCode(MSID_GES_Location)*>')
                GES_Valuecode = {'GES India': 'IN', 'GES China': 'CN', 'GES Romania': 'RO', 'GES Uzbekistan': 'UZ', 'GES Egypt': 'EG'}.get(GES_location, '')
                populatelLabCon(msidproduct, traceCon,traceProductivity,mpaAvailable,activeServiceContract,contractType,"Trace Software",GES_Valuecode) if "Trace Software" in selectedProducts else 0
                con = Product.GetContainerByName('Trace_Software_License_Configuration_transpose')
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