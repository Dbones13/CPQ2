con = Product.GetContainerByName('SM_CG_Cabinet_Details_Cont_Left')
if con.Rows.Count == 1:
    check_1 = con.Rows[0]
    check = check_1.GetColumnByName("Marshalling_Option").DisplayValue
    cab_cont = Product.GetContainerByName('SM_CG_Universal_Marshalling_Cabinet_Details')
    if check in ("Universal Marshalling"):
        if cab_cont.Rows.Count == 0:
            row = cab_cont.AddNewRow(False)
            row.GetColumnByName('IP_Rating').SetAttributeValue('IP20')
            row.GetColumnByName('Cabinet').SetAttributeValue('Dual Access')
            row.GetColumnByName('Cabinet Layout').ReferencingAttribute.SelectDisplayValue('3 Column')
            row.GetColumnByName('Mounting Option').SetAttributeValue('Bracket Mounting')
            row.GetColumnByName('Supply Vendor').SetAttributeValue('Honeywell')
            row.GetColumnByName('Cabinet Power').SetAttributeValue('120/230VAC')
            row.GetColumnByName('AC Input Voltage').SetAttributeValue('230VAC')
            row.GetColumnByName('Cabinet Fan').SetAttributeValue('No')
            row.GetColumnByName('Cabinet Thermostat').SetAttributeValue('No')
            row.GetColumnByName('Cabinet Light (LED)').SetAttributeValue('No')
            row.GetColumnByName('Utility Socket (230/115 VAC)').SetAttributeValue('No')
            row.GetColumnByName('Wiring & Ducts').SetAttributeValue('Standard PVC FRLS(Fire Retard +Low Smoke)')
            row.GetColumnByName('Termination of Spare Wires in Field Cabinets').SetAttributeValue('Not Terminated')
            row.GetColumnByName('Percentage of Spare Space').SetAttributeValue('0')
            row.GetColumnByName('SIC cable length for RUSIO/PUIO/ PDIO').SetAttributeValue('6M')
            #row.GetColumnByName('SM_CG_RelayTypeForESD').SetAttributeValue('Non SIL')
            #cab_cont.Rows[0].Product.ApplyRules()
            row.ApplyProductChanges()
            row.Calculate()
    else:
        if cab_cont.Rows.Count > 0:
            cab_cont.Rows.Clear()
            cab_cont.Calculate()
            
#rule name:cabinet_Q_Visibility condition 1
#rule name:Cabinet_Q_Visibility2 condition 1
get_cont_1=Product.GetContainerByName('SM_CG_Cabinet_Details_Cont_Left').Rows
for row in get_cont_1:
    if row['Marshalling_Option'] =='Universal Marshalling':
        Product.ParseString('<CTX( Container({}).Column({}).SetPermission(Editable) )>'.format('SM_CG_Cabinet_Details_Cont_Right', 'DI_SIL1_Relay_5K_resistor_Adapter_UMC'))
        Product.ParseString('<CTX( Container({}).Column({}).SetPermission(Editable) )>'.format('SM_CG_Cabinet_Details_Cont_Right', 'DI/DO_SIL2/3_Relay_Adapter_UMC'))
        Product.ParseString('<CTX( Container({}).Column({}).SetPermission(Editable) )>'.format('SM_CG_Cabinet_Details_Cont_Right', 'DI_NAMUR_proximity_Switches_Adapter_UMC'))
    elif row['Marshalling_Option'] =='Hardware Marshalling with P+F':
        Product.ParseString('<CTX( Container({}).Column({}).SetPermission(Editable) )>'.format('SM_CG_Cabinet_Details_Cont_Left', 'Fault_Contact_GIIS_Integration_Boards'))
    else:
        Product.ParseString('<CTX( Container({}).Column({}).SetPermission(Hidden) )>'.format('SM_CG_Cabinet_Details_Cont_Left', 'Fault_Contact_GIIS_Integration_Boards'))
        Product.ParseString('<CTX( Container({}).Column({}).SetPermission(Editable) )>'.format('SM_CG_Cabinet_Details_Cont_Left', 'SM_CG_RelayTypeForESD'))
        #Trace.Write('Editable is SM_CG_RelayTypeForESD')
        Product.ParseString('<CTX( Container({}).Column({}).SetPermission(Hidden) )>'.format('SM_CG_Cabinet_Details_Cont_Right', 'DI_SIL1_Relay_5K_resistor_Adapter_UMC'))
        Product.ParseString('<CTX( Container({}).Row(1).Column({}).Set(No) )>'.format('SM_CG_Cabinet_Details_Cont_Right', 'DI_SIL1_Relay_5K_resistor_Adapter_UMC'))
        Product.ParseString('<CTX( Container({}).Column({}).SetPermission(Hidden) )>'.format('SM_CG_Cabinet_Details_Cont_Right', 'DI/DO_SIL2/3_Relay_Adapter_UMC'))
        Product.ParseString('<CTX( Container({}).Row(1).Column({}).Set(No) )>'.format('SM_CG_Cabinet_Details_Cont_Right', 'DI/DO_SIL2/3_Relay_Adapter_UMC'))
        Product.ParseString('<CTX( Container({}).Column({}).SetPermission(Hidden) )>'.format('SM_CG_Cabinet_Details_Cont_Right', 'DI_NAMUR_proximity_Switches_Adapter_UMC'))
        Product.ParseString('<CTX( Container({}).Row(1).Column({}).Set(No) )>'.format('SM_CG_Cabinet_Details_Cont_Right', 'DI_NAMUR_proximity_Switches_Adapter_UMC'))
