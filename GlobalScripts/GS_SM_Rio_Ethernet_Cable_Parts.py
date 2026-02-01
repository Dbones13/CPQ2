#CXCPQ-33622
import System.Decimal as D
from GS_SM_CompA1_Calcs import get_CompA1
#from GS_SM_Comp_B_CNMPart_Calc import Comp_B_CNMPart_Calc

def Rio_Ethernet_Cable_Parts(Prod, parts_dict):
    Trace.Write("Product Name : "+Prod.Name)
    comp_a = {}
    #comp_b = {}
    if Prod.Name=="SM Control Group":
        try:
            switch_type = Prod.GetContainerByName('SM_CG_Common_Questions_Cont').Rows[0].GetColumnByName("SM_Switch_Safety_IO").Value
            Trace.Write("Switch Type = "+str(switch_type))
        except:
            Trace.Write("Error getting SM_CG_Common_Questions_Cont.SM_Switch_Safety_IO value")
        if switch_type:
            if switch_type != "Control Network Module (CNM)":
                Trace.Write("Not adding the part FS-CCI-HSE-08 as switch type is not CNM")
                return parts_dict
        else:
            Trace.Write("Could not identify switch type")
            return parts_dict
        try:
            comp_a = get_CompA1(Prod)
            #comp_b = Comp_B_CNMPart_Calc(Prod)
        except:
            Trace.Write("Error getting Component A and /or B value")
        if comp_a:
            Trace.Write("A comp = "+str(comp_a))
            #Trace.Write("B comp = "+str(comp_b))
            cnm_mod = 2 * D.Ceiling(comp_a['M'])
            Trace.Write("CNM mod = "+str(cnm_mod))
            qty = 2 * (cnm_mod - 1)
            if qty > 0:
                parts_dict["FS-CCI-HSE-08"] = {'Quantity' : qty, 'Description': 'SM RIO Ethernet Cable Set'}
        else:
            Trace.Write("Component A and / or Component B is empty")
    elif Prod.Name=="SM Remote Group":
        try:
            switch_type = Prod.Attr('SM_CG_Safety_IO_Link').GetValue()
            Trace.Write("Switch Type = "+str(switch_type))
        except:
            Trace.Write("Error getting SM_CG_Safety_IO_Link")
        if switch_type:
            if switch_type != "Control Network Module (CNM)":
                Trace.Write("Not adding the part FS-CCI-HSE-08 as switch type is not CNM")
                return parts_dict
        else:
            Trace.Write("Could not identify switch type")
            return parts_dict
        try:
            comp_a = get_CompA1(Prod)
        except:
            Trace.Write("Error getting Component A value")
        if comp_a:
            Trace.Write("A comp = "+str(comp_a))
            cnm_mod = 2 * D.Ceiling(comp_a['M'])
            Trace.Write("CNM mod = "+str(cnm_mod))
            qty = 2 * (cnm_mod - 1)
            if qty > 0:
                parts_dict["FS-CCI-HSE-08"] = {'Quantity' : qty, 'Description': 'SM RIO Ethernet Cable Set'}
        else:
            Trace.Write("Component A is empty")
    else:
        Trace.Write("Product is neither CG nor RG")
    return parts_dict

#parts = {}
#x=Rio_Ethernet_Cable_Parts(Product, parts)
#Trace.Write("Parts = "+str(parts))