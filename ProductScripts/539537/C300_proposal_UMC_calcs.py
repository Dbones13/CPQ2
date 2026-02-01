#import GS_C300_AMP_A_Calcs,GS_Get_Set_AtvQty
#import GS_C300_MCAR_calcs
#import GS_C300_markII_umc_calcs,GS_C300_USCA_intermediate_Calcs
import GS_SerC_parts
hn = hn2 = qty1 = qty2 = GS_SerC_parts.getPmioCgIota(Product)
Product.Attr("CG_PMIO_HN").AssignValue(str(hn))
rg_count=Product.GetContainerByName('Series_C_Remote_Groups_Cont')
doc96sum=doc32sum=doc64sum=0
CurrentTab=Product.Tabs.GetByName('Part Summary').IsSelected
if CurrentTab==True:
    Product.Attr('CurrentTab_Is_partsummery').AssignValue('Part Summary')
    Trace.Write("correct")
else:
    Product.Attr('CurrentTab_Is_partsummery').AssignValue('OtherTab')
    Trace.Write("Notcorrect")
if rg_count.Rows.Count >0:
    for row in rg_count.Rows:
        if row.GetColumnByName("C300_RG_UPC_Universal_IO_Count").Value =="9":
            doc96sum +=int(row.GetColumnByName("C300_RG_UPC_Cab_Count").Value)
        elif row.GetColumnByName("C300_RG_UPC_Universal_IO_Count").Value =="6":
            doc64sum +=int(row.GetColumnByName("C300_RG_UPC_Cab_Count").Value)
        elif row.GetColumnByName("C300_RG_UPC_Universal_IO_Count").Value =="3":
            doc32sum +=int(row.GetColumnByName("C300_RG_UPC_Cab_Count").Value)
Product.Attr('Doc_Umc_total_32').AssignValue(str(doc32sum))
Product.Attr('Doc_Umc_total_64').AssignValue(str(doc64sum))
Product.Attr('Doc_Umc_total_96').AssignValue(str(doc96sum))
Product.Attr('Dummy_RG_IO_Mounting_Solution').AssignValue(str(int(doc96sum)+int(doc64sum)+int(doc32sum)))
#below section only for displaying msg as request for testing.after testing need to remove.
'''Sum_IsM,Sum_Is1M,Sum_NIsM,Sum_NIs1M=GS_C300_markII_umc_calcs.USCA_Calcs1(Product)
Sum_Is,Sum_NIs,Sum_Is1,Sum_NIs1=GS_C300_USCA_intermediate_Calcs.USCA_Calcs(Product)
"""Product.Messages.Add("mark 2 NIs is {}".format(Sum_NIs1M))
Product.Messages.Add("mark 2 Is is {}".format(Sum_Is1M))
Product.Messages.Add("series c Is is {}".format(Sum_Is1))
Product.Messages.Add("series c NIs is {}".format(Sum_NIs1))"""
AmP_A=GS_C300_AMP_A_Calcs.AMP_A(Product)
Trace.Write("AmP_A "+str(AmP_A))
#Product.Messages.Add("Total Amp A is {}".format(AmP_A))
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
#Product.Messages.Add("Mcar Componant (Family_Series-C as per senario 1-3 form overall calculation sheet) C = {}, D = {}".format(CC, DD))'''