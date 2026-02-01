# TST - GS_PMD_Labor_Parameters

import System.Decimal as d

def float_cast(n):
    if n == '' or n is None:
        Log.Write("Invalid argument for cast to float in GS_PMD_ReadAttrs, returned 0.00")
        return float(0)
    else:
        return float(n)

class AttrStorage:
    def __init__(self, Product, get_attrs):

        #Inherited Parameters
        self.project_type = Product.Attr('New_Expansion').GetValue()
        self.loop_drawings = Product.Attr('Labor_Loop_Drawings').GetValue()
        self.unreleased_product = Product.Attr('Labor_Unreleased_Product').GetValue()
        self.marshalling_db = Product.Attr('Labor_Marshalling_Database').GetValue()
        self.perc_fat = Product.Attr('Labor_Percentage_FAT').GetValue()
        self.site_activities = Product.Attr('Labor_Site_Activities').GetValue()
        self.operation_manual = Product.Attr('Labor_Operation_Manual_Scope').GetValue()
        self.custom_scope = Product.Attr('Labor_Custom_Scope').GetValue()

        #PMD General Inputs
        self.pmd_cut_over =  Product.Attr('CE_Cutover').GetValue()

        #PMD System level Parameters
        self.process_type =  Product.GetContainerByName('PMD_Labour_Details').Rows[0].GetColumnByName("PMD_Process_Type").Value
        self.loop_count = Product.GetContainerByName('PMD_Labour_Details').Rows[0].GetColumnByName("PMD_Enter_Total_Cont").Value

        #Calculation based values
        AI = AO = DI = DO = MODBUS = self.num_switches = self.num_cim = self.num_cpm = self.num_cabinet = self.num_rg = 0

        self.num_cabinet = get_attrs.fce_cab_max8 + get_attrs.cab_max16 + get_attrs.dual_cc + get_attrs.single_cc_600 + get_attrs.single_cc_400 + get_attrs.furn_pie + get_attrs.pmd_plc_cab #System Cabinet count
        #BFJ - Defect CXCPQ-27022 - Adding in Dual Sided Cabinets into formula (dsccc)
        self.marshalling_cabinets = get_attrs.ssccc + get_attrs.dsccc + get_attrs.sscc_1200 + get_attrs.dscc_1200 + get_attrs.sscc_482 + get_attrs.dscc_482 + get_attrs.sscc_d400 + get_attrs.ssccc_2 + get_attrs.dsccc_2 + get_attrs.sscc_1200_2 + get_attrs.dscc_1200_2 + get_attrs.sscc_482_2 + get_attrs.dscc_482_2 + get_attrs.sscc_d400_2 + get_attrs.pdc_ds #Marshalling cabinet count - including Power Distribution Cabinet - last value (BFJ)
        Trace.Write('Marshalling Cabinet Count:')
        Trace.Write(self.marshalling_cabinets)
        Trace.Write('System Cabinet Count:')
        Trace.Write(self.num_cabinet)

        self.num_switches = get_attrs.repeater + get_attrs.repeater_profib_diag + get_attrs.ab7646f_anybus + get_attrs.dp_coupler + get_attrs.dp_pa_link + get_attrs.dp_pa_coupler + get_attrs.scalance_xc206_2 + get_attrs.scalance_x101_1 #No of Switches for PMD
        self.num_cpm = get_attrs.nrfce_profib_dp + get_attrs.rfce_profib_dp + get_attrs.nrfce_profin_pn #PMD Controller

        self.engineering_stations = 1.00


        self.AI = AI
        self.AO = AO
        self.DI = DI
        self.DO = DO
        self.MODBUS = MODBUS
        self.C = AI + AO + DI + DO
        
        
        # Bus AI/AO, DI/DO (CXCPQ-23740-45 TDH)
        sb_conts = ['PMD_Profibus_Drives_Cont_cpq',
                    'PMD_Profibus_Links_and_Gateways_Cont_cpq',
                    'PMD_Profibus_Motor_Starters_and_CD_Cont_cpq',
                    'PMD_Profibus_Modular_IO_Cont_cpq',
                    'PMD_Profibus_Displays_Cont_cpq',
                    'PMD_Other_Profibus_DP-Devices_Cont_cpq',
                    'PMD_Profinet_Device_Support_blocks_Cont_cpq']
        busAI = busAO = 0.0
        busDI = busDO = 0.0
        varA = 0.0
        for cont_name in sb_conts:
            cont = Product.GetContainerBySystemId(cont_name)
            try:
                if cont.Rows.Count != 0:
                    for row in cont.Rows:
                        varA += 1.0
                        busAI += float_cast(row.GetColumnByName('AI_Calc').Value)
                        busAO += float_cast(row.GetColumnByName('AO_Calc').Value)
                        busDI += float_cast(row.GetColumnByName('DI_Calc').Value)
                        busDO += float_cast(row.GetColumnByName('DO_Calc').Value)
            except:
                Trace.Write("Param error for: " + cont_name)
        Trace.Write('Number of Systems:')
        Trace.Write(varA)
        
        BFJ = self.num_rg
        Trace.Write('Test - # of Systems from attrs.num_rg')
        Trace.Write(BFJ)
        
        cc_cards = Product.GetContainerByName('PMD_CC_Cards').Rows[0]
        ce_plc_io = Product.GetContainerByName('PMD_IO_ControlEdge_PLC_IO_Cards').Rows[0]
        # Hardwired AI Count
        hardwiredAI = float_cast(cc_cards.GetColumnByName('PMD_Analog_IC').Value) + (d.Ceiling(float_cast(ce_plc_io.GetColumnByName('PMD_Uni_IO').Value))/2) + float_cast(ce_plc_io.GetColumnByName('PMD_Uni_AI').Value)
        hardwiredAO = float_cast(cc_cards.GetColumnByName('PMD_Analog_OC').Value) + (d.Ceiling(float_cast(ce_plc_io.GetColumnByName('PMD_Uni_IO').Value))/2)
        
        hardwiredDI = float_cast(cc_cards.GetColumnByName('PMD_Binary_IC_16Channel').Value) + float_cast(cc_cards.GetColumnByName('PMD_Binary_IC_24Channel').Value) + float_cast(cc_cards.GetColumnByName('PMD_Power_BIC_115V').Value) + float_cast(cc_cards.GetColumnByName('PMD_Power_BIC_230V').Value) + float_cast(ce_plc_io.GetColumnByName('PMD_DI_16').Value) + float_cast(ce_plc_io.GetColumnByName('PMD_DI_32').Value)
        
        #CXCPQ-23744 addded by Adarsh #"total_do_count" gives the value of total_DO
        hardwired_al_DO = float_cast(cc_cards.GetColumnByName('PMD_Binary_OC').Value) + float_cast(cc_cards.GetColumnByName('PMD_Power_BOC_115V').Value) + float_cast(cc_cards.GetColumnByName('PMD_Power_BOC_230V').Value)

        hardwired_ce_DO = float_cast(Product.GetContainerByName('PMD_IO_ControlEdge_PLC_IO_Cards').Rows[0].GetColumnByName('PMD_DO_8').Value) + float_cast(Product.GetContainerByName('PMD_IO_ControlEdge_PLC_IO_Cards').Rows[0].GetColumnByName('PMD_DO_32').Value)

        hardwiredDO = hardwired_al_DO + hardwired_ce_DO
        
        # Alcont CXCPQ-23745
        alcont = 0.0
        if float_cast(cc_cards.GetColumnByName('PMD_Analog_OC').Value) > 0 or \
            float_cast(cc_cards.GetColumnByName('PMD_Analog_IC').Value) > 0 or \
            float_cast(cc_cards.GetColumnByName('PMD_Binary_OC').Value) > 0 or \
            float_cast(cc_cards.GetColumnByName('PMD_Power_BOC_115V').Value) > 0 or \
            float_cast(cc_cards.GetColumnByName('PMD_Power_BOC_230V').Value) > 0 or \
            float_cast(cc_cards.GetColumnByName('PMD_Binary_IC_16Channel').Value) > 0 or \
            float_cast(cc_cards.GetColumnByName('PMD_Binary_IC_24Channel').Value) > 0 or \
            float_cast(cc_cards.GetColumnByName('PMD_Power_BIC_115V').Value) > 0 or \
            float_cast(cc_cards.GetColumnByName('PMD_Power_BIC_230V').Value) > 0:
            alcont = 1.0
        
        # CE900 CXCPQ-23745
        ce900 = 0.0
        if float_cast(ce_plc_io.GetColumnByName('PMD_Uni_IO').Value) > 0 or \
            float_cast(ce_plc_io.GetColumnByName('PMD_Uni_AI').Value) > 0 or \
            float_cast(ce_plc_io.GetColumnByName('PMD_DI_16').Value) > 0 or \
            float_cast(ce_plc_io.GetColumnByName('PMD_DI_32').Value) > 0 or \
            float_cast(ce_plc_io.GetColumnByName('PMD_DO_8').Value) > 0 or \
            float_cast(ce_plc_io.GetColumnByName('PMD_DO_32').Value) > 0:
            ce900 = 1.0
            
        self.AI = hardwiredAI + busAI
        self.AO = hardwiredAO + busAO
        self.DI = hardwiredDI + busDI
        self.DO = hardwiredDO + busDO
        self.MODBUS = MODBUS
        self.C = (hardwiredAI + busAI) + (hardwiredAO + busAO) + (hardwiredDI + busDI) + (hardwiredDO + busDO)
        self.num_rg = varA + alcont + ce900
        
        Trace.Write("PMD Params. TotalAI: {0}, TotalAO: {1}, TotalDI: {2}, TotalDO: {3}, MODBUS: {4}, C: {5}, A: {6}, CPMs: {7}, Switches: {8}".format(self.AI,self.AO,self.DI,self.DO,self.MODBUS,self.C,self.num_rg, self.num_cpm, self.num_switches))