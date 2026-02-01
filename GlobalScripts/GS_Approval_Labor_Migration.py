def getContainer(item,Name,Quote,RowIndex):
	containers=[]
	for i in range(len(Name)):
		if item.ProductName=="Migration":
			child=Quote_child_items(item,RowIndex)
									 
			container_name=child.SelectedAttributes.GetContainerByName(Name[i])
		if item.ProductName=="MSID_New":
			container_name=item.SelectedAttributes.GetContainerByName(Name[i])
		if container_name:
			containers.append(container_name)
	return containers

def getFloat(Var):
	if Var:
		return float(Var)
	return 0

def Quote_child_items(item,RowIndex):
	count=0
	for child in item.Children:  
																																											
		if child.ProductName == "MSID" or child.ProductName == "MSID_New" and count==RowIndex:
											   
			return child
		elif child.ProductName == "MSID" or child.ProductName == "MSID_New":
									   
			count+=1
def addFinalHours(totalDict, key, value):
	totalDict[key] = getFloat(totalDict.get(key, 0)) + getFloat(value)
	return totalDict[key]

def getExecutionCountry(quote):
	marketCode = quote.SelectedMarket.MarketCode
	salesOrg = quote.GetCustomField('Sales Area').Content
	currency = quote.GetCustomField('Currency').Content
	query = SqlHelper.GetFirst("select Execution_County from NEW_EXECUTION_COUNTRY_SALES_ORG_MAPPING where Sales_Area = '{}' and Currency = '{}'".format(salesOrg,currency))
	if query is not None:
		return query.Execution_County

def getFinalHours(item,container,Quote,RowIndex):
									  
	laboHours = {}
	prdcontainers=getContainer(item,container,Quote,RowIndex)
	for prodcontainer in prdcontainers:
		for row in prodcontainer.Rows:
						
			if row["Deliverable"] not in ('Off-Site','On-Site','Total'):
				excecutionCountry=getExecutionCountry(Quote)
				if row["Execution_Country"] == excecutionCountry and row["Final_Hrs"] not in ('',"0") and row["FO_Eng"] != '' and row["FO_Eng_Percentage_Split"] != '0':
					addFinalHours(laboHours, "Local Labor", round(getFloat(row["Final_Hrs"]) * getFloat(row["FO_Eng_Percentage_Split"]) / 100))
				elif row["Final_Hrs"] not in ('',"0") and row["FO_Eng"] != '' and row["FO_Eng_Percentage_Split"] != '0':
					addFinalHours(laboHours, "Cross Border Labor", round(getFloat(row["Final_Hrs"]) * getFloat(row["FO_Eng_Percentage_Split"]) / 100))
				if row["Final_Hrs"] not in ('',"0") and row["GES_Eng"] != '' and row["GES_Eng_Percentage_Split"] != '0':
					GES_Eng=row["GES_Eng"]
					if GES_Eng in ('SVC_GES_P350B_IN','SVC_GES_P350B_CN','SVC_GES_P350B_RO','SVC_GES_P350B_UZ','SVC_GES_P335B_IN','SVC_GES_P335B_CN','SVC_GES_P335B_RO','SVC_GES_P335B_UZ','SVC_GES_P215B_IN','SVC_GES_P215B_CN','SVC_GES_P215B_RO','SVC_GES_P215B_UZ','SVC_GES_PLCB_IN','SVC_GES_PLCB_CN','SVC_GES_PLCB_RO','SVC_GES_PLCB_UZ','HPS_GES_P350B_IN','HPS_GES_P350B_CN','HPS_GES_P350B_RO','HPS_GES_P350B_UZ','HPS_GES_P335B_IN','HPS_GES_P335B_CN','HPS_GES_P335B_RO','HPS_GES_P335B_UZ','HPS_GES_P215B_IN','HPS_GES_P215B_CN','HPS_GES_P215B_RO','HPS_GES_P215B_UZ','SVC_GES_P350B_EG','SVC_GES_P335B_EG','SVC_GES_PLCB_EG','SVC_GES_P215B_EG','SVC_GES_P215F_EG'):
						addFinalHours(laboHours, "GES - Work @ GES Location", round(getFloat(row["Final_Hrs"]) * getFloat(row["GES_Eng_Percentage_Split"]) / 100))
					elif GES_Eng in ('SVC_GES_P350F_IN','SVC_GES_P350F_CN','SVC_GES_P350F_RO','SVC_GES_P350F_UZ','SVC_GES_P335F_IN','SVC_GES_P335F_CN','SVC_GES_P335F_RO','SVC_GES_P335F_UZ','SVC_GES_P215F_IN','SVC_GES_P215F_CN','SVC_GES_P215F_RO','SVC_GES_P215F_UZ','SVC_GES_PLCF_IN','SVC_GES_PLCF_CN','SVC_GES_PLCF_RO','SVC_GES_PLCF_UZ','HPS_GES_P350F_IN','HPS_GES_P350F_CN','HPS_GES_P350F_RO','HPS_GES_P350F_UZ','HPS_GES_P215F_CN','HPS_GES_P215F_IN','HPS_GES_P215F_RO','HPS_GES_P215F_UZ','HPS_GES_P335F_CN','HPS_GES_P335F_IN','HPS_GES_P335F_RO','HPS_GES_P335F_UZ','SVC_GES_P350F_EG','SVC_GES_P335F_EG','SVC_GES_P215B_EG','SVC_GES_P215F_EG'):
						addFinalHours(laboHours, "GES - Work @ Non GES Location", round(getFloat(row["Final_Hrs"]) * getFloat(row["GES_Eng_Percentage_Split"]) / 100))
											
	return laboHours
