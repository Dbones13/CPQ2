#populate common container

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

def calculateFoSplit(totalDict, key, hours,percentage):
    totalDict[key] = getFloat(totalDict.get(key, 0)) + (getFloat(hours) * getFloat(percentage)) / 100

def getFloat(Var):
    if Var:
        return float(Var)
    return 0

def calculateproductivity(row):

    if (round(getFloat(row["Calculated_Hrs"])) == round(getFloat(row["Final_Hrs"]))) or (getFloat(row["Calculated_Hrs"]) == 0.00):
        return "1"
    else:
        prod = round(getFloat(row["Final_Hrs"]) / getFloat(row["Calculated_Hrs"]),2)
        return str(int(prod)) if (prod.is_integer() == True) else str(prod)

def getcontainersData(container,product):
    moduleDict = containerData.get(product,dict())
    for row in container.Rows:
        deliverableDict = moduleDict.get(row["Deliverable"],dict())
        foPartNumberDict = deliverableDict.get(row["FO_Eng"],dict())
        gesPartNumberDict = foPartNumberDict.get(row["GES_Eng"],dict())
        exeCountryDict = gesPartNumberDict.get(row["Execution_Country"],dict())
        #exeYearDict = exeCountryDict.get(row["Execution_Year"],dict())
        commentsDict = exeCountryDict.get(row["Comments"],dict())
        exeYearDict = commentsDict.get(row["Execution_Year"],dict())
        #commentsDict = exeYearDict.get(row["Comments"],dict())
        addFinalHours(exeYearDict,"Calculated_Hrs",row["Calculated_Hrs"])
        addFinalHours(exeYearDict,"Final_Hrs",row["Final_Hrs"])
        calculateFoSplit(exeYearDict,"FoSplit",row["Final_Hrs"],row["FO_Eng_Percentage_Split"])
        #commentsDict = deliverableDict.get(row['Comments'],dict())
        commentsDict[row["Execution_Year"]] = exeYearDict #key5
        #exeYearDict[row["Comments"]] = commentsDict
        exeCountryDict[row["Comments"]] = commentsDict #key4
        gesPartNumberDict[row["Execution_Country"]] = exeCountryDict #key3
        foPartNumberDict[row["GES_Eng"]] = gesPartNumberDict #key4
        deliverableDict[row["FO_Eng"]] = foPartNumberDict #key5
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
    Trace.Write(str(adtnl_deliver))
    Trace.Write(str(containerData))

