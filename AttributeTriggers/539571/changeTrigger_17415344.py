import GS_C300_IO_Calc
Universal_Marshalling_Cabinet = Product.Attr('Ser_RG_Universal_Marshalling_Cabinet').GetValue()
IO_Family_Type = Product.Attr('SerC_CG_IO_Family_Type').GetValue()
if Universal_Marshalling_Cabinet != 'No' and IO_Family_Type != 'Turbomachinery':
    #CXCPQ-40833 , CXCPQ-41229
    paramDict2 = {'L21':0,'J31':0,'K31':0,'J41':0,'K41':0,'J51':0,'K51':0,'L61':0,'J71':0,'K71':0,'J81':0,'K81':0,'J91':0,'K91':0, 'O11':0, 'M21':0, 'N21':0, 'M31':0, 'N31':0, 'P31':0, 'Q31':0, 'O41':0, 'O71':0, 'O81':0, 'R21':0, 'M51':0, 'N51':0, 'M61':0, 'N61':0, 'M91':0, 'N91':0, 'P11':0, 'Q11':0, 'P31':0, 'Q31':0, 'V13':0, 'V21':0, 'V22':0, 'V31':0, 'V32':0, 'V43':0, 'V53':0, 'V61':0, 'V62':0, 'V71':0, 'V72':0, 'V83':0}
    #Reset all GIIS IO paramters to 0
    #GS_C300_IO_Calc.setIOCount(Product, 'SerC_IO_Params', paramDict2)
    parts_dict = GS_C300_IO_Calc.getParts40833(Product, {})
    parts_dict = GS_C300_IO_Calc.getParts40872(Product, parts_dict)
    parts_dict = GS_C300_IO_Calc.getParts41229(Product, parts_dict)
    GS_C300_IO_Calc.setIOCount(Product, 'Series_C_RG_Part_Summary', parts_dict)
    ScriptExecutor.Execute('PS_Series_C_RG_Part_Summary_Cont_update_parts')
    Product.GetContainerByName('Series_C_RG_Part_Summary_Cont').Calculate()