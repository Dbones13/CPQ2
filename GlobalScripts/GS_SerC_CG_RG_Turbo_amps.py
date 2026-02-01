import GS_Get_Set_AtvQty
import GS_C300_BOM_UIO
import GS_C300_BOM_Rail_IO_Part_calcs
from GS_C300_IO_Calc import getFloat, percentInstalledSpareCalc, divideByX, setIOCount
j=1
def Get_turbo_amps(Product):
    iofam=Product.Attributes.GetByName("SerC_CG_IO_Family_Type").GetValue()
    amps=Product.Attributes.GetByName('SerC_CG_Current_required_for_each_DO').GetValue()
    if amps=="":
        amps=0
    else:
        amps=int(amps)
    import math as m
    cont="Series_C_CG_Part_Summary"
    if Product.Name=="Series-C Remote Group":
        cont="Series_C_RG_Part_Summary"


    #A1	= GS_Get_Set_AtvQty.getAtvQty(Product,cont,"CC-SCMB02")*	0.01 CXDEV-6770
    A1	= GS_Get_Set_AtvQty.getAtvQty(Product,cont,"CC-SCMB02")*	0.271
    A2	= GS_Get_Set_AtvQty.getAtvQty(Product,cont,"CC-PCF901")*	0.15
    A3	= GS_Get_Set_AtvQty.getAtvQty(Product,cont,"CC-PAIH01")*	0.18
    A4	= GS_Get_Set_AtvQty.getAtvQty(Product,cont,"CC-TAIX01")*	0.32
    A5	= GS_Get_Set_AtvQty.getAtvQty(Product,cont,"CC-TAIX11")*	0.32
    A6	= GS_Get_Set_AtvQty.getAtvQty(Product,cont,"CC-PAOH01")*	0.479
    A7	= GS_Get_Set_AtvQty.getAtvQty(Product,cont,"CC-TAOX01")*	0
    A8	= GS_Get_Set_AtvQty.getAtvQty(Product,cont,"CC-TAOX11")*	0
    A9	= GS_Get_Set_AtvQty.getAtvQty(Product,cont,"CC-PDIL01")*	0.095
    A10	= GS_Get_Set_AtvQty.getAtvQty(Product,cont,"CC-TDIL01")*	0.19
    A11	= GS_Get_Set_AtvQty.getAtvQty(Product,cont,"CC-TDIL11")*	0.19
    A12	= GS_Get_Set_AtvQty.getAtvQty(Product,cont,"CC-PDIH01")*	0.05
    A13	= GS_Get_Set_AtvQty.getAtvQty(Product,cont,"CC-TDI110")*	0
    A14	= GS_Get_Set_AtvQty.getAtvQty(Product,cont,"CC-TDI120")*	0
    A15	= GS_Get_Set_AtvQty.getAtvQty(Product,cont,"CC-TDI220")*	0
    A16	= GS_Get_Set_AtvQty.getAtvQty(Product,cont,"CC-TDI230")*	0
    A17	= GS_Get_Set_AtvQty.getAtvQty(Product,cont,"CC-PDOB01")*	0.8
    #A18	= GS_Get_Set_AtvQty.getAtvQty(Product,cont,"CC-TDOB01")*	5 CXDEV-6770
    #A19	= GS_Get_Set_AtvQty.getAtvQty(Product,cont,"CC-TDOB11")*	5
    A18	= GS_Get_Set_AtvQty.getAtvQty(Product,cont,"CC-TDOB01")*	0
    A19	= GS_Get_Set_AtvQty.getAtvQty(Product,cont,"CC-TDOB11")*	0
    A20	= GS_Get_Set_AtvQty.getAtvQty(Product,cont,"CC-TDOR01")*	0
    A21	= GS_Get_Set_AtvQty.getAtvQty(Product,cont,"CC-TDOR11")*	0
    A22	= GS_Get_Set_AtvQty.getAtvQty(Product,cont,"CC-SDOR01")*	0.147
    A23	= GS_Get_Set_AtvQty.getAtvQty(Product,cont,"CC-PFB402")*	0.212
    A24	= GS_Get_Set_AtvQty.getAtvQty(Product,cont,"CC-TFB402")*	0
    A25	= GS_Get_Set_AtvQty.getAtvQty(Product,cont,"CC-TFB411")*	0
    A26	= GS_Get_Set_AtvQty.getAtvQty(Product,cont,"CC-SFPR01")*	0.6
    A27	= GS_Get_Set_AtvQty.getAtvQty(Product,cont,"CC-PAIM01")*	0.076
    A28	= GS_Get_Set_AtvQty.getAtvQty(Product,cont,"CC-TAIM01")*	0
    A29	= GS_Get_Set_AtvQty.getAtvQty(Product,cont,"MC-TAMT04")*	0.15
    A30	= GS_Get_Set_AtvQty.getAtvQty(Product,cont,"MC-TAMR04")*	0.15
    A31	= GS_Get_Set_AtvQty.getAtvQty(Product,cont,"MC-TAMT14")*	0.15
    #A32	= GS_Get_Set_AtvQty.getAtvQty(Product,cont,"CC-PDIS01")*	0.346 CXDEV-6770
    A32	= GS_Get_Set_AtvQty.getAtvQty(Product,cont,"CC-PDIS01")*	0.095
    A33	= GS_Get_Set_AtvQty.getAtvQty(Product,cont,"CC-PAIX01")*	0.18
    A34	= GS_Get_Set_AtvQty.getAtvQty(Product,cont,"CC-PAOX01")*	0.479
    A35	= GS_Get_Set_AtvQty.getAtvQty(Product,cont,"CC-GAIX21")*	0.32
    A36	= GS_Get_Set_AtvQty.getAtvQty(Product,cont,"CC-GAIX11")*	0.32
    A37	= GS_Get_Set_AtvQty.getAtvQty(Product,cont,"CC-GAOX21")*	0.03
    A38	= GS_Get_Set_AtvQty.getAtvQty(Product,cont,"CC-GAOX11")*	0.03
    A39	= GS_Get_Set_AtvQty.getAtvQty(Product,cont,"CC-GDIL21")*	0.02
    A40	= GS_Get_Set_AtvQty.getAtvQty(Product,cont,"CC-GDIL11")*	0.02
    A41	= GS_Get_Set_AtvQty.getAtvQty(Product,cont,"CC-GDIL01")*	0.02
    A42	= GS_Get_Set_AtvQty.getAtvQty(Product,cont,"CC-GDIL01")*	0.02
    A43	= GS_Get_Set_AtvQty.getAtvQty(Product,cont,"CC-SDXX01")*	0
    A44	= GS_Get_Set_AtvQty.getAtvQty(Product,cont,"CC-TPOX01")*	0.39
    A45	= GS_Get_Set_AtvQty.getAtvQty(Product,cont,"CC-TAID01")*	0.32
    A46	= GS_Get_Set_AtvQty.getAtvQty(Product,cont,"CC-TAID11")*	0.32
    A47	= GS_Get_Set_AtvQty.getAtvQty(Product,cont,"CC-PAIX02")*	0.18
    A48	= GS_Get_Set_AtvQty.getAtvQty(Product,cont,"CC-PAIH02")*	0.18
    A49	= GS_Get_Set_AtvQty.getAtvQty(Product,cont,"TC-CCN014")*	0.002
    A50	= GS_Get_Set_AtvQty.getAtvQty(Product,cont,"TC-CEN021")*	0.003
    A51	= GS_Get_Set_AtvQty.getAtvQty(Product,cont,"CC-TAIX51")*	0.32
    A52	= GS_Get_Set_AtvQty.getAtvQty(Product,cont,"CC-TAIX61")*	0.32
    A53	= GS_Get_Set_AtvQty.getAtvQty(Product,cont,"CC-TAOX51")*	0
    A54	= GS_Get_Set_AtvQty.getAtvQty(Product,cont,"CC-TAOX61")*	0
    A55	= GS_Get_Set_AtvQty.getAtvQty(Product,cont,"CC-TDIL51")*	0
    A56	= GS_Get_Set_AtvQty.getAtvQty(Product,cont,"CC-TDIL61")*	0
    A57	= GS_Get_Set_AtvQty.getAtvQty(Product,cont,"CC-TDOD51")*	0
    A58	= GS_Get_Set_AtvQty.getAtvQty(Product,cont,"CC-TDOD61")*	0
    A59	= GS_Get_Set_AtvQty.getAtvQty(Product,cont,"CC-PAIH51")*	0.18
    A60	= GS_Get_Set_AtvQty.getAtvQty(Product,cont,"CC-PAOH51")*	0.48
    A61	= GS_Get_Set_AtvQty.getAtvQty(Product,cont,"CC-PDIL51")*	0.07
    A62	= GS_Get_Set_AtvQty.getAtvQty(Product,cont,"CC-PDOD51")*	0.14
    Trace.Write("A62:::" +str(A62))
    A63	= GS_Get_Set_AtvQty.getAtvQty(Product,cont,"CC-SDRX01")*	0.07
    A64	= GS_Get_Set_AtvQty.getAtvQty(Product,cont,"CC-PAIN01")*	0.18
    A65	= GS_Get_Set_AtvQty.getAtvQty(Product,cont,"CC-PAIL51")*	0.18
    A66	= GS_Get_Set_AtvQty.getAtvQty(Product,cont,"CC-PAON01")*	0.48
    A67	= GS_Get_Set_AtvQty.getAtvQty(Product,cont,"CC-PPIX01")*	1.2
    A68	= GS_Get_Set_AtvQty.getAtvQty(Product,cont,"CC-TPIX11")*	0.5
    A69	= GS_Get_Set_AtvQty.getAtvQty(Product,cont,"CC-PCNT02")*	0.32
    A70	= GS_Get_Set_AtvQty.getAtvQty(Product,cont,"CC-PCNT05")*	0.32
    A71	= GS_Get_Set_AtvQty.getAtvQty(Product,cont,"CC-IP0101")*	0.39
    A72	= GS_Get_Set_AtvQty.getAtvQty(Product,cont,"CC-PFB802")*	0.38
    A73	= GS_Get_Set_AtvQty.getAtvQty(Product,cont,"CC-PEIM01")*	0.157
    A74	= GS_Get_Set_AtvQty.getAtvQty(Product,cont,"CC-PSV201")*	1.5
    A75	= GS_Get_Set_AtvQty.getAtvQty(Product,cont,"CC-TSV211")*	0.05
    A76	= GS_Get_Set_AtvQty.getAtvQty(Product,cont,"CC-PSP401")*	1.15
    A77	= GS_Get_Set_AtvQty.getAtvQty(Product,cont,"CC-TSP411")*	0.28
    A78 = GS_Get_Set_AtvQty.getAtvQty(Product,cont,"8937-HN2")*     0.08

    sumpup1=(A1+A2+A3+A4+A5+A6+A7+A8+A9+A10+A11+A12+A13+A14+A15+A16+A17+A18+A19+A20)
    sumpup2=(A21+A22+A23+A24+A25+A26+A27+A28+A29+A30+A31+A32+A33+A34+A35+A36+A37+A38+A39+A40)
    sumpup3=(A41+A42+A43+A44+A45+A46+A47+A48+A49+A50+A51+A52+A53+A54+A55+A56+A57+A58+A59+A60)
    sumpup4=(A61+A62+A63+A64+A65+A66+A67+A68+A69+A70+A71+A72+A73+A74+A75+A76+A77+A78)

    j=1
    tlist=[A1,A2,A3,A4,A5,A6,A7,A8,A9,A10,A11,A12,A13,A14,A15,A16,A17,A18,A19,A20,A21,A22,A23,A24,A25,A26,A27,A28,A29,A30,A31,A32,A33,A34,A35,A36,A37,A38,A39,A40,A41,A42,A43,A44,A45,A46,A47,A48,A49,A50,A51,A52,A53,A54,A55,A56,A57,A58,A59,A60,A61,A62,A63,A64,A65,A66,A67,A68,A69,A70,A71,A72,A73,A74,A75,A76,A77,A78]
    for i in tlist:
        j=j+1
        Trace.Write("A"+str(j)+": "+str(i))


    A61 = B61 = C61 = A62 = B62 = C62 = A63 = B63 = C63 = 0
    A73 = B73 = C73 = 0
    A81 = B81 = C81 = A82 = B82 = C82 = A83 = B83 = C83 = 0
    A91 = B91 = C91 = A92 = B92 = C92 = A93 = B93 = C93 = A94 = B94 = C94 = 0
    D11 = E11 = F11 = D12 = E12 = F12 = D13 = E13 = F13 = D14 = E14 = F14 = 0
    paramDict = dict()
    AttrName = 'SerC_IO_Params'
    averageCurrent = Product.Attr('General_Question_Average_current_DO').GetValue()
    if averageCurrent =="":
        averageCurrent=0
    else:
        averageCurrent=m.ceil(float(averageCurrent))
    paramList = ['A61', 'B61', 'C61', 'A62', 'B62', 'C62', 'A63', 'B63', 'C63']
    paramList.extend(['A73', 'B73', 'C73'])
    paramList.extend(['A81', 'B81', 'C81', 'A82', 'B82', 'C82', 'A83', 'B83', 'C83'])
    paramList.extend(['A91', 'B91', 'C91', 'A92', 'B92', 'C92', 'A93', 'B93', 'C93', 'A94', 'B94', 'C94'])
    paramList.extend(['D11', 'E11', 'F11', 'D12', 'E12', 'F12', 'D13', 'E13', 'F13', 'D14', 'E14', 'F14'])
    #Get attribute value quantity and assigned to local variable 
    for key in paramList:
        locals()[key] = GS_Get_Set_AtvQty.getAtvQty(Product, AttrName, key)
    X61 = (A61 + A81 + A91)* 25
    X61v= (D11 * averageCurrent)
    X62 = (A62 + A82 + A92 + A94)* 25
    X62v=(D12 + D14) * averageCurrent
    X63 = (A63 + A73 + A83 + A93)* 25
    X63v=(D13 * averageCurrent)
    X71 = (B61 + B81 + B91)* 25     
    X71v=(E11 * averageCurrent)
    X72 = (B62 + B82 + B92 + B94)* 25 
    X72v=(E12 + E14) * averageCurrent
    X73 = (B63 + B73 + B83 + B93)* 25 
    X73v=(E13 * averageCurrent)
    X81 = (C61 + C81 + C91)* 25     
    X81v=(F11 * averageCurrent)
    X82 = (C62 + C82 + C92 + C94)* 25 
    X82v=(F12 + F14) * averageCurrent
    X83 = (C63 + C73 + C83 + C93)* 25
    X83v=(F13 * averageCurrent)

    AttrName = 'SerC_IO_Params'
    Z51 = divideByX(Product, AttrName, ['G51', 'G52', 'G53', 'G54'], 32.0)
    Z52 = divideByX(Product, AttrName, ['H51', 'H52', 'H53', 'H54'], 32.0)
    Z53 = divideByX(Product, AttrName, ['I51', 'I52', 'I53', 'I54'], 32.0)
    Trace.Write(Z51)
    Trace.Write(Z52)
    Trace.Write(Z53)

    #zsum=(Z51* m.ceil (amps/1000.0)) + (Z52* m.ceil (amps/1000.0)) + (Z53*m.ceil (amps/1000.0)) CXDEV-6770
    zsum = (Z51 + Z52 + Z53) * 5

    x2 = m.ceil ((X61 + X61v)/1000.0) + m.ceil ((X62 + X62v)/1000.0) + m.ceil ((X63 + X63v)/1000.0) + m.ceil ((X71 +X71v)/1000.0) + m.ceil ((X72 +X72v)/1000.0) + m.ceil ((X73 +X73v)/1000.0) + m.ceil ((X81 +X81v)/1000.0) + m.ceil ((X82 +X82v)/1000.0) + m.ceil ((X83 +X83v)/1000.0)


    if iofam=="Turbomachinery":
        sumall=m.ceil(sumpup1+sumpup2+sumpup3+sumpup4+x2+zsum)
    else:
        sumall=0
    Trace.Write("sumall "+str(sumall))
    Trace.Write("zsum "+str(zsum))
    Trace.Write("x2 "+str(x2))
    return sumall