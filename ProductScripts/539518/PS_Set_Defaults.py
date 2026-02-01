def getContainer(Name):
    return Product.GetContainerByName(Name)

attrs = ["SM_RG_ATEX Compliance_and_Enclosure_Type_Cont", "SM_RG_Cabinet_Details_Cont_Left","SM_SC_Universal_Safety_Cab_1_3M_Details_cont", "SM_RG_Universal_Safety_Cabinet_1.3M_Cont", "SM_RG_Cabinet_Details_Cont","SM_RG_Universal_Marshalling_Cabinet_Details"]
for attr in attrs:
    container = getContainer(attr)
    Trace.Write(attr)
    if container.Rows.Count == 0:
        row = container.AddNewRow(False)
        if attr == 'SM_RG_ATEX Compliance_and_Enclosure_Type_Cont':
            row.GetColumnByName('ATEX_Compliance').SetAttributeValue('No')
            enclosure_type =  'Universal Safety Cab-1.3M'
            row.SetColumnValue('Enclosure_Type',enclosure_type)
            row.GetColumnByName('Enclosure_Type').SetAttributeValue(enclosure_type)
            Product.Attr('SM_RG_Enclosure_Type').AssignValue(enclosure_type)
        elif attr == 'SM_RG_Universal_Safety_Cabinet_1.3M_Cont':
            row.GetColumnByName('Specify_Identifier_Modifier_for_SM_SC_Universal_Safety_Cabinet').SetAttributeValue('No')
            #row.GetColumnByName('Number_of_SM_SC_1.3M_Universal_Safety_Cabinets_(0-63)').SetAttributeValue('0')
            row.SetColumnValue( 'Number_of_SM_SC_1.3M_Universal_Safety_Cabinets_(0-63)', '1')
        elif attr == 'SM_RG_Universal_Marshalling_Cabinet_Details':
            row.GetColumnByName('IP_Rating').SetAttributeValue('IP20')
            row.GetColumnByName('Cabinet').SetAttributeValue('Dual Access')
            row.GetColumnByName('Cabinet Layout').SetAttributeValue('3 Column')
            row.GetColumnByName('Mounting Option').SetAttributeValue('Bracket Mounting')
            row.GetColumnByName('Supply Vendor').SetAttributeValue('Meanwell')
            row.GetColumnByName('Cabinet Power').SetAttributeValue('120/230 VAC')
            row.GetColumnByName('AC Input Voltage').SetAttributeValue('230VAC')
            row.GetColumnByName('Cabinet Fan').SetAttributeValue('No')
            row.GetColumnByName('Cabinet Thermostat').SetAttributeValue('No')
            row.GetColumnByName('Cabinet Light (LED)').SetAttributeValue('No')
            row.GetColumnByName('Utility Socket (230/115 VAC)').SetAttributeValue('Standard PVC FRLS(Fire Retard +Low Smoke')
            row.GetColumnByName('Termination of Spare Wires in Field Cabinets').SetAttributeValue('Not Terminated')
            row.GetColumnByName('SIC cable length for RUSIO/PUIO/ PDIO').SetAttributeValue('0')
            row.GetColumnByName('Percentage of Spare Space').SetAttributeValue('6M')
        elif attr == 'SM_RG_Cabinet_Details_Cont_Left':
            row.GetColumnByName('Cabinet_IP_Rating').SetAttributeValue('IP20')
            # Changes done by RDT--->CCEECOMMBR-6769 by Ravika Pupneja
            row.GetColumnByName('Cabinet_Access').SetAttributeValue('Dual Access')
            row.GetColumnByName('Cabinet_Light').SetAttributeValue('No')
            row.GetColumnByName('Cabinet_Feeder_Voltage').SetAttributeValue('120/230VAC')
            row.GetColumnByName('Cabinet_Thermostat').SetAttributeValue('No')
            row.GetColumnByName('Power_Supply').SetAttributeValue('Redundant')
            row.GetColumnByName('Marshalling_Option').SetAttributeValue('Universal Marshalling')
            row.GetColumnByName('IOTA_Ethernet_Cable_Length').SetAttributeValue('3M')
            row.GetColumnByName('SIC_Length').SetAttributeValue('3M')
            row.GetColumnByName('Fault_Contact_GIIS_Integration_Boards').SetAttributeValue('No')
            row.GetColumnByName('ELD_Module').SetAttributeValue('Yes')
        elif attr == 'SM_SC_Universal_Safety_Cab_1_3M_Details_cont':
            #row.GetColumnByName('Cabinet_Material_Type_Ingress_Protection&Power').SetAttributeValue('316L Stainless 1.3M, IP66')
            row.GetColumnByName('Cabinet_Material_Type_Ingress_Protection').SetAttributeValue('316L Stainless 1.3M, IP66')
            row.GetColumnByName('Ambient_Temperature_Range').SetAttributeValue('Without Fan, Max Ambient +40DegC')
            row.GetColumnByName('S300').SetAttributeValue('Redundant S300')
            row.GetColumnByName('Fiber_Optic_Extender').SetAttributeValue('Single Mode x4 EDS-408A')
            row.GetColumnByName('Field_Termination_Assembly_for_PUIO').SetAttributeValue('Default Marshalling FC-TUIO51/52')
            row.GetColumnByName('Field_Termination_Assembly_for_PDIO').SetAttributeValue('Default Marshalling FC-TDIO51/52')
            row.GetColumnByName('Wire_Routing_Options').SetAttributeValue('No Panduit')
            row.GetColumnByName('PUIO_Count').SetAttributeValue('64')
            row.GetColumnByName('PDIO_Count').SetAttributeValue('0')
            row.GetColumnByName('Power_Supply_Type').SetAttributeValue('20A AC/DC QUINT 4+ PS')
            row.GetColumnByName('Power_Supply_Redundancy').SetAttributeValue('Redundant')
            row.GetColumnByName('Earth_Leakage_Detector_TELD').SetAttributeValue('Grounded Power(No TELD)')
            row.GetColumnByName('IO_Redundancy').SetAttributeValue('Redundant IO')
            row.GetColumnByName('Temperature_Monitoring').SetAttributeValue('No STT650')
            row.GetColumnByName('External _24VDC_Terminal_Block').SetAttributeValue('No External TB')
            row.GetColumnByName('Abu_Dhabi_Build_Loc').SetAttributeValue('No')
            row.SetColumnValue( 'Number_of_Control_Network_Module_0-100', '0')
            row.GetColumnByName('CNM_SFP_Type').SetAttributeValue('None')
        elif attr == 'SM_RG_Cabinet_Details_Cont':
            row.GetColumnByName('SM_Conformally_Coated').SetAttributeValue('Yes')
            row.GetColumnByName('SM_Key_Switch_ModuleRequired').SetAttributeValue('No')
            row.GetColumnByName('SM_MCAR_Blank_Filler').SetAttributeValue('No')
            row.GetColumnByName('SM_Percent_Installed_Spare_IO').SetAttributeValue('0')
            row.GetColumnByName('SM_SDO_UIO_DIO').SetAttributeValue('250')
            row.SetColumnValue('SM_SDO_UIO_DIO','250')
            row.GetColumnByName('SM_SDO_UIO_UnitLoad').SetAttributeValue('750')
            row.SetColumnValue('SM_SDO_UIO_UnitLoad','750')
            row.GetColumnByName('SM_SDO_UIO_Unit_Load').SetAttributeValue('1500')
            row.SetColumnValue('SM_SDO_UIO_Unit_Load','1500')
            row.GetColumnByName('SM_Shutdown_Input_UIO_Redundant').SetAttributeValue('No')
            row.GetColumnByName('SM_Shutdown_Input_UIO').SetAttributeValue('No')
            row.GetColumnByName('SM_Shutdown_Input_DIO_Redundant').SetAttributeValue('No')
            row.GetColumnByName('SM_Shutdown_Input_DIO').SetAttributeValue('No')
            row.GetColumnByName('SM_DI_Relay_resistor_Adapter_UMC').SetAttributeValue('No')
            row.GetColumnByName('SM_DI_DORelay_Adapter_UMC').SetAttributeValue('No')
            row.GetColumnByName('SM_DI_NAMUR_Switches_Adapter_UMC').SetAttributeValue('No')
        row.Calculate()
    container.Calculate()