isR2Qquote = True if Quote.GetCustomField("R2QFlag").Content else False
containers = [
    'C300_SerC_GIIS_CG_Cont', 
    'C300_CG_Universal_IO_cont_1', 
    'C300_CG_Universal_IO_cont_2', 
    'SerC_CG_Enhanced_Function_IO_Cont', 
    'SerC_CG_Enhanced_Function_IO_Cont2'
]
for container in containers:
    if not isR2Qquote:
        Product.GetContainerByName(container).Rows.Clear()

if not isR2Qquote:
# Reset specified attributes
    attributes_to_reset = [
        'SerC_GC_Profibus_Gateway_Interface', 
        'SerC_CG_Ethernet_Interface', 
        'SerC_IO_Params', 
        'Series_C_CG_Part_Summary', 
        'Series_C_CG_Part_Summary_Cont'
    ]
    for attr in attributes_to_reset:
        Product.ResetAttr(attr)

# Import necessary modules
import GS_C300_IO_Calc, GS_C300_IO_Calc2, GS_Get_Set_AtvQty, GS_SerC_Turbo_IO_Calc

# Log values for 'SerC_CG_IO_Family_Type' and 'MIB Configuration Required?'
#for attr_name in ["SerC_CG_IO_Family_Type", "MIB Configuration Required?"]:
#    for value in Product.Attributes.GetByName(attr_name).Values:
#        Log.Info("{} : {}".format(value.Display, value.IsSelected))

ioFamilyType = Product.Attr('SerC_CG_IO_Family_Type').GetValue()
parts_dict = dict()
if ioFamilyType != 'Series C':
    #CXCPQ-40833, CXCPQ-40859, CXCPQ-40887,CXCPQ-40972 , CXCPQ-41229
    paramDict = {'D21':0, 'E21':0, 'F21':0, 'D22':0, 'E22':0, 'F22':0, 'D23':0, 'E23':0, 'F23':0, 'D31':0, 'E31':0, 'F31':0, 'D32':0, 'E32':0, 'F32':0, 'D33':0, 'E33':0, 'F33':0,'L21':0,'J31':0,'K31':0,'J41':0,'K41':0,'J51':0,'K51':0,'L61':0,'J71':0,'K71':0,'J81':0,'K81':0,'J91':0,'K91':0,'F41': 0, 'F42': 0, 'F43': 0, 'F51': 0, 'F52': 0, 'F53': 0, 'F61': 0, 'F62': 0, 'F63': 0, 'O11':0, 'M21':0, 'N21':0, 'M31':0, 'N31':0, 'Y71':0, 'Y72':0, 'Y73':0, 'W73':0, 'W81':0, 'W82':0, 'W91':0, 'W92':0, 'D81':0, 'E81':0, 'F81':0, 'D82':0, 'E82':0, 'F82':0, 'D83':0, 'E83':0, 'F83':0, 'D84':0, 'E84':0, 'F84':0, 'D91':0, 'E91':0, 'F91':0, 'D92':0, 'E92':0, 'F92':0, 'D93':0, 'E93':0, 'F93':0, 'D94':0, 'E94':0, 'F94':0, 'O41':0, 'M51':0, 'N51':0, 'M61':0, 'N61':0, 'O71':0, 'O81':0, 'M91':0, 'N91':0, 'P11':0, 'Q11':0, 'R21':0,'G41':0, 'H41':0, 'I41':0, 'G42':0, 'H42':0, 'I42':0, 'G43':0, 'H43':0, 'I43':0, 'G44':0, 'H44':0, 'I44':0, 'G51':0, 'H51':0, 'I51':0, 'G52':0, 'H52':0, 'I52':0, 'G53':0, 'H53':0, 'I53':0, 'G54':0, 'H54':0, 'I54':0, 'G64':0, 'H64':0, 'I64':0, 'G74':0, 'H74':0, 'I74':0, 'P31':0, 'Q31':0, 'G12':0,'H12':0,'I12':0,'I22':0,'G32':0,'H32':0,'I32':0,'Z11':0,'Z12':0,'Z13':0,'Z23':0,'Z31':0,'Z32':0,'Z33':0,'G81':0,'G82':0,'G83':0,'G91':0,'G92':0,'G93':0,'H81':0,'H82':0,'H83':0,'H91':0,'H92':0,'H93':0,'J11':0,'J12':0,'J13':0,'K11':0,'K12':0,'K13':0, 'Y21':0, 'Y22':0, 'Y23':0, 'Y31':0, 'Y32':0, 'Y33':0,'Z91':0,'W11':0, 'W12':0,'W21':0, 'W22':0,'W31':0, 'W32':0,'W41':0, 'W42':0,'W51':0, 'W52':0,'W61':0, 'W62':0}
    parts_dict = {'CC-PAIH02':0, 'CC-PAIX02':0, 'CC-PAIM01':0, 'CC-TAIM01':0, 'CC-PAOH01':0, 'CC-TAOX11':0, 'CC-TAOX01':0, 'CC-PDIL01':0, 'CC-PDIS01':0, 'CC-TDIL11':0, 'CC-TDIL01':0, 'CC-PDOB01':0, 'CC-TDOB11':0, 'CC-TDOB01':0, 'CC-TDOR11':0, 'CC-TDOR01':0, 'CC-GDOL11':0, 'CC-PDIH01':0,'CC-TDI120':0,'CC-TDI230':0,'CC-TDI110':0,'CC-TDI151':0,'CC-TDI220':0,'CC-PPIX01':0,'CC-TPIX11':0, 'CC-TAID11':0,'CC-TAID01':0,'CC-GAIX11':0,'CC-GAIX21':0}
    #GS_C300_IO_Calc.setIOCount(Product, 'SerC_IO_Params', paramDict)
    GS_C300_IO_Calc.setIOCount(Product, 'Series_C_CG_Part_Summary', parts_dict)
