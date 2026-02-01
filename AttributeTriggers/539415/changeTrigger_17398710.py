attributes = ( 'QCS_Mig_Analog_Input_Modules_8_point', 'QCS_Mig_Analog_Output_Modules_4_point', 'QCS_Mig_Digital_Input_Contact_type_Modules_16_poin', 'QCS_Mig_Digital_Input_24VDC_Modules_16_point', 'QCS_Mig_Digital_Input_120_240_VAC_Modules_16_point', 'QCS_Mig_Digital_Output_Relays_Modules_8_point', 'QCS_Mig_Digital_Output_24VDC_Modules_16_point', 'QCS_Mig_Digital_Output_120_240_VAC_Modules_8_point', 'QCS_Mig_Digital_Output_24VDC_Modules_32_point', 'QCS_Mig_Digital_Input_24VDC_Modules_32_point', 'QCS_Mig_Hi_level_Analog_Input_Modules_16_point', 'QCS_Mig_Pulse_Frequency_Quadrature_Input_Modules_4', 'QCS_Mig_Number_of_die_bolts','QCS_Mig_Total_number_of_HC_900_IO_points')

for attr in attributes:
    if Product.Attr(attr).GetValue() == '':
        Product.Attr(attr).AssignValue('0')
if Product.Attr('QCS_Mig_System_Chassis_with_C50_Controller_power').GetValue() == '':
    Product.Attr('QCS_Mig_System_Chassis_with_C50_Controller_power').AssignValue('1')