def populateCommonCon(product,container):
    #query = queryData = SqlHelper.GetList("select * from LABOR_DELIVERABLES where Product_Module = '{}' and IsDocument = 'Yes'".format(product))
    if product == "3rd Party PLC to ControlEdge PLC/UOC":
        query = queryData = SqlHelper.GetList("select * from TABLE_3RD_PARTY_PLC_UOC_LABOR_DELIVERABLES where IsDocument = 'Yes'")
    elif product == "Virtualization System":
        query = queryData = SqlHelper.GetList("select * from VIRTUALIZATION_LABOR_DELIVERABLES where IsDocument = 'Yes'")
    elif "Generic System" in product:
        query = queryData = SqlHelper.GetList("select * from GENERIC_LABOR_DELIVERABLES where IsDocument = 'Yes'")
    elif product == "QCS RAE Upgrade":
        query = queryData = SqlHelper.GetList("select * from QCS_RAE_UPGRADE_LABOR_DELIVERABLES_MSID where IsDocument = 'Yes'")
    elif product == "C200 Migration":
        query = queryData = SqlHelper.GetList("select * from Labor_Deliverable_Excel_Pull_C200 where Product_Module = '{}' and IsDocument = 'Yes'".format(product))
    elif product == "TPA/PMD Migration":
        query = queryData = SqlHelper.GetList("select * from TPAPMD_MIGRATION_LABOR_DELIVERABLES where IsDocument = 'Yes'")
    # for Extending Logic to generate Migration Project - Excel Pull for Labor Document -- Boya YashwanthKumar : CXCPQ-60198 :start
    elif product == "ELEPIU ControlEdge RTU Migration Engineering":
        query = queryData = SqlHelper.GetList("select * from ELEPIU_MIGRATION_LABOR_DELIVERABLES where IsDocument = 'Yes'")
    # for Extending Logic to generate Migration Project - Excel Pull for Labor Document -- Boya YashwanthKumar : CXCPQ-60198 :end
    else:
        query = queryData = SqlHelper.GetList("select * from LABOR_DELIVERABLES where Product_Module = '{}' and IsDocument = 'Yes'".format(product))
    deliver_list = []
    for row in adtnl_deliver:
        if product == row["Product_Module"]:
            deliver_list.append(row["Deliverable_Name"])

    if queryData is not None:
        moduleDict = containerData.get(product,'')
        if moduleDict:
            Trace.Write("product = " + str(product))
            for entry in deliver_list:
                deliverableDict = moduleDict.get(entry,'')
                Trace.Write(str(entry)+'----'+str(deliverableDict))
                if deliverableDict:
                    if entry in ('Total','Off-Site','On-Site'):
                        row = container.AddNewRow(False)
                        row["Deliverable"] = entry
                        row["Calculated_Hrs"] = str(round(deliverableDict['']['']['']['']['']["Calculated_Hrs"],2))
                        row["Final_Hrs"] = str(round(deliverableDict['']['']['']['']['']["Final_Hrs"],0))
                        #row["Comments"] = str(deliverableDict['']['']['']['']["Comments"])
                    else:
                        for key1,value1 in deliverableDict.items():
                            Trace.Write("Key1:"+str(key1) +"Value = "+ str(value1))
                            for key2,value2 in value1.items():
                                Trace.Write("Key2:"+str(key2) +"Value = "+ str(value2))
                                for key3,value3 in value2.items():
                                    for key4,value4 in value3.items():
                                        for key5,value5 in value4.items():
                                            Trace.Write("Key3:"+str(key3) +"Value = "+ str(value3))
                                            Trace.Write("Key 4:"+str(key4) + "Value ="+str(value4))
                                            Trace.Write("Key 5:"+str(key5) + "Value ="+str(value5))
                                            row = container.AddNewRow(False)
                                            row["Deliverable"] = entry
                                            row["Calculated_Hrs"] = str(format(round(value5.get("Calculated_Hrs",0),2), ".2f"))
                                            row["Final_Hrs"] = str(round(value5.get("Final_Hrs",0),2))
                                            row["FO_Eng"] = key1
                                            row["FO_Eng_Percentage_Split"] = str(getFloat(value5.get("FoSplit",0)) / getFloat(value5.get("Final_Hrs",0)) * 100) if getFloat(value5.get("Final_Hrs",0)) else "100.0"
                                            row["GES_Eng"] = key2
                                            row["GES_Eng_Percentage_Split"] = str(100 - getFloat(row["FO_Eng_Percentage_Split"])) if row["Final_Hrs"] not in ('0.0',"0") else "0.0"
                                            row["Execution_Country"] = key3
                                            row["Execution_Year"] = key5
                                            row["Comments"] = key4
    if container.Rows.Count > 0:
        for row in container.Rows:
            Trace.Write("checking = " + str(row["Calculated_Hrs"]))
            if row["Deliverable"] not in ('Total','Off-Site','On-Site') and row["Calculated_Hrs"] not in ('0.0',"0"):
                row["Adjustment_Productivity"] = calculateproductivity(row)
                