get_cont_2 = Product.GetContainerByName('SM_CG_Common_Questions_Cont').Rows
for row in get_cont_2:
    if row['SM_Switch_Safety_IO'] =='Control Network Module (CNM)':
        Product.ParseString('<CTX( Container({}).Column({}).SetPermission(Editable) )>'.format('SM_CG_Common_Questions_Cont', 'SM_CNM_Switch_Network_IOTA'))
    elif row['SM_Universal_IOTA'] =='RUSIO':
        Product.ParseString('<CTX( Container({}).Column({}).SetPermission(Editable) )>'.format('SM_CG_Cabinet_Details_Cont_Right', 'SDO_2_24Vdc1A_UIO_Unit_Load_501mA_1000mA'))
        Product.ParseString('<CTX( Container({}).Column({}).SetPermission(Editable) )>'.format('SM_CG_Cabinet_Details_Cont_Right', 'SDO_4_24Vdc2A_UIO_Unit_Load_1001mA_2000mA'))
        Product.ParseString('<CTX( Container({}).Column({}).SetPermission(Editable) )>'.format('SM_CG_Cabinet_Details_Cont_Right', 'Shutdown_Input_UIO_Redundant'))
        Product.ParseString('<CTX( Container({}).Column({}).SetPermission(Editable) )>'.format('SM_CG_Cabinet_Details_Cont_Right', 'Shutdown_Inpu_UIO')) 
        Product.ParseString('<CTX( Container({}).Column({}).SetPermission(Editable) )>'.format('SM_CG_Cabinet_Details_Cont_Right', 'Shutdown_Input_DIO_Redundant'))
        Product.ParseString('<CTX( Container({}).Column({}).SetPermission(Editable) )>'.format('SM_CG_Cabinet_Details_Cont_Right', 'Shutdown_Input_DIO'))       
    else:
        Product.ParseString('<CTX( Container({}).Column({}).SetPermission(Hidden) )>'.format('SM_CG_Common_Questions_Cont', 'SM_CNM_Switch_Network_IOTA'))
        Product.ParseString('<CTX( Container({}).Column({}).SetPermission(Hidden) )>'.format('SM_CG_Cabinet_Details_Cont_Right', 'SDO_2_24Vdc1A_UIO_Unit_Load_501mA_1000mA'))
        Product.ParseString('<CTX( Container({}).Column({}).SetPermission(Hidden) )>'.format('SM_CG_Cabinet_Details_Cont_Right', 'SDO_4_24Vdc2A_UIO_Unit_Load_1001mA_2000mA'))
        Product.ParseString('<CTX( Container({}).Column({}).SetPermission(Hidden) )>'.format('SM_CG_Cabinet_Details_Cont_Right', 'Shutdown_Input_UIO_Redundant'))
        Product.ParseString('<CTX( Container({}).Column({}).SetPermission(Hidden) )>'.format('SM_CG_Cabinet_Details_Cont_Right', 'Shutdown_Inpu_UIO'))       
        Product.ParseString('<CTX( Container({}).Column({}).SetPermission(Hidden) )>'.format('SM_CG_Cabinet_Details_Cont_Right', 'Shutdown_Input_DIO_Redundant'))
        Product.ParseString('<CTX( Container({}).Column({}).SetPermission(Hidden) )>'.format('SM_CG_Cabinet_Details_Cont_Right', 'Shutdown_Input_DIO'))