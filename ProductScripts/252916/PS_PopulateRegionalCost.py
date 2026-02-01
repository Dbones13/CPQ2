def getContainer(product,Name):
    return product.GetContainerByName(Name)

def addFinalHours(totalDict , partNumber,key, value):
    partDict = totalDict.get(partNumber,dict())
    partDict[key] = getFloat(partDict.get(key , 0)) + getFloat(value)
    totalDict[partNumber] = partDict

def getFloat(Var):
    if Var:
        return float(Var)
    return 0

def getpartNumbersData(container,product):
    partsNumbers[productCon[product]] = dict()
    for row in container.Rows:
        if row["Regional_Cost"] not in ('',0.0):
            addFinalHours(partsNumbers[productCon[product]],row["FO_Eng"],"Cost",row["Regional_Cost"])
            addFinalHours(partsNumbers[productCon[product]],row["FO_Eng"],"Qty",(round(getFloat(row["Final_Hrs"]) * getFloat(row["FO_Eng_Percentage_Split"]) / 100)))
        if row["FOUnitWTWCost"] not in ('',0.0):
            addFinalHours(partsNumbers[productCon[product]],row["FO_Eng"],"WTWCost",row["FOUnitWTWCost"])
        if row["GES_Regional_Cost"] not in ('',0.0):
            addFinalHours(partsNumbers[productCon[product]],row["GES_Eng"],"Cost",row["GES_Regional_Cost"])
            addFinalHours(partsNumbers[productCon[product]],row["GES_Eng"],"Qty",(round(getFloat(row["Final_Hrs"]) * getFloat(row["GES_Eng_Percentage_Split"]) / 100)))
        if row["FO_ListPrice"] not in ('',0.0):
            addFinalHours(partsNumbers[productCon[product]],row["FO_Eng"],"ListPrice",row["FO_ListPrice"])
        if row["GES_ListPrice"] not in ('',0.0):
            addFinalHours(partsNumbers[productCon[product]],row["GES_Eng"],"ListPrice",row["GES_ListPrice"])
        if row["GES_MPA_Price"] not in ('',0.0):
            addFinalHours(partsNumbers[productCon[product]],row["GES_Eng"],"MPAPrice",row["GES_MPA_Price"])
            addFinalHours(partsNumbers[productCon[product]],row["GES_Eng"],"MPAQty",(round(getFloat(row["Final_Hrs"]) * getFloat(row["GES_Eng_Percentage_Split"]) / 100)))
        if row["FO_MPA_Price"] not in ('',0.0):
            addFinalHours(partsNumbers[productCon[product]],row["FO_Eng"],"MPAPrice",row["FO_MPA_Price"])
            addFinalHours(partsNumbers[productCon[product]],row["FO_Eng"],"MPAQty",(round(getFloat(row["Final_Hrs"]) * getFloat(row["FO_Eng_Percentage_Split"]) / 100)))

