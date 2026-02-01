isR2Qquote = True if Quote.GetCustomField("isR2QRequest").Content else False
if not isR2Qquote:
    import math
    msidCont = Product.GetContainerByName("CONT_MSID_SUBPRD")
    msid_product = Product
    for row in msidCont.Rows:
        #msid_product = row.Product
        if row['Selected_Products'] == 'OPM':
            from GS_MigrationLaborHoursModule_new import getnumberOfjumpRealease,checkForMPACustomer,calculateTotals
            from GS_MigrationLaborHoursModule_1_new import getDataGatheringHours,getDOcumentationHours,getPreFATSAT,getMigration2Hours,getSATHours,getMigrationL1Hours,getPostMigrationTask,getOpmMcoe,getOPMDeploymentL2
            from GS_MigrationLaborHoursModule_2 import calculateFinalHours1,reCalAdj
            from GS_MigrationLaborHoursModule_4New import calculateEMPEfforts
            def getContainer(Product,Name):
                return Product.GetContainerByName(Name)

            def getRowData(Product,container,column):
                Container = getContainer(Product,container)
                for row in Container.Rows:
                    return row[column]

            def getRowDataIndex(Product,container,column,index):
                Container = getContainer(Product,container)
                for row in Container.Rows:
                    if row.RowIndex == index:
                        return row[column]
            def getAttrData(Product,attr):
                return Product.Attr(attr).GetValue()
            def getFloat(Var):
                if Var:
                    return float(Var)
                return 0

            def getTotalEngHours(Product,container):
                totalFinalHours = 0
                if getContainer(Product,container):
                    for row in getContainer(Product,container).Rows:
                        if row["Deliverable"] == "Total":
                            totalFinalHours += getFloat(row["Final_Hrs"])
                return totalFinalHours

            mpaAvailable = checkForMPACustomer(TagParserQuote)
            entitlement = Quote.GetCustomField("Entitlement").Content if Quote is not None else ""
            opmEngineeringCon = getContainer(Product,"MSID_Labor_OPM_Engineering")
            parameters = {"MSID_CommonQuestions":{"Var_22":"MSID_FEL_Data_Gathering_Required","Var_5":"MSID_Current_Experion_Release","Var_6":"MSID_Future_Experion_Release"},"OPM_Node_Configuration":{"Var_1":"OPM_No_of_Experion_Servers","Var_2_1":"OPM_No_of_ACET_Servers_LCN_Connected","Var_2_2":"OPM_No_of_EAPP_Servers_LCN_Connected","Var_3_1":"OPM_Qty_of_ESF_and_ES-CE_Rack_Mount","Var_3_2":"OPM_Qty_of_ESF_and_ESCE_Tower","Var_27_1":"OPM_Qty_of_ESC_Rack_Mount","Var_27_2":"OPM_Qty_of_ESC_Tower","Var_4_1":"OPM_No_of_EST_Rack_mount","Var_4_2":"OPM_No_of_EST_Tower","Var_8":"OPM_No_of_Other_Servers_to_be_migrated","Var_9":"OPM_Qty_of_RPS_and_Thin_Clients","Var_10":"OPM_Qty_of_Series_C_Controllers","Var_11":"OPM_Qty_of_Profibus_Modules","Var_12":"OPM_Qty_of_Control_Firewalls_CF9s","Var_13":"OPM_Qty_of_Series_C_IO_Modules_excluding_UIO","Var_14":"OPM_Qty_of_Fieldbus_Interface_Modules","Var_25":"OPM_Qty_of_Series_A_IO_Modules","Var_26":"OPM_Qty_of_UIO_UIO2_Modules"},"OPM_Services":{"Var_32":"OPM_is_system_required_Domain_controller_upgrade","Var_33":"ATT_OPMADNLHRS","Var_23":"OPM_Acceptance_Test_Required"},"OPM_Basic_Information":{"Var_24":"OPM_RESS_Migration_in_scope","Var_21":"OPM_Is_the_Experion_System_LCN_Connected","Var_31":"OPM_Is_this_is_a_Remote_Migration_Service_RMS"},"OPM_FTE_Switches_migration_info":{"Var_28":"ATT_OPMQTYSWTS","Var_29":"ATT_OPMQTYBBON"}}
            Var_28,Var_29=0,0
            product = row.Product
            for key in parameters:
                if key == "MSID_CommonQuestions":
                    Var_22 = getAttrData(Product,parameters[key]["Var_22"])
                    Var_5 = getAttrData(Product,parameters[key]["Var_5"])
                    Var_6 = getAttrData(Product,parameters[key]["Var_6"])

                if key == "OPM_Node_Configuration":
                    Var_1 = getFloat(getRowData(product,key,parameters[key]["Var_1"]))
                    Var_2 = getFloat(getRowData(product,key,parameters[key]["Var_2_1"])) + getFloat(getRowData(product,key,parameters[key]["Var_2_2"]))
                    Var_3 = getFloat(getRowData(product,key,parameters[key]["Var_3_1"])) + getFloat(getRowData(product,key,parameters[key]["Var_3_2"]))
                    Var_27 = getFloat(getRowData(product,key,parameters[key]["Var_27_1"])) + getFloat(getRowData(product,key,parameters[key]["Var_27_2"]))
                    Var_4 = getFloat(getRowData(product,key,parameters[key]["Var_4_1"])) + getFloat(getRowData(product,key,parameters[key]["Var_4_2"]))
                    Var_8 = getFloat(getRowData(product,key,parameters[key]["Var_8"]))
                    Var_9 = getFloat(getRowData(product,key,parameters[key]["Var_9"]))
                    Var_10 = getFloat(getRowData(product,key,parameters[key]["Var_10"]))
                    Var_11 = getFloat(getRowData(product,key,parameters[key]["Var_11"]))
                    Var_12 = getFloat(getRowData(product,key,parameters[key]["Var_12"]))
                    Var_13 = getFloat(getRowData(product,key,parameters[key]["Var_13"]))
                    Var_14 = getFloat(getRowData(product,key,parameters[key]["Var_14"]))
                    Var_25 = getFloat(getRowData(product,key,parameters[key]["Var_25"]))
                    Var_26 = getFloat(getRowData(product,key,parameters[key]["Var_26"]))

                elif key == "OPM_Services":
                    Var_32 = getAttrData(product,parameters[key]["Var_32"])
                    Var_33 = getAttrData(product,parameters[key]["Var_33"])
                    Var_23 = getAttrData(product,parameters[key]["Var_23"])
                elif key == "OPM_Basic_Information":
                    ressScope = getRowData(product,key,parameters[key]["Var_24"])
                    Var_24 = 0
                    Var_31 = getRowData(product,key,parameters[key]["Var_31"])
                    if ressScope == "Yes":
                        Var_24 = 1
                    elif ressScope == "No":
                        Var_24 = 0
                    Var_21 = getRowData(product,key,parameters[key]["Var_21"])
                elif key == "OPM_FTE_Switches_migration_info":
                    Var_28 = getFloat(getAttrData(product,parameters[key]["Var_28"]))
                    Var_29 = getFloat(getAttrData(product,parameters[key]["Var_29"]))
                Var_7 = getFloat(getnumberOfjumpRealease(Product,product))
            Var_30 = "No" if Quote and Quote.GetCustomField("Entitlement").Content in ('','None','Non-SESP MSID with new SESP Flex','Support Flex') else "Yes"
            additonOfParamenters = Var_1 + Var_2 + Var_3 + Var_4 + Var_8 + Var_27
            if Var_1 > 0:
                updatedAdditonOfParamenters = Var_1 + math.ceil((Var_2 + Var_3 + Var_4 + Var_8 + Var_27)/(Var_1/2))
            else:
                updatedAdditonOfParamenters = 0
                #Var_7 = getFloat(getnumberOfjumpRealease(Product,product))
            if opmEngineeringCon.Rows.Count > 0:
                for row in opmEngineeringCon.Rows:
                    oldCalHrs = row["Calculated_Hrs"]
                    if row["Deliverable"] == "OPM Plan Review & Migration Registration KOM":
                        kom = 8
                        if Var_31 == 'Yes':
                            kom+=1
                        row["Calculated_Hrs"] = str(kom)
                        row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
                        row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
                    elif row["Deliverable"] == "OPM HW/SW Order To Factory":
                        row["Calculated_Hrs"] = "4"
                        row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
                        row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
                    elif row["Deliverable"] == "OPM Pre-Migration Audit":
                        '''if mpaAvailable or entitlement in ('K&E Pricing Plus','K&E Pricing Flex'):
                            row["Calculated_Hrs"] = "0"
                        else:
                            row["Calculated_Hrs"] = "4"
                            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
                            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)'''
                        if Var_31 in ('No',''):
                            if Var_30 != 'No':
                                row["Calculated_Hrs"] = "0"
                            else:
                                row["Calculated_Hrs"] = "4"
                                row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
                                row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
                        else:
                            row["Calculated_Hrs"] = "0"
                            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
                            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
                    elif row["Deliverable"] == "OPM Site Visit Data Gathering":
                        row["Calculated_Hrs"] = str(getDataGatheringHours(Var_7,Var_22,Var_31,updatedAdditonOfParamenters,Var_1))
                        row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
                        row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
                    elif row["Deliverable"] == "OPM Documentation":
                        row["Calculated_Hrs"] = str(getDOcumentationHours(product,Var_32,Var_33,additonOfParamenters))
                        row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
                        row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
                    elif row["Deliverable"] == "OPM Pre-FAT & FAT":
                        row["Calculated_Hrs"] = str(getPreFATSAT(Var_31, Var_23, Var_4, Var_27, Var_7, Var_3, Var_8, Var_24, Var_9, Var_28, Var_29, Var_21, Var_10, Var_1, Var_2))
                        row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
                        row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
                    elif row["Deliverable"] == "OPM Migration L2":
                        row["Calculated_Hrs"] = str(getMigration2Hours(Var_23,Var_4,Var_27,Var_7,Var_3,Var_8,Var_24,Var_9,Var_28,Var_29,Var_10,Var_1,Var_2,Var_21,Var_31))
                        row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
                        row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
                    elif row["Deliverable"] == "OPM Migration L1":
                        #row["Calculated_Hrs"] = str(getMigrationL1Hours(Var_10,Var_7,Var_14,Var_11,Var_12,Var_13,Var_26,Var_25,Var_5))
                        row["Calculated_Hrs"] = str(getMigrationL1Hours(Var_10,Var_7,Var_14,Var_11,Var_12,Var_13,Var_26,Var_25,Var_5,Var_6))
                        row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
                        row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
                    elif row["Deliverable"] == "OPM SAT":
                        row["Calculated_Hrs"] = str(getSATHours(Var_23))
                        row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
                        row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
                    elif row["Deliverable"] == "OPM Post Migration Task":
                        row["Calculated_Hrs"] = str(getPostMigrationTask(additonOfParamenters))
                        row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
                        row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
                    elif row["Deliverable"] == "OPM Deployment L2 - AMT":
                        row["Calculated_Hrs"] = str(getOPMDeploymentL2(Var_31,Var_1,Var_2,Var_3,Var_4,Var_7,Var_8,Var_9,Var_24,Var_27,Var_28,Var_29,Var_6,Var_5))
                        row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
                        row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
                    elif row["Deliverable"] == "OPM MCOE - AMT":
                        row["Calculated_Hrs"] = str(getOpmMcoe(Var_1,Var_2,Var_3,Var_4,Var_7,Var_8,Var_9,Var_10,Var_21,Var_23,Var_24,Var_27,Var_28,Var_29,Var_31,Var_6,Var_5))
                        row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
                        row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)

                if getRowData(product,"OPM_Basic_Information","OPM_Is_this_is_a_Remote_Migration_Service_RMS") == "Yes":
                    for row in opmEngineeringCon.Rows:
                        oldCalHrs = row["Calculated_Hrs"]
                        if row["Deliverable"] not in ('Off-Site','On-Site','Total'):
                            if row["Calculated_Hrs"] not in ('',"0.00"):
                                #row["Calculated_Hrs"] = str(getFloat(row["Calculated_Hrs"]) * 0.88)
                                row["Calculated_Hrs"] = str(getFloat(row["Calculated_Hrs"]))#Refer CCEECOMMBR-3645
                                row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
                                row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
                calculateEMPEfforts(msid_product,opmEngineeringCon)
                calculateTotals(opmEngineeringCon)