"""import GS_C300_IO_Calc
IO_Mounting_Solution = Product.Attr('SerC_IO_Mounting_Solution').GetValue()
IO_Family_Type = Product.Attr('SerC_CG_IO_Family_Type').GetValue()
if IO_Mounting_Solution != 'Cabinet' and IO_Family_Type == 'Series C':
    #CXCPQ-40833
    paramDict2 = {'L21':0,'J31':0,'K31':0,'J41':0,'K41':0,'J51':0,'K51':0,'L61':0,'J71':0,'K71':0,'J81':0,'K81':0,'J91':0,'K91':0, 'O11':0, 'M21':0, 'N21':0, 'M31':0, 'N31':0}
    #Reset all GIIS IO paramters to 0
    ##GS_C300_IO_Calc.setIOCount(Product, 'SerC_IO_Params', paramDict2)
    parts_dict = GS_C300_IO_Calc.getParts40833(Product, {})
    parts_dict = GS_C300_IO_Calc.getParts40872(Product, parts_dict)
    GS_C300_IO_Calc.setIOCount(Product, 'Series_C_RG_Part_Summary', parts_dict)
    ScriptExecutor.Execute('PS_Series_C_RG_Part_Summary_Cont_update_parts')
    Product.GetContainerByName('Series_C_RG_Part_Summary_Cont').Calculate()"""
import GS_Get_Set_AtvQty
IO_Mounting_Solution = Product.Attr('SerC_IO_Mounting_Solution').GetValue()
IO_Family_Type = Product.Attr('SerC_CG_IO_Family_Type').GetValue()
if IO_Family_Type == 'Series C':
    if IO_Mounting_Solution in ['Universal Process Cab - 1.3M', 'Cabinet']:
        GS_Get_Set_AtvQty.resetAllAtvQty(Product, 'SerC_IO_Params')
        GS_Get_Set_AtvQty.resetAllAtvQty(Product, 'Series_C_RG_Part_Summary')
        Product.ApplyRules()