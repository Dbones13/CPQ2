import ProductUtil as pu
error_msgs = []

idModForSMSC = ''
if Product.GetContainerByName("SM_RG_Universal_Safety_Cabinet_1.3M_Cont").Rows.Count > 0:
    idModForSMSC = Product.GetContainerByName("SM_RG_Universal_Safety_Cabinet_1.3M_Cont").Rows[0].GetColumnByName("Specify_Identifier_Modifier_for_SM_SC_Universal_Safety_Cabinet").DisplayValue

if idModForSMSC=="Yes":
    code=str(Product.GetContainerByName("SM_RG_Universal_Safety_Cabinet_1.3M_Cont").Rows[0].GetColumnByName("Identifier_Modifier_for_SM_SC_Universal_Safety_Cabinet").Value)
    if len(code) >= 23:

        if code[3] == "S":
            if code[17] == "2":
                error_msgs.append('When S300 is installed the CNM options are limited to either none or 4. If Number of Control Network Module is selected, 4 CNMs would be required to support FTE A, FTE B and Safety IO link connections.')
                pu.addMessage(Product , 'When S300 is installed the CNM options are limited to either none or 4. If Number of Control Network Module is selected, 4 CNMs would be required to support FTE A, FTE B and Safety IO link connections.')

        if code[3] == "X":
            if code[17] == "4":
                error_msgs.append('When no S300 is installed the CNM options are limited to either none or 2. If CNM is selected, 2 CNMs would be required to support Safety IO link connections.')
                pu.addMessage(Product , 'When no S300 is installed the CNM options are limited to either none or 2. If CNM is selected, 2 CNMs would be required to support Safety IO link connections.')
        
        if code[3] == "S" and (code[15] == "Y" or code[15] == "V"):
            error_msgs.append('Terminal block is not supported for S300 controller')
            pu.addMessage(Product , 'Terminal block is not supported for S300 controller')

        if (code[10] == "Q" or code[10] == "D") and code[15] == "V":
            error_msgs.append('External TB with 6A fuse is not supported with Phoenix Quint power supply (20A AC/DC QUINT4+ PS and 24 VDC/DC QUINT4+ Supply)')
            pu.addMessage(Product , 'External TB with 6A fuse is not supported with Phoenix Quint power supply (20A AC/DC QUINT4+ PS and 24 VDC/DC QUINT4+ Supply)')
        
        if (code[17] == "2" or code[17] == "4") and (code[3] == "X") and (code[8] == "C" or code[9] == "C"):
            if code[15] == "Y" or code[15] == "V":
                error_msgs.append('When CNM is installed and 96pts IO are used, the CNM is installed on the comm backplate and Option 16 can’t be installed in their usual location.')
                pu.addMessage(Product , 'When CNM is installed and 96pts IO are used, the CNM is installed on the comm backplate and Option 16 can’t be installed in their usual location.')

        if (code[3] == "S") and (code[8] == "B" or code[8] == "C") and (code[5] == "M"):
            if code[14] == "Y":
                error_msgs.append('When USC has the S300, UIO > 32pts and the default marshaling FC-TUIO51/52 installed there is no space left for the STT650.')
                pu.addMessage(Product , 'When USC has the S300, UIO > 32pts and the default marshaling FC-TUIO51/52 installed there is no space left for the STT650.')

        if code[17] == "4" and code[3] == "S":
            if (code[8] == "C") or (code[9] == "C"):
                error_msgs.append('when CNM and S300 are installed the number of IO is restricted to 64pts max')
                pu.addMessage(Product , 'when CNM and S300 are installed the number of IO is restricted to 64pts max')
            elif (code[8] == "A" and code[9] == "B") or (code[8] == "B" and code[9] == "A") or (code[8] == "B" and code[9] == "B"):
                error_msgs.append('when CNM and S300 are installed the number of IO is restricted to 64pts max')
                pu.addMessage(Product , 'when CNM and S300 are installed the number of IO is restricted to 64pts max')


