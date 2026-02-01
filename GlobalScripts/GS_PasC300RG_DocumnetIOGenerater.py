import GS_PasC300RG_IO_Documnet_1
def populateC300Data2(Quote,rg):
    rg=rg
    rgIoSum1=[0]*800
    ms_attr =rg.SelectedAttributes.GetContainerByName("Document_cont_c3001").Rows
    for io_f in ms_attr:
        io_Family=io_f['Io_family']
        rgIoSum1[554] = io_f['Io_family']
        Mounting_Solution=io_f['Dummy_RG_IO_Mounting_Solution']
        universal=io_f['SerC_CG_Universal_Marshalling_Cabinet']
        pmio=io_f['SerC_CG_PM_IO_Solution_required']
        rgIoSum1[556] = io_f['SerC_CG_PM_IO_Solution_required']
        rgIoSum1[559] = io_f['C300_RG_Total_IO_Load']
        Ethernet="No"
        fmio='No'
        cont_req=io_f['cont_req']
        if io_Family=="Mark2" and Mounting_Solution !='Yes':
            MS = rg.SelectedAttributes.GetContainerByName("C300_C IO_RG MS2").Rows
            EN = rg.SelectedAttributes.GetContainerByName("C300_SerC_Enhanced_Function_IO_Mark_Group_RG_Cont").Rows
            EN1 = rg.SelectedAttributes.GetContainerByName("C300_SerC_Enhanced_Function_IO_Mark_Group_RG_Cont1").Rows
            UN = rg.SelectedAttributes.GetContainerByName("C300_CG_Universal_IO_Mark_1").Rows
            UN1 = rg.SelectedAttributes.GetContainerByName("C300_CG_Universal_IO_Mark_2").Rows
        elif io_Family=="seriesC" and Mounting_Solution !='Yes':
            rail1 = rg.SelectedAttributes.GetContainerByName("C300_RAIL_Universal_IO_cont_RG_1").Rows
            rail2 = rg.SelectedAttributes.GetContainerByName("C300_RAIL_Universal_io_RG_cont_2").Rows
            EN1 = rg.SelectedAttributes.GetContainerByName("SerC_RG_Enhanced_Function_IO_Cont2").Rows
            UN = rg.SelectedAttributes.GetContainerByName("C300_RG_Universal_IO_cont_1").Rows
            UN1 = rg.SelectedAttributes.GetContainerByName("C300_RG_Universal_IO_cont_2").Rows
        elif io_Family=="TurboM" and Mounting_Solution !='Yes':
            EN = rg.SelectedAttributes.GetContainerByName("SerC_RG_Enhanced_Function_IO_Cont").Rows
            EN1 = rg.SelectedAttributes.GetContainerByName("SerC_RG_Enhanced_Function_IO_Cont2").Rows
            UN = rg.SelectedAttributes.GetContainerByName("C300_RG_Universal_IO_cont_1").Rows
            UN1 = rg.SelectedAttributes.GetContainerByName("C300_RG_Universal_IO_cont_2").Rows
    if Mounting_Solution !='Yes':
        for ms in EN1:
            if ms['IO_Type'] in ['Series-C: DO (32) 24VDC Bus External Power Supply (0-5000)']:
                rgIoSum1[316] = int(ms['Red_IS']) if ms['Red_IS']!='' else 0
                rgIoSum1[318] = int(ms['Future_Red_IS']) if ms['Future_Red_IS']!='' else 0
                rgIoSum1[320] = int(ms['Non_Red_IS']) if ms['Non_Red_IS']!='' else 0
                rgIoSum1[322] = int(ms['Red_NIS']) if ms['Red_NIS']!='' else 0
                rgIoSum1[324] = int(ms['Future_Red_NIS']) if ms['Future_Red_NIS']!='' else 0
                rgIoSum1[326] = int(ms['Non_Red_NIS']) if ms['Non_Red_NIS']!='' else 0
                rgIoSum1[328] = int(ms['Red_ISLTR']) if ms['Red_ISLTR']!='' else 0
                rgIoSum1[330] = int(ms['Future_Red_ISLTR']) if ms['Future_Red_ISLTR']!='' else 0
                rgIoSum1[332] = int(ms['Non_Red_ISLTR']) if ms['Non_Red_ISLTR']!='' else 0 
                rgIoSum1[334] = int(ms['Red_RLY']) if ms['Red_RLY']!='' else 0
                rgIoSum1[336] = int(ms['Future_Red_RLY']) if ms['Future_Red_RLY']!='' else 0
                rgIoSum1[338] = int(ms['Non_Red_RLY']) if ms['Non_Red_RLY']!='' else 0
                rgIoSum1[584] = int(ms['Red_HV_RLY']) if ms['Red_HV_RLY']!='' else 0
                rgIoSum1[586] = int(ms['Future_Red_HV_RLY']) if ms['Future_Red_HV_RLY']!='' else 0
                rgIoSum1[588] = int(ms['Non_Red_HV_RLY']) if ms['Non_Red_HV_RLY']!='' else 0
            if ms['IO_Type'] in ['Series-C: DO (32) 24VDC Bus Internal Power Supply (0-5000)']:
                rgIoSum1[340] = int(ms['Red_IS']) if ms['Red_IS']!='' else 0
                rgIoSum1[342] = int(ms['Future_Red_IS']) if ms['Future_Red_IS']!='' else 0
                rgIoSum1[344] = int(ms['Non_Red_IS']) if ms['Non_Red_IS']!='' else 0
                rgIoSum1[346] = int(ms['Red_NIS']) if ms['Red_NIS']!='' else 0
                rgIoSum1[348] = int(ms['Future_Red_NIS']) if ms['Future_Red_NIS']!='' else 0
                rgIoSum1[350] = int(ms['Non_Red_NIS']) if ms['Non_Red_NIS']!='' else 0
                rgIoSum1[352] = int(ms['Red_ISLTR']) if ms['Red_ISLTR']!='' else 0
                rgIoSum1[354] = int(ms['Future_Red_ISLTR']) if ms['Future_Red_ISLTR']!='' else 0
                rgIoSum1[356] = int(ms['Non_Red_ISLTR']) if ms['Non_Red_ISLTR']!='' else 0 
                rgIoSum1[358] = int(ms['Red_RLY']) if ms['Red_RLY']!='' else 0
                rgIoSum1[360] = int(ms['Future_Red_RLY']) if ms['Future_Red_RLY']!='' else 0
                rgIoSum1[362] = int(ms['Non_Red_RLY']) if ms['Non_Red_RLY']!='' else 0
                rgIoSum1[590] = int(ms['Red_HV_RLY']) if ms['Red_HV_RLY']!='' else 0
                rgIoSum1[592] = int(ms['Future_Red_HV_RLY']) if ms['Future_Red_HV_RLY']!='' else 0
                rgIoSum1[594] = int(ms['Non_Red_HV_RLY']) if ms['Non_Red_HV_RLY']!='' else 0
            if ms['IO_Type'] in ['SCM: DO (32) 24VDC Bus External Power Supply (0-5000)']:
                rgIoSum1[317] += int(ms['Red_IS']) if ms['Red_IS']!='' else 0
                rgIoSum1[319] += int(ms['Future_Red_IS']) if ms['Future_Red_IS']!='' else 0
                rgIoSum1[321] += int(ms['Non_Red_IS']) if ms['Non_Red_IS']!='' else 0
                rgIoSum1[323] += int(ms['Red_NIS']) if ms['Red_NIS']!='' else 0
                rgIoSum1[325] += int(ms['Future_Red_NIS']) if ms['Future_Red_NIS']!='' else 0
                rgIoSum1[327] += int(ms['Non_Red_NIS']) if ms['Non_Red_NIS']!='' else 0
                rgIoSum1[329] += int(ms['Red_ISLTR']) if ms['Red_ISLTR']!='' else 0
                rgIoSum1[331] += int(ms['Future_Red_ISLTR']) if ms['Future_Red_ISLTR']!='' else 0
                rgIoSum1[333] += int(ms['Non_Red_ISLTR']) if ms['Non_Red_ISLTR']!='' else 0 
                rgIoSum1[335] += int(ms['Red_RLY']) if ms['Red_RLY']!='' else 0
                rgIoSum1[337] += int(ms['Future_Red_RLY']) if ms['Future_Red_RLY']!='' else 0
                rgIoSum1[339] += int(ms['Non_Red_RLY']) if ms['Non_Red_RLY']!='' else 0
                rgIoSum1[585] += int(ms['Red_HV_Rly']) if ms['Red_HV_Rly']!='' else 0
                rgIoSum1[587] += int(ms['Future_HV_Rly']) if ms['Future_HV_Rly']!='' else 0
                rgIoSum1[589] += int(ms['Non_Red_HV_Rly']) if ms['Non_Red_HV_Rly']!='' else 0
            if ms['IO_Type'] in ['SCM: DO (32) 24VDC Bus Internal Power Supply (0-5000)']:
                rgIoSum1[341] += int(ms['Red_IS']) if ms['Red_IS']!='' else 0
                rgIoSum1[343] += int(ms['Future_Red_IS']) if ms['Future_Red_IS']!='' else 0
                rgIoSum1[345] += int(ms['Non_Red_IS']) if ms['Non_Red_IS']!='' else 0
                rgIoSum1[347] += int(ms['Red_NIS']) if ms['Red_NIS']!='' else 0
                rgIoSum1[349] += int(ms['Future_Red_NIS']) if ms['Future_Red_NIS']!='' else 0
                rgIoSum1[351] += int(ms['Non_Red_NIS']) if ms['Non_Red_NIS']!='' else 0
                rgIoSum1[353] += int(ms['Red_ISLTR']) if ms['Red_ISLTR']!='' else 0
                rgIoSum1[355] += int(ms['Future_Red_ISLTR']) if ms['Future_Red_ISLTR']!='' else 0
                rgIoSum1[357] += int(ms['Non_Red_ISLTR']) if ms['Non_Red_ISLTR']!='' else 0 
                rgIoSum1[359] += int(ms['Red_RLY']) if ms['Red_RLY']!='' else 0
                rgIoSum1[361] += int(ms['Future_Red_RLY']) if ms['Future_Red_RLY']!='' else 0
                rgIoSum1[363] += int(ms['Non_Red_RLY']) if ms['Non_Red_RLY']!='' else 0
                rgIoSum1[591] += int(ms['Red_HV_Rly']) if ms['Red_HV_Rly']!='' else 0
                rgIoSum1[593] += int(ms['Future_HV_Rly']) if ms['Future_HV_Rly']!='' else 0
                rgIoSum1[595] += int(ms['Non_Red_HV_Rly']) if ms['Non_Red_HV_Rly']!='' else 0
    if io_Family =="Mark2" and Mounting_Solution !='Yes':
        MS3 =rg.SelectedAttributes.GetContainerByName("C300_C IO_RG MS3").Rows
        for ms in MS3:
            if ms['IO_Type'] in ['SCM: DI (32) 24VDC (0-5000)']:
                rgIoSum1[198] = int(ms['Red_IS']) if ms['Red_IS']!='' else 0
                rgIoSum1[199] = int(ms['Future_Red_IS']) if ms['Future_Red_IS']!='' else 0
                rgIoSum1[200] = int(ms['Non_Red_IS']) if ms['Non_Red_IS']!='' else 0
                rgIoSum1[201] = int(ms['Red_NIS']) if ms['Red_NIS']!='' else 0
                rgIoSum1[202] = int(ms['Future_Red_NIS']) if ms['Future_Red_NIS']!='' else 0
                rgIoSum1[203] = int(ms['Non_Red_NIS']) if ms['Non_Red_NIS']!='' else 0
                rgIoSum1[204] = int(ms['Red_ISLTR']) if ms['Red_ISLTR']!='' else 0
                rgIoSum1[205] = int(ms['Future_Red_ISLTR']) if ms['Future_Red_ISLTR']!='' else 0
                rgIoSum1[206] = int(ms['Non_Red_ISLTR']) if ms['Non_Red_ISLTR']!='' else 0 
                rgIoSum1[207] = int(ms['Red_RLY']) if ms['Red_RLY']!='' else 0
                rgIoSum1[208] = int(ms['Future_Red_RLY']) if ms['Future_Red_RLY']!='' else 0
                rgIoSum1[209] = int(ms['Non_Red_RLY']) if ms['Non_Red_RLY']!='' else 0
                rgIoSum1[560] = int(ms['Red_HV_Rly']) if ms['Red_HV_Rly']!='' else 0
                rgIoSum1[561] = int(ms['Future_HV_Rly']) if ms['Future_HV_Rly']!='' else 0
                rgIoSum1[562] = int(ms['Non_Red_HV_Rly']) if ms['Non_Red_HV_Rly']!='' else 0
            if ms['IO_Type'] in ['SCM: DI (32) 24VDC SOE (0-5000)']:
                rgIoSum1[235] = int(ms['Red_IS']) if ms['Red_IS']!='' else 0
                rgIoSum1[237] = int(ms['Future_Red_IS']) if ms['Future_Red_IS']!='' else 0
                rgIoSum1[239] = int(ms['Non_Red_IS']) if ms['Non_Red_IS']!='' else 0
                rgIoSum1[241] = int(ms['Red_NIS']) if ms['Red_NIS']!='' else 0
                rgIoSum1[243] = int(ms['Future_Red_NIS']) if ms['Future_Red_NIS']!='' else 0
                rgIoSum1[245] = int(ms['Non_Red_NIS']) if ms['Non_Red_NIS']!='' else 0
                rgIoSum1[247] = int(ms['Red_ISLTR']) if ms['Red_ISLTR']!='' else 0
                rgIoSum1[249] = int(ms['Future_Red_ISLTR']) if ms['Future_Red_ISLTR']!='' else 0
                rgIoSum1[251] = int(ms['Non_Red_ISLTR']) if ms['Non_Red_ISLTR']!='' else 0 
                rgIoSum1[253] = int(ms['Red_RLY']) if ms['Red_RLY']!='' else 0
                rgIoSum1[255] = int(ms['Future_Red_RLY']) if ms['Future_Red_RLY']!='' else 0
                rgIoSum1[257] = int(ms['Non_Red_RLY']) if ms['Non_Red_RLY']!='' else 0
                rgIoSum1[570] = int(ms['Red_HV_Rly']) if ms['Red_HV_Rly']!='' else 0
                rgIoSum1[572] = int(ms['Future_HV_Rly']) if ms['Future_HV_Rly']!='' else 0
                rgIoSum1[574] = int(ms['Non_Red_HV_Rly']) if ms['Non_Red_HV_Rly']!='' else 0
            if ms['IO_Type'] in ['SCM: DO (32) 24VDC Bus External Power Supply (0-5000)']:
                rgIoSum1[317] += int(ms['Red_IS']) if ms['Red_IS']!='' else 0
                rgIoSum1[319] += int(ms['Future_Red_IS']) if ms['Future_Red_IS']!='' else 0
                rgIoSum1[321] += int(ms['Non_Red_IS']) if ms['Non_Red_IS']!='' else 0
                rgIoSum1[323] += int(ms['Red_NIS']) if ms['Red_NIS']!='' else 0
                rgIoSum1[325] += int(ms['Future_Red_NIS']) if ms['Future_Red_NIS']!='' else 0
                rgIoSum1[327] += int(ms['Non_Red_NIS']) if ms['Non_Red_NIS']!='' else 0
                rgIoSum1[329] += int(ms['Red_ISLTR']) if ms['Red_ISLTR']!='' else 0
                rgIoSum1[331] += int(ms['Future_Red_ISLTR']) if ms['Future_Red_ISLTR']!='' else 0
                rgIoSum1[333] += int(ms['Non_Red_ISLTR']) if ms['Non_Red_ISLTR']!='' else 0 
                rgIoSum1[335] += int(ms['Red_RLY']) if ms['Red_RLY']!='' else 0
                rgIoSum1[337] += int(ms['Future_Red_RLY']) if ms['Future_Red_RLY']!='' else 0
                rgIoSum1[339] += int(ms['Non_Red_RLY']) if ms['Non_Red_RLY']!='' else 0
                rgIoSum1[585] += int(ms['Red_HV_Rly']) if ms['Red_HV_Rly']!='' else 0
                rgIoSum1[587] += int(ms['Future_HV_Rly']) if ms['Future_HV_Rly']!='' else 0
                rgIoSum1[589] += int(ms['Non_Red_HV_Rly']) if ms['Non_Red_HV_Rly']!='' else 0
            if ms['IO_Type'] in ['SCM: DO (32) 24VDC Bus Internal Power Supply (0-5000)']:
                rgIoSum1[341] += int(ms['Red_IS']) if ms['Red_IS']!='' else 0
                rgIoSum1[343] += int(ms['Future_Red_IS']) if ms['Future_Red_IS']!='' else 0
                rgIoSum1[345] += int(ms['Non_Red_IS']) if ms['Non_Red_IS']!='' else 0
                rgIoSum1[347] += int(ms['Red_NIS']) if ms['Red_NIS']!='' else 0
                rgIoSum1[349] += int(ms['Future_Red_NIS']) if ms['Future_Red_NIS']!='' else 0
                rgIoSum1[351] += int(ms['Non_Red_NIS']) if ms['Non_Red_NIS']!='' else 0
                rgIoSum1[353] += int(ms['Red_ISLTR']) if ms['Red_ISLTR']!='' else 0
                rgIoSum1[355] += int(ms['Future_Red_ISLTR']) if ms['Future_Red_ISLTR']!='' else 0
                rgIoSum1[357] += int(ms['Non_Red_ISLTR']) if ms['Non_Red_ISLTR']!='' else 0 
                rgIoSum1[359] += int(ms['Red_RLY']) if ms['Red_RLY']!='' else 0
                rgIoSum1[361] += int(ms['Future_Red_RLY']) if ms['Future_Red_RLY']!='' else 0
                rgIoSum1[363] += int(ms['Non_Red_RLY']) if ms['Non_Red_RLY']!='' else 0
                rgIoSum1[591] += int(ms['Red_HV_Rly']) if ms['Red_HV_Rly']!='' else 0
                rgIoSum1[593] += int(ms['Future_HV_Rly']) if ms['Future_HV_Rly']!='' else 0
                rgIoSum1[595] += int(ms['Non_Red_HV_Rly']) if ms['Non_Red_HV_Rly']!='' else 0
    if ((io_Family =="seriesC" and universal=="No")or(io_Family =="TurboM")) and Mounting_Solution !='Yes':
        Giis=rg.SelectedAttributes.GetContainerByName("C300_SerC_GIIS_RG_Cont").Rows
        for giis in Giis:
            if giis['IO_Type'] in ['Series-C: GI/IS HLAI (16) Single Channel Isolator (0-5000)','Series-C: GI/IS HLAI (16) Dual Channel Isolator (0-5000)','Series-C: GI/IS HLAI (16) Temperature Isolator (0-5000)','Series-C: GI/IS HLAI (16) (0-5000)']:
                rgIoSum1[19] += int(giis['Red_IS']) if giis['Red_IS']!='' else 0
                rgIoSum1[20] += int(giis['Future_Red_IS']) if giis['Future_Red_IS']!='' else 0
                rgIoSum1[21] += int(giis['Non_Red_IS']) if giis['Non_Red_IS']!='' else 0
            if giis['IO_Type'] in ['Series-C: GI/IS HLAI (16) HART Single Channel Isolator (0-5000)','Series-C: GI/IS HLAI (16) HART Dual Channel Isolator (0-5000)','Series-C: GI/IS HLAI (16) HART Temperature Isolator (0-5000)','Series-C: GI/IS HLAI (16) HART (0-5000)']:
                rgIoSum1[40] += int(giis['Red_IS']) if giis['Red_IS']!='' else 0
                rgIoSum1[41] += int(giis['Future_Red_IS']) if giis['Future_Red_IS']!='' else 0
                rgIoSum1[42] += int(giis['Non_Red_IS']) if giis['Non_Red_IS']!='' else 0
            if giis['IO_Type'] in ['Series-C: GI/IS AO (16) HART Single Channel Isolator (0-5000)','Series-C: GI/IS AO (16) HART Dual Channel Isolator (0-5000)','Series-C: GI/IS AO (16) HART (0-5000)']:
                rgIoSum1[168] += int(giis['Red_IS']) if giis['Red_IS']!='' else 0
                rgIoSum1[169] += int(giis['Future_Red_IS']) if giis['Future_Red_IS']!='' else 0
                rgIoSum1[170] += int(giis['Non_Red_IS']) if giis['Non_Red_IS']!='' else 0
            if giis['IO_Type'] in ['Series-C: GI/IS DO (32) 24 VDC Bus with Expansion Board (0-5000)']:
                rgIoSum1[376] += int(giis['Non_Red_IS']) if giis['Non_Red_IS']!='' else 0
            if giis['IO_Type'] in ['Series-C: GI/IS DI (32) 24 VDC Relay (0-5000)','Series-C: GI/IS DI (32) 24 VDC Relay LFD (0-5000)','Series-C: GI/IS DI (32) 24VDC Solid State (0-5000)']:
                rgIoSum1[272] += int(giis['Red_IS']) if giis['Red_IS']!='' else 0
                rgIoSum1[273] += int(giis['Future_Red_IS']) if giis['Future_Red_IS']!='' else 0
                rgIoSum1[274] += int(giis['Non_Red_IS']) if giis['Non_Red_IS']!='' else 0
            if giis['IO_Type'] in ['Series-C: GI/IS DI (32) 24 VDC SOE Relay (0-5000)','Series-C: GI/IS DI (32) 24 VDC SOE Relay LFD (0-5000)','Series-C: GI/IS DI (32) 24VDC Relay with Expansion Board (0-5000)']:
                rgIoSum1[276] += int(giis['Red_IS']) if giis['Red_IS']!='' else 0
                rgIoSum1[277] += int(giis['Future_Red_IS']) if giis['Future_Red_IS']!='' else 0
                rgIoSum1[275] += int(giis['Non_Red_IS']) if giis['Non_Red_IS']!='' else 0
            if giis['IO_Type'] in ['Series-C: GI/IS DI (32) 24VDC SOE Solid State (0-5000)']:
                rgIoSum1[278] = int(giis['Non_Red_IS']) if giis['Non_Red_IS']!='' else 0
            if giis['IO_Type'] in ['Series-C: GI/IS DI (32) 24VDC SOE Relay with Expansion Board (0-5000)']:
                rgIoSum1[279] = int(giis['Non_Red_IS']) if giis['Non_Red_IS']!='' else 0
    if io_Family=="seriesC" and cont_req =='Yes' and Mounting_Solution !='Yes':
        for rail in rail1:
            if rail['IO_Type'] in ['Series-C: UIO (32) Analog Input (0-5000)']:
                rgIoSum1[123] = int(rail['Red_IS']) if rail['Red_IS']!='' else 0
                rgIoSum1[124] = int(rail['Future_Red_IS']) if rail['Future_Red_IS']!='' else 0
                rgIoSum1[125] = int(rail['Non_Red_IS']) if rail['Non_Red_IS']!='' else 0
                rgIoSum1[126] = int(rail['Red_NIS']) if rail['Red_NIS']!='' else 0
                rgIoSum1[127] = int(rail['Future_Red_NIS']) if rail['Future_Red_NIS']!='' else 0
                rgIoSum1[128] = int(rail['Non_Red_NIS']) if rail['Non_Red_NIS']!='' else 0
                rgIoSum1[129] = int(rail['Red_ISLTR']) if rail['Red_ISLTR']!='' else 0
                rgIoSum1[130] = int(rail['Future_Red_ISLTR']) if rail['Future_Red_ISLTR']!='' else 0
                rgIoSum1[131] = int(rail['Non_Red_ISLTR']) if rail['Non_Red_ISLTR']!='' else 0 
            if rail['IO_Type'] in ['Series-C: UIO (32) Analog Output (0-5000)']:
                rgIoSum1[189] = int(rail['Red_IS']) if rail['Red_IS']!='' else 0
                rgIoSum1[190] = int(rail['Future_Red_IS']) if rail['Future_Red_IS']!='' else 0
                rgIoSum1[191] = int(rail['Non_Red_IS']) if rail['Non_Red_IS']!='' else 0
                rgIoSum1[192] = int(rail['Red_NIS']) if rail['Red_NIS']!='' else 0
                rgIoSum1[193] = int(rail['Future_Red_NIS']) if rail['Future_Red_NIS']!='' else 0
                rgIoSum1[194] = int(rail['Non_Red_NIS']) if rail['Non_Red_NIS']!='' else 0
                rgIoSum1[195] = int(rail['Red_ISLTR']) if rail['Red_ISLTR']!='' else 0
                rgIoSum1[196] = int(rail['Future_Red_ISLTR']) if rail['Future_Red_ISLTR']!='' else 0
                rgIoSum1[197] = int(rail['Non_Red_ISLTR']) if rail['Non_Red_ISLTR']!='' else 0 
        for rail in rail2:
            if rail['IO_Type'] in ['Series-C: UIO (32) Digital Input (0-5000)']:
                rgIoSum1[304] = int(rail['Red_IS']) if rail['Red_IS']!='' else 0
                rgIoSum1[305] = int(rail['Future_Red_IS']) if rail['Future_Red_IS']!='' else 0
                rgIoSum1[306] = int(rail['Non_Red_IS']) if rail['Non_Red_IS']!='' else 0
                rgIoSum1[307] = int(rail['Red_NIS']) if rail['Red_NIS']!='' else 0
                rgIoSum1[308] = int(rail['Future_Red_NIS']) if rail['Future_Red_NIS']!='' else 0
                rgIoSum1[309] = int(rail['Non_Red_NIS']) if rail['Non_Red_NIS']!='' else 0
                rgIoSum1[310] = int(rail['Red_ISLTR']) if rail['Red_ISLTR']!='' else 0
                rgIoSum1[311] = int(rail['Future_Red_ISLTR']) if rail['Future_Red_ISLTR']!='' else 0
                rgIoSum1[312] = int(rail['Non_Red_ISLTR']) if rail['Non_Red_ISLTR']!='' else 0 
                rgIoSum1[313] = int(rail['Red_RLY']) if rail['Red_RLY']!='' else 0
                rgIoSum1[314] = int(rail['Future_Red_RLY']) if rail['Future_Red_RLY']!='' else 0
                rgIoSum1[315] = int(rail['Non_Red_RLY']) if rail['Non_Red_RLY']!='' else 0
                rgIoSum1[605] = int(rail['Red_HV_RLY']) if rail['Red_HV_RLY']!='' else 0
                rgIoSum1[606] = int(rail['Future_Red_HV_RLY']) if rail['Future_Red_HV_RLY']!='' else 0
                rgIoSum1[607] = int(rail['Non_Red_HV_RLY']) if rail['Non_Red_HV_RLY']!='' else 0
            if rail['IO_Type'] in ['Series-C: UIO (32) Digital Output (0-5000)']:
                rgIoSum1[401] = int(rail['Red_IS']) if rail['Red_IS']!='' else 0
                rgIoSum1[402] = int(rail['Future_Red_IS']) if rail['Future_Red_IS']!='' else 0
                rgIoSum1[403] = int(rail['Non_Red_IS']) if rail['Non_Red_IS']!='' else 0
                rgIoSum1[404] = int(rail['Red_NIS']) if rail['Red_NIS']!='' else 0
                rgIoSum1[405] = int(rail['Future_Red_NIS']) if rail['Future_Red_NIS']!='' else 0
                rgIoSum1[406] = int(rail['Non_Red_NIS']) if rail['Non_Red_NIS']!='' else 0
                rgIoSum1[407] = int(rail['Red_ISLTR']) if rail['Red_ISLTR']!='' else 0
                rgIoSum1[408] = int(rail['Future_Red_ISLTR']) if rail['Future_Red_ISLTR']!='' else 0
                rgIoSum1[409] = int(rail['Non_Red_ISLTR']) if rail['Non_Red_ISLTR']!='' else 0 
                rgIoSum1[410] = int(rail['Red_RLY']) if rail['Red_RLY']!='' else 0
                rgIoSum1[411] = int(rail['Future_Red_RLY']) if rail['Future_Red_RLY']!='' else 0
                rgIoSum1[412] = int(rail['Non_Red_RLY']) if rail['Non_Red_RLY']!='' else 0
                rgIoSum1[602] = int(rail['Red_HV_RLY']) if rail['Red_HV_RLY']!='' else 0
                rgIoSum1[603] = int(rail['Future_Red_HV_RLY']) if rail['Future_Red_HV_RLY']!='' else 0
                rgIoSum1[604] = int(rail['Non_Red_HV_RLY']) if rail['Non_Red_HV_RLY']!='' else 0
    if io_Family=="TurboM" and Mounting_Solution !='Yes':
        cont= rg.SelectedAttributes.GetContainerByName("C300_TurboM_IOM_RG_Cont").Rows
        for i in cont:
            if i['IO_Type'] in ['Number of Servo Position Modules (0-480)']:
                rgIoSum1[431] += int(i['Red_IOM']) if i['Red_IOM']!='' else 0
            if i['IO_Type'] in ['Number of Speed Protection Modules (0-480)']:
                rgIoSum1[432] += int(i['Red_IOM']) if i['Red_IOM']!='' else 0
    if pmio=="Yes" and Mounting_Solution !='Yes':
        cont1=rg.SelectedAttributes.GetContainerByName("C300_SerC_PointCount_PMIO_RG_Cont").Rows
        cont2=rg.SelectedAttributes.GetContainerByName("C300_SerC_PointCount_PMIO_RG_RlyCont").Rows
        cont3=rg.SelectedAttributes.GetContainerByName("SerC_PMIO_CG_Group").Rows
        for pmio in cont1:
            if pmio['IO_Type'] in ['PMIO HLAI (16) (0-5000)']:
                rgIoSum1[433] = int(pmio['Red_IS']) if pmio['Red_IS']!='' else 0
                rgIoSum1[434] = int(pmio['Future_Red_IS']) if pmio['Future_Red_IS']!='' else 0
                rgIoSum1[435] = int(pmio['Non_Red_IS']) if pmio['Non_Red_IS']!='' else 0
                rgIoSum1[436] = int(pmio['Red_NIS']) if pmio['Red_NIS']!='' else 0
                rgIoSum1[437] = int(pmio['Future_Red_NIS']) if pmio['Future_Red_NIS']!='' else 0
                rgIoSum1[438] = int(pmio['Non_Red_NIS']) if pmio['Non_Red_NIS']!='' else 0
            if pmio['IO_Type'] in ['PMIO HLAI (16) w/ External HART Mux (0-5000)']:
                rgIoSum1[439] = int(pmio['Red_IS']) if pmio['Red_IS']!='' else 0
                rgIoSum1[440] = int(pmio['Future_Red_IS']) if pmio['Future_Red_IS']!='' else 0
                rgIoSum1[441] = int(pmio['Red_NIS']) if pmio['Red_NIS']!='' else 0
                rgIoSum1[442] = int(pmio['Future_Red_NIS']) if pmio['Future_Red_NIS']!='' else 0
            if pmio['IO_Type'] in ['PMIO HLAI Active HART (16) (0-5000)']:
                rgIoSum1[443] = int(pmio['Red_IS']) if pmio['Red_IS']!='' else 0
                rgIoSum1[444] = int(pmio['Future_Red_IS']) if pmio['Future_Red_IS']!='' else 0
                rgIoSum1[445] = int(pmio['Non_Red_IS']) if pmio['Non_Red_IS']!='' else 0
                rgIoSum1[446] = int(pmio['Red_NIS']) if pmio['Red_NIS']!='' else 0
                rgIoSum1[447] = int(pmio['Future_Red_NIS']) if pmio['Future_Red_NIS']!='' else 0
                rgIoSum1[448] = int(pmio['Non_Red_NIS']) if pmio['Non_Red_NIS']!='' else 0
            if pmio['IO_Type'] in ['PMIO HLAI Enhanced Power (16) (0-5000)']:
                rgIoSum1[449] = int(pmio['Red_IS']) if pmio['Red_IS']!='' else 0
                rgIoSum1[450] = int(pmio['Future_Red_IS']) if pmio['Future_Red_IS']!='' else 0
                rgIoSum1[451] = int(pmio['Red_NIS']) if pmio['Red_NIS']!='' else 0
                rgIoSum1[452] = int(pmio['Future_Red_NIS']) if pmio['Future_Red_NIS']!='' else 0
            if pmio['IO_Type'] in ['PMIO LLAI (8) (0-5000)']:
                rgIoSum1[453] = int(pmio['Non_Red_IS']) if pmio['Non_Red_IS']!='' else 0
                rgIoSum1[454] = int(pmio['Non_Red_NIS']) if pmio['Non_Red_NIS']!='' else 0
            if pmio['IO_Type'] in ['PMIO LLAI Mux PMIO Remote CJR (16) (0-5000)']:
                rgIoSum1[455] = int(pmio['Non_Red_IS']) if pmio['Non_Red_IS']!='' else 0
                rgIoSum1[456] = int(pmio['Non_Red_NIS']) if pmio['Non_Red_NIS']!='' else 0
            if pmio['IO_Type'] in ['PMIO LLAI Mux PMIO RTD (16) (0-5000)']:
                rgIoSum1[457] = int(pmio['Non_Red_IS']) if pmio['Non_Red_IS']!='' else 0
                rgIoSum1[458] = int(pmio['Non_Red_NIS']) if pmio['Non_Red_NIS']!='' else 0
            if pmio['IO_Type'] in ['PMIO LLAI Mux PMIO TC (16) (0-5000)']:
                rgIoSum1[459] = int(pmio['Non_Red_IS']) if pmio['Non_Red_IS']!='' else 0
                rgIoSum1[460] = int(pmio['Non_Red_NIS']) if pmio['Non_Red_NIS']!='' else 0
            if pmio['IO_Type'] in ['PMIO RHMUX (32)  w/NI Pwr Adptr (0-5000)']:
                rgIoSum1[461] = int(pmio['Non_Red_IS']) if pmio['Non_Red_IS']!='' else 0
                rgIoSum1[462] = int(pmio['Non_Red_NIS']) if pmio['Non_Red_NIS']!='' else 0
            if pmio['IO_Type'] in ['PMIO STI (16) (0-5000)']:
                rgIoSum1[463] = int(pmio['Red_IS']) if pmio['Red_IS']!='' else 0
                rgIoSum1[464] = int(pmio['Future_Red_IS']) if pmio['Future_Red_IS']!='' else 0
                rgIoSum1[465] = int(pmio['Non_Red_IS']) if pmio['Non_Red_IS']!='' else 0
                rgIoSum1[466] = int(pmio['Red_NIS']) if pmio['Red_NIS']!='' else 0
                rgIoSum1[467] = int(pmio['Future_Red_NIS']) if pmio['Future_Red_NIS']!='' else 0
                rgIoSum1[468] = int(pmio['Non_Red_NIS']) if pmio['Non_Red_NIS']!='' else 0
            if pmio['IO_Type'] in ['PMIO STI Enhanced Power (16) (0-5000)']:
                rgIoSum1[469] = int(pmio['Future_Red_IS']) if pmio['Future_Red_IS']!='' else 0
                rgIoSum1[470] = int(pmio['Future_Red_NIS']) if pmio['Future_Red_NIS']!='' else 0
            if pmio['IO_Type'] in ['PMIO AO HD (16) (0-5000)']:
                rgIoSum1[471] = int(pmio['Red_IS']) if pmio['Red_IS']!='' else 0
                rgIoSum1[472] = int(pmio['Future_Red_IS']) if pmio['Future_Red_IS']!='' else 0
                rgIoSum1[473] = int(pmio['Red_NIS']) if pmio['Red_NIS']!='' else 0
                rgIoSum1[474] = int(pmio['Future_Red_NIS']) if pmio['Future_Red_NIS']!='' else 0
            if pmio['IO_Type'] in ['PMIO AO HD w/ External HART Mux (16) (0-5000)']:
                rgIoSum1[475] = int(pmio['Red_IS']) if pmio['Red_IS']!='' else 0
                rgIoSum1[476] = int(pmio['Future_Red_IS']) if pmio['Future_Red_IS']!='' else 0
                rgIoSum1[477] = int(pmio['Red_NIS']) if pmio['Red_NIS']!='' else 0
                rgIoSum1[478] = int(pmio['Future_Red_NIS']) if pmio['Future_Red_NIS']!='' else 0
            if pmio['IO_Type'] in ['PMIO AO Active HART (0-5000)']:
                rgIoSum1[479] = int(pmio['Red_IS']) if pmio['Red_IS']!='' else 0
                rgIoSum1[480] = int(pmio['Future_Red_IS']) if pmio['Future_Red_IS']!='' else 0
                rgIoSum1[481] = int(pmio['Red_NIS']) if pmio['Red_NIS']!='' else 0
                rgIoSum1[482] = int(pmio['Future_Red_NIS']) if pmio['Future_Red_NIS']!='' else 0
        for pmio in cont2:
            if pmio['IO_Type'] in ['PMIO DI 24 VDC (32) (0-5000)']:
                rgIoSum1[483] = int(pmio['Non_Red_IS']) if pmio['Non_Red_IS']!='' else 0
                rgIoSum1[484] = int(pmio['Non_Red_NIS']) if pmio['Non_Red_NIS']!='' else 0
            if pmio['IO_Type'] in ['PMIO DI 24 HD VDC (32) (0-5000)']:
                rgIoSum1[485] = int(pmio['Red_IS']) if pmio['Red_IS']!='' else 0
                rgIoSum1[486] = int(pmio['Future_Red_IS']) if pmio['Future_Red_IS']!='' else 0
                rgIoSum1[487] = int(pmio['Red_NIS']) if pmio['Red_NIS']!='' else 0
                rgIoSum1[488] = int(pmio['Future_Red_NIS']) if pmio['Future_Red_NIS']!='' else 0
            if pmio['IO_Type'] in ['PMIO DI SOE 24 VDC (32) (0-5000)']:
                rgIoSum1[489] = int(pmio['Red_IS']) if pmio['Red_IS']!='' else 0
                rgIoSum1[490] = int(pmio['Non_Red_IS']) if pmio['Non_Red_IS']!='' else 0
                rgIoSum1[491] = int(pmio['Red_NIS']) if pmio['Red_NIS']!='' else 0
                rgIoSum1[492] = int(pmio['Non_Red_NIS']) if pmio['Non_Red_NIS']!='' else 0
            if pmio['IO_Type'] in ['PMIO DI 120 VAC (32) (0-5000)']:
                rgIoSum1[493] = int(pmio['Non_Red_IS']) if pmio['Non_Red_IS']!='' else 0
                rgIoSum1[494] = int(pmio['Non_Red_NIS']) if pmio['Non_Red_NIS']!='' else 0
            if pmio['IO_Type'] in ['PMIO DI SOE 120 VAC (32) (0-5000)']:
                rgIoSum1[495] = int(pmio['Red_IS']) if pmio['Red_IS']!='' else 0
                rgIoSum1[496] = int(pmio['Non_Red_IS']) if pmio['Non_Red_IS']!='' else 0
                rgIoSum1[497] = int(pmio['Red_NIS']) if pmio['Red_NIS']!='' else 0
                rgIoSum1[498] = int(pmio['Non_Red_NIS']) if pmio['Non_Red_NIS']!='' else 0
            if pmio['IO_Type'] in ['PMIO DI 240 VAC (32) (0-5000)']:
                rgIoSum1[499] = int(pmio['Non_Red_IS']) if pmio['Non_Red_IS']!='' else 0
                rgIoSum1[500] = int(pmio['Non_Red_NIS']) if pmio['Non_Red_NIS']!='' else 0
            if pmio['IO_Type'] in ['PMIO DI SOE 240 VAC (32) (0-5000)']:
                rgIoSum1[501] = int(pmio['Red_IS']) if pmio['Red_IS']!='' else 0
                rgIoSum1[502] = int(pmio['Non_Red_IS']) if pmio['Non_Red_IS']!='' else 0
                rgIoSum1[503] = int(pmio['Red_NIS']) if pmio['Red_NIS']!='' else 0
                rgIoSum1[504] = int(pmio['Non_Red_NIS']) if pmio['Non_Red_NIS']!='' else 0
            if pmio['IO_Type'] in ['PMIO DO 24 VDC (16) (0-5000)']:
                rgIoSum1[505] = int(pmio['Non_Red_IS']) if pmio['Non_Red_IS']!='' else 0
                rgIoSum1[506] = int(pmio['Non_Red_NIS']) if pmio['Non_Red_NIS']!='' else 0
            if pmio['IO_Type'] in ['PMIO DO 24 VDC HD (32) (0-5000)']:
                rgIoSum1[507] = int(pmio['Red_IS']) if pmio['Red_IS']!='' else 0
                rgIoSum1[508] = int(pmio['Future_Red_IS']) if pmio['Future_Red_IS']!='' else 0
                rgIoSum1[509] = int(pmio['Red_NIS']) if pmio['Red_NIS']!='' else 0
                rgIoSum1[510] = int(pmio['Future_Red_NIS']) if pmio['Future_Red_NIS']!='' else 0
            if pmio['IO_Type'] in ['PMIO DO 3 to 30 VDC (16) (0-5000)']:
                rgIoSum1[511] = int(pmio['Non_Red_IS']) if pmio['Non_Red_IS']!='' else 0
                rgIoSum1[512] = int(pmio['Non_Red_NIS']) if pmio['Non_Red_NIS']!='' else 0
            if pmio['IO_Type'] in ['PMIO DO 31 to 200 VDC (16) (0-5000)']:
                rgIoSum1[513] = int(pmio['Non_Red_IS']) if pmio['Non_Red_IS']!='' else 0
                rgIoSum1[514] = int(pmio['Non_Red_NIS']) if pmio['Non_Red_NIS']!='' else 0
            if pmio['IO_Type'] in ['PMIO DO 120/240 VAC SS (16) (0-5000)']:
                rgIoSum1[515] = int(pmio['Non_Red_IS']) if pmio['Non_Red_IS']!='' else 0
                rgIoSum1[516] = int(pmio['Non_Red_NIS']) if pmio['Non_Red_NIS']!='' else 0
            if pmio['IO_Type'] in ['PMIO DO HD Relay (32) (0-5000)']:
                rgIoSum1[517] = int(pmio['Red_IS']) if pmio['Red_IS']!='' else 0
                rgIoSum1[518] = int(pmio['Future_Red_IS']) if pmio['Future_Red_IS']!='' else 0
                rgIoSum1[519] = int(pmio['Red_NIS']) if pmio['Red_NIS']!='' else 0
                rgIoSum1[520] = int(pmio['Future_Red_NIS']) if pmio['Future_Red_NIS']!='' else 0
            if pmio['IO_Type'] in ['PMIO DO 120 VAC Relay (16) (0-5000)']:
                rgIoSum1[521] = int(pmio['Non_Red_IS']) if pmio['Non_Red_IS']!='' else 0
                rgIoSum1[522] = int(pmio['Non_Red_NIS']) if pmio['Non_Red_NIS']!='' else 0
            if pmio['IO_Type'] in ['PMIO DO 240 VAC Relay (16) (0-5000)']:
                rgIoSum1[523] = int(pmio['Non_Red_IS']) if pmio['Non_Red_IS']!='' else 0
                rgIoSum1[524] = int(pmio['Non_Red_NIS']) if pmio['Non_Red_NIS']!='' else 0
        for pmio in cont3:
            if pmio['IO_Type'] in ['PMIO GI/IS AO (16) External HART  (0-5000)']:
                rgIoSum1[525] = int(pmio['Red_IS']) if pmio['Red_IS']!='' else 0
                rgIoSum1[526] = int(pmio['Future_Red_IS']) if pmio['Future_Red_IS']!='' else 0
            if pmio['IO_Type'] in ['PMIO GI/IS AO (16) Active HART  (0-5000)']:
                rgIoSum1[527] = int(pmio['Red_IS']) if pmio['Red_IS']!='' else 0
                rgIoSum1[528] = int(pmio['Future_Red_IS']) if pmio['Future_Red_IS']!='' else 0
            if pmio['IO_Type'] in ['PMIO GI/IS DI (32)  (0-5000)']:
                rgIoSum1[529] = int(pmio['Non_Red_IS']) if pmio['Non_Red_IS']!='' else 0
            if pmio['IO_Type'] in ['PMIO GI/IS DI SOE (32)  (0-5000)']:
                rgIoSum1[530] = int(pmio['Red_IS']) if pmio['Red_IS']!='' else 0
                rgIoSum1[531] = int(pmio['Non_Red_IS']) if pmio['Non_Red_IS']!='' else 0
            if pmio['IO_Type'] in ['PMIO GI/IS DI Solid State SOE (32)  (0-5000)']:
                rgIoSum1[532] = int(pmio['Red_IS']) if pmio['Red_IS']!='' else 0
                rgIoSum1[533] = int(pmio['Non_Red_IS']) if pmio['Non_Red_IS']!='' else 0
            if pmio['IO_Type'] in ['PMIO GI/IS DI Solid State (32)  (0-5000)']:
                rgIoSum1[534] = int(pmio['Non_Red_IS']) if pmio['Non_Red_IS']!='' else 0
            if pmio['IO_Type'] in ['PMIO GI/IS DO LFD (16)  (0-5000)']:
                rgIoSum1[535] = int(pmio['Non_Red_IS']) if pmio['Non_Red_IS']!='' else 0
            if pmio['IO_Type'] in ['PMIO GI/IS DO (16)  (0-5000)']:
                rgIoSum1[536] = int(pmio['Non_Red_IS']) if pmio['Non_Red_IS']!='' else 0
            if pmio['IO_Type'] in ['PMIO GI/IS DO (32) Via non red combine panel  (0-5000)']:
                rgIoSum1[537] = int(pmio['Non_Red_IS']) if pmio['Non_Red_IS']!='' else 0
            if pmio['IO_Type'] in ['PMIO GI/IS HLAI Aux PMIO Cur (16)  (0-5000)']:
                rgIoSum1[538] = int(pmio['Red_IS']) if pmio['Red_IS']!='' else 0
                rgIoSum1[539] = int(pmio['Non_Red_IS']) if pmio['Non_Red_IS']!='' else 0
            if pmio['IO_Type'] in ['PMIO GI/IS HLAI Aux PMIO Cur External HART (16)  (0-5000)']:
                rgIoSum1[540] = int(pmio['Red_IS']) if pmio['Red_IS']!='' else 0
                rgIoSum1[541] = int(pmio['Non_Red_IS']) if pmio['Non_Red_IS']!='' else 0
            if pmio['IO_Type'] in ['PMIO GI/IS HLAI Aux & Hi V (16)  (0-5000)']:
                rgIoSum1[542] = int(pmio['Red_IS']) if pmio['Red_IS']!='' else 0
                rgIoSum1[543] = int(pmio['Non_Red_IS']) if pmio['Non_Red_IS']!='' else 0
            if pmio['IO_Type'] in ['PMIO GI/IS HLAI Active HART Aux Current (16)  (0-5000)']:
                rgIoSum1[544] = int(pmio['Red_IS']) if pmio['Red_IS']!='' else 0
                rgIoSum1[545] = int(pmio['Non_Red_IS']) if pmio['Non_Red_IS']!='' else 0
            if pmio['IO_Type'] in ['PMIO GI/IS HLAI Active HART Aux & Hi V (16)  (0-5000)']:
                rgIoSum1[546] = int(pmio['Red_IS']) if pmio['Red_IS']!='' else 0
                rgIoSum1[547] = int(pmio['Non_Red_IS']) if pmio['Non_Red_IS']!='' else 0
            if pmio['IO_Type'] in ['PMIO GI/IS STI Aux PMIO Current (16)  (0-5000)']:
                rgIoSum1[548] = int(pmio['Red_IS']) if pmio['Red_IS']!='' else 0
                rgIoSum1[549] = int(pmio['Non_Red_IS']) if pmio['Non_Red_IS']!='' else 0
            if pmio['IO_Type'] in ['PMIO GI/IS STI Aux PMIO Current External HART (16)  (0-5000)']:
                rgIoSum1[550] = int(pmio['Red_IS']) if pmio['Red_IS']!='' else 0
                rgIoSum1[551] = int(pmio['Future_Red_IS']) if pmio['Future_Red_IS']!='' else 0
            if pmio['IO_Type'] in ['PMIO GI/IS STI Aux & Hi V (16)  (0-5000)']:
                rgIoSum1[552] = int(pmio['Red_IS']) if pmio['Red_IS']!='' else 0
                rgIoSum1[553] = int(pmio['Non_Red_IS']) if pmio['Non_Red_IS']!='' else 0
    return rgIoSum1