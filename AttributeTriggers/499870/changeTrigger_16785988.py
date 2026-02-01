#CXCPQ-51170: Set multiplier to 2 for SIL Universal IO Module (AI/DO/DI, 4-20mA, 16 channel) AND  SIL Universal Analog Outputs 4-20 mA (8 channel)
lv_RRUIO=Product.Attributes.GetByName("HC900_Redundancy_Required_in_Universal_IO").GetValue()
lv_Redun_UIO_Multiplier=1
lv_AI_DO_Channel_Num=16 #CXCPQ-55711 default 16
if lv_RRUIO=='Yes':
    lv_Redun_UIO_Multiplier =2
    lv_AI_DO_Channel_Num=14 #CXCPQ-55711 set to 14 when redundancy required UIO Yes

lv_System_Type=Product.Attributes.GetByName("HC900_System_Type").GetValue()

#SIL Additional container
if lv_System_Type=='SIL2 Safety System':
    HC900_SIL2=Product.GetContainerByName("HC900_Additional_IO_Details_of_SIL2")
    if HC900_SIL2.Rows.Count>0:
        for prow in HC900_SIL2.Rows:
            #CXCPQ-55711: Start
            if prow.GetColumnByName("IO_Section").Value=='SIL Universal IO Module (AI/DO/DI, 4-20mA, 16 channel)':
                prow["Channel_Num"]=str(lv_AI_DO_Channel_Num)
            #CXCPQ-55711 End
            prow["Redun_UIO_Multiplier"]=str(lv_Redun_UIO_Multiplier)
            prow.Calculate()

#Non SIL 
if lv_System_Type=='Non-SIL HC900 System':
    HC900_NSIL = Product.GetContainerByName('HC900_IO_Details_of_Non-SIL')
    if HC900_NSIL.Rows.Count>0:
        for prow in HC900_NSIL.Rows:
            #CXCPQ-55711: Start
            if prow.GetColumnByName("IO_Section").Value=='SIL Universal IO Module (AI/DO/DI, 4-20mA, 16 channel)':
                prow["Channel_Num"]=str(lv_AI_DO_Channel_Num)
                prow.Calculate()
            #CXCPQ-55711: End
            Model_Number = prow.GetColumnByName("Model_Number").Value
            if Model_Number=='900U02-0100_dummy':
                prow["Redun_UIO_Multiplier"]=str(lv_Redun_UIO_Multiplier)
                prow.Calculate()
                #CXCPQ-51170: Set multiplier to 2 for SIL Universal IO Module (AI/DO/DI, 4-20mA, 16 channel) AND  SIL Universal Analog Outputs 4-20 mA (8 channel)