def getContainer(Name):
    return Product.GetContainerByName(Name)

def getFloat(Var):
    if Var:
        return float(Var)
    return 0

AdjustmentProductivity = Product.Attr('QCS_RAE_Upgrade_Adjustment_Productivity').GetValue()
QCSRAECon = getContainer("MSID_Labor_QCS_RAE_Upgrade_con")
if QCSRAECon.Rows.Count > 0:
    for row in QCSRAECon.Rows:
        if row.IsSelected == True:
            if (row["Deliverable"] not in ('Total','Off-Site','On-Site')) and getFloat(row["Calculated_Hrs"])!= 0:
                row["Adjustment_Productivity"] = AdjustmentProductivity
                row["Final_Hrs"] = str(round(float(row["Calculated_Hrs"]) * float(AdjustmentProductivity)))
    totalOffSiteFinalHrs = 0
    totalOnSiteFinalHrs = 0
    totalFinalHrs = 0
    for row in QCSRAECon.Rows:
        if row["Deliverable_Type"] in ("Offsite","Off-Site"):
            totalOffSiteFinalHrs = totalOffSiteFinalHrs + float(row["Final_Hrs"])
        elif row["Deliverable_Type"] in ("Onsite","On-Site"):
            totalOnSiteFinalHrs = totalOnSiteFinalHrs + float(row["Final_Hrs"])
        totalFinalHrs = totalOffSiteFinalHrs + totalOnSiteFinalHrs
    for row in QCSRAECon.Rows:
        if row["Deliverable"] == "Off-Site":
            row["Final_Hrs"] = str(totalOffSiteFinalHrs)
        elif row["Deliverable"] == "On-Site":
            row["Final_Hrs"] = str(totalOnSiteFinalHrs)
        elif row["Deliverable"] == "Total":
            row["Final_Hrs"] = str(totalFinalHrs)
    QCSRAECon.Calculate()
Product.Attr('QCS_RAE_Upgrade_Adjustment_Productivity').AssignValue('')
ScriptExecutor.Execute('PS_CalculateProjectManagementLaborHours')