if ioFamilyType != 'Series-C Mark II':
    #CXCPQ-44474, CXCPQ-44488
    Product.DisallowAttr('SerC_CG_IOTA_Carrier_Cover')
    paramDict = {'I12':0, 'I32':0, 'G41':0, 'H41':0, 'I41':0, 'G42':0, 'H42':0, 'I42':0, 'G43':0, 'H43':0, 'I43':0, 'G44':0, 'H44':0, 'I44':0,'G51':0, 'H51':0, 'I51':0, 'G52':0, 'H52':0, 'I52':0, 'G53':0, 'H53':0, 'I53':0, 'G54':0, 'H54':0, 'I54':0, 'G64':0, 'H64':0, 'I64':0, 'G74':0, 'H74':0, 'I74':0, 'Z41':0, 'Z42':0, 'Z43':0, 'Z51':0, 'Z52':0, 'Z53':0, 'Z61':0, 'Z62':0, 'Z63':0, 'Z71':0, 'Z72':0, 'Z73':0, 'G81':0, 'H81':0, 'G82':0, 'H82':0, 'G83':0, 'H83':0, 'G91':0, 'H91':0, 'G92':0, 'H92':0, 'G93':0, 'H93':0, 'J11':0, 'K11':0, 'J12':0, 'K12':0, 'J13':0, 'K13':0, 'Z81':0, 'Z82':0, 'Z83':0, 'Z84':0, 'Z85':0, 'Z86':0}
    parts_dict = {'CC-PDIH01':0, 'CC-TDI110':0, 'CC-TDI220':0, 'CC-PDOB01':0, 'DC-TDOB11':0, 'DC-TDOB01':0, 'CC-SDOR01': 0, 'CC-KREBR5':0, 'CC-KREB01':0, 'CC-KREB02':0, 'CC-KREB05':0, 'CC-KREB10':0, 'CC-PPIX01':0, 'DC-TPIX11':0}
    ##GS_C300_IO_Calc.setIOCount(Product, 'SerC_IO_Params', paramDict)
    GS_C300_IO_Calc.setIOCount(Product, 'Series_C_CG_Part_Summary', parts_dict)
if ioFamilyType != 'Turbomachinery':
    #CXCPQ-49227           
    paramDict = {'A11':0, 'A21':0}
    parts_dict = {'CC-PSV201':0, 'CC-PSP401':0, 'CC-TSV211':0, 'CC-TSP411':0}
    GS_C300_IO_Calc.setIOCount(Product, 'SerC_IO_Params', paramDict)
    GS_C300_IO_Calc.setIOCount(Product, 'Series_C_CG_Part_Summary', parts_dict)

