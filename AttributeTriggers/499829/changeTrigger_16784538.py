def getContainer(Name):
    return Product.GetContainerByName(Name)

def getFloat(Var):
    if Var:
        return float(Var)
    return 0

AdjustmentProductivity = Product.Attr('PM_Adjustment_Productivity').GetValue()
projectManagementCon = getContainer("Trace_Project_Management_Labor_con")
if projectManagementCon.Rows.Count > 0:
    for row in projectManagementCon.Rows:
        if row.IsSelected == True:
            if (row["Deliverable"] not in ('Total')) and getFloat(row["Calculated_Hrs"])!= 0:
                row["Adjustment_Productivity"] = AdjustmentProductivity
                row["Final_Hrs"] = str(round(float(row["Calculated_Hrs"]) * float(AdjustmentProductivity)))
    totalFinalHrs = 0
    for row in projectManagementCon.Rows:
        if row["Deliverable_Type"] in ("Offsite","Off-Site"):
            totalFinalHrs = totalFinalHrs + float(row["Final_Hrs"])
    for row in projectManagementCon.Rows:
        if row["Deliverable"] == "Total":
            row["Final_Hrs"] = str(totalFinalHrs)
    projectManagementCon.Calculate()
Product.Attr('PM_Adjustment_Productivity').AssignValue('')