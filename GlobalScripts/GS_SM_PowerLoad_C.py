import System.Decimal as d
def get_int(val):
    if val:
       return int(val)
    return 0

def get_float(val):
    if val:
        return float(val)
    return 0

def get_component_c(attrs):
    sil2_di = sil3_di = typePf_ai = typePf_ao = sil3_do = 0
    sil2_di1 = sil3_di1 = typePf_ai1 = typePf_ao1 = sil3_do1 = 0
    component_C1 =component_C1=component_C1=0
    #Red Is
    # DI
    try:
        sil2_di = (get_int(attrs.uio_di_sil2) * 7.0)
    except:
        sil2_di = 0
    try:
        sil3_di = (get_int(attrs.uio_di_sil3) * 7.0)
    except:
        sil3_di = 0
    # AI
    try:
        typePf_ai = (get_int(attrs.uio_ai_pf)* 25.0)
    except:
        typePf_ai = 0
    # AO
    try:
        typePf_ao = (get_int(attrs.uio_ao_pf)*25.0)
    except:
        typePf_ao = 0
    # DO
    try:
        sil3_do = (get_int(attrs.uio_do_sil3)* 70.0)
    except:
        sil3_do = 0
    component_C1 = (sil2_di+sil3_di+typePf_ai+typePf_ao+sil3_do)
    if component_C1 >0:
        component_C1=component_C1+ 600.0
    # Non red IS
    # DI
    try:
        sil2_di1 = (get_int(attrs.uio_di_sil2_nr) * 7.0)
    except:
        sil2_di1 = 0
    try:
        sil3_di1 = (get_int(attrs.uio_di_sil3_nr) * 7.0)
    except:
        sil3_di1 = 0
    # AI
    try:
        typePf_ai1 = (get_int(attrs.uio_ai_pf_nr) * 25.0)
    except:
        typePf_ai1 = 0
    # AO
    try:
        typePf_ao1 = (get_int(attrs.uio_ao_pf_nr) * 25.0)
    except:
        typePf_ao1 = 0
    # DO
    try:
        sil3_do1 = (get_int(attrs.uio_do_sil3_nr) * 70.0)
    except:
        sil3_do1 = 0
    component_C2 = (sil2_di1+sil3_di1+typePf_ai1+typePf_ao1+sil3_do1)
    if component_C2 >0:
        component_C2=component_C2+ 300.0
    component_C = d.Ceiling(component_C1 + component_C2)
    return component_C

#CXCPQ-31187 added by Lahu.
#CXCPQ-31187 added by Lahu.
def get_component_c1(attrs,Product):
    component_C=0
    if Product.Name=="SM Control Group":
        if Product.GetContainerByName("SM_CG_Common_Questions_Cont").Rows[0].GetColumnByName("SM_Universal_IOTA").DisplayValue=="RUSIO":
            sil2_di = sil3_di = typePf_ai = typePf_ao = sil3_do = 0
            sil2_di1 = sil3_di1 = typePf_ai1 = typePf_ao1 = sil3_do1 = 0
            component_C2=component_C1=0
            #Red Is
            # DI
            try:
                sil2_di = (get_int(attrs.uio_di_sil2) * 7.0)
            except:
                sil2_di = 0
            try:
                sil3_di = (get_int(attrs.uio_di_sil3) * 7.0)
            except:
                sil3_di = 0
            # AI
            try:
                typePf_ai = (get_int(attrs.uio_ai_pf)* 25.0)
            except:
                typePf_ai = 0
            # AO
            try:
                typePf_ao = (get_int(attrs.uio_ao_pf)*25.0)
            except:
                typePf_ao = 0
            # DO
            try:
                sil3_do = (get_int(attrs.uio_do_sil3)* 70.0)
            except:
                sil3_do = 0
            component_C1 = (sil2_di+sil3_di+typePf_ai+typePf_ao+sil3_do)
            if component_C1 >0:
                component_C1=component_C1+ 600.0
            # Non red IS
            # DI
            try:
                sil2_di1 = (get_int(attrs.uio_di_sil2_nr) * 7.0)
            except:
                sil2_di1 = 0
            try:
                sil3_di1 = (get_int(attrs.uio_di_sil3_nr) * 7.0)
            except:
                sil3_di1 = 0
            # AI
            try:
                typePf_ai1 = (get_int(attrs.uio_ai_pf_nr) * 25.0)
            except:
                typePf_ai1 = 0
            # AO
            try:
                typePf_ao1 = (get_int(attrs.uio_ao_pf_nr) * 25.0)
            except:
                typePf_ao1 = 0
            # DO
            try:
                sil3_do1 = (get_int(attrs.uio_do_sil3_nr) * 70.0)
            except:
                sil3_do1 = 0
            component_C2 = (sil2_di1+sil3_di1+typePf_ai1+typePf_ao1+sil3_do1)
            if component_C2 >0:
                component_C2=component_C2+ 300.0
            component_C = d.Ceiling(component_C1 + component_C2)
    elif Product.Name=="SM Remote Group":
        if Product.Attr("SM_Universal_IOTA_Type").GetValue()=="RUSIO":
            sil2_di = sil3_di = typePf_ai = typePf_ao = sil3_do = 0
            sil2_di1 = sil3_di1 = typePf_ai1 = typePf_ao1 = sil3_do1 = 0
            component_C =component_C2=component_C1=0
            #Red Is
            # DI
            try:
                sil2_di = (get_int(attrs.uio_di_sil2) * 7.0)
            except:
                sil2_di = 0
            try:
                sil3_di = (get_int(attrs.uio_di_sil3) * 7.0)
            except:
                sil3_di = 0
            # AI
            try:
                typePf_ai = (get_int(attrs.uio_ai_pf)* 25.0)
            except:
                typePf_ai = 0
            # AO
            try:
                typePf_ao = (get_int(attrs.uio_ao_pf)*25.0)
            except:
                typePf_ao = 0
            # DO
            try:
                sil3_do = (get_int(attrs.uio_do_sil3)* 70.0)
            except:
                sil3_do = 0
            component_C1 = (sil2_di+sil3_di+typePf_ai+typePf_ao+sil3_do)
            if component_C1 >0:
                component_C1=component_C1+ 600.0
            # Non red IS
            # DI
            try:
                sil2_di1 = (get_int(attrs.uio_di_sil2_nr) * 7.0)
            except:
                sil2_di1 = 0
            try:
                sil3_di1 = (get_int(attrs.uio_di_sil3_nr) * 7.0)
            except:
                sil3_di1 = 0
            # AI
            try:
                typePf_ai1 = (get_int(attrs.uio_ai_pf_nr) * 25.0)
            except:
                typePf_ai1 = 0
            # AO
            try:
                typePf_ao1 = (get_int(attrs.uio_ao_pf_nr) * 25.0)
            except:
                typePf_ao1 = 0
            # DO
            try:
                sil3_do1 = (get_int(attrs.uio_do_sil3_nr) * 70.0)
            except:
                sil3_do1 = 0
            component_C2 = (sil2_di1+sil3_di1+typePf_ai1+typePf_ao1+sil3_do1)
            if component_C2 >0:
                component_C2=component_C2+ 300.0
            component_C = d.Ceiling(component_C1 + component_C2)
    return component_C

#red=get_component_c(attrs)
#Trace.Write(red)