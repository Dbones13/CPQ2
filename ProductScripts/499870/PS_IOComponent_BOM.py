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

lv_System_Type=Product.Attributes.GetByName("HC900_System_Type").GetValue()
#Get Model and source of Qty mapping
Get_Unique_Models_query = SqlHelper.GetList('select distinct Model_Number, Get_Qty_From_Col from HC900_IOCOMPONENT_IOSECTION_MAPPING')

#Non SIL IO Section components BOM - Start CXCPQ-41981
if lv_System_Type=='Non-SIL HC900 System':
    HC900_NSIO_Cont = Product.GetContainerByName('HC900_IO_Details_of_Non-SIL')

    for row_1 in Get_Unique_Models_query:
        Get_IOSection_query = SqlHelper.GetList("select Model_Number, IO_Section, Get_Qty_From_Col,Multiplier from HC900_IOCOMPONENT_IOSECTION_MAPPING where Model_Number='{}' and Get_Qty_From_Col='{}'".format(row_1.Model_Number,row_1.Get_Qty_From_Col))
        if row_1.Get_Qty_From_Col=='TBEURO':
            lv_TB_EURO=0
            for row_2 in Get_IOSection_query:
                for row_3 in HC900_NSIO_Cont.Rows:
                    if row_3.GetColumnByName("IO_Section").Value==row_2.IO_Section and int(row_3.GetColumnByName("IO_Point_Quantity").Value)>0:
                        if row_2.Get_Qty_From_Col=='TBEURO':
                            lv_TB_EURO=lv_TB_EURO+int(row_3.GetColumnByName("Euro_TB").Value) * row_2.Multiplier
            Trace.Write('lv_TB_EURO:'+str(lv_TB_EURO))
            setAtvQty('HC900_PART_SUMMARY',row_1.Model_Number,lv_TB_EURO)
        if row_1.Get_Qty_From_Col=='TBBARRIER':
            lv_TB_BARRIER=0
            for row_2 in Get_IOSection_query:
                for row_3 in HC900_NSIO_Cont.Rows:
                    if row_3.GetColumnByName("IO_Section").Value==row_2.IO_Section and int(row_3.GetColumnByName("IO_Point_Quantity").Value)>0:
                        lv_TB_BARRIER=lv_TB_BARRIER+int(row_3.GetColumnByName("Barrier_TB").Value) * row_2.Multiplier
            Trace.Write('lv_TB_BARRIER:'+str(lv_TB_BARRIER))
            setAtvQty('HC900_PART_SUMMARY',row_1.Model_Number,lv_TB_BARRIER)
        if row_1.Get_Qty_From_Col=='REQ_QTY':#CXCPQ-41984 -Start
            lv_REQ_QTY=0
            for row_2 in Get_IOSection_query:
                for row_3 in HC900_NSIO_Cont.Rows:
                    if row_3.GetColumnByName("IO_Section").Value==row_2.IO_Section and int(row_3.GetColumnByName("IO_Point_Quantity").Value)>0:
                        lv_REQ_QTY=lv_REQ_QTY+int(row_3.GetColumnByName("Required_Qty").Value) * row_2.Multiplier
            Trace.Write('lv_REQ_QTY:'+str(lv_REQ_QTY))
            setAtvQty('HC900_PART_SUMMARY',row_1.Model_Number,lv_REQ_QTY)#CXCPQ-41984 -end
#CXCPQ-41986 -Start
        if row_1.Get_Qty_From_Col=='RTP_1M':
            lv_RTP_1M=0
            for row_2 in Get_IOSection_query:
                for row_3 in HC900_NSIO_Cont.Rows:
                    if row_3.GetColumnByName("IO_Section").Value==row_2.IO_Section and int(row_3.GetColumnByName("IO_Point_Quantity").Value)>0:
                        lv_RTP_1M=lv_RTP_1M+int(row_3.GetColumnByName("RTP_1_Pt_0M").Value) * row_2.Multiplier
            Trace.Write('lv_RTP_1M:'+str(lv_RTP_1M))
            setAtvQty('HC900_PART_SUMMARY',row_1.Model_Number,lv_RTP_1M)

        if row_1.Get_Qty_From_Col=='RTP_2P5M':
            lv_RTP_2P5M=0
            for row_2 in Get_IOSection_query:
                for row_3 in HC900_NSIO_Cont.Rows:
                    if row_3.GetColumnByName("IO_Section").Value==row_2.IO_Section and int(row_3.GetColumnByName("IO_Point_Quantity").Value)>0:
                        lv_RTP_2P5M=lv_RTP_2P5M+int(row_3.GetColumnByName("RTP_2_Pt_5M").Value) * row_2.Multiplier
            Trace.Write('lv_RTP_2P5M:'+str(lv_RTP_2P5M))
            setAtvQty('HC900_PART_SUMMARY',row_1.Model_Number,lv_RTP_2P5M)

        if row_1.Get_Qty_From_Col=='RTP_5M':
            lv_RTP_5M=0
            for row_2 in Get_IOSection_query:
                for row_3 in HC900_NSIO_Cont.Rows:
                    if row_3.GetColumnByName("IO_Section").Value==row_2.IO_Section and int(row_3.GetColumnByName("IO_Point_Quantity").Value)>0:
                        lv_RTP_5M=lv_RTP_5M+int(row_3.GetColumnByName("RTP_5_Pt_0M").Value) * row_2.Multiplier
            Trace.Write('lv_RTP_5M:'+str(lv_RTP_5M))
            setAtvQty('HC900_PART_SUMMARY',row_1.Model_Number,lv_RTP_5M)
#End-CXCPQ-41986
#End of Non SIL IO Section components BOM - CXCPQ-41981

#SIL2 Safety System IO Section components BOM - Start CXCPQ-41981
if lv_System_Type=='SIL2 Safety System':
    HC900_SIL_IO_Cont = Product.GetContainerByName('HC900_IO_Details_of_SIL2')
    HC900_AddSIL_IO_Cont = Product.GetContainerByName('HC900_Additional_IO_Details_of_SIL2')

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
            Trace.Write('lv_TB_EURO:'+str(lv_TB_EURO))
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
            Trace.Write('lv_TB_BARRIER:'+str(lv_TB_BARRIER))
            setAtvQty('HC900_PART_SUMMARY',row_1.Model_Number,lv_TB_BARRIER)
        if row_1.Get_Qty_From_Col=='REQ_QTY':#CXCPQ-41984 -Start
            lv_REQ_QTY=0
            for row_2 in Get_IOSection_query:
                for row_3 in HC900_SIL_IO_Cont.Rows:
                    if row_3.GetColumnByName("IO_Section").Value==row_2.IO_Section and int(row_3.GetColumnByName("IO_Point_Quantity").Value)>0:
                        lv_REQ_QTY=lv_REQ_QTY+int(row_3.GetColumnByName("Required_Qty").Value) * row_2.Multiplier
            Trace.Write('lv_REQ_QTY:'+str(lv_REQ_QTY))
            setAtvQty('HC900_PART_SUMMARY',row_1.Model_Number,lv_REQ_QTY)#CXCPQ-41984 -end
#CXCPQ-41986 -Start
        if row_1.Get_Qty_From_Col=='RTP_1M':
            lv_RTP_1M=0
            for row_2 in Get_IOSection_query:
                for row_3 in HC900_AddSIL_IO_Cont.Rows:
                    if row_3.GetColumnByName("IO_Section").Value==row_2.IO_Section and int(row_3.GetColumnByName("IO_Point_Quantity").Value)>0:
                        lv_RTP_1M=lv_RTP_1M+int(row_3.GetColumnByName("RTP_1_Pt_0M").Value) * row_2.Multiplier
            Trace.Write('lv_RTP_1M:'+str(lv_RTP_1M))
            setAtvQty('HC900_PART_SUMMARY',row_1.Model_Number,lv_RTP_1M)

        if row_1.Get_Qty_From_Col=='RTP_2P5M':
            lv_RTP_2P5M=0
            for row_2 in Get_IOSection_query:
                for row_3 in HC900_AddSIL_IO_Cont.Rows:
                    if row_3.GetColumnByName("IO_Section").Value==row_2.IO_Section and int(row_3.GetColumnByName("IO_Point_Quantity").Value)>0:
                        lv_RTP_2P5M=lv_RTP_2P5M+int(row_3.GetColumnByName("RTP_2_Pt_5M").Value) * row_2.Multiplier
            Trace.Write('lv_RTP_2P5M:'+str(lv_RTP_2P5M))
            setAtvQty('HC900_PART_SUMMARY',row_1.Model_Number,lv_RTP_2P5M)

        if row_1.Get_Qty_From_Col=='RTP_5M':
            lv_RTP_5M=0
            for row_2 in Get_IOSection_query:
                for row_3 in HC900_AddSIL_IO_Cont.Rows:
                    if row_3.GetColumnByName("IO_Section").Value==row_2.IO_Section and int(row_3.GetColumnByName("IO_Point_Quantity").Value)>0:
                        lv_RTP_5M=lv_RTP_5M+int(row_3.GetColumnByName("RTP_5_Pt_0M").Value) * row_2.Multiplier
            Trace.Write('lv_RTP_5M:'+str(lv_RTP_5M))
            setAtvQty('HC900_PART_SUMMARY',row_1.Model_Number,lv_RTP_5M)
#End-CXCPQ-41986
#End of SIL2 Safety System IO Section components BOM - CXCPQ-41981
Product.ApplyRules()