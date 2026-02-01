def populateC300RGData1(Quote,rg):
    n =0
    rgIoSum = [0] * 800
    rg=rg
    ms_attr =rg.SelectedAttributes.GetContainerByName("Document_cont_c3001").Rows
    for io_f in ms_attr:
        io_Family=io_f['Io_family']
        Trace.Write('Io_family '+str(io_f['Io_family']))
        Mounting_Solution=io_f['Dummy_RG_IO_Mounting_Solution']
        Trace.Write('Io_family '+str(io_f['Dummy_RG_IO_Mounting_Solution']))
        if io_Family=="Mark2" and Mounting_Solution !='Yes':
            MS = rg.SelectedAttributes.GetContainerByName("C300_C IO_RG MS2").Rows
            EN = rg.SelectedAttributes.GetContainerByName("C300_SerC_Enhanced_Function_IO_Mark_Group_RG_Cont").Rows
            EN1 = rg.SelectedAttributes.GetContainerByName("C300_SerC_Enhanced_Function_IO_Mark_Group_RG_Cont1").Rows
            UN = rg.SelectedAttributes.GetContainerByName("C300_CG_Universal_IO_Mark_1").Rows
            UN1 = rg.SelectedAttributes.GetContainerByName("C300_CG_Universal_IO_Mark_2").Rows
        elif io_Family=="seriesC" and Mounting_Solution !='Yes':
            MS = rg.SelectedAttributes.GetContainerByName("C300_C IO_RG MS").Rows
            EN = rg.SelectedAttributes.GetContainerByName("SerC_RG_Enhanced_Function_IO_Cont").Rows
            EN1 = rg.SelectedAttributes.GetContainerByName("SerC_RG_Enhanced_Function_IO_Cont2").Rows
            UN = rg.SelectedAttributes.GetContainerByName("C300_RG_Universal_IO_cont_1").Rows
            UN1 = rg.SelectedAttributes.GetContainerByName("C300_RG_Universal_IO_cont_2").Rows
        elif io_Family=="TurboM" and Mounting_Solution !='Yes':
            EN = rg.SelectedAttributes.GetContainerByName("SerC_RG_Enhanced_Function_IO_Cont").Rows
            EN1 = rg.SelectedAttributes.GetContainerByName("SerC_RG_Enhanced_Function_IO_Cont2").Rows
            UN = rg.SelectedAttributes.GetContainerByName("C300_RG_Universal_IO_cont_1").Rows
            UN1 = rg.SelectedAttributes.GetContainerByName("C300_RG_Universal_IO_cont_2").Rows
    if io_Family !="TurboM" and Mounting_Solution !='Yes':
        for attr_cnt in MS:
            if attr_cnt['IO_Type'] in ['Series-C: HLAI (16) 4-20mA (0-5000)']:
                rgIoSum[1] = int(attr_cnt['Red_IS']) if attr_cnt['Red_IS']!='' else 0
                rgIoSum[3] = int(attr_cnt['Future_Red_IS']) if attr_cnt['Future_Red_IS']!='' else 0
                rgIoSum[5] = int(attr_cnt['Non_Red_IS']) if attr_cnt['Non_Red_IS']!='' else 0
                rgIoSum[7] = int(attr_cnt['Red_NIS']) if attr_cnt['Red_NIS']!='' else 0
                rgIoSum[9] = int(attr_cnt['Future_Red_NIS']) if attr_cnt['Future_Red_NIS']!='' else 0
                rgIoSum[11] = int(attr_cnt['Non_Red_NIS']) if attr_cnt['Non_Red_NIS']!='' else 0
                rgIoSum[13] = int(attr_cnt['Red_ISLTR']) if attr_cnt['Red_ISLTR']!='' else 0
                rgIoSum[15] = int(attr_cnt['Future_Red_ISLTR']) if attr_cnt['Future_Red_ISLTR']!='' else 0
                rgIoSum[17] = int(attr_cnt['Non_Red_ISLTR']) if attr_cnt['Non_Red_ISLTR']!='' else 0
            if attr_cnt['IO_Type'] in ['SCM: HLAI (16) 4-20mA (0-5000)']:
                rgIoSum[2] = int(attr_cnt['Red_IS']) if attr_cnt['Red_IS']!='' else 0
                rgIoSum[4] = int(attr_cnt['Future_Red_IS']) if attr_cnt['Future_Red_IS']!='' else 0
                rgIoSum[6] = int(attr_cnt['Non_Red_IS']) if attr_cnt['Non_Red_IS']!='' else 0
                rgIoSum[8] = int(attr_cnt['Red_NIS']) if attr_cnt['Red_NIS']!='' else 0
                rgIoSum[10] = int(attr_cnt['Future_Red_NIS']) if attr_cnt['Future_Red_NIS']!='' else 0
                rgIoSum[12] = int(attr_cnt['Non_Red_NIS']) if attr_cnt['Non_Red_NIS']!='' else 0
                rgIoSum[14] = int(attr_cnt['Red_ISLTR']) if attr_cnt['Red_ISLTR']!='' else 0
                rgIoSum[16] = int(attr_cnt['Future_Red_ISLTR']) if attr_cnt['Future_Red_ISLTR']!='' else 0
                rgIoSum[18] = int(attr_cnt['Non_Red_ISLTR']) if attr_cnt['Non_Red_ISLTR']!='' else 0
            if attr_cnt['IO_Type'] in ['Series-C: AO (16) HART Config/Status (0-5000)']:
                rgIoSum[150] += int(attr_cnt['Red_IS']) if attr_cnt['Red_IS']!='' else 0
                rgIoSum[152] += int(attr_cnt['Future_Red_IS']) if attr_cnt['Future_Red_IS']!='' else 0
                rgIoSum[154] += int(attr_cnt['Non_Red_IS']) if attr_cnt['Non_Red_IS']!='' else 0
                rgIoSum[156] += int(attr_cnt['Red_NIS']) if attr_cnt['Red_NIS']!='' else 0
                rgIoSum[158] += int(attr_cnt['Future_Red_NIS']) if attr_cnt['Future_Red_NIS']!='' else 0
                rgIoSum[160] += int(attr_cnt['Non_Red_NIS']) if attr_cnt['Non_Red_NIS']!='' else 0
                rgIoSum[162] += int(attr_cnt['Red_ISLTR']) if attr_cnt['Red_ISLTR']!='' else 0
                rgIoSum[164] += int(attr_cnt['Future_Red_ISLTR']) if attr_cnt['Future_Red_ISLTR']!='' else 0
                rgIoSum[166] += int(attr_cnt['Non_Red_ISLTR']) if attr_cnt['Non_Red_ISLTR']!='' else 0
            if attr_cnt['IO_Type'] in ['SCM: AO (16) HART Config/Status (0-5000)']:
                rgIoSum[151] += int(attr_cnt['Red_IS']) if attr_cnt['Red_IS']!='' else 0
                rgIoSum[153] += int(attr_cnt['Future_Red_IS']) if attr_cnt['Future_Red_IS']!='' else 0
                rgIoSum[155] += int(attr_cnt['Non_Red_IS']) if attr_cnt['Non_Red_IS']!='' else 0
                rgIoSum[157] += int(attr_cnt['Red_NIS']) if attr_cnt['Red_NIS']!='' else 0
                rgIoSum[159] += int(attr_cnt['Future_Red_NIS']) if attr_cnt['Future_Red_NIS']!='' else 0
                rgIoSum[161] += int(attr_cnt['Non_Red_NIS']) if attr_cnt['Non_Red_NIS']!='' else 0
                rgIoSum[163] += int(attr_cnt['Red_ISLTR']) if attr_cnt['Red_ISLTR']!='' else 0
                rgIoSum[165] += int(attr_cnt['Future_Red_ISLTR']) if attr_cnt['Future_Red_ISLTR']!='' else 0
                rgIoSum[167] += int(attr_cnt['Non_Red_ISLTR']) if attr_cnt['Non_Red_ISLTR']!='' else 0
            if attr_cnt['IO_Type'] in ['Series-C: LLAI (16) (0-5000)']:
                rgIoSum[79] = int(attr_cnt['Non_Red_NIS']) if attr_cnt['Non_Red_NIS']!='' else 0
            if attr_cnt['IO_Type'] in ['SCM: LLAI (16) (0-5000)']:
                rgIoSum[80] = int(attr_cnt['Non_Red_NIS']) if attr_cnt['Non_Red_NIS']!='' else 0
            if attr_cnt['IO_Type'] in ['Series-C: HLAI (16) HART Config/Status (0-5000)']:
                rgIoSum[22] = int(attr_cnt['Red_IS']) if attr_cnt['Red_IS']!='' else 0
                rgIoSum[24] = int(attr_cnt['Future_Red_IS']) if attr_cnt['Future_Red_IS']!='' else 0
                rgIoSum[26] = int(attr_cnt['Non_Red_IS']) if attr_cnt['Non_Red_IS']!='' else 0
                rgIoSum[28] = int(attr_cnt['Red_NIS']) if attr_cnt['Red_NIS']!='' else 0
                rgIoSum[30] = int(attr_cnt['Future_Red_NIS']) if attr_cnt['Future_Red_NIS']!='' else 0
                rgIoSum[32] = int(attr_cnt['Non_Red_NIS']) if attr_cnt['Non_Red_NIS']!='' else 0
                rgIoSum[34] = int(attr_cnt['Red_ISLTR']) if attr_cnt['Red_ISLTR']!='' else 0
                rgIoSum[36] = int(attr_cnt['Future_Red_ISLTR']) if attr_cnt['Future_Red_ISLTR']!='' else 0
                rgIoSum[38] = int(attr_cnt['Non_Red_ISLTR']) if attr_cnt['Non_Red_ISLTR']!='' else 0
            if attr_cnt['IO_Type'] in ['SCM: HLAI (16) HART Config/Status (0-5000)']:
                rgIoSum[23] = int(attr_cnt['Red_IS']) if attr_cnt['Red_IS']!='' else 0
                rgIoSum[25] = int(attr_cnt['Future_Red_IS']) if attr_cnt['Future_Red_IS']!='' else 0
                rgIoSum[27] = int(attr_cnt['Non_Red_IS']) if attr_cnt['Non_Red_IS']!='' else 0
                rgIoSum[29] = int(attr_cnt['Red_NIS']) if attr_cnt['Red_NIS']!='' else 0
                rgIoSum[31] = int(attr_cnt['Future_Red_NIS']) if attr_cnt['Future_Red_NIS']!='' else 0
                rgIoSum[33] = int(attr_cnt['Non_Red_NIS']) if attr_cnt['Non_Red_NIS']!='' else 0
                rgIoSum[35] = int(attr_cnt['Red_ISLTR']) if attr_cnt['Red_ISLTR']!='' else 0
                rgIoSum[37] = int(attr_cnt['Future_Red_ISLTR']) if attr_cnt['Future_Red_ISLTR']!='' else 0
                rgIoSum[39] = int(attr_cnt['Non_Red_ISLTR']) if attr_cnt['Non_Red_ISLTR']!='' else 0
            if attr_cnt['IO_Type'] in ['Series-C: AO (16) (0-5000)']:
                rgIoSum[132] = int(attr_cnt['Red_IS']) if attr_cnt['Red_IS']!='' else 0
                rgIoSum[134] = int(attr_cnt['Future_Red_IS']) if attr_cnt['Future_Red_IS']!='' else 0
                rgIoSum[136] = int(attr_cnt['Non_Red_IS']) if attr_cnt['Non_Red_IS']!='' else 0
                rgIoSum[138] = int(attr_cnt['Red_NIS']) if attr_cnt['Red_NIS']!='' else 0
                rgIoSum[140] = int(attr_cnt['Future_Red_NIS']) if attr_cnt['Future_Red_NIS']!='' else 0
                rgIoSum[142] = int(attr_cnt['Non_Red_NIS']) if attr_cnt['Non_Red_NIS']!='' else 0
                rgIoSum[144] = int(attr_cnt['Red_ISLTR']) if attr_cnt['Red_ISLTR']!='' else 0
                rgIoSum[146] = int(attr_cnt['Future_Red_ISLTR']) if attr_cnt['Future_Red_ISLTR']!='' else 0
                rgIoSum[148] = int(attr_cnt['Non_Red_ISLTR']) if attr_cnt['Non_Red_ISLTR']!='' else 0
            if attr_cnt['IO_Type'] in ['SCM: AO (16) (0-5000)']:
                rgIoSum[133] = int(attr_cnt['Red_IS']) if attr_cnt['Red_IS']!='' else 0
                rgIoSum[135] = int(attr_cnt['Future_Red_IS']) if attr_cnt['Future_Red_IS']!='' else 0
                rgIoSum[137] = int(attr_cnt['Non_Red_IS']) if attr_cnt['Non_Red_IS']!='' else 0
                rgIoSum[139] = int(attr_cnt['Red_NIS']) if attr_cnt['Red_NIS']!='' else 0
                rgIoSum[141] = int(attr_cnt['Future_Red_NIS']) if attr_cnt['Future_Red_NIS']!='' else 0
                rgIoSum[143] = int(attr_cnt['Non_Red_NIS']) if attr_cnt['Non_Red_NIS']!='' else 0
                rgIoSum[145] = int(attr_cnt['Red_ISLTR']) if attr_cnt['Red_ISLTR']!='' else 0
                rgIoSum[147] = int(attr_cnt['Future_Red_ISLTR']) if attr_cnt['Future_Red_ISLTR']!='' else 0
                rgIoSum[149] = int(attr_cnt['Non_Red_ISLTR']) if attr_cnt['Non_Red_ISLTR']!='' else 0
    if Mounting_Solution !='Yes':
        for attr_cnt in EN:
            if attr_cnt['IO_Type'] in ['Series-C: HLAI (16) without HART with differential inputs (0-5000)']:
                rgIoSum[43] = int(attr_cnt['Red_IS']) if attr_cnt['Red_IS']!='' else 0
                rgIoSum[45] = int(attr_cnt['Future_Red_IS']) if attr_cnt['Future_Red_IS']!='' else 0
                rgIoSum[47] = int(attr_cnt['Non_Red_IS']) if attr_cnt['Non_Red_IS']!='' else 0
                rgIoSum[49] = int(attr_cnt['Red_NIS']) if attr_cnt['Red_NIS']!='' else 0
                rgIoSum[51] = int(attr_cnt['Future_Red_NIS']) if attr_cnt['Future_Red_NIS']!='' else 0
                rgIoSum[53] = int(attr_cnt['Non_Red_NIS']) if attr_cnt['Non_Red_NIS']!='' else 0
                rgIoSum[55] = int(attr_cnt['Red_ISLTR']) if attr_cnt['Red_ISLTR']!='' else 0
                rgIoSum[57] = int(attr_cnt['Future_Red_ISLTR']) if attr_cnt['Future_Red_ISLTR']!='' else 0
                rgIoSum[59] = int(attr_cnt['Non_Red_ISLTR']) if attr_cnt['Non_Red_ISLTR']!='' else 0
            if attr_cnt['IO_Type'] in ['SCM: HLAI (16) without HART with differential inputs (0-5000)']:
                rgIoSum[44] = int(attr_cnt['Red_IS']) if attr_cnt['Red_IS']!='' else 0
                rgIoSum[46] = int(attr_cnt['Future_Red_IS']) if attr_cnt['Future_Red_IS']!='' else 0
                rgIoSum[48] = int(attr_cnt['Non_Red_IS']) if attr_cnt['Non_Red_IS']!='' else 0
                rgIoSum[50] = int(attr_cnt['Red_NIS']) if attr_cnt['Red_NIS']!='' else 0
                rgIoSum[52] = int(attr_cnt['Future_Red_NIS']) if attr_cnt['Future_Red_NIS']!='' else 0
                rgIoSum[54] = int(attr_cnt['Non_Red_NIS']) if attr_cnt['Non_Red_NIS']!='' else 0
                rgIoSum[56] = int(attr_cnt['Red_ISLTR']) if attr_cnt['Red_ISLTR']!='' else 0
                rgIoSum[58] = int(attr_cnt['Future_Red_ISLTR']) if attr_cnt['Future_Red_ISLTR']!='' else 0
                rgIoSum[60] = int(attr_cnt['Non_Red_ISLTR']) if attr_cnt['Non_Red_ISLTR']!='' else 0
            if attr_cnt['IO_Type'] in ['Series-C: AO (16) HART (0-5000)']:
                rgIoSum[150] += int(attr_cnt['Red_IS']) if attr_cnt['Red_IS']!='' else 0
                rgIoSum[152] += int(attr_cnt['Future_Red_IS']) if attr_cnt['Future_Red_IS']!='' else 0
                rgIoSum[154] += int(attr_cnt['Non_Red_IS']) if attr_cnt['Non_Red_IS']!='' else 0
                rgIoSum[156] += int(attr_cnt['Red_NIS']) if attr_cnt['Red_NIS']!='' else 0
                rgIoSum[158] += int(attr_cnt['Future_Red_NIS']) if attr_cnt['Future_Red_NIS']!='' else 0
                rgIoSum[160] += int(attr_cnt['Non_Red_NIS']) if attr_cnt['Non_Red_NIS']!='' else 0
                rgIoSum[162] += int(attr_cnt['Red_ISLTR']) if attr_cnt['Red_ISLTR']!='' else 0
                rgIoSum[164] += int(attr_cnt['Future_Red_ISLTR']) if attr_cnt['Future_Red_ISLTR']!='' else 0
                rgIoSum[166] += int(attr_cnt['Non_Red_ISLTR']) if attr_cnt['Non_Red_ISLTR']!='' else 0
            if attr_cnt['IO_Type'] in ['SCM: AO (16) HART (0-5000)']:
                rgIoSum[151] += int(attr_cnt['Red_IS']) if attr_cnt['Red_IS']!='' else 0
                rgIoSum[153] += int(attr_cnt['Future_Red_IS']) if attr_cnt['Future_Red_IS']!='' else 0
                rgIoSum[155] += int(attr_cnt['Non_Red_IS']) if attr_cnt['Non_Red_IS']!='' else 0
                rgIoSum[157] += int(attr_cnt['Red_NIS']) if attr_cnt['Red_NIS']!='' else 0
                rgIoSum[159] += int(attr_cnt['Future_Red_NIS']) if attr_cnt['Future_Red_NIS']!='' else 0
                rgIoSum[161] += int(attr_cnt['Non_Red_NIS']) if attr_cnt['Non_Red_NIS']!='' else 0
                rgIoSum[163] += int(attr_cnt['Red_ISLTR']) if attr_cnt['Red_ISLTR']!='' else 0
                rgIoSum[165] += int(attr_cnt['Future_Red_ISLTR']) if attr_cnt['Future_Red_ISLTR']!='' else 0
                rgIoSum[167] += int(attr_cnt['Non_Red_ISLTR']) if attr_cnt['Non_Red_ISLTR']!='' else 0
            if attr_cnt['IO_Type'] in ['Series-C: HLAI (16) with HART with differential inputs (0-5000)']:
                rgIoSum[61] = int(attr_cnt['Red_IS']) if attr_cnt['Red_IS']!='' else 0
                rgIoSum[63] = int(attr_cnt['Future_Red_IS']) if attr_cnt['Future_Red_IS']!='' else 0
                rgIoSum[65] = int(attr_cnt['Non_Red_IS']) if attr_cnt['Non_Red_IS']!='' else 0
                rgIoSum[67] = int(attr_cnt['Red_NIS']) if attr_cnt['Red_NIS']!='' else 0
                rgIoSum[69] = int(attr_cnt['Future_Red_NIS']) if attr_cnt['Future_Red_NIS']!='' else 0
                rgIoSum[71] = int(attr_cnt['Non_Red_NIS']) if attr_cnt['Non_Red_NIS']!='' else 0
                rgIoSum[73] = int(attr_cnt['Red_ISLTR']) if attr_cnt['Red_ISLTR']!='' else 0
                rgIoSum[75] = int(attr_cnt['Future_Red_ISLTR']) if attr_cnt['Future_Red_ISLTR']!='' else 0
                rgIoSum[77] = int(attr_cnt['Non_Red_ISLTR']) if attr_cnt['Non_Red_ISLTR']!='' else 0 
            if attr_cnt['IO_Type'] in ['SCM: HLAI (16) with HART with differential inputs (0-5000)']:
                rgIoSum[62] = int(attr_cnt['Red_IS']) if attr_cnt['Red_IS']!='' else 0
                rgIoSum[64] = int(attr_cnt['Future_Red_IS']) if attr_cnt['Future_Red_IS']!='' else 0
                rgIoSum[66] = int(attr_cnt['Non_Red_IS']) if attr_cnt['Non_Red_IS']!='' else 0
                rgIoSum[68] = int(attr_cnt['Red_NIS']) if attr_cnt['Red_NIS']!='' else 0
                rgIoSum[70] = int(attr_cnt['Future_Red_NIS']) if attr_cnt['Future_Red_NIS']!='' else 0
                rgIoSum[72] = int(attr_cnt['Non_Red_NIS']) if attr_cnt['Non_Red_NIS']!='' else 0
                rgIoSum[74] = int(attr_cnt['Red_ISLTR']) if attr_cnt['Red_ISLTR']!='' else 0
                rgIoSum[76] = int(attr_cnt['Future_Red_ISLTR']) if attr_cnt['Future_Red_ISLTR']!='' else 0
                rgIoSum[78] = int(attr_cnt['Non_Red_ISLTR']) if attr_cnt['Non_Red_ISLTR']!='' else 0     
            if attr_cnt['IO_Type'] in ['Series-C: LLAI (1) Mux RTD (0-5000)']:
                rgIoSum[81] = int(attr_cnt['Non_Red_IS']) if attr_cnt['Non_Red_IS']!='' else 0
                rgIoSum[82] = int(attr_cnt['Non_Red_NIS']) if attr_cnt['Non_Red_NIS']!='' else 0
                rgIoSum[83] = int(attr_cnt['Non_Red_ISLTR']) if attr_cnt['Non_Red_ISLTR']!='' else 0
            if attr_cnt['IO_Type'] in ['Series-C: LLAI (1) Mux TC (0-5000)']:
                rgIoSum[84] = int(attr_cnt['Non_Red_IS']) if attr_cnt['Non_Red_IS']!='' else 0
                rgIoSum[85] = int(attr_cnt['Non_Red_NIS']) if attr_cnt['Non_Red_NIS']!='' else 0
                rgIoSum[86] = int(attr_cnt['Non_Red_ISLTR']) if attr_cnt['Non_Red_ISLTR']!='' else 0
            if attr_cnt['IO_Type'] in ['Series-C: LLAI (1) Mux TC Remote CJR (0-5000)']:
                rgIoSum[87] = int(attr_cnt['Non_Red_IS']) if attr_cnt['Non_Red_IS']!='' else 0
                rgIoSum[88] = int(attr_cnt['Non_Red_NIS']) if attr_cnt['Non_Red_NIS']!='' else 0
                rgIoSum[89] = int(attr_cnt['Non_Red_ISLTR']) if attr_cnt['Non_Red_ISLTR']!='' else 0
    if Mounting_Solution !='Yes':
        for attr_cnt in UN:
            if attr_cnt['IO_Type'] in ['Series-C: UIO (32) Analog Input (HLAI Adapt) (0-5000)']:
                rgIoSum[102] = int(attr_cnt['Red_IS']) if attr_cnt['Red_IS']!='' else 0
                rgIoSum[104] = int(attr_cnt['Future_Red_IS']) if attr_cnt['Future_Red_IS']!='' else 0
                rgIoSum[106] = int(attr_cnt['Non_Red_IS']) if attr_cnt['Non_Red_IS']!='' else 0
                rgIoSum[108] = int(attr_cnt['Red_NIS']) if attr_cnt['Red_NIS']!='' else 0
                rgIoSum[110] = int(attr_cnt['Future_Red_NIS']) if attr_cnt['Future_Red_NIS']!='' else 0
                rgIoSum[112] = int(attr_cnt['Non_Red_NIS']) if attr_cnt['Non_Red_NIS']!='' else 0
                rgIoSum[114] = int(attr_cnt['Red_ISLTR']) if attr_cnt['Red_ISLTR']!='' else 0
                rgIoSum[116] = int(attr_cnt['Future_Red_ISLTR']) if attr_cnt['Future_Red_ISLTR']!='' else 0
                rgIoSum[118] = int(attr_cnt['Non_Red_ISLTR']) if attr_cnt['Non_Red_ISLTR']!='' else 0 
            if attr_cnt['IO_Type'] in ['SCM: UIO (32) Analog Input (HLAI Adapt) (0-5000)']:
                rgIoSum[103] = int(attr_cnt['Red_IS']) if attr_cnt['Red_IS']!='' else 0
                rgIoSum[105] = int(attr_cnt['Future_Red_IS']) if attr_cnt['Future_Red_IS']!='' else 0
                rgIoSum[107] = int(attr_cnt['Non_Red_IS']) if attr_cnt['Non_Red_IS']!='' else 0
                rgIoSum[109] = int(attr_cnt['Red_NIS']) if attr_cnt['Red_NIS']!='' else 0
                rgIoSum[111] = int(attr_cnt['Future_Red_NIS']) if attr_cnt['Future_Red_NIS']!='' else 0
                rgIoSum[113] = int(attr_cnt['Non_Red_NIS']) if attr_cnt['Non_Red_NIS']!='' else 0
                rgIoSum[115] = int(attr_cnt['Red_ISLTR']) if attr_cnt['Red_ISLTR']!='' else 0
                rgIoSum[117] = int(attr_cnt['Future_Red_ISLTR']) if attr_cnt['Future_Red_ISLTR']!='' else 0
                rgIoSum[119] = int(attr_cnt['Non_Red_ISLTR']) if attr_cnt['Non_Red_ISLTR']!='' else 0 
            if attr_cnt['IO_Type'] in ['Series-C: UIO (32) Analog Input (LLAI Adapt) (0-5000)']:
                rgIoSum[120] = int(attr_cnt['Red_ISLTR']) if attr_cnt['Red_ISLTR']!='' else 0
                rgIoSum[121] = int(attr_cnt['Future_Red_ISLTR']) if attr_cnt['Future_Red_ISLTR']!='' else 0
                rgIoSum[122] = int(attr_cnt['Non_Red_ISLTR']) if attr_cnt['Non_Red_ISLTR']!='' else 0
            if attr_cnt['IO_Type'] in ['Series-C: UIO (32) Analog Output (0-5000)']:
                rgIoSum[171] = int(attr_cnt['Red_IS']) if attr_cnt['Red_IS']!='' else 0
                rgIoSum[173] = int(attr_cnt['Future_Red_IS']) if attr_cnt['Future_Red_IS']!='' else 0
                rgIoSum[175] = int(attr_cnt['Non_Red_IS']) if attr_cnt['Non_Red_IS']!='' else 0
                rgIoSum[177] = int(attr_cnt['Red_NIS']) if attr_cnt['Red_NIS']!='' else 0
                rgIoSum[179] = int(attr_cnt['Future_Red_NIS']) if attr_cnt['Future_Red_NIS']!='' else 0
                rgIoSum[181] = int(attr_cnt['Non_Red_NIS']) if attr_cnt['Non_Red_NIS']!='' else 0
                rgIoSum[183] = int(attr_cnt['Red_ISLTR']) if attr_cnt['Red_ISLTR']!='' else 0
                rgIoSum[185] = int(attr_cnt['Future_Red_ISLTR']) if attr_cnt['Future_Red_ISLTR']!='' else 0
                rgIoSum[187] = int(attr_cnt['Non_Red_ISLTR']) if attr_cnt['Non_Red_ISLTR']!='' else 0
            if attr_cnt['IO_Type'] in ['SCM: UIO (32) Analog Output (0-5000)']:
                rgIoSum[172] = int(attr_cnt['Red_IS']) if attr_cnt['Red_IS']!='' else 0
                rgIoSum[174] = int(attr_cnt['Future_Red_IS']) if attr_cnt['Future_Red_IS']!='' else 0
                rgIoSum[176] = int(attr_cnt['Non_Red_IS']) if attr_cnt['Non_Red_IS']!='' else 0
                rgIoSum[178] = int(attr_cnt['Red_NIS']) if attr_cnt['Red_NIS']!='' else 0
                rgIoSum[180] = int(attr_cnt['Future_Red_NIS']) if attr_cnt['Future_Red_NIS']!='' else 0
                rgIoSum[182] = int(attr_cnt['Non_Red_NIS']) if attr_cnt['Non_Red_NIS']!='' else 0
                rgIoSum[184] = int(attr_cnt['Red_ISLTR']) if attr_cnt['Red_ISLTR']!='' else 0
                rgIoSum[186] = int(attr_cnt['Future_Red_ISLTR']) if attr_cnt['Future_Red_ISLTR']!='' else 0
                rgIoSum[188] = int(attr_cnt['Non_Red_ISLTR']) if attr_cnt['Non_Red_ISLTR']!='' else 0
    if Mounting_Solution !='Yes':
        for attr_cnt in EN1:
            if attr_cnt['IO_Type'] in ['Series-C: DI (32) 24 VDC with Open Wire Detect (0-5000)']:
                rgIoSum[210] = int(attr_cnt['Red_IS']) if attr_cnt['Red_IS']!='' else 0
                rgIoSum[212] = int(attr_cnt['Future_Red_IS']) if attr_cnt['Future_Red_IS']!='' else 0
                rgIoSum[214] = int(attr_cnt['Non_Red_IS']) if attr_cnt['Non_Red_IS']!='' else 0
                rgIoSum[216] = int(attr_cnt['Red_NIS']) if attr_cnt['Red_NIS']!='' else 0
                rgIoSum[218] = int(attr_cnt['Future_Red_NIS']) if attr_cnt['Future_Red_NIS']!='' else 0
                rgIoSum[220] = int(attr_cnt['Non_Red_NIS']) if attr_cnt['Non_Red_NIS']!='' else 0
                rgIoSum[222] = int(attr_cnt['Red_ISLTR']) if attr_cnt['Red_ISLTR']!='' else 0
                rgIoSum[224] = int(attr_cnt['Future_Red_ISLTR']) if attr_cnt['Future_Red_ISLTR']!='' else 0
                rgIoSum[226] = int(attr_cnt['Non_Red_ISLTR']) if attr_cnt['Non_Red_ISLTR']!='' else 0 
                rgIoSum[228] = int(attr_cnt['Red_RLY']) if attr_cnt['Red_RLY']!='' else 0
                rgIoSum[230] = int(attr_cnt['Future_Red_RLY']) if attr_cnt['Future_Red_RLY']!='' else 0
                rgIoSum[232] = int(attr_cnt['Non_Red_RLY']) if attr_cnt['Non_Red_RLY']!='' else 0
                rgIoSum[563] = int(attr_cnt['Red_HV_RLY']) if attr_cnt['Red_HV_RLY']!='' else 0
                rgIoSum[565] = int(attr_cnt['Future_Red_HV_RLY']) if attr_cnt['Future_Red_HV_RLY']!='' else 0
                rgIoSum[567] = int(attr_cnt['Non_Red_HV_RLY']) if attr_cnt['Non_Red_HV_RLY']!='' else 0
            if attr_cnt['IO_Type'] in ['SCM: DI (32) 24 VDC with Open Wire Detect (0-5000)']:
                rgIoSum[211] = int(attr_cnt['Red_IS']) if attr_cnt['Red_IS']!='' else 0
                rgIoSum[213] = int(attr_cnt['Future_Red_IS']) if attr_cnt['Future_Red_IS']!='' else 0
                rgIoSum[215] = int(attr_cnt['Non_Red_IS']) if attr_cnt['Non_Red_IS']!='' else 0
                rgIoSum[217] = int(attr_cnt['Red_NIS']) if attr_cnt['Red_NIS']!='' else 0
                rgIoSum[219] = int(attr_cnt['Future_Red_NIS']) if attr_cnt['Future_Red_NIS']!='' else 0
                rgIoSum[221] = int(attr_cnt['Non_Red_NIS']) if attr_cnt['Non_Red_NIS']!='' else 0
                rgIoSum[223] = int(attr_cnt['Red_ISLTR']) if attr_cnt['Red_ISLTR']!='' else 0
                rgIoSum[225] = int(attr_cnt['Future_Red_ISLTR']) if attr_cnt['Future_Red_ISLTR']!='' else 0
                rgIoSum[227] = int(attr_cnt['Non_Red_ISLTR']) if attr_cnt['Non_Red_ISLTR']!='' else 0 
                rgIoSum[229] = int(attr_cnt['Red_RLY']) if attr_cnt['Red_RLY']!='' else 0
                rgIoSum[231] = int(attr_cnt['Future_Red_RLY']) if attr_cnt['Future_Red_RLY']!='' else 0
                rgIoSum[233] = int(attr_cnt['Non_Red_RLY']) if attr_cnt['Non_Red_RLY']!='' else 0
                rgIoSum[564] = int(attr_cnt['Red_HV_RLY']) if attr_cnt['Red_HV_RLY']!='' else 0
                rgIoSum[566] = int(attr_cnt['Future_Red_HV_RLY']) if attr_cnt['Future_Red_HV_RLY']!='' else 0
                rgIoSum[568] = int(attr_cnt['Non_Red_HV_RLY']) if attr_cnt['Non_Red_HV_RLY']!='' else 0
            if attr_cnt['IO_Type'] in ['Series-C: DI (32) 110 VAC (0-5000)']:
                rgIoSum[258] = int(attr_cnt['Red_NIS']) if attr_cnt['Red_NIS']!='' else 0
                rgIoSum[260] = int(attr_cnt['Future_Red_NIS']) if attr_cnt['Future_Red_NIS']!='' else 0
                rgIoSum[262] = int(attr_cnt['Non_Red_NIS']) if attr_cnt['Non_Red_NIS']!='' else 0
            if attr_cnt['IO_Type'] in ['SCM: DI (32) 110 VAC (0-5000)']:
                rgIoSum[259] = int(attr_cnt['Red_NIS']) if attr_cnt['Red_NIS']!='' else 0
                rgIoSum[261] = int(attr_cnt['Future_Red_NIS']) if attr_cnt['Future_Red_NIS']!='' else 0
                rgIoSum[263] = int(attr_cnt['Non_Red_NIS']) if attr_cnt['Non_Red_NIS']!='' else 0
            if attr_cnt['IO_Type'] in ['Series-C: DI (32) 110 VAC PROX (0-5000)']:
                rgIoSum[264] = int(attr_cnt['Non_Red_NIS']) if attr_cnt['Non_Red_NIS']!='' else 0
            if attr_cnt['IO_Type'] in ['SCm: DI (32) 110 VAC PROX (0-5000)']:
                rgIoSum[265] = int(attr_cnt['Non_Red_NIS']) if attr_cnt['Non_Red_NIS']!='' else 0
            if attr_cnt['IO_Type'] in ['Series-C: DI (32) 220 VAC (0-5000)']:
                rgIoSum[266] = int(attr_cnt['Red_NIS']) if attr_cnt['Red_NIS']!='' else 0
                rgIoSum[268] = int(attr_cnt['Future_Red_NIS']) if attr_cnt['Future_Red_NIS']!='' else 0
                rgIoSum[270] = int(attr_cnt['Non_Red_NIS']) if attr_cnt['Non_Red_NIS']!='' else 0
            if attr_cnt['IO_Type'] in ['SCM: DI (32) 220 VAC (0-5000)']:
                rgIoSum[267] = int(attr_cnt['Red_NIS']) if attr_cnt['Red_NIS']!='' else 0
                rgIoSum[269] = int(attr_cnt['Future_Red_NIS']) if attr_cnt['Future_Red_NIS']!='' else 0
                rgIoSum[271] = int(attr_cnt['Non_Red_NIS']) if attr_cnt['Non_Red_NIS']!='' else 0
            if attr_cnt['IO_Type'] in ['Series-C: DO (32) 24VDC Relay Bus above 30V (0-5000)']:
                rgIoSum[364] = int(attr_cnt['Red_RLY']) if attr_cnt['Red_RLY']!='' else 0
                rgIoSum[366] = int(attr_cnt['Future_Red_RLY']) if attr_cnt['Future_Red_RLY']!='' else 0
                rgIoSum[368] = int(attr_cnt['Non_Red_RLY']) if attr_cnt['Non_Red_RLY']!='' else 0
            if attr_cnt['IO_Type'] in ['SCM: DO (32) 24VDC Relay Bus above 30V (0-5000)']:
                rgIoSum[365] = int(attr_cnt['Red_RLY']) if attr_cnt['Red_RLY']!='' else 0
                rgIoSum[367] = int(attr_cnt['Future_Red_RLY']) if attr_cnt['Future_Red_RLY']!='' else 0
                rgIoSum[369] = int(attr_cnt['Non_Red_RLY']) if attr_cnt['Non_Red_RLY']!='' else 0
            if attr_cnt['IO_Type'] in ['Series-C: DO (32) 24VDC Relay Bus up to 30V (0-5000)']:
                rgIoSum[370] = int(attr_cnt['Red_RLY']) if attr_cnt['Red_RLY']!='' else 0
                rgIoSum[372] = int(attr_cnt['Future_Red_RLY']) if attr_cnt['Future_Red_RLY']!='' else 0
                rgIoSum[374] = int(attr_cnt['Non_Red_RLY']) if attr_cnt['Non_Red_RLY']!='' else 0
            if attr_cnt['IO_Type'] in ['SCM: DO (32) 24VDC Relay Bus up to 30V (0-5000)']:
                rgIoSum[371] = int(attr_cnt['Red_RLY']) if attr_cnt['Red_RLY']!='' else 0
                rgIoSum[373] = int(attr_cnt['Future_Red_RLY']) if attr_cnt['Future_Red_RLY']!='' else 0
                rgIoSum[375] = int(attr_cnt['Non_Red_RLY']) if attr_cnt['Non_Red_RLY']!='' else 0
            if attr_cnt['IO_Type'] in ['Series-C: Pulse Input (8) Single Channel (0-5000)','Series-C: Pulse Input (4) Dual Channel (0-5000)','Series-C: Pulse Input (2) Fast Cut Off Channel (0-5000)']:
                rgIoSum[90] += int(attr_cnt['Red_IS']) if attr_cnt['Red_IS']!='' else 0
                rgIoSum[92] += int(attr_cnt['Future_Red_IS']) if attr_cnt['Future_Red_IS']!='' else 0
                rgIoSum[94] += int(attr_cnt['Red_NIS']) if attr_cnt['Red_NIS']!='' else 0
                rgIoSum[96] += int(attr_cnt['Future_Red_NIS']) if attr_cnt['Future_Red_NIS']!='' else 0
                rgIoSum[98] += int(attr_cnt['Red_ISLTR']) if attr_cnt['Red_ISLTR']!='' else 0
                rgIoSum[100] += int(attr_cnt['Future_Red_ISLTR']) if attr_cnt['Future_Red_ISLTR']!='' else 0
            if attr_cnt['IO_Type'] in ['SCM: Pulse Input (8) Single Channel (0-5000)','SCM: Pulse Input (4) Dual Channel (0-5000)','SCM: Pulse Input (2) Fast Cut Off Channel (0-5000)']:
                rgIoSum[91] += int(attr_cnt['Red_IS']) if attr_cnt['Red_IS']!='' else 0
                rgIoSum[93] += int(attr_cnt['Future_Red_IS']) if attr_cnt['Future_Red_IS']!='' else 0
                rgIoSum[95] += int(attr_cnt['Red_NIS']) if attr_cnt['Red_NIS']!='' else 0
                rgIoSum[97] += int(attr_cnt['Future_Red_NIS']) if attr_cnt['Future_Red_NIS']!='' else 0
                rgIoSum[99] += int(attr_cnt['Red_ISLTR']) if attr_cnt['Red_ISLTR']!='' else 0
                rgIoSum[101] += int(attr_cnt['Future_Red_ISLTR']) if attr_cnt['Future_Red_ISLTR']!='' else 0
            if attr_cnt['IO_Type'] in ['Series-C: DI (32) 24VDC SOE (0-5000)']:
                rgIoSum[234] = int(attr_cnt['Red_IS']) if attr_cnt['Red_IS']!='' else 0
                rgIoSum[236] = int(attr_cnt['Future_Red_IS']) if attr_cnt['Future_Red_IS']!='' else 0
                rgIoSum[238] = int(attr_cnt['Non_Red_IS']) if attr_cnt['Non_Red_IS']!='' else 0
                rgIoSum[240] = int(attr_cnt['Red_NIS']) if attr_cnt['Red_NIS']!='' else 0
                rgIoSum[242] = int(attr_cnt['Future_Red_NIS']) if attr_cnt['Future_Red_NIS']!='' else 0
                rgIoSum[244] = int(attr_cnt['Non_Red_NIS']) if attr_cnt['Non_Red_NIS']!='' else 0
                rgIoSum[246] = int(attr_cnt['Red_ISLTR']) if attr_cnt['Red_ISLTR']!='' else 0
                rgIoSum[248] = int(attr_cnt['Future_Red_ISLTR']) if attr_cnt['Future_Red_ISLTR']!='' else 0
                rgIoSum[250] = int(attr_cnt['Non_Red_ISLTR']) if attr_cnt['Non_Red_ISLTR']!='' else 0 
                rgIoSum[252] = int(attr_cnt['Red_RLY']) if attr_cnt['Red_RLY']!='' else 0
                rgIoSum[254] = int(attr_cnt['Future_Red_RLY']) if attr_cnt['Future_Red_RLY']!='' else 0
                rgIoSum[256] = int(attr_cnt['Non_Red_RLY']) if attr_cnt['Non_Red_RLY']!='' else 0
                rgIoSum[569] = int(attr_cnt['Red_HV_RLY']) if attr_cnt['Red_HV_RLY']!='' else 0
                rgIoSum[571] = int(attr_cnt['Future_Red_HV_RLY']) if attr_cnt['Future_Red_HV_RLY']!='' else 0
                rgIoSum[573] = int(attr_cnt['Non_Red_HV_RLY']) if attr_cnt['Non_Red_HV_RLY']!='' else 0
    if Mounting_Solution !='Yes':
        for attr_cnt in UN1:
            if attr_cnt['IO_Type'] in ['Series-C: UIO (32) Digital Input (0-5000)']:
                rgIoSum[280] = int(attr_cnt['Red_IS']) if attr_cnt['Red_IS']!='' else 0
                rgIoSum[282] = int(attr_cnt['Future_Red_IS']) if attr_cnt['Future_Red_IS']!='' else 0
                rgIoSum[284] = int(attr_cnt['Non_Red_IS']) if attr_cnt['Non_Red_IS']!='' else 0
                rgIoSum[286] = int(attr_cnt['Red_NIS']) if attr_cnt['Red_NIS']!='' else 0
                rgIoSum[288] = int(attr_cnt['Future_Red_NIS']) if attr_cnt['Future_Red_NIS']!='' else 0
                rgIoSum[290] = int(attr_cnt['Non_Red_NIS']) if attr_cnt['Non_Red_NIS']!='' else 0
                rgIoSum[292] = int(attr_cnt['Red_ISLTR']) if attr_cnt['Red_ISLTR']!='' else 0
                rgIoSum[294] = int(attr_cnt['Future_Red_ISLTR']) if attr_cnt['Future_Red_ISLTR']!='' else 0
                rgIoSum[296] = int(attr_cnt['Non_Red_ISLTR']) if attr_cnt['Non_Red_ISLTR']!='' else 0 
                rgIoSum[298] = int(attr_cnt['Red_RLY']) if attr_cnt['Red_RLY']!='' else 0
                rgIoSum[300] = int(attr_cnt['Future_Red_RLY']) if attr_cnt['Future_Red_RLY']!='' else 0
                rgIoSum[302] = int(attr_cnt['Non_Red_RLY']) if attr_cnt['Non_Red_RLY']!='' else 0
                rgIoSum[575] = int(attr_cnt['Red_HV_RLY']) if attr_cnt['Red_HV_RLY']!='' else 0
                rgIoSum[577] = int(attr_cnt['Future_Red_HV_RLY']) if attr_cnt['Future_Red_HV_RLY']!='' else 0
                rgIoSum[578] = int(attr_cnt['Non_Red_HV_RLY']) if attr_cnt['Non_Red_HV_RLY']!='' else 0
                #rgIoSum[581] = int(attr_cnt['Red_HV_RLY']) if attr_cnt['Non_Red_HV_RLY']!='' else 0
            if attr_cnt['IO_Type'] in ['SCM: UIO (32) Digital Input (0-5000)']:
                rgIoSum[281] = int(attr_cnt['Red_IS']) if attr_cnt['Red_IS']!='' else 0
                rgIoSum[283] = int(attr_cnt['Future_Red_IS']) if attr_cnt['Future_Red_IS']!='' else 0
                rgIoSum[285] = int(attr_cnt['Non_Red_IS']) if attr_cnt['Non_Red_IS']!='' else 0
                rgIoSum[287] = int(attr_cnt['Red_NIS']) if attr_cnt['Red_NIS']!='' else 0
                rgIoSum[289] = int(attr_cnt['Future_Red_NIS']) if attr_cnt['Future_Red_NIS']!='' else 0
                rgIoSum[291] = int(attr_cnt['Non_Red_NIS']) if attr_cnt['Non_Red_NIS']!='' else 0
                rgIoSum[293] = int(attr_cnt['Red_ISLTR']) if attr_cnt['Red_ISLTR']!='' else 0
                rgIoSum[295] = int(attr_cnt['Future_Red_ISLTR']) if attr_cnt['Future_Red_ISLTR']!='' else 0
                rgIoSum[297] = int(attr_cnt['Non_Red_ISLTR']) if attr_cnt['Non_Red_ISLTR']!='' else 0 
                rgIoSum[299] = int(attr_cnt['Red_RLY']) if attr_cnt['Red_RLY']!='' else 0
                rgIoSum[301] = int(attr_cnt['Future_Red_RLY']) if attr_cnt['Future_Red_RLY']!='' else 0
                rgIoSum[303] = int(attr_cnt['Non_Red_RLY']) if attr_cnt['Non_Red_RLY']!='' else 0
                rgIoSum[576] = int(attr_cnt['Red_HV_RLY']) if attr_cnt['Red_HV_RLY']!='' else 0
                rgIoSum[579] = int(attr_cnt['Future_HV_Rly']) if attr_cnt['Future_HV_Rly']!='' else 0
                rgIoSum[580] = int(attr_cnt['Non_Red_HV_Rly']) if attr_cnt['Non_Red_HV_Rly']!='' else 0
            if attr_cnt['IO_Type'] in ['Series-C: UIO (32) Digital Output (0-5000)']:
                rgIoSum[377] = int(attr_cnt['Red_IS']) if attr_cnt['Red_IS']!='' else 0
                rgIoSum[379] = int(attr_cnt['Future_Red_IS']) if attr_cnt['Future_Red_IS']!='' else 0
                rgIoSum[381] = int(attr_cnt['Non_Red_IS']) if attr_cnt['Non_Red_IS']!='' else 0
                rgIoSum[383] = int(attr_cnt['Red_NIS']) if attr_cnt['Red_NIS']!='' else 0
                rgIoSum[385] = int(attr_cnt['Future_Red_NIS']) if attr_cnt['Future_Red_NIS']!='' else 0
                rgIoSum[387] = int(attr_cnt['Non_Red_NIS']) if attr_cnt['Non_Red_NIS']!='' else 0
                rgIoSum[389] = int(attr_cnt['Red_ISLTR']) if attr_cnt['Red_ISLTR']!='' else 0
                rgIoSum[391] = int(attr_cnt['Future_Red_ISLTR']) if attr_cnt['Future_Red_ISLTR']!='' else 0
                rgIoSum[393] = int(attr_cnt['Non_Red_ISLTR']) if attr_cnt['Non_Red_ISLTR']!='' else 0 
                rgIoSum[395] = int(attr_cnt['Red_RLY']) if attr_cnt['Red_RLY']!='' else 0
                rgIoSum[397] = int(attr_cnt['Future_Red_RLY']) if attr_cnt['Future_Red_RLY']!='' else 0
                rgIoSum[399] = int(attr_cnt['Non_Red_RLY']) if attr_cnt['Non_Red_RLY']!='' else 0
                rgIoSum[596] = int(attr_cnt['Red_HV_RLY']) if attr_cnt['Red_HV_RLY']!='' else 0
                rgIoSum[598] = int(attr_cnt['Future_Red_HV_RLY']) if attr_cnt['Future_Red_HV_RLY']!='' else 0
                rgIoSum[600] = int(attr_cnt['Non_Red_HV_RLY']) if attr_cnt['Non_Red_HV_RLY']!='' else 0
            if attr_cnt['IO_Type'] in ['SCM: UIO (32) Digital Output (0-5000)']:
                rgIoSum[378] = int(attr_cnt['Red_IS']) if attr_cnt['Red_IS']!='' else 0
                rgIoSum[380] = int(attr_cnt['Future_Red_IS']) if attr_cnt['Future_Red_IS']!='' else 0
                rgIoSum[382] = int(attr_cnt['Non_Red_IS']) if attr_cnt['Non_Red_IS']!='' else 0
                rgIoSum[384] = int(attr_cnt['Red_NIS']) if attr_cnt['Red_NIS']!='' else 0
                rgIoSum[386] = int(attr_cnt['Future_Red_NIS']) if attr_cnt['Future_Red_NIS']!='' else 0
                rgIoSum[388] = int(attr_cnt['Non_Red_NIS']) if attr_cnt['Non_Red_NIS']!='' else 0
                rgIoSum[390] = int(attr_cnt['Red_ISLTR']) if attr_cnt['Red_ISLTR']!='' else 0
                rgIoSum[392] = int(attr_cnt['Future_Red_ISLTR']) if attr_cnt['Future_Red_ISLTR']!='' else 0
                rgIoSum[394] = int(attr_cnt['Non_Red_ISLTR']) if attr_cnt['Non_Red_ISLTR']!='' else 0 
                rgIoSum[396] = int(attr_cnt['Red_RLY']) if attr_cnt['Red_RLY']!='' else 0
                rgIoSum[398] = int(attr_cnt['Future_Red_RLY']) if attr_cnt['Future_Red_RLY']!='' else 0
                rgIoSum[303] = int(attr_cnt['Non_Red_RLY']) if attr_cnt['Non_Red_RLY']!='' else 0
                rgIoSum[597] = int(attr_cnt['Red_HV_Rly']) if attr_cnt['Red_HV_Rly']!='' else 0 
                rgIoSum[599] = int(attr_cnt['Future_HV_Rly']) if attr_cnt['Future_HV_Rly']!='' else 0 
                rgIoSum[601] = int(attr_cnt['Non_Red_HV_Rly']) if attr_cnt['Non_Red_HV_Rly']!='' else 0 
    #rgIoSum.pop(0)
    #CCEECOMMBR-7345
    if io_Family == 'seriesC' and Mounting_Solution == 'Yes':
        UPC = rg.SelectedAttributes.GetContainerByName("C300_UPC_Labor_IO_count_RG_1").Rows
        UPC1 = rg.SelectedAttributes.GetContainerByName("C300_UPC_Labor_IO_count_RG_2").Rows
        for ms in UPC:
            if ms['IO_Type'] in ['Series-C: UIO (32) Analog Input (0-5000)']:
                rgIoSum[102] += int(ms['Red_IS']) if ms['Red_IS']!='' else 0
                rgIoSum[106] += int(ms['Non_Red_IS']) if ms['Non_Red_IS']!='' else 0
                rgIoSum[108] += int(ms['Red_NIS']) if ms['Red_NIS']!='' else 0
                rgIoSum[112] += int(ms['Non_Red_NIS']) if ms['Non_Red_NIS']!='' else 0
            if ms['IO_Type'] in ['Series-C: UIO (32) Analog Output (0-5000)']:
                rgIoSum[171] += int(ms['Red_IS']) if ms['Red_IS']!='' else 0
                rgIoSum[175] += int(ms['Non_Red_IS']) if ms['Non_Red_IS']!='' else 0
                rgIoSum[177] += int(ms['Red_NIS']) if ms['Red_NIS']!='' else 0
                rgIoSum[181] += int(ms['Non_Red_NIS']) if ms['Non_Red_NIS']!='' else 0
        for ms1 in UPC1:
            if ms1['IO_Type'] in ['Series-C: UIO (32) Digital Input (0-5000)']:
                rgIoSum[280] += int(ms1['Red_IS']) if ms1['Red_IS']!='' else 0
                rgIoSum[284] += int(ms1['Non_Red_IS']) if ms1['Non_Red_IS']!='' else 0
                rgIoSum[286] += int(ms1['Red_NIS']) if ms1['Red_NIS']!='' else 0
                rgIoSum[290] += int(ms1['Non_Red_NIS']) if ms1['Non_Red_NIS']!='' else 0
            if ms1['IO_Type'] in ['Series-C: UIO (32) Digital Output (0-5000)']:
                rgIoSum[377] += int(ms1['Red_IS']) if ms1['Red_IS']!='' else 0
                rgIoSum[381] += int(ms1['Non_Red_IS']) if ms1['Non_Red_IS']!='' else 0
                rgIoSum[383] += int(ms1['Red_NIS']) if ms1['Red_NIS']!='' else 0
                rgIoSum[387] += int(ms1['Non_Red_NIS']) if ms1['Non_Red_NIS']!='' else 0
                #rgIoSum[387] += int(ms1['Non_Red_NIS']) if ms1['Non_Red_NIS']!='' else 0
                #rgIoSum[387] += int(ms1['Non_Red_NIS']) if ms1['Non_Red_NIS']!='' else 0
                #rgIoSum[387] += int(ms1['Non_Red_NIS']) if ms1['Non_Red_NIS']!='' else 0
    return rgIoSum