def getContainer(product,Name):
    return product.GetContainerByName(Name)

def getFloat(Var):
    if Var:
        return float(Var)
    return 0

def addFinalHours(totalDict, key, value):
    totalDict[key] = getFloat(totalDict.get(key, 0)) + getFloat(value)

def getExecutionCountry():
    marketCode = Quote.SelectedMarket.MarketCode
    salesOrg = marketCode.partition('_')[0]
    #query = SqlHelper.GetFirst("select Execution_County from EXECUTION_COUNTRY_SALES_ORG_MAPPING where Execution_Country_Sales_Org = '{}'".format(salesOrg))
    #Update for Defect CXCPQ-27359
    currency = marketCode.partition('_')[2]
    query = SqlHelper.GetFirst("select Execution_County from NEW_EXECUTION_COUNTRY_SALES_ORG_MAPPING where Sales_Area = '{}' and Currency = '{}'".format(salesOrg,currency))
    if query is not None:
        return query.Execution_County

def getFinalHours(msidProduct,container):
    for row in getContainer(msidProduct,container).Rows:
        if row["Deliverable"] not in ('Off-Site','On-Site','Total'):
            if row["Execution_Country"] == excecutionCountry and row["Final_Hrs"] not in ('',"0") and row["FO_Eng"] != '' and row["FO_Eng_Percentage_Split"] != '0':
                addFinalHours(laboHours, "Local Labor", round(getFloat(row["Final_Hrs"]) * getFloat(row["FO_Eng_Percentage_Split"]) / 100))
            elif row["Final_Hrs"] not in ('',"0") and row["FO_Eng"] != '' and row["FO_Eng_Percentage_Split"] != '0':
                addFinalHours(laboHours, "Cross Border Labor", round(getFloat(row["Final_Hrs"]) * getFloat(row["FO_Eng_Percentage_Split"]) / 100))
            if row["Final_Hrs"] not in ('',"0") and row["GES_Eng"] != '' and row["GES_Eng_Percentage_Split"] != '0':
                if row["GES_Eng"] in ('SVC_GES_P350B_IN','SVC_GES_P350B_CN','SVC_GES_P350B_RO','SVC_GES_P350B_UZ','SVC_GES_P335B_IN','SVC_GES_P335B_CN','SVC_GES_P335B_RO','SVC_GES_P335B_UZ','SVC_GES_P215B_IN','SVC_GES_P215B_CN','SVC_GES_P215B_RO','SVC_GES_P215B_UZ'):
                    addFinalHours(laboHours, "GES - Work @ GES Location", round(getFloat(row["Final_Hrs"]) * getFloat(row["GES_Eng_Percentage_Split"]) / 100))
                else:
                    addFinalHours(laboHours, "GES - Work @ Non GES Location", round(getFloat(row["Final_Hrs"]) * getFloat(row["GES_Eng_Percentage_Split"]) / 100))

laboHours = dict()
excecutionCountry = getExecutionCountry()
selectedProducts = Product.Attr('MSID_Selected_Products').GetValue().split('<br>')

