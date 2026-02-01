import GS_C300_IO_Calc
Universal_Marshalling_Cabinet = Product.Attr('SerC_CG_Universal_Marshalling_Cabinet').GetValue()
IO_Family_Type = Product.Attr('SerC_CG_IO_Family_Type').GetValue()
if Universal_Marshalling_Cabinet != 'No' and IO_Family_Type != 'Turbomachinery':
    #CXCPQ-40833, CXCPQ-40887
    paramDict2 = {'L21':0,'J31':0,'K31':0,'J41':0,'K41':0,'J51':0,'K51':0,'L61':0,'J71':0,'K71':0,'J81':0,'K81':0,'J91':0,'K91':0, 'O11':0, 'M21':0, 'N21':0, 'M31':0, 'N31':0, 'O41':0, 'M51':0, 'N51':0, 'M61':0, 'N61':0, 'O71':0, 'O81':0, 'M91':0, 'N91':0, 'P11':0, 'Q11':0, 'R21':0, 'P31':0, 'Q31':0}
    #Reset all GIIS IO paramters to 0
    #GS_C300_IO_Calc.setIOCount(Product, 'SerC_IO_Params', paramDict2)
    parts_dict = GS_C300_IO_Calc.getParts40833(Product, {})
    parts_dict = GS_C300_IO_Calc.getParts40872(Product, parts_dict)
    parts_dict = GS_C300_IO_Calc.getParts40887(Product, parts_dict)
    parts_dict = GS_C300_IO_Calc.getParts41229(Product, parts_dict)
    GS_C300_IO_Calc.setIOCount(Product, 'Series_C_CG_Part_Summary', parts_dict)
    ScriptExecutor.Execute('PS_Series_C_CG_Part_Summary_Cont_update_parts')
    Product.GetContainerByName('Series_C_CG_Part_Summary_Cont').Calculate()
else:
    isR2Qquote = True if Quote.GetCustomField("R2QFlag").Content else False
    Disallow_attrs = [
    "ATTCON_01_close",''
    "ATTCON_01_open",
    "Header_01_close",
    "Header_01_open",
    "SerC_Cabinet_Power",
    "SerC_CG_AC_Input_Voltage",
    "SerC_CG_Cabinet_Fan",
    "SerC_CG_Cabinet_Light_(LED)",
    "SerC_CG_Cabinet_Thermostat",
    "SerC_CG_Cabinet_Type",
    "SerC_CG_label_Universal_Marshalling_Cabinet",
    "SerC_CG_Mounting_Option",
    "SerC_CG_Percentage_of_Spare_Space_required(0-100%)",
    "SerC_CG_Power_Supply_Vendor",
    "SerC_CG_SIC_Length_for_UMC",
    "SerC_CG_Termination_of_Spare_Wires_in_Field_Cabin",
    "SerC_CG_Universal_Marshaling_Cabinet_layout",
    "SerC_CG_Utility_Socket_(230/115 VAC)",
    "SerC_CG_Wiring_and_Ducts",
    "SerC_CG_GIIS_Analog_Inputs_Isolator_2Wire_Type",
    "SerC_CG_Is_NAMUR_isolator_type_Required", 'SerC_CG_Ethernet_Interface', 'SerC_CG_Integrated_Marshalling_Cabinet','SerC_CG_IP_Rating']
    for attr in Disallow_attrs:
        if isR2Qquote and attr  in  ['SerC_CG_Ethernet_Interface']:
            continue
        Product.DisallowAttr(attr)