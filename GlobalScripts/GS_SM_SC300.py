import System.Decimal as D
def get_int(n):
    return int(n) if n else 0

def roundup(n):
    res = int(n)
    return res if res == n else res+1

def get_thing(n):
    if n != "":
        n = int(float(n))
    else:
        n = 0
    return n

def get_TCNT(Product, parts_dict):
    IO=IOTA=0
    contrl_arc = Product.GetContainerByName("SM_CG_Common_Questions_Cont").Rows[0].GetColumnByName("SM_SCController_Architecture")
    iota = Product.GetContainerByName("SM_CG_Common_Questions_Cont").Rows[0].GetColumnByName("SM_Universal_IOTA")
    ##<--- IOM --->
    #CXCPQ-31134
    PUIO = get_thing(Product.Attr('FC_PUIO').GetValue())
    Trace.Write('FC_PUIO'+str(PUIO))
    #CXCPQ-31136
    PDIO = get_thing(Product.Attr('FC_PDIO').GetValue())
    Trace.Write('FC_PDIO'+str(PDIO))
    #CXCPQ-31172
    RUSIO = get_thing(Product.Attr('FC_RUSIO').GetValue())
    Trace.Write('FC_RUSIO'+str(RUSIO))
    ##<--- IOTA --->
    #CXCPQ-31139
    TUIO = get_thing(Product.Attr('FC_TUIO').GetValue())
    Trace.Write('FC_TUIO'+str(TUIO))
    #CXCPQ-31140
    TDIO = get_thing(Product.Attr('FC_TDIO').GetValue())
    Trace.Write("Tduio: "+str(TDIO))
    #CXCPQ-31173
    IOTANR = get_thing(Product.Attr('Rusio_IotaNR').GetValue())
    Trace.Write('Rusio_IotaNR:'+str(IOTANR))
    #CXCPQ-31174
    IOTAR = get_thing(Product.Attr('Rusio_IotaR').GetValue())
    Trace.Write('Rusio_IotaR:'+str(IOTAR))
    
    if contrl_arc.Value == "Redundant":
        #IO points
        IOpts = PUIO + PDIO + RUSIO
        Trace.Write("IOpts : "+str(IOpts))
        if IOpts == 0:
            IO = 0
            Trace.Write("IO: "+str(IO))
        elif IOpts > 1984:
            IO = roundup(IOpts/1984.0)
            Trace.Write("IO: "+str(IO))
        else:
            IO = 1
            Trace.Write("IO: "+str(IO))

        #IOTA
        Trace.Write("R: "+str(IOTAR))
        Trace.Write("NR: "+str(IOTANR))
        Trace.Write("TUIO: "+str(TUIO))
        Trace.Write("TDIO: "+str(TDIO))
        IOMS = IOTANR + IOTAR + TUIO + TDIO

        Trace.Write("IOMS : "+str(IOMS))
        if IOMS == 0:
            IOTA = 0
            Trace.Write("IOTA: "+str(IOTA))
        elif IOMS > 62:
            IOTA = roundup(IOMS/62.0)
            Trace.Write("IOTA: "+str(IOTA))
        else:
            IOTA = 1
            Trace.Write("IOTA: "+str(IOTA))
        qty = max(IO,IOTA)
        Trace.Write("FC-TCNT1_A_QT:"+str(qty))
        parts_dict["FC-TCNT11"] = {'Quantity' : int(qty), 'Description': 'SC S300 IOTA CNTRL REDUNDANT'}
    
    if contrl_arc.Value == "Redundant_ART":
        #IO points
        IOpts = PUIO + PDIO + RUSIO
        Trace.Write("IOpts : "+str(IOpts))
        if IOpts == 0:
            IO = 0
            Trace.Write("IO: "+str(IO))
        elif IOpts > 896:
            IO = roundup(IOpts/896.0)
            Trace.Write("IO: "+str(IO))
        else:
            IO = 1
            Trace.Write("IO: "+str(IO))

        #IOTA
        Trace.Write("R: "+str(IOTAR))
        Trace.Write("NR: "+str(IOTANR))
        Trace.Write("TUIO: "+str(TUIO))
        Trace.Write("TDIO: "+str(TDIO))
        IOMS = IOTANR + IOTAR + TUIO + TDIO

        Trace.Write("IOMS : "+str(IOMS))
        if IOMS == 0:
            IOTA = 0
            Trace.Write("IOTA: "+str(IOTA))
        elif IOMS > 28:
            IOTA = roundup(IOMS/28.0)
            Trace.Write("IOTA: "+str(IOTA))
        else:
            IOTA = 1
            Trace.Write("IOTA: "+str(IOTA))
        qty = max(IO,IOTA)
        Trace.Write("FC-TCNT1_B_QT:"+str(qty))
        parts_dict["FC-TCNT11"] = {'Quantity' : int(qty), 'Description': 'SC S300 IOTA CNTRL REDUNDANT'}
    if contrl_arc.Value == "Redundant":
        rg_count = 1
        remote_groups = Product.GetContainerByName('SM_RemoteGroup_Cont').Rows
        for rgs in remote_groups:
            #Remote groups
            rg_product = rgs.Product
            Trace.Write(rg_product.Name)
            #CXCPQ-31134
            PUIO_rg = get_thing(rg_product.Attr('FC_RG_PUIO').GetValue())
            Trace.Write("Rg_"+"PUIO_"+str(PUIO_rg))
            #CXCPQ-31136
            PDIO_rg = get_thing(rg_product.Attr('FC_RG_PDIO').GetValue())
            Trace.Write("Rg_"+"PDIO_"+str(PDIO_rg))
            #CXCPQ-31172
            RUSIO_rg = get_thing(rg_product.Attr('FC_RG_RUSIO').GetValue())
            Trace.Write("Rg_"+"RUSIO_"+str(RUSIO_rg))
            #RUSIO_rg = 0
            
            #CXCPQ-31134
            TUIO_rg = get_thing(rg_product.Attr('FC_RG_TUIO').GetValue())
            Trace.Write("Rg_"+"TUIO_"+str(TUIO_rg))
            #CXCPQ-31136
            TDIO_rg = get_thing(rg_product.Attr('FC_RG_TDIO').GetValue())
            Trace.Write("Rg_"+"TDIO_"+str(TDIO_rg))
            #CXCPQ-31173
            IOTANR_rg = get_thing(rg_product.Attr('RUSIO_RG_IOTANR').GetValue())
            Trace.Write("Rg_"+"IOTANR_"+str(IOTANR_rg))
            #CXCPQ-31174
            IOTAR_rg = get_thing(rg_product.Attr('RUSIO_RG_IOTAR').GetValue())
            Trace.Write("Rg_"+"IOTAR_"+str(IOTAR_rg))
            if PUIO_rg:
                #rg_count+=1
                PUIO+=PUIO_rg
                Trace.Write("PUIO_"+str(PUIO))
            if PDIO_rg:
                #rg_count+=1
                PDIO+=PDIO_rg
                Trace.Write("PDIO_"+str(PDIO))
            if RUSIO_rg:
                #rg_count+=1
                RUSIO+=RUSIO_rg
                Trace.Write("RUSIO_"+str(RUSIO))
                
            if TUIO_rg:
                #rg_count+=1
                TUIO+=TUIO_rg
                Trace.Write("TUIO_"+str(TUIO))
            if TDIO_rg:
                #rg_count+=1
                TDIO+=TDIO_rg
                Trace.Write("TDIO_"+str(TDIO))
            if IOTANR_rg:
                #rg_count+=1
                IOTANR+=IOTANR_rg
                Trace.Write("IOTANR_"+str(PDIO))
            if IOTAR_rg:
                #rg_count+=1
                IOTAR+=IOTAR_rg
                Trace.Write("IOTAR_"+str(IOTAR))
            #IO points
            IOpts = PUIO + PDIO + RUSIO
            Trace.Write("IOpts : "+str(IOpts))
            if IOpts == 0:
                IO = 0
                Trace.Write("IO: "+str(IO))
            elif IOpts > 1984:
                IO = roundup(IOpts/1984.0)
                Trace.Write("IO: "+str(IO))
            else:
                IO = 1
                Trace.Write("IO: "+str(IO))
                
            #IOTA
            Trace.Write("R: "+str(IOTAR))
            Trace.Write("NR: "+str(IOTANR))
            Trace.Write("TUIO: "+str(TUIO))
            Trace.Write("TDIO: "+str(TDIO))
            IOMS = IOTANR + IOTAR + TUIO + TDIO
            
            Trace.Write("IOMS : "+str(IOMS))
            if IOMS == 0:
                IOTA = 0
                Trace.Write("IOTA: "+str(IOTA))
            elif IOMS > 62:
                IOTA = roundup(IOMS/62.0)
                Trace.Write("IOTA: "+str(IOTA))
            else:
                IOTA = 1
                Trace.Write("IOTA: "+str(IOTA))
        qty = max(IO,IOTA)
        Trace.Write("FC-TCNT11_C-_QT:"+str(qty))
        parts_dict["FC-TCNT11"] = {'Quantity' : int(qty), 'Description': 'SC S300 IOTA CNTRL REDUNDANT'}

    elif contrl_arc.Value == "Redundant_ART":
        rg_count = 1
        remote_groups = Product.GetContainerByName('SM_RemoteGroup_Cont').Rows
        for rgs in remote_groups:
            #Remote groups
            rg_product = rgs.Product
            Trace.Write(rg_product.Name)
            #CXCPQ-31134
            PUIO_rg = get_thing(rg_product.Attr('FC_RG_PUIO').GetValue())
            #CXCPQ-31136
            PDIO_rg = get_thing(rg_product.Attr('FC_RG_PDIO').GetValue())
            #CXCPQ-31172
            RUSIO_rg = get_thing(rg_product.Attr('FC_RG_RUSIO').GetValue())
            
            #CXCPQ-31134
            TUIO_rg = get_thing(rg_product.Attr('FC_RG_TUIO').GetValue())
            #CXCPQ-31136
            TDIO_rg = get_thing(rg_product.Attr('FC_RG_TDIO').GetValue())
            #CXCPQ-31173
            IOTANR_rg = get_thing(rg_product.Attr('RUSIO_RG_IOTANR').GetValue())
            #CXCPQ-31174
            IOTAR_rg = get_thing(rg_product.Attr('RUSIO_RG_IOTAR').GetValue())
            if PUIO_rg:
                #rg_count+=1
                PUIO+=PUIO_rg
                Trace.Write("PUIO_"+str(PUIO))
            if PDIO_rg:
                #rg_count+=1
                PDIO+=PDIO_rg
                Trace.Write("PDIO_"+str(PDIO))
            if RUSIO_rg:
                #rg_count+=1
                RUSIO+=RUSIO_rg
                Trace.Write("RUSIO_"+str(RUSIO))
                
            if TUIO_rg:
                #rg_count+=1
                TUIO+=TUIO_rg
                Trace.Write("TUIO_"+str(TUIO))
            if TDIO_rg:
                #rg_count+=1
                TDIO+=TDIO_rg
                Trace.Write("TDIO_"+str(TDIO))
            if IOTANR_rg:
                #rg_count+=1
                IOTANR+=IOTANR_rg
                Trace.Write("IOTANR_"+str(PDIO))
            if IOTAR_rg:
                #rg_count+=1
                IOTAR+=IOTAR_rg
                Trace.Write("IOTAR_"+str(IOTAR))
            #IO points
            IOpts = PUIO + PDIO + RUSIO
            Trace.Write("ART IOpts : "+str(IOpts))
            if IOpts == 0:
                IO = 0
                Trace.Write("ART IO: "+str(IO))
            elif IOpts > 896:
                IO = roundup(IOpts/896.0)
                Trace.Write("ART IO: "+str(IO))
            else:
                IO = 1
                Trace.Write("ART IO: "+str(IO))
                
            #IOTA
            IOMS = IOTANR + IOTAR + TUIO + TDIO
            Trace.Write("ART IOMS : "+str(IOMS))
            if IOMS == 0:
                IOTA = 0
                Trace.Write("ART IOTA: "+str(IOTA))
            elif IOMS > 28:
                IOTA = roundup(IOMS/28.0)
                Trace.Write("ART IOTA: "+str(IOTA))
            else:
                IOTA = 1
                Trace.Write("ART IOTA: "+str(IOTA))
        qty = max(IO,IOTA)
        Trace.Write("FC-TCNT11_D__QT:"+str(qty))
        parts_dict["FC-TCNT11"] = {'Quantity' : int(qty), 'Description': 'SC S300 IOTA CNTRL REDUNDANT'}
    return parts_dict, qty
#test,qty = get_TCNT(Product, {})
#Trace.Write(str(test))