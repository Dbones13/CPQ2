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

#Trace.Write("outside if")
if measuremment:
    sensor = Product.Attr("MX_SE_Sensor_Type").GetValue()
    #Trace.Write("above query")
    if scanner == "Q4000-80 O-Frame" and measuremment in ("Gloss","Color","Caliper","Ash","Moisture","Basis Weight","Infrarred"):
        qkit = Product.Attr("MX_SE_Is Q_Kit_required").GetValue()
        if qkit != '':
            queryData_qkit = SqlHelper.GetFirst("select Part_number,Qty from Exp_MX_Sensor_BOM where MX_SG_Type_of_Scanner = '{}'and MX_SE_Measurement_Type = '{}'and MX_SE_Is_Q_Kit_required = '{}' ".format(scanner,measuremment,qkit))

            if queryData_qkit is not None:
                setAtvQty('Scanner_sensor_bom_parts',queryData_qkit.Part_number,queryData_qkit.Qty)

    if scanner != '' and measuremment != '' and sensor != '':
        #Trace.Write(scanner+" "+measuremment+" "+sensor)
        queryData = SqlHelper.GetFirst("select Part_number,Qty from Exp_MX_Sensor_BOM where MX_SG_Type_of_Scanner = '{}'and MX_SE_Measurement_Type = '{}'and MX_SE_Sensor_Type = '{}' ".format(scanner,measuremment,sensor))

        if queryData is not None:
            #Trace.Write(queryData.Part_number+" "+str(queryData.Qty))
            setAtvQty('Scanner_sensor_bom_parts',queryData.Part_number,queryData.Qty)

Product.ApplyRules()