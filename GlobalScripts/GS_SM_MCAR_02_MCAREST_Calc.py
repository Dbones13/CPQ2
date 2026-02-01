#CXCPQ-31169
import GS_SM_SUMRIONIS_Calc
import GS_SM_SUMRIORIS_Calcs
import GS_SM_CG_Component_Attribute
import GS_SMIOComponents
import GS_SM_CG_UIO_CALC
import System.Decimal as D
def MCAR_02_MCAREST_Calc(Product):
    #Control Group
    cg_count = 1
    control_groups = Product.GetContainerByName('SM_ControlGroup_Cont').Rows
    mcarest = dict()
    for cgs in control_groups:
        cg_product = cgs.Product
        Trace.Write(cg_product.Name)
        iocomp_rion = GS_SMIOComponents.IOComponents(cg_product)
        iocomp_rioris = GS_SM_SUMRIORIS_Calcs.IOComponents(cg_product)
        sumrion = iocomp_rion.getSumRion()
        sumrionis = GS_SM_SUMRIONIS_Calc.SUMRIONIS_Calc(cg_product)
        Trace.Write("CG - sumrion = "+str(sumrion))
        Trace.Write("CG - sumrionis = "+str(sumrionis))
        try:
            attrs = GS_SM_CG_Component_Attribute.AttrStorage(cg_product)
        except Exception,e:
            attrs = None
            Trace.Write("Error when Reading SM CG System Attributes: " + str(e))
        try:
            IOComp = GS_SMIOComponents.IOComponents(cg_product)
            SUMUIONPF, SUMUIORPF = IOComp.getUniversalIOCountRedNonRed()
        except Exception,e:
            SUMUIORPF = 0
            SUMUIONPF = 0
            Trace.Write("Error in SUMUIORPF & SUMUIONPF Calc: " + str(e))
        if attrs:
            try:
                sumrior = GS_SM_CG_UIO_CALC.get_sum_red_io(attrs, SUMUIORPF)
            except Exception,e:
                sumrior = 0
                Trace.Write("Error in GS_SM_CG_UIO_CALC: " + str(e) )
        Trace.Write("CG - sumrior = "+str(sumrior))
        sumrioris = iocomp_rioris.SUMRIORIS_value()
        Trace.Write("CG - sumrioris = "+str(sumrioris))
        mcarest_tmp = 0.0
        mcarest_tmp = D.Ceiling(D.Ceiling(((D.Ceiling((sumrion/float(32))) + D.Ceiling((sumrionis/float(32))))/float(3))) + D.Ceiling(((D.Ceiling((sumrior/float(32))) + D.Ceiling((sumrioris/float(32))))/float(2))))
        mcarest[str('mcarest_cg_' + str(cg_count))] = str(mcarest_tmp)
        rg_count = 1
        remote_groups = cg_product.GetContainerByName('SM_RemoteGroup_Cont').Rows
        for rgs in remote_groups:
            rg_product = rgs.Product
            Trace.Write(rg_product.Name)
            iocomp_rion = GS_SMIOComponents.IOComponents(rg_product)
            iocomp_rioris = GS_SM_SUMRIORIS_Calcs.IOComponents(rg_product)
            sumrion = iocomp_rion.getSumRion()
            sumrionis = GS_SM_SUMRIONIS_Calc.SUMRIONIS_Calc(rg_product)
            Trace.Write("RG - sumrion = "+str(sumrion))
            Trace.Write("RG - sumrionis = "+str(sumrionis))
            
            try:
                attrs = GS_SM_CG_Component_Attribute.AttrStorage(rg_product)
            except Exception,e:
                attrs = None
                Trace.Write("Error when Reading SM CG System Attributes: " + str(e))
            try:
                IOComp = GS_SMIOComponents.IOComponents(rg_product)
                SUMUIONPF, SUMUIORPF = IOComp.getUniversalIOCountRedNonRed()
            except Exception,e:
                SUMUIORPF = 0
                SUMUIONPF = 0
                Trace.Write("Error in SUMUIORPF & SUMUIONPF Calc: " + str(e))
            if attrs:
                try:
                    sumrior = GS_SM_CG_UIO_CALC.get_sum_red_io(attrs, SUMUIORPF)
                except Exception,e:
                    sumrior = 0
                    Trace.Write("Error in GS_SM_CG_UIO_CALC: " + str(e))
            
            Trace.Write("RG - sumrior = "+str(sumrior))
            sumrioris = iocomp_rioris.SUMRIORIS_value()
            Trace.Write("RG - sumrioris = "+str(sumrioris))
            mcarest_tmp = 0.0
            mcarest_tmp = D.Ceiling(D.Ceiling(((D.Ceiling((sumrion/float(32))) + D.Ceiling((sumrionis/float(32))))/float(3))) + D.Ceiling(((D.Ceiling((sumrior/float(32))) + D.Ceiling((sumrioris/float(32))))/float(2))))
            mcarest[str('mcarest_cg_' + str(cg_count)+'_rg_'+str(rg_count))] = str(mcarest_tmp)
            rg_count+=1
        cg_count+=1
    return mcarest
    
