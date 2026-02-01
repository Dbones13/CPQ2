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
	Product.Attr('HC900_IO_Details_of_SIL2').Access = AttributeAccess.Editable
	HC900_SIL2=Product.GetContainerByName("HC900_Additional_IO_Details_of_SIL2")
	if HC900_SIL2.Rows.Count>0:
		for prow in HC900_SIL2.Rows:
			#CXCPQ-55711: Start
			if prow.GetColumnByName("IO_Section").Value=='SIL Universal IO Module (AI/DO/DI, 4-20mA, 16 channel)':
				prow["Channel_Num"]=str(lv_AI_DO_Channel_Num)
			#CXCPQ-55711 End
			prow["Redun_UIO_Multiplier"]=str(lv_Redun_UIO_Multiplier)
			prow.Calculate()
	if Quote.GetCustomField("R2QFlag").Content=='Yes':
		for row in Product.GetContainerByName('HC900_IO_Details_of_Non-SIL').Rows:
			row['IO_Point_Quantity'] = str(0)
			row['Euro_TB'] = str(0)
	
#Non SIL 
if lv_System_Type=='Non-SIL HC900 System':
	Product.Attr('HC900_IO_Details_of_Non-SIL').Access = AttributeAccess.Editable
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
	if Quote.GetCustomField("R2QFlag").Content=='Yes':
		for row in Product.GetContainerByName('HC900_IO_Details_of_SIL2').Rows:
			row['IO_Point_Quantity'] = str(0)
			row['Euro_TB'] = str(0)
if Quote.GetCustomField("R2QFlag").Content=='Yes':
	Product.Attr('HC900_Shield_Grounding_Strip_(Package of 2)').AssignValue('')
	Product.Attr('HC900_TerminalBoardJumpers_10_2_position_jumpers').AssignValue('')
	Product.Attr('HC900_TerminalBoardJumpers_10_10_position_jumpers').AssignValue('')
	Product.Attr('HC900 24 VDC Power Supply (2.5A)').AssignValue('')
	Product.Attr('HC900_250_Ohm_Shunt_Resistor_Kit_(8/pkg.)').AssignValue('')
	rack_container = Product.GetContainerByName('HC900_Rack_Size_Quantity_Cont')
	for row_new in rack_container.Rows:
		if row_new["Rack Size"] == "8 I/O Slot Rack":
			row_new["Quantity"] = ''