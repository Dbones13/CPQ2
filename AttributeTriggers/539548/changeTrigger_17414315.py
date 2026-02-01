def getContainer(Name):
    return Product.GetContainerByName(Name)

def getFloat(Var):
    if Var:
        return float(Var)
    return 0

AdjustmentProductivity = Product.Attr('Orion_Console_Adjustment_Productivity').GetValue()
orionConsoleCon = getContainer("MSID_Labor_Orion_Console_Con")
if orionConsoleCon.Rows.Count > 0:
    for row in orionConsoleCon.Rows:
        if row.IsSelected == True:
            if (row["Deliverable"] not in ('Total','Off-Site','On-Site')) and getFloat(row["Calculated_Hrs"])!= 0:
                row["Adjustment_Productivity"] = AdjustmentProductivity
                row["Final_Hrs"] = str(round(getFloat(row["Calculated_Hrs"]) * getFloat(AdjustmentProductivity)))
    totalOffSiteFinalHrs = 0
    totalOnSiteFinalHrs = 0
    totalFinalHrs = 0
    for row in orionConsoleCon.Rows:
        if row["Deliverable_Type"] in ("Offsite","Off-Site"):
            totalOffSiteFinalHrs = totalOffSiteFinalHrs + getFloat(row["Final_Hrs"])
        elif row["Deliverable_Type"] in ("Onsite","On-Site"):
            totalOnSiteFinalHrs = totalOnSiteFinalHrs + getFloat(row["Final_Hrs"])
        totalFinalHrs = totalOffSiteFinalHrs + totalOnSiteFinalHrs
    for row in orionConsoleCon.Rows:
        if row["Deliverable"] == "Off-Site":
            row["Final_Hrs"] = str(totalOffSiteFinalHrs)
        elif row["Deliverable"] == "On-Site":
            row["Final_Hrs"] = str(totalOnSiteFinalHrs)
        elif row["Deliverable"] == "Total":
            row["Final_Hrs"] = str(totalFinalHrs)
    orionConsoleCon.Calculate()
Product.Attr('Orion_Console_Adjustment_Productivity').AssignValue('')
ScriptExecutor.Execute('PS_CalculateProjectManagementLaborHours')