def setAtvQty(AttrName,Model_Number,qty):
    product_attr_val=Product.Attr(AttrName).Values
    for av in product_attr_val:
        if av.Display == Model_Number:
            if float(qty)>0:
                av.IsSelected=True
                av.Quantity=float(qty)
            else:
                av.IsSelected=False
                av.Quantity=0.0
            Trace.Write('Selected ' + Model_Number + ' in  attribute ' + AttrName + ' at Qty ' + str(qty))
            break
if Quote.GetCustomField("R2QFlag").Content=='Yes':
    lv_System_Type=Product.Attributes.GetByName("HC900_System_Type").GetValue()
    #Get Model and source of Qty mapping
    Get_Unique_Models_query = SqlHelper.GetList('select distinct Model_Number, Get_Qty_From_Col from HC900_IOCOMPONENT_IOSECTION_MAPPING')

    #Non SIL IO Section BOM - Start CXCPQ-40187
    if lv_System_Type=='Non-SIL HC900 System':
        HC900_NSIO_Cont = Product.GetContainerByName('HC900_IO_Details_of_Non-SIL')
        lv_QtySum_900U02_0100=0
        if HC900_NSIO_Cont.Rows.Count>0:
            for row in HC900_NSIO_Cont.Rows:
                Model_Number = row.GetColumnByName("Model_Number").Value
                Required_Qty= int(row.GetColumnByName("Required_Qty").Value)
                if Model_Number=='900U02-0100_dummy':
                    #Model - 900U02-0100:Qty of SIL Universal IO Module (AI/DO/DI, 4-20mA, 16 channel) + Qty of SIL Universal Analog Outputs 4-20 mA (8 channel)
                    lv_QtySum_900U02_0100=lv_QtySum_900U02_0100 + Required_Qty
                else:
                    setAtvQty('HC900_PART_SUMMARY',Model_Number,Required_Qty)
        #Setting Model - 900U02-0100
        setAtvQty('HC900_PART_SUMMARY','900U02-0100',int(lv_QtySum_900U02_0100))

        for row_1 in Get_Unique_Models_query:
            Get_IOSection_query = SqlHelper.GetList("select Model_Number, IO_Section, Get_Qty_From_Col,Multiplier from HC900_IOCOMPONENT_IOSECTION_MAPPING where Model_Number='{}' and Get_Qty_From_Col='{}'".format(row_1.Model_Number,row_1.Get_Qty_From_Col))
            if row_1.Get_Qty_From_Col=='TBEURO':
                lv_TB_EURO=0
                for row_2 in Get_IOSection_query:
                    for row_3 in HC900_NSIO_Cont.Rows:
                        if row_3.GetColumnByName("IO_Section").Value==row_2.IO_Section and int(row_3.GetColumnByName("IO_Point_Quantity").Value)>0:
                            if row_2.Get_Qty_From_Col=='TBEURO':
                                lv_TB_EURO=lv_TB_EURO+int(row_3.GetColumnByName("Euro_TB").Value) * row_2.Multiplier
                setAtvQty('HC900_PART_SUMMARY',row_1.Model_Number,lv_TB_EURO)
            if row_1.Get_Qty_From_Col=='TBBARRIER':
                lv_TB_BARRIER=0
                for row_2 in Get_IOSection_query:
                    for row_3 in HC900_NSIO_Cont.Rows:
                        if row_3.GetColumnByName("IO_Section").Value==row_2.IO_Section and int(row_3.GetColumnByName("IO_Point_Quantity").Value)>0:
                            lv_TB_BARRIER=lv_TB_BARRIER+int(row_3.GetColumnByName("Barrier_TB").Value) * row_2.Multiplier
                setAtvQty('HC900_PART_SUMMARY',row_1.Model_Number,lv_TB_BARRIER)
            if row_1.Get_Qty_From_Col=='REQ_QTY':#CXCPQ-41984 -Start
                lv_REQ_QTY=0
                for row_2 in Get_IOSection_query:
                    for row_3 in HC900_NSIO_Cont.Rows:
                        if row_3.GetColumnByName("IO_Section").Value==row_2.IO_Section and int(row_3.GetColumnByName("IO_Point_Quantity").Value)>0:
                            lv_REQ_QTY=lv_REQ_QTY+int(row_3.GetColumnByName("Required_Qty").Value) * row_2.Multiplier
                setAtvQty('HC900_PART_SUMMARY',row_1.Model_Number,lv_REQ_QTY)#CXCPQ-41984 -end
    #CXCPQ-41986 -Start
            if row_1.Get_Qty_From_Col=='RTP_1M':
                lv_RTP_1M=0
                for row_2 in Get_IOSection_query:
                    for row_3 in HC900_NSIO_Cont.Rows:
                        if row_3.GetColumnByName("IO_Section").Value==row_2.IO_Section and int(row_3.GetColumnByName("IO_Point_Quantity").Value)>0:
                            lv_RTP_1M=lv_RTP_1M+int(row_3.GetColumnByName("RTP_1_Pt_0M").Value) * row_2.Multiplier
                setAtvQty('HC900_PART_SUMMARY',row_1.Model_Number,lv_RTP_1M)

            if row_1.Get_Qty_From_Col=='RTP_2P5M':
                lv_RTP_2P5M=0
                for row_2 in Get_IOSection_query:
                    for row_3 in HC900_NSIO_Cont.Rows:
                        if row_3.GetColumnByName("IO_Section").Value==row_2.IO_Section and int(row_3.GetColumnByName("IO_Point_Quantity").Value)>0:
                            lv_RTP_2P5M=lv_RTP_2P5M+int(row_3.GetColumnByName("RTP_2_Pt_5M").Value) * row_2.Multiplier
                setAtvQty('HC900_PART_SUMMARY',row_1.Model_Number,lv_RTP_2P5M)

            if row_1.Get_Qty_From_Col=='RTP_5M':
                lv_RTP_5M=0
                for row_2 in Get_IOSection_query:
                    for row_3 in HC900_NSIO_Cont.Rows:
                        if row_3.GetColumnByName("IO_Section").Value==row_2.IO_Section and int(row_3.GetColumnByName("IO_Point_Quantity").Value)>0:
                            lv_RTP_5M=lv_RTP_5M+int(row_3.GetColumnByName("RTP_5_Pt_0M").Value) * row_2.Multiplier
                setAtvQty('HC900_PART_SUMMARY',row_1.Model_Number,lv_RTP_5M)
    #Non SIL IO Section BOM - End CXCPQ-40187

    #SIL2 Safety System IO Section BOM - Start CXCPQ-40187
    if lv_System_Type=='SIL2 Safety System':
        #SIL IO Container
        HC900_SIL_IO_Cont = Product.GetContainerByName('HC900_IO_Details_of_SIL2')
        if HC900_SIL_IO_Cont.Rows.Count>0:
            for row in HC900_SIL_IO_Cont.Rows:
                Model_Number = row.GetColumnByName("Model_Number").Value
                if row.GetColumnByName("Required_Qty").Value!='':
                    Required_Qty= int(row.GetColumnByName("Required_Qty").Value)
                else:
                    Required_Qty=0
                setAtvQty('HC900_PART_SUMMARY',Model_Number,Required_Qty)
        #SIL Additional IO Container
        HC900_AddSIL_IO_Cont = Product.GetContainerByName('HC900_Additional_IO_Details_of_SIL2')
        if HC900_AddSIL_IO_Cont.Rows.Count>0:
            lv_QtySum_900U02_0100=0
            for row in HC900_AddSIL_IO_Cont.Rows:
                Model_Number = row.GetColumnByName("Model_Number").Value
                if row.GetColumnByName("Required_Qty").Value:
                    Required_Qty= int(row.GetColumnByName("Required_Qty").Value)
                if Model_Number=='900U02-0100_dummy':
                    lv_QtySum_900U02_0100=lv_QtySum_900U02_0100 + Required_Qty
            setAtvQty('HC900_PART_SUMMARY','900U02-0100',int(lv_QtySum_900U02_0100))

        for row_1 in Get_Unique_Models_query:
            Get_IOSection_query = SqlHelper.GetList("select Model_Number, IO_Section, Get_Qty_From_Col,Multiplier from HC900_IOCOMPONENT_IOSECTION_MAPPING where Model_Number='{}' and Get_Qty_From_Col='{}'".format(row_1.Model_Number,row_1.Get_Qty_From_Col))
            if row_1.Get_Qty_From_Col=='TBEURO':
                lv_TB_EURO=0
                for row_2 in Get_IOSection_query:
                    for row_3 in HC900_SIL_IO_Cont.Rows:
                        if row_3.GetColumnByName("IO_Section").Value==row_2.IO_Section and int(row_3.GetColumnByName("IO_Point_Quantity").Value)>0:
                            if row_2.Get_Qty_From_Col=='TBEURO':
                                lv_TB_EURO=lv_TB_EURO+int(row_3.GetColumnByName("Euro_TB").Value) * row_2.Multiplier

                        if HC900_AddSIL_IO_Cont.Rows.Count>0:
                            for row_4 in HC900_AddSIL_IO_Cont.Rows:
                                if row_4.GetColumnByName("IO_Section").Value==row_2.IO_Section and int(row_4.GetColumnByName("IO_Point_Quantity").Value)>0:
                                    lv_TB_EURO=lv_TB_EURO+int(row_4.GetColumnByName("Euro_TB").Value) * row_2.Multiplier
                setAtvQty('HC900_PART_SUMMARY',row_1.Model_Number,lv_TB_EURO)
            if row_1.Get_Qty_From_Col=='TBBARRIER':
                lv_TB_BARRIER=0
                for row_2 in Get_IOSection_query:
                    for row_3 in HC900_SIL_IO_Cont.Rows:
                        if row_3.GetColumnByName("IO_Section").Value==row_2.IO_Section and int(row_3.GetColumnByName("IO_Point_Quantity").Value)>0:
                            lv_TB_BARRIER=lv_TB_BARRIER+int(row_3.GetColumnByName("Barrier_TB").Value) * row_2.Multiplier
                    if HC900_AddSIL_IO_Cont.Rows.Count>0:
                        for row_4 in HC900_AddSIL_IO_Cont.Rows:
                            if row_4.GetColumnByName("IO_Section").Value==row_2.IO_Section and int(row_4.GetColumnByName("IO_Point_Quantity").Value)>0:
                                lv_TB_BARRIER=lv_TB_BARRIER+int(row_4.GetColumnByName("Barrier_TB").Value) * row_2.Multiplier
                setAtvQty('HC900_PART_SUMMARY',row_1.Model_Number,lv_TB_BARRIER)
            if row_1.Get_Qty_From_Col=='REQ_QTY':#CXCPQ-41984 -Start
                lv_REQ_QTY=0
                for row_2 in Get_IOSection_query:
                    for row_3 in HC900_SIL_IO_Cont.Rows:
                        if row_3.GetColumnByName("IO_Section").Value==row_2.IO_Section and int(row_3.GetColumnByName("IO_Point_Quantity").Value)>0:
                            lv_REQ_QTY=lv_REQ_QTY+int(row_3.GetColumnByName("Required_Qty").Value) * row_2.Multiplier
                setAtvQty('HC900_PART_SUMMARY',row_1.Model_Number,lv_REQ_QTY)#CXCPQ-41984 -end
    #CXCPQ-41986 -Start
            if row_1.Get_Qty_From_Col=='RTP_1M':
                lv_RTP_1M=0
                for row_2 in Get_IOSection_query:
                    for row_3 in HC900_AddSIL_IO_Cont.Rows:
                        if row_3.GetColumnByName("IO_Section").Value==row_2.IO_Section and int(row_3.GetColumnByName("IO_Point_Quantity").Value)>0:
                            lv_RTP_1M=lv_RTP_1M+int(row_3.GetColumnByName("RTP_1_Pt_0M").Value) * row_2.Multiplier
                setAtvQty('HC900_PART_SUMMARY',row_1.Model_Number,lv_RTP_1M)

            if row_1.Get_Qty_From_Col=='RTP_2P5M':
                lv_RTP_2P5M=0
                for row_2 in Get_IOSection_query:
                    for row_3 in HC900_AddSIL_IO_Cont.Rows:
                        if row_3.GetColumnByName("IO_Section").Value==row_2.IO_Section and int(row_3.GetColumnByName("IO_Point_Quantity").Value)>0:
                            lv_RTP_2P5M=lv_RTP_2P5M+int(row_3.GetColumnByName("RTP_2_Pt_5M").Value) * row_2.Multiplier
                setAtvQty('HC900_PART_SUMMARY',row_1.Model_Number,lv_RTP_2P5M)

            if row_1.Get_Qty_From_Col=='RTP_5M':
                lv_RTP_5M=0
                for row_2 in Get_IOSection_query:
                    for row_3 in HC900_AddSIL_IO_Cont.Rows:
                        if row_3.GetColumnByName("IO_Section").Value==row_2.IO_Section and int(row_3.GetColumnByName("IO_Point_Quantity").Value)>0:
                            lv_RTP_5M=lv_RTP_5M+int(row_3.GetColumnByName("RTP_5_Pt_0M").Value) * row_2.Multiplier
                setAtvQty('HC900_PART_SUMMARY',row_1.Model_Number,lv_RTP_5M)
    #SIL2 Safety System IO Section BOM - End CXCPQ-40187
    #CXCPQ-40183 -Start
    lv_Redu_Rack_PS=Product.Attributes.GetByName("HC900_Redundant_I/O_Rack_Power_Supplies").GetValue()
    HC900_Rack_Cont = Product.GetContainerByName('HC900_Rack_Size_Quantity_Cont')
    if HC900_Rack_Cont.Rows.Count>0:
        for row in HC900_Rack_Cont.Rows:
            lv_Rack_Size=row.GetColumnByName("Rack Size").Value
            if row.GetColumnByName("Quantity").Value:
                lv_Quantity=float(row.GetColumnByName("Quantity").Value)
                if lv_Redu_Rack_PS=='Yes':
                    if lv_Rack_Size=='8 I/O Slot Rack':
                        setAtvQty('HC900_PART_SUMMARY','900R08R-0300',lv_Quantity)
                        setAtvQty('HC900_PART_SUMMARY','900R08-0300',0)
                    if lv_Rack_Size=='12 I/O Slot Rack':
                        setAtvQty('HC900_PART_SUMMARY','900R12R-0300',lv_Quantity)
                        setAtvQty('HC900_PART_SUMMARY','900R12-0300',0)
                    if lv_Rack_Size=='4 I/O Slot Rack':
                        setAtvQty('HC900_PART_SUMMARY','900R04-0300',0)
                if lv_Redu_Rack_PS=='No':
                    if lv_Rack_Size=='8 I/O Slot Rack':
                        setAtvQty('HC900_PART_SUMMARY','900R08R-0300',0)
                        setAtvQty('HC900_PART_SUMMARY','900R08-0300',lv_Quantity)
                    if lv_Rack_Size=='12 I/O Slot Rack':
                        setAtvQty('HC900_PART_SUMMARY','900R12R-0300',0)
                        setAtvQty('HC900_PART_SUMMARY','900R12-0300',lv_Quantity)
                    if lv_Rack_Size=='4 I/O Slot Rack':
                        setAtvQty('HC900_PART_SUMMARY','900R04-0300',lv_Quantity)
    #CXCPQ-40183 -End
    Product.ApplyRules()