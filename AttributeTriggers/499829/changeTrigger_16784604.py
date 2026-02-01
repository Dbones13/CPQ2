def getContainer(Name):
    return Product.GetContainerByName(Name)
def getAttrValue(Name):
    return Product.Attr(Name).GetValue()


containers = ['Trace_Software_Labor_con','Trace_Project_Management_Labor_con']

if getAttrValue("Trace_software_GES_Location") != 'None':
    #ScriptExecutor.Execute('PS_PopulatePartNumberContainer')
    for container in containers:
        if container != "MSID_Additional_Custom_Deliverables":
            for row in getContainer(container).Rows:
                if row["Deliverable_Type"] in ("Offsite","Off-Site") and container != "Trace_Project_Management_Labor_con":
                    Trace.Write("Check1" +","+ str(container))
                    row["GES_Eng"] = "SVC_GES_P350B_{}".format(TagParserProduct.ParseString('<*ValueCode(Trace_software_GES_Location)*>'))
                elif row["Deliverable_Type"] in ("Offsite","Off-Site") and container == "Trace_Project_Management_Labor_con":
                    Trace.Write("Check2" +","+ str(container))
                    row["GES_Eng"] = "SVC_GES_P215B_{}".format(TagParserProduct.ParseString('<*ValueCode(Trace_software_GES_Location)*>'))
                if row["Deliverable_Type"] in ("Onsite","On-Site"):
                    row["GES_Eng"] = "SVC_GES_P350F_{}".format(TagParserProduct.ParseString('<*ValueCode(Trace_software_GES_Location)*>'))
            #showGESColumns(container)
else:
    for container in containers:
        for row in getContainer(container).Rows:
            if row["Deliverable"] not in ('Total','Off-Site','On-Site'):
                row["GES_Eng_Percentage_Split"] = "0"
                row["FO_Eng_Percentage_Split"] = "100"
        
ScriptExecutor.Execute('PopulatePartNumberContainer')