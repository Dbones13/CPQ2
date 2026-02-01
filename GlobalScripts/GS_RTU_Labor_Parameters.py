from math import ceil

class AttrStorage:
    def __init__(self, Product):

        #Inherited Parameters
        #self.project_type = Product.Attr('New_Expansion').GetValue()
        self.Loop = Product.Attr('Labor_Loop_Drawings').GetValue()
        '''self.unreleased_product = Product.Attr('Labor_Unreleased_Product').GetValue()
        self.marshalling_db = Product.Attr('Labor_Marshalling_Database').GetValue()
        self.perc_fat = Product.Attr('Labor_Percentage_FAT').GetValue()
        self.site_activities = Product.Attr('Labor_Site_Activities').GetValue()
        self.operation_manual = Product.Attr('Labor_Operation_Manual_Scope').GetValue()
        self.custom_scope = Product.Attr('Labor_Custom_Scope').GetValue()'''
        
        #UOC System level Parameters
        self.stn = Product.GetContainerByName('RTU_Software_Labor_Container1').Rows[0].GetColumnByName("RTU_Engineering_Stations").Value
        self.Rswt = Product.GetContainerByName('RTU_Software_Labor_Container2').Rows[0].GetColumnByName("RTU_Switches").Value
        self.LTp = Product.GetContainerByName('RTU_Software_Labor_Container2').Rows[0].GetColumnByName("RTU_Loop_Typical").Value
        
        #Section to read from Control Groups
        '''self.ai_1 = self.ai_2 = self.ai_3 = self.ai_4 = self.ai_5 = self.ai_6 = self.ai_7 = self.ai_8 = self.ai_9 = self.ai_10 = 0
        self.ao_1 = self.ao_2 = self.ao_3 = self.ao_4 = self.ao_5 = self.ao_6 = self.ao_7 = self.ao_8 = self.ao_9 = self.ao_10 = 0
        self.di_1 = self.di_2 = self.di_3 = self.di_4 = self.di_5 = self.di_6 = self.di_7 = self.di_8 = self.di_9 = self.di_10 = 0
        self.do_1 = self.do_2 = self.do_3 = self.do_4 = self.do_5 = self.do_6 = self.do_7 = self.do_8 = self.do_9 = self.do_10 = 0
        self.sl_1 = self.sl_2 = self.sl_3 = self.sl_4 = self.sl_5 = self.sl_6 = self.sl_7 = self.sl_8 = self.sl_9 = self.sl_10 = 0
        self.cl_1 = self.cl_2 = self.cl_3 = self.cl_4 = self.cl_5 = self.cl_6 = self.cl_7 = self.cl_8 = self.cl_9 = self.cl_10 = 0
        self.se_1 = self.se_2 = self.se_3 = self.se_4 = self.se_5 = self.se_6 = self.se_7 = self.se_8 = self.se_9 = self.se_10 = 0
        self.ce_1 = self.ce_2 = self.ce_3 = self.ce_4 = self.ce_5 = self.ce_6 = self.ce_7 = self.ce_8 = self.ce_9 = self.ce_10 = 0
        self.ffio_1 = self.ffio_2 = self.ffio_3 = self.ffio_4 = self.ffio_5 = self.ffio_6 = self.ffio_7 = self.ffio_8 = self.ffio_9 = self.ffio_10 = 0
        self.wio_1 = self.wio_2 = self.wio_3 = self.wio_4 = self.wio_5 = self.wio_6 = self.wio_7 = self.wio_8 = self.wio_9 = self.wio_10 = 0
        self.iom_1 = self.iom_2 = self.iom_3 = self.iom_4 = self.iom_5 = self.iom_6 = self.iom_7 = self.iom_8 = self.iom_9 = self.iom_10 = 0
        self.scab_1 = self.scab_2 = self.scab_3 = self.scab_4 = self.scab_5 = self.scab_6 = self.scab_7 = self.scab_8 = self.scab_9 = self.scab_10 = 0
        self.mar_1 = self.mar_2 = self.mar_3 = self.mar_4 = self.mar_5 = self.mar_6 = self.mar_7 = self.mar_8 = self.mar_9 = self.mar_10 = 0
        self.aga_1 = self.aga_2 = self.aga_3 = self.aga_4 = self.aga_5 = self.aga_6 = self.aga_7 = self.aga_8 = self.aga_9 = self.aga_10 = 0
        self.ins_1 = self.ins_2 = self.ins_3 = self.ins_4 = self.ins_5 = self.ins_6 = self.ins_7 = self.ins_8 = self.ins_9 = self.ins_10 = 0'''
        self.rtu = 0

        #AI = AO = DI = DO = MODBUS = self.num_switches = self.num_rg = self.ctr = self.sys = self.is_ios =  0.0
        cg_count = 1
        control_groups = Product.GetContainerByName('RTU_ControlGroup_Cont').Rows
        for control_group in control_groups:
            control = control_group.Product
            ins = control.GetContainerByName('RTU_CG_Controller_Cont').Rows[0].GetColumnByName('Replica_configurations').Value
            self.rtu += int(ins)
            setattr(self, str('ins_' + str(cg_count)), str(ins))

            #AI Params
            ai_non_hart = control.GetContainerByName('RTU_CG_IO_Container').Rows[0].GetColumnByName("Non_HART_Analog_Input").Value
            ai_hart = control.GetContainerByName('RTU_CG_IO_Container').Rows[0].GetColumnByName("HART_Analog_Input").Value
            ai_pulse_input = control.GetContainerByName('RTU_CG_IO_Container').Rows[0].GetColumnByName("Pulse_Input").Value
            AI = int(ai_non_hart) + int(ai_hart) + int(ai_pulse_input)
            #AO Parms
            ao_non_hart = control.GetContainerByName('RTU_CG_IO_Container').Rows[0].GetColumnByName("Non_HART_Analog_Output").Value
            ao_hart = control.GetContainerByName('RTU_CG_IO_Container').Rows[0].GetColumnByName("HART_Analog_Output").Value
            AO = int(ao_non_hart) + int(ao_hart)

            #DI and DO
            di = control.GetContainerByName('RTU_CG_IO_Container').Rows[0].GetColumnByName("Digital_Input").Value
            DI = int(di)
            do = control.GetContainerByName('RTU_CG_IO_Container').Rows[0].GetColumnByName("Digital_Output").Value
            DO = int(do)
            self.AI = AI
            self.AO = AO
            self.DI = DI
            self.DO = DO
            wio = control.GetContainerByName('RTU_CG_IO_Container').Rows[0].GetColumnByName('Field_ISA100_Wireless_Devices').Value
            ffio = control.GetContainerByName('RTU_CG_IO_Container').Rows[0].GetColumnByName('FIM_Analog_Input').Value

            setattr(self, str('ai_' + str(cg_count)), str(AI))
            setattr(self, str('ao_' + str(cg_count)), str(AO))
            setattr(self, str('di_' + str(cg_count)), str(di))
            setattr(self, str('do_' + str(cg_count)), str(do))
            setattr(self, str('wio_' + str(cg_count)), str(wio))
            setattr(self, str('ffio_' + str(cg_count)), str(ffio))

            setattr(self, str('sl_' + str(cg_count)), round(float(70 * (float(AO)/100)), 0))
            setattr(self, str('cl_' + str(cg_count)), round(float(30 * (float(AO)/100)), 0))
            setattr(self, str('se_' + str(cg_count)), round(float(70 * (float(DO)/100)), 0))
            setattr(self, str('ce_' + str(cg_count)), round(float(30 * (float(DO)/100)), 0))

            setattr(self, str('scab_' + str(cg_count)), 0)
            setattr(self, str('iom_' + str(cg_count)), 0)
            for part in control.GetContainerByName('RTU_CG_PartSummary_Cont').Rows:
                if part['CE_Part_Number'] == 'SC-UMIX01':
                    setattr(self, str('iom_' + str(cg_count)), str(int(part['CE_Part_Qty'])/int(ins)))
                elif part['CE_Part_Number'] == 'CC-CBDD01':
                    setattr(self, str('scab_' + str(cg_count)),str(int(part['CE_Part_Qty'])/int(ins)))
                elif part['CE_Part_Number'] == 'CC-CBDS01':
                    setattr(self, str('scab_' + str(cg_count)), ceil(float(int(part['CE_Part_Qty'])/int(ins))/2))
            #mar
            mar = control.GetContainerByName('RTU_CG_Labor_Cont').Rows[0].GetColumnByName('Marshalling_Cabinet_Count').Value
            setattr(self, str('mar_' + str(cg_count)), str(mar))

            #AGA Calc
            aga = control.GetContainerByName('RTU_CG_Labor_Cont').Rows[0].GetColumnByName('AGA_Calculation_present').Value
            if aga == 'Yes':
                setattr(self, str('aga_' + str(cg_count)), float(0.2 * (int(AI) + int(ffio) + int(wio))))

            # Hardware Similarity
            hws  = control.GetContainerByName('RTU_CG_Labor_Cont').Rows[0].GetColumnByName('RTU_Similar_Control_Groups').Value
            setattr(self, str('hws_' + str(cg_count)), str(hws))

            cg_count+=1

        self.cg_count = cg_count -1