import GS_C300_IO_Calc,  GS_C300_IO_Calc2, GS_SerC_Turbo_IO_Calc
IO_Family_Type = Product.Attr('SerC_CG_IO_Family_Type').GetValue()
percentInstalledSpare = Product.Attr('SerC_RG_Percent_Installed_Spare(0-100%)').GetValue()
IO_Mounting_Solution = Product.Attr('SerC_IO_Mounting_Solution').GetValue()
Universal_Marshalling_Cabinet = Product.Attr('Ser_RG_Universal_Marshalling_Cabinet').GetValue()
contName1 = 'SerC_RG_Enhanced_Function_IO_Cont'
contName2 = ''
contName3 = ''
parts_dict = dict()
if IO_Mounting_Solution == 'Cabinet' and Universal_Marshalling_Cabinet == 'No':
    contName2 = 'C300_SerC_GIIS_RG_Cont'
if IO_Family_Type == 'Series C':
    contName3 = 'SerC_RG_Enhanced_Function_IO_Cont2'
    GS_C300_IO_Calc.applyPercentage(Product, percentInstalledSpare, IO_Family_Type, IO_Mounting_Solution, Universal_Marshalling_Cabinet, contName1, contName2, contName3)
    parts_dict = GS_C300_IO_Calc.getParts40833(Product, {})
    parts_dict = GS_C300_IO_Calc.getParts40859(Product, parts_dict)
    parts_dict = GS_C300_IO_Calc.getParts40872(Product, parts_dict)
    parts_dict = GS_C300_IO_Calc.getParts40887(Product, parts_dict)
    parts_dict = GS_C300_IO_Calc.getParts41229(Product, parts_dict)
    parts_dict = GS_C300_IO_Calc.getParts40972(Product, parts_dict)
    parts_dict = GS_C300_IO_Calc.getParts41449(Product, parts_dict)
elif IO_Family_Type == 'Series-C Mark II':
    #CXCPQ-44474
    contName1 = 'C300_SerC_Enhanced_Function_IO_Mark_Group_RG_Cont1'
    GS_C300_IO_Calc.applyPercentage(Product, percentInstalledSpare, IO_Family_Type, IO_Mounting_Solution, Universal_Marshalling_Cabinet, contName1, '', '')
    parts_dict = GS_C300_IO_Calc.getParts44474(Product, parts_dict)
    #parts_dict = GS_C300_IO_Calc2.getParts44488(Product, parts_dict)
    parts_dict = GS_C300_IO_Calc2.getParts44490(Product, parts_dict)
