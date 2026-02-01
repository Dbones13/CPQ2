#CXCPQ-37930
import System.Decimal as D

def FF_Segment_Calc(Prod):
    if Prod.Attributes.GetByName("FIM_Percent_Installed_Spare_Fieldbus_IO").GetValue():
        IS = int(Prod.Attributes.GetByName("FIM_Percent_Installed_Spare_Fieldbus_IO").GetValue())
        IS = 1 + float(IS)/float(100)
    else:
        IS = 1
    #Trace.Write("IS = "+str(IS))
    if Prod.Attributes.GetByName("FIM_Num_Devices_Open_Loop").GetValue():
        DO = int(Prod.Attributes.GetByName("FIM_Num_Devices_Open_Loop").GetValue())
    else:
        DO = 0
    #Trace.Write("DO = "+str(DO))
    if Prod.Attributes.GetByName("FIM_Num_Devices_Close_Loop").GetValue():
        DC = int(Prod.Attributes.GetByName("FIM_Num_Devices_Close_Loop").GetValue())
    else:
        DC = 0
    #Trace.Write("DC = "+str(DC))
    if Prod.Attributes.GetByName("FIM_Num_Close_Loop_per_Segment").GetValue():
        SC = int(Prod.Attributes.GetByName("FIM_Num_Close_Loop_per_Segment").GetValue())
    else:
        SC = 1
    #Trace.Write("SC = "+str(SC))
    if Prod.Attributes.GetByName("FIM_Num_FF_Temp_Mux_per_Segment").GetValue():
        FF = int(Prod.Attributes.GetByName("FIM_Num_FF_Temp_Mux_per_Segment").GetValue())
    else:
        FF = 0
    #Trace.Write("FF = "+str(FF))
    if Prod.Attributes.GetByName("FIM_Num_of_MOVs_per_Segment").GetValue():
        MOV = int(Prod.Attributes.GetByName("FIM_Num_of_MOVs_per_Segment").GetValue())
    else:
        MOV = 1
    #Trace.Write("MOV = "+str(MOV))
    if Prod.Attributes.GetByName("FIM_need_separate_segment_for_MOVs").GetValue():
        Need_separate_MOV = Prod.Attributes.GetByName("FIM_need_separate_segment_for_MOVs").GetValue()
    else:
        Need_separate_MOV = 'No'
    #Trace.Write("Need_separate_MOV = "+str(Need_separate_MOV))
    
    ff_io_cont = Prod.GetContainerByName('SerC_CG_FIM_FF_IO_Cont')
    
    i = 10
    ff_io_cont_vals = dict()
    for cont_row in ff_io_cont.Rows:
        if cont_row.GetColumnByName('Identifiers').Value == 'F5':
            break;
        j=i
        if cont_row.GetColumnByName('Red_wo_C300').Value:
            ff_io_cont_vals['F' + str(j)] = cont_row.GetColumnByName('Red_wo_C300').Value
        else:
            ff_io_cont_vals['F' + str(j)] = 0
        j = j + 1
        if cont_row.GetColumnByName('Future_Red_wo_C300').Value:
            ff_io_cont_vals['F' + str(j)] = cont_row.GetColumnByName('Future_Red_wo_C300').Value
        else:
            ff_io_cont_vals['F' + str(j)] = 0
        j = j + 1
        if cont_row.GetColumnByName('Non_Red_wo_C300').Value:
            ff_io_cont_vals['F' + str(j)] = cont_row.GetColumnByName('Non_Red_wo_C300').Value
        else:
            ff_io_cont_vals['F' + str(j)] = 0
        j = j + 1
        if cont_row.GetColumnByName('Red_C300').Value:
            ff_io_cont_vals['F' + str(j)] = cont_row.GetColumnByName('Red_C300').Value
        else:
            ff_io_cont_vals['F' + str(j)] = 0
        j = j + 1
        if cont_row.GetColumnByName('Future_Red_C300').Value:
            ff_io_cont_vals['F' + str(j)] = cont_row.GetColumnByName('Future_Red_C300').Value
        else:
            ff_io_cont_vals['F' + str(j)] = 0
        j = j + 1
        if cont_row.GetColumnByName('Non_Red_C300').Value:
            ff_io_cont_vals['F' + str(j)] = cont_row.GetColumnByName('Non_Red_C300').Value
        else:
            ff_io_cont_vals['F' + str(j)] = 0
        i = i + 10
    
    ff_io_tot_seg_cont = Prod.GetContainerByName('SerC_CG_FIM_FF_Tot_Seg_transpose')
    ff_tot_segments = dict()
    if Need_separate_MOV == 'Yes':
        R10 = 0
        #Trace.Write("F10 = "+ff_io_cont_vals['F10'])
        #Trace.Write("F20 = "+ff_io_cont_vals['F20'])
        #Trace.Write("F30 = "+ff_io_cont_vals['F30'])
        #Trace.Write("F40 = "+ff_io_cont_vals['F40'])
        R10_temp = D.Ceiling(float(ff_io_cont_vals['F10']) * IS) + (D.Ceiling(D.Ceiling(float(ff_io_cont_vals['F20']) * IS)/float(FF)) if FF > 0 else 0) + D.Ceiling(float(ff_io_cont_vals['F30']) * IS) - D.Ceiling(D.Ceiling(D.Ceiling(float(ff_io_cont_vals['F30']) * IS)/float(SC)) * DC)
        Trace.Write("R10 temp = "+str(R10_temp))
        if R10_temp < 0:
            R10_temp = 0
        else:
            R10_temp = (D.Ceiling(R10_temp / float(DO)) if DO > 0 else 0)
        R10 = D.Ceiling(D.Ceiling(float(ff_io_cont_vals['F30']) * IS)/SC) + R10_temp + D.Ceiling(D.Ceiling(float(ff_io_cont_vals['F40']) * IS)/ float(MOV))
        Trace.Write("R10 = "+str(R10))
        ff_tot_segments['R10'] = R10
        
        R11 = 0
        R11_temp = D.Ceiling(float(ff_io_cont_vals['F11']) * IS) + (D.Ceiling(D.Ceiling(float(ff_io_cont_vals['F21']) * IS)/float(FF)) if FF > 0 else 0) + D.Ceiling(float(ff_io_cont_vals['F31']) * IS) - D.Ceiling(D.Ceiling(D.Ceiling(float(ff_io_cont_vals['F31']) * IS)/float(SC)) * DC)
        Trace.Write("R11 temp = "+str(R11_temp))
        if R11_temp < 0:
            R11_temp = 0
        else:
            R11_temp = (D.Ceiling(R11_temp / float(DO)) if DO > 0 else 0)
        R11 = D.Ceiling(D.Ceiling(float(ff_io_cont_vals['F31']) * IS)/SC) + R11_temp + D.Ceiling(D.Ceiling(float(ff_io_cont_vals['F41']) * IS)/ float(MOV))
        Trace.Write("R11 = "+str(R11))
        ff_tot_segments['R11'] = R11
        
        R12 = 0
        R12_temp = D.Ceiling(float(ff_io_cont_vals['F12']) * IS) + (D.Ceiling(D.Ceiling(float(ff_io_cont_vals['F22']) * IS)/float(FF)) if FF > 0 else 0) + D.Ceiling(float(ff_io_cont_vals['F32']) * IS) - D.Ceiling(D.Ceiling(D.Ceiling(float(ff_io_cont_vals['F32']) * IS)/float(SC)) * DC)
        Trace.Write("R12 temp = "+str(R12_temp))
        if R12_temp < 0:
            R12_temp = 0
        else:
            R12_temp = (D.Ceiling(R12_temp / float(DO)) if DO > 0 else 0)
        R12 = D.Ceiling(D.Ceiling(float(ff_io_cont_vals['F32']) * IS)/SC) + R12_temp + D.Ceiling(D.Ceiling(float(ff_io_cont_vals['F42']) * IS)/ float(MOV))
        Trace.Write("R12 = "+str(R12))
        ff_tot_segments['R12'] = R12
        
        R13 = 0
        R13_temp = D.Ceiling(float(ff_io_cont_vals['F13']) * IS) + (D.Ceiling(D.Ceiling(float(ff_io_cont_vals['F23']) * IS)/float(FF)) if FF > 0 else 0) + D.Ceiling(float(ff_io_cont_vals['F33']) * IS) - D.Ceiling(D.Ceiling(D.Ceiling(float(ff_io_cont_vals['F33']) * IS)/float(SC)) * DC)
        Trace.Write("R13 temp = "+str(R13_temp))
        if R13_temp < 0:
            R13_temp = 0
        else:
            R13_temp = (D.Ceiling(R13_temp / float(DO)) if DO > 0 else 0)
        R13 = D.Ceiling(D.Ceiling(float(ff_io_cont_vals['F33']) * IS)/SC) + R13_temp + D.Ceiling(D.Ceiling(float(ff_io_cont_vals['F43']) * IS)/ float(MOV))
        Trace.Write("R13 = "+str(R13))
        ff_tot_segments['R13'] = R13
        
        R14 = 0
        R14_temp = D.Ceiling(float(ff_io_cont_vals['F14']) * IS) + (D.Ceiling(D.Ceiling(float(ff_io_cont_vals['F24']) * IS)/float(FF)) if FF > 0 else 0) + D.Ceiling(float(ff_io_cont_vals['F34']) * IS) - D.Ceiling(D.Ceiling(D.Ceiling(float(ff_io_cont_vals['F34']) * IS)/float(SC)) * DC)
        Trace.Write("R14 temp = "+str(R14_temp))
        if R14_temp < 0:
            R14_temp = 0
        else:
            R14_temp = (D.Ceiling(R14_temp / float(DO)) if DO > 0 else 0)
        R14 = D.Ceiling(D.Ceiling(float(ff_io_cont_vals['F34']) * IS)/SC) + R14_temp + D.Ceiling(D.Ceiling(float(ff_io_cont_vals['F44']) * IS)/ float(MOV))
        Trace.Write("R14 = "+str(R14))
        ff_tot_segments['R14'] = R14
        
        R15 = 0
        R15_temp = D.Ceiling(float(ff_io_cont_vals['F15']) * IS) + (D.Ceiling(D.Ceiling(float(ff_io_cont_vals['F25']) * IS)/float(FF)) if FF > 0 else 0) + D.Ceiling(float(ff_io_cont_vals['F35']) * IS) - D.Ceiling(D.Ceiling(D.Ceiling(float(ff_io_cont_vals['F35']) * IS)/float(SC)) * DC)
        Trace.Write("R15 temp = "+str(R15_temp))
        if R15_temp < 0:
            R15_temp = 0
        else:
            R15_temp = (D.Ceiling(R15_temp / float(DO)) if DO > 0 else 0)
        R15 = D.Ceiling(D.Ceiling(float(ff_io_cont_vals['F35']) * IS)/SC) + R15_temp + D.Ceiling(D.Ceiling(float(ff_io_cont_vals['F45']) * IS)/ float(MOV))
        Trace.Write("R15 = "+str(R15))
        ff_tot_segments['R15'] = R15
              
    else:
        R10 = 0
        #Trace.Write("F10 = "+ff_io_cont_vals['F10'])
        #Trace.Write("F20 = "+ff_io_cont_vals['F20'])
        #Trace.Write("F30 = "+ff_io_cont_vals['F30'])
        #Trace.Write("F40 = "+ff_io_cont_vals['F40'])
        R10_temp = D.Ceiling(float(ff_io_cont_vals['F10']) * IS) + (D.Ceiling(D.Ceiling(float(ff_io_cont_vals['F20']) * IS)/float(FF)) if FF > 0 else 0) + D.Ceiling(float(ff_io_cont_vals['F30']) * IS) + D.Ceiling(float(ff_io_cont_vals['F40']) * IS) - D.Ceiling(D.Ceiling((D.Ceiling(float(ff_io_cont_vals['F30']) * IS) + D.Ceiling(float(ff_io_cont_vals['F40']) * IS))/float(SC)) * DC)
        Trace.Write("R10 temp = "+str(R10_temp))
        if R10_temp < 0:
            R10_temp = 0
        else:
            R10_temp = (D.Ceiling(R10_temp / float(DO)) if DO > 0 else 0)
        R10 = D.Ceiling((D.Ceiling(float(ff_io_cont_vals['F30']) * IS) + D.Ceiling(float(ff_io_cont_vals['F40']) * IS))/ float(SC)) + R10_temp 
        Trace.Write("R10 = "+str(R10))
        ff_tot_segments['R10'] = R10
        
        R11 = 0
        R11_temp = D.Ceiling(float(ff_io_cont_vals['F11']) * IS) + (D.Ceiling(D.Ceiling(float(ff_io_cont_vals['F21']) * IS)/float(FF)) if FF > 0 else 0) + D.Ceiling(float(ff_io_cont_vals['F31']) * IS) + D.Ceiling(float(ff_io_cont_vals['F41']) * IS) - D.Ceiling(D.Ceiling((D.Ceiling(float(ff_io_cont_vals['F31']) * IS) + D.Ceiling(float(ff_io_cont_vals['F41']) * IS))/float(SC)) * DC)
        Trace.Write("R11 temp = "+str(R11_temp))
        if R11_temp < 0:
            R11_temp = 0
        else:
            R11_temp = (D.Ceiling(R11_temp / float(DO)) if DO > 0 else 0)
        R11 = D.Ceiling((D.Ceiling(float(ff_io_cont_vals['F31']) * IS) + D.Ceiling(float(ff_io_cont_vals['F41']) * IS))/ float(SC)) + R11_temp
        Trace.Write("R11 = "+str(R11))
        ff_tot_segments['R11'] = R11
        
        R12 = 0
        R12_temp = D.Ceiling(float(ff_io_cont_vals['F12']) * IS) + (D.Ceiling(D.Ceiling(float(ff_io_cont_vals['F22']) * IS)/float(FF)) if FF > 0 else 0) + D.Ceiling(float(ff_io_cont_vals['F32']) * IS) + D.Ceiling(float(ff_io_cont_vals['F42']) * IS) - D.Ceiling(D.Ceiling((D.Ceiling(float(ff_io_cont_vals['F32']) * IS) + D.Ceiling(float(ff_io_cont_vals['F42']) * IS))/float(SC)) * DC)
        Trace.Write("R12 temp = "+str(R12_temp))
        if R12_temp < 0:
            R12_temp = 0
        else:
            R12_temp = (D.Ceiling(R12_temp / float(DO)) if DO > 0 else 0)
        R12 = D.Ceiling((D.Ceiling(float(ff_io_cont_vals['F32']) * IS) + D.Ceiling(float(ff_io_cont_vals['F42']) * IS))/ float(SC)) + R12_temp
        Trace.Write("R12 = "+str(R12))
        ff_tot_segments['R12'] = R12
        
        R13 = 0
        R13_temp = D.Ceiling(float(ff_io_cont_vals['F13']) * IS) + (D.Ceiling(D.Ceiling(float(ff_io_cont_vals['F23']) * IS)/float(FF)) if FF > 0 else 0) + D.Ceiling(float(ff_io_cont_vals['F33']) * IS) + D.Ceiling(float(ff_io_cont_vals['F43']) * IS) - D.Ceiling(D.Ceiling((D.Ceiling(float(ff_io_cont_vals['F33']) * IS) + D.Ceiling(float(ff_io_cont_vals['F43']) * IS))/float(SC)) * DC)
        Trace.Write("R13 temp = "+str(R13_temp))
        if R13_temp < 0:
            R13_temp = 0
        else:
            R13_temp = (D.Ceiling(R13_temp / float(DO)) if DO > 0 else 0)
        R13 = D.Ceiling((D.Ceiling(float(ff_io_cont_vals['F33']) * IS) + D.Ceiling(float(ff_io_cont_vals['F43']) * IS))/ float(SC)) + R13_temp
        Trace.Write("R13 = "+str(R13))
        ff_tot_segments['R13'] = R13
        
        R14 = 0
        R14_temp = D.Ceiling(float(ff_io_cont_vals['F14']) * IS) + (D.Ceiling(D.Ceiling(float(ff_io_cont_vals['F24']) * IS)/float(FF)) if FF > 0 else 0) + D.Ceiling(float(ff_io_cont_vals['F34']) * IS) + D.Ceiling(float(ff_io_cont_vals['F44']) * IS) - D.Ceiling(D.Ceiling((D.Ceiling(float(ff_io_cont_vals['F34']) * IS) + D.Ceiling(float(ff_io_cont_vals['F44']) * IS))/float(SC)) * DC)
        Trace.Write("R14 temp = "+str(R14_temp))
        if R14_temp < 0:
            R14_temp = 0
        else:
            R14_temp = (D.Ceiling(R14_temp / float(DO)) if DO > 0 else 0)
        R14 = D.Ceiling((D.Ceiling(float(ff_io_cont_vals['F34']) * IS) + D.Ceiling(float(ff_io_cont_vals['F44']) * IS))/ float(SC)) + R14_temp
        Trace.Write("R14 = "+str(R14))
        ff_tot_segments['R14'] = R14
        
        R15 = 0
        R15_temp = D.Ceiling(float(ff_io_cont_vals['F15']) * IS) + (D.Ceiling(D.Ceiling(float(ff_io_cont_vals['F25']) * IS)/float(FF)) if FF > 0 else 0) + D.Ceiling(float(ff_io_cont_vals['F35']) * IS) + D.Ceiling(float(ff_io_cont_vals['F45']) * IS) - D.Ceiling(D.Ceiling((D.Ceiling(float(ff_io_cont_vals['F35']) * IS) + D.Ceiling(float(ff_io_cont_vals['F45']) * IS))/float(SC)) * DC)
        Trace.Write("R15 temp = "+str(R15_temp))
        if R15_temp < 0:
            R15_temp = 0
        else:
            R15_temp = (D.Ceiling(R15_temp / float(DO)) if DO > 0 else 0)
        R15 = D.Ceiling((D.Ceiling(float(ff_io_cont_vals['F35']) * IS) + D.Ceiling(float(ff_io_cont_vals['F45']) * IS))/ float(SC)) + R15_temp
        Trace.Write("R15 = "+str(R15))
        ff_tot_segments['R15'] = R15
        
    seg_count = 10
    for tot_seg_cont_row in ff_io_tot_seg_cont.Rows:
        tot_seg_cont_row.SetColumnValue("Tot_Seg", str(ff_tot_segments['R'+str(seg_count)]))
        seg_count = seg_count + 1
    
    ff_io_tot_seg_cont.Calculate()
    
if Product.Attributes.GetByName("SerC_CG_Foundation_Fieldbus_Interface_required").GetValue():
    Foundation_FB = Product.Attributes.GetByName("SerC_CG_Foundation_Fieldbus_Interface_required").GetValue()
else:
    Foundation_FB = 'No'
if Foundation_FB == 'Yes':
    FF_Segment_Calc(Product)
#FF_Segment_Calc(Product)