def setAtvQty(AttrName,sv,qty):
    pvs=Product.Attr(AttrName).Values
    for av in pvs:
        if av.Display == sv:
            av.IsSelected=True
            av.Quantity=qty
            break

def resetAtvQty(AttrName):
    pvs=Product.Attr(AttrName).Values
    for av in pvs:
        av.IsSelected=False
        av.Quantity=0

measuremment = Product.Attr("MX_SE_Measurement_Type").GetValue()
scanner = Product.Attr("MX_SG_Type_of_Scanner").GetValue()
#Product.ResetAttr('Scanner_sensor_bom_parts')
resetAtvQty('Scanner_sensor_bom_parts')

if measuremment:
    sensor = Product.Attr("MX_SE_Sensor_Type").GetValue()
    if scanner != '' and measuremment != '' and sensor != '':
        #Trace.Write(scanner+" "+measuremment+" "+sensor)
        queryData = SqlHelper.GetFirst("select Part_number,Qty from Exp_MX_Sensor_BOM where MX_SG_Type_of_Scanner = '{}'and MX_SE_Measurement_Type = '{}'and MX_SE_Sensor_Type = '{}' ".format(scanner,measuremment,sensor))
        if queryData is not None:
            #Trace.Write(queryData.Part_number+" "+str(queryData.Qty))
            setAtvQty('Scanner_sensor_bom_parts',queryData.Part_number,queryData.Qty)