msidContainer = Product.GetContainerByName("Migration_MSID_Selection_Container")
for row in msidContainer.Rows:
    msidProduct = row.Product
    getFinalHours(msidProduct,"MSID_Labor_OPM_Engineering") if "OPM" in selectedProducts else 0
    getFinalHours(msidProduct,"MSID_Labor_LCN_One_Time_Upgrade_Engineering") if "LCN One Time Upgrade" in selectedProducts else 0
    getFinalHours(msidProduct,"MSID_Labor_EBR_Con") if "EBR" in selectedProducts else 0
    getFinalHours(msidProduct,"MSID_Labor_ELCN_Con") if "ELCN" in selectedProducts else 0
    getFinalHours(msidProduct,"MSID_Labor_Orion_Console_Con") if "Orion Console" in selectedProducts else 0
    getFinalHours(msidProduct,"MSID_Labor_EHPM_C300PM_Con") if "EHPM/ C300PM" in selectedProducts else 0
    getFinalHours(msidProduct,"MSID_Labor_TPS_TO_EXPERION_Con") if "TPS to Experion" in selectedProducts else 0
    getFinalHours(msidProduct,"MSID_Labor_TCMI_Con") if "TCMI" in selectedProducts else 0
    getFinalHours(msidProduct,"MSID_Labor_C200_Migration_Con") if "C200 Migration" in selectedProducts else 0
    getFinalHours(msidProduct,"MSID_Labor_CB-EC_Upgrade_to_C300-UHIO_con") if "CB-EC Upgrade to C300-UHIO" in selectedProducts else 0
    getFinalHours(msidProduct,"MSID_Labor_xPM_to_C300_Migration_Con") if "xPM to C300 Migration" in selectedProducts else 0
    getFinalHours(msidProduct,"MSID_Labor_FDM_Upgrade_Con") if "FDM Upgrade" in selectedProducts else 0
    getFinalHours(msidProduct,"MSID_Labor_FSC_to_SM_con") if "FSC to SM" in selectedProducts else 0
    getFinalHours(msidProduct,"MSID_Labor_FSC_to_SM_audit_Con") if "FSC to SM" in selectedProducts else 0
    getFinalHours(msidProduct,"MSID_Labor_LM_to_ELMM_Con") if "LM to ELMM ControlEdge PLC" in selectedProducts else 0
    getFinalHours(msidProduct,"MSID_Labor_EHPM_HART_IO_Con") if "EHPM HART IO" in selectedProducts else 0
    getFinalHours(msidProduct,"MSID_Labor_XP10_Actuator_Upgrade_con") if "XP10 Actuator Upgrade" in selectedProducts else 0
    getFinalHours(msidProduct,"MSID_Labor_Graphics_Migration_con") if "Graphics Migration" in selectedProducts else 0
    getFinalHours(msidProduct,"MSID_Labor_CD_Actuator_con") if "CD Actuator I-F Upgrade" in selectedProducts else 0
    getFinalHours(msidProduct,"MSID_Labor_Project_Management")

Trace.Write(str(laboHours))

'''
laborFields = ['Local Labor','Cross Border Labor','GES - Work @ GES Location','GES - Work @ Non GES Location','Total GES Hours','Total Labor']
laborGESTable = Quote.QuoteTables["EGAP_Labor_and_Engineering_Service"]
laborGESTable.Rows.Clear()
totalLabor = laboHours.get("Local Labor",0) + laboHours.get("Cross Border Labor",0) + laboHours.get("GES - Work @ GES Location",0) + laboHours.get("GES - Work @ Non GES Location",0)
for field in laborFields:
    addRow = laborGESTable.AddNewRow()
    if field == "Total GES Hours":
        addRow["EGAP_Labor_Field_Details"] = field
        addRow["EGAP_Labor_Hours"] = laboHours.get("GES - Work @ GES Location",0) + laboHours.get("GES - Work @ Non GES Location",0)
        addRow["EGAP_Labor_Pct"] = round(((laboHours.get("GES - Work @ GES Location",0) + laboHours.get("GES - Work @ Non GES Location",0)) / totalLabor * 100) ,2)
    elif field == "Total Labor":
        addRow["EGAP_Labor_Field_Details"] = field
        addRow["EGAP_Labor_Hours"] = totalLabor
        addRow["EGAP_Labor_Pct"] = 100
    else:
        addRow["EGAP_Labor_Field_Details"] = field
        addRow["EGAP_Labor_Hours"] = laboHours.get(field,0)
        addRow["EGAP_Labor_Pct"] = round(((laboHours.get(field,0) / totalLabor) * 100),2)
laborGESTable.Save()'''
#To Populate QuoteItemCustom Fields
Local_Labor = laboHours.get("Local Labor",0)
Cross_Border_Labor = laboHours.get("Cross Border Labor",0)
GES_Location = laboHours.get("GES - Work @ GES Location",0)
Non_GES_Location = laboHours.get("GES - Work @ Non GES Location",0)
items = arg.QuoteItemCollection
for item in items:
    Trace.Write(item.ProductName + '-------')
    if item.ProductName == "Migration":
        item["QI_Local_Labor"].Value = Local_Labor
        item["QI_Cross_Border_Labor"].Value = Cross_Border_Labor
        item["QI_GES_Work_GES_Location"].Value = GES_Location
        item["QI_GES_Work_Non_GES_Location"].Value = Non_GES_Location
        break
Quote.Calculate(1)