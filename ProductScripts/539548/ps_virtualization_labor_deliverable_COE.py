isR2Qquote = True if Quote.GetCustomField("isR2QRequest").Content else False
if not isR2Qquote:
    from GS_MigrationLaborHoursModule_4 import calculateFinalHours1
    container1 = Product.GetContainerByName('MSID_Labor_Virtualization_con')
    scope = Product.Attr('MIgration_Scope_Choices').GetValue()
    def getContainer(Name):
        return Product.GetContainerByName(Name)

    def getFloat(Var):
        if Var:
            return float(Var)
        return 0

    #Virtualization_hidden_cont = Product.GetContainerByName("MSID_Product_Container_Virtualization_hidden").Rows.Count
    Virtualization_hidden_cont = 0
    for item in Product.GetContainerByName('CONT_MSID_SUBPRD').Rows:
        if item['Selected_Products'] == 'Virtualization System Migration':
            Virtualization_hidden_cont += 1
    Trace.Write("Virtualization_hidden_cont"+str(Virtualization_hidden_cont))
    if (scope == 'HW/SW/LABOR' or scope == 'LABOR') and (Virtualization_hidden_cont >0):
        totalOffSiteFinalHrs = 0
        totalOnSiteFinalHrs = 0
        totalFinalHrs = 0
        newdiffCOE = 0
        a = 0
        Principle_eff_final_hrs=0
        RMP_Effort = Product.Attr('Regional_Migration_Principal_Efforts_Required').GetValue()
        for row in container1.Rows:
            if row["Deliverable"] in ["Plan review & Kick off Meetings","HW/SW order to factory","Configuration","FAT","On Site activities","SAT"]:
                a += getFloat(row["Final_Hrs"])
            if row["Deliverable"] not in ["Virtualization CoE","Off-Site","On-Site","Total","Regional Migration Principal Efforts"]:
                Principle_eff_final_hrs+=getFloat(row["Final_Hrs"])
        a = a*0.1
        for row in container1.Rows:
            if row["Deliverable"] == "Virtualization CoE":
                oldCOEValue = getFloat(row["Calculated_Hrs"])
                row["Calculated_Hrs"] = str(a)
                newdiffCOE = getFloat(row["Calculated_Hrs"]) - oldCOEValue
                row["Final_Hrs"] = str(round(getFloat(row["Calculated_Hrs"]) * getFloat(row["Adjustment_Productivity"])))
                a=row["Final_Hrs"]
                row.Calculate()
            if RMP_Effort=="Yes" and row["Deliverable"] == "Regional Migration Principal Efforts":
                oldCalHrs = row["Calculated_Hrs"]
                Principle_eff_final_hrs = (Principle_eff_final_hrs+int(getFloat(a)))*8/100
                row["Calculated_Hrs"] = str(Principle_eff_final_hrs)
                Product.Attr('msid_Virtualization_RMP_Efforts').AssignValue(str(Principle_eff_final_hrs))
                row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
                row.Calculate()
            elif row["Deliverable"] == "Regional Migration Principal Efforts":
                oldCalHrs = row["Calculated_Hrs"]
                row["Calculated_Hrs"] = '0'
                row["Final_Hrs"]=calculateFinalHours1(row,oldCalHrs)
                Product.Attr('msid_Virtualization_RMP_Efforts').AssignValue('0')
                row.Calculate()
            if row["Deliverable_Type"] in ("Offsite","Off-Site"):
                totalOffSiteFinalHrs = totalOffSiteFinalHrs + getFloat(row["Final_Hrs"])
            elif row["Deliverable_Type"] in ("Onsite","On-Site"):
                totalOnSiteFinalHrs = totalOnSiteFinalHrs + getFloat(row["Final_Hrs"])
            totalFinalHrs = totalOffSiteFinalHrs + totalOnSiteFinalHrs
        for row in container1.Rows:
            if row["Deliverable"] == "Off-Site":
                row["Calculated_Hrs"] = str(getFloat(row["Calculated_Hrs"]) + getFloat(newdiffCOE))
                row["Final_Hrs"] = str(totalOffSiteFinalHrs)
            elif row["Deliverable"] == "On-Site":
                row["Final_Hrs"] = str(totalOnSiteFinalHrs)
            elif row["Deliverable"] == "Total":
                row["Calculated_Hrs"] = str(getFloat(row["Calculated_Hrs"]) + getFloat(newdiffCOE))
                row["Final_Hrs"] = str(totalFinalHrs)
        #ScriptExecutor.Execute('PS_PopulateGESCost')
        #ScriptExecutor.Execute('PS_CalculateProjectManagementLaborHours')
    container1.Calculate()