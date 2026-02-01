import GS_Exp_ENT_BOM_Calcs
import Gs_EXpEnt_Grp_BOM_calcs

#CXCPQ-37543,37198,37544
serever_qnt_T,serever_qntnode_T,station_37200=GS_Exp_ENT_BOM_Calcs.server_qnt1(Product)
station_svr37545=GS_Exp_ENT_BOM_Calcs.QNTCXCPQ_37545(Product)
svr_hardt37547=GS_Exp_ENT_BOM_Calcs.Qnt37547(Product)
svr_hardt37552,svr_hardt16gb,svr_hardt16gb1=Gs_EXpEnt_Grp_BOM_calcs.QNTCXCPQ_37552(Product)
svr_MZ_PCIS02_2,svr_MZ_PCIS02_4,svr_MZ_PCIS02_6,svr_MZ_PCIS02_8,svr_MZ_PCIS02_10=Gs_EXpEnt_Grp_BOM_calcs.MZ_PCIS02(Product)

Product.Attr('exp_ent_Quantity37198').AssignValue(str(serever_qnt_T))#CXCPQ-37198
Product.Attr('stationQnt37198').AssignValue(str(station_svr37545))#for CXCPQ-37545,CXCPQ-37546
Product.Attr('ServerQuantity37544').AssignValue(str(serever_qntnode_T)) #CXCPQ-37543,CXCPQ-37544
Product.Attr('station_37200').AssignValue(str(station_37200)) #CXCPQ-37200
Product.Attr('svr_hardt37547qnt').AssignValue(str(svr_hardt37547)) #CXCPQ-37547
Product.Attr('Quantity_MZ-PCEH17').AssignValue(str(svr_hardt37552)) #CXCPQ-37552
Product.Attr('svr_hardt16gb_qnt').AssignValue(str(svr_hardt16gb)) #CXCPQ-37554
Product.Attr('MZ-PCEM44_qnt').AssignValue(str(svr_hardt16gb1)) #CXCPQ-37553
Product.Attr('MZ_PCSV84_qnt').AssignValue(str(svr_MZ_PCIS02_4)) #CXCPQ-37555
Product.Attr('MZ_PCIS02_qnt').AssignValue(str(svr_MZ_PCIS02_2)) #CXCPQ-37556
Product.Attr('MZ_PCST02 qnt').AssignValue(str(svr_MZ_PCIS02_8)) #CXCPQ-37557
Product.Attr('MZ_PCST82 qnt').AssignValue(str(svr_MZ_PCIS02_6)) #CXCPQ-37558
Product.Attr('MZ_PCSR02 qnt').AssignValue(str(svr_MZ_PCIS02_10)) #CXCPQ-37559