msidContainer = Product.GetContainerByName("Migration_MSID_Selection_Container")
for row in msidContainer.Rows:
    msidProduct = row.Product
    msidproductCon = msidProduct.GetContainerByName("MSID_Product_Container")
    productCon = dict()
    partsNumbers = dict()
    laborParts = dict()
    laborPartsListPrice = dict()
    msidproductVirtCon = msidProduct.GetContainerByName("MSID_Product_Container_Virtualization_hidden")
    msidproductGenericCon = msidProduct.GetContainerByName("MSID_Product_Container_Generic_hidden")
    for row in msidproductCon.Rows:
        productCon[row["Product Name"]] = row.UniqueIdentifier
        if row["Product Name"] == "FSC to SM":
            msidfscCon = msidProduct.GetContainerByName("MSID_Product_Container_FSC_hidden")
            rowfsc = msidfscCon.Rows[0]
            productCon[rowfsc["Product Name"]] = rowfsc.UniqueIdentifier
        if row["Product Name"] == "FSC to SM IO Migration":
            msidfscIoCon = msidProduct.GetContainerByName("MSID_Product_Container_FSC_IO_hidden")
            rowfscIO = msidfscIoCon.Rows[0]
            productCon[rowfscIO["Product Name"]] = rowfscIO.UniqueIdentifier

    for row in msidproductVirtCon.Rows:
        productCon[row["Product Name"]] = row.UniqueIdentifier

    for row in msidproductGenericCon.Rows:
        productCon[row["Product Name"]] = row.UniqueIdentifier

    opmEngineeringCon = getContainer(msidProduct,"MSID_Labor_OPM_Engineering")
    lcnOneTimeUpgradeCon = getContainer(msidProduct,"MSID_Labor_LCN_One_Time_Upgrade_Engineering")
    ebrCon = getContainer(msidProduct,"MSID_Labor_EBR_Con")
    elcnCon = getContainer(msidProduct,"MSID_Labor_ELCN_Con")
    orionConsoleCon = getContainer(msidProduct,"MSID_Labor_Orion_Console_Con")
    ehpmCon = getContainer(msidProduct,"MSID_Labor_EHPM_C300PM_Con")
    tpsCon = getContainer(msidProduct,"MSID_Labor_TPS_TO_EXPERION_Con")
    tcmiCon = getContainer(msidProduct,"MSID_Labor_TCMI_Con")
    ehpmhartioCon = getContainer(msidProduct,"MSID_Labor_EHPM_HART_IO_Con")
    c200MigrationCon = getContainer(msidProduct,"MSID_Labor_C200_Migration_Con")
    cbecCon = getContainer(msidProduct,"MSID_Labor_CB-EC_Upgrade_to_C300-UHIO_con")
    xpmCon = getContainer(msidProduct,"MSID_Labor_xPM_to_C300_Migration_Con")
    fdmCon = getContainer(msidProduct,"MSID_Labor_FDM_Upgrade_Con")
    fscCon = getContainer(msidProduct,"MSID_Labor_FSC_to_SM_con")
    lmCon = getContainer(msidProduct,"MSID_Labor_LM_to_ELMM_Con")
    fscauditCon = getContainer(msidProduct,"MSID_Labor_FSC_to_SM_audit_Con")
    XP10Con = getContainer(msidProduct,"MSID_Labor_XP10_Actuator_Upgrade_con")
    GraphicsCon = getContainer(msidProduct,"MSID_Labor_Graphics_Migration_con")
    fscsmioCon = getContainer(msidProduct,"MSID_Labor_FSCtoSM_IO_con")
    CDActuatorCon = getContainer(msidProduct,"MSID_Labor_CD_Actuator_con")
    CWSRAECon = getContainer(msidProduct,"MSID_Labor_CWS_RAE_Upgrade_con")
    qcsraeCon = getContainer(msidProduct,"MSID_Labor_QCS_RAE_Upgrade_con")
    plcuocCon = getContainer(msidProduct,"3rd_Party_PLC_UOC_Labor")
    virtualizationCon = getContainer(msidProduct,"MSID_Labor_Virtualization_con")
    tpaCon = getContainer(msidProduct,"MSID_Labor_TPA_con")
    fscauditIOCon = getContainer(msidProduct,"MSID_Labor_FSC_to_SM_IO_Audit_Con")
    # Added 'MSID_Labor_ELEPIU_con' in the below container list -- Janhavi Tanna : CXCPQ-60180 :start
    ELEPIUCon = getContainer(msidProduct,"MSID_Labor_ELEPIU_con")
    #-- Janhavi Tanna : CXCPQ-60180 :end
    projectManagementCon = getContainer(msidProduct,"MSID_Labor_Project_Management")
    genericSystem1 = getContainer(msidProduct,"MSID_Labor_Generic_System1_Cont")
    genericSystem2 = getContainer(msidProduct,"MSID_Labor_Generic_System2_Cont")
    genericSystem3 = getContainer(msidProduct,"MSID_Labor_Generic_System3_Cont")
    genericSystem4 = getContainer(msidProduct,"MSID_Labor_Generic_System4_Cont")
    genericSystem5 = getContainer(msidProduct,"MSID_Labor_Generic_System5_Cont")

    if productCon.get("OPM"):
        getpartNumbersData(opmEngineeringCon,"OPM")
    if productCon.get("LCN One Time Upgrade"):
        getpartNumbersData(lcnOneTimeUpgradeCon,"LCN One Time Upgrade")
    if productCon.get("EBR"):
        getpartNumbersData(ebrCon,"EBR")
    if productCon.get("ELCN"):
        getpartNumbersData(elcnCon,"ELCN")
    if productCon.get("Orion Console"):
        getpartNumbersData(orionConsoleCon,"Orion Console")
    if productCon.get("EHPM/EHPMX/ C300PM"):
        getpartNumbersData(ehpmCon,"EHPM/EHPMX/ C300PM")
    if productCon.get("TPS to Experion"):
        getpartNumbersData(tpsCon,"TPS to Experion")
    if productCon.get("TCMI"):
        getpartNumbersData(tcmiCon,"TCMI")
    if productCon.get("EHPM HART IO"):
        getpartNumbersData(ehpmhartioCon,"EHPM HART IO")
    if productCon.get("C200 Migration"):
        getpartNumbersData(c200MigrationCon,"C200 Migration")
    if productCon.get("CB-EC Upgrade to C300-UHIO"):
        getpartNumbersData(cbecCon,"CB-EC Upgrade to C300-UHIO")
    if productCon.get("xPM to C300 Migration"):
        getpartNumbersData(xpmCon,"xPM to C300 Migration")
    if productCon.get("FDM Upgrade"):
        getpartNumbersData(fdmCon,"FDM Upgrade")
    if productCon.get("FSC to SM"):
        getpartNumbersData(fscCon,"FSC to SM")
    if productCon.get("FSC to SM Audit"):
        getpartNumbersData(fscauditCon,"FSC to SM Audit")
    if productCon.get("LM to ELMM ControlEdge PLC"):
        getpartNumbersData(lmCon,"LM to ELMM ControlEdge PLC")
    if productCon.get("XP10 Actuator Upgrade"):
        getpartNumbersData(XP10Con,"XP10 Actuator Upgrade")
    if productCon.get("CWS RAE Upgrade"):
        getpartNumbersData(CWSRAECon,"CWS RAE Upgrade")
    if productCon.get("Graphics Migration"):
        getpartNumbersData(GraphicsCon,"Graphics Migration")
    if productCon.get("CD Actuator I-F Upgrade"):
        getpartNumbersData(CDActuatorCon,"CD Actuator I-F Upgrade")
    if productCon.get("FSC to SM IO Migration"):
        getpartNumbersData(fscsmioCon,"FSC to SM IO Migration")
    if productCon.get("FSC to SM IO Audit"):
        getpartNumbersData(fscauditIOCon,"FSC to SM IO Audit")
    if productCon.get("3rd Party PLC to ControlEdge PLC/UOC"):
        getpartNumbersData(plcuocCon,"3rd Party PLC to ControlEdge PLC/UOC")
    if productCon.get("QCS RAE Upgrade"):
        getpartNumbersData(qcsraeCon,"QCS RAE Upgrade")
    if productCon.get("Virtualization System"):
        getpartNumbersData(virtualizationCon,"Virtualization System")
     # Fetch Parts Number for 'MSID_Labor_ELEPIU_con' in the below container list -- Janhavi Tanna : CXCPQ-60180 :start
    if productCon.get("ELEPIU ControlEdge RTU Migration Engineering"):
        getpartNumbersData(ELEPIUCon,"ELEPIU ControlEdge RTU Migration Engineering")
   #-- Janhavi Tanna : CXCPQ-60180 :end
    if productCon.get("TPA/PMD Migration"):
        getpartNumbersData(tpaCon,"TPA/PMD Migration")
    if productCon.get("Project Management"):
        getpartNumbersData(projectManagementCon,"Project Management")
    if productCon.get("Generic System 1"):
        getpartNumbersData(genericSystem1,"Generic System 1")
    if productCon.get("Generic System 2"):
        getpartNumbersData(genericSystem2,"Generic System 2")
    if productCon.get("Generic System 3"):
        getpartNumbersData(genericSystem3,"Generic System 3")
    if productCon.get("Generic System 4"):
        getpartNumbersData(genericSystem4,"Generic System 4")
    if productCon.get("Generic System 5"):
        getpartNumbersData(genericSystem5,"Generic System 5")
    Trace.Write(str(partsNumbers))
    #Trace.Write(str(laborParts))
    #Trace.Write(str(laborPartsListPrice))
    if partsNumbers:
        for item in arg.QuoteItemCollection:
            if item.ParentItemGuid in partsNumbers:
                module =  partsNumbers[item.ParentItemGuid]
                partData = module.get(item.PartNumber,'')
                #item.QI_Manual_labor_Regional_Cost.Value = float(x.get(item.PartNumber,0))
                if partData:
                    if "Cost" in partData and getFloat(partData.get("Qty",0))>0:
                        unitCost = getFloat(partData.get("Cost",0)) / getFloat(partData.get("Qty",0))
                        Trace.Write("Test2 = " + str(unitCost))
                        item.QI_GESRegionalCost.Value = getFloat(unitCost) if unitCost else 0
                    if "WTWCost" in partData and getFloat(partData.get("Qty",0))>0:
                        unitWtwCost = getFloat(partData.get("WTWCost",0)) / getFloat(partData.get("Qty",0))
                        Trace.Write("Test3 = " + str(unitWtwCost))
                        item.QI_FoWTWCost.Value = getFloat(unitWtwCost) if unitWtwCost else 0
                    if "ListPrice" in partData and getFloat(partData.get("Qty",0))>0:
                        unitListPrice = getFloat(partData.get("ListPrice",0)) / getFloat(partData.get("Qty",0))
                        Trace.Write("Test4 = " + str(unitListPrice))
                        item.QI_LaorPartsListPrice.Value = getFloat(unitListPrice) if unitListPrice else 0
                    if "MPAPrice" in partData and getFloat(partData.get("MPAQty",0))>0:
                        unitMPAPrice = getFloat(partData.get("MPAPrice",0)) / getFloat(partData.get("MPAQty",0))
                        item.QI_MPA_Price.Value = getFloat(unitMPAPrice) if unitMPAPrice else 0
Quote.Calculate()