percentInstalledSpare = Product.Attr('SerC_CG_Percent_Installed_Spare').GetValue()
if ioFamilyType == 'Series C':
    Product.AllowAttr('SerC_CG_IOTA_Carrier_Cover')
    Product.AllowAttr('SerC_CG_Integrated_Marshalling_Cabinet')
    Product.DisallowAttr('SerC_CG_Cabinet_Type_03')
    if Product.Attr('SerC_CG_IOTA_Carrier_Cover').GetValue() == '':
        Product.Attr('SerC_CG_IOTA_Carrier_Cover').SelectDisplayValue('No')
    parts_dict = dict()
    IO_Mounting_Solution = Product.Attr('SerC_CG_IO_Mounting_Solution').GetValue()
    Universal_Marshalling_Cabinet = Product.Attr('SerC_CG_Universal_Marshalling_Cabinet').GetValue()
    contName1 = 'SerC_CG_Enhanced_Function_IO_Cont'
    contName2 = ''
    contName3 = 'SerC_CG_Enhanced_Function_IO_Cont2'
    if IO_Mounting_Solution != 'Mounting Panel' and Universal_Marshalling_Cabinet == 'No':
        contName2 = 'C300_SerC_GIIS_CG_Cont'
    GS_C300_IO_Calc.applyPercentage(Product, percentInstalledSpare, ioFamilyType, IO_Mounting_Solution, Universal_Marshalling_Cabinet, contName1, contName2, contName3)
    parts_dict = GS_C300_IO_Calc.getParts40833(Product, parts_dict)
    parts_dict = GS_C300_IO_Calc.getParts40859(Product, parts_dict)
    parts_dict = GS_C300_IO_Calc.getParts40872(Product, parts_dict)
    parts_dict = GS_C300_IO_Calc.getParts40887(Product, parts_dict)
    parts_dict = GS_C300_IO_Calc.getParts41229(Product, parts_dict)
    parts_dict = GS_C300_IO_Calc.getParts40972(Product, parts_dict)
    parts_dict = GS_C300_IO_Calc.getParts41449(Product, parts_dict)
