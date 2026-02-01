p_no_of_points=0
if Product.Attributes.GetByName("Exp HS Enter Number of additional Points").GetValue() !='':
    p_no_of_points=float(Product.Attributes.GetByName("Exp HS Enter Number of additional Points").GetValue())
if p_no_of_points>0:
    def setAtvQty(AttrName,Model_Number,qty):
        product_attr_val=Product.Attr(AttrName).Values
        for av in product_attr_val:
            if av.Display == Model_Number:
                if int(qty)>0:
                    av.IsSelected=True
                    av.Quantity=int(qty)
                else:
                    av.IsSelected=False
                    av.Quantity=0
                Trace.Write('Selected ' + Model_Number + ' in  attribute ' + AttrName + ' at Qty ' + str(qty))
                break
    #CXCPQ-43096
    def attribute_Qty_cal(p_no_of_points,p_redun_servers):
        Trace.Write('p_redun_servers:'+p_redun_servers)
        ret_value=0
        if p_no_of_points==16000:
            setAtvQty('Experion_HS_PART_SUMMARY','EP-HME16K',1)
            if p_redun_servers=='Yes':
                setAtvQty('Experion_HS_PART_SUMMARY','EP-HMR16K',1)                
            ret_value=0
        elif p_no_of_points>=8000 and p_no_of_points<16000:
            setAtvQty('Experion_HS_PART_SUMMARY','EP-HME08K',int(p_no_of_points/8000))
            if p_redun_servers=='Yes':
                setAtvQty('Experion_HS_PART_SUMMARY','EP-HMR08K',int(p_no_of_points/8000))
            ret_value=p_no_of_points%8000
        elif p_no_of_points>=5000 and p_no_of_points<8000:
            setAtvQty('Experion_HS_PART_SUMMARY','EP-HME05K',int(p_no_of_points/5000))
            if p_redun_servers=='Yes':
                setAtvQty('Experion_HS_PART_SUMMARY','EP-HMR05K',int(p_no_of_points/5000))
            ret_value=p_no_of_points%5000
        elif p_no_of_points>=2000 and p_no_of_points<5000:
            setAtvQty('Experion_HS_PART_SUMMARY','EP-HME02K',int(p_no_of_points/2000))
            if p_redun_servers=='Yes':
                setAtvQty('Experion_HS_PART_SUMMARY','EP-HMR02K',int(p_no_of_points/2000))
            ret_value=p_no_of_points%2000
        elif p_no_of_points>=1000 and p_no_of_points<2000:
            setAtvQty('Experion_HS_PART_SUMMARY','EP-HME01K',int(p_no_of_points/1000))
            if p_redun_servers=='Yes':
                setAtvQty('Experion_HS_PART_SUMMARY','EP-HMR01K',int(p_no_of_points/1000))
            ret_value=p_no_of_points%1000
        elif p_no_of_points>=1 and p_no_of_points<1000:
            if p_no_of_points%100>0:
                setAtvQty('Experion_HS_PART_SUMMARY','EP-HME100',1+int(p_no_of_points/100))
                if p_redun_servers=='Yes':
                    setAtvQty('Experion_HS_PART_SUMMARY','EP-HMR100',1+int(p_no_of_points/100))
            else:
                setAtvQty('Experion_HS_PART_SUMMARY','EP-HME100',int(p_no_of_points/100))
                if p_redun_servers=='Yes':
                    setAtvQty('Experion_HS_PART_SUMMARY','EP-HMR100',int(p_no_of_points/100))
            ret_value=0
        return ret_value

    lv_Pointer_Modes=['EP-HME100','EP-HME01K','EP-HME02K','EP-HME05K','EP-HME08K','EP-HME16K','EP-HMR100','EP-HMR01K','EP-HMR02K','EP-HMR05K','EP-HMR08K','EP-HMR16K']
    #Reset Models
    for i in lv_Pointer_Modes:
        setAtvQty('Experion_HS_PART_SUMMARY',i,0)

    p_no_of_points=float(Product.Attributes.GetByName("Exp HS Enter Number of additional Points").GetValue())
    p_redun_servers=Product.Attributes.GetByName("Exp HS Redundant Servers").GetValue()

    Trace.Write('p_no_of_points:'+ str(p_no_of_points))
    #set Models
    while True:
        i=attribute_Qty_cal(p_no_of_points,p_redun_servers)
        if i>0:
            p_no_of_points=i
        else:
            break
    #Load models to container in rules
    Product.ApplyRules()