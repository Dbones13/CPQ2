#CXCPQ-  Sprint 16
import System.Decimal as D
import math as m
import GS_SMPartsCalc
#parts_dict={}
def get_parts(Product,parts_dict):
    if Product.Name == "SM Control Group":
        SM_CG_Uni_IOTA = Product.GetContainerByName('SM_CG_Common_Questions_Cont').Rows[0].GetColumnByName('SM_Universal_IOTA').DisplayValue
        SM_CG_Cab_Access= Product.GetContainerByName('SM_CG_Cabinet_Details_Cont_Left').Rows[0].GetColumnByName('Cabinet_Access').DisplayValue
        SM_CG_Cab_Light= Product.GetContainerByName('SM_CG_Cabinet_Details_Cont_Left').Rows[0].GetColumnByName('Cabinet_Light').DisplayValue
        SM_CG_ELD_Mod= Product.GetContainerByName('SM_CG_Cabinet_Details_Cont_Left').Rows[0].GetColumnByName('ELD_Module').DisplayValue
        SM_CG_Key_Switch_Mod = Product.GetContainerByName('SM_CG_Cabinet_Details_Cont_Right').Rows[0].GetColumnByName('Key_Switch_Module_Required').DisplayValue
        cab_qnt,powerSupply,switches=GS_SMPartsCalc.getNumberOfCGCabinet(Product)
        Trace.Write("cabinet qty : "+str(cab_qnt))
        Trace.Write("Power Supply : "+str(powerSupply))
        Trace.Write("Switches : "+str(switches))
        cg_qty = cab_qnt
        if SM_CG_Uni_IOTA == "PUIO" and SM_CG_Cab_Access == "Dual Access" :
            if cg_qty >0:
                parts_dict["FC-FANWR-24R"] = {"Quantity" : int(cg_qty) , "Description": '24Vdc fan unit with readback CC'}   #CXCPQ-32167
                if SM_CG_Cab_Light == "Yes":
                    parts_dict["4140252"] = {"Quantity" : 2*int(cg_qty) , "Description": 'ABL SURSUM BREAKER 8A 2D8UM'}  #CXCPQ-32169
                    parts_dict["SZ 4315.150"] = {"Quantity" : 2*int(cg_qty) , "Description": 'RITTAL POWER CABLE 3M GREY'}  #CXCPQ-32172
                    parts_dict["SZ 4155.110"] = {"Quantity" : 2*int(cg_qty) , "Description": '(RITTAL CAB. LIGHT 110/240V+SENSOR+OUTLET)'}  #CXCPQ-32168
                if SM_CG_ELD_Mod == "Yes":
                    if powerSupply >0 or switches >0:
                        cg_qty1 = D.Ceiling(switches/6.0)
                        cg_qty2 = D.Ceiling(powerSupply/4.0)
                        cg_qty= max(cg_qty1,cg_qty2)
                        parts_dict["FC-TELD-0001"] = {"Quantity" : int(cg_qty) , "Description": 'UIO EARTH LEAKAGE DETECTOR 24VDC CC'}
        cg_qty = cab_qnt
    elif Product.Name == "SM Remote Group":
        SM_RG_Uni_IOTA = Product.Attr("SM_Universal_IOTA_Type").GetValue()
        Enclosure_Type = Product.GetContainerByName('SM_RG_ATEX Compliance_and_Enclosure_Type_Cont').Rows[0].GetColumnByName('Enclosure_Type').DisplayValue
        SM_RG_Cab_Access= Product.GetContainerByName('SM_RG_Cabinet_Details_Cont_Left').Rows[0].GetColumnByName('Cabinet_Access').DisplayValue
        SM_RG_Cab_Light= Product.GetContainerByName('SM_RG_Cabinet_Details_Cont_Left').Rows[0].GetColumnByName('Cabinet_Light').DisplayValue
        SM_RG_ELD_Mod= Product.GetContainerByName('SM_RG_Cabinet_Details_Cont_Left').Rows[0].GetColumnByName('ELD_Module').DisplayValue
        SM_RG_Key_Switch_Mod = Product.GetContainerByName('SM_RG_Cabinet_Details_Cont').Rows[0].GetColumnByName('SM_Key_Switch_ModuleRequired').DisplayValue
        cab_qnt, powerSupply, switches = GS_SMPartsCalc.getNumberOfRGCabinet(Product)
        Trace.Write("Cabinet qty : "+str(cab_qnt))
        Trace.Write("Power Supply : "+str(powerSupply))
        Trace.Write("Switches : "+str(switches))
        rg_qty = cab_qnt
        if Enclosure_Type == "Cabinet":
            if SM_RG_Uni_IOTA == "PUIO" and SM_RG_Cab_Access == "Dual Access" :
                if rg_qty >0:
                    parts_dict["FC-FANWR-24R"] = {"Quantity" : int(rg_qty) , "Description": '24Vdc fan unit with readback CC'}   #CXCPQ-32167
                    if SM_RG_Cab_Light == "Yes":
                        parts_dict["4140252"] = {"Quantity" : 2*int(rg_qty) ,"Description" :  'ABL SURSUM BREAKER 8A 2D8UM'}  #CXCPQ-32169
                        parts_dict["SZ 4315.150"] = {"Quantity" : 2*int(rg_qty) , "Description": 'RITTAL POWER CABLE 3M GREY'}   #CXCPQ-32172
                        parts_dict["SZ 4155.110"] = {"Quantity" : 2*int(rg_qty) , "Description": '(RITTAL CAB. LIGHT 110/240V+SENSOR+OUTLET)'}  #CXCPQ-32168
                    if SM_RG_ELD_Mod == "Yes":
                        if powerSupply >0 or switches >0:
                            rg_qty1 = D.Ceiling(switches/6.0)
                            rg_qty2 = D.Ceiling(powerSupply/4.0)
                            rg_qty = max(rg_qty1,rg_qty2)
                            parts_dict["FC-TELD-0001"] = {"Quantity" : int(rg_qty) , "Description": 'UIO EARTH LEAKAGE DETECTOR 24VDC CC'}
            rg_qty = cab_qnt
    return parts_dict
#func1= get_parts(Product,parts_dict)
#Trace.Write("CR&RG"+str(func1))