elif ioFamilyType == 'Turbomachinery':
    Disallow_attrs = [
    "ATTCON_01_close",
    "ATTCON_01_open",
    "Header_01_close",
    "Header_01_open",
    "SerC_Cabinet_Power",
    "SerC_CG_AC_Input_Voltage",
    "SerC_CG_Cabinet_Fan",
    "SerC_CG_Cabinet_Light_(LED)",
    "SerC_CG_Cabinet_Thermostat",
    "SerC_CG_Cabinet_Type",
    "SerC_CG_label_Universal_Marshalling_Cabinet",
    "SerC_CG_Mounting_Option",
    "SerC_CG_Percentage_of_Spare_Space_required(0-100%)",
    "SerC_CG_Power_Supply_Vendor",
    "SerC_CG_SIC_Length_for_UMC",
    "SerC_CG_Termination_of_Spare_Wires_in_Field_Cabin",
    "SerC_CG_Universal_Marshaling_Cabinet_layout",
    "SerC_CG_Utility_Socket_(230/115 VAC)",
    "SerC_CG_Wiring_and_Ducts",
    "SerC_CG_GIIS_Analog_Inputs_Isolator_2Wire_Type",
    "SerC_CG_Is_NAMUR_isolator_type_Required", 'SerC_CG_Ethernet_Interface', 'SerC_CG_Integrated_Marshalling_Cabinet', 'SerC_CG_Universal_Marshalling_Cabinet','SerC_CG_IP_Rating']
    for attr in Disallow_attrs:
        Product.DisallowAttr(attr)
    Product.AllowAttr('SerC_CG_IOTA_Carrier_Cover')
    if Product.Attr('SerC_CG_IOTA_Carrier_Cover').GetValue() == '':       
        Product.Attr('SerC_CG_IOTA_Carrier_Cover').SelectDisplayValue('No')
    parts_dict = dict()
    GS_Get_Set_AtvQty.resetAllAtvQty(Product, "Series_C_CG_Part_Summary")
    #GS_Get_Set_AtvQty.resetAllAtvQty(Product, "SerC_IO_Params")
    #module 49227 container is not included as it is visible only when we select turbomachinery
    modules = ['49225', '49225_1', '49229', '49229_1', '49231', '50461', '49233', '50463']
    #Module and container mapping
    contList = {'49225': 'SerC_CG_Enhanced_Function_IO_Cont2', '49225_1': 'C300_SerC_GIIS_CG_Cont', '49229':'SerC_CG_Enhanced_Function_IO_Cont' , '49229_1':'C300_SerC_GIIS_CG_Cont'}
    contList['49231'] = 'SerC_CG_Enhanced_Function_IO_Cont'
    contList['50461'] = 'SerC_CG_Enhanced_Function_IO_Cont2'
    contList['49233'] = 'SerC_CG_Enhanced_Function_IO_Cont'
    contList['49233_1'] = 'C300_SerC_GIIS_CG_Cont'
    contList['50463'] = 'SerC_CG_Enhanced_Function_IO_Cont2'
    contList['50463_1'] = 'C300_SerC_GIIS_CG_Cont'
    #Module and IO questions mapping
    #CXCPQ-49225
    iOType = {'49225':['Series-C: DI (32) 24 VDC with Open Wire Detect (0-5000)', 'Series-C: DI (32) 24VDC SOE (0-5000)']}
    ioTypes49225_1 = ['Series-C: GI/IS DI (32) 24VDC Solid State (0-5000)', 'Series-C: GI/IS DI (32) 24 VDC Relay (0-5000)']
    ioTypes49225_1.extend(['Series-C: GI/IS DI (32) 24 VDC Relay LFD (0-5000)', 'Series-C: GI/IS DI (32) 24VDC Relay with Expansion Board (0-5000)'])
    ioTypes49225_1.extend(['Series-C: GI/IS DI (32) 24VDC SOE Solid State (0-5000)', 'Series-C: GI/IS DI (32) 24 VDC SOE Relay (0-5000)'])
    ioTypes49225_1.extend(['Series-C: GI/IS DI (32) 24 VDC SOE Relay LFD (0-5000)', 'Series-C: GI/IS DI (32) 24VDC SOE Relay with Expansion Board (0-5000)'])
    iOType['49225_1'] = ioTypes49225_1
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
    #Module and container columns mapping
    column = {'49225':['Red_IS', 'Future_Red_IS', 'Non_Red_IS', 'Red_NIS', 'Future_Red_NIS', 'Non_Red_NIS', 'Red_ISLTR', 'Future_Red_ISLTR',  'Non_Red_ISLTR',  'Red_RLY',  'Future_Red_RLY',  'Non_Red_RLY'], '49225_1': ['Red_IS', 'Future_Red_IS', 'Non_Red_IS']}
    column['49229'] = ['Red_IS', 'Future_Red_IS', 'Non_Red_IS', 'Red_NIS', 'Future_Red_NIS', 'Non_Red_NIS', 'Red_ISLTR', 'Future_Red_ISLTR',  'Non_Red_ISLTR']
    column['49229_1'] = ['Red_IS', 'Future_Red_IS', 'Non_Red_IS']
    column['49231'] = ['Non_Red_IS', 'Non_Red_NIS', 'Non_Red_ISLTR']
    column['50461'] = ['Red_NIS', 'Future_Red_NIS', 'Non_Red_NIS']
    column['49233'] = ['Red_IS', 'Future_Red_IS', 'Non_Red_IS', 'Red_NIS', 'Future_Red_NIS', 'Non_Red_NIS', 'Red_ISLTR', 'Future_Red_ISLTR',  'Non_Red_ISLTR']
    column['49233_1'] = ['Red_IS', 'Future_Red_IS', 'Non_Red_IS']
    column['50463'] = ['Red_IS', 'Future_Red_IS', 'Non_Red_IS', 'Red_NIS', 'Future_Red_NIS', 'Non_Red_NIS', 'Red_ISLTR', 'Future_Red_ISLTR',  'Non_Red_ISLTR',  'Red_RLY',  'Future_Red_RLY',  'Non_Red_RLY']
    column['50463_1'] = ['Red_IS', 'Future_Red_IS', 'Non_Red_IS']
    #IO Calculation
    GS_SerC_Turbo_IO_Calc.applyPercentageOnTurboIOs(Product, percentInstalledSpare, modules, contList, iOType, column)
    #Get parts and quantity
    parts_dict = GS_SerC_Turbo_IO_Calc.getParts49225(Product, parts_dict)
    parts_dict = GS_SerC_Turbo_IO_Calc.getParts49229(Product, parts_dict)
    #As parameter of the userstory CXCPQ-49230 depends on CXCPQ-49229
    parts_dict = GS_SerC_Turbo_IO_Calc.getParts49230(Product, parts_dict)
    parts_dict = GS_SerC_Turbo_IO_Calc.getParts49231(Product, parts_dict)
    #As parameter of the userstory CXCPQ-49232 depends on CXCPQ-49231
    parts_dict = GS_SerC_Turbo_IO_Calc.getParts49232(Product, parts_dict)
    parts_dict = GS_SerC_Turbo_IO_Calc.getParts50461(Product, parts_dict)
    parts_dict = GS_SerC_Turbo_IO_Calc.getParts49233(Product, parts_dict)
    parts_dict = GS_SerC_Turbo_IO_Calc.getParts50463(Product, parts_dict)
