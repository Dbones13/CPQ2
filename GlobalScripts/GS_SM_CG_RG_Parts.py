#cxcpq-33364,33365, 33366 and 33368,33369
import System.Decimal as D
import math as m
import GS_SMPartsCalc
#parts_dict={}

def cabinet_part(Product,parts_dict):
    if Product.Name=="SM Control Group":
        iota = Product.GetContainerByName("SM_CG_Common_Questions_Cont").Rows[0].GetColumnByName("SM_Universal_IOTA").DisplayValue
        #Trace.Write("iota= "+str(iota))
        Cabinet_Access = Product.GetContainerByName("SM_CG_Cabinet_Details_Cont_Left").Rows[0].GetColumnByName("Cabinet_Access").DisplayValue
        #Trace.Write("Cabinet_Access= "+str(Cabinet_Access))
        Cabinet_Light = Product.GetContainerByName("SM_CG_Cabinet_Details_Cont_Left").Rows[0].GetColumnByName("Cabinet_Light").DisplayValue
        #Trace.Write("Cabinet_Light= "+str(Cabinet_Light))
        ELD_Module = Product.GetContainerByName("SM_CG_Cabinet_Details_Cont_Left").Rows[0].GetColumnByName("ELD_Module").DisplayValue
        #Trace.Write("ELD_Module= "+str(ELD_Module))
        cab_qnt,power_supply,switches = GS_SMPartsCalc.getNumberOfCGCabinet(Product)
        var = cab_qnt

        Trace.Write("cab_qnt"+str(cab_qnt))
        Trace.Write("power_supply"+str(power_supply))
        Trace.Write("switches"+str(switches))
        Trace.Write("var= "+str(var))

        #CXCPQ-33366 and CXCPQ-33369
        if iota == "RUSIO" and Cabinet_Access == "Single Access":
            if var>0:
                parts_dict["FS-MB-0002"] = {"Quantity" : int(var), "Description" : "Power busbar max.200A 24/48/110Vdc, 60cm"}
                parts_dict["FS-PDC-MB24-1P"] = {"Quantity" : int(var), "Description" : "POWER DISTR.CABLE MB-0001 TO PDB-0824 LS"}
                if Cabinet_Light == "Yes":
                    parts_dict["SZ 4315.150"] = {"Quantity" : int(var), "Description" : "RITTAL POWER CABLE 3M GREY"}

        if iota == "RUSIO" and Cabinet_Access == "Single Access":
            if power_supply >0 or switches > 0 or var>0:
                qty = max(m.ceil(power_supply/4.0),m.ceil(switches/6.0))
                parts_dict["FC-PDB-0824P"] = {"Quantity" : int(qty), "Description" : "Power distr.board 8ch.24Vdc 2A CC"}
        if iota == "RUSIO" and Cabinet_Access == "Single Access" and ELD_Module == "Yes":
            if power_supply >0 or switches > 0 or var>0:
                qty = max(m.ceil(power_supply/4.0),m.ceil(switches/6.0))
                parts_dict["FC-TELD-0001"] = {"Quantity" : int(qty), "Description" : "UIO EARTH LEAKAGE DETECTOR 24VDC CC"}
        if iota == "RUSIO" and Cabinet_Access != "Single Access":
            if var>0:
                parts_dict["FS-MB-0002"] = {"Quantity" : int(var), "Description" : "Power busbar max.200A 24/48/110Vdc, 60cm"}
        if iota == "RUSIO" and Cabinet_Access != "Single Access" and ELD_Module == "Yes":
            if power_supply >0 or switches > 0 or var>0:
                qty = max(m.ceil(power_supply/4.0),m.ceil(switches/6.0))
                parts_dict["FC-TELD-0001"] = {"Quantity" : int(qty), "Description" : "UIO EARTH LEAKAGE DETECTOR 24VDC CC"}


    elif Product.Name=="SM Remote Group":
        iota = Product.Attr("SM_Universal_IOTA_Type").GetValue()
        Trace.Write("iota= "+str(iota))
        Cabinet_Access = Product.GetContainerByName("SM_RG_Cabinet_Details_Cont_Left").Rows[0].GetColumnByName("Cabinet_Access").DisplayValue
        Trace.Write("Cabinet_Access= "+str(Cabinet_Access))
        Enclosure_Type =Product.GetContainerByName('SM_RG_ATEX Compliance_and_Enclosure_Type_Cont').Rows[0].GetColumnByName('Enclosure_Type').DisplayValue
        Trace.Write("Enclosure_Type= "+str(Enclosure_Type))
        Cabinet_Light = Product.GetContainerByName("SM_RG_Cabinet_Details_Cont_Left").Rows[0].GetColumnByName("Cabinet_Light").DisplayValue
        Trace.Write("Cabinet_Light= "+str(Cabinet_Light))
        ELD_Module = Product.GetContainerByName("SM_RG_Cabinet_Details_Cont_Left").Rows[0].GetColumnByName("ELD_Module").DisplayValue
        Trace.Write("ELD_Module= "+str(ELD_Module))
        cab_qnt,power_supply,switches = GS_SMPartsCalc.getNumberOfRGCabinet(Product)
        var = cab_qnt

        Trace.Write("cab_qnt"+str(cab_qnt))
        Trace.Write("power_supply"+str(power_supply))
        Trace.Write("switches"+str(switches))
        Trace.Write("var= "+str(var))

        if Enclosure_Type == "Cabinet":
            if iota == "RUSIO" and Cabinet_Access != "Single Access":
                if power_supply >0 or switches > 0 or var>0:
                    parts_dict["FS-MB-0002"] = {"Quantity" : int(var), "Description" : "Power busbar max.200A 24/48/110Vdc, 60cm"}
                    if ELD_Module == "Yes":
                        qty = max(m.ceil(power_supply/4.0),m.ceil(switches/6.0))
                        parts_dict["FC-TELD-0001"] = {"Quantity" : int(qty), "Description" : "UIO EARTH LEAKAGE DETECTOR 24VDC CC"}
            if iota == "RUSIO" and Cabinet_Access == "Single Access":
                if var>0 :
                    parts_dict["FS-MB-0002"] = {"Quantity" : int(var), "Description" : "Power busbar max.200A 24/48/110Vdc, 60cm"}
                    parts_dict["FS-PDC-MB24-1P"] = {"Quantity" : int(var), "Description" : "POWER DISTR.CABLE MB-0001 TO PDB-0824 LS"}
                    if Cabinet_Light == "Yes":
                        parts_dict["SZ 4315.150"] = {"Quantity" : int(var), "Description" : "RITTAL POWER CABLE 3M GREY"}

            if iota == "RUSIO" and Cabinet_Access == "Single Access":
                if power_supply >0 or switches > 0 or var>0:
                    qty = max(m.ceil(power_supply/4.0),m.ceil(switches/6.0))
                    parts_dict["FC-PDB-0824P"] = {"Quantity" : int(qty), "Description" : "Power distr.board 8ch.24Vdc 2A CC"}
                    if ELD_Module == "Yes":
                        qty = max(m.ceil(power_supply/4.0),m.ceil(switches/6.0))
                        parts_dict["FC-TELD-0001"] = {"Quantity" : int(qty), "Description" : "UIO EARTH LEAKAGE DETECTOR 24VDC CC"}


    return parts_dict