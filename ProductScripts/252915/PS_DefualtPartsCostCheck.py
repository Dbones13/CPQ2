def getContainer(Name):
    return Product.GetContainerByName(Name)

def setAttrValue(Name,value):
    Product.Attr(Name).AssignValue(value)

foPartNumberCon = getContainer("MSID_Labor_FO_Part_Number")
opmEngineeringCon = getContainer("MSID_Labor_OPM_Engineering")
lcnOneTimeUpgradeCon = getContainer("MSID_Labor_LCN_One_Time_Upgrade_Engineering")
projectManagementCon = getContainer("MSID_Labor_Project_Management")
setAttrValue("Labor_OPM_Message",'')
setAttrValue("Labor_LCN_Message",'')
setAttrValue("Labor_PM_Message",'')
for Row in foPartNumberCon.Rows:
    if Row["Product_Module"] == "OPM":
        if Row["FO_Part_Number"] in ('SVC-EST1-ST','SVC-EST1-ST-NC') and Row["Cost"] in ("0.00",''):
            for row in opmEngineeringCon.Rows:
                if row["FO_Eng"] in ('SVC-EST1-ST','SVC-EST1-ST-NC'):
                    row["FO_Eng"] = ''
                    setAttrValue("Labor_OPM_Message",'The Cost of the Default Part Number is not available and you need to provide the Cost as manual entry in below Column to select that default partNumber')
        if Row["GES_Part_Number"] == "SVC_GES_P350B_{}".format(TagParserProduct.ParseString('<*ValueCode(MSID_GES_Location)*>')) and Row["Cost"] in ("0.00",''):
            for row in opmEngineeringCon.Rows:
                if row["GES_Eng"] == "SVC_GES_P350B_{}".format(TagParserProduct.ParseString('<*ValueCode(MSID_GES_Location)*>')):
                    row["GES_Eng"] = ''
                    setAttrValue("Labor_OPM_Message",'The Cost of the Default GES Part Number is not available')
        
        if Row["GES_Part_Number"] == "SVC_GES_P350F_{}".format(TagParserProduct.ParseString('<*ValueCode(MSID_GES_Location)*>')) and Row["Cost"] in ("0.00",''):
            for row in opmEngineeringCon.Rows:
                if row["GES_Eng"] == "SVC_GES_P350F_{}".format(TagParserProduct.ParseString('<*ValueCode(MSID_GES_Location)*>')):
                    row["GES_Eng"] = ''
                    setAttrValue("Labor_OPM_Message",'The Cost of the Default GES Part Number is not available')

    if Row["Product_Module"] == "LCN":
        if Row["FO_Part_Number"] in ('SVC-EAPS-ST','SVC-EAPS-ST-NC') and Row["Cost"] in ("0.00",''):
            for row in lcnOneTimeUpgradeCon.Rows:
                if row["FO_Eng"] in ('SVC-EAPS-ST','SVC-EAPS-ST-NC'):
                    row["FO_Eng"] = ''
                    setAttrValue("Labor_LCN_Message",'The Cost of the Default Part Number is not available and you need to provide the Cost as manual entry in below Column to select that default partNumber')
        if Row["GES_Part_Number"] == "SVC_GES_P350B_{}".format(TagParserProduct.ParseString('<*ValueCode(MSID_GES_Location)*>')) and Row["Cost"] in ("0.00",''):
            for row in lcnOneTimeUpgradeCon.Rows:
                if row["GES_Eng"] == "SVC_GES_P350B_{}".format(TagParserProduct.ParseString('<*ValueCode(MSID_GES_Location)*>')):
                    row["GES_Eng"] = ''
                    setAttrValue("Labor_OPM_Message",'The Cost of the Default GES Part Number is not available')

    if Row["Product_Module"] in ('PM','PA'):
        if Row["FO_Part_Number"] in ('SVC-PMGT-ST','SVC-PMGT-ST-NC') and Row["Cost"] in ("0.00",''):
            for row in projectManagementCon.Rows:
                if row["FO_Eng"] in ('SVC-PMGT-ST','SVC-PMGT-ST-NC'):
                    row["FO_Eng"] = ''
                    setAttrValue("Labor_PM_Message",'The Cost of the Default Part Number is not available and you need to provide the Cost as manual entry in below Column to select that default partNumber')
        if Row["FO_Part_Number"] in ('SVC-PADM-ST','SVC-PADM-ST-NC') and Row["Cost"]in (''):
            for row in projectManagementCon.Rows:
                if row["FO_Eng"] in ('SVC-PADM-ST','SVC-PADM-ST-NC'):
                    row["FO_Eng"] = ''
                    setAttrValue("Labor_PM_Message",'The Cost of the Default Part Number is not available and you need to provide the Cost as manual entry in below Column to select that default partNumber')

        if Row["GES_Part_Number"] == "SVC_GES_P215B_{}".format(TagParserProduct.ParseString('<*ValueCode(MSID_GES_Location)*>')) and Row["Cost"] in ("0.00",''):
            for row in projectManagementCon.Rows:
                if row["GES_Eng"] == "SVC_GES_P215B_{}".format(TagParserProduct.ParseString('<*ValueCode(MSID_GES_Location)*>')):
                    row["GES_Eng"] = ''
                    setAttrValue("Labor_OPM_Message",'The Cost of the Default GES Part Number is not available')