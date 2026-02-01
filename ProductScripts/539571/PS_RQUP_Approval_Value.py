import re
import GS_C300_AMP_A_Calcs,GS_Get_Set_AtvQty
import GS_C300_markII_umc_calcs,GS_C300_USCA_intermediate_Calcs
import GS_C300_MCAR_calcs
C,GI=GS_C300_MCAR_calcs.MCARW1(Product)
SUM_HI,SUM_LO,SUM_HI1,SUM_LO1,SUM_HI11,SUM_LO11,SUM_D,HI,LO,LL=GS_C300_MCAR_calcs.mcar_cals(Product)
#msg section need to remove after testing
#below section only for displaying msg as request for testing.after testing need to remove.
A= int(GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','A_for_C'))
B= int(GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','B_for_C'))
C= int(GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','C_for_C'))
D= int(GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','D_for_C'))
E= int(GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','E_for_C'))
F= int(GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','F_for_C'))
G= int(GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','G_for_C'))
H= int(GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','H_for_C'))
CC= int(C)
DD=int(SUM_D)
#Product.Messages.Add("Mcar Componant (Family_Series-C) A = {}, B = {}, As per senario-4 C is = {}, As per senario-4 D is = {}, E = {}, F = {}, G = {}, H = {}".format(A, B, C, D, E, F, G, H))
#Product.Messages.Add("Mcar Componant (Family_Series-C as per senario 1-3 form overall calculation sheet) C = {}, D = {}".format(CC, DD))
#end section
Sum_IsM,Sum_Is1M,Sum_NIsM,Sum_NIs1M=GS_C300_markII_umc_calcs.USCA_Calcs1(Product)
Sum_Is,Sum_NIs,Sum_Is1,Sum_NIs1,Sum_HV=GS_C300_USCA_intermediate_Calcs.USCA_Calcs(Product)
"""Product.Messages.Add("mark 2 NIs is {}".format(Sum_NIs1M))
Product.Messages.Add("mark 2 Is is {}".format(Sum_Is1M))
Product.Messages.Add("series c Is is {}".format(Sum_Is1))
Product.Messages.Add("series c NIs is {}".format(Sum_NIs1))"""
##end of msg section
Power_System_Type = Product.Attr('SerC_RG_Power_System_Type').GetValue()
#Power_System_Type = Product.Attr('SerC_CG_Power_System_Type').SelectValue('Locally Supplied Power')
Trace.Write(Power_System_Type)
RQUP_Approval_Value = Product.Attr('SerC_RG_RQUP_ApprovalValue_for_Locally_Supp_Power').GetValue()
Trace.Write("RQUP_Approval_Value= "+str(RQUP_Approval_Value))
list1=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
#list2=["K","L","M","N","O","P","Q","R","S","T"]
#list3=["U","V","W","X","Y","Z"]
#list4=["0","1","2","3","4","5","6","7","8","9"]
if Power_System_Type =='Locally Supplied Power' and (len(str(RQUP_Approval_Value)) >0 and len(str(RQUP_Approval_Value))<17):
    Trace.Write(RQUP_Approval_Value)
    for i in RQUP_Approval_Value:
        if i not in list1:
            #Trace.Write()
            Product.ResetAttr('SerC_RG_RQUP_ApprovalValue_for_Locally_Supp_Power')
elif Power_System_Type =='Locally Supplied Power' and (len(str(RQUP_Approval_Value)) <1 or len(str(RQUP_Approval_Value))>16):
    Product.ResetAttr('SerC_RG_RQUP_ApprovalValue_for_Locally_Supp_Power')
#AmP_A=GS_C300_AMP_A_Calcs.AMP_A(Product)
#Trace.Write("AmP_A "+str(AmP_A))
#Product.Messages.Add("Total Amp A is {}".format(AmP_A))