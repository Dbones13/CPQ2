isR2Qquote = True if Quote.GetCustomField("isR2QRequest").Content else False
if not isR2Qquote:
    def getContainer(Name):
        return Product.GetContainerByName(Name)

    def calculateFinalHours(row):
        return str(round(getFloat(row["Calculated_Hrs"]) * getFloat(row["Adjustment_Productivity"])))

    def getFloat(Var):
        if Var:
            return float(Var)
        return 0

    def getTotalEngHours(container):
        totalFinalHours = 0
        for row in getContainer(container).Rows:
            if row["Deliverable"] == "Total":
                totalFinalHours += getFloat(row["Final_Hrs"])
        return totalFinalHours

    def getProjectMangementHours():
        
        EngHours = getTotalEngHours("Trace_Software_Labor_con")

        Trace.Write("EngHours = " + str(EngHours))
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
        if EngHours <= 160:
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

        return pmOtherActivities,paOtherActivities,paMonthlyProjectManagement,pmEngineeringManagement


    projectManagementCon = getContainer("Trace_Project_Management_Labor_con")
    if projectManagementCon.Rows.Count > 0:
        pmOtherActivities,paOtherActivities,paMonthlyProjectManagement,pmEngineeringManagement = getProjectMangementHours()
        for row in projectManagementCon.Rows:
            if row["Deliverable"] == "PM Engineering Management":
                row["Calculated_Hrs"] = str(pmEngineeringManagement)
                if getFloat(row["Calculated_Hrs"]) == 0:
                    row["Adjustment_Productivity"] = str(1)    
                row["Final_Hrs"] = calculateFinalHours(row)
            elif row["Deliverable"] == "PM Other activities":
                row["Calculated_Hrs"] = str(pmOtherActivities)
                if getFloat(row["Calculated_Hrs"]) == 0:
                    row["Adjustment_Productivity"] = str(1)
                row["Final_Hrs"] = calculateFinalHours(row)
            elif row["Deliverable"] == "PA Monthly Project Management":
                row["Calculated_Hrs"] = str(paMonthlyProjectManagement)
                if getFloat(row["Calculated_Hrs"]) == 0:
                    row["Adjustment_Productivity"] = str(1)
                row["Final_Hrs"] = calculateFinalHours(row)
            elif row["Deliverable"] == "PA Other activities":
                row["Calculated_Hrs"] = str(paOtherActivities)
                if getFloat(row["Calculated_Hrs"]) == 0:
                    row["Adjustment_Productivity"] = str(1)
                row["Final_Hrs"] = calculateFinalHours(row)
        projectManagementCon.Calculate()

    if projectManagementCon.Rows.Count > 0:
        '''for row in projectManagementCon.Rows:
            if row["Deliverable"] not in ('Total'):
                row["Adjustment_Productivity"] = AdjustmentProductivity
                row["Final_Hrs"] = str(round(getFloat(row["Calculated_Hrs"]) * getFloat(AdjustmentProductivity)))'''
        totalCalculatedHrs = 0
        totalFinalHrs = 0
        for row in projectManagementCon.Rows:
            if row["Deliverable_Type"] == "Offsite":
                if row["Calculated_Hrs"] != "0":
                    totalCalculatedHrs = totalCalculatedHrs + getFloat(row["Calculated_Hrs"])
                    totalFinalHrs = totalFinalHrs + getFloat(row["Final_Hrs"])
        for row in projectManagementCon.Rows:
            if row["Deliverable"] == "Total":
                row["Calculated_Hrs"] = str(totalCalculatedHrs)
                row["Final_Hrs"] = str(totalFinalHrs)
        projectManagementCon.Calculate()