def getFinalHoursCyber(item,container,Quote):
	laboHours = {}
	for prodcontainer in container:
		for row in item.SelectedAttributes.GetContainerByName(prodcontainer).Rows:
			if prodcontainer !='Cyber_Labor_Project_Management':
				partNumber = row["PartNumber"]
				hours_field = row["Edit Hours"]
				activity_key = row["Activity"]
				country = row["Execution Country"]
			else:
				partNumber = row["FO_Eng"]
				hours_field = row["Final_Hrs"]
				activity_key = row["Deliverable"]
				country = row["Execution_Country"]
			if activity_key not in ('Off-Site','On-Site','Total'):
				excecutionCountry=getExecutionCountry(Quote)
				if country == excecutionCountry and hours_field not in ('',"0") and partNumber != '':
					addFinalHours(laboHours, "Local Labor", round(getFloat(hours_field)))
				elif hours_field not in ('',"0") and partNumber != '':
					addFinalHours(laboHours, "Cross Border Labor", round(getFloat(hours_field)))
	return laboHours

def getFinalHours_hci(item,container,Quote):
    laboHours = {}
    excecutionCountry=getExecutionCountry(Quote)
    if item.ProductName in ("PHD Labor","AFM Labor","Uniformance Insight Labor"):
        for prodcontainer in container:
            for row in item.SelectedAttributes.GetContainerByName(prodcontainer).Rows:
                if row["Eng"] and "GES" not in row["Eng"] and row["Execution Country"] == excecutionCountry and row["Final Hrs"] not in ('',"0.0"):
                    addFinalHours(laboHours, "Local Labor", round(getFloat(row["Final Hrs"])))
                elif row["Eng"] and "GES" not in row["Eng"] and row["Execution Country"] != excecutionCountry and row["Final Hrs"] not in ('',"0.0"):
                    addFinalHours(laboHours, "Cross Border Labor", round(getFloat(row["Final Hrs"])))
                if row["Eng"] and "GES" in row["Eng"] and row["Final Hrs"] not in ('',"0.0"):
                    addFinalHours(laboHours, "GES - Work @ GES Location", round(getFloat(row["Final Hrs"])))
    elif item.ProductName == "HCI Labor Upload":
        for prodcontainer in container:
            for row in item.SelectedAttributes.GetContainerByName(prodcontainer).Rows:
                if row["LaborResource"] and "GES" not in row["LaborResource"] and row["ExecutionCountry"] == excecutionCountry:
                    addFinalHours(laboHours, "Local Labor", round(getFloat(row["FinalHours"])))
                elif row["LaborResource"] and "GES" not in row["LaborResource"] and row["ExecutionCountry"] != excecutionCountry:
                    addFinalHours(laboHours, "Cross Border Labor", round(getFloat(row["FinalHours"])))
                if row["LaborResource"] and "GES" in row["LaborResource"]:
                    addFinalHours(laboHours, "GES - Work @ GES Location", round(getFloat(row["FinalHours"])))
    return laboHours

def getFinalHours_winest(item,contList,Quote):
    laborHours = {}
    excecutionCountry = getExecutionCountry(Quote)
    for cont in contList:
        cont = item.SelectedAttributes.GetContainerByName(cont)
        if cont:
            for row in cont.Rows:
                if row["Service Material"] and "GES" not in row["Service Material"] and row["Execution Country"] == excecutionCountry:
                    addFinalHours(laborHours, "Local Labor", round(getFloat(row["Final Hrs"])))
                elif row["Service Material"] and "GES" not in row["Service Material"] and row["Execution Country"] != excecutionCountry:
                    addFinalHours(laborHours, "Cross Border Labor", round(getFloat(row["Final Hrs"])))
                elif row["Service Material"] and "GES" in row["Service Material"] and row["Service Material"][-4] == 'B':
                    addFinalHours(laborHours, "GES - Work @ GES Location", round(getFloat(row["Final Hrs"])))
                elif row["Service Material"] and "GES" in row["Service Material"] and row["Service Material"][-4] == 'F':
                    addFinalHours(laborHours, "GES - Work @ Non GES Location", round(getFloat(row["Final Hrs"])))
    return laborHours