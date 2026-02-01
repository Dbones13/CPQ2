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
            break
lv_System_Type=Product.Attributes.GetByName("HC900_System_Type").GetValue()

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
            Required_Qty= int(row.GetColumnByName("Required_Qty").Value)
            if Model_Number=='900U02-0100_dummy':
                lv_QtySum_900U02_0100=lv_QtySum_900U02_0100 + Required_Qty
        setAtvQty('HC900_PART_SUMMARY','900U02-0100',int(lv_QtySum_900U02_0100))
#SIL2 Safety System IO Section BOM - End CXCPQ-40187
#CXCPQ-40183 -Start
if Quote.GetCustomField("R2QFlag").Content != 'Yes':
    lv_Redu_Rack_PS=Product.Attributes.GetByName("HC900_Redundant_I/O_Rack_Power_Supplies").GetValue()
    HC900_Rack_Cont = Product.GetContainerByName('HC900_Rack_Size_Quantity_Cont')
    if HC900_Rack_Cont.Rows.Count>0:
        for row in HC900_Rack_Cont.Rows:
            lv_Rack_Size=row.GetColumnByName("Rack Size").Value
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