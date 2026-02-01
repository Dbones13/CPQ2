#PS_CalculateTotals
def getContainer(Name):
    return Product.GetContainerByName(Name)

def getFloat(Var):
    if Var:
        return float(Var)
    return 0

def calculateTotals(container):
    totalOffSiteHrs = 0
    totalOnSiteHrs = 0
    totalOffSiteFinalHrs = 0
    totalOnSiteFinalHrs = 0
    totalCalculatedHrs = 0
    totalFinalHrs = 0
    for row in container.Rows:
        if row["Deliverable_Type"] == "Offsite":
            if row["Calculated_Hrs"] != "0":
                totalOffSiteHrs = totalOffSiteHrs + getFloat(row["Calculated_Hrs"])
                totalOffSiteFinalHrs = totalOffSiteFinalHrs + getFloat(row["Final_Hrs"])
        elif row["Deliverable_Type"] == "Onsite":
            if row["Calculated_Hrs"] != "0":
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

opmEngineeringCon = getContainer("MSID_Labor_OPM_Engineering")
lcnOneTimeUpgradeCon = getContainer("MSID_Labor_LCN_One_Time_Upgrade_Engineering")
projectManagementCon = getContainer("MSID_Labor_Project_Management")
ebrCon = getContainer("MSID_Labor_EBR_Con")
elcnCon = getContainer("MSID_Labor_ELCN_Con")

if opmEngineeringCon.Rows.Count > 0:
    calculateTotals(opmEngineeringCon)

if ebrCon.Rows.Count > 0:
    calculateTotals(ebrCon)

if elcnCon.Rows.Count > 0:
    calculateTotals(elcnCon)   

if lcnOneTimeUpgradeCon.Rows.Count > 0:
    totalOffSiteHrs = 0
    totalOffSiteFinalHrs = 0
    totalCalculatedHrs = 0
    totalFinalHrs = 0
    for row in lcnOneTimeUpgradeCon.Rows:
        if row["Deliverable_Type"] == "Offsite":
            if row["Calculated_Hrs"] != "0":
                totalOffSiteHrs = totalOffSiteHrs + getFloat(row["Calculated_Hrs"])
                totalOffSiteFinalHrs = totalOffSiteFinalHrs + getFloat(row["Final_Hrs"])
    for row in lcnOneTimeUpgradeCon.Rows:
        if row["Deliverable"] == "Off-Site":
            row["Calculated_Hrs"] = str(totalOffSiteHrs)
            row["Final_Hrs"] = str(totalOffSiteFinalHrs)
        if row["Deliverable"] == "Total":
            row["Calculated_Hrs"] = str(totalOffSiteHrs)
            row["Final_Hrs"] = str(totalOffSiteFinalHrs)
    lcnOneTimeUpgradeCon.Calculate()

if projectManagementCon.Rows.Count > 0:
    totalCalculatedHrs = 0
    totalFinalHrs = 0
    for row in projectManagementCon.Rows:
        if row["Deliverable_Type"] in ("Offsite","Off-Site","On-Site","Onsite"):
            if row["Calculated_Hrs"] != "0":
                totalCalculatedHrs = totalCalculatedHrs + getFloat(row["Calculated_Hrs"])
            totalFinalHrs = totalFinalHrs + getFloat(row["Final_Hrs"])
    for row in projectManagementCon.Rows:
        if row["Deliverable"] == "Total":
            row["Calculated_Hrs"] = str(totalCalculatedHrs)
            row["Final_Hrs"] = str(totalFinalHrs)
    projectManagementCon.Calculate()