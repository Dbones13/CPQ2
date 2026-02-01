def getContainer(Name):
    return Product.GetContainerByName(Name)

def getRowData(container,column):
    Container = getContainer(container)
    for row in Container.Rows:
        return row[column]

selectedProducts = list()
for row in getContainer("MSID_Product_Container").Rows:
    selectedProducts.append(row["Product Name"])

if 'CB-EC Upgrade to C300-UHIO' in selectedProducts:#CB-EC Calculations
    CB_Number = int(getRowData("CB_EC_migration_to_C300_UHIO_Configuration_Cont","CB_EC_How_many_CBs_are_being_migrated"))
    EC_Number = int(getRowData("CB_EC_migration_to_C300_UHIO_Configuration_Cont","CB_EC_How_many_ECs_are_being_migrated"))
    KnowRegPoints = getRowData("CB_EC_Services_1_Cont", "CB_EC_Do_you_know_the_number_of AI_AO_Regulatory_points_DI_DO_and_Digital_Composite_points")
    proposalType = Quote.GetCustomField("EGAP_Proposal_Type").Content

    totalRegPoints = int(round((CB_Number * 16 + EC_Number * 16) * 0.6)) #Calculated Value No.3
    totalDigitalCompPoints = int(round(EC_Number * 16 * 0.6)) #Calculated Value No.6
    totalAnalogInputPoints= int(round(totalRegPoints * 0.5))# Calculated Value No.1
    totalAnalogOutputPoints = int(round(totalRegPoints * 0.6))# Calculated Value No.2
    totalDigitalInputPoints = int(round(totalDigitalCompPoints * 0.5))# Calculated Value No.4
    totalDigitalOutputPoints = int(round(totalDigitalCompPoints * 0.6))# Calculated Value No.5
    totalCascadeLoop = int(round(totalRegPoints * 0.4))# Calculated Value No.7
    totalComplexLoop = int(round(totalRegPoints * 0.4))# Calculated Value No.8
    totalAuxFunc = int(round(totalRegPoints * 0.05))# Calculated Value No.9

    CBECServicesCont1 = getContainer('CB_EC_Services_1_Cont')
    for row in CBECServicesCont1.Rows:
        if KnowRegPoints != "Yes":
            row.SetColumnValue('CB_EC_Total_Number_of_Analog_Input_points_HGAIN', str(totalAnalogInputPoints))
            row.SetColumnValue('CB_EC_Total_Number_of_Analog_Output_points_HGAOT', str(totalAnalogOutputPoints))
            row.SetColumnValue('CB_EC_Total_Number_of_Regulatory_points_HGREG', str(totalRegPoints))
            row.SetColumnValue('CB_EC_Total_Number_of_Digital_Input_points_HGDIN', str(totalDigitalInputPoints))
            row.SetColumnValue('CB_EC_Total_Number_of_Digital_Output_points_HGDOT', str(totalDigitalOutputPoints))
            row.SetColumnValue('CB_EC_Total_Number_of_Digital_Composite_points_HGDCP', str(totalDigitalCompPoints))
        if proposalType == "Budgetary":
            row.SetColumnValue('CB_EC_Total_Number_of_Cascade_Loop', str(totalCascadeLoop))
            row.SetColumnValue('CB_EC_Total_Number_of_Complex_Loop', str(totalComplexLoop))
            row.SetColumnValue('CB_EC_Total_Number_of_Aux_function', str(totalAuxFunc))
    CBECServicesCont1.Calculate()

if 'xPM to C300 Migration' in selectedProducts:#xPM to C300 Calculations
    if getRowData("xPM_C300_General_Qns_Cont", "xPM_C300_Number_of_xPMs_to_be_Migrated_to_C300_with_PMIO") != "0" and getRowData("xPM_C300_General_Qns_Cont", "xPM_C300_Number_of_xPMs_to_be_Migrated_to_C300_with_PMIO") != "": 
        xPMC300MigrationCont = getContainer('xPM_C300_Migration_Configuration_Cont')
        for row in xPMC300MigrationCont.Rows:
            if row['xPM_C300_split_of_xPM_CL_into_simple_and_complex'] != "Yes":#Split PM Calculated value
                PM_CL = row['xPM_C300_Number_of_xPM_CL']
                if PM_CL != "" and PM_CL != "0":
                    PM_CLNo = int(PM_CL)
                    simplePMCL = int(round(PM_CLNo * 0.7))
                    complexPMCL = PM_CLNo - simplePMCL
                    row.SetColumnValue('xPM_C300_Number_of_Simple_xPM_CL', str(simplePMCL))
                    row.SetColumnValue('xPM_C300_Number_of_Complex_xPM_CL', str(complexPMCL))
                else:
                    row.SetColumnValue('xPM_C300_Number_of_Simple_xPM_CL', str(0))
                    row.SetColumnValue('xPM_C300_Number_of_Complex_xPM_CL', str(0))
            if row['xPM_C300_split_of_AM_CL_into_simple_medium_complex'] != "Yes":#Split AM Calculated value
                AM_CL = row['xPM_C300_Number_of_AM_CL']
                if AM_CL != "" and AM_CL != "0":
                    AM_CLNo = int(AM_CL)
                    simpleAMCL = int(round(AM_CLNo * 0.4))
                    mediumAMCL = int(round(AM_CLNo * 0.3))
                    complexAMCL = AM_CLNo - simpleAMCL - mediumAMCL
                    row.SetColumnValue('xPM_C300_Number_of_Simple_AM_CL', str(int(simpleAMCL)))
                    row.SetColumnValue('xPM_C300_Number_of_medium_AM_CL', str(int(mediumAMCL)))
                    row.SetColumnValue('xPM_C300_Number_of_complex_AM_CL', str(int(complexAMCL)))
                else:
                    row.SetColumnValue('xPM_C300_Number_of_Simple_AM_CL', str(0))
                    row.SetColumnValue('xPM_C300_Number_of_medium_AM_CL', str(0))
                    row.SetColumnValue('xPM_C300_Number_of_complex_AM_CL', str(0))
        xPMC300MigrationCont.Calculate()