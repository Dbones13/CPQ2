elcn_Voltage= Product.Attr("ELCN_Power_Supply_Voltage").GetValue()
fiber_optic_switch= Product.Attr("ELCN_Select_type_of_fiber_optic_switch").GetValue()
Att_No_ngs= Product.Attr("ATT_ELCN_Qty_of_NGs_more_than_100mts").GetValue()
if elcn_Voltage == "":
    Product.Attr('ELCN_Power_Supply_Voltage').SelectDisplayValue('120V, 60 Hz')
if fiber_optic_switch =="":
    Product.Attr('ELCN_Select_type_of_fiber_optic_switch').SelectDisplayValue('Moxa (SM-G512I2)')
if Att_No_ngs=="":
    Product.Attr('ATT_ELCN_Qty_of_NGs_more_than_100mts').AssignValue('1')