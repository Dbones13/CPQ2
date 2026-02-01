profibus_attr = ["Header_07_open","SerC_Number_of_Profibus_DP_Slave_devices - Non_Red","SerC_Number_of_Profibus_DP_Slave_devices - Red","SerC_Number_of_Devices_per_Profibus_Network (0-32)","Header_07_close"]
if Product.Attr('SerC_GC_Profibus_Gateway_Interface').GetValue() == "Yes":
	Product.Attr('SerC_Number_of_Profibus_DP_Slave_devices - Non_Red').AssignValue('0')
	Product.Attr('SerC_Number_of_Profibus_DP_Slave_devices - Red').AssignValue('0')
	Product.Attr('SerC_Number_of_Devices_per_Profibus_Network (0-32)').AssignValue('1')
	for attr in profibus_attr:
		Product.AllowAttr(attr)
else:
    for attr in profibus_attr:
		Product.DisallowAttr(attr)