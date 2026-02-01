import ProductUtil as pu
import GS_SM_PowerLoad_IOTA_A_Calc,GS_SM_component_A_Calc_IOTA
import GS_SM_CompA1_Calcs
import GS_SM_Comp_B_CNMPart_Calc
import GS_SM_Power_Attrs
import GS_SM_PowerLoad_C
import GS_SM_Power_Calc
attrs = GS_SM_Power_Attrs.AttrStorage(Product)
comp_c = GS_SM_PowerLoad_C.get_component_c1(attrs, Product)
if Product.GetContainerByName("SM_CG_Common_Questions_Cont").Rows[0].GetColumnByName("SM_Universal_IOTA").DisplayValue=="PUIO":
    comp_c1 = GS_SM_PowerLoad_C.get_component_c(attrs)
else:
    comp_c1=0
pu.addMessage(Product, "Calculated Value of Component C (RUSIO) : " + str(comp_c))
pu.addMessage(Product, "Calculated Value of Component C (PUIO) : " + str(comp_c1))
A_dict=GS_SM_CompA1_Calcs.get_CompA1(Product)
b_dict=GS_SM_Comp_B_CNMPart_Calc.Comp_B_CNMPart_Calc(Product)

powerload_A = GS_SM_PowerLoad_IOTA_A_Calc.PowerLoad_IOTA_A_Calc(Product)
powerload_A1=GS_SM_component_A_Calc_IOTA.PowerLoad_IOTA_A_Calc(Product)
pu.addMessage(Product, "Calculated Value of Component A (PUIO) : " + str(powerload_A))
pu.addMessage(Product, "Calculated Value of Component A (RUSIO) : " + str(powerload_A1))
pu.addMessage(Product, "A comp = "+str(A_dict))
pu.addMessage(Product, "B comp = "+str(b_dict))

comp_b = GS_SM_Power_Calc.get_power_component_b(attrs)
pu.addMessage(Product, "Calculated Value of Component B (PUIO) : " + str(comp_b))
if Product.GetContainerByName("SM_CG_Common_Questions_Cont").Rows[0].GetColumnByName("SM_Universal_IOTA").DisplayValue=="RUSIO":
    pu.addMessage(Product, "Calculated Value of Component B (RUSIO) : " + str(comp_b))