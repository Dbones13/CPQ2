attrList = ['CWS_Mig_Hi_level_Analog_Input_Modules_16_point', 'CWS_Mig_Analog_Input_Modules_8_point', 'CWS_Mig_Analog_Output_Modules_4_point', 'CWS_Mig_Digital_Input_Contact_type_Modules_16_point', 'CWS_Mig_Digital_Input_24VDC_Modules_32_point', 'CWS_Mig_Digital_Input_24VDC_Modules_16_point', 'CWS_Mig_Digital_Input_120_240_VAC_Modules_16_point', 'CWS_Mig_Pulse_Frequency_Quadrature_Input_Modules_4_point', 'CWS_Mig_Digital_Output_120_240_VAC_Modules_8_point', 'CWS_Mig_Digital_Output_24VDC_Modules_16_point', 'CWS_Mig_Digital_Output_24VDC_Modules_32_point', 'CWS_Mig_Digital_Output_Relays_Modules_8_point', 'CWS_Mig_Total_number_of_HC900_IO_points']
for attrName in attrList:
    if Product.Attr(attrName).GetValue() == '':
        Product.Attr(attrName).AssignValue('0')

if Product.Attr('CWS_Mig_System_Chassis_with_C50_Controller').GetValue() == '':
    Product.Attr('CWS_Mig_System_Chassis_with_C50_Controller').AssignValue('1')