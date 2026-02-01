def getContainer(Name):
    return Product.GetContainerByName(Name)

def getAttrValue(Name):
    return Product.Attr(Name).GetValue()

def setAttrValue(Name,value):
    Product.Attr(Name).AssignValue(value)

def getFloat(Var):
    if Var:
        return float(Var)
    return 0

def getContainerData(container):
    containerData = {}
    for row in container.Rows:
        containerData[row.RowIndex] = dict()
        for column in row.Columns:
            containerData[row.RowIndex][column.Name] = row[column.Name]
        containerData[row.RowIndex]["SelectedRow"] = row.IsSelected
    return containerData

def updateTotals(container):
    totalOffSiteFinalHrs = 0
    totalOnSiteFinalHrs = 0
    totalFinalHrs = 0
    for row in container.Rows:
        if row["Deliverable_Type"] in ("Offsite","Off-Site"):
            totalOffSiteFinalHrs = totalOffSiteFinalHrs + getFloat(row["Final_Hrs"])
        elif row["Deliverable_Type"] in ("Onsite","On-Site"):
            totalOnSiteFinalHrs = totalOnSiteFinalHrs + getFloat(row["Final_Hrs"])
        totalFinalHrs = totalOffSiteFinalHrs + totalOnSiteFinalHrs
    for row in container.Rows:
        if row["Deliverable"] == "Off-Site":
            row["Final_Hrs"] = str(totalOffSiteFinalHrs)
        elif row["Deliverable"] == "On-Site":
            row["Final_Hrs"] = str(totalOnSiteFinalHrs)
        elif row["Deliverable"] == "Total":
            row["Final_Hrs"] = str(totalFinalHrs)
    container.Calculate()

def populateOPM(container,row):
    deliverablePresent = False
    for Row in container.Rows:
        if Row["Deliverable"] == row["Deliverable_Name"]:
            Row["Final_Hrs"] = row["Final_Hrs"]
            Row["Deliverable_Type"] = row["Type"]
            Row["FO_Eng"] = row["FO_Eng"]
            Row["FO_Eng_Percentage_Split"] = row["FO_Eng_Percentage_Split"]
            Row["GES_Eng"] = row["GES_Eng"]
            Row["GES_Eng_Percentage_Split"] = row["GES_Eng_Percentage_Split"]
            Row["Standard_Deliverable_Selection"] = row["Deliverable"]
            Row["Manual_Entry"] = row["Manual_Entry"]
            Row["Regional_Cost"] = row["Regional_Cost"]
            Row["GES_Regional_Cost"] = row["GES_Regional_Cost"]
            Row["Execution_Year"] = row["Execution_Year"]
            Row["Execution_Country"] = row["Execution_Country"]
            Row["FOUnitWTWCost"] = row["FOUnitWTWCost"]
            Row["FO_ListPrice"] = row["FO_ListPrice"]
            Row["Standard Deliverable selection"] = row["Deliverable"]
            deliverablePresent = True
    if not deliverablePresent:
        if row["Product_Module"] in ('Trace Software') and row["Type"] == "Off-Site":
            containerData = getContainerData(container)
            container.Rows.Clear()
            for data in containerData:
                if containerData[data]["Deliverable"] == "On-Site":
                    addRow = container.AddNewRow(False)
                    addRow["Deliverable"] = row["Deliverable_Name"]
                    addRow["Calculated_Hrs"] = "0.00"
                    addRow["Adjustment_Productivity"] = "1"
                    addRow["Final_Hrs"] = row["Final_Hrs"]
                    addRow["FO_Eng"] = row["FO_Eng"]
                    addRow["FO_Eng_Percentage_Split"] = row["FO_Eng_Percentage_Split"]
                    addRow["GES_Eng"] = row["GES_Eng"]
                    addRow["GES_Eng_Percentage_Split"] = row["GES_Eng_Percentage_Split"]
                    addRow["Standard_Deliverable_Selection"] = row["Deliverable"]
                    addRow["Manual_Entry"] = row["Manual_Entry"]
                    addRow["Regional_Cost"] = row["Regional_Cost"]
                    addRow["GES_Regional_Cost"] = row["GES_Regional_Cost"]
                    addRow["Execution_Year"] = row["Execution_Year"]
                    addRow["Execution_Country"] = row["Execution_Country"]
                    addRow["FOUnitWTWCost"] = row["FOUnitWTWCost"]
                    addRow["FO_ListPrice"] = row["FO_ListPrice"]
                    addRow["Deliverable_Type"] = row["Type"]
                    addRow["Standard Deliverable selection"] = row["Deliverable"]

                addRow = container.AddNewRow(False)
                for column in addRow.Columns:
                    for key,value in containerData[data].items():
                        if column.Name == key:
                            addRow[column.Name] = value
                    if containerData[data]["SelectedRow"] == True and addRow.IsSelected == False:
                        addRow.IsSelected = True
        else:
            addRow = container.AddNewRow(False)
            addRow["Deliverable"] = row["Deliverable_Name"]
            addRow["Calculated_Hrs"] = "0.00"
            addRow["Adjustment_Productivity"] = "1"
            addRow["Final_Hrs"] = row["Final_Hrs"]
            addRow["FO_Eng"] = row["FO_Eng"]
            addRow["FO_Eng_Percentage_Split"] = row["FO_Eng_Percentage_Split"]
            addRow["GES_Eng"] = row["GES_Eng"]
            addRow["GES_Eng_Percentage_Split"] = row["GES_Eng_Percentage_Split"]
            addRow["Standard_Deliverable_Selection"] = row["Deliverable"]
            addRow["Manual_Entry"] = row["Manual_Entry"]
            addRow["Regional_Cost"] = row["Regional_Cost"]
            addRow["GES_Regional_Cost"] = row["GES_Regional_Cost"]
            addRow["Execution_Year"] = row["Execution_Year"]
            addRow["Execution_Country"] = row["Execution_Country"]
            addRow["FOUnitWTWCost"] = row["FOUnitWTWCost"]
            addRow["FO_ListPrice"] = row["FO_ListPrice"]
            addRow["Deliverable_Type"] = row["Type"]
            addRow["Standard Deliverable selection"] = row["Deliverable"]
    container.Calculate()
    setAttrValue("MSID_Labor_Message","Deliverables has been successfully applied")



additonalCustomDelivCon = getContainer("Trace_Additional_Custom_Deliverables")
projectManagementCon = getContainer("Trace_Project_Management_Labor_con")
TraceCon = getContainer("Trace_Software_Labor_con")


setAttrValue("MSID_Labor_Message",'')
setAttrValue("IncompleteAdditionalDeliverables",'')

if additonalCustomDelivCon.Rows.Count > 0:
    for row in additonalCustomDelivCon.Rows:
        if row["Deliverable_Name"] == '':
            setAttrValue("MSID_Labor_Message","Deliverable Name is empty. Please enter the deliverable Name.")
            setAttrValue("IncompleteAdditionalDeliverables","1")

            break
        elif row["Final_Hrs"] == '':
            setAttrValue("MSID_Labor_Message","Final Hrs is empty. Please enter the Final Hours.")
            setAttrValue("IncompleteAdditionalDeliverables","1")

            break
        elif row["FO_Eng"] == '':
            setAttrValue("MSID_Labor_Message","FO Eng is empty. Please apply Fo Eng material.")
            setAttrValue("IncompleteAdditionalDeliverables","1")

            break
        elif row["GES_Eng"] == '' and Product.Attr('Trace_software_GES_Location').GetValue() != 'None' and row["FO_Eng_Percentage_Split"] != "100":
            setAttrValue("MSID_Labor_Message","GES Eng is empty. Please apply GES Eng material.")
            setAttrValue("IncompleteAdditionalDeliverables","1")
            break
        elif row["Execution_Country"] == '':
            setAttrValue("MSID_Labor_Message","Execution Country is empty. Please apply Execution Country.")
            setAttrValue("IncompleteAdditionalDeliverables","1")
            break
        elif row["Execution_Year"] == '':
            setAttrValue("MSID_Labor_Message","Execution Year is empty. Please apply Execution Year.")
            setAttrValue("IncompleteAdditionalDeliverables","1")
            break

        if row["Product_Module"] == "Trace Software":
            populateOPM(TraceCon,row)
            updateTotals(TraceCon)

        elif row["Product_Module"] == "PM":
            populateOPM(projectManagementCon,row)
    ScriptExecutor.ExecuteGlobal('GS_CalculateLaborHoursTotals')