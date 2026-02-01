QCS_Standard=Product.Attr("CWS_Mig_Will_customer_provide_HW_for_QCS_Standard").GetValue()

#if QCS_Standard ==None or QCS_Standard =="":
#    Product.Attr('CWS_Mig_Will_customer_provide_HW_for_QCS_Standard').SelectDisplayValue('No')
C50_controller=Product.Attr("CWS_Mig_System_Chassis_with_C50_Controller").GetValue()
CWS_Mig_Analog_Input_Modules_8_point=Product.Attr("CWS_Mig_Analog_Input_Modules_8_point").GetValue()
CWS_Mig_Analog_Output_Modules_4_point=Product.Attr("CWS_Mig_Analog_Output_Modules_4_point").GetValue()
CWS_Mig_Digital_Input_Contact_type_Modules_16_point=Product.Attr("CWS_Mig_Digital_Input_Contact_type_Modules_16_point").GetValue()
CWS_Mig_Digital_Input_24VDC_Modules_16_point=Product.Attr("CWS_Mig_Digital_Input_24VDC_Modules_16_point").GetValue()
CWS_Mig_Digital_Input_120_240_VAC_Modules_16_point=Product.Attr("CWS_Mig_Digital_Input_120_240_VAC_Modules_16_point").GetValue()
CWS_Mig_Digital_Output_Relays_Modules_8_point=Product.Attr("CWS_Mig_Digital_Output_Relays_Modules_8_point").GetValue()
CWS_Mig_Digital_Output_24VDC_Modules_16_point=Product.Attr("CWS_Mig_Digital_Output_24VDC_Modules_16_point").GetValue()
CWS_Mig_Digital_Output_120_240_VAC_Modules_8_point=Product.Attr("CWS_Mig_Digital_Output_120_240_VAC_Modules_8_point").GetValue()
CWS_Mig_Digital_Output_24VDC_Modules_32_point=Product.Attr("CWS_Mig_Digital_Output_24VDC_Modules_32_point").GetValue()
CWS_Mig_Digital_Input_24VDC_Modules_32_point=Product.Attr("CWS_Mig_Digital_Input_24VDC_Modules_32_point").GetValue()
CWS_Mig_Hi_level_Analog_Input_Modules_16_point=Product.Attr("CWS_Mig_Hi_level_Analog_Input_Modules_16_point").GetValue()
CWS_Mig_Pulse_Frequency_Quadrature_Input_Modules_4_point=Product.Attr("CWS_Mig_Pulse_Frequency_Quadrature_Input_Modules_4_point").GetValue()


if C50_controller =="":
	Product.Attr('CWS_Mig_System_Chassis_with_C50_Controller').AssignValue('0')
if CWS_Mig_Analog_Input_Modules_8_point =="":
	Product.Attr('CWS_Mig_Analog_Input_Modules_8_point').AssignValue('0')
if CWS_Mig_Analog_Output_Modules_4_point =="":
	Product.Attr('CWS_Mig_Analog_Output_Modules_4_point').AssignValue('0')
if CWS_Mig_Digital_Input_Contact_type_Modules_16_point =="":
	Product.Attr('CWS_Mig_Digital_Input_Contact_type_Modules_16_point').AssignValue('0')
if CWS_Mig_Digital_Input_24VDC_Modules_16_point =="":
	Product.Attr('CWS_Mig_Digital_Input_24VDC_Modules_16_point').AssignValue('0')
if CWS_Mig_Digital_Input_120_240_VAC_Modules_16_point =="":
	Product.Attr('CWS_Mig_Digital_Input_120_240_VAC_Modules_16_point').AssignValue('0')
if CWS_Mig_Digital_Output_Relays_Modules_8_point =="":
	Product.Attr('CWS_Mig_Digital_Output_Relays_Modules_8_point').AssignValue('0')
if CWS_Mig_Digital_Output_24VDC_Modules_16_point =="":
	Product.Attr('CWS_Mig_Digital_Output_24VDC_Modules_16_point').AssignValue('0')
if CWS_Mig_Digital_Output_120_240_VAC_Modules_8_point =="":
	Product.Attr('CWS_Mig_Digital_Output_120_240_VAC_Modules_8_point').AssignValue('0')
if CWS_Mig_Digital_Output_24VDC_Modules_32_point =="":
	Product.Attr('CWS_Mig_Digital_Output_24VDC_Modules_32_point').AssignValue('0')
if CWS_Mig_Digital_Input_24VDC_Modules_32_point =="":
	Product.Attr('CWS_Mig_Digital_Input_24VDC_Modules_32_point').AssignValue('0')
if CWS_Mig_Hi_level_Analog_Input_Modules_16_point =="":
	Product.Attr('CWS_Mig_Hi_level_Analog_Input_Modules_16_point').AssignValue('0')
if CWS_Mig_Pulse_Frequency_Quadrature_Input_Modules_4_point =="":
	Product.Attr('CWS_Mig_Pulse_Frequency_Quadrature_Input_Modules_4_point').AssignValue('0')