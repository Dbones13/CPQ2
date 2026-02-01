prod_cont_Details = {"One Wireless System":"OWS_Engineering_Labor_Container","Public Address General Alarm System":"PAGA_Labor_Container","Tank Gauging Engineering":"TGE_Engineering_Labor_Container","Fire Detection & Alarm Engineering":"FDA_Engineering_Labor_Container","Metering Skid Engineering":"MSE_Engineering_Labor_Container","PRMS Skid Engineering":"PRMS_Engineering_Labor_Container","Liquid MeterSuite Engineering - C300 Functions":"LMS_Labor_Container","Gas MeterSuite Engineering - C300 Functions":"Gas_MeterSuite_Engineering_Labor_Container","Industrial Security (Access Control)":"IS_Labor_Container","MeterSuite Engineering - MSC Functions":"MSC_Engineering_Labor_Container","MS Analyser System Engineering":"MS_ASE_Engineering_Labor_Container"}
SG_cont_Details = {"One Wireless System":"SG_OWS_Engineering_Labor_Container","Public Address General Alarm System":"SG_PAGA_Labor_Container","Tank Gauging Engineering":"SG_TGE_Engineering_Labor_Container","Fire Detection & Alarm Engineering":"SG_FDA_Engineering_Labor_Container","Metering Skid Engineering":"SG_MSE_Engineering_Labor_Container","PRMS Skid Engineering":"SG_PRMS_Engineering_Labor_Container","Liquid MeterSuite Engineering - C300 Functions":"SG_LMS_Labor_Container","Gas MeterSuite Engineering - C300 Functions":"SG_Gas_MeterSuite_Engineering_Labor_Container","Industrial Security (Access Control)":"SG_IS_Labor_Container","MeterSuite Engineering - MSC Functions":"SG_MSC_Engineering_Labor_Container","MS Analyser System Engineering":"SG_MS_ASE_Engineering_Labor_Container"}
Prod_cont_Details_AL = {"One Wireless System":"OWS_Additional_Labour_Container","Public Address General Alarm System":"PAGA_Additional_Labour_Container","Tank Gauging Engineering":"TGE_Additional_Labour_Container","Fire Detection & Alarm Engineering":"FDA_Additional_Labor_Container","Metering Skid Engineering":"MSE_Additional_Labor_Container","PRMS Skid Engineering":"PRMS_Additional_Labor_Container","Liquid MeterSuite Engineering - C300 Functions":"LMS_Additional_Labor_Container","Gas MeterSuite Engineering - C300 Functions":"Gas_MeterSuite_Additional_Labor_Container","Industrial Security (Access Control)":"IS_Additional_Labor_Container","MeterSuite Engineering - MSC Functions":"MSC_Additional_Labour_Container","MS Analyser System Engineering":"MS_ASE_Additional_Labour_Container"}
SG_cont_Details_AL = {"One Wireless System":"SG_OWS_Additional_Labour_Container","Public Address General Alarm System":"SG_PAGA_Additional_Labour_Container","Tank Gauging Engineering":"SG_TGE_Additional_Labour_Container","Fire Detection & Alarm Engineering":"SG_FDA_Additional_Labor_Container","Metering Skid Engineering":"SG_MSE_Additional_Labor_Container","PRMS Skid Engineering":"SG_PRMS_Additional_Labor_Container","Liquid MeterSuite Engineering - C300 Functions":"SG_LMS_Additional_Labor_Container","Gas MeterSuite Engineering - C300 Functions":"SG_Gas_MeterSuite_Additional_Labor_Container","Industrial Security (Access Control)":"SG_IS_Additional_Labor_Container","MeterSuite Engineering - MSC Functions":"SG_MSC_Additional_Labour_Container","MS Analyser System Engineering":"SG_MS_ASE_Additional_Labour_Container"}


def getFloat(Var):
    if Var:
        return float(Var)
    return 0

def populateProjectManagment(sgProduct,laborContainer):
	
	adtnl_deliver = []
	#sgProduct = row.Product
	getcontainersData(laborContainer,"System Group")
	sgcontainer = sgProduct.GetContainerByName("SG_Labor_Container")
	sgcontainer.Rows.Clear()
	populateCommonCon("System Group",sgcontainer)
	sgcontainer.Calculate()
	sgProduct.ApplyRules()

def appendStringValues(totalDict,key,value):
    totalDict[key] = value


def appendNumaricValues(totalDict,key,value):
    totalDict[key] = getFloat(value)
    

def populateAdditionalCommonCon(product,container):
    if product == "One Wireless System":
        query = queryData = SqlHelper.GetList("select * from ONE_WIRELESS_SYSTEM_LABOR_CUSTOM_TABLE")
    elif product== "Industrial Security (Access Control)":
        query = queryData = SqlHelper.GetList("select * from INDUSTRIAL_SECURITY_LABOR_CUSTOM_TABLE")
    elif product== "Public Address General Alarm System":
        query = queryData = SqlHelper.GetList("select * from PAGA_Labor_Custom_Table")
    elif product== "Fire Detection & Alarm Engineering":
        query = queryData = SqlHelper.GetList("select * from FIRE_DETECTION_AND_ALARM_ENGINEERING_LABOR_CUSTOM_TABLE")
    elif product== "MeterSuite Engineering - MSC Functions":
        query = queryData = SqlHelper.GetList("select * from MSC_Labor_Custom_Table")
    elif product== "Liquid MeterSuite Engineering - C300 Functions":
        query = queryData = SqlHelper.GetList("select * from LIQUID_METERINGSUITE_ENGINEERING_LABOR_CUSTOM_TABLE")
    elif product== "MS Analyser System Engineering":
        query = queryData = SqlHelper.GetList("select * from MS_Analyser_System_Engineering_Labor_Custom_Table")
    elif product== "PRMS Skid Engineering":
        query = queryData = SqlHelper.GetList("select * from PRMS_Skid_Engineering_Labor_Custom_Table")
    elif product== "Metering Skid Engineering":
        query = queryData = SqlHelper.GetList("select * from MSE_Labor_Custom_Table")
    elif product== "Tank Gauging Engineering":
        query = queryData = SqlHelper.GetList("select * from Tank_Gauging_Engineering_LABOR_CUSTOM_TABLE")
    else:
        query = queryData = SqlHelper.GetList("select * from Gas_MeterSuite_ENGINEERING_LABOR_CUSTOM_TABLE")
    if queryData is not None:
        moduleDict = containerLaborData.get(product,'')
        if moduleDict:
            for key1 in adtnl_Labor_deliver:
                value1 = moduleDict[key1]
                if key1 == "Total":
                    row = container.AddNewRow(False)
                    row["Standard Deliverable selection"] = key1
                    row["Final Hrs"] = str(format(round(value1.get("Final Hrs",0),2),".0f"))
                    row["FO Eng % Split"] = str("")
    container.Calculate()

def getAdditionalcontainersData(container,sg_container,product):
    moduleDict = containerLaborData.get(product,dict())
    totalFinalHours = 0
    for row in container.Rows:
        selectedDeliverable = row.GetColumnByName("Standard Deliverable selection").DisplayValue
        deliverableDict = moduleDict.get(selectedDeliverable,dict())
        totalFinalHours = totalFinalHours+getFloat(row.GetColumnByName("Final Hrs").Value)
        Trace.Write("module dice"+str(moduleDict))
        Trace.Write("selectedDeliverable"+str(selectedDeliverable))
        #value1 = moduleDict[selectedDeliverable]
        sgrow = sg_container.AddNewRow(False)
        sgrow["Standard Deliverable selection"] = selectedDeliverable
        sgrow["Deliverable Name"] = str(row.GetColumnByName("Deliverable Name").Value)
        if row["Final Hrs"] != "":
            sgrow["Final Hrs"] = row["Final Hrs"]
        else:
            sgrow["Final Hrs"] = "0"
        sgrow["GES Eng"] =  row.GetColumnByName("GES Eng").DisplayValue
        sgrow["GES Eng % Split"] = str(format(round(getFloat(row["GES Eng % Split"]),2),".2f"))
        sgrow["FO Eng"] = row.GetColumnByName("FO Eng").DisplayValue
        sgrow["FO Eng % Split"] = str(format(round(getFloat(row["FO Eng % Split"]),2),".2f"))
        sgrow["Execution Country"] = row.GetColumnByName("Execution Country").Value
        sgrow["Execution Year"] = row.GetColumnByName("Execution Year").Value
        sgrow["Comment"] = row.GetColumnByName("Comment").Value
        moduleDict[selectedDeliverable] = deliverableDict
        containerLaborData[product] = moduleDict
        adtnl_Labor_deliver.append(selectedDeliverable)
    deliverableDict = moduleDict.get("Total",dict())
    appendNumaricValues(deliverableDict,"Final Hrs",totalFinalHours)
    moduleDict["Total"] = deliverableDict
    adtnl_Labor_deliver.append("Total")
    

def populateCommonCon(product,container):
    if product == "One Wireless System":
        query = queryData = SqlHelper.GetList("select * from ONE_WIRELESS_SYSTEM_LABOR_CUSTOM_TABLE")
    elif product== "Industrial Security (Access Control)":
        query = queryData = SqlHelper.GetList("select * from INDUSTRIAL_SECURITY_LABOR_CUSTOM_TABLE")
    elif product== "Public Address General Alarm System":
        query = queryData = SqlHelper.GetList("select * from PAGA_Labor_Custom_Table")
    elif product== "Fire Detection & Alarm Engineering":
        query = queryData = SqlHelper.GetList("select * from FIRE_DETECTION_AND_ALARM_ENGINEERING_LABOR_CUSTOM_TABLE")
    elif product== "MeterSuite Engineering - MSC Functions":
        query = queryData = SqlHelper.GetList("select * from MSC_Labor_Custom_Table")
    elif product== "Liquid MeterSuite Engineering - C300 Functions":
        query = queryData = SqlHelper.GetList("select * from LIQUID_METERINGSUITE_ENGINEERING_LABOR_CUSTOM_TABLE")
    elif product== "MS Analyser System Engineering":
        query = queryData = SqlHelper.GetList("select * from MS_Analyser_System_Engineering_Labor_Custom_Table")
    elif product== "PRMS Skid Engineering":
        query = queryData = SqlHelper.GetList("select * from PRMS_Skid_Engineering_Labor_Custom_Table")
    elif product== "Metering Skid Engineering":
        query = queryData = SqlHelper.GetList("select * from MSE_Labor_Custom_Table")
    elif product== "Tank Gauging Engineering":
        query = queryData = SqlHelper.GetList("select * from Tank_Gauging_Engineering_LABOR_CUSTOM_TABLE")
    else:
        query = queryData = SqlHelper.GetList("select * from Gas_MeterSuite_ENGINEERING_LABOR_CUSTOM_TABLE")
    if queryData is not None:
        moduleDict = containerData.get(product,'')
        if moduleDict:
            for key1 in adtnl_deliver:
                value1 = moduleDict[key1]
                if key1 == "Total":
                    row = container.AddNewRow(False)
                    row["Deliverable"] = key1
                    #row["Calculated Hrs"] = str(value1.get("Calculated Hrs"))
                    row["Calculated Hrs"] = str(format(round(value1.get("Calculated Hrs"),2), ".2f"))
                    row["Final Hrs"] = str(format(round(value1.get("Final Hrs",0),2),".0f"))
                else:
                    row = container.AddNewRow(False)
                    row["Deliverable"] = key1
                    #row["Calculated Hrs"] = str(value1.get("Calculated Hrs"))
                    row["Calculated Hrs"] = str(format(round(value1.get("Calculated Hrs"),2), ".2f"))
                    row["Productivity"] = str(format(round(value1.get("Productivity"),2), ".2f"))
                    row["Final Hrs"] = str(format(round(value1.get("Final Hrs",0),2),".0f"))
                    row["GES Eng"] =  value1.get("GES Eng")
                    row["GES Eng % Split"] = str(format(value1.get("GES Eng % Split"),".2f"))
                    row["FO Eng 1"] = value1.get("FO Eng 1")
                    row["FO Eng 1 % Split"] = str(format(value1.get("FO Eng 1 % Split"),".2f"))
                    row["FO Eng 2"] = value1.get("FO Eng 2")
                    row["FO Eng 2 % Split"] = str(format(value1.get("FO Eng 2 % Split"),".2f"))
                    row["Execution Country"] = value1.get("Execution Country")
                    row["Execution Year"] = value1.get("Execution Year")
                    row["Comment"] = value1.get("Comment"," ")
    container.Calculate()

def getcontainersData(container,product):
    moduleDict = containerData.get(product,dict())
    totalCalculatedHours = 0
    totalFinalHours = 0
    for row in container.Rows:
        deliverableDict = moduleDict.get(row.GetColumnByName("Deliverable").Value,dict())
        appendNumaricValues(deliverableDict,"Calculated Hrs",row.GetColumnByName("Calculated Hrs").Value)
        appendNumaricValues(deliverableDict,"Productivity",row.GetColumnByName("Productivity").Value)
        appendNumaricValues(deliverableDict,"Final Hrs",row.GetColumnByName("Final Hrs").Value)
        appendStringValues(deliverableDict,"GES Eng",row.GetColumnByName("GES Eng").DisplayValue)
        appendNumaricValues(deliverableDict,"GES Eng % Split",row.GetColumnByName("GES Eng % Split").Value)
        appendStringValues(deliverableDict,"FO Eng 1",row.GetColumnByName("FO Eng 1").DisplayValue)
        appendNumaricValues(deliverableDict,"FO Eng 1 % Split",row.GetColumnByName("FO Eng 1 % Split").Value)
        appendStringValues(deliverableDict,"FO Eng 2",row.GetColumnByName("FO Eng 2").DisplayValue)
        appendNumaricValues(deliverableDict,"FO Eng 2 % Split",row.GetColumnByName("FO Eng 2 % Split").Value)
        appendStringValues(deliverableDict,"Execution Country",row.GetColumnByName("Execution Country").Value)
        appendStringValues(deliverableDict,"Execution Year",row.GetColumnByName("Execution Year").Value)
        appendStringValues(deliverableDict,"Comment",row.GetColumnByName("Comment").Value)
        totalCalculatedHours = totalCalculatedHours+getFloat(row.GetColumnByName("Calculated Hrs").Value)
        totalFinalHours = totalFinalHours+getFloat(row.GetColumnByName("Final Hrs").Value)
        moduleDict[row["Deliverable"]] = deliverableDict
        containerData[product] = moduleDict
        adtnl_deliver.append(row.GetColumnByName("Deliverable").Value)
    deliverableDict = moduleDict.get("Total",dict())
    appendNumaricValues(deliverableDict,"Calculated Hrs",totalCalculatedHours)
    appendNumaricValues(deliverableDict,"Final Hrs",totalFinalHours)
    moduleDict["Total"] = deliverableDict
    adtnl_deliver.append("Total")


prjtContainer = Product.GetContainerBySystemId("CE_SystemGroup_Cont_cpq")
Log.Write("Script Strated SG")
laborContainer =  Product.GetContainerBySystemId("Project_management_Labor_Container_cpq")

for p_name,c_name in SG_cont_Details.items():
    sgLaborContainer = Product.GetContainerByName(c_name)
    sgLaborContainer.Rows.Clear()

for p_name,c_name in SG_cont_Details_AL.items():
    sgLaborContainer = Product.GetContainerByName(c_name)
    sgLaborContainer.Rows.Clear()

systemgroupContainer =  Product.GetContainerBySystemId("CE_System_Cont_cpq")
for row in systemgroupContainer.Rows:
    containerData = dict()
    adtnl_deliver = []
    containerLaborData = dict()
    adtnl_Labor_deliver = []
    productName = row.GetColumnByName("Product Name").Value
    baseProduct = row.Product
    for prod_name,labor_cont in prod_cont_Details.items():
        if prod_name == productName:
            prodlaborContainer = baseProduct.GetContainerByName(labor_cont)
            prodadditionallaborContainer = baseProduct.GetContainerByName(Prod_cont_Details_AL[productName])
            getcontainersData(prodlaborContainer,prod_name)
            productName = row.GetColumnByName("Product Name").Value
            sgcontainername = SG_cont_Details[productName]
            sglaborcontainername = SG_cont_Details_AL[productName]
            sgcontainer = Product.GetContainerByName(sgcontainername)
            sglaborcontainer = Product.GetContainerByName(sglaborcontainername)
            getAdditionalcontainersData(prodadditionallaborContainer,sglaborcontainer,prod_name)
            populateCommonCon(productName,sgcontainer)
            populateAdditionalCommonCon(productName,sglaborcontainer)
            sgcontainer.Calculate()
            sglaborcontainer.Calculate()