def getPartQuantity(parts_dict,part):
    try:
        return int(parts_dict[part]['Quantity'])
    except KeyError:
        return 0
def roundup(n):
    res = int(n)
    return res if res == n else res+1

def get_partz(Product,parts_dict):
    if Product.Name=="SM Control Group":
        iota = Product.GetContainerByName("SM_CG_Common_Questions_Cont").Rows[0].GetColumnByName("SM_Universal_IOTA").DisplayValue
        marshaling = Product.GetContainerByName("SM_CG_Cabinet_Details_Cont_Left").Rows[0].GetColumnByName("Marshalling_Option").DisplayValue
        sic_length = Product.GetContainerByName("SM_CG_Cabinet_Details_Cont_Left").Rows[0].GetColumnByName("SIC_Length").DisplayValue
        TUIO = getPartQuantity(parts_dict,'FC-TUIO52')
        TDIO = getPartQuantity(parts_dict,'FC-TDIO52')
        TSROUNI = getPartQuantity(parts_dict,'FC-TSRO-08UNI')
        TDOL = getPartQuantity(parts_dict,'FC-TDOL-0724U')
        TSRO = getPartQuantity(parts_dict,'FC-TSRO-0824')
        
        qty = TUIO + TDIO
        qty1 = roundup(TDIO/4.5) + roundup(TDOL/3.5) + roundup((TUIO+TSROUNI)/3.0) + roundup(TSRO/2.5)
        #CXCPQ-31813
        if iota == "PUIO" and marshaling == "Hardware Marshalling with Other":
            parts_dict["4603076"] = {'Quantity' : int(qty1),'Description': 'MOB1 MOUNTING CHASSIS FTA, TERMINALS / MOB1'}
        '''#CXCPQ-31824
        if iota == "PUIO" and marshaling == "Hardware Marshalling with Other" and sic_length == "1M":
            parts_dict["FC-SIC2010"] = {'Quantity' : int(qty),'Description': 'SC SIC CABLE 2XCONNECTOR L1M / SIC2010'}
        #CXCPQ-31839
        if iota == "PUIO" and marshaling == "Hardware Marshalling with Other" and sic_length == "10M":
            parts_dict["FC-SIC2100"] = {'Quantity' : int(qty),'Description': 'SC SIC CABLE 2XCONNECTOR L10M / SIC2100'}
        #CXCPQ-31841
        if iota == "PUIO" and marshaling == "Hardware Marshalling with Other" and sic_length == "15M":
            parts_dict["FC-SIC2150"] = {'Quantity' : int(qty),'Description': 'SC SIC CABLE 2XCONNECTOR L15M / SIC2150'}'''
    elif Product.Name == "SM Remote Group":
        iota = Product.Attr("SM_Universal_IOTA_Type").GetValue()
        Enclosure_type = Product.GetContainerByName('SM_RG_ATEX Compliance_and_Enclosure_Type_Cont').Rows[0].GetColumnByName('Enclosure_Type').DisplayValue
        marshaling = Product.GetContainerByName("SM_RG_Cabinet_Details_Cont_Left").Rows[0].GetColumnByName("Marshalling_Option").DisplayValue 
        sic_length = Product.GetContainerByName("SM_RG_Cabinet_Details_Cont_Left").Rows[0].GetColumnByName("SIC_Length").DisplayValue
        Trace.Write("Enclosure_type "+str(Enclosure_type))
        Trace.Write("sic "+str(sic_length))
        Trace.Write("marshaling "+str(marshaling))
        Trace.Write("iota "+str(iota))
        TUIO = getPartQuantity(parts_dict,'FC-TUIO52')
        TDIO = getPartQuantity(parts_dict,'FC-TDIO52')
        TSROUNI = getPartQuantity(parts_dict,'FC-TSRO-08UNI')
        TDOL = getPartQuantity(parts_dict,'FC-TDOL-0724U')
        TSRO = getPartQuantity(parts_dict,'FC-TSRO-0824')

        qty = TUIO + TDIO
        qty1 = roundup(TDIO/4.5) + roundup(TDOL/3.5) + roundup((TUIO+TSROUNI)/3.0) + roundup(TSRO/2.5)
        if Enclosure_type == "Cabinet":
            #CXCPQ-31813
            if iota == "PUIO" and marshaling == "Hardware Marshalling with Other":
                parts_dict["4603076"] = {'Quantity' : int(qty1),'Description': 'MOB1 MOUNTING CHASSIS FTA, TERMINALS / MOB1'}
            '''#CXCPQ-31824
            if iota == "PUIO" and marshaling == "Hardware Marshalling with Other" and sic_length == "1M":
                parts_dict["FC-SIC2010"] = {'Quantity' : int(qty),'Description': 'SC SIC CABLE 2XCONNECTOR L1M / SIC2010'}
            #CXCPQ-31839
            if iota == "PUIO" and marshaling == "Hardware Marshalling with Other" and sic_length == "10M":
                parts_dict["FC-SIC2100"] = {'Quantity' : int(qty),'Description': 'SC SIC CABLE 2XCONNECTOR L10M / SIC2100'}
            #CXCPQ-31841
            if iota == "PUIO" and marshaling == "Hardware Marshalling with Other" and sic_length == "15M":
                parts_dict["FC-SIC2150"] = {'Quantity' : int(qty),'Description': 'SC SIC CABLE 2XCONNECTOR L15M / SIC2150'}'''

    return parts_dict