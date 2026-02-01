def populateC300Data1(Quote,child):
    n = RIO_CNT = LIO_CNT = 0
    child=child
    ioSum = [0] * 800
    ms_attr =child.SelectedAttributes.GetContainerByName("Document_cont_c300").Rows
    for io_f in ms_attr:
        io_Family=io_f['Io_family']
        universal=io_f['Io_family']
        fmio=io_f['Io_family']
        pmio=io_f['Io_family']
        #Trace.Write("io_Family "+str(io_f['Io_family']))
        if io_Family=="Mark2":
            MS = child.SelectedAttributes.GetContainerByName("C300_C IO MS2").Rows
            EN = child.SelectedAttributes.GetContainerByName("C300_SerC_Enhanced_Function_IO_Mark_Group_CG_Cont").Rows
            EN1 = child.SelectedAttributes.GetContainerByName("C300_SerC_Enhanced_Function_IO_Mark_Group_CG_Cont1").Rows
            UN = child.SelectedAttributes.GetContainerByName("C300_CG_Universal_IO_Mark_1").Rows
            UN1 = child.SelectedAttributes.GetContainerByName("C300_CG_Universal_IO_Mark_2").Rows
        elif io_Family=="seriesC":
            MS = child.SelectedAttributes.GetContainerByName("C300_C IO MS").Rows
            UN=child.SelectedAttributes.GetContainerByName("C300_CG_Universal_IO_cont_1").Rows
            UN1=child.SelectedAttributes.GetContainerByName("C300_CG_Universal_IO_cont_2").Rows
            EN=child.SelectedAttributes.GetContainerByName("SerC_CG_Enhanced_Function_IO_Cont").Rows
            EN1=child.SelectedAttributes.GetContainerByName("SerC_CG_Enhanced_Function_IO_Cont2").Rows
        elif io_Family=="TurboM":
            UN=child.SelectedAttributes.GetContainerByName("C300_CG_Universal_IO_cont_1").Rows
            UN1=child.SelectedAttributes.GetContainerByName("C300_CG_Universal_IO_cont_2").Rows
            EN=child.SelectedAttributes.GetContainerByName("SerC_CG_Enhanced_Function_IO_Cont").Rows
            EN1=child.SelectedAttributes.GetContainerByName("SerC_CG_Enhanced_Function_IO_Cont2").Rows
    #Digital Input Container Data
    if io_Family !="TurboM":
        for attr_cnt in MS:
            if attr_cnt['IO_Type'] in ['Series-C: HLAI (16) 4-20mA (0-5000)']:
                ioSum[1] = int(attr_cnt['Red_IS']) if attr_cnt['Red_IS']!='' else 0
                ioSum[3] = int(attr_cnt['Future_Red_IS']) if attr_cnt['Future_Red_IS']!='' else 0
                ioSum[5] = int(attr_cnt['Non_Red_IS']) if attr_cnt['Non_Red_IS']!='' else 0
                ioSum[7] = int(attr_cnt['Red_NIS']) if attr_cnt['Red_NIS']!='' else 0
                ioSum[9] = int(attr_cnt['Future_Red_NIS']) if attr_cnt['Future_Red_NIS']!='' else 0
                ioSum[11] = int(attr_cnt['Non_Red_NIS']) if attr_cnt['Non_Red_NIS']!='' else 0
                ioSum[13] = int(attr_cnt['Red_ISLTR']) if attr_cnt['Red_ISLTR']!='' else 0
                ioSum[15] = int(attr_cnt['Future_Red_ISLTR']) if attr_cnt['Future_Red_ISLTR']!='' else 0
                ioSum[17] = int(attr_cnt['Non_Red_ISLTR']) if attr_cnt['Non_Red_ISLTR']!='' else 0
            if attr_cnt['IO_Type'] in ['SCM: HLAI (16) 4-20mA (0-5000)']:
                ioSum[2] = int(attr_cnt['Red_IS']) if attr_cnt['Red_IS']!='' else 0
                ioSum[4] = int(attr_cnt['Future_Red_IS']) if attr_cnt['Future_Red_IS']!='' else 0
                ioSum[6] = int(attr_cnt['Non_Red_IS']) if attr_cnt['Non_Red_IS']!='' else 0
                ioSum[8] = int(attr_cnt['Red_NIS']) if attr_cnt['Red_NIS']!='' else 0
                ioSum[10] = int(attr_cnt['Future_Red_NIS']) if attr_cnt['Future_Red_NIS']!='' else 0
                ioSum[12] = int(attr_cnt['Non_Red_NIS']) if attr_cnt['Non_Red_NIS']!='' else 0
                ioSum[14] = int(attr_cnt['Red_ISLTR']) if attr_cnt['Red_ISLTR']!='' else 0
                ioSum[16] = int(attr_cnt['Future_Red_ISLTR']) if attr_cnt['Future_Red_ISLTR']!='' else 0
                ioSum[18] = int(attr_cnt['Non_Red_ISLTR']) if attr_cnt['Non_Red_ISLTR']!='' else 0
            if attr_cnt['IO_Type'] in ['Series-C: AO (16) HART Config/Status (0-5000)']:
                ioSum[150] += int(attr_cnt['Red_IS']) if attr_cnt['Red_IS']!='' else 0
                ioSum[152] += int(attr_cnt['Future_Red_IS']) if attr_cnt['Future_Red_IS']!='' else 0
                ioSum[154] += int(attr_cnt['Non_Red_IS']) if attr_cnt['Non_Red_IS']!='' else 0
                ioSum[156] += int(attr_cnt['Red_NIS']) if attr_cnt['Red_NIS']!='' else 0
                ioSum[158] += int(attr_cnt['Future_Red_NIS']) if attr_cnt['Future_Red_NIS']!='' else 0
                ioSum[160] += int(attr_cnt['Non_Red_NIS']) if attr_cnt['Non_Red_NIS']!='' else 0
                ioSum[162] += int(attr_cnt['Red_ISLTR']) if attr_cnt['Red_ISLTR']!='' else 0
                ioSum[164] += int(attr_cnt['Future_Red_ISLTR']) if attr_cnt['Future_Red_ISLTR']!='' else 0
                ioSum[166] += int(attr_cnt['Non_Red_ISLTR']) if attr_cnt['Non_Red_ISLTR']!='' else 0
            if attr_cnt['IO_Type'] in ['SCM: AO (16) HART Config/Status (0-5000)']:
                ioSum[151] += int(attr_cnt['Red_IS']) if attr_cnt['Red_IS']!='' else 0
                ioSum[153] += int(attr_cnt['Future_Red_IS']) if attr_cnt['Future_Red_IS']!='' else 0
                ioSum[155] += int(attr_cnt['Non_Red_IS']) if attr_cnt['Non_Red_IS']!='' else 0
                ioSum[157] += int(attr_cnt['Red_NIS']) if attr_cnt['Red_NIS']!='' else 0
                ioSum[159] += int(attr_cnt['Future_Red_NIS']) if attr_cnt['Future_Red_NIS']!='' else 0
                ioSum[161] += int(attr_cnt['Non_Red_NIS']) if attr_cnt['Non_Red_NIS']!='' else 0
                ioSum[163] += int(attr_cnt['Red_ISLTR']) if attr_cnt['Red_ISLTR']!='' else 0
                ioSum[165] += int(attr_cnt['Future_Red_ISLTR']) if attr_cnt['Future_Red_ISLTR']!='' else 0
                ioSum[167] += int(attr_cnt['Non_Red_ISLTR']) if attr_cnt['Non_Red_ISLTR']!='' else 0
            if attr_cnt['IO_Type'] in ['Series-C: LLAI (16) (0-5000)']:
                ioSum[79] = int(attr_cnt['Non_Red_NIS']) if attr_cnt['Non_Red_NIS']!='' else 0
            if attr_cnt['IO_Type'] in ['SCM: LLAI (16) (0-5000)']:
                ioSum[80] = int(attr_cnt['Non_Red_NIS']) if attr_cnt['Non_Red_NIS']!='' else 0
            if attr_cnt['IO_Type'] in ['Series-C: HLAI (16) HART Config/Status (0-5000)']:
                ioSum[22] = int(attr_cnt['Red_IS']) if attr_cnt['Red_IS']!='' else 0
                ioSum[24] = int(attr_cnt['Future_Red_IS']) if attr_cnt['Future_Red_IS']!='' else 0
                ioSum[26] = int(attr_cnt['Non_Red_IS']) if attr_cnt['Non_Red_IS']!='' else 0
                ioSum[28] = int(attr_cnt['Red_NIS']) if attr_cnt['Red_NIS']!='' else 0
                ioSum[30] = int(attr_cnt['Future_Red_NIS']) if attr_cnt['Future_Red_NIS']!='' else 0
                ioSum[32] = int(attr_cnt['Non_Red_NIS']) if attr_cnt['Non_Red_NIS']!='' else 0
                ioSum[34] = int(attr_cnt['Red_ISLTR']) if attr_cnt['Red_ISLTR']!='' else 0
                ioSum[36] = int(attr_cnt['Future_Red_ISLTR']) if attr_cnt['Future_Red_ISLTR']!='' else 0
                ioSum[38] = int(attr_cnt['Non_Red_ISLTR']) if attr_cnt['Non_Red_ISLTR']!='' else 0
            if attr_cnt['IO_Type'] in ['SCM: HLAI (16) HART Config/Status (0-5000)']:
                ioSum[23] = int(attr_cnt['Red_IS']) if attr_cnt['Red_IS']!='' else 0
                ioSum[25] = int(attr_cnt['Future_Red_IS']) if attr_cnt['Future_Red_IS']!='' else 0
                ioSum[27] = int(attr_cnt['Non_Red_IS']) if attr_cnt['Non_Red_IS']!='' else 0
                ioSum[29] = int(attr_cnt['Red_NIS']) if attr_cnt['Red_NIS']!='' else 0
                ioSum[31] = int(attr_cnt['Future_Red_NIS']) if attr_cnt['Future_Red_NIS']!='' else 0
                ioSum[33] = int(attr_cnt['Non_Red_NIS']) if attr_cnt['Non_Red_NIS']!='' else 0
                ioSum[35] = int(attr_cnt['Red_ISLTR']) if attr_cnt['Red_ISLTR']!='' else 0
                ioSum[37] = int(attr_cnt['Future_Red_ISLTR']) if attr_cnt['Future_Red_ISLTR']!='' else 0
                ioSum[39] = int(attr_cnt['Non_Red_ISLTR']) if attr_cnt['Non_Red_ISLTR']!='' else 0

            if attr_cnt['IO_Type'] in ['Series-C: AO (16) (0-5000)']:
                ioSum[132] = int(attr_cnt['Red_IS']) if attr_cnt['Red_IS']!='' else 0
                ioSum[134] = int(attr_cnt['Future_Red_IS']) if attr_cnt['Future_Red_IS']!='' else 0
                ioSum[136] = int(attr_cnt['Non_Red_IS']) if attr_cnt['Non_Red_IS']!='' else 0
                ioSum[138] = int(attr_cnt['Red_NIS']) if attr_cnt['Red_NIS']!='' else 0
                ioSum[140] = int(attr_cnt['Future_Red_NIS']) if attr_cnt['Future_Red_NIS']!='' else 0
                ioSum[142] = int(attr_cnt['Non_Red_NIS']) if attr_cnt['Non_Red_NIS']!='' else 0
                ioSum[144] = int(attr_cnt['Red_ISLTR']) if attr_cnt['Red_ISLTR']!='' else 0
                ioSum[146] = int(attr_cnt['Future_Red_ISLTR']) if attr_cnt['Future_Red_ISLTR']!='' else 0
                ioSum[148] = int(attr_cnt['Non_Red_ISLTR']) if attr_cnt['Non_Red_ISLTR']!='' else 0
            if attr_cnt['IO_Type'] in ['SCM: AO (16) (0-5000)']:
                ioSum[133] = int(attr_cnt['Red_IS']) if attr_cnt['Red_IS']!='' else 0
                ioSum[135] = int(attr_cnt['Future_Red_IS']) if attr_cnt['Future_Red_IS']!='' else 0
                ioSum[137] = int(attr_cnt['Non_Red_IS']) if attr_cnt['Non_Red_IS']!='' else 0
                ioSum[139] = int(attr_cnt['Red_NIS']) if attr_cnt['Red_NIS']!='' else 0
                ioSum[141] = int(attr_cnt['Future_Red_NIS']) if attr_cnt['Future_Red_NIS']!='' else 0
                ioSum[143] = int(attr_cnt['Non_Red_NIS']) if attr_cnt['Non_Red_NIS']!='' else 0
                ioSum[145] = int(attr_cnt['Red_ISLTR']) if attr_cnt['Red_ISLTR']!='' else 0
                ioSum[147] = int(attr_cnt['Future_Red_ISLTR']) if attr_cnt['Future_Red_ISLTR']!='' else 0
                ioSum[149] = int(attr_cnt['Non_Red_ISLTR']) if attr_cnt['Non_Red_ISLTR']!='' else 0
    for attr_cnt in EN:
        if attr_cnt['IO_Type'] in ['Series-C: HLAI (16) without HART with differential inputs (0-5000)']:
            ioSum[43] = int(attr_cnt['Red_IS']) if attr_cnt['Red_IS']!='' else 0
            ioSum[45] = int(attr_cnt['Future_Red_IS']) if attr_cnt['Future_Red_IS']!='' else 0
            ioSum[47] = int(attr_cnt['Non_Red_IS']) if attr_cnt['Non_Red_IS']!='' else 0
            ioSum[49] = int(attr_cnt['Red_NIS']) if attr_cnt['Red_NIS']!='' else 0
            ioSum[51] = int(attr_cnt['Future_Red_NIS']) if attr_cnt['Future_Red_NIS']!='' else 0
            ioSum[53] = int(attr_cnt['Non_Red_NIS']) if attr_cnt['Non_Red_NIS']!='' else 0
            ioSum[55] = int(attr_cnt['Red_ISLTR']) if attr_cnt['Red_ISLTR']!='' else 0
            ioSum[57] = int(attr_cnt['Future_Red_ISLTR']) if attr_cnt['Future_Red_ISLTR']!='' else 0
            ioSum[59] = int(attr_cnt['Non_Red_ISLTR']) if attr_cnt['Non_Red_ISLTR']!='' else 0
        if attr_cnt['IO_Type'] in ['SCM: HLAI (16) without HART with differential inputs (0-5000)']:
            ioSum[44] = int(attr_cnt['Red_IS']) if attr_cnt['Red_IS']!='' else 0
            ioSum[46] = int(attr_cnt['Future_Red_IS']) if attr_cnt['Future_Red_IS']!='' else 0
            ioSum[48] = int(attr_cnt['Non_Red_IS']) if attr_cnt['Non_Red_IS']!='' else 0
            ioSum[50] = int(attr_cnt['Red_NIS']) if attr_cnt['Red_NIS']!='' else 0
            ioSum[52] = int(attr_cnt['Future_Red_NIS']) if attr_cnt['Future_Red_NIS']!='' else 0
            ioSum[54] = int(attr_cnt['Non_Red_NIS']) if attr_cnt['Non_Red_NIS']!='' else 0
            ioSum[56] = int(attr_cnt['Red_ISLTR']) if attr_cnt['Red_ISLTR']!='' else 0
            ioSum[58] = int(attr_cnt['Future_Red_ISLTR']) if attr_cnt['Future_Red_ISLTR']!='' else 0
            ioSum[60] = int(attr_cnt['Non_Red_ISLTR']) if attr_cnt['Non_Red_ISLTR']!='' else 0
        if attr_cnt['IO_Type'] in ['Series-C: AO (16) HART (0-5000)']:
            ioSum[150] += int(attr_cnt['Red_IS']) if attr_cnt['Red_IS']!='' else 0
            ioSum[152] += int(attr_cnt['Future_Red_IS']) if attr_cnt['Future_Red_IS']!='' else 0
            ioSum[154] += int(attr_cnt['Non_Red_IS']) if attr_cnt['Non_Red_IS']!='' else 0
            ioSum[156] += int(attr_cnt['Red_NIS']) if attr_cnt['Red_NIS']!='' else 0
            ioSum[158] += int(attr_cnt['Future_Red_NIS']) if attr_cnt['Future_Red_NIS']!='' else 0
            ioSum[160] += int(attr_cnt['Non_Red_NIS']) if attr_cnt['Non_Red_NIS']!='' else 0
            ioSum[162] += int(attr_cnt['Red_ISLTR']) if attr_cnt['Red_ISLTR']!='' else 0
            ioSum[164] += int(attr_cnt['Future_Red_ISLTR']) if attr_cnt['Future_Red_ISLTR']!='' else 0
            ioSum[166] += int(attr_cnt['Non_Red_ISLTR']) if attr_cnt['Non_Red_ISLTR']!='' else 0
        if attr_cnt['IO_Type'] in ['SCM: AO (16) HART (0-5000)']:
            ioSum[151] += int(attr_cnt['Red_IS']) if attr_cnt['Red_IS']!='' else 0
            ioSum[153] += int(attr_cnt['Future_Red_IS']) if attr_cnt['Future_Red_IS']!='' else 0
            ioSum[155] += int(attr_cnt['Non_Red_IS']) if attr_cnt['Non_Red_IS']!='' else 0
            ioSum[157] += int(attr_cnt['Red_NIS']) if attr_cnt['Red_NIS']!='' else 0
            ioSum[159] += int(attr_cnt['Future_Red_NIS']) if attr_cnt['Future_Red_NIS']!='' else 0
            ioSum[161] += int(attr_cnt['Non_Red_NIS']) if attr_cnt['Non_Red_NIS']!='' else 0
            ioSum[163] += int(attr_cnt['Red_ISLTR']) if attr_cnt['Red_ISLTR']!='' else 0
            ioSum[165] += int(attr_cnt['Future_Red_ISLTR']) if attr_cnt['Future_Red_ISLTR']!='' else 0
            ioSum[167] += int(attr_cnt['Non_Red_ISLTR']) if attr_cnt['Non_Red_ISLTR']!='' else 0
        if attr_cnt['IO_Type'] in ['Series-C: HLAI (16) with HART with differential inputs (0-5000)']:
            ioSum[61] = int(attr_cnt['Red_IS']) if attr_cnt['Red_IS']!='' else 0
            ioSum[63] = int(attr_cnt['Future_Red_IS']) if attr_cnt['Future_Red_IS']!='' else 0
            ioSum[65] = int(attr_cnt['Non_Red_IS']) if attr_cnt['Non_Red_IS']!='' else 0
            ioSum[67] = int(attr_cnt['Red_NIS']) if attr_cnt['Red_NIS']!='' else 0
            ioSum[69] = int(attr_cnt['Future_Red_NIS']) if attr_cnt['Future_Red_NIS']!='' else 0
            ioSum[71] = int(attr_cnt['Non_Red_NIS']) if attr_cnt['Non_Red_NIS']!='' else 0
            ioSum[73] = int(attr_cnt['Red_ISLTR']) if attr_cnt['Red_ISLTR']!='' else 0
            ioSum[75] = int(attr_cnt['Future_Red_ISLTR']) if attr_cnt['Future_Red_ISLTR']!='' else 0
            ioSum[77] = int(attr_cnt['Non_Red_ISLTR']) if attr_cnt['Non_Red_ISLTR']!='' else 0 
        if attr_cnt['IO_Type'] in ['SCM: HLAI (16) with HART with differential inputs (0-5000)']:
            ioSum[62] = int(attr_cnt['Red_IS']) if attr_cnt['Red_IS']!='' else 0
            ioSum[64] = int(attr_cnt['Future_Red_IS']) if attr_cnt['Future_Red_IS']!='' else 0
            ioSum[66] = int(attr_cnt['Non_Red_IS']) if attr_cnt['Non_Red_IS']!='' else 0
            ioSum[68] = int(attr_cnt['Red_NIS']) if attr_cnt['Red_NIS']!='' else 0
            ioSum[70] = int(attr_cnt['Future_Red_NIS']) if attr_cnt['Future_Red_NIS']!='' else 0
            ioSum[72] = int(attr_cnt['Non_Red_NIS']) if attr_cnt['Non_Red_NIS']!='' else 0
            ioSum[74] = int(attr_cnt['Red_ISLTR']) if attr_cnt['Red_ISLTR']!='' else 0
            ioSum[76] = int(attr_cnt['Future_Red_ISLTR']) if attr_cnt['Future_Red_ISLTR']!='' else 0
            ioSum[78] = int(attr_cnt['Non_Red_ISLTR']) if attr_cnt['Non_Red_ISLTR']!='' else 0     

        if attr_cnt['IO_Type'] in ['Series-C: LLAI (1) Mux RTD (0-5000)']:
            ioSum[81] = int(attr_cnt['Non_Red_IS']) if attr_cnt['Non_Red_IS']!='' else 0
            ioSum[82] = int(attr_cnt['Non_Red_NIS']) if attr_cnt['Non_Red_NIS']!='' else 0
            ioSum[83] = int(attr_cnt['Non_Red_ISLTR']) if attr_cnt['Non_Red_ISLTR']!='' else 0
        if attr_cnt['IO_Type'] in ['Series-C: LLAI (1) Mux TC (0-5000)']:
            ioSum[84] = int(attr_cnt['Non_Red_IS']) if attr_cnt['Non_Red_IS']!='' else 0
            ioSum[85] = int(attr_cnt['Non_Red_NIS']) if attr_cnt['Non_Red_NIS']!='' else 0
            ioSum[86] = int(attr_cnt['Non_Red_ISLTR']) if attr_cnt['Non_Red_ISLTR']!='' else 0
        if attr_cnt['IO_Type'] in ['Series-C: LLAI (1) Mux TC Remote CJR (0-5000)']:
            ioSum[87] = int(attr_cnt['Non_Red_IS']) if attr_cnt['Non_Red_IS']!='' else 0
            ioSum[88] = int(attr_cnt['Non_Red_NIS']) if attr_cnt['Non_Red_NIS']!='' else 0
            ioSum[89] = int(attr_cnt['Non_Red_ISLTR']) if attr_cnt['Non_Red_ISLTR']!='' else 0
    for attr_cnt in UN:
        if attr_cnt['IO_Type'] in ['Series-C: UIO (32) Analog Input (HLAI Adapt) (0-5000)']:
            ioSum[102] = int(attr_cnt['Red_IS']) if attr_cnt['Red_IS']!='' else 0
            ioSum[104] = int(attr_cnt['Future_Red_IS']) if attr_cnt['Future_Red_IS']!='' else 0
            ioSum[106] = int(attr_cnt['Non_Red_IS']) if attr_cnt['Non_Red_IS']!='' else 0
            ioSum[108] = int(attr_cnt['Red_NIS']) if attr_cnt['Red_NIS']!='' else 0
            ioSum[110] = int(attr_cnt['Future_Red_NIS']) if attr_cnt['Future_Red_NIS']!='' else 0
            ioSum[112] = int(attr_cnt['Non_Red_NIS']) if attr_cnt['Non_Red_NIS']!='' else 0
            ioSum[114] = int(attr_cnt['Red_ISLTR']) if attr_cnt['Red_ISLTR']!='' else 0
            ioSum[116] = int(attr_cnt['Future_Red_ISLTR']) if attr_cnt['Future_Red_ISLTR']!='' else 0
            ioSum[118] = int(attr_cnt['Non_Red_ISLTR']) if attr_cnt['Non_Red_ISLTR']!='' else 0 
        if attr_cnt['IO_Type'] in ['SCM: UIO (32) Analog Input (HLAI Adapt) (0-5000)']:
            ioSum[103] = int(attr_cnt['Red_IS']) if attr_cnt['Red_IS']!='' else 0
            ioSum[105] = int(attr_cnt['Future_Red_IS']) if attr_cnt['Future_Red_IS']!='' else 0
            ioSum[107] = int(attr_cnt['Non_Red_IS']) if attr_cnt['Non_Red_IS']!='' else 0
            ioSum[109] = int(attr_cnt['Red_NIS']) if attr_cnt['Red_NIS']!='' else 0
            ioSum[111] = int(attr_cnt['Future_Red_NIS']) if attr_cnt['Future_Red_NIS']!='' else 0
            ioSum[113] = int(attr_cnt['Non_Red_NIS']) if attr_cnt['Non_Red_NIS']!='' else 0
            ioSum[115] = int(attr_cnt['Red_ISLTR']) if attr_cnt['Red_ISLTR']!='' else 0
            ioSum[117] = int(attr_cnt['Future_Red_ISLTR']) if attr_cnt['Future_Red_ISLTR']!='' else 0
            ioSum[119] = int(attr_cnt['Non_Red_ISLTR']) if attr_cnt['Non_Red_ISLTR']!='' else 0 
        
        if attr_cnt['IO_Type'] in ['Series-C: UIO (32) Analog Input (LLAI Adapt) (0-5000)']:
            ioSum[120] = int(attr_cnt['Red_ISLTR']) if attr_cnt['Red_ISLTR']!='' else 0
            ioSum[121] = int(attr_cnt['Future_Red_ISLTR']) if attr_cnt['Future_Red_ISLTR']!='' else 0
            ioSum[122] = int(attr_cnt['Non_Red_ISLTR']) if attr_cnt['Non_Red_ISLTR']!='' else 0

        if attr_cnt['IO_Type'] in ['Series-C: UIO (32) Analog Output (0-5000)']:
            ioSum[171] = int(attr_cnt['Red_IS']) if attr_cnt['Red_IS']!='' else 0
            ioSum[173] = int(attr_cnt['Future_Red_IS']) if attr_cnt['Future_Red_IS']!='' else 0
            ioSum[175] = int(attr_cnt['Non_Red_IS']) if attr_cnt['Non_Red_IS']!='' else 0
            ioSum[177] = int(attr_cnt['Red_NIS']) if attr_cnt['Red_NIS']!='' else 0
            ioSum[179] = int(attr_cnt['Future_Red_NIS']) if attr_cnt['Future_Red_NIS']!='' else 0
            ioSum[181] = int(attr_cnt['Non_Red_NIS']) if attr_cnt['Non_Red_NIS']!='' else 0
            ioSum[183] = int(attr_cnt['Red_ISLTR']) if attr_cnt['Red_ISLTR']!='' else 0
            ioSum[185] = int(attr_cnt['Future_Red_ISLTR']) if attr_cnt['Future_Red_ISLTR']!='' else 0
            ioSum[187] = int(attr_cnt['Non_Red_ISLTR']) if attr_cnt['Non_Red_ISLTR']!='' else 0
        if attr_cnt['IO_Type'] in ['SCM: UIO (32) Analog Output (0-5000)']:
            ioSum[172] = int(attr_cnt['Red_IS']) if attr_cnt['Red_IS']!='' else 0
            ioSum[174] = int(attr_cnt['Future_Red_IS']) if attr_cnt['Future_Red_IS']!='' else 0
            ioSum[176] = int(attr_cnt['Non_Red_IS']) if attr_cnt['Non_Red_IS']!='' else 0
            ioSum[178] = int(attr_cnt['Red_NIS']) if attr_cnt['Red_NIS']!='' else 0
            ioSum[180] = int(attr_cnt['Future_Red_NIS']) if attr_cnt['Future_Red_NIS']!='' else 0
            ioSum[182] = int(attr_cnt['Non_Red_NIS']) if attr_cnt['Non_Red_NIS']!='' else 0
            ioSum[184] = int(attr_cnt['Red_ISLTR']) if attr_cnt['Red_ISLTR']!='' else 0
            ioSum[186] = int(attr_cnt['Future_Red_ISLTR']) if attr_cnt['Future_Red_ISLTR']!='' else 0
            ioSum[188] = int(attr_cnt['Non_Red_ISLTR']) if attr_cnt['Non_Red_ISLTR']!='' else 0
    for attr_cnt in EN1:
        if attr_cnt['IO_Type'] in ['Series-C: DI (32) 24 VDC with Open Wire Detect (0-5000)']:
            ioSum[210] = int(attr_cnt['Red_IS']) if attr_cnt['Red_IS']!='' else 0
            ioSum[212] = int(attr_cnt['Future_Red_IS']) if attr_cnt['Future_Red_IS']!='' else 0
            ioSum[214] = int(attr_cnt['Non_Red_IS']) if attr_cnt['Non_Red_IS']!='' else 0
            ioSum[216] = int(attr_cnt['Red_NIS']) if attr_cnt['Red_NIS']!='' else 0
            ioSum[218] = int(attr_cnt['Future_Red_NIS']) if attr_cnt['Future_Red_NIS']!='' else 0
            ioSum[220] = int(attr_cnt['Non_Red_NIS']) if attr_cnt['Non_Red_NIS']!='' else 0
            ioSum[222] = int(attr_cnt['Red_ISLTR']) if attr_cnt['Red_ISLTR']!='' else 0
            ioSum[224] = int(attr_cnt['Future_Red_ISLTR']) if attr_cnt['Future_Red_ISLTR']!='' else 0
            ioSum[226] = int(attr_cnt['Non_Red_ISLTR']) if attr_cnt['Non_Red_ISLTR']!='' else 0 
            ioSum[228] = int(attr_cnt['Red_RLY']) if attr_cnt['Red_RLY']!='' else 0
            ioSum[230] = int(attr_cnt['Future_Red_RLY']) if attr_cnt['Future_Red_RLY']!='' else 0
            ioSum[232] = int(attr_cnt['Non_Red_RLY']) if attr_cnt['Non_Red_RLY']!='' else 0
            ioSum[563] = int(attr_cnt['Red_HV_Rly']) if attr_cnt['Red_HV_Rly']!='' else 0
            ioSum[565] = int(attr_cnt['Future_Red_HV_RLY']) if attr_cnt['Future_Red_HV_RLY']!='' else 0
            ioSum[567] = int(attr_cnt['Non_Red_HV_RLY']) if attr_cnt['Non_Red_HV_RLY']!='' else 0
        if attr_cnt['IO_Type'] in ['SCM: DI (32) 24 VDC with Open Wire Detect (0-5000)']:
            ioSum[211] = int(attr_cnt['Red_IS']) if attr_cnt['Red_IS']!='' else 0
            ioSum[213] = int(attr_cnt['Future_Red_IS']) if attr_cnt['Future_Red_IS']!='' else 0
            ioSum[215] = int(attr_cnt['Non_Red_IS']) if attr_cnt['Non_Red_IS']!='' else 0
            ioSum[217] = int(attr_cnt['Red_NIS']) if attr_cnt['Red_NIS']!='' else 0
            ioSum[219] = int(attr_cnt['Future_Red_NIS']) if attr_cnt['Future_Red_NIS']!='' else 0
            ioSum[221] = int(attr_cnt['Non_Red_NIS']) if attr_cnt['Non_Red_NIS']!='' else 0
            ioSum[223] = int(attr_cnt['Red_ISLTR']) if attr_cnt['Red_ISLTR']!='' else 0
            ioSum[225] = int(attr_cnt['Future_Red_ISLTR']) if attr_cnt['Future_Red_ISLTR']!='' else 0
            ioSum[227] = int(attr_cnt['Non_Red_ISLTR']) if attr_cnt['Non_Red_ISLTR']!='' else 0 
            ioSum[229] = int(attr_cnt['Red_RLY']) if attr_cnt['Red_RLY']!='' else 0
            ioSum[231] = int(attr_cnt['Future_Red_RLY']) if attr_cnt['Future_Red_RLY']!='' else 0
            ioSum[233] = int(attr_cnt['Non_Red_RLY']) if attr_cnt['Non_Red_RLY']!='' else 0
            ioSum[564] = int(attr_cnt['Red_HV_Rly']) if attr_cnt['Red_HV_Rly']!='' else 0
            ioSum[566] = int(attr_cnt['Future_HV_Rly']) if attr_cnt['Future_HV_Rly']!='' else 0
            ioSum[568] = int(attr_cnt['Non_Red_HV_Rly']) if attr_cnt['Non_Red_HV_Rly']!='' else 0
        if attr_cnt['IO_Type'] in ['Series-C: DI (32) 110 VAC (0-5000)']:
            ioSum[258] = int(attr_cnt['Red_NIS']) if attr_cnt['Red_NIS']!='' else 0
            ioSum[260] = int(attr_cnt['Future_Red_NIS']) if attr_cnt['Future_Red_NIS']!='' else 0
            ioSum[262] = int(attr_cnt['Non_Red_NIS']) if attr_cnt['Non_Red_NIS']!='' else 0
        if attr_cnt['IO_Type'] in ['SCM: DI (32) 110 VAC (0-5000)']:
            ioSum[259] = int(attr_cnt['Red_NIS']) if attr_cnt['Red_NIS']!='' else 0
            ioSum[261] = int(attr_cnt['Future_Red_NIS']) if attr_cnt['Future_Red_NIS']!='' else 0
            ioSum[263] = int(attr_cnt['Non_Red_NIS']) if attr_cnt['Non_Red_NIS']!='' else 0
        if attr_cnt['IO_Type'] in ['Series-C: DI (32) 110 VAC PROX (0-5000)']:
            ioSum[264] = int(attr_cnt['Non_Red_NIS']) if attr_cnt['Non_Red_NIS']!='' else 0
        if attr_cnt['IO_Type'] in ['SCm: DI (32) 110 VAC PROX (0-5000)']:
            ioSum[265] = int(attr_cnt['Non_Red_NIS']) if attr_cnt['Non_Red_NIS']!='' else 0
        if attr_cnt['IO_Type'] in ['Series-C: DI (32) 220 VAC (0-5000)']:
            ioSum[266] = int(attr_cnt['Red_NIS']) if attr_cnt['Red_NIS']!='' else 0
            ioSum[268] = int(attr_cnt['Future_Red_NIS']) if attr_cnt['Future_Red_NIS']!='' else 0
            ioSum[270] = int(attr_cnt['Non_Red_NIS']) if attr_cnt['Non_Red_NIS']!='' else 0
        if attr_cnt['IO_Type'] in ['SCM: DI (32) 220 VAC (0-5000)']:
            ioSum[267] = int(attr_cnt['Red_NIS']) if attr_cnt['Red_NIS']!='' else 0
            ioSum[269] = int(attr_cnt['Future_Red_NIS']) if attr_cnt['Future_Red_NIS']!='' else 0
            ioSum[271] = int(attr_cnt['Non_Red_NIS']) if attr_cnt['Non_Red_NIS']!='' else 0
        if attr_cnt['IO_Type'] in ['Series-C: DO (32) 24VDC Relay Bus above 30V (0-5000)']:
            ioSum[364] = int(attr_cnt['Red_RLY']) if attr_cnt['Red_RLY']!='' else 0
            ioSum[366] = int(attr_cnt['Future_Red_RLY']) if attr_cnt['Future_Red_RLY']!='' else 0
            ioSum[368] = int(attr_cnt['Non_Red_RLY']) if attr_cnt['Non_Red_RLY']!='' else 0
        if attr_cnt['IO_Type'] in ['SCM: DO (32) 24VDC Relay Bus above 30V (0-5000)']:
            ioSum[365] = int(attr_cnt['Red_RLY']) if attr_cnt['Red_RLY']!='' else 0
            ioSum[367] = int(attr_cnt['Future_Red_RLY']) if attr_cnt['Future_Red_RLY']!='' else 0
            ioSum[369] = int(attr_cnt['Non_Red_RLY']) if attr_cnt['Non_Red_RLY']!='' else 0
        if attr_cnt['IO_Type'] in ['Series-C: DO (32) 24VDC Relay Bus up to 30V (0-5000)']:
            ioSum[370] = int(attr_cnt['Red_RLY']) if attr_cnt['Red_RLY']!='' else 0
            ioSum[372] = int(attr_cnt['Future_Red_RLY']) if attr_cnt['Future_Red_RLY']!='' else 0
            ioSum[374] = int(attr_cnt['Non_Red_RLY']) if attr_cnt['Non_Red_RLY']!='' else 0
        if attr_cnt['IO_Type'] in ['SCM: DO (32) 24VDC Relay Bus up to 30V (0-5000)']:
            ioSum[371] = int(attr_cnt['Red_RLY']) if attr_cnt['Red_RLY']!='' else 0
            ioSum[373] = int(attr_cnt['Future_Red_RLY']) if attr_cnt['Future_Red_RLY']!='' else 0
            ioSum[375] = int(attr_cnt['Non_Red_RLY']) if attr_cnt['Non_Red_RLY']!='' else 0
        if attr_cnt['IO_Type'] in ['Series-C: Pulse Input (8) Single Channel (0-5000)','Series-C: Pulse Input (4) Dual Channel (0-5000)','Series-C: Pulse Input (2) Fast Cut Off Channel (0-5000)']:
            ioSum[90] += int(attr_cnt['Red_IS']) if attr_cnt['Red_IS']!='' else 0
            ioSum[92] += int(attr_cnt['Future_Red_IS']) if attr_cnt['Future_Red_IS']!='' else 0
            ioSum[94] += int(attr_cnt['Red_NIS']) if attr_cnt['Red_NIS']!='' else 0
            ioSum[96] += int(attr_cnt['Future_Red_NIS']) if attr_cnt['Future_Red_NIS']!='' else 0
            ioSum[98] += int(attr_cnt['Red_ISLTR']) if attr_cnt['Red_ISLTR']!='' else 0
            ioSum[100] += int(attr_cnt['Future_Red_ISLTR']) if attr_cnt['Future_Red_ISLTR']!='' else 0
        if attr_cnt['IO_Type'] in ['SCM: Pulse Input (8) Single Channel (0-5000)','SCM: Pulse Input (4) Dual Channel (0-5000)','SCM: Pulse Input (2) Fast Cut Off Channel (0-5000)']:
            ioSum[91] += int(attr_cnt['Red_IS']) if attr_cnt['Red_IS']!='' else 0
            ioSum[93] += int(attr_cnt['Future_Red_IS']) if attr_cnt['Future_Red_IS']!='' else 0
            ioSum[95] += int(attr_cnt['Red_NIS']) if attr_cnt['Red_NIS']!='' else 0
            ioSum[97] += int(attr_cnt['Future_Red_NIS']) if attr_cnt['Future_Red_NIS']!='' else 0
            ioSum[99] += int(attr_cnt['Red_ISLTR']) if attr_cnt['Red_ISLTR']!='' else 0
            ioSum[101] += int(attr_cnt['Future_Red_ISLTR']) if attr_cnt['Future_Red_ISLTR']!='' else 0
        if attr_cnt['IO_Type'] in ['Series-C: DI (32) 24VDC SOE (0-5000)']:
            ioSum[234] = int(attr_cnt['Red_IS']) if attr_cnt['Red_IS']!='' else 0
            ioSum[236] = int(attr_cnt['Future_Red_IS']) if attr_cnt['Future_Red_IS']!='' else 0
            ioSum[238] = int(attr_cnt['Non_Red_IS']) if attr_cnt['Non_Red_IS']!='' else 0
            ioSum[240] = int(attr_cnt['Red_NIS']) if attr_cnt['Red_NIS']!='' else 0
            ioSum[242] = int(attr_cnt['Future_Red_NIS']) if attr_cnt['Future_Red_NIS']!='' else 0
            ioSum[244] = int(attr_cnt['Non_Red_NIS']) if attr_cnt['Non_Red_NIS']!='' else 0
            ioSum[246] = int(attr_cnt['Red_ISLTR']) if attr_cnt['Red_ISLTR']!='' else 0
            ioSum[248] = int(attr_cnt['Future_Red_ISLTR']) if attr_cnt['Future_Red_ISLTR']!='' else 0
            ioSum[250] = int(attr_cnt['Non_Red_ISLTR']) if attr_cnt['Non_Red_ISLTR']!='' else 0 
            ioSum[252] = int(attr_cnt['Red_RLY']) if attr_cnt['Red_RLY']!='' else 0
            ioSum[254] = int(attr_cnt['Future_Red_RLY']) if attr_cnt['Future_Red_RLY']!='' else 0
            ioSum[256] = int(attr_cnt['Non_Red_RLY']) if attr_cnt['Non_Red_RLY']!='' else 0
            ioSum[569] = int(attr_cnt['Red_HV_RLY']) if attr_cnt['Red_HV_RLY']!='' else 0
            ioSum[571] = int(attr_cnt['Future_Red_HV_RLY']) if attr_cnt['Future_Red_HV_RLY']!='' else 0
            ioSum[573] = int(attr_cnt['Non_Red_HV_RLY']) if attr_cnt['Non_Red_HV_RLY']!='' else 0
    for attr_cnt in UN1:
        if attr_cnt['IO_Type'] in ['Series-C: UIO (32) Digital Input (0-5000)']:
            ioSum[280] = int(attr_cnt['Red_IS']) if attr_cnt['Red_IS']!='' else 0
            ioSum[282] = int(attr_cnt['Future_Red_IS']) if attr_cnt['Future_Red_IS']!='' else 0
            ioSum[284] = int(attr_cnt['Non_Red_IS']) if attr_cnt['Non_Red_IS']!='' else 0
            ioSum[286] = int(attr_cnt['Red_NIS']) if attr_cnt['Red_NIS']!='' else 0
            ioSum[288] = int(attr_cnt['Future_Red_NIS']) if attr_cnt['Future_Red_NIS']!='' else 0
            ioSum[290] = int(attr_cnt['Non_Red_NIS']) if attr_cnt['Non_Red_NIS']!='' else 0
            ioSum[292] = int(attr_cnt['Red_ISLTR']) if attr_cnt['Red_ISLTR']!='' else 0
            ioSum[294] = int(attr_cnt['Future_Red_ISLTR']) if attr_cnt['Future_Red_ISLTR']!='' else 0
            ioSum[296] = int(attr_cnt['Non_Red_ISLTR']) if attr_cnt['Non_Red_ISLTR']!='' else 0 
            ioSum[298] = int(attr_cnt['Red_RLY']) if attr_cnt['Red_RLY']!='' else 0
            ioSum[300] = int(attr_cnt['Future_Red_RLY']) if attr_cnt['Future_Red_RLY']!='' else 0
            ioSum[302] = int(attr_cnt['Non_Red_RLY']) if attr_cnt['Non_Red_RLY']!='' else 0
            ioSum[575] = int(attr_cnt['Red_HV_RLY']) if attr_cnt['Red_HV_RLY']!='' else 0
            ioSum[577] = int(attr_cnt['Future_Red_HV_RLY']) if attr_cnt['Future_Red_HV_RLY']!='' else 0
            ioSum[578] = int(attr_cnt['Non_Red_HV_RLY']) if attr_cnt['Non_Red_HV_RLY']!='' else 0
        if attr_cnt['IO_Type'] in ['SCM: UIO (32) Digital Input (0-5000)']:
            ioSum[281] = int(attr_cnt['Red_IS']) if attr_cnt['Red_IS']!='' else 0
            ioSum[283] = int(attr_cnt['Future_Red_IS']) if attr_cnt['Future_Red_IS']!='' else 0
            ioSum[285] = int(attr_cnt['Non_Red_IS']) if attr_cnt['Non_Red_IS']!='' else 0
            ioSum[287] = int(attr_cnt['Red_NIS']) if attr_cnt['Red_NIS']!='' else 0
            ioSum[289] = int(attr_cnt['Future_Red_NIS']) if attr_cnt['Future_Red_NIS']!='' else 0
            ioSum[291] = int(attr_cnt['Non_Red_NIS']) if attr_cnt['Non_Red_NIS']!='' else 0
            ioSum[293] = int(attr_cnt['Red_ISLTR']) if attr_cnt['Red_ISLTR']!='' else 0
            ioSum[295] = int(attr_cnt['Future_Red_ISLTR']) if attr_cnt['Future_Red_ISLTR']!='' else 0
            ioSum[297] = int(attr_cnt['Non_Red_ISLTR']) if attr_cnt['Non_Red_ISLTR']!='' else 0 
            ioSum[299] = int(attr_cnt['Red_RLY']) if attr_cnt['Red_RLY']!='' else 0
            ioSum[301] = int(attr_cnt['Future_Red_RLY']) if attr_cnt['Future_Red_RLY']!='' else 0
            ioSum[303] = int(attr_cnt['Non_Red_RLY']) if attr_cnt['Non_Red_RLY']!='' else 0
            ioSum[576] = int(attr_cnt['Red_HV_Rly']) if attr_cnt['Red_HV_Rly']!='' else 0
            ioSum[579] = int(attr_cnt['Future_HV_Rly']) if attr_cnt['Future_HV_Rly']!='' else 0
            ioSum[580] = int(attr_cnt['Non_Red_HV_Rly']) if attr_cnt['Non_Red_HV_Rly']!='' else 0
        if attr_cnt['IO_Type'] in ['Series-C: UIO (32) Digital Output (0-5000)']:
            ioSum[377] = int(attr_cnt['Red_IS']) if attr_cnt['Red_IS']!='' else 0
            ioSum[379] = int(attr_cnt['Future_Red_IS']) if attr_cnt['Future_Red_IS']!='' else 0
            ioSum[381] = int(attr_cnt['Non_Red_IS']) if attr_cnt['Non_Red_IS']!='' else 0
            ioSum[383] = int(attr_cnt['Red_NIS']) if attr_cnt['Red_NIS']!='' else 0
            ioSum[385] = int(attr_cnt['Future_Red_NIS']) if attr_cnt['Future_Red_NIS']!='' else 0
            ioSum[387] = int(attr_cnt['Non_Red_NIS']) if attr_cnt['Non_Red_NIS']!='' else 0
            ioSum[389] = int(attr_cnt['Red_ISLTR']) if attr_cnt['Red_ISLTR']!='' else 0
            ioSum[391] = int(attr_cnt['Future_Red_ISLTR']) if attr_cnt['Future_Red_ISLTR']!='' else 0
            ioSum[393] = int(attr_cnt['Non_Red_ISLTR']) if attr_cnt['Non_Red_ISLTR']!='' else 0 
            ioSum[395] = int(attr_cnt['Red_RLY']) if attr_cnt['Red_RLY']!='' else 0
            ioSum[397] = int(attr_cnt['Future_Red_RLY']) if attr_cnt['Future_Red_RLY']!='' else 0
            ioSum[399] = int(attr_cnt['Non_Red_RLY']) if attr_cnt['Non_Red_RLY']!='' else 0
            ioSum[596] = int(attr_cnt['Red_HV_RLY']) if attr_cnt['Red_HV_RLY']!='' else 0
            ioSum[598] = int(attr_cnt['Future_Red_HV_RLY']) if attr_cnt['Future_Red_HV_RLY']!='' else 0
            ioSum[600] = int(attr_cnt['Non_Red_HV_RLY']) if attr_cnt['Non_Red_HV_RLY']!='' else 0
        if attr_cnt['IO_Type'] in ['SCM: UIO (32) Digital Output (0-5000)']:
            ioSum[378] = int(attr_cnt['Red_IS']) if attr_cnt['Red_IS']!='' else 0
            ioSum[380] = int(attr_cnt['Future_Red_IS']) if attr_cnt['Future_Red_IS']!='' else 0
            ioSum[382] = int(attr_cnt['Non_Red_IS']) if attr_cnt['Non_Red_IS']!='' else 0
            ioSum[384] = int(attr_cnt['Red_NIS']) if attr_cnt['Red_NIS']!='' else 0
            ioSum[386] = int(attr_cnt['Future_Red_NIS']) if attr_cnt['Future_Red_NIS']!='' else 0
            ioSum[388] = int(attr_cnt['Non_Red_NIS']) if attr_cnt['Non_Red_NIS']!='' else 0
            ioSum[390] = int(attr_cnt['Red_ISLTR']) if attr_cnt['Red_ISLTR']!='' else 0
            ioSum[392] = int(attr_cnt['Future_Red_ISLTR']) if attr_cnt['Future_Red_ISLTR']!='' else 0
            ioSum[394] = int(attr_cnt['Non_Red_ISLTR']) if attr_cnt['Non_Red_ISLTR']!='' else 0 
            ioSum[396] = int(attr_cnt['Red_RLY']) if attr_cnt['Red_RLY']!='' else 0
            ioSum[398] = int(attr_cnt['Future_Red_RLY']) if attr_cnt['Future_Red_RLY']!='' else 0
            ioSum[303] = int(attr_cnt['Non_Red_RLY']) if attr_cnt['Non_Red_RLY']!='' else 0
            ioSum[597] = int(attr_cnt['Red_HV_Rly']) if attr_cnt['Red_HV_Rly']!='' else 0
            ioSum[599] = int(attr_cnt['Future_HV_Rly']) if attr_cnt['Future_HV_Rly']!='' else 0
            ioSum[601] = int(attr_cnt['Non_Red_HV_Rly']) if attr_cnt['Non_Red_HV_Rly']!='' else 0
    return ioSum