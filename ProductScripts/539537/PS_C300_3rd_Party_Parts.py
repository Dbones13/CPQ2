import System.Decimal as D
import GS_PS_Exp_Ent_BOM as GS_EEB
import GS_Get_Set_AtvQty
from math import ceil
Product.ExecuteRulesOnce = True
family_type=Product.Attr('SerC_CG_IO_Family_Type').GetValue()
IO_Mounting_Solution = Product.Attr('Dummy_CG_IO_Mounting_Solution').GetValue()
#CXCPQ-41510
L21= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','L21')
L61= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','L61')
J31= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','J31')
K31= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','K31')
J41= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','J41')
K41= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','K41')
J51= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','K51')
K51= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','K51')
J71= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','J71')
K71= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','K71')
J81= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','J81')
K81= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','K81')
J91= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','J91')
K91= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','K91')
O11= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','O11')
M21= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','M21')
N21= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','N21')
M31= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','M31')
N31= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','N31')
O41= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','O41')
O71= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','O71')
O81= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','O81')
R21= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','R21')
M51= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','M51')
N51= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','N51')
M61= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','M61')
N61= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','N61')
M91= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','M91')
N91= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','N91')
P11= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','P11')
Q11= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','Q11')
P31= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','P31')
Q31= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','Q31')
Trace.Write("family_type"+str (family_type))
Universal1=Product.Attr('SerC_CG_Universal_Marshalling_Cabinet').GetValue()
Trace.Write("Universal1"+str (Universal1))
if family_type == 'Series C' and Universal1== 'No' and IO_Mounting_Solution == "Cabinet":
    MTL4510 = D.Ceiling((O41+O81)/4)
    GS_EEB.setAtvQty(Product,"Series_C_CG_Third_Party_Part_Summary","MTL4510",MTL4510)
    MTL4511 = (O71+R21)
    GS_EEB.setAtvQty(Product,"Series_C_CG_Third_Party_Part_Summary","MTL4511",MTL4511)
    MTL4516 = D.Ceiling((M51+N51+M91+N91)/2)
    GS_EEB.setAtvQty(Product,"Series_C_CG_Third_Party_Part_Summary","MTL4516",MTL4516)
    MTL4517 = D.Ceiling((M61+N61+P11+Q11)/2)
    GS_EEB.setAtvQty(Product,"Series_C_CG_Third_Party_Part_Summary","MTL4517",MTL4517)
    MTL4521 = (P31+Q31)
    GS_EEB.setAtvQty(Product,"Series_C_CG_Third_Party_Part_Summary","MTL4521",MTL4521)
    MTL4541 = (J31+K31+J71+K71)
    GS_EEB.setAtvQty(Product,"Series_C_CG_Third_Party_Part_Summary","MTL4541",MTL4541)
    MTL4544 = D.Ceiling((L21+J41+K41+L61+J81+K81)/2)
    GS_EEB.setAtvQty(Product,"Series_C_CG_Third_Party_Part_Summary","MTL4544",MTL4544)
    MTL4546C = (M21+N21)
    GS_EEB.setAtvQty(Product,"Series_C_CG_Third_Party_Part_Summary","MTL4546C",MTL4546C)
    MTL4549C = D.Ceiling((O11+M31+N31)/2)
    GS_EEB.setAtvQty(Product,"Series_C_CG_Third_Party_Part_Summary","MTL4549C",MTL4549C)
    MTL4575 = (J51+K51+J91+K91)
    GS_EEB.setAtvQty(Product,"Series_C_CG_Third_Party_Part_Summary","MTL4575",MTL4575)
#CXCPQ-50473
elif family_type == 'Turbomachinery':
    MTL4510 = D.Ceiling((O41+O81)/4)
    GS_EEB.setAtvQty(Product,"Series_C_CG_Third_Party_Part_Summary","MTL4510",MTL4510)
    MTL4511 = (O71+R21)
    GS_EEB.setAtvQty(Product,"Series_C_CG_Third_Party_Part_Summary","MTL4511",MTL4511)
    MTL4516 = D.Ceiling((M51+N51+M91+N91)/2)
    GS_EEB.setAtvQty(Product,"Series_C_CG_Third_Party_Part_Summary","MTL4516",MTL4516)
    MTL4517 = D.Ceiling((M61+N61+P11+Q11)/2)
    GS_EEB.setAtvQty(Product,"Series_C_CG_Third_Party_Part_Summary","MTL4517",MTL4517)
    MTL4521 = (P31+Q31)
    GS_EEB.setAtvQty(Product,"Series_C_CG_Third_Party_Part_Summary","MTL4521",MTL4521)
    MTL4541 = (J31+K31+J71+K71)
    GS_EEB.setAtvQty(Product,"Series_C_CG_Third_Party_Part_Summary","MTL4541",MTL4541)
    MTL4544 = D.Ceiling((L21+J41+K41+L61+J81+K81)/2)
    GS_EEB.setAtvQty(Product,"Series_C_CG_Third_Party_Part_Summary","MTL4544",MTL4544)
    MTL4546C = (M21+N21)
    GS_EEB.setAtvQty(Product,"Series_C_CG_Third_Party_Part_Summary","MTL4546C",MTL4546C)
    MTL4549C = D.Ceiling((O11+M31+N31)/2)
    GS_EEB.setAtvQty(Product,"Series_C_CG_Third_Party_Part_Summary","MTL4549C",MTL4549C)
    MTL4575 = (J51+K51+J91+K91)
    GS_EEB.setAtvQty(Product,"Series_C_CG_Third_Party_Part_Summary","MTL4575",MTL4575)
else:
    GS_EEB.setAtvQty(Product,"Series_C_CG_Third_Party_Part_Summary","MTL4510",0)
    GS_EEB.setAtvQty(Product,"Series_C_CG_Third_Party_Part_Summary","MTL4511",0)
    GS_EEB.setAtvQty(Product,"Series_C_CG_Third_Party_Part_Summary","MTL4516",0)
    GS_EEB.setAtvQty(Product,"Series_C_CG_Third_Party_Part_Summary","MTL4517",0)
    GS_EEB.setAtvQty(Product,"Series_C_CG_Third_Party_Part_Summary","MTL4521",0)
    GS_EEB.setAtvQty(Product,"Series_C_CG_Third_Party_Part_Summary","MTL4541",0)
    GS_EEB.setAtvQty(Product,"Series_C_CG_Third_Party_Part_Summary","MTL4544",0)
    GS_EEB.setAtvQty(Product,"Series_C_CG_Third_Party_Part_Summary","MTL4546C",0)
    GS_EEB.setAtvQty(Product,"Series_C_CG_Third_Party_Part_Summary","MTL4549C",0)
    GS_EEB.setAtvQty(Product,"Series_C_CG_Third_Party_Part_Summary","MTL4575",0)

Product.ApplyRules()
#Product.ExecuteRulesOnce = False