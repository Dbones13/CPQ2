import System.Decimal as d

def calc_io_details_rtu_system(attrs, parts_dict):
    total_io = 0
    qty_NRC = 0
    qty_RC = 0
    qty_DIO = 0
    #CXCPQ-25653--Added by Shivani
    
    #total_num_of_seg_reqired_for_fim4 = (float(attrs.FIM_Analog_Input) + float(attrs.FIM_Analog_Input) * float(attrs.IO_Spare_Percentage/100)) / float(attrs.FIM_devices_segment_withOpen_loop)
    #num_FIM = d.Ceiling(float(total_num_of_seg_reqired_for_fim4 / 4))
    num_FIM = d.Ceiling(float(attrs.Number_Segments_FIM4) / 4.00)
    if num_FIM > 0:
        parts_dict["CC-PFB402"] = {'Quantity' : int(1 * num_FIM), 'Description': 'Fieldbus Interface Module, 4 H1 Nets'}
        parts_dict["CC-TFB402"] = {'Quantity' : int(1 * num_FIM), 'Description': 'Fieldbus Interface IOTA Non-Red - 4 Nets'}
        parts_dict["F860"] = {'Quantity' : int(1 * num_FIM), 'Description': 'MTL PWR SYS, RED 8-SEG FIELDBUS'}
        parts_dict["FCAB-05"] = {'Quantity' : int(1 * num_FIM), 'Description': 'FIELDBUS IOTA POWER CABLE 30CM'}
    
    #CXCPQ-25654--Added by Prabhat
    if int(attrs.Modbus_TCP_IP_Ethernet_Device) > 0:
        qnt = d.Ceiling(float(attrs.Modbus_TCP_IP_Ethernet_Device)/8)
        '''if int(attrs.Modbus_TCP_IP_Ethernet_Device) % 8 == 0:
            qnt = int(attrs.Modbus_TCP_IP_Ethernet_Device)/8
        else:
            qnt = int(attrs.Modbus_TCP_IP_Ethernet_Device)/8 + 1'''
        parts_dict["SI-3300I2"] = {'Quantity' : str(qnt), 'Description': 'IND ETHERNET SWITCH 8 10/100 TX 2 SFP'}
    
    # CXCPQ-104965
    Total_DIO_Point_Count = float(attrs.Digital_Input_Output) + (float(attrs.Digital_Input_Output) * float(attrs.io_spare_per) / 100)
    qty_DIO = d.Ceiling(float(Total_DIO_Point_Count)/28)
    total_dio = qty_DIO
    if int(attrs.Digital_Input_Output) > 0:
        parts_dict["SC-UDIO01"] = {'Quantity' : str(qty_DIO), 'Description': 'CONTROLEDGE 2020 UNIVERSAL DIG IOM, 28CH'}

    # CXCPQ-25647

    hart_input = float(attrs.HART_Analog_Input)
    non_hart_input = float(attrs.Non_HART_Analog_Input)

    Total_IO_Point_Count = hart_input + non_hart_input + ((hart_input + non_hart_input) * float(attrs.io_spare_per) / 100)
    qnt = d.Ceiling(float(Total_IO_Point_Count)/8)
    REQ_CAL_TOT_AI  = qnt
    
    # CXCPQ-25648
    hart_output = float(attrs.HART_Analog_Output)
    non_hart_output = float(attrs.Non_HART_Analog_Output)

    Total_IO_Point_Count = hart_output + non_hart_output + ((hart_output + non_hart_output) * float(attrs.io_spare_per) / 100)
    qnt = d.Ceiling(float(Total_IO_Point_Count)/2)
    REQ_CAL_TOT_AO  = qnt
    

    # CXCPQ-25650

    Total_IO_Point_Count = float(attrs.Digital_Output) + (float(attrs.Digital_Output) * float(attrs.io_spare_per) / 100)
    qnt = d.Ceiling(float(Total_IO_Point_Count)/6)
    REQ_CAL_TOT_DO  = qnt
    

    #CXCPQ-25651

    Total_IO_Point_Count1 = float(attrs.Pulse_Input) + (float(attrs.Pulse_Input) * float(attrs.io_spare_per) / 100)
    qnt = d.Ceiling(float(Total_IO_Point_Count1)/2)
    REQ_CAL_TOT_PI  = qnt
    
    # CXCPQ-25649

    Total_IO_Point_Count = float(attrs.Digital_Input) + (float(attrs.Digital_Input) * float(attrs.io_spare_per) / 100)
    qnt = d.Ceiling((float(Total_IO_Point_Count)+float(Total_IO_Point_Count1))/12)
    REQ_CAL_TOT_DI  = qnt
    
    
    #CXCPQ-25652
    if attrs.controller_redundancy == 'Redundant':
        total_io = max(REQ_CAL_TOT_AI, REQ_CAL_TOT_AO, REQ_CAL_TOT_DI, REQ_CAL_TOT_DO, REQ_CAL_TOT_PI)
        if total_io > 0:
            parts_dict["SC-UMIX01"] = {'Quantity' : str(total_io), 'Description': 'RTU2020 MIXED IO (28)'}
    elif attrs.controller_redundancy == 'Non Redundant':
        total_io = max(REQ_CAL_TOT_AI, REQ_CAL_TOT_AO, REQ_CAL_TOT_DI, REQ_CAL_TOT_DO, REQ_CAL_TOT_PI)
        if total_io > 0:
            parts_dict["SC-UMIX01"] = {'Quantity' : str(total_io - 1), 'Description': 'RTU2020 MIXED IO (28)'}
            
     #CXCPQ-29565
    '''if attrs.cabinet_type == 'Dual':
        spare_spc_ned =d.Ceiling(float(float(total_io)*float(attrs.cab_spare_space_per))/100)
        tio_model_cab =d.Ceiling(float(total_io)+float(spare_spc_ned ))
        if tio_model_cab > 0 and float(attrs.cab_spare_space_per) > 0 :
            parts_dict["SC-UMIX01"] = {'Quantity' : str(tio_model_cab ), 'Description': 'RTU2020 MIXED IO (28)'}
        elif total_io > 0:
            parts_dict["SC-UMIX01"] = {'Quantity' : str(total_io), 'Description': 'RTU2020 MIXED IO (28)'}
    #CXCPQ-25628
    elif attrs.cabinet_type == 'One':
        spare_spc_ned =d.Ceiling(float(float(total_io)*float(attrs.cab_spare_space_per))/100)
        tio_model_cab =d.Ceiling(float(total_io)+float(spare_spc_ned ))
        if tio_model_cab > 0 and float(attrs.cab_spare_space_per) > 0 :
            parts_dict["SC-UMIX01"] = {'Quantity' : str(tio_model_cab ), 'Description': 'RTU2020 MIXED IO (28)'}
        elif total_io > 0:
            parts_dict["SC-UMIX01"] = {'Quantity' : str(total_io), 'Description': 'RTU2020 MIXED IO (28)'}'''
            
    '''elif attrs.cabinet_type == 'One':
        if attrs.controller_redundancy == 'Redundant':
            total_io = max(REQ_CAL_TOT_AI, REQ_CAL_TOT_AO, REQ_CAL_TOT_DI, REQ_CAL_TOT_DO, REQ_CAL_TOT_PI)
            if total_io > 0:
                parts_dict["SC-UMIX01"] = {'Quantity' : str(total_io), 'Description': 'RTU2020 MIXED IO (28)'}
        elif attrs.controller_redundancy == 'Non Redundant':
            total_io = max(REQ_CAL_TOT_AI, REQ_CAL_TOT_AO, REQ_CAL_TOT_DI, REQ_CAL_TOT_DO, REQ_CAL_TOT_PI)
            if total_io > 0:
                parts_dict["SC-UMIX01"] = {'Quantity' : str(total_io - 1), 'Description': 'RTU2020 MIXED IO (28)'}'''
       
        
    #CXCPQ-21362--Added by Prabhat
    if (int(attrs.HART_Analog_Input) + int(attrs.HART_Analog_Output))>0:
        AI_HART_IO_Points = d.Ceiling(float(float(attrs.HART_Analog_Input)/8))
        AO_HART_IO_Points = d.Ceiling(float(float(attrs.HART_Analog_Output)/2))
        HART_License_Qty= max(AI_HART_IO_Points,AO_HART_IO_Points)
        parts_dict['SP-IHARTP'] = {'Quantity' :str(HART_License_Qty), 'Description': 'HART PROTOCOL'}

    #CXCPQ-21361--Added by Prabhat
    if int(attrs.Field_ISA100)>0 or int(attrs.FDAP)>0:
        No_ISA100 = d.Ceiling(float(float(attrs.Field_ISA100)/25))
        FDAP_Wireless = d.Ceiling(float(float(attrs.FDAP)/4))
        Qty_wireless = max(No_ISA100 ,FDAP_Wireless )
        if int(Qty_wireless )>0:
            parts_dict['SP-IWIO01'] = {'Quantity' :str(Qty_wireless ), 'Description': 'WIRELESS IO PROTOCOL'}
    #CXCPQ-21365...added by prabhat
    nr_io_mod=d.Ceiling(float(float(total_io) + float(total_dio))/30)
    nr_fim=int(num_FIM )
    nr_rs485_scd=d.Ceiling(float(float(attrs.Modbus_RS485_Serial_Communication_Devices ))/64)
    nr_rs232_scd=d.Ceiling(float(float(attrs.Modbus_RS232_Serial_Communication_Devices ))/2)
    nr_ISA100_wd=d.Ceiling(float(float(attrs.Field_ISA100)/25))
    nr_FDAP=d.Ceiling(float(float(attrs.FDAP)/4))
    nr_gl_li=d.Ceiling(float(float(attrs.Gas_and_Liquid_Meter_Run_License))/12)

    if attrs.controller_redundancy =="Redundant":
        qty_RC = max(nr_io_mod,nr_fim,nr_rs485_scd,nr_rs232_scd,nr_ISA100_wd,nr_FDAP,nr_gl_li)
        if int(qty_RC)>0:
            parts_dict["SC-UCNN11"] = {'Quantity' : str(qty_RC), 'Description': 'Control Edge RTU Redundant Controller'}
    
    #CXCPQ-21367...added by Lahu
    nr_io_mod=d.Ceiling(float(float(total_io) + float(total_dio))/29)
    nr_fim=int(num_FIM)
    nr_rs485_scd=d.Ceiling(float(float(attrs.Modbus_RS485_Serial_Communication_Devices))/64)
    nr_rs232_scd=d.Ceiling(float(float(attrs.Modbus_RS232_Serial_Communication_Devices))/2)
    nr_ISA100_wd=d.Ceiling(float(float(attrs.Field_ISA100))/25)
    nr_FDAP=d.Ceiling(float(float(attrs.FDAP))/4)
    nr_gl_li=d.Ceiling(float(float(attrs.Gas_and_Liquid_Meter_Run_License))/4)

    if attrs.controller_redundancy=="Non Redundant":
        qty_NRC= max(nr_io_mod,nr_fim,nr_rs485_scd,nr_rs232_scd,nr_ISA100_wd,nr_FDAP,nr_gl_li)
        if int(qty_NRC)>0:
            parts_dict["SC-UCMX02"] = {'Quantity' : str(qty_NRC), 'Description': 'Control Edge RTU Non-Redundant Controller'}
    
    #CXCPQ-21372...added by Lahu
    qty_CNR=int(qty_RC+qty_NRC)
    if int(total_io )>0 or int(qty_CNR)>0 or int(total_dio)>0:
        No_mod_Rows =d.Ceiling(float(float(total_io) + float(total_dio) + float(float(qty_CNR))) / 5)
        Right_End_Plate = float(No_mod_Rows)
        Left_End_Plate=int(int(Right_End_Plate) -1)
        if int(Right_End_Plate)> 0:
            parts_dict["SC-TEPR01"] = {'Quantity' : Right_End_Plate, 'Description': 'Control Edge RTU Expansion End Plate Right'}
        
        if int(Left_End_Plate)> 0:
            parts_dict["SC-TEPL01"] = {'Quantity' : Left_End_Plate, 'Description': 'Control Edge RTU Expansion End Plate Left'}
    return parts_dict