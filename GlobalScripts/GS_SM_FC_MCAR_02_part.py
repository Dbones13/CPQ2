import math as m

def get_fc_mcar_02(Product,IOTANR,IOTAR,FC_TDIO11,TCNT11,parts_dict):
    if Product.Name=="SM Control Group":
        if Product.GetContainerByName('SM_CG_Common_Questions_Cont').Rows[0].GetColumnByName('SM_Universal_IOTA').DisplayValue=="RUSIO":
            fc_mcar_02 = (m.ceil(float(IOTANR)/3)) + (m.ceil(float(IOTAR)/2)) + (m.ceil(float(TCNT11)/2)) + (m.ceil(float(FC_TDIO11)/3))
            fc_mcar_02=m.ceil(fc_mcar_02)
            Trace.Write("fc_mr: "+str(fc_mcar_02))
            parts_dict["FC-MCAR-02"] = {'Quantity' : int(fc_mcar_02) , 'Description': 'SM RIO 36 inch carrier'}
    elif Product.Name=="SM Remote Group":
        iota = Product.Attr("SM_Universal_IOTA_Type").GetValue()
        if iota =="RUSIO":
            fc_mcar_02 = (m.ceil(float(IOTANR)/3)) + (m.ceil(float(IOTAR)/2)) +  (m.ceil(float(FC_TDIO11)/3))
            fc_mcar_02=m.ceil(fc_mcar_02)
            Trace.Write("fc_mr: "+str(fc_mcar_02))
            parts_dict["FC-MCAR-02"] = {'Quantity' : int(fc_mcar_02) , 'Description': 'SM RIO 36 inch carrier'}
    return parts_dict