if idModForSMSC=="No":
    if Product.GetContainerByName("SM_SC_Universal_Safety_Cab_1_3M_Details_cont").Rows.Count > 0:
        s300 = Product.GetContainerByName("SM_SC_Universal_Safety_Cab_1_3M_Details_cont").Rows[0].GetColumnByName("S300").DisplayValue
        cnm = Product.GetContainerByName("SM_SC_Universal_Safety_Cab_1_3M_Details_cont").Rows[0].GetColumnByName("Number_of_Control_Network_Module_0-100").Value
        puio = Product.GetContainerByName("SM_SC_Universal_Safety_Cab_1_3M_Details_cont").Rows[0].GetColumnByName("PUIO_Count").DisplayValue
        pdio = Product.GetContainerByName("SM_SC_Universal_Safety_Cab_1_3M_Details_cont").Rows[0].GetColumnByName("PDIO_Count").DisplayValue
        ext_tb = Product.GetContainerByName("SM_SC_Universal_Safety_Cab_1_3M_Details_cont").Rows[0].GetColumnByName("External _24VDC_Terminal_Block").DisplayValue
        fta_puio = Product.GetContainerByName("SM_SC_Universal_Safety_Cab_1_3M_Details_cont").Rows[0].GetColumnByName("Field_Termination_Assembly_for_PUIO").DisplayValue
        temp = Product.GetContainerByName("SM_SC_Universal_Safety_Cab_1_3M_Details_cont").Rows[0].GetColumnByName("Temperature_Monitoring").DisplayValue
        power = Product.GetContainerByName("SM_SC_Universal_Safety_Cab_1_3M_Details_cont").Rows[0].GetColumnByName("Power_Supply_Type").DisplayValue
        
        if s300 != "No S300":
            if cnm == "2":
                error_msgs.append('When S300 is installed the CNM options are limited to either none or 4. If Number of Control Network Module is selected, 4 CNMs would be required to support FTE A, FTE B and Safety IO link connections.')
                pu.addMessage(Product , 'When S300 is installed the CNM options are limited to either none or 4. If Number of Control Network Module is selected, 4 CNMs would be required to support FTE A, FTE B and Safety IO link connections.')
        if s300 == "No S300":
            if cnm == "4":
                error_msgs.append('When no S300 is installed the CNM options are limited to either none or 2. If CNM is selected, 2 CNMs would be required to support Safety IO link connections.')
                pu.addMessage(Product , 'When no S300 is installed the CNM options are limited to either none or 2. If CNM is selected, 2 CNMs would be required to support Safety IO link connections.')
        if s300 == "Redundant S300" and (ext_tb == "External TB 4A or less" or ext_tb == "External TB w/6A Fuse"):
            error_msgs.append('Terminal block is not supported for S300 controller')
            pu.addMessage(Product , 'Terminal block is not supported for S300 controller')
        if (power == "20A AC/DC QUINT 4+ PS" or power == "24 VDC/DC QUINT 4+ Supply") and ext_tb == "External TB w/6A Fuse":
            error_msgs.append('External TB with 6A fuse is not supported with Phoenix Quint power supply (20A AC/DC QUINT4+ PS and24 VDC/DC QUINT4+ Supply')
            pu.addMessage(Product , 'External TB with 6A fuse is not supported with Phoenix Quint power supply (20A AC/DC QUINT4+ PS and24 VDC/DC QUINT4+ Supply')
        if (cnm == "2" or cnm == "4") and (s300 == "No S300") and (puio == "96" or pdio == "96"):
            if ext_tb == "External TB 4A or less" or ext_tb == "External TB w/6A Fuse":
                error_msgs.append('When CNM is installed and 96pts IO are used, the CNM is installed on the comm backplate and Option 16 can’t be installed in their usual location.')
                pu.addMessage(Product , 'When CNM is installed and 96pts IO are used, the CNM is installed on the comm backplate and Option 16 can’t be installed in their usual location.')
        if (s300 != "No S300") and (puio == "64" or puio == "96") and (fta_puio == "Default Marshalling FC-TUIO51/52"):
            if temp == "STT650":
                error_msgs.append('When USC has the S300, UIO > 32pts and the default marshaling FC-TUIO51/52 installed there is no space left for the STT650.')
                pu.addMessage(Product , 'When USC has the S300, UIO > 32pts and the default marshaling FC-TUIO51/52 installed there is no space left for the STT650.')
        if cnm == "4" and s300 != "No S300":
            if (puio == "96") or (pdio == "96"):
                error_msgs.append('when CNM and S300 are installed the number of IO is restricted to 64pts max')
                pu.addMessage(Product , 'when CNM and S300 are installed the number of IO is restricted to 64pts max')
            elif (puio == "32" and pdio == "64") or (puio == "64" and pdio == "32") or (puio == "64" and pdio == "64"):
                error_msgs.append('when CNM and S300 are installed the number of IO is restricted to 64pts max')
                pu.addMessage(Product , 'when CNM and S300 are installed the number of IO is restricted to 64pts max')

error_msg = Product.Attr('ErrorMessage').GetValue()
Trace.Write(error_msg)
for msg in error_msgs:
    if not error_msg:
        error_msg +=msg
    else:
        error_msg += '<br/>' + msg
#Trace.Write('Error Message1: ' +error_msg)
#Trace.Write(error_msg)
Product.Attr('ErrorMessage').AssignValue(error_msg)