def poppulateAMTCont(product):
    con1 = getContainer(product,'OPM_LaborAMT_Details')
    if con1.Rows.Count > 0:
        for row in con1.Rows:
            var1 = row['Description']
            var2 = row['Actual MCOE hour charge for AMT (Hr)']
            var3 = row['Deployment L2 - AMT (Hr)']
            var4 = row['Migration_L2_Non-AMT_Hr']
            var5 = row['L2 AMT Migration Hour saved (Hr)']
            var6 = row['Productivity EAC in %']
            var7 = row['Execution Country']
            var8 = row['Execution Year']
            var9 = row['FO Engineer']
            var10 = row['Cost Saving with AMT']
        con2 = Product.GetContainerByName('Migration_OPM_LaborAMT_Details')
        con2.Rows.Clear()
        row = con2.AddNewRow(False)
        row['Description'] = var1
        row['Actual MCOE hour charge for AMT (Hr)'] = var2
        row['Deployment L2 - AMT (Hr)'] = var3
        row['Migration_L2_Non-AMT_Hr'] = var4
        row['L2 AMT Migration Hour saved (Hr)'] = var5
        row['Productivity EAC in %'] = var6
        row['Execution Country'] = var7
        row['Execution Year'] = var8
        row['FO Engineer'] = var9
        row['Cost Saving with AMT'] = var10
    else:
        con2 = Product.GetContainerByName('Migration_OPM_LaborAMT_Details')
        con2.Rows.Clear()

