def getContainer(Name):
    return Product.GetContainerByName(Name)
attrs = ["SM_CG_Common_Questions_Cont", "SM_CG_Cabinet_Details_Cont_Left","SM_CG_Cabinet_Details_Cont_Right","Number_SM_Remote_Groups_Cont"]
for attr in attrs:
    container = getContainer(attr)
    Trace.Write(attr)
    if container.Rows.Count == 0:
        row = container.AddNewRow(False)
        if attr == 'SM_CG_Common_Questions_Cont':
            row["SM_SCController_Architecture"] = 'Redundant'
            row.GetColumnByName("SM_SCController_Architecture").SetAttributeValue('Redundant')
            row['SM_Universal_IOTA'] = 'PUIO'
            row.GetColumnByName("SM_Universal_IOTA").SetAttributeValue('PUIO')
            row['SM_Experion_Integration'] = 'SCADA'
            row.GetColumnByName("SM_Experion_Integration").SetAttributeValue('SCADA')
            row['SM_Switch_Safety_IO'] = 'Control Network Module (CNM)'
            row.GetColumnByName("SM_Switch_Safety_IO").SetAttributeValue('Control Network Module (CNM)')
            row['SM_CNM_Switch_Network_IOTA'] = 'CNM CCA IOTA'
            row.GetColumnByName("SM_CNM_Switch_Network_IOTA").SetAttributeValue('CNM CCA IOTA')
            row.GetColumnByName("SM_Safety_Builder_Options").SetAttributeValue('Via FTE')
            #row['SM_Safenet_Options'] = 'Via CNM Separate Red Ethernet'
            #row.SetColumnValue('SM_Safety_Builder_Options', 'Via_FTE')
            #row["SM_Safety_Builder_Options"] = 'Via_FTE'
            row.GetColumnByName("SM_ThirdParty_Communication_Options").SetAttributeValue('Not Required')
            #row['SM_ThirdParty_Communication_Options'] = 'Not Required'
            row['SM_DNP3_ProtocolLicense'] = 'None'
        elif attr == 'SM_CG_Cabinet_Details_Cont_Left':
            row.GetColumnByName('Cabinet_IP_Rating').SetAttributeValue('IP20')
            # Changes done by RDT--->CCEECOMMBR-6769 by Ravika Pupneja
            row.GetColumnByName('Cabinet_Access').SetAttributeValue('Dual Access')
            row.GetColumnByName('Cabinet_Light').SetAttributeValue('No')
            row.GetColumnByName('Cabinet_Feeder_Voltage').SetAttributeValue('120/230VAC')
            row.GetColumnByName('Cabinet_Thermostat').SetAttributeValue('No')
            row.GetColumnByName('Power_Supply').SetAttributeValue('Redundant')
            row.SetColumnValue('Marshalling_Option', 'Universal_Marshalling')
            row.GetColumnByName('Marshalling_Option').SetAttributeValue('Universal Marshalling')
            Product.Attr('Universal Marshalling Cabinet').AssignValue('Universal Marshalling')
            row.GetColumnByName('IOTA_Ethernet_Cable_Length').SetAttributeValue('3M')
            row.GetColumnByName('SIC_Length').SetAttributeValue('3M')
            row.GetColumnByName('Fault_Contact_GIIS_Integration_Boards').SetAttributeValue('No')
            row.GetColumnByName('ELD_Module').SetAttributeValue('Yes')
            #row.GetColumnByName('Distance_SM_SC_UIO/DIO_modules').SetAttributeValue('70km Single Mode SFP')
            row.GetColumnByName('Distance_SM_SC_UIO/DIO_modules').ReferencingAttribute.SelectDisplayValue('70km Single Mode SFP')
            row.GetColumnByName('SM_CG_RelayTypeForESD').SetAttributeValue('Non SIL')
            row['SM_CG_RelayTypeForESD'] = 'Non SIL'
            row.Product.Attr('SM_General_RelayTypeForESD').SelectDisplayValue('Non SIL')
        elif attr == 'SM_CG_Cabinet_Details_Cont_Right':
            row.GetColumnByName('Conformally_Coated').SetAttributeValue('Yes')
            row.GetColumnByName('Key_Switch_Module_Required').SetAttributeValue('No')
            row.GetColumnByName('MCAR_Blank_Filler').SetAttributeValue('No')
            row.GetColumnByName('Shutdown_Input_UIO_Redundant').SetAttributeValue('No')
            row.GetColumnByName('Shutdown_Inpu_UIO').SetAttributeValue('No')
            row.GetColumnByName('Shutdown_Input_DIO_Redundant').SetAttributeValue('No')
            row.GetColumnByName('Shutdown_Input_DIO').SetAttributeValue('No')
            row.GetColumnByName('DI_SIL1_Relay_5K_resistor_Adapter_UMC').SetAttributeValue('No')
            row.GetColumnByName('DI/DO_SIL2/3_Relay_Adapter_UMC').SetAttributeValue('No')
            row.GetColumnByName('DI_NAMUR_proximity_Switches_Adapter_UMC').SetAttributeValue('No')
            row.SetColumnValue( 'SDO_24Vdc_500mA_UIO_DIO_UnitLoad1mA-500mA', '250')
            row.SetColumnValue( 'SDO_2_24Vdc1A_UIO_Unit_Load_501mA_1000mA', '750')
            row.SetColumnValue( 'SDO_4_24Vdc2A_UIO_Unit_Load_1001mA_2000mA', '1500')
        elif attr == 'Number_SM_Remote_Groups_Cont':
            row.SetColumnValue( 'Number_SM_Remote_Groups', '0')
        row.Calculate()
    container.Calculate()