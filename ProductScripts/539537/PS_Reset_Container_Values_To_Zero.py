import GS_C300_IO_Calc
Universal_Marshalling_Cabinet = Product.Attr('SerC_CG_Universal_Marshalling_Cabinet').GetValue()
IO_Family_Type = Product.Attr('SerC_CG_IO_Family_Type').GetValue()
IO_Mounting_Solution = Product.Attr('Dummy_CG_IO_Mounting_Solution').GetValue()
if (IO_Family_Type == 'Series C' and (Universal_Marshalling_Cabinet != 'No' or IO_Mounting_Solution != "Cabinet")) or  IO_Family_Type == 'Series-C Mark II':
    paramDict2 = {'L21':0,'J31':0,'K31':0,'J41':0,'K41':0,'J51':0,'K51':0,'L61':0,'J71':0,'K71':0,'J81':0,'K81':0,'J91':0,'K91':0, 'O11':0, 'M21':0, 'N21':0, 'M31':0, 'N31':0, 'O41':0, 'M51':0, 'N51':0, 'M61':0, 'N61':0, 'O71':0, 'O81':0, 'M91':0, 'N91':0, 'P11':0, 'Q11':0, 'R21':0, 'P31':0, 'Q31':0}
    #Reset all GIIS IO paramters to 0
    GS_C300_IO_Calc.setIOCount(Product, 'SerC_IO_Params', paramDict2)