msidContainer = Product.GetContainerByName("Migration_MSID_Selection_Container")
containerData = dict()
adtnl_deliver = []
for row in msidContainer.Rows:
    msidProduct = row.Product
    msidproductCon = msidProduct.GetContainerByName("MSID_Product_Container")
    msidNumber = msidProduct.Attr('Migration_MSID_Choices').GetValue()
    productCon = dict()
    msidproductVirtCon = msidProduct.GetContainerByName("MSID_Product_Container_Virtualization_hidden")
    msidproductGenCon = msidProduct.GetContainerByName("MSID_Product_Container_Generic_hidden")

    for row in msidproductCon.Rows:
        productCon[row["Product Name"]] = row.UniqueIdentifier
        if row["Product Name"] == "FSC to SM":
            msidfscCon = msidProduct.GetContainerByName("MSID_Product_Container_FSC_hidden")
            rowfsc = msidfscCon.Rows[0]
            productCon[rowfsc["Product Name"]] = rowfsc.UniqueIdentifier
        if row["Product Name"] == "FSC to SM IO Migration":
            msidfscioCon = msidProduct.GetContainerByName("MSID_Product_Container_FSC_IO_hidden")
            rowfscio = msidfscioCon.Rows[0]
            productCon[rowfscio["Product Name"]] = rowfscio.UniqueIdentifier
    for row in msidproductVirtCon.Rows:
        productCon[row["Product Name"]] = row.UniqueIdentifier
    for row in msidproductGenCon.Rows:
        productCon[row["Product Name"]] = row.UniqueIdentifier
    opmEngineeringCon = getContainer(msidProduct,"MSID_Labor_OPM_Engineering")
    lcnOneTimeUpgradeCon = getContainer(msidProduct,"MSID_Labor_LCN_One_Time_Upgrade_Engineering")
    ebrCon = getContainer(msidProduct,"MSID_Labor_EBR_Con")
    elcnCon = getContainer(msidProduct,"MSID_Labor_ELCN_Con")
    orionConsoleCon = getContainer(msidProduct,"MSID_Labor_Orion_Console_Con")
    ehpmCon = getContainer(msidProduct,"MSID_Labor_EHPM_C300PM_Con")
    tpsCon = getContainer(msidProduct,"MSID_Labor_TPS_TO_EXPERION_Con")
    tcmiCon = getContainer(msidProduct,"MSID_Labor_TCMI_Con")
    c200Con = getContainer(msidProduct,"MSID_Labor_C200_Migration_Con")
    ehpmhartCon = getContainer(msidProduct,"MSID_Labor_EHPM_HART_IO_Con")
    cbecCon = getContainer(msidProduct,"MSID_Labor_CB-EC_Upgrade_to_C300-UHIO_con")
    xpmCon = getContainer(msidProduct,"MSID_Labor_xPM_to_C300_Migration_Con")
    fdmCon = getContainer(msidProduct,"MSID_Labor_FDM_Upgrade_Con")
    fscCon = getContainer(msidProduct,"MSID_Labor_FSC_to_SM_con")
    fscauditCon = getContainer(msidProduct,"MSID_Labor_FSC_to_SM_audit_Con")
    lmCon = getContainer(msidProduct,"MSID_Labor_LM_to_ELMM_Con")
    XP10Con = getContainer(msidProduct,"MSID_Labor_XP10_Actuator_Upgrade_con")
    GraphicsCon = getContainer(msidProduct,"MSID_Labor_Graphics_Migration_con")
    CWSRAECon = getContainer(msidProduct,"MSID_Labor_CWS_RAE_Upgrade_con")
    CDActuatorCon = getContainer(msidProduct,"MSID_Labor_CD_Actuator_con")
    fscsmioCon = getContainer(msidProduct,"MSID_Labor_FSCtoSM_IO_con")
    fscsmioauditCon = getContainer(msidProduct,"MSID_Labor_FSC_to_SM_IO_Audit_Con")
    plcuocCon = getContainer(msidProduct,"3rd_Party_PLC_UOC_Labor")
    virtualizationCon = getContainer(msidProduct,"MSID_Labor_Virtualization_con")
    generic1_con= getContainer(msidProduct,"MSID_Labor_Generic_System1_Cont")
    generic2_con= getContainer(msidProduct,"MSID_Labor_Generic_System2_Cont")
    generic3_con= getContainer(msidProduct,"MSID_Labor_Generic_System3_Cont")
    generic4_con= getContainer(msidProduct,"MSID_Labor_Generic_System4_Cont")
    generic5_con= getContainer(msidProduct,"MSID_Labor_Generic_System5_Cont")
    QCSCon = getContainer(msidProduct,"MSID_Labor_QCS_RAE_Upgrade_con")
    TPACon = getContainer(msidProduct,"MSID_Labor_TPA_con")
    # for Extending Logic to generate Migration Project - Excel Pull for Labor Document -- Boya YashwanthKumar : CXCPQ-60198 :start
    ELEPIUCon = getContainer(msidProduct,"MSID_Labor_ELEPIU_con")
    # for Extending Logic to generate Migration Project - Excel Pull for Labor Document -- Boya YashwanthKumar : CXCPQ-60198 :end
    projectManagementCon = getContainer(msidProduct,"MSID_Labor_Project_Management")

    if productCon.get("OPM"):
        getcontainersData(opmEngineeringCon,"OPM")
        poppulateAMTCont(msidProduct)
    if productCon.get("LCN One Time Upgrade"):
        getcontainersData(lcnOneTimeUpgradeCon,"LCN")
    if productCon.get("EBR"):
        getcontainersData(ebrCon,"EBR")
    if productCon.get("ELCN"):
        getcontainersData(elcnCon,"ELCN")
    if productCon.get("Orion Console"):
        getcontainersData(orionConsoleCon,"Orion Console")
    if productCon.get("EHPM/EHPMX/ C300PM"):
        getcontainersData(ehpmCon,"EHPM/EHPMX/ C300PM")
    if productCon.get("TPS to Experion"):
        getcontainersData(tpsCon,"TPS to Experion")
    if productCon.get("TCMI"):
        getcontainersData(tcmiCon,"TCMI")
    if productCon.get("C200 Migration"):
        getcontainersData(c200Con,"C200 Migration")
    if productCon.get("EHPM HART IO"):
        getcontainersData(ehpmhartCon,"EHPM HART IO")
    if productCon.get("CB-EC Upgrade to C300-UHIO"):
        getcontainersData(cbecCon,"CB-EC Upgrade to C300-UHIO")
    if productCon.get("xPM to C300 Migration"):
        getcontainersData(xpmCon,"xPM to C300 Migration")
    if productCon.get("FSC to SM"):
        getcontainersData(fscCon,"FSC to SM")
    if productCon.get("FSC to SM Audit"):
        getcontainersData(fscauditCon,"FSC to SM Audit")
    if productCon.get("FDM Upgrade"):
        getcontainersData(fdmCon,"FDM Upgrade")
    if productCon.get("LM to ELMM ControlEdge PLC"):
        getcontainersData(lmCon,"LM to ELMM ControlEdge PLC")
    if productCon.get("XP10 Actuator Upgrade"):
        getcontainersData(XP10Con,"XP10 Actuator Upgrade")
    if productCon.get("Graphics Migration"):
        getcontainersData(GraphicsCon,"Graphics Migration")
    if productCon.get("CWS RAE Upgrade"):
        getcontainersData(CWSRAECon,"CWS RAE Upgrade")
    if productCon.get("CD Actuator I-F Upgrade"):
        getcontainersData(CDActuatorCon,"CD Actuator I-F Upgrade")
    if productCon.get("FSC to SM IO Migration"):
        getcontainersData(fscsmioCon,"FSC to SM IO Migration")
    if productCon.get("FSC to SM IO Audit"):
        getcontainersData(fscsmioauditCon,"FSC to SM IO Audit")
    if productCon.get("3rd Party PLC to ControlEdge PLC/UOC"):
        getcontainersData(plcuocCon,"3rd Party PLC to ControlEdge PLC/UOC")
    if productCon.get("Virtualization System"):
        getcontainersData(virtualizationCon,"Virtualization System")
    if productCon.get("Generic System 1"):
        getcontainersData(generic1_con,"Generic System 1")
    if productCon.get("Generic System 2"):
        getcontainersData(generic2_con,"Generic System 2")
    if productCon.get("Generic System 3"):
        getcontainersData(generic3_con,"Generic System 3")
    if productCon.get("Generic System 4"):
        getcontainersData(generic4_con,"Generic System 4")
    if productCon.get("Generic System 5"):
        getcontainersData(generic5_con,"Generic System 5")
    if productCon.get("QCS RAE Upgrade"):
        getcontainersData(QCSCon,"QCS RAE Upgrade")
    if productCon.get("TPA/PMD Migration"):
        getcontainersData(TPACon,"TPA/PMD Migration")
    # for Extending Logic to generate Migration Project - Excel Pull for Labor Document -- Boya YashwanthKumar : CXCPQ-60198 :start
    if productCon.get("ELEPIU ControlEdge RTU Migration Engineering"):
        getcontainersData(ELEPIUCon,"ELEPIU ControlEdge RTU Migration Engineering")
    # for Extending Logic to generate Migration Project - Excel Pull for Labor Document -- Boya YashwanthKumar : CXCPQ-60198 :end
    if productCon.get("Project Management"):
        getcontainersData(projectManagementCon,"PM")
