ethernet_attr = ["SerC_Number_of_Rockwell_ControlLogix_Processors","SerC_Number of Rockwell Control Processors(NON)","SerC_Number of Process Connected I/O Devices 1","SerC_Number of Motor Starter IOMs per EIM 255","SerC_NO of Rock Ctrl Processors Redundant0-999NEW","SerC_Numbe of Rockwelix Proc EIM Redundant 0-10","SerC_Nu of Proc Conn I/O Devi (Redundant ) (0-999)","SerC_Number of Motor Start IOMs per EIM Redun 255","SerC_Number of Non Redundant EIM for IEC61850","SerC_Number of Redundant EIM for IEC61850","SerC_Number of Non Redund EIM for Profinet Devices","SerC_Number of Redundant EIM for Profinet Devices","SerC_Number of Non Redundant EIM for EIP Device","SerC_Number of Redunt EIM for EIP Devices (0-300)","SerC_Number_NonRedundant_EIM_for_Modbus","SerC_Number_Redundant_EIM_for_Modbus"]
if Product.Attr("SerC_CG_Ethernet_Interface").GetValue() == 'Yes':
    for attr in ethernet_attr:
        Product.AllowAttr(attr)
        Product.Attr(attr).AssignValue('0')
    Product.AllowAttr("Header_08_close")
    Product.AllowAttr("Header_08_open")
else:
    for attr in ethernet_attr:
        Product.DisallowAttr(attr)
    Product.DisallowAttr("Header_08_close")
    Product.DisallowAttr("Header_08_open")