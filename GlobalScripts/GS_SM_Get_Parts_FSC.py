import System.Decimal as D
import GS_SMPartsCalc
#parts_dict={}
#cab = GS_SM_CGSystemCabinetsFront.getCGNoOfSystemCabinetFront(parts_dict)

def Get_CG_Parts_FSC(Product,parts_dict):
    if Product.Name=="SM Control Group":
        cab, powerSupply, switches = GS_SMPartsCalc.getNumberOfCGCabinet(Product)
        iota = Product.GetContainerByName("SM_CG_Common_Questions_Cont").Rows[0].GetColumnByName("SM_Universal_IOTA").DisplayValue
        #Trace.Write("iota="+str(iota))
        cabinet_access = Product.GetContainerByName("SM_CG_Cabinet_Details_Cont_Left").Rows[0].GetColumnByName("Cabinet_Access").DisplayValue
        eld=Product.GetContainerByName("SM_CG_Cabinet_Details_Cont_Left").Rows[0].GetColumnByName("ELD_Module").DisplayValue
        #Trace.Write("cabinet_access="+str(cabinet_access))
        qty = cab
        #CXCPQ-33071,33078
        if iota =="PUIO" and cabinet_access == "Single Access":
            if qty>0:
                parts_dict["FS-MB-0002"] = {'Quantity' : qty,'Description':'Power busbar max.200A 24/48/110Vdc, 60cm'}
                parts_dict["FS-PDC-MB24-1P"]={'Quantity':qty,'Description':'POWER DISTR.CABLE MB-0001 TO PDB-0824 LS'}
            #CXCPQ-33070
            if eld=="Yes":
                if powerSupply>0 or switches>0:
                    var1=D.Ceiling(powerSupply/4.0)
                    var2=D.Ceiling(switches/6.0)
                    var=max(var1,var2)
                    
                    parts_dict["FC-TELD-0001"]={'Quantity':var,'Description':'UIO EARTH LEAKAGE DETECTOR 24VDC CC'}
            if powerSupply>0 or switches>0:
                var1 = D.Ceiling(switches/6.0)
                var2 =D.Ceiling(powerSupply/4.0)
                var= max(var1,var2)
                parts_dict["FC-PDB-0824P"] = {'Quantity' :var,'Description':'Power distr.board 8ch.24Vdc 2A CC'}
    
    elif Product.Name == "SM Remote Group":
        cab1, powerSupply1, switches1 = GS_SMPartsCalc.getNumberOfRGCabinet(Product)
        Enclosure_type = Product.GetContainerByName('SM_RG_ATEX Compliance_and_Enclosure_Type_Cont').Rows[0].GetColumnByName('Enclosure_Type').DisplayValue
        #Trace.Write("Enclosure_type="+str(Enclosure_type))
        iota = Product.Attr("SM_Universal_IOTA_Type").GetValue()
        #Trace.Write("iota="+str(iota))
        Cabinet_Access = Product.GetContainerByName("SM_RG_Cabinet_Details_Cont_Left").Rows[0].GetColumnByName("Cabinet_Access").DisplayValue
        #Trace.Write("Cabinet_Access= "+str(Cabinet_Access))
        eld=Product.GetContainerByName("SM_RG_Cabinet_Details_Cont_Left").Rows[0].GetColumnByName("ELD_Module").DisplayValue
        qty1 = cab1
        if Enclosure_type == "Cabinet":
            #CXCPQ-33071,33078
            if iota =="PUIO" and Cabinet_Access == "Single Access":
                if qty1>0:
                    parts_dict["FS-MB-0002"] = {'Quantity' : qty1,'Description':'Power busbar max.200A 24/48/110Vdc, 60cm'}
                    parts_dict["FS-PDC-MB24-1P"]={'Quantity':qty1,'Description':'POWER DISTR CABLE MB-0001 TO PDB-0824 LS'}
                #CXCPQ-33070
                if eld=="Yes":
                    if powerSupply1>0 or switches1>0:
                        var1=D.Ceiling(powerSupply1/4.0)
                        var2=D.Ceiling(switches1/6.0)
                        var=max(var1,var2)
                        parts_dict["FC-TELD-0001"]={'Quantity':var,'Description':'UIO EARTH LEAKAGE DETECTOR 24VDC CC'}
                if powerSupply1>0 or switches1>0:
                    var1=D.Ceiling(powerSupply1/4.0)
                    var2=D.Ceiling(switches1/6.0)
                    var=max(var1,var2)
                    parts_dict["FC-PDB-0824P"] = {'Quantity' :var,'Description':'Power distr.board 8ch.24Vdc 2A CC'}
    return parts_dict
#func =Get_CG_Parts_FSC(Product,parts_dict)
#Trace.Write("func="+str(func))