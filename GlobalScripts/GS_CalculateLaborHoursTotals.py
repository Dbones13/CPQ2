def getContainer(Name):
    return Product.GetContainerByName(Name)

def getFloat(Var):
    if Var:
        return float(Var)
    return 0

def calculateTotals(container):
    #totalOffSiteHrs = 0
    #totalOnSiteHrs = 0
    totalOffSiteFinalHrs = 0
    totalOnSiteFinalHrs = 0
    #totalCalculatedHrs = 0
    totalFinalHrs = 0
    for row in container.Rows:
        if row["Deliverable_Type"] in ("Offsite","Off-Site"):
            if row["Final_Hrs"] != "0":
                #totalOffSiteHrs = totalOffSiteHrs + getFloat(row["Calculated_Hrs"])
                totalOffSiteFinalHrs = totalOffSiteFinalHrs + getFloat(row["Final_Hrs"])
        elif row["Deliverable_Type"] in ("Onsite","On-Site"):
            if row["Final_Hrs"] != "0":
                #totalOnSiteHrs = totalOnSiteHrs + getFloat(row["Calculated_Hrs"])
                totalOnSiteFinalHrs = totalOnSiteFinalHrs + getFloat(row["Final_Hrs"])
        #totalCalculatedHrs = totalOffSiteHrs + totalOnSiteHrs
        totalFinalHrs = totalOffSiteFinalHrs + totalOnSiteFinalHrs
    for row in container.Rows:
        if row["Deliverable"] == "Off-Site":
            #row["Calculated_Hrs"] = str(totalOffSiteHrs)
            row["Final_Hrs"] = str(totalOffSiteFinalHrs)
        elif row["Deliverable"] == "On-Site":
            #row["Calculated_Hrs"] = str(totalOnSiteHrs)
            row["Final_Hrs"] = str(totalOnSiteFinalHrs)
        elif row["Deliverable"] == "Total":
            #row["Calculated_Hrs"] = str(totalCalculatedHrs)
            row["Final_Hrs"] = str(totalFinalHrs)

containers = ['MSID_Labor_OPM_Engineering','MSID_Labor_LCN_One_Time_Upgrade_Engineering','MSID_Labor_EBR_Con','MSID_Labor_ELCN_Con','MSID_Labor_Orion_Console_Con','MSID_Labor_EHPM_C300PM_Con','MSID_Labor_TPS_TO_EXPERION_Con','MSID_Labor_TCMI_Con']

for container in containers:
    if getContainer(container).Rows.Count > 0:
        calculateTotals(getContainer(container))

projectManagementCon = getContainer("MSID_Labor_Project_Management")
if projectManagementCon.Rows.Count > 0:
    #totalCalculatedHrs = 0
    totalFinalHrs = 0
    for row in projectManagementCon.Rows:
        if row["Deliverable_Type"] in ("Offsite","Off-Site"):
            if row["Final_Hrs"] != "0":
                #totalCalculatedHrs = totalCalculatedHrs + getFloat(row["Calculated_Hrs"])
                totalFinalHrs = totalFinalHrs + getFloat(row["Final_Hrs"])
    for row in projectManagementCon.Rows:
        if row["Deliverable"] == "Total":
            #row["Calculated_Hrs"] = str(totalCalculatedHrs)
            row["Final_Hrs"] = str(totalFinalHrs)
    projectManagementCon.Calculate()