# for Extending Logic to generate Migration Project - Excel Pull for Labor Document -- Boya YashwanthKumar : CXCPQ-60198 :start
containers = ['Migration_Labor_OPM_Common','Migration_Labor_LCN_Common','Migration_Labor_EBR_Common','Migration_Labor_ELCN_Common','Migration_Labor_OrionConsole_Common','Migration_Labor_EHPM_Common','Migration_Labor_TPS_Common','Migration_Labor_TCMI_Common','Migration_Labor_C200_Common','Migration_Labor_EHPMHART_Common','Migration_Labor_CB-EC_Upgrade_to_C300-UHIO_Common','Migration_Labor_LM_to_ELMM_Common','Migration_Labor_FSC_to_SM_Common','Migration_Labor_FSC_to_SM_Audit_Common','Migration_Labor_FDM_Upgrade_Common','Migration_Labor_xPM_to_C300_Migration_Common','Migration_Labor_XP10_Actuator_Upgrade_Common','Migration_Labor_PM_Common','Migration_Labor_Graphics_Migration_Common','Migration_Labor_CD_Actuator_Common','Migration_Labor_FSCtoSM_IO_Common','Migration_Labor_CWS_RAE_Upgrade_Common','Migration_Labor_3rd_Party_PLC_UOC_Common','Migration_Labor_Virtualization_System_Common','Migration_Labor_QCS_RAE_Upgrade_Common','Migration_Labor_Generic_System1_Common','Migration_Labor_Generic_System2_Common','Migration_Labor_Generic_System3_Common','Migration_Labor_Generic_System4_Common','Migration_Labor_Generic_System5_Common','Migration_Labor_TPA_Common','Migration_Labor_FSC_to_SM_IO_Audit_Common','Migration_Labor_ELEPIU_Common']
# for Extending Logic to generate Migration Project - Excel Pull for Labor Document -- Boya YashwanthKumar : CXCPQ-60198 :end
for container in containers:
    getContainer1(container).Rows.Clear()

