def populateC300Data2(Quote,child):
	child=child
	ioSum1=[0]*800
	n = RIO_CNT = LIO_CNT = 0
	ms_attr =child.SelectedAttributes.GetContainerByName("Document_cont_c300").Rows
	for io_f in ms_attr:
		io_Family=io_f['Io_family']
		ioSum1[554] = io_f['Io_family']
		Trace.Write('Io_family '+str(io_Family))
		universal=io_f['SerC_CG_Universal_Marshalling_Cabinet']
		Trace.Write('universal '+str(universal))
		fmio=io_f['SerC_CG_Foundation_Fieldbus_Interface_required']
		ioSum1[555] = io_f['SerC_CG_Foundation_Fieldbus_Interface_required']
		Trace.Write('fmio '+str(fmio))
		pmio=io_f['SerC_CG_PM_IO_Solution_required']
		ioSum1[556] = io_f['SerC_CG_PM_IO_Solution_required']
		Trace.Write('pmio '+str(pmio))
		Profibus=io_f['Profibus Gateway Interface']
		ioSum1[557] = io_f['Profibus Gateway Interface']
		Ethernet=io_f['Ethernet Interface']
		ioSum1[558] = io_f['Ethernet Interface']
		Slave_devicesRed=io_f['Number of Profibus DP Slave devicesRed']
		Slave_devicesNRed=io_f['Number of Profibus DP Slave devicesNred']
		Red_ControlLogix=io_f['Red ControlLogix Processors']
		NRed_ControlLogix=io_f['NonRed ControlLogix Processors']
		Red_Process=io_f['Red Process Connected IO Devices']
		NRed_Process=io_f['NonRed Process Connected IO Devices']
		Mounting_solution=io_f['Mounting_solution']
		ioSum1[559] = io_f['C300_CG_Total_IO_Load']
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
	if  True:
		for ms in EN1:
			if ms['IO_Type'] in ['Series-C: DO (32) 24VDC Bus External Power Supply (0-5000)']:
				ioSum1[316] = int(ms['Red_IS']) if ms['Red_IS']!='' else 0
				ioSum1[318] = int(ms['Future_Red_IS']) if ms['Future_Red_IS']!='' else 0
				ioSum1[320] = int(ms['Non_Red_IS']) if ms['Non_Red_IS']!='' else 0
				ioSum1[322] = int(ms['Red_NIS']) if ms['Red_NIS']!='' else 0
				ioSum1[324] = int(ms['Future_Red_NIS']) if ms['Future_Red_NIS']!='' else 0
				ioSum1[326] = int(ms['Non_Red_NIS']) if ms['Non_Red_NIS']!='' else 0
				ioSum1[328] = int(ms['Red_ISLTR']) if ms['Red_ISLTR']!='' else 0
				ioSum1[330] = int(ms['Future_Red_ISLTR']) if ms['Future_Red_ISLTR']!='' else 0
				ioSum1[332] = int(ms['Non_Red_ISLTR']) if ms['Non_Red_ISLTR']!='' else 0 
				ioSum1[334] = int(ms['Red_RLY']) if ms['Red_RLY']!='' else 0
				ioSum1[336] = int(ms['Future_Red_RLY']) if ms['Future_Red_RLY']!='' else 0
				ioSum1[338] = int(ms['Non_Red_RLY']) if ms['Non_Red_RLY']!='' else 0
				ioSum1[584] = int(ms['Red_HV_RLY']) if ms['Red_HV_RLY']!='' else 0
				ioSum1[586] = int(ms['Future_Red_HV_RLY']) if ms['Future_Red_HV_RLY']!='' else 0
				ioSum1[588] = int(ms['Non_Red_HV_RLY']) if ms['Non_Red_HV_RLY']!='' else 0
			if ms['IO_Type'] in ['Series-C: DO (32) 24VDC Bus Internal Power Supply (0-5000)']:
				ioSum1[340] = int(ms['Red_IS']) if ms['Red_IS']!='' else 0
				ioSum1[342] = int(ms['Future_Red_IS']) if ms['Future_Red_IS']!='' else 0
				ioSum1[344] = int(ms['Non_Red_IS']) if ms['Non_Red_IS']!='' else 0
				ioSum1[346] = int(ms['Red_NIS']) if ms['Red_NIS']!='' else 0
				ioSum1[348] = int(ms['Future_Red_NIS']) if ms['Future_Red_NIS']!='' else 0
				ioSum1[350] = int(ms['Non_Red_NIS']) if ms['Non_Red_NIS']!='' else 0
				ioSum1[352] = int(ms['Red_ISLTR']) if ms['Red_ISLTR']!='' else 0
				ioSum1[354] = int(ms['Future_Red_ISLTR']) if ms['Future_Red_ISLTR']!='' else 0
				ioSum1[356] = int(ms['Non_Red_ISLTR']) if ms['Non_Red_ISLTR']!='' else 0 
				ioSum1[358] = int(ms['Red_RLY']) if ms['Red_RLY']!='' else 0
				ioSum1[360] = int(ms['Future_Red_RLY']) if ms['Future_Red_RLY']!='' else 0
				ioSum1[362] = int(ms['Non_Red_RLY']) if ms['Non_Red_RLY']!='' else 0
				ioSum1[590] = int(ms['Red_HV_RLY']) if ms['Red_HV_RLY']!='' else 0
				ioSum1[592] = int(ms['Future_Red_HV_RLY']) if ms['Future_Red_HV_RLY']!='' else 0
				ioSum1[594] = int(ms['Non_Red_HV_RLY']) if ms['Non_Red_HV_RLY']!='' else 0
			if ms['IO_Type'] in ['SCM: DO (32) 24VDC Bus External Power Supply (0-5000)']:
				ioSum1[317] += int(ms['Red_IS']) if ms['Red_IS']!='' else 0
				ioSum1[319] += int(ms['Future_Red_IS']) if ms['Future_Red_IS']!='' else 0
				ioSum1[321] += int(ms['Non_Red_IS']) if ms['Non_Red_IS']!='' else 0
				ioSum1[323] += int(ms['Red_NIS']) if ms['Red_NIS']!='' else 0
				ioSum1[325] += int(ms['Future_Red_NIS']) if ms['Future_Red_NIS']!='' else 0
				ioSum1[327] += int(ms['Non_Red_NIS']) if ms['Non_Red_NIS']!='' else 0
				ioSum1[329] += int(ms['Red_ISLTR']) if ms['Red_ISLTR']!='' else 0
				ioSum1[331] += int(ms['Future_Red_ISLTR']) if ms['Future_Red_ISLTR']!='' else 0
				ioSum1[333] += int(ms['Non_Red_ISLTR']) if ms['Non_Red_ISLTR']!='' else 0 
				ioSum1[335] += int(ms['Red_RLY']) if ms['Red_RLY']!='' else 0
				ioSum1[337] += int(ms['Future_Red_RLY']) if ms['Future_Red_RLY']!='' else 0
				ioSum1[339] += int(ms['Non_Red_RLY']) if ms['Non_Red_RLY']!='' else 0
				ioSum1[585] += int(ms['Red_HV_Rly']) if ms['Red_HV_Rly']!='' else 0
				ioSum1[587] += int(ms['Future_HV_Rly']) if ms['Future_HV_Rly']!='' else 0
				ioSum1[589] += int(ms['Non_Red_HV_Rly']) if ms['Non_Red_HV_Rly']!='' else 0
			if ms['IO_Type'] in ['SCM: DO (32) 24VDC Bus Internal Power Supply (0-5000)']:
				ioSum1[341] += int(ms['Red_IS']) if ms['Red_IS']!='' else 0
				ioSum1[343] += int(ms['Future_Red_IS']) if ms['Future_Red_IS']!='' else 0
				ioSum1[345] += int(ms['Non_Red_IS']) if ms['Non_Red_IS']!='' else 0
				ioSum1[347] += int(ms['Red_NIS']) if ms['Red_NIS']!='' else 0
				ioSum1[349] += int(ms['Future_Red_NIS']) if ms['Future_Red_NIS']!='' else 0
				ioSum1[351] += int(ms['Non_Red_NIS']) if ms['Non_Red_NIS']!='' else 0
				ioSum1[353] += int(ms['Red_ISLTR']) if ms['Red_ISLTR']!='' else 0
				ioSum1[355] += int(ms['Future_Red_ISLTR']) if ms['Future_Red_ISLTR']!='' else 0
				ioSum1[357] += int(ms['Non_Red_ISLTR']) if ms['Non_Red_ISLTR']!='' else 0 
				ioSum1[359] += int(ms['Red_RLY']) if ms['Red_RLY']!='' else 0
				ioSum1[361] += int(ms['Future_Red_RLY']) if ms['Future_Red_RLY']!='' else 0
				ioSum1[363] += int(ms['Non_Red_RLY']) if ms['Non_Red_RLY']!='' else 0
				ioSum1[591] += int(ms['Red_HV_RLY']) if ms['Red_HV_RLY']!='' else 0
				ioSum1[593] += int(ms['Future_HV_Rly']) if ms['Future_HV_Rly']!='' else 0
				ioSum1[595] += int(ms['Non_Red_HV_RLY']) if ms['Non_Red_HV_RLY']!='' else 0
	if io_Family =="Mark2":
		MS3 =child.SelectedAttributes.GetContainerByName("C300_C IO MS3").Rows
		for ms in MS3:
			if ms['IO_Type'] in ['SCM: DI (32) 24VDC (0-5000)']:
				ioSum1[198] = int(ms['Red_IS']) if ms['Red_IS']!='' else 0
				ioSum1[199] = int(ms['Future_Red_IS']) if ms['Future_Red_IS']!='' else 0
				ioSum1[200] = int(ms['Non_Red_IS']) if ms['Non_Red_IS']!='' else 0
				ioSum1[201] = int(ms['Red_NIS']) if ms['Red_NIS']!='' else 0
				ioSum1[202] = int(ms['Future_Red_NIS']) if ms['Future_Red_NIS']!='' else 0
				ioSum1[203] = int(ms['Non_Red_NIS']) if ms['Non_Red_NIS']!='' else 0
				ioSum1[204] = int(ms['Red_ISLTR']) if ms['Red_ISLTR']!='' else 0
				ioSum1[205] = int(ms['Future_Red_ISLTR']) if ms['Future_Red_ISLTR']!='' else 0
				ioSum1[206] = int(ms['Non_Red_ISLTR']) if ms['Non_Red_ISLTR']!='' else 0 
				ioSum1[207] = int(ms['Red_RLY']) if ms['Red_RLY']!='' else 0
				ioSum1[208] = int(ms['Future_Red_RLY']) if ms['Future_Red_RLY']!='' else 0
				ioSum1[209] = int(ms['Non_Red_RLY']) if ms['Non_Red_RLY']!='' else 0
				ioSum1[560] = int(ms['Red_HV_Rly']) if ms['Red_HV_Rly']!='' else 0
				ioSum1[561] = int(ms['Future_HV_Rly']) if ms['Future_HV_Rly']!='' else 0
				ioSum1[562] = int(ms['Non_Red_HV_Rly']) if ms['Non_Red_HV_Rly']!='' else 0
			if ms['IO_Type'] in ['SCM: DI (32) 24VDC SOE (0-5000)']:
				ioSum1[235] = int(ms['Red_IS']) if ms['Red_IS']!='' else 0
				ioSum1[237] = int(ms['Future_Red_IS']) if ms['Future_Red_IS']!='' else 0
				ioSum1[239] = int(ms['Non_Red_IS']) if ms['Non_Red_IS']!='' else 0
				ioSum1[241] = int(ms['Red_NIS']) if ms['Red_NIS']!='' else 0
				ioSum1[243] = int(ms['Future_Red_NIS']) if ms['Future_Red_NIS']!='' else 0
				ioSum1[245] = int(ms['Non_Red_NIS']) if ms['Non_Red_NIS']!='' else 0
				ioSum1[247] = int(ms['Red_ISLTR']) if ms['Red_ISLTR']!='' else 0
				ioSum1[249] = int(ms['Future_Red_ISLTR']) if ms['Future_Red_ISLTR']!='' else 0
				ioSum1[251] = int(ms['Non_Red_ISLTR']) if ms['Non_Red_ISLTR']!='' else 0 
				ioSum1[253] = int(ms['Red_RLY']) if ms['Red_RLY']!='' else 0
				ioSum1[255] = int(ms['Future_Red_RLY']) if ms['Future_Red_RLY']!='' else 0
				ioSum1[257] = int(ms['Non_Red_RLY']) if ms['Non_Red_RLY']!='' else 0
				ioSum1[570] = int(ms['Red_HV_Rly']) if ms['Red_HV_Rly']!='' else 0
				ioSum1[572] = int(ms['Future_HV_Rly']) if ms['Future_HV_Rly']!='' else 0
				ioSum1[574] = int(ms['Non_Red_HV_Rly']) if ms['Non_Red_HV_Rly']!='' else 0
				
			if ms['IO_Type'] in ['SCM: DO (32) 24VDC Bus External Power Supply (0-5000)']:
				ioSum1[317] += int(ms['Red_IS']) if ms['Red_IS']!='' else 0
				ioSum1[319] += int(ms['Future_Red_IS']) if ms['Future_Red_IS']!='' else 0
				ioSum1[321] += int(ms['Non_Red_IS']) if ms['Non_Red_IS']!='' else 0
				ioSum1[323] += int(ms['Red_NIS']) if ms['Red_NIS']!='' else 0
				ioSum1[325] += int(ms['Future_Red_NIS']) if ms['Future_Red_NIS']!='' else 0
				ioSum1[327] += int(ms['Non_Red_NIS']) if ms['Non_Red_NIS']!='' else 0
				ioSum1[329] += int(ms['Red_ISLTR']) if ms['Red_ISLTR']!='' else 0
				ioSum1[331] += int(ms['Future_Red_ISLTR']) if ms['Future_Red_ISLTR']!='' else 0
				ioSum1[333] += int(ms['Non_Red_ISLTR']) if ms['Non_Red_ISLTR']!='' else 0 
				ioSum1[335] += int(ms['Red_RLY']) if ms['Red_RLY']!='' else 0
				ioSum1[337] += int(ms['Future_Red_RLY']) if ms['Future_Red_RLY']!='' else 0
				ioSum1[339] += int(ms['Non_Red_RLY']) if ms['Non_Red_RLY']!='' else 0
				ioSum1[585] += int(ms['Red_HV_Rly']) if ms['Red_HV_Rly']!='' else 0
				ioSum1[587] += int(ms['Future_HV_Rly']) if ms['Future_HV_Rly']!='' else 0
				ioSum1[589] += int(ms['Non_Red_HV_Rly']) if ms['Non_Red_HV_Rly']!='' else 0
			if ms['IO_Type'] in ['SCM: DO (32) 24VDC Bus Internal Power Supply (0-5000)']:
				ioSum1[341] += int(ms['Red_IS']) if ms['Red_IS']!='' else 0
				ioSum1[343] += int(ms['Future_Red_IS']) if ms['Future_Red_IS']!='' else 0
				ioSum1[345] += int(ms['Non_Red_IS']) if ms['Non_Red_IS']!='' else 0
				ioSum1[347] += int(ms['Red_NIS']) if ms['Red_NIS']!='' else 0
				ioSum1[349] += int(ms['Future_Red_NIS']) if ms['Future_Red_NIS']!='' else 0
				ioSum1[351] += int(ms['Non_Red_NIS']) if ms['Non_Red_NIS']!='' else 0
				ioSum1[353] += int(ms['Red_ISLTR']) if ms['Red_ISLTR']!='' else 0
				ioSum1[355] += int(ms['Future_Red_ISLTR']) if ms['Future_Red_ISLTR']!='' else 0
				ioSum1[357] += int(ms['Non_Red_ISLTR']) if ms['Non_Red_ISLTR']!='' else 0 
				ioSum1[359] += int(ms['Red_RLY']) if ms['Red_RLY']!='' else 0
				ioSum1[361] += int(ms['Future_Red_RLY']) if ms['Future_Red_RLY']!='' else 0
				ioSum1[363] += int(ms['Non_Red_RLY']) if ms['Non_Red_RLY']!='' else 0
				ioSum1[591] += int(ms['Red_HV_RLY']) if ms['Red_HV_RLY']!='' else 0
				ioSum1[593] += int(ms['Future_HV_Rly']) if ms['Future_HV_Rly']!='' else 0
				ioSum1[595] += int(ms['Non_Red_HV_RLY']) if ms['Non_Red_HV_RLY']!='' else 0
	if ((io_Family =="seriesC" and universal=="No") or (io_Family =="TurboM")) and (Mounting_solution !='Mounting Panel' or Mounting_solution !=''):
		Giis=child.SelectedAttributes.GetContainerByName("C300_SerC_GIIS_CG_Cont")
		if Giis is not None:
			for giis in Giis.Rows:
				if giis['IO_Type'] in ['Series-C: GI/IS HLAI (16) Single Channel Isolator (0-5000)','Series-C: GI/IS HLAI (16) Dual Channel Isolator (0-5000)','Series-C: GI/IS HLAI (16) Temperature Isolator (0-5000)','Series-C: GI/IS HLAI (16) (0-5000)']:
					ioSum1[19] += int(giis['Red_IS']) if giis['Red_IS']!='' else 0
					ioSum1[20] += int(giis['Future_Red_IS']) if giis['Future_Red_IS']!='' else 0
					ioSum1[21] += int(giis['Non_Red_IS']) if giis['Non_Red_IS']!='' else 0
				if giis['IO_Type'] in ['Series-C: GI/IS HLAI (16) HART Single Channel Isolator (0-5000)','Series-C: GI/IS HLAI (16) HART Dual Channel Isolator (0-5000)','Series-C: GI/IS HLAI (16) HART Temperature Isolator (0-5000)','Series-C: GI/IS HLAI (16) HART (0-5000)']:
					ioSum1[40] += int(giis['Red_IS']) if giis['Red_IS']!='' else 0
					ioSum1[41] += int(giis['Future_Red_IS']) if giis['Future_Red_IS']!='' else 0
					ioSum1[42] += int(giis['Non_Red_IS']) if giis['Non_Red_IS']!='' else 0
				if giis['IO_Type'] in ['Series-C: GI/IS AO (16) HART Single Channel Isolator (0-5000)','Series-C: GI/IS AO (16) HART Dual Channel Isolator (0-5000)','Series-C: GI/IS AO (16) HART (0-5000)']:
					ioSum1[168] += int(giis['Red_IS']) if giis['Red_IS']!='' else 0
					ioSum1[169] += int(giis['Future_Red_IS']) if giis['Future_Red_IS']!='' else 0
					ioSum1[170] += int(giis['Non_Red_IS']) if giis['Non_Red_IS']!='' else 0
				if giis['IO_Type'] in ['Series-C: GI/IS DO (32) 24 VDC Bus with Expansion Board (0-5000)']:
					ioSum1[376] += int(giis['Non_Red_IS']) if giis['Non_Red_IS']!='' else 0
				if giis['IO_Type'] in ['Series-C: GI/IS DI (32) 24 VDC Relay (0-5000)','Series-C: GI/IS DI (32) 24 VDC Relay LFD (0-5000)','Series-C: GI/IS DI (32) 24VDC Solid State (0-5000)']:
					ioSum1[272] += int(giis['Red_IS']) if giis['Red_IS']!='' else 0
					ioSum1[273] += int(giis['Future_Red_IS']) if giis['Future_Red_IS']!='' else 0
					ioSum1[274] += int(giis['Non_Red_IS']) if giis['Non_Red_IS']!='' else 0
				if giis['IO_Type'] in ['Series-C: GI/IS DI (32) 24 VDC SOE Relay (0-5000)','Series-C: GI/IS DI (32) 24 VDC SOE Relay LFD (0-5000)','Series-C: GI/IS DI (32) 24VDC Relay with Expansion Board (0-5000)']:
					ioSum1[275] += int(giis['Non_Red_IS']) if giis['Non_Red_IS']!='' else 0
					ioSum1[277] += int(giis['Future_Red_IS']) if giis['Future_Red_IS']!='' else 0
					ioSum1[276] += int(giis['Red_IS']) if giis['Red_IS']!='' else 0
				if giis['IO_Type'] in ['Series-C: GI/IS DI (32) 24VDC SOE Solid State (0-5000)']:
					ioSum1[278] = int(giis['Non_Red_IS']) if giis['Non_Red_IS']!='' else 0
				if giis['IO_Type'] in ['Series-C: GI/IS DI (32) 24VDC SOE Relay with Expansion Board (0-5000)']:
					ioSum1[279] = int(giis['Non_Red_IS']) if giis['Non_Red_IS']!='' else 0
	if fmio=="Yes":
		fmio_cont= child.SelectedAttributes.GetContainerByName("SerC_CG_FIM_FF_IO_Cont").Rows
		for fmio_C in fmio_cont:
			if fmio_C['IO_Type'] in ['Number of FF AI devices (0-16000)']:
				ioSum1[413] += int(fmio_C['Red_wo_C300']) if fmio_C['Red_wo_C300']!='' else 0
				ioSum1[413] += int(fmio_C['Red_C300']) if fmio_C['Red_C300']!='' else 0
				ioSum1[414] += int(fmio_C['Future_Red_wo_C300']) if fmio_C['Future_Red_wo_C300']!='' else 0
				ioSum1[414] += int(fmio_C['Future_Red_C300']) if fmio_C['Future_Red_C300']!='' else 0
				ioSum1[415] += int(fmio_C['Non_Red_wo_C300']) if fmio_C['Non_Red_wo_C300']!='' else 0
				ioSum1[415] += int(fmio_C['Non_Red_C300']) if fmio_C['Non_Red_C300']!='' else 0
			if fmio_C['IO_Type'] in ['Number of FF AI Temperature devices (0-8000)']:
				ioSum1[416] += int(fmio_C['Red_wo_C300']) if fmio_C['Red_wo_C300']!='' else 0
				ioSum1[416] += int(fmio_C['Red_C300']) if fmio_C['Red_C300']!='' else 0
				ioSum1[417] += int(fmio_C['Future_Red_wo_C300']) if fmio_C['Future_Red_wo_C300']!='' else 0
				ioSum1[417] += int(fmio_C['Future_Red_C300']) if fmio_C['Future_Red_C300']!='' else 0
				ioSum1[418] += int(fmio_C['Non_Red_wo_C300']) if fmio_C['Non_Red_wo_C300']!='' else 0
				ioSum1[418] += int(fmio_C['Non_Red_C300']) if fmio_C['Non_Red_C300']!='' else 0
			if fmio_C['IO_Type'] in ['Number of FF AO devices (0-4000)']:
				ioSum1[419] += int(fmio_C['Red_wo_C300']) if fmio_C['Red_wo_C300']!='' else 0
				ioSum1[419] += int(fmio_C['Red_C300']) if fmio_C['Red_C300']!='' else 0
				ioSum1[420] += int(fmio_C['Future_Red_wo_C300']) if fmio_C['Future_Red_wo_C300']!='' else 0
				ioSum1[420] += int(fmio_C['Future_Red_C300']) if fmio_C['Future_Red_C300']!='' else 0
				ioSum1[421] += int(fmio_C['Non_Red_wo_C300']) if fmio_C['Non_Red_wo_C300']!='' else 0
				ioSum1[421] += int(fmio_C['Non_Red_C300']) if fmio_C['Non_Red_C300']!='' else 0
			if fmio_C['IO_Type'] in ['Number of MOVs (0-6000)']:
				ioSum1[422] += int(fmio_C['Red_wo_C300']) if fmio_C['Red_wo_C300']!='' else 0
				ioSum1[422] += int(fmio_C['Red_C300']) if fmio_C['Red_C300']!='' else 0
				ioSum1[423] += int(fmio_C['Future_Red_wo_C300']) if fmio_C['Future_Red_wo_C300']!='' else 0
				ioSum1[423] += int(fmio_C['Future_Red_C300']) if fmio_C['Future_Red_C300']!='' else 0
				ioSum1[424] += int(fmio_C['Non_Red_wo_C300']) if fmio_C['Non_Red_wo_C300']!='' else 0
				ioSum1[424] += int(fmio_C['Non_Red_C300']) if fmio_C['Non_Red_C300']!='' else 0
	if Profibus=="Yes":
		ioSum1[425] = int(Slave_devicesRed) if Slave_devicesRed !='' else 0
		ioSum1[426] = int(Slave_devicesNRed) if Slave_devicesNRed !='' else 0 
	if Ethernet=="Yes":
		ioSum1[427] = int(Red_ControlLogix) if Red_ControlLogix !='' else 0
		ioSum1[428] = int(NRed_ControlLogix) if NRed_ControlLogix !='' else 0 
		ioSum1[429] = int(Red_Process) if Red_Process !='' else 0
		ioSum1[430] = int(NRed_Process) if NRed_Process !='' else 0 
	if io_Family=="TurboM":
		cont= child.SelectedAttributes.GetContainerByName("C300_TurboM_IOM_CG_Cont").Rows
		for i in cont:
			if i['IO_Type'] in ['Number of Servo Position Modules (0-480)']:
				ioSum1[431] += int(i['Red_IOM']) if i['Red_IOM']!='' else 0
			if i['IO_Type'] in ['Number of Speed Protection Modules (0-480)']:
				ioSum1[432] += int(i['Red_IOM']) if i['Red_IOM']!='' else 0
	if pmio=="Yes":
		cont1=child.SelectedAttributes.GetContainerByName("C300_SerC_PointCount_PMIO_CG_Cont").Rows
		cont2=child.SelectedAttributes.GetContainerByName("C300_SerC_PointCount_PMIO_CG_RlyCont").Rows
		cont3=child.SelectedAttributes.GetContainerByName("C300_SerC_GIIS_PMIO_CG_Cont").Rows
		for pmio in cont1:
			if pmio['IO_Type'] in ['PMIO HLAI (16) (0-5000)']:
				ioSum1[433] = int(pmio['Red_IS']) if pmio['Red_IS']!='' else 0
				ioSum1[434] = int(pmio['Future_Red_IS']) if pmio['Future_Red_IS']!='' else 0
				ioSum1[435] = int(pmio['Non_Red_IS']) if pmio['Non_Red_IS']!='' else 0
				ioSum1[436] = int(pmio['Red_NIS']) if pmio['Red_NIS']!='' else 0
				ioSum1[437] = int(pmio['Future_Red_NIS']) if pmio['Future_Red_NIS']!='' else 0
				ioSum1[438] = int(pmio['Non_Red_NIS']) if pmio['Non_Red_NIS']!='' else 0
			if pmio['IO_Type'] in ['PMIO HLAI (16) w/ External HART Mux (0-5000)']:
				ioSum1[439] = int(pmio['Red_IS']) if pmio['Red_IS']!='' else 0
				ioSum1[440] = int(pmio['Future_Red_IS']) if pmio['Future_Red_IS']!='' else 0
				ioSum1[441] = int(pmio['Red_NIS']) if pmio['Red_NIS']!='' else 0
				ioSum1[442] = int(pmio['Future_Red_NIS']) if pmio['Future_Red_NIS']!='' else 0
			if pmio['IO_Type'] in ['PMIO HLAI Active HART (16) (0-5000)']:
				ioSum1[443] = int(pmio['Red_IS']) if pmio['Red_IS']!='' else 0
				ioSum1[444] = int(pmio['Future_Red_IS']) if pmio['Future_Red_IS']!='' else 0
				ioSum1[445] = int(pmio['Non_Red_IS']) if pmio['Non_Red_IS']!='' else 0
				ioSum1[446] = int(pmio['Red_NIS']) if pmio['Red_NIS']!='' else 0
				ioSum1[447] = int(pmio['Future_Red_NIS']) if pmio['Future_Red_NIS']!='' else 0
				ioSum1[448] = int(pmio['Non_Red_NIS']) if pmio['Non_Red_NIS']!='' else 0
			if pmio['IO_Type'] in ['PMIO HLAI Enhanced Power (16) (0-5000)']:
				ioSum1[449] = int(pmio['Red_IS']) if pmio['Red_IS']!='' else 0
				ioSum1[450] = int(pmio['Future_Red_IS']) if pmio['Future_Red_IS']!='' else 0
				ioSum1[451] = int(pmio['Red_NIS']) if pmio['Red_NIS']!='' else 0
				ioSum1[452] = int(pmio['Future_Red_NIS']) if pmio['Future_Red_NIS']!='' else 0
			if pmio['IO_Type'] in ['PMIO LLAI (8) (0-5000)']:
				ioSum1[453] = int(pmio['Non_Red_IS']) if pmio['Non_Red_IS']!='' else 0
				ioSum1[454] = int(pmio['Non_Red_NIS']) if pmio['Non_Red_NIS']!='' else 0
			if pmio['IO_Type'] in ['PMIO LLAI Mux PMIO Remote CJR (16) (0-5000)']:
				ioSum1[455] = int(pmio['Non_Red_IS']) if pmio['Non_Red_IS']!='' else 0
				ioSum1[456] = int(pmio['Non_Red_NIS']) if pmio['Non_Red_NIS']!='' else 0
			if pmio['IO_Type'] in ['PMIO LLAI Mux PMIO RTD (16) (0-5000)']:
				ioSum1[457] = int(pmio['Non_Red_IS']) if pmio['Non_Red_IS']!='' else 0
				ioSum1[458] = int(pmio['Non_Red_NIS']) if pmio['Non_Red_NIS']!='' else 0
			if pmio['IO_Type'] in ['PMIO LLAI Mux PMIO TC (16) (0-5000)']:
				ioSum1[459] = int(pmio['Non_Red_IS']) if pmio['Non_Red_IS']!='' else 0
				ioSum1[460] = int(pmio['Non_Red_NIS']) if pmio['Non_Red_NIS']!='' else 0
			if pmio['IO_Type'] in ['PMIO RHMUX (32)  w/NI Pwr Adptr (0-5000)']:
				ioSum1[461] = int(pmio['Non_Red_IS']) if pmio['Non_Red_IS']!='' else 0
				ioSum1[462] = int(pmio['Non_Red_NIS']) if pmio['Non_Red_NIS']!='' else 0
			if pmio['IO_Type'] in ['PMIO STI (16) (0-5000)']:
				ioSum1[463] = int(pmio['Red_IS']) if pmio['Red_IS']!='' else 0
				ioSum1[464] = int(pmio['Future_Red_IS']) if pmio['Future_Red_IS']!='' else 0
				ioSum1[465] = int(pmio['Non_Red_IS']) if pmio['Non_Red_IS']!='' else 0
				ioSum1[466] = int(pmio['Red_NIS']) if pmio['Red_NIS']!='' else 0
				ioSum1[467] = int(pmio['Future_Red_NIS']) if pmio['Future_Red_NIS']!='' else 0
				ioSum1[468] = int(pmio['Non_Red_NIS']) if pmio['Non_Red_NIS']!='' else 0
			if pmio['IO_Type'] in ['PMIO STI Enhanced Power (16) (0-5000)']:
				ioSum1[469] = int(pmio['Future_Red_IS']) if pmio['Future_Red_IS']!='' else 0
				ioSum1[470] = int(pmio['Future_Red_NIS']) if pmio['Future_Red_NIS']!='' else 0
			if pmio['IO_Type'] in ['PMIO AO HD (16) (0-5000)']:
				ioSum1[471] = int(pmio['Red_IS']) if pmio['Red_IS']!='' else 0
				ioSum1[472] = int(pmio['Future_Red_IS']) if pmio['Future_Red_IS']!='' else 0
				ioSum1[473] = int(pmio['Red_NIS']) if pmio['Red_NIS']!='' else 0
				ioSum1[474] = int(pmio['Future_Red_NIS']) if pmio['Future_Red_NIS']!='' else 0
			if pmio['IO_Type'] in ['PMIO AO HD w/ External HART Mux (16) (0-5000)']:
				ioSum1[475] = int(pmio['Red_IS']) if pmio['Red_IS']!='' else 0
				ioSum1[476] = int(pmio['Future_Red_IS']) if pmio['Future_Red_IS']!='' else 0
				ioSum1[477] = int(pmio['Red_NIS']) if pmio['Red_NIS']!='' else 0
				ioSum1[478] = int(pmio['Future_Red_NIS']) if pmio['Future_Red_NIS']!='' else 0
			if pmio['IO_Type'] in ['PMIO AO Active HART (0-5000)']:
				ioSum1[479] = int(pmio['Red_IS']) if pmio['Red_IS']!='' else 0
				ioSum1[480] = int(pmio['Future_Red_IS']) if pmio['Future_Red_IS']!='' else 0
				ioSum1[481] = int(pmio['Red_NIS']) if pmio['Red_NIS']!='' else 0
				ioSum1[482] = int(pmio['Future_Red_NIS']) if pmio['Future_Red_NIS']!='' else 0
		for pmio in cont2:
			if pmio['IO_Type'] in ['PMIO DI 24 VDC (32) (0-5000)']:
				ioSum1[483] = int(pmio['Non_Red_IS']) if pmio['Non_Red_IS']!='' else 0
				ioSum1[484] = int(pmio['Non_Red_NIS']) if pmio['Non_Red_NIS']!='' else 0
			if pmio['IO_Type'] in ['PMIO DI 24 HD VDC (32) (0-5000)']:
				ioSum1[485] = int(pmio['Red_IS']) if pmio['Red_IS']!='' else 0
				ioSum1[486] = int(pmio['Future_Red_IS']) if pmio['Future_Red_IS']!='' else 0
				ioSum1[487] = int(pmio['Red_NIS']) if pmio['Red_NIS']!='' else 0
				ioSum1[488] = int(pmio['Future_Red_NIS']) if pmio['Future_Red_NIS']!='' else 0
			if pmio['IO_Type'] in ['PMIO DI SOE 24 VDC (32) (0-5000)']:
				ioSum1[489] = int(pmio['Red_IS']) if pmio['Red_IS']!='' else 0
				ioSum1[490] = int(pmio['Non_Red_IS']) if pmio['Non_Red_IS']!='' else 0
				ioSum1[491] = int(pmio['Red_NIS']) if pmio['Red_NIS']!='' else 0
				ioSum1[492] = int(pmio['Non_Red_NIS']) if pmio['Non_Red_NIS']!='' else 0
			if pmio['IO_Type'] in ['PMIO DI 120 VAC (32) (0-5000)']:
				ioSum1[493] = int(pmio['Non_Red_IS']) if pmio['Non_Red_IS']!='' else 0
				ioSum1[494] = int(pmio['Non_Red_NIS']) if pmio['Non_Red_NIS']!='' else 0
			if pmio['IO_Type'] in ['PMIO DI SOE 120 VAC (32) (0-5000)']:
				ioSum1[495] = int(pmio['Red_IS']) if pmio['Red_IS']!='' else 0
				ioSum1[496] = int(pmio['Non_Red_IS']) if pmio['Non_Red_IS']!='' else 0
				ioSum1[497] = int(pmio['Red_NIS']) if pmio['Red_NIS']!='' else 0
				ioSum1[498] = int(pmio['Non_Red_NIS']) if pmio['Non_Red_NIS']!='' else 0
			if pmio['IO_Type'] in ['PMIO DI 240 VAC (32) (0-5000)']:
				ioSum1[499] = int(pmio['Non_Red_IS']) if pmio['Non_Red_IS']!='' else 0
				ioSum1[500] = int(pmio['Non_Red_NIS']) if pmio['Non_Red_NIS']!='' else 0
			if pmio['IO_Type'] in ['PMIO DI SOE 240 VAC (32) (0-5000)']:
				ioSum1[501] = int(pmio['Red_IS']) if pmio['Red_IS']!='' else 0
				ioSum1[502] = int(pmio['Non_Red_IS']) if pmio['Non_Red_IS']!='' else 0
				ioSum1[503] = int(pmio['Red_NIS']) if pmio['Red_NIS']!='' else 0
				ioSum1[504] = int(pmio['Non_Red_NIS']) if pmio['Non_Red_NIS']!='' else 0
			if pmio['IO_Type'] in ['PMIO DO 24 VDC (16) (0-5000)']:
				ioSum1[505] = int(pmio['Non_Red_IS']) if pmio['Non_Red_IS']!='' else 0
				ioSum1[506] = int(pmio['Non_Red_NIS']) if pmio['Non_Red_NIS']!='' else 0
			if pmio['IO_Type'] in ['PMIO DO 24 VDC HD (32) (0-5000)']:
				ioSum1[507] = int(pmio['Red_IS']) if pmio['Red_IS']!='' else 0
				ioSum1[508] = int(pmio['Future_Red_IS']) if pmio['Future_Red_IS']!='' else 0
				ioSum1[509] = int(pmio['Red_NIS']) if pmio['Red_NIS']!='' else 0
				ioSum1[510] = int(pmio['Future_Red_NIS']) if pmio['Future_Red_NIS']!='' else 0
			if pmio['IO_Type'] in ['PMIO DO 3 to 30 VDC (16) (0-5000)']:
				ioSum1[511] = int(pmio['Non_Red_IS']) if pmio['Non_Red_IS']!='' else 0
				ioSum1[512] = int(pmio['Non_Red_NIS']) if pmio['Non_Red_NIS']!='' else 0
			if pmio['IO_Type'] in ['PMIO DO 31 to 200 VDC (16) (0-5000)']:
				ioSum1[513] = int(pmio['Non_Red_IS']) if pmio['Non_Red_IS']!='' else 0
				ioSum1[514] = int(pmio['Non_Red_NIS']) if pmio['Non_Red_NIS']!='' else 0
			if pmio['IO_Type'] in ['PMIO DO 120/240 VAC SS (16) (0-5000)']:
				ioSum1[515] = int(pmio['Non_Red_IS']) if pmio['Non_Red_IS']!='' else 0
				ioSum1[516] = int(pmio['Non_Red_NIS']) if pmio['Non_Red_NIS']!='' else 0
			if pmio['IO_Type'] in ['PMIO DO HD Relay (32) (0-5000)']:
				ioSum1[517] = int(pmio['Red_IS']) if pmio['Red_IS']!='' else 0
				ioSum1[518] = int(pmio['Future_Red_IS']) if pmio['Future_Red_IS']!='' else 0
				ioSum1[519] = int(pmio['Red_NIS']) if pmio['Red_NIS']!='' else 0
				ioSum1[520] = int(pmio['Future_Red_NIS']) if pmio['Future_Red_NIS']!='' else 0
			if pmio['IO_Type'] in ['PMIO DO 120 VAC Relay (16) (0-5000)']:
				ioSum1[521] = int(pmio['Non_Red_IS']) if pmio['Non_Red_IS']!='' else 0
				ioSum1[522] = int(pmio['Non_Red_NIS']) if pmio['Non_Red_NIS']!='' else 0
			if pmio['IO_Type'] in ['PMIO DO 240 VAC Relay (16) (0-5000)']:
				ioSum1[523] = int(pmio['Non_Red_IS']) if pmio['Non_Red_IS']!='' else 0
				ioSum1[524] = int(pmio['Non_Red_NIS']) if pmio['Non_Red_NIS']!='' else 0
		for pmio in cont3:
			if pmio['IO_Type'] in ['PMIO GI/IS AO (16) External HART  (0-5000)']:
				ioSum1[525] = int(pmio['Red_IS']) if pmio['Red_IS']!='' else 0
				ioSum1[526] = int(pmio['Future_Red_IS']) if pmio['Future_Red_IS']!='' else 0
			if pmio['IO_Type'] in ['PMIO GI/IS AO (16) Active HART  (0-5000)']:
				ioSum1[527] = int(pmio['Red_IS']) if pmio['Red_IS']!='' else 0
				ioSum1[528] = int(pmio['Future_Red_IS']) if pmio['Future_Red_IS']!='' else 0
			if pmio['IO_Type'] in ['PMIO GI/IS DI (32)  (0-5000)']:
				ioSum1[529] = int(pmio['Non_Red_IS']) if pmio['Non_Red_IS']!='' else 0
			if pmio['IO_Type'] in ['PMIO GI/IS DI SOE (32)  (0-5000)']:
				ioSum1[530] = int(pmio['Red_IS']) if pmio['Red_IS']!='' else 0
				ioSum1[531] = int(pmio['Non_Red_IS']) if pmio['Non_Red_IS']!='' else 0
			if pmio['IO_Type'] in ['PMIO GI/IS DI Solid State SOE (32)  (0-5000)']:
				ioSum1[532] = int(pmio['Red_IS']) if pmio['Red_IS']!='' else 0
				ioSum1[533] = int(pmio['Non_Red_IS']) if pmio['Non_Red_IS']!='' else 0
			if pmio['IO_Type'] in ['PMIO GI/IS DI Solid State (32)  (0-5000)']:
				ioSum1[534] = int(pmio['Non_Red_IS']) if pmio['Non_Red_IS']!='' else 0
			if pmio['IO_Type'] in ['PMIO GI/IS DO LFD (16)  (0-5000)']:
				ioSum1[535] = int(pmio['Non_Red_IS']) if pmio['Non_Red_IS']!='' else 0
			if pmio['IO_Type'] in ['PMIO GI/IS DO (16)  (0-5000)']:
				ioSum1[536] = int(pmio['Non_Red_IS']) if pmio['Non_Red_IS']!='' else 0
			if pmio['IO_Type'] in ['PMIO GI/IS DO (32) Via non red combine panel  (0-5000)']:
				ioSum1[537] = int(pmio['Non_Red_IS']) if pmio['Non_Red_IS']!='' else 0
			if pmio['IO_Type'] in ['PMIO GI/IS HLAI Aux PMIO Cur (16)  (0-5000)']:
				ioSum1[538] = int(pmio['Red_IS']) if pmio['Red_IS']!='' else 0
				ioSum1[539] = int(pmio['Non_Red_IS']) if pmio['Non_Red_IS']!='' else 0
			if pmio['IO_Type'] in ['PMIO GI/IS HLAI Aux PMIO Cur External HART (16)  (0-5000)']:
				ioSum1[540] = int(pmio['Red_IS']) if pmio['Red_IS']!='' else 0
				ioSum1[541] = int(pmio['Non_Red_IS']) if pmio['Non_Red_IS']!='' else 0
			if pmio['IO_Type'] in ['PMIO GI/IS HLAI Aux & Hi V (16)  (0-5000)']:
				ioSum1[542] = int(pmio['Red_IS']) if pmio['Red_IS']!='' else 0
				ioSum1[543] = int(pmio['Non_Red_IS']) if pmio['Non_Red_IS']!='' else 0
			if pmio['IO_Type'] in ['PMIO GI/IS HLAI Active HART Aux Current (16)  (0-5000)']:
				ioSum1[544] = int(pmio['Red_IS']) if pmio['Red_IS']!='' else 0
				ioSum1[545] = int(pmio['Non_Red_IS']) if pmio['Non_Red_IS']!='' else 0
			if pmio['IO_Type'] in ['PMIO GI/IS HLAI Active HART Aux & Hi V (16)  (0-5000)']:
				ioSum1[546] = int(pmio['Red_IS']) if pmio['Red_IS']!='' else 0
				ioSum1[547] = int(pmio['Non_Red_IS']) if pmio['Non_Red_IS']!='' else 0
			if pmio['IO_Type'] in ['PMIO GI/IS STI Aux PMIO Current (16)  (0-5000)']:
				ioSum1[548] = int(pmio['Red_IS']) if pmio['Red_IS']!='' else 0
				ioSum1[549] = int(pmio['Non_Red_IS']) if pmio['Non_Red_IS']!='' else 0
			if pmio['IO_Type'] in ['PMIO GI/IS STI Aux PMIO Current External HART (16)  (0-5000)']:
				ioSum1[550] = int(pmio['Red_IS']) if pmio['Red_IS']!='' else 0
				ioSum1[551] = int(pmio['Future_Red_IS']) if pmio['Future_Red_IS']!='' else 0
			if pmio['IO_Type'] in ['PMIO GI/IS STI Aux & Hi V (16)  (0-5000)']:
				ioSum1[552] = int(pmio['Red_IS']) if pmio['Red_IS']!='' else 0
				ioSum1[553] = int(pmio['Non_Red_IS']) if pmio['Non_Red_IS']!='' else 0
	return ioSum1