p_no_of_points=0
if Product.Attributes.GetByName("MIQ_Total_Points_Required").GetValue() !='':
    p_no_of_points=float(Product.Attributes.GetByName("MIQ_Total_Points_Required").GetValue())

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
    def attribute_Qty_cal(p_curr_points):
        lv_rem=0
    
        if p_curr_points>8201:
            if p_curr_points<=16000:
                lv_rem=1
                p_curr_points=0
            else:
                lv_rem=int(p_curr_points/16000)
                p_curr_points=p_no_of_points-(lv_rem*16000)  
            setAtvQty('MIQ_PART_SUMMARY','EP-HME16K',lv_rem)                
        elif p_curr_points>5401:
            if p_curr_points<=8000:
                lv_rem=1
                p_curr_points=0
            else:
                lv_rem=int(p_curr_points/8000)
                p_curr_points=p_no_of_points-(lv_rem*8000)
            setAtvQty('MIQ_PART_SUMMARY','EP-HME08K',lv_rem)
  
        elif p_curr_points>2000:
            if p_curr_points<=5000:
                lv_rem=1                
                p_curr_points=0
            else:
                lv_rem=int(p_curr_points/5000)
                p_curr_points=p_no_of_points-(lv_rem*5000)
            setAtvQty('MIQ_PART_SUMMARY','EP-HME05K',lv_rem)
        elif p_curr_points>1000:
            if p_curr_points<=2000:
                lv_rem=1
                p_curr_points=0
            else:
                lv_rem=int(p_curr_points/2000)
                p_curr_points=p_no_of_points-(lv_rem*2000)
            setAtvQty('MIQ_PART_SUMMARY','EP-HME02K',lv_rem)
        elif p_curr_points>701:
            if p_curr_points<=1000:
                lv_rem=1
                p_curr_points=0                
            else:
                lv_rem=int(p_curr_points/1000)
                p_curr_points=p_no_of_points-(lv_rem*1000)
            setAtvQty('MIQ_PART_SUMMARY','EP-HME01K',lv_rem)

        elif p_curr_points>=1 and p_curr_points<=701:
            if p_curr_points%100>0:
                setAtvQty('MIQ_PART_SUMMARY','EP-HME100',1+int(p_curr_points/100))
            else:
                setAtvQty('MIQ_PART_SUMMARY','EP-HME100',int(p_curr_points/100))
            p_curr_points=0

        return p_curr_points


    lv_Pointer_Models=['EP-HME16K','EP-HME08K','EP-HME05K','EP-HME02K','EP-HME01K','EP-HME100']
    #Reset Models
    for i in lv_Pointer_Models:
        setAtvQty('MIQ_PART_SUMMARY',i,0)

    p_curr_points=p_no_of_points
    Trace.Write('p_no_of_points:'+ str(p_no_of_points))
    #set Models
    while True:
        i=attribute_Qty_cal(p_curr_points)
        if i>0:
            p_curr_points=i
        else:
            break
    #Load models to container in rules
    Product.ApplyRules()