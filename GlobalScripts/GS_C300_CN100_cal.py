import math as m
import GS_Get_Set_AtvQty
from GS_C300_Calc_Module import getTotalLoadIOSerC

#52186
def Controller(Product):
    varValueMap = GS_Get_Set_AtvQty.getAllAtvQty(Product,'SerC_IO_Params')
    totalLoad = getTotalLoadIOSerC(Product, varValueMap)
    section1 = 0
    section2 = 0
    section1 = m.ceil(totalLoad/40)
    
    varDict2={"CC-TAIN01":16,"CC-TAIX51":16,"CC-TAIL51":16,"CC-TAON01":16,"CC-TAOX51":16,"CC-TAIN11":16,"CC-TAIX61":16,"CC-TAON11":16,"CC-TAOX61":16,"CC-TUIO41":32,"CC-TUIO31":32,"CC-TUIO11":32,"CC-TUIO01":32,"CC-TAID11":16,"CC-TAOX11":16,"CC-TAID01":16,"CC-TAOX01":16,"CC-TAIM01":64,"CC-TDIL11":32,"CC-TDI120":32,"CC-TDI230":32,"CC-TDOB11	":32,"CC-TDOR11":32,"CC-TDIL01":32,"CC-TDI110":32,"CC-TDI151":32,"CC-TDI220":32,"CC-TDOB01":32,"CC-TDOR01":32,"CC-TPIX11":8,"CC-GAIX11":16,"CC-GAIX21":16,"CC-GAOX11":16,"CC-GAOX21":16,"CC-GDIL11":32,"CC-GDIL21":32,"CC-GDIL01":32,"CC-GDOL11":32,"CC-TAIX11":16,"CC-TAIX01":16}
    
    for key in varDict2:
        section2 += int(GS_Get_Set_AtvQty.getAtvQty(Product,'Series_C_RG_Part_Summary',key))*int(varDict2[key])
    
    section2 = m.ceil(section2/1280)
    
    result = max(section1,section2)
    #Trace.Write(str(result))
    return result