populateCommonCon("OPM",getContainer1("Migration_Labor_OPM_Common"))
populateCommonCon("LCN",getContainer1("Migration_Labor_LCN_Common"))
populateCommonCon("EBR",getContainer1("Migration_Labor_EBR_Common"))
populateCommonCon("ELCN",getContainer1("Migration_Labor_ELCN_Common"))
populateCommonCon("Orion Console",getContainer1("Migration_Labor_OrionConsole_Common"))
populateCommonCon("EHPM/ C300PM",getContainer1("Migration_Labor_EHPM_Common"))
populateCommonCon("TPS to Experion",getContainer1("Migration_Labor_TPS_Common"))
populateCommonCon("TCMI",getContainer1("Migration_Labor_TCMI_Common"))
populateCommonCon("C200 Migration",getContainer1("Migration_Labor_C200_Common"))
populateCommonCon("EHPM HART IO",getContainer1("Migration_Labor_EHPMHART_Common"))
populateCommonCon("CB-EC Upgrade to C300-UHIO",getContainer1("Migration_Labor_CB-EC_Upgrade_to_C300-UHIO_Common"))
populateCommonCon("xPM to C300 Migration",getContainer1("Migration_Labor_xPM_to_C300_Migration_Common"))
populateCommonCon("LM to ELMM ControlEdge PLC",getContainer1("Migration_Labor_LM_to_ELMM_Common"))
populateCommonCon("FSC to SM",getContainer1("Migration_Labor_FSC_to_SM_Common"))
populateCommonCon("FSC to SM Audit",getContainer1("Migration_Labor_FSC_to_SM_Audit_Common"))
populateCommonCon("FDM Upgrade",getContainer1("Migration_Labor_FDM_Upgrade_Common"))
populateCommonCon("XP10 Actuator Upgrade",getContainer1("Migration_Labor_XP10_Actuator_Upgrade_Common"))
populateCommonCon("Graphics Migration",getContainer1("Migration_Labor_Graphics_Migration_Common"))
populateCommonCon("CD Actuator I-F Upgrade",getContainer1("Migration_Labor_CD_Actuator_Common"))
populateCommonCon("CWS RAE Upgrade",getContainer1("Migration_Labor_CWS_RAE_Upgrade_Common"))
populateCommonCon("FSC to SM IO Migration",getContainer1("Migration_Labor_FSCtoSM_IO_Common"))
populateCommonCon("FSC to SM IO Audit",getContainer1("Migration_Labor_FSC_to_SM_IO_Audit_Common"))
populateCommonCon("3rd Party PLC to ControlEdge PLC/UOC",getContainer1("Migration_Labor_3rd_Party_PLC_UOC_Common"))
populateCommonCon("Virtualization System",getContainer1("Migration_Labor_Virtualization_System_Common"))
populateCommonCon("Generic System 1",getContainer1("Migration_Labor_Generic_System1_Common"))
populateCommonCon("Generic System 2",getContainer1("Migration_Labor_Generic_System2_Common"))
populateCommonCon("Generic System 3",getContainer1("Migration_Labor_Generic_System3_Common"))
populateCommonCon("Generic System 4",getContainer1("Migration_Labor_Generic_System4_Common"))
populateCommonCon("Generic System 5",getContainer1("Migration_Labor_Generic_System5_Common"))
populateCommonCon("QCS RAE Upgrade",getContainer1("Migration_Labor_QCS_RAE_Upgrade_Common"))
populateCommonCon("TPA/PMD Migration",getContainer1("Migration_Labor_TPA_Common"))
# for Extending Logic to generate Migration Project - Excel Pull for Labor Document -- Boya YashwanthKumar : CXCPQ-60198 :start
populateCommonCon("ELEPIU ControlEdge RTU Migration Engineering",getContainer1("Migration_Labor_ELEPIU_Common"))
# for Extending Logic to generate Migration Project - Excel Pull for Labor Document -- Boya YashwanthKumar : CXCPQ-60198 :end
populateCommonCon("PM",getContainer1("Migration_Labor_PM_Common"))