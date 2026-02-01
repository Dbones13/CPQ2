def getContainer(Name):
    return Product.GetContainerByName(Name)

def getRowData(container,column):
    Container = getContainer(container)
    for row in Container.Rows:
        return row[column]

CB_Number = int(getRowData("CB_EC_migration_to_C300_UHIO_Configuration_Cont","CB_EC_How_many_CBs_are_being_migrated"))
EC_Number = int(getRowData("CB_EC_migration_to_C300_UHIO_Configuration_Cont","CB_EC_How_many_ECs_are_being_migrated"))
KnowRegPoints = getRowData("CB_EC_Services_1_Cont", "CB_EC_Do_you_know_the_number_of AI_AO_Regulatory_points_DI_DO_and_Digital_Composite_points")
proposalType = Quote.GetCustomField("EGAP_Proposal_Type").Content

totalRegPoints = round((CB_Number * 16 + EC_Number * 16) * 0.6) #Calculated Value No.3
totalDigitalCompPoints = round(EC_Number * 16 * 0.6) #Calculated Value No.6
totalAnalogInputPoints= round(totalRegPoints * 0.5)# Calculated Value No.1
totalAnalogOutputPoints = round(totalRegPoints * 0.6)# Calculated Value No.2
totalDigitalInputPoints = round(totalDigitalCompPoints * 0.5)# Calculated Value No.4
totalDigitalOutputPoints = round(totalDigitalCompPoints * 0.6)# Calculated Value No.5
totalCascadeLoop = round(totalRegPoints * 0.4)# Calculated Value No.7
totalComplexLoop = round(totalRegPoints * 0.4)# Calculated Value No.8
totalAuxFunc = round(totalRegPoints * 0.05)# Calculated Value No.9

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