#else:
    #Product.DisallowAttr('SerC_CG_Universal_Marshalling_Cabinet')

if len(parts_dict) > 0:
    ##Trace.Write(str(parts_dict))
    GS_C300_IO_Calc.setIOCount(Product, 'Series_C_CG_Part_Summary', parts_dict)
    ##ScriptExecutor.Execute('PS_Series_C_CG_Part_Summary_Cont_update_parts')
    ##Product.GetContainerByName('Series_C_CG_Part_Summary_Cont').Calculate()
if Product.Attr('SerC_CG_IO_Family_Type').GetValue()=="Series C":
    Product.SelectAttrValues('SerC_CG_Power_System_Type', 'Minimum Required Redundant')

#update the remote group name as per the selected io family type
isR2Qquote = True if Quote.GetCustomField("R2QFlag").Content else False
if not isR2Qquote:
    cgName = Product.Attr('Series_C_CG_Name').GetValue()
    if ioFamilyType == 'Series C':
        rgName = "Series-C {}".format(cgName)
    else:
        rgName = "{} {}".format(ioFamilyType, cgName)
    RGCont = Product.GetContainerByName('Series_C_Remote_Groups_Cont')
    idx = 0
    if RGCont.Rows.Count > 0:
        for row in RGCont.Rows:
            row["Series_C_RG_Name"] = "{} Remote Group{}".format(rgName, idx+1)
            idx += 1
            row.Product.Attr('Series_C_RG_Name').AssignValue(str(row["Series_C_RG_Name"]))
            row.ApplyProductChanges()
            row.Calculate()
fim_io_cont = Product.GetContainerByName('SerC_CG_FIM_FF_IO_Cont')
fim_io_tot_seg_cont = Product.GetContainerByName('SerC_CG_FIM_FF_Tot_Seg_transpose')
fim_io_cont.Rows.Clear()
fim_io_tot_seg_cont.Rows.Clear()
Product.Attr('FIM_Type').SelectValue('FIM8')
Product.Attr('FIM_Percent_Installed_Spare_Fieldbus_IO').AssignValue('0')
Product.Attr('FIM_Num_Devices_Open_Loop').AssignValue('10')
Product.Attr('FIM_Num_Devices_Close_Loop').AssignValue('10')
Product.Attr('FIM_Num_Close_Loop_per_Segment').AssignValue('4')
Product.Attr('FIM_Num_FF_Temp_Mux_per_Segment').AssignValue('8')
Product.Attr('FIM_Num_of_MOVs_per_Segment').AssignValue('6')
Product.Attr('FIM_need_separate_segment_for_MOVs').SelectValue('Yes')
Product.Attr('FIM_Ctrl_Firewall_to_FIM_Cable_Len').SelectValue('84 Inch')
Product.Attr('FIM_FF_IOs_with_Power_conditioner').SelectValue('No')
Product.Attr('FIM_power_source_FIM_Power_Conditioner').SelectValue('Internal')
Product.Attr('FIM_xFIM_Current_per_link_mA').AssignValue('160')