def MCAR_02_MCAREST_CG_RG_Calc(Product):
    Trace.Write("Product = "+Product.Name)
    if Product.Name=="SM Control Group":
        iota_type = ''
        if Product.GetContainerByName('SM_CG_Common_Questions_Cont').Rows.Count > 0:
            iota_type = Product.GetContainerByName('SM_CG_Common_Questions_Cont').Rows[0].GetColumnByName("SM_Universal_IOTA").Value
        if iota_type != 'RUSIO':
            Trace.Write("Universal IOTA is not RUSIO. Returning 0")
            return 0
    elif Product.Name=="SM Remote Group":
        iota_type = Product.Attr('SM_Universal_IOTA_Type').GetValue()
        if iota_type != 'RUSIO':
            Trace.Write("Universal IOTA is not RUSIO. Returning 0")
            return 0
    else:
        Trace.Write("Product is neither CG nor RG")
        return 0
    iocomp_rion = GS_SMIOComponents.IOComponents(Product)
    iocomp_rioris = GS_SM_SUMRIORIS_Calcs.IOComponents(Product)
    sumrion = iocomp_rion.getSumRion()
    sumrionis = GS_SM_SUMRIONIS_Calc.SUMRIONIS_Calc(Product)
    Trace.Write("sumrion = "+str(sumrion))
    Trace.Write("sumrionis = "+str(sumrionis))
    try:
        attrs = GS_SM_CG_Component_Attribute.AttrStorage(Product)
    except Exception,e:
        attrs = None
        Trace.Write("Error when Reading SM CG System Attributes: " + str(e))
    try:
        IOComp = GS_SMIOComponents.IOComponents(Product)
        SUMUIONPF, SUMUIORPF = IOComp.getUniversalIOCountRedNonRed()
    except Exception,e:
        SUMUIORPF = 0
        SUMUIONPF = 0
        Trace.Write("Error in SUMUIORPF & SUMUIONPF Calc: " + str(e))
    if attrs:
        try:
            sumrior = GS_SM_CG_UIO_CALC.get_sum_red_io(attrs, SUMUIORPF)
        except Exception,e:
            sumrior = 0
            Trace.Write("Error in GS_SM_CG_UIO_CALC: " + str(e))
    Trace.Write("sumrior = "+str(sumrior))
    sumrioris = iocomp_rioris.SUMRIORIS_value()
    Trace.Write("sumrioris = "+str(sumrioris))
    mcarest = 0.0
    mcarest= D.Ceiling(D.Ceiling(((D.Ceiling((sumrion/float(32))) + D.Ceiling((sumrionis/float(32))))/float(3))) + D.Ceiling(((D.Ceiling((sumrior/float(32))) + D.Ceiling((sumrioris/float(32))))/float(2))))
    return mcarest

#Trace.Write("mcarest = "+str(MCAR_02_MCAREST_CG_RG_Calc(Product)))