def getContainer(Name):
    return Product.GetContainerByName(Name)

def setAttrValue(Name,value):
    Product.Attr(Name).AssignValue(value)

def populateFoEngColumn(container,row):
    for Row in container.Rows:
        if Row["Deliverable"] not in ('Total','Off-Site','On-Site') and Row.IsSelected:
            if row["Product_Module"] in ('Trace Software'):
                Row["FO_Eng"] = row["FO_Part_Number"]
                Row["Regional_Cost"] = row["Cost"]
                Row["Manual_Entry"] = row["Manual_Entry"]
            elif row["Product_Module"] == "PM" and Row["Deliverable_Flag"] == "PM":
                Row["FO_Eng"] = row["FO_Part_Number"]
                Row["Regional_Cost"] = row["Cost"]
                Row["Manual_Entry"] = row["Manual_Entry"]
            elif row["Product_Module"] == "PA" and Row["Deliverable_Flag"] == "PA":
                Row["FO_Eng"] = row["FO_Part_Number"]
                Row["Regional_Cost"] = row["Cost"]
                Row["Manual_Entry"] = row["Manual_Entry"]
            #Row.IsSelected = False
            row.IsSelected = False

def populateGesEngColumn(container,row):
    for Row in container.Rows:
        if Row["Deliverable"] not in ('Total','Off-Site','On-Site') and Row.IsSelected:
            if row["Product_Module"] in ('Trace Software'):
                Row["GES_Eng"] = row["GES_Part_Number"]
            elif row["Product_Module"] == "PM":
                Row["GES_Eng"] = row["GES_Part_Number"]
            #Row.IsSelected = False
            row.IsSelected = False

foPartNumberCon = getContainer("MSID_Labor_FO_Part_Number_T_Software")
foPartNumberTrace= getContainer("MSID_Labor_FO_Part_Number_Trace")
fopartNumberPM = getContainer("MSID_Labor_FO_Part_Number_PM")
TraceCon = getContainer("Trace_Software_Labor_con")
projectManagementCon = getContainer("Trace_Project_Management_Labor_con")
additonalCustomDelivCon = getContainer("Trace_Additional_Custom_Deliverables")

laborMessagesAttrs = ['Labor_PM_Message','MSID_Labor_Message','Labor_Trace_Software_Message']
for attrName in laborMessagesAttrs:
    setAttrValue(attrName,'')


for row in foPartNumberTrace.Rows:
    if row.IsSelected and row["Cost"] not in ("0.00",'') and row["GES_Part_Number"] == '':
        if row["Product_Module"] == "Trace Software":
            if row["ListPrice"] not in ("0.00",'',"0"):
                populateFoEngColumn(TraceCon,row)
            else:
                setAttrValue("Labor_Trace_Software_Message",'Part Cannot be applied over activity as the selected Part Number does not have a list price.')
    if row.IsSelected and row["GES_Part_Number"] != '':
        if row["Product_Module"] == "Trace Software":
            populateGesEngColumn(TraceCon,row)

for row in fopartNumberPM.Rows:
    if row.IsSelected and row["Cost"] not in ("0.00",'') and row["GES_Part_Number"] == '':
        if row["Product_Module"] in ('PA','PM'):
            if row["ListPrice"] not in ("0.00",'',"0"):
                populateFoEngColumn(projectManagementCon,row)
            else:
                setAttrValue("Labor_PM_Message",'Part Cannot be applied over activity as the selected Part Number does not have a list price.')
    if row.IsSelected and row["GES_Part_Number"] != '':
        if row["Product_Module"] == "PM":
            populateGesEngColumn(projectManagementCon,row)


for row in foPartNumberCon.Rows:
    if row.IsSelected and row["Cost"] not in ("0.00",'') and row["GES_Part_Number"] == '':
        if row["Product_Module"] in ('PM','PA','Trace Software'):
            if additonalCustomDelivCon.Rows.Count > 0:
                for Row in additonalCustomDelivCon.Rows:
                    if Row.IsSelected:
                        if row["ListPrice"] not in ("0.00",'',"0"):
                            if row["Product_Module"] not in ('PM','PA'):
                                if Row["Product_Module"] == row["Product_Module"]:
                                    Row["FO_Eng"] = row["FO_Part_Number"]
                                    Row["Regional_Cost"] = row["Cost"]
                                    Row["Manual_Entry"] = row["Manual_Entry"]
                                    #Row.IsSelected = False
                            else:
                                if Row["Product_Module"] == row["Product_Module"]:
                                    Row["FO_Eng"] = row["FO_Part_Number"]
                                    Row["Regional_Cost"] = row["Cost"]
                                    Row["Manual_Entry"] = row["Manual_Entry"]
                                    #Row.IsSelected = False
                            row.IsSelected = False
                        else:
                            setAttrValue("MSID_Labor_Message",'Part Cannot be applied over activity as the selected Part Number does not have a list price.')
    if row.IsSelected and row["GES_Part_Number"] != '':

        if row["Product_Module"] in ('PM','PA','Trace Software'):
            if additonalCustomDelivCon.Rows.Count > 0:
                for Row in additonalCustomDelivCon.Rows:
                    if Row.IsSelected:
                        if Row["Product_Module"] == row["Product_Module"]:
                            Row["GES_Eng"] = row["GES_Part_Number"]
                            #Row.IsSelected = False
                            row.IsSelected = False
ScriptExecutor.Execute('PS_PopulateGESCost')