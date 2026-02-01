import System.Decimal as d
def total_io_rtu(attrs):

    # CXCPQ-25647
    hart_input = int(attrs.HART_Analog_Input)
    non_hart_input = int(attrs.Non_HART_Analog_Input)
    #Trace.Write('HART Inuput : {0}, Non HART input : {1}'.format(hart_input,non_hart_input))

    Total_IO_Point_Count = hart_input + non_hart_input + ((hart_input + non_hart_input) * int(attrs.io_spare_per) / 100)
    if int(Total_IO_Point_Count) % 8 == 0:
        qnt = int(Total_IO_Point_Count)/8
    else:
        qnt = int(Total_IO_Point_Count)/8 + 1

    REQ_CAL_TOT_AI  = qnt
    
    # CXCPQ-25648
    hart_output = int(attrs.HART_Analog_Output)
    non_hart_output = int(attrs.Non_HART_Analog_Output)

    Total_IO_Point_Count = hart_output + non_hart_output + ((hart_output + non_hart_output) * int(attrs.io_spare_per) / 100)
    if int(Total_IO_Point_Count) % 2 == 0:
        qnt = int(Total_IO_Point_Count)/2
    else:
        qnt = int(Total_IO_Point_Count)/2 + 1

    REQ_CAL_TOT_AO  = qnt
    
    # CXCPQ-25649

    Total_IO_Point_Count = int(attrs.Digital_Input) + (int(attrs.Digital_Input) * int(attrs.io_spare_per) / 100)
    if int(Total_IO_Point_Count) % 10 == 0:
        qnt = int(Total_IO_Point_Count)/10
    else:
        qnt = int(Total_IO_Point_Count)/10 + 1

    REQ_CAL_TOT_DI  = qnt
    
    # CXCPQ-25650

    Total_IO_Point_Count = int(attrs.Digital_Output) + (int(attrs.Digital_Output) * int(attrs.io_spare_per) / 100)
    if int(Total_IO_Point_Count) % 6 == 0:
        qnt = int(Total_IO_Point_Count)/6
    else:
        qnt = int(Total_IO_Point_Count)/6 + 1

    REQ_CAL_TOT_DO  = qnt
    
    #CXCPQ-25651

    Total_IO_Point_Count = int(attrs.Pulse_Input) + (int(attrs.Pulse_Input) * int(attrs.io_spare_per) / 100)
    if int(Total_IO_Point_Count) % 2 == 0:
        qnt = int(Total_IO_Point_Count)/2
    else:
        qnt = int(Total_IO_Point_Count)/2 + 1

    REQ_CAL_TOT_PI  = qnt

    #CXCPQ-25652
    #Trace.Write('REQ_CAL_TOT_AI : {0}, REQ_CAL_TOT_AO : {1}, REQ_CAL_TOT_DI : {2}, REQ_CAL_TOT_DO : {3}, REQ_CAL_TOT_PI : {4}'.format(REQ_CAL_TOT_AI,REQ_CAL_TOT_AO,REQ_CAL_TOT_DI,REQ_CAL_TOT_DO,REQ_CAL_TOT_PI))
    total_io = max(REQ_CAL_TOT_AI, REQ_CAL_TOT_AO, REQ_CAL_TOT_DI, REQ_CAL_TOT_DO, REQ_CAL_TOT_PI)

    return total_io
 
def total_dio_rtu(attrs):
    Total_DIO_Point_Count = float(attrs.Digital_Input_Output) + (float(attrs.Digital_Input_Output) * float(attrs.io_spare_per) / 100)
    qty_DIO = d.Ceiling(float(Total_DIO_Point_Count)/28)
    total_dio = qty_DIO
    
    return total_dio