prod_cont_Details = {"One Wireless System":"OWS_Engineering_Labor_Container","Public Address General Alarm System":"PAGA_Labor_Container","Tank Gauging Engineering":"TGE_Engineering_Labor_Container","Fire Detection & Alarm Engineering":"FDA_Engineering_Labor_Container","Metering Skid Engineering":"MSE_Engineering_Labor_Container","PRMS Skid Engineering":"PRMS_Engineering_Labor_Container","Liquid MeterSuite Engineering - C300 Functions":"LMS_Labor_Container","Gas MeterSuite Engineering - C300 Functions":"Gas_MeterSuite_Engineering_Labor_Container","Industrial Security (Access Control)":"IS_Labor_Container","MeterSuite Engineering - MSC Functions":"MSC_Engineering_Labor_Container","MS Analyser System Engineering":"MS_ASE_Engineering_Labor_Container"}
PRJT_Containers = {"One Wireless System":"PRJT_OWS_Engineering_Labor_Container","Industrial Security (Access Control)":"PRJT_IS_Labor_Container", "Public Address General Alarm System":"PRJT_PAGA_Labor_Container","Fire Detection & Alarm Engineering":"PRJT_FDA_Engineering_Labor_Container","MeterSuite Engineering - MSC Functions":"PRJT_MSC_Engineering_Labor_Container","Liquid MeterSuite Engineering - C300 Functions":"PRJT_LMS_Labor_Container", "Gas MeterSuite Engineering - C300 Functions":"PRJT_Gas_MeterSuite_Engineering_Labor_Container","MS Analyser System Engineering":"PRJT_MS_ASE_Engineering_Labor_Container", "PRMS Skid Engineering":"PRJT_PRMS_Engineering_Labor_Container", "Metering Skid Engineering":"PRJT_MSE_Engineering_Labor_Container", "Tank Gauging Engineering":"PRJT_TGE_Engineering_Labor_Container"}
Prod_cont_Details_AL = {"One Wireless System":"OWS_Additional_Labour_Container","Public Address General Alarm System":"PAGA_Additional_Labour_Container","Tank Gauging Engineering":"TGE_Additional_Labour_Container","Fire Detection & Alarm Engineering":"FDA_Additional_Labor_Container","Metering Skid Engineering":"MSE_Additional_Labor_Container","PRMS Skid Engineering":"PRMS_Additional_Labor_Container","Liquid MeterSuite Engineering - C300 Functions":"LMS_Additional_Labor_Container","Gas MeterSuite Engineering - C300 Functions":"Gas_MeterSuite_Additional_Labor_Container","Industrial Security (Access Control)":"IS_Additional_Labor_Container","MeterSuite Engineering - MSC Functions":"MSC_Additional_Labour_Container","MS Analyser System Engineering":"MS_ASE_Additional_Labour_Container"}
PRJT_adtnl_Containers = {"One Wireless System":"PRJT_OWS_Additional_Labour_Container","Industrial Security (Access Control)":"PRJT_IS_Additional_Labor_Container", "Public Address General Alarm System":"PRJT_PAGA_Additional_Labour_Container","Fire Detection & Alarm Engineering":"PRJT_FDA_Additional_Labor_Container","MeterSuite Engineering - MSC Functions":"PRJT_MSC_Additional_Labour_Container","Liquid MeterSuite Engineering - C300 Functions":"PRJT_LMS_Additional_Labor_Container", "Gas MeterSuite Engineering - C300 Functions":"PRJT_Gas_MeterSuite_Additional_Labor_Container","MS Analyser System Engineering":"PRJT_MS_ASE_Additional_Labour_Container", "PRMS Skid Engineering":"PRJT_PRMS_Additional_Labor_Container", "Metering Skid Engineering":"PRJT_MSE_Additional_Labor_Container", "Tank Gauging Engineering":"PRJT_TGE_Additional_Labour_Container"}

def getContainer(product,Name):
    return product.GetContainerByName(Name)

def getAttrValue(product,Name):
    return product.Attr(Name).GetValue()

def getContainer1(Name):
    return Product.GetContainerByName(Name)

def addValues(totalDict , partNumber,key, value):
    partDict = totalDict.get(partNumber,dict())
    partDict[key] = getFloat(partDict.get(key , 0)) + getFloat(value)
    totalDict[partNumber] = partDict

def addFinalHours(totalDict, key, value):
    totalDict[key] = getFloat(totalDict.get(key, 0)) + getFloat(value)

def calculateSplit(totalDict, key, hours,percentage):
    totalDict[key] = getFloat(totalDict.get(key, 0)) + (getFloat(hours) * getFloat(percentage)) / 100

def getFloat(Var):
    if Var:
        return float(Var)
    return 0

def calculateproductivity(row):
    Trace.Write(getFloat(row["Calculated Hrs"]))
    Trace.Write(getFloat(row["Final Hrs"]))
    if getFloat(row["Calculated Hrs"]) != 0:
        return round(getFloat(row["Final Hrs"]) / getFloat(row["Calculated Hrs"]),2)
    else:
        return 1.00
    
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
    deliver_list = []
    for row in adtnl_deliver:
        if product == row["Product_Module"]:
            deliver_list.append(row["Deliverable_Name"])

    if queryData is not None:
        moduleDict = containerData.get(product,'')
        if moduleDict:
            for entry in deliver_list:
                deliverableDict = moduleDict.get(entry,'')
                if deliverableDict:
                    if entry in ('Total'):
                        row = container.AddNewRow(False)
                        row["Deliverable"] = entry
                        row["Calculated Hrs"] = str(round(deliverableDict['']['']['']['']['']['']["Calculated Hrs"],2))
                        row["Final Hrs"] = str(round(deliverableDict['']['']['']['']['']['']["Final Hrs"],0))
                    else:
                        for key1,value1 in deliverableDict.items():
                            for key2,value2 in value1.items():
                                for key3,value3 in value2.items():
                                    for key4,value4 in value3.items():
                                        for key5,value5 in value4.items():
                                            for key6,value6 in value5.items():
                                                row = container.AddNewRow(False)
                                                row["Deliverable"] = entry
                                                Trace.Write(entry)
                                                row["Calculated Hrs"] = str(format(value6.get("Calculated Hrs",0), ".2f"))
                                                row["Final Hrs"] = str(format(round(value6.get("Final Hrs",0),2), ".0f"))
                                                Trace.Write(product)
                                                row["FO Eng 1"] = key1
                                                row["FO Eng 2"] = key2
                                                row["FO Eng 2 % Split"] = str(format(round((getFloat(value6.get("FO Eng 2 % Split",0)) / getFloat(value6.get("Final Hrs",0)) * 100),2),".2f")) if getFloat(value6.get("Final Hrs",0)) else "0.00"
                                                row["GES Eng % Split"] = str(format(round((getFloat(value6.get("GES Eng % Split",0)) / getFloat(value6.get("Final Hrs",0)) * 100),2),".2f")) if getFloat(value6.get("Final Hrs",0)) else "0.00"
                                                row["FO Eng 1 % Split"] = str(format(round((100 - (getFloat(row["GES Eng % Split"])+getFloat(row["FO Eng 2 % Split"]))),2),".2f")) if row["Final Hrs"] not in ('0.0',"0") else "100.00"
                                                row["GES Eng"] = key3
                                                row["Execution Country"] = key4
                                                row["Execution Year"] = key6
                                                row["Comment"] = key5
    if container.Rows.Count > 0:
        CalculateHrsTotal = 0.0
        FinalHrsTotal = 0
        for row in container.Rows:
            if row["Calculated Hrs"] not in ('0.0',"0","") or row["Final Hrs"] not in ('0.0',"0","" ) :
                CalculateHrsTotal += float(row["Calculated Hrs"])
                FinalHrsTotal += int(float(row["Final Hrs"]))
            row["Productivity"] = str(format(calculateproductivity(row),".2f"))
        row = container.AddNewRow(False)
        row["Deliverable"] = "Total"
        row["Calculated Hrs"] = str(CalculateHrsTotal)
        row["Final Hrs"] = str(FinalHrsTotal)
        container.Calculate()

def populate_adtnl_CommonCon(product,container):
    deliver_list = []
    for row in adtnl_deliver_AL:
        if product == row["Product_Module"]:
            deliver_list.append(row["Deliverable_Name"])
    moduleDict_AL = containerData_AL.get(product,'')
    if moduleDict_AL:
        for entry in deliver_list:
            Std_deliverableDict = moduleDict_AL.get(entry,'')
            if Std_deliverableDict:
                if entry in ('Total'):
                    row = container.AddNewRow(False)
                    row["Standard Deliverable selection"] = entry
                    row["Final Hrs"] = str(round(Std_deliverableDict['']['']['']['']['']['']["Final Hrs"],0))
                else:
                    for key1,value1 in Std_deliverableDict.items():
                        for key2,value2 in value1.items():
                            for key3,value3 in value2.items():
                                for key4,value4 in value3.items():
                                    for key5,value5 in value4.items():
                                        for key6,value6 in value5.items():
                                            row = container.AddNewRow(False)
                                            row["Standard Deliverable selection"] = entry
                                            Trace.Write(entry)
                                            row["Final Hrs"] = str(format(round(value6.get("Final Hrs",0),2), ".0f"))
                                            Trace.Write(product)
                                            row["Deliverable Name"] = key1
                                            row["FO Eng"] = key2
                                            row["FO Eng % Split"] = str(format(round((getFloat(value6.get("FO Eng % Split",0)) / getFloat(value6.get("Final Hrs",0)) * 100),2),".2f")) if getFloat(value6.get("Final Hrs",0)) else "100.00"
                                            row["GES Eng % Split"] = str(format(round((100 - (getFloat(row["FO Eng % Split"]))),2),".2f")) if row["Final Hrs"] not in ('0.0',"0") else "0.00"
                                            row["GES Eng"] = key3
                                            row["Execution Country"] = key4
                                            row["Execution Year"] = key6
                                            row["Comment"] = key5
    if container.Rows.Count > 0:
        FinalHrsTotal = 0
        for row in container.Rows:
            if row["Final Hrs"] not in ('0.0',"0","" ) :
                FinalHrsTotal += int(float(row["Final Hrs"]))
        row = container.AddNewRow(False)
        row["Standard Deliverable selection"] = "Total"
        row["Final Hrs"] = str(FinalHrsTotal)
        row["FO Eng % Split"] = str("")
        container.Calculate()


def getcontainersData(container,product):
    moduleDict = containerData.get(product,dict())
    for row in container.Rows:
        fo1 = str(row.GetColumnByName("FO Eng 1").DisplayValue)
        fo2 = str(row.GetColumnByName("FO Eng 2").DisplayValue)
        ges1 = str(row.GetColumnByName("GES Eng").DisplayValue)
        deliverableDict = moduleDict.get(row.GetColumnByName("Deliverable").Value,dict())
        foPartNumberDict1 = deliverableDict.get(fo1,dict())
        foPartNumberDict2 = foPartNumberDict1.get(fo2,dict())
        gesPartNumberDict = foPartNumberDict2.get(ges1,dict())
        Trace.Write(product)
        exeCountryDict = gesPartNumberDict.get(row.GetColumnByName("Execution Country").Value,dict())
        commentsDict = exeCountryDict.get(row.GetColumnByName("Comment").Value,dict())
        exeYearDict = commentsDict.get(row.GetColumnByName("Execution Year").Value,dict())
        addFinalHours(exeYearDict,"Calculated Hrs",row.GetColumnByName("Calculated Hrs").Value)
        addFinalHours(exeYearDict,"Final Hrs",row.GetColumnByName("Final Hrs").Value)
        #calculateSplit(exeYearDict,"FO Eng 1 % Split",row.GetColumnByName("Final Hrs").Value,row.GetColumnByName("FO Eng 1 % Split").Value)
        calculateSplit(exeYearDict,"FO Eng 2 % Split",row.GetColumnByName("Final Hrs").Value,row.GetColumnByName("FO Eng 2 % Split").Value)
        calculateSplit(exeYearDict,"GES Eng % Split",row.GetColumnByName("Final Hrs").Value,row.GetColumnByName("GES Eng % Split").Value)
        commentsDict[row["Execution Year"]] = exeYearDict #key6
        exeCountryDict[row["Comment"]] = commentsDict #key5
        gesPartNumberDict[row["Execution Country"]] = exeCountryDict #key4
        foPartNumberDict2[ges1] = gesPartNumberDict #key3
        foPartNumberDict1[fo2] = foPartNumberDict2 #key2
        deliverableDict[fo1] = foPartNumberDict1 #key1
        moduleDict[row["Deliverable"]] = deliverableDict
        containerData[product] = moduleDict
        
        data = {}
        data["Deliverable_Name"] = row["Deliverable"]
        data["Product_Module"] = product
        valExist = False
        for addel in adtnl_deliver:
            if addel["Product_Module"] == product and addel["Deliverable_Name"] == row["Deliverable"]:
                valExist = True
        if valExist == False:
            adtnl_deliver.append(data)
def get_adtnl_containersData(container,product):
    moduleDict_AL = containerData_AL.get(product,dict())
    for row in container.Rows:
        fo = str(row.GetColumnByName("FO Eng").DisplayValue)
        ges = str(row.GetColumnByName("GES Eng").DisplayValue)
        deliverable_AL = (row.GetColumnByName("Deliverable Name").Value)
        Stddeliverable_AL = str(row.GetColumnByName("Standard Deliverable selection").DisplayValue)
        stddeliverableDict = moduleDict_AL.get(Stddeliverable_AL,dict())
        deliverableDict = stddeliverableDict.get(deliverable_AL,dict())
        foPartNumberDict = deliverableDict.get(fo,dict())
        gesPartNumberDict = foPartNumberDict.get(ges,dict())
        Trace.Write(product)
        exeCountryDict = gesPartNumberDict.get(row.GetColumnByName("Execution Country").Value,dict())
        commentsDict = exeCountryDict.get(row.GetColumnByName("Comment").Value,dict())
        exeYearDict = commentsDict.get(row.GetColumnByName("Execution Year").Value,dict())
        addFinalHours(exeYearDict,"Final Hrs",row.GetColumnByName("Final Hrs").Value)
        calculateSplit(exeYearDict,"FO Eng % Split",row.GetColumnByName("Final Hrs").Value,row.GetColumnByName("FO Eng % Split").Value)
        calculateSplit(exeYearDict,"GES Eng % Split",row.GetColumnByName("Final Hrs").Value,row.GetColumnByName("GES Eng % Split").Value)
        commentsDict[row["Execution Year"]] = exeYearDict #key6
        exeCountryDict[row["Comment"]] = commentsDict #key5
        gesPartNumberDict[row["Execution Country"]] = exeCountryDict #key4
        foPartNumberDict[ges] = gesPartNumberDict #key3
        deliverableDict[fo] = foPartNumberDict #key2
        stddeliverableDict[deliverable_AL] = deliverableDict #key1
        moduleDict_AL[row["Standard Deliverable selection"]] = stddeliverableDict
        containerData_AL[product] = moduleDict_AL

        data = {}
        data["Deliverable_Name"] = row["Standard Deliverable selection"]
        data["Product_Module"] = product
        valExist = False
        for addel in adtnl_deliver_AL:
            if addel["Product_Module"] == product and addel["Deliverable_Name"] == row["Standard Deliverable selection"]:
                valExist = True
        if valExist == False:
            adtnl_deliver_AL.append(data)
        
prjtContainer = Product.GetContainerBySystemId("CE_SystemGroup_Cont_cpq")
containerData = dict()
containerData_AL = dict()
adtnl_deliver = []
adtnl_deliver_AL = []
prod_list = []
Prod_AL_list = []
for p_name,c_name in PRJT_Containers.items():
    prjtLaborContainer = Product.GetContainerByName(c_name)
    prjtLaborContainer.Rows.Clear()

for p_name,c_name in PRJT_adtnl_Containers.items():
    prjtLaborContainer = Product.GetContainerByName(c_name)
    prjtLaborContainer.Rows.Clear()

for row1 in prjtContainer.Rows:
    sgProduct = row1.Product
    systemgroupContainer =  sgProduct.GetContainerBySystemId("CE_System_Cont_cpq")
    for row in systemgroupContainer.Rows:
        productName = row.GetColumnByName("Product Name").Value
        baseProduct = row.Product
        for prod_name,labor_cont in prod_cont_Details.items():
            if prod_name == productName:
                prodlaborContainer = baseProduct.GetContainerByName(labor_cont)
                getcontainersData(prodlaborContainer,prod_name)
                prod_list.append(productName)
        
        for prod_name,labor_cont in Prod_cont_Details_AL.items():
            if prod_name == productName:
                prodlaborContainer = baseProduct.GetContainerByName(labor_cont)
                get_adtnl_containersData(prodlaborContainer,prod_name)
                Prod_AL_list.append(productName)
        
for row1 in prjtContainer.Rows:
    productNameList = row1.GetColumnByName("Selected_Products").Value.split("<br>")
    for productName in productNameList:
        if productName in prod_list:
            prjtLaborContainer = Product.GetContainerByName(PRJT_Containers[productName])
            populateCommonCon(productName,prjtLaborContainer)
            prjtLaborContainer.Calculate()
            c = prod_list.count(productName)
            for i in range(c):
                prod_list.remove(productName)
            
            prjtLaborContainer_AL = Product.GetContainerByName(PRJT_adtnl_Containers[productName])
            populate_adtnl_CommonCon(productName,prjtLaborContainer_AL)
            prjtLaborContainer_AL.Calculate()
            c = Prod_AL_list.count(productName)
            for i in range(c):
                Prod_AL_list.remove(productName)

Product.ApplyRules()
#Quote.Save()