import GS_SM_component_A_Calc_IOTA, GS_SM_PowerLoad_IOTA_A_Calc
#Component B and C
import GS_SM_Power_Attrs
#Component B
import GS_SM_Power_Calc
#Component C
import GS_SM_PowerLoad_C

def getFloat(val):
    if val:
        try:
            return float(val)
        except:
            return 0
    return 0

def Load_SM_RIO_cabinet_summary_Calc(Product, parts_dict):
    #Control Groups
    cg_count = 1
    control_groups = Product.GetContainerByName('SM_ControlGroup_Cont').Rows
    load_sm_rio = dict()
    for cgs in control_groups:
        cg_product = cgs.Product
        Trace.Write(cg_product.Name)
        try:
            comp_a = GS_SM_component_A_Calc_IOTA.PowerLoad_IOTA_A_Calc(cg_product)
            Trace.Write("CG "+str(cg_count)+ " - A = "+str(comp_a))
        except:
            comp_a = 0.0
            Trace.Write("Error in CG - A component "+str(cg_count))

        comp_b = 0.0

        try:
            power_attrs = GS_SM_Power_Attrs.AttrStorage(cg_product)
        except Exception,e:
            power_attrs = None
            Trace.Write("Error when Reading GS_SM_Power_Attrs: " + str(e))

        if power_attrs:
            try:
                comp_b = GS_SM_Power_Calc.get_power_component_b(power_attrs)
                Trace.Write("CG "+str(cg_count)+ " - B = "+str(comp_b))
            except Exception,e:
                Trace.Write("Error in GS_SM_Power_Calc - Component B calculations: " + str(e))

        try:
            attrs = GS_SM_Power_Attrs.AttrStorage(cg_product)
            comp_c = GS_SM_PowerLoad_C.get_component_c1(attrs, cg_product)
            Trace.Write("CG "+str(cg_count)+ " - C = "+str(comp_c))
        except:
            comp_c = 0.0
            Trace.Write("Error in CG - C component "+str(cg_count))

        try:
            d_dict = calculate_loads(parts_dict)
            comp_d = 0.0
            for x in d_dict.values():
                comp_d = comp_d + x
            Trace.Write("D = "+str(comp_d))
        except:
            comp_d = 0.0
            Trace.Write("Error in D component")

        load_sm_rio_tmp = 0.0
        load_sm_rio_tmp = float((comp_a + comp_b + comp_c + comp_d)/float(1000))
        load_sm_rio[str('load_sm_rio_cg_' + str(cg_count))] = str(round(load_sm_rio_tmp))
        Trace.Write(str('load_sm_rio_cg_' + str(cg_count)) + " : " + str(load_sm_rio[str('load_sm_rio_cg_' + str(cg_count))]))
        rg_count = 1
        remote_groups = cg_product.GetContainerByName('SM_RemoteGroup_Cont').Rows
        for rgs in remote_groups:
            #Remote groups
            rg_product = rgs.Product
            Trace.Write(rg_product.Name)
            try:
                comp_a = GS_SM_component_A_Calc_IOTA.PowerLoad_IOTA_A_Calc(rg_product)
                Trace.Write("RG "+str(rg_count)+ " - A = "+str(comp_a))
            except:
                comp_a = 0.0
                Trace.Write("Error in RG - A component "+str(rg_count))
                
            comp_b = 0.0
            
            try:
                power_attrs = GS_SM_Power_Attrs.AttrStorage(rg_product)
            except Exception,e:
                power_attrs = None
                Trace.Write("Error when Reading GS_SM_Power_Attrs: " + str(e))
            
            if power_attrs:
                try:
                    comp_b = GS_SM_Power_Calc.get_power_component_b(power_attrs)
                    Trace.Write("RG "+str(rg_count)+ " - B = "+str(comp_b))
                except Exception,e:
                    Trace.Write("Error in GS_SM_Power_Calc - Component B calculations: " + str(e))
            
            try:
                attrs = GS_SM_Power_Attrs.AttrStorage(rg_product)
                comp_c = GS_SM_PowerLoad_C.get_component_c1(attrs, rg_product)
                Trace.Write("RG "+str(rg_count)+ " - C = "+str(comp_c))
            except:
                comp_c = 0.0
                Trace.Write("Error in RG - C component "+str(rg_count))
            
            try:
                d_dict = calculate_loads(parts_dict)
                comp_d = 0.0
                for x in d_dict.values():
                    comp_d = comp_d + x
                Trace.Write("D = "+str(comp_d))
            except:
                comp_d = 0.0
                Trace.Write("Error in D component")
                
            load_sm_rio_tmp = 0.0
            load_sm_rio_tmp = float((comp_a + comp_b + comp_c + comp_d)/float(1000))
            load_sm_rio[str('load_sm_rio_cg_' + str(cg_count)+'_rg_'+str(rg_count))] = str(round(load_sm_rio_tmp))
            Trace.Write(str('load_sm_rio_cg_' + str(cg_count)+'_rg_'+str(rg_count)) + " : " + str(load_sm_rio[str('load_sm_rio_cg_' + str(cg_count)+'_rg_'+str(rg_count))]))
            rg_count+=1
        cg_count+=1
    return load_sm_rio
    
def Load_SM_RIO_cabinet_summary_CG_RG_Calc(Product, parts_dict, cabinet_calculated=False):
    Trace.Write("Product name : "+Product.Name)
    iota = ""
    if Product.Name == "SM Remote Group":
        iota = Product.Attr("SM_Universal_IOTA_Type").GetValue()
    elif Product.Name == "SM Control Group":
        iota=Product.GetContainerByName('SM_CG_Common_Questions_Cont').Rows[0].GetColumnByName('SM_Universal_IOTA').DisplayValue
    try:
        comp_a = 0
        if iota == "RUSIO":
            comp_a = GS_SM_component_A_Calc_IOTA.PowerLoad_IOTA_A_Calc(Product)
        else:
            comp_a = GS_SM_PowerLoad_IOTA_A_Calc.PowerLoad_IOTA_A_Calc(Product)
        Trace.Write("A = "+str(comp_a))
    except:
        comp_a = 0.0
        Trace.Write("Error in A component")
        
    comp_b = 0.0
    
    try:
        power_attrs = GS_SM_Power_Attrs.AttrStorage(Product)
    except Exception,e:
        power_attrs = None
        Trace.Write("Error when Reading GS_SM_Power_Attrs: " + str(e))
        
    if power_attrs:
        try:
            comp_b = GS_SM_Power_Calc.get_power_component_b(power_attrs)
            Trace.Write("B = "+str(comp_b))
        except Exception,e:
            Trace.Write("Error in GS_SM_Power_Calc - Component B calculations: " + str(e))

    try:
        comp_c = 0
        attrs = GS_SM_Power_Attrs.AttrStorage(Product)
        if iota == "RUSIO":
            comp_c = GS_SM_PowerLoad_C.get_component_c1(attrs, Product)
        else:
            comp_c = GS_SM_PowerLoad_C.get_component_c(attrs)
        Trace.Write("C = "+str(comp_c))
    except:
        comp_c = 0.0
        Trace.Write("Error in C component")

    try:
        d_dict = calculate_loads(parts_dict, cabinet_calculated)
        comp_d = 0.0
        for x in d_dict.values():
            comp_d = comp_d + x
        labor_parameter_ai = getFloat(Product.Attr("Labor_parameter_ai").getValue())
        labor_parameter_ao = getFloat(Product.Attr("Labor_parameter_ao").getValue())
        labor_parameter_di = getFloat(Product.Attr("Labor_parameter_di").getValue())
        labor_parameter_do = getFloat(Product.Attr("Labor_parameter_do").getValue())
        if labor_parameter_ai + labor_parameter_ao + labor_parameter_di + labor_parameter_do == 0:
            comp_d = 0.0
        Trace.Write("D = "+str(comp_d))
    except:
        comp_d = 0.0
        Trace.Write("Error in D component")

    load_sm_rio = 0.0
    load_sm_rio = (comp_a + comp_b + comp_c + comp_d)/1000.0
    Trace.Write("a : {}, b : {}, c : {}, d : {}".format(comp_a, comp_b, comp_c, comp_d))
    return load_sm_rio

def getPartQty(parts_dict, part):
    part_data = parts_dict.get(part)
    if part_data:
        return part_data["Quantity"]
    return 0

def getPartsQty(parts_dict, parts):
    res = 0
    for part in parts:
        res += getPartQty(parts_dict, part)
    return res

def calculate_loads(parts_dict, cabinet_calculated=False):
    res = dict()
    if cabinet_calculated:
        res["FAN_LOAD"] = getPartQty(parts_dict, "FC-FANWR-24R") * 400
        res["TELD_LOAD"] = getPartQty(parts_dict, "FC-TELD-0001") * 10
    else:
        res["FAN_LOAD"] = 1 * 400 # if cabinet are not calculated default 1 fan and 2 TELD
        res["TELD_LOAD"] = 2 * 10
    res["CNM_SWITCH_LOAD"] = (getPartsQty(parts_dict, ["CC-INWM01", "CC-INWE01"]))*450 + (getPartsQty(parts_dict, ["CC-TNWD01", "CC-TNWC01"]))*900
    res["GIIS_INTEGRATION_BOARD_LOAD"] = (
        getPartQty(parts_dict, "FC-GPCS-RIO16-PF") * 21
        + getPartQty(parts_dict, "HIC2831R2") * 46
        + getPartQty(parts_dict, "HIC2853R2") * 30
        + getPartQty(parts_dict, "HIC2025") * 46
        + getPartQty(parts_dict, "HIC2031") * 30
        + getPartQty(parts_dict, "HIC2871") * 42
    )
    res["MOXA_LOAD"] = (
        getPartQty(parts_dict, "4600116") * 1120
        + getPartQty(parts_dict, "4600131") * 160
        + getPartQty(parts_dict, "4600117") * 160
        + getPartQty(parts_dict, "4600132") * 170
        + getPartQty(parts_dict, "4600118") * 170
        + getPartQty(parts_dict, "4600133") * 250
        + getPartsQty(parts_dict, ["4600112", "4600136", "4600130", "4600121"])*440
        + getPartsQty(parts_dict, ["4600122", "4600113"])*160
        + getPartsQty(parts_dict, ["4600114", "4600123"])*250
    )
    return res