elif IO_Family_Type == 'Turbomachinery':
    #modules = ['49225', '49227', '49229', '49231', '49233', '50461', '50463']
    modules = ['49225', '49225_1', '49227', '49229', '49229_1', '49231', '50461', '49233', '50463', '49228']
    #Module and container mapping
    contList = {'49225': 'SerC_RG_Enhanced_Function_IO_Cont2', '49225_1': 'C300_SerC_GIIS_RG_Cont', '49227': 'C300_TurboM_IOM_RG_Cont', '49229':'SerC_RG_Enhanced_Function_IO_Cont' , '49229_1':'C300_SerC_GIIS_RG_Cont'}
    contList['49231'] = 'SerC_RG_Enhanced_Function_IO_Cont'
    contList['50461'] = 'SerC_RG_Enhanced_Function_IO_Cont2'
    contList['49233'] = 'SerC_RG_Enhanced_Function_IO_Cont'
    contList['49233_1'] = 'C300_SerC_GIIS_RG_Cont'
    contList['50463'] = 'SerC_RG_Enhanced_Function_IO_Cont2'
    contList['50463_1'] = 'C300_SerC_GIIS_RG_Cont'
    contList['49228'] = 'C300_RG_Universal_IO_cont_1'
    contList['49228_1'] = 'C300_RG_Universal_IO_cont_2'
    #Module and IO questions mapping
    #CXCPQ-49225
    iOType = {'49225':['Series-C: DI (32) 24 VDC with Open Wire Detect (0-5000)', 'Series-C: DI (32) 24VDC SOE (0-5000)'], '49227': ['Number of Servo Position Modules (0-480)', 'Number of Speed Protection Modules (0-480)']}
    ioTypes = ['Series-C: GI/IS DI (32) 24VDC Solid State (0-5000)', 'Series-C: GI/IS DI (32) 24 VDC Relay (0-5000)']
    ioTypes.extend(['Series-C: GI/IS DI (32) 24 VDC Relay LFD (0-5000)', 'Series-C: GI/IS DI (32) 24VDC Relay with Expansion Board (0-5000)'])
    ioTypes.extend(['Series-C: GI/IS DI (32) 24VDC SOE Solid State (0-5000)', 'Series-C: GI/IS DI (32) 24 VDC SOE Relay (0-5000)'])
    ioTypes.extend(['Series-C: GI/IS DI (32) 24 VDC SOE Relay LFD (0-5000)', 'Series-C: GI/IS DI (32) 24VDC SOE Relay with Expansion Board (0-5000)'])
    iOType['49225_1'] = ioTypes
    #CXCPQ-49229
    iOType['49229'] = ['Series-C: HLAI (16) with HART with differential inputs (0-5000)', 'Series-C: HLAI (16) without HART with differential inputs (0-5000)']
    ioTypes49229_1 = ['Series-C: GI/IS HLAI (16) HART (0-5000)', 'Series-C: GI/IS HLAI (16) HART Single Channel Isolator (0-5000)']
    ioTypes49229_1.extend(['Series-C: GI/IS HLAI (16) HART Dual Channel Isolator (0-5000)', 'Series-C: GI/IS HLAI (16) HART Temperature Isolator (0-5000)'])
    ioTypes49229_1.extend(['Series-C: GI/IS HLAI (16) (0-5000)', 'Series-C: GI/IS HLAI (16) Single Channel Isolator (0-5000)'])
    ioTypes49229_1.extend(['Series-C: GI/IS HLAI (16) Dual Channel Isolator (0-5000)', 'Series-C: GI/IS HLAI (16) Temperature Isolator (0-5000)'])
    iOType['49229_1'] = ioTypes49229_1
    #CXCPQ-49231
    iOType['49231'] = ['Series-C: LLAI (1) Mux RTD (0-5000)', 'Series-C: LLAI (1) Mux TC (0-5000)', 'Series-C: LLAI (1) Mux TC Remote CJR (0-5000)']
    #CXCPQ-50461
    iOType['50461'] = ['Series-C: DI (32) 110 VAC (0-5000)', 'Series-C: DI (32) 110 VAC PROX (0-5000)', 'Series-C: DI (32) 220 VAC (0-5000)']
    #CXCPQ-49233
    iOType['49233'] = ['Series-C: AO (16) HART (0-5000)']
    iOType['49233_1'] = ['Series-C: GI/IS AO (16) HART (0-5000)', 'Series-C: GI/IS AO (16) HART Single Channel Isolator (0-5000)', 'Series-C: GI/IS AO (16) HART Dual Channel Isolator (0-5000)']
    #CXCPQ-50463
    ioTypes50463 = ['Series-C: DO (32) 24VDC Bus External Power Supply (0-5000)', 'Series-C: DO (32) 24VDC Bus Internal Power Supply (0-5000)']
    ioTypes50463.extend(['Series-C: DO (32) 24VDC Relay Bus above 30V (0-5000)', 'Series-C: DO (32) 24VDC Relay Bus up to 30V (0-5000)'])
    iOType['50463'] = ioTypes50463
    iOType['50463_1'] = ['Series-C: GI/IS DO (32) 24 VDC Bus with Expansion Board (0-5000)']
    #CXCPQ-49228
    ioTypes49228 = ['Series-C: UIO (32) Analog Input (HLAI Adapt) (0-5000)', 'Series-C: UIO (32) Analog Input (LLAI Adapt) (0-5000)', 'Series-C: UIO (32) Analog Output (0-5000)']
    iOType['49228'] = ioTypes49228
    iOType['49228_1'] = ['Series-C: UIO (32) Digital Input (0-5000)', 'Series-C: UIO (32) Digital Output (0-5000)']
    #Module and container columns mapping
    column = {'49225':['Red_IS', 'Future_Red_IS', 'Non_Red_IS', 'Red_NIS', 'Future_Red_NIS', 'Non_Red_NIS', 'Red_ISLTR', 'Future_Red_ISLTR',  'Non_Red_ISLTR',  'Red_RLY',  'Future_Red_RLY',  'Non_Red_RLY'], '49225_1': ['Red_IS', 'Future_Red_IS', 'Non_Red_IS'], '49227': ['Red_IOM']}
    column['49229'] = ['Red_IS', 'Future_Red_IS', 'Non_Red_IS', 'Red_NIS', 'Future_Red_NIS', 'Non_Red_NIS', 'Red_ISLTR', 'Future_Red_ISLTR',  'Non_Red_ISLTR']
    column['49229_1'] = ['Red_IS', 'Future_Red_IS', 'Non_Red_IS']
    column['49231'] = ['Non_Red_IS', 'Non_Red_NIS', 'Non_Red_ISLTR']
    column['50461'] = ['Red_NIS', 'Future_Red_NIS', 'Non_Red_NIS']
    column['49233'] = ['Red_IS', 'Future_Red_IS', 'Non_Red_IS', 'Red_NIS', 'Future_Red_NIS', 'Non_Red_NIS', 'Red_ISLTR', 'Future_Red_ISLTR',  'Non_Red_ISLTR']
    column['49233_1'] = ['Red_IS', 'Future_Red_IS', 'Non_Red_IS']
    column['50463'] = ['Red_IS', 'Future_Red_IS', 'Non_Red_IS', 'Red_NIS', 'Future_Red_NIS', 'Non_Red_NIS', 'Red_ISLTR', 'Future_Red_ISLTR',  'Non_Red_ISLTR',  'Red_RLY',  'Future_Red_RLY',  'Non_Red_RLY']
    column['50463_1'] = ['Red_IS', 'Future_Red_IS', 'Non_Red_IS']
    column['49228'] = ['Red_IS', 'Future_Red_IS', 'Non_Red_IS', 'Red_NIS', 'Future_Red_NIS', 'Non_Red_NIS', 'Red_ISLTR', 'Future_Red_ISLTR',  'Non_Red_ISLTR']
    column['49228_1'] = ['Red_IS', 'Future_Red_IS', 'Non_Red_IS', 'Red_NIS', 'Future_Red_NIS', 'Non_Red_NIS', 'Red_ISLTR', 'Future_Red_ISLTR',  'Non_Red_ISLTR',  'Red_RLY',  'Future_Red_RLY',  'Non_Red_RLY']
    #IO Calculation
    GS_SerC_Turbo_IO_Calc.applyPercentageOnTurboIOs(Product, percentInstalledSpare, modules, contList, iOType, column)
    #Get parts and quantity
    parts_dict = GS_SerC_Turbo_IO_Calc.getParts49225(Product, parts_dict)
    parts_dict = GS_SerC_Turbo_IO_Calc.getParts49227(Product, parts_dict)
    parts_dict = GS_SerC_Turbo_IO_Calc.getParts49229(Product, parts_dict)
    #As parameter of the userstory CXCPQ-49230 depends on CXCPQ-49229
    parts_dict = GS_SerC_Turbo_IO_Calc.getParts49230(Product, parts_dict)
    parts_dict = GS_SerC_Turbo_IO_Calc.getParts49231(Product, parts_dict)
    #As parameter of the userstory CXCPQ-49232 depends on CXCPQ-49231
    parts_dict = GS_SerC_Turbo_IO_Calc.getParts49232(Product, parts_dict)
    parts_dict = GS_SerC_Turbo_IO_Calc.getParts50461(Product, parts_dict)
    parts_dict = GS_SerC_Turbo_IO_Calc.getParts49233(Product, parts_dict)
    parts_dict = GS_SerC_Turbo_IO_Calc.getParts50463(Product, parts_dict)
    parts_dict = GS_SerC_Turbo_IO_Calc.getParts49228(Product, parts_dict)

if len(parts_dict) > 0:
    GS_C300_IO_Calc.setIOCount(Product, 'Series_C_RG_Part_Summary', parts_dict)
    ScriptExecutor.Execute('PS_Series_C_RG_Part_Summary_Cont_update_parts')
    Product.GetContainerByName('Series_C_RG_Part_Summary_Cont').Calculate()