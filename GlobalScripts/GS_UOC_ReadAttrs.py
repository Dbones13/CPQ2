# GS_UOC_Read_Attrs

class AttrStorage:
    def getFloat(self, value):
        try:
            return float(value)
        except:
            return float(0)
    def __init__(self, Product):
        ## Product: Project
        if Product.Name == "New / Expansion Project":

            ## Container: CE_Project_Questions_Cont
            ce_proj_cont = Product.GetContainerByName('CE_Project_Questions_Cont').Rows[0]
            self.ce_proj_type = ce_proj_cont.GetColumnByName('CE_Project_Type').Value
            self.ce_proj_site_volt = ce_proj_cont.GetColumnByName('CE_Site_Voltage').Value
            self.ce_proj_site_freq = ce_proj_cont.GetColumnByName('CE_Site_Frequency').Value

        ## Product: System Group
        elif Product.Name == "System Group":

            #Inherit attr from parent product
            self.ce_proj_site_volt = Product.Attr('CE_Site_Voltage').GetValue()

            ## Container: CE_General_Inputs_Cont
            ce_gen_inputs_cont = Product.GetContainerByName('CE_General_Inputs_Cont').Rows[0]
            self.ce_gen_inputs_sys_asset = ce_gen_inputs_cont.GetColumnByName('CE_System_Asset').Value
            self.ce_gen_inputs_sys_num = ce_gen_inputs_cont.GetColumnByName('CE_System_Number').Value
            self.ce_gen_inputs_ebr_media = ce_gen_inputs_cont.GetColumnByName('CE_EBR_Media').Value

        # UOC System
            ## Product: UOC System
        elif Product.Name in ["ControlEdge UOC System","ControlEdge UOC System Migration"]:

            self.plc_or_uoc = 'UOC'

            #Inherit attr from parent product
            self.ce_proj_site_volt = Product.Attr('CE_Site_Voltage').GetValue()


            ## Container: UOC_Software_Question_Cont
            UOC_soft_q_cont = Product.GetContainerByName('UOC_Software_Question_Cont').Rows[0]
            self.UOC_soft_q_soft_release = UOC_soft_q_cont.GetColumnByName('UOC_Software_Release').Value
            self.UOC_soft_q_med_deliv = UOC_soft_q_cont.GetColumnByName('UOC_Media_Delivery').Value
            self.UOC_soft_q_soft_release_backup = UOC_soft_q_cont.GetColumnByName('UOC_Backup_Restore_Software_Release').Value
            self.UOC_soft_q_med_deliv_backup = UOC_soft_q_cont.GetColumnByName('UOC_Backup_Restore_Media_Delivery').Value

            ## Container: UOC_Common_Questions_Cont
            UOC_comm_q_cont = Product.GetContainerByName('UOC_Common_Questions_Cont').Rows[0]
            self.UOC_comm_q_shielded_term_setup = UOC_comm_q_cont.GetColumnByName('UOC_Shielded_Terminal_Strip').Value
            self.UOC_comm_q_io_fill_mod = UOC_comm_q_cont.GetColumnByName('UOC_IO_Filler_Module').Value
            self.UOC_comm_q_io_spare = self.getFloat(UOC_comm_q_cont.GetColumnByName('UOC_IO_Spare').Value)/100
            self.UOC_comm_q_io_slot_spare = self.getFloat(UOC_comm_q_cont.GetColumnByName('UOC_IO_Slot_Spare').Value)/100
            self.UOC_comm_q_number_cg = self.getFloat(UOC_comm_q_cont.GetColumnByName('UOC_Number_CGs').Value)/100
            self.UOC_comm_q_cabinet_required = UOC_comm_q_cont.GetColumnByName('UOC_Cabinet_Required_Racks_Mounting').Value
            self.UOC_comm_q_starter_kit = UOC_comm_q_cont.GetColumnByName('UOC_Starter_Kit').Value
            self.UOC_comm_q_starter_kit_with_experion_license = UOC_comm_q_cont.GetColumnByName('UOC_Starter_ Kit_with_Experion_License').Value

            ## Container: UOC_PartSummary_Cont
            #UOC_partsumm_cont = Product.GetContainerByName('UOC_PartSummary_Cont').Rows[0]

            ## Container: UOC_ControlGroup_Cont
            #UOC_ctrlgrp_cont = Product.GetContainerByName('UOC_ControlGroup_Cont').Rows[0]

        ## Product: UOC Control Group
        elif Product.Name == "UOC Control Group":

            self.plc_or_uoc = 'UOC'
            self.cg_or_rg = 'CG'
            
            #Inherit attr from parent product
            self.ce_proj_site_volt = Product.Attr('CE_Site_Voltage').GetValue()
            self.comm_q_io_fill_mod = Product.Attr('UOC_IO_Filler_Module').GetValue()
            self.UOC_comm_q_io_spare = self.getFloat(Product.Attr('UOC_IO_Spare').GetValue())/100
            self.UOC_comm_q_io_slot_spare = self.getFloat(Product.Attr('UOC_IO_Slot_Spare').GetValue())/100
            self.comm_q_shielded_term_setup = Product.Attr('UOC_Shielded_Terminal_Strip').GetValue()
            self.comm_q_cabinet_required = Product.Attr('Cabinet_Required_Racks_Mounting').GetValue()
            self.exp_pks_software_release= Product.Attr('Controledge_Exp_PKS_software_release').GetValue()

            ## Container: UOC_CG_Cabinet_Cont
            cabinet_cont = Product.GetContainerByName('UOC_CG_Cabinet_Cont').Rows[0]
            self.cabinet_type = cabinet_cont.GetColumnByName('UOC_Cabinet_Type').Value
            self.cabinet_door_type = cabinet_cont.GetColumnByName('UOC_Cabinet_Door_Type').Value
            self.cabinet_door_keylock = cabinet_cont.GetColumnByName('UOC_Cabinet_Door_Keylock').Value
            self.cabinet_base_size = cabinet_cont.GetColumnByName('UOC_Cabinet_Base_Size').Value
            self.cabinet_pwr_entry = cabinet_cont.GetColumnByName('UOC_Cabinet_Power_Entry').Value
            self.cabinet_spare_space = self.getFloat(cabinet_cont.GetColumnByName('UOC_Cabinet_Spare_Space').Value)/100
            self.cabinet_integ_marshalling = cabinet_cont.GetColumnByName('UOC_Integrated_Marshalling_Cabinet').Value
            self.cabinet_tstat = cabinet_cont.GetColumnByName('UOC_Cabinet_Thermostat').Value
            self.cabinet_light = cabinet_cont.GetColumnByName('UOC_Cabinet_Light').Value

            ## Container: UOC_CG_Controller_Rack_Cont
            ctrl_rack_cont = Product.GetContainerByName('UOC_CG_Controller_Rack_Cont').Rows[0]
            self.ctrl_rack_ctrl_type = ctrl_rack_cont.GetColumnByName('UOC_Controller_Type').Value.replace(' ','')
            self.ctrl_rack_io_rack_type = ctrl_rack_cont.GetColumnByName('UOC_IO_Rack_Type').Value
            self.ctrl_rack_pwr_sply = ctrl_rack_cont.GetColumnByName('UOC_Power_Supply').Value.replace(' ','')
            self.ctrl_rack_pwr_input = ctrl_rack_cont.GetColumnByName('UOC_Power_Input').Value
            self.ctrl_rack_pwr_status_mod_red_sply = ctrl_rack_cont.GetColumnByName('UOC_Power_Status_Mod_Redundant_Supply').Value
            self.ctrl_rack_field_wire_didoaoai = ctrl_rack_cont.GetColumnByName('UOC_Field_Wiring_DIDOAOAI_Channel_Mod').Value
            #self.ctrl_rack_field_wire_PIFII = ctrl_rack_cont.GetColumnByName('UOC_Field_Wiring_PIFII_Channel_Mod').Value
            self.ctrl_rack_field_wire_other = ctrl_rack_cont.GetColumnByName('UOC_Field_Wiring_Other_Mod').Value
            self.ctrl_rack_remote_term_cbl_len = ctrl_rack_cont.GetColumnByName('UOC_Remote_Terminal_Cable_Length').Value
            self.ctrl_rack_network_topo = ctrl_rack_cont.GetColumnByName('UOC_Network_Topology').Value
            self.ctrl_rack_ether_swtch_splyr = ctrl_rack_cont.GetColumnByName('UOC_Ethernet_Switch_Supplier').Value
            self.ctrl_rack_ether_swtch_type = ctrl_rack_cont.GetColumnByName('UOC_Ethernet_Switch_Type').Value
            self.ctrl_rack_rem_term_pan_cab_type = ctrl_rack_cont.GetColumnByName('UOC_Remote_Terminal_Panel_Cable_Type').Value
            self.ctrl_rack_phys_sep = ctrl_rack_cont.GetColumnByName('UOC_Redundant_Controller_Physical_Seperation').Value
            self.ctrl_operating_temp = ctrl_rack_cont.GetColumnByName('UOC_Operating_Temprature').Value

            ## Container: UOC_CG_NR_UIO_Cont Non-Redundant
            nr_uio_cont = Product.GetContainerByName('UOC_CG_UIO_Cont').Rows[0]
            self.nr_uio_ai_pts = self.getFloat(nr_uio_cont.GetColumnByName('UOC_AI_Points').Value)
            self.nr_uio_ai_hart_pts = self.getFloat(nr_uio_cont.GetColumnByName('UOC_AI_HART_Points').Value)
            self.nr_uio_ao_100_250 = self.getFloat(nr_uio_cont.GetColumnByName('UOC_AO_100_250').Value)
            self.nr_uio_ao_250_499 = self.getFloat(nr_uio_cont.GetColumnByName('UOC_AO_250_499').Value)
            self.nr_uio_ao_500 = self.getFloat(nr_uio_cont.GetColumnByName('UOC_AO_500').Value)
            self.nr_uio_ao_hart_100_250 = self.getFloat(nr_uio_cont.GetColumnByName('UOC_AO_HART_100_250').Value)
            self.nr_uio_ao_hart_250_499 = self.getFloat(nr_uio_cont.GetColumnByName('UOC_AO_HART_250_499').Value)
            self.nr_uio_ao_hart_500 = self.getFloat(nr_uio_cont.GetColumnByName('UOC_AO_HART_500').Value)
            self.nr_uio_di_pts = self.getFloat(nr_uio_cont.GetColumnByName('UOC_DI_Points').Value)
            self.nr_uio_do_10_250 = self.getFloat(nr_uio_cont.GetColumnByName('UOC_DO_10_250').Value)
            self.nr_uio_do_250_500 = self.getFloat(nr_uio_cont.GetColumnByName('UOC_DO_250_500').Value)

            ## Container: UOC_CG_R_UIO_Cont Redundant
            r_uio_cont = Product.GetContainerByName('UOC_CG_UIO_Cont').Rows[1]
            self.r_uio_ai_pts = self.getFloat(r_uio_cont.GetColumnByName('UOC_AI_Points').Value)
            self.r_uio_ao_100_250 = self.getFloat(r_uio_cont.GetColumnByName('UOC_AO_100_250').Value)
            self.r_uio_ao_250_499 = self.getFloat(r_uio_cont.GetColumnByName('UOC_AO_250_499').Value)
            self.r_uio_ao_500 = self.getFloat(r_uio_cont.GetColumnByName('UOC_AO_500').Value)
            self.r_uio_di_pts = self.getFloat(r_uio_cont.GetColumnByName('UOC_DI_Points').Value)
            self.r_uio_do_10_250 = self.getFloat(r_uio_cont.GetColumnByName('UOC_DO_10_250').Value)
            self.r_uio_do_250_500 = self.getFloat(r_uio_cont.GetColumnByName('UOC_DO_250_500').Value)
            self.r_uio_ai_hart_pts = self.getFloat(r_uio_cont.GetColumnByName('UOC_AI_HART_Points').Value)
            self.r_uio_ao_hart_100_250 = self.getFloat(r_uio_cont.GetColumnByName('UOC_AO_HART_100_250').Value)
            self.r_uio_ao_hart_250_499 = self.getFloat(r_uio_cont.GetColumnByName('UOC_AO_HART_250_499').Value)
            self.r_uio_ao_hart_500 = self.getFloat(r_uio_cont.GetColumnByName('UOC_AO_HART_500').Value)
            
            ## Container: UOC_CG_PF_IO_Cont
            pf_io_cont = Product.GetContainerByName('UOC_CG_PF_IO_Cont').Rows[0]
            self.pf_io_cab_len = pf_io_cont.GetColumnByName('UOC_PF_Cable_Length').Value
            self.pf_io_ai_hart = self.getFloat(pf_io_cont.GetColumnByName('UOC_AI_Hart').Value)
            self.pf_io_ao_hart = self.getFloat(pf_io_cont.GetColumnByName('UOC_AO_Hart').Value)
            self.pf_io_di_cont = self.getFloat(pf_io_cont.GetColumnByName('UOC_DI_Contact').Value)
            self.pf_io_do_points = self.getFloat(pf_io_cont.GetColumnByName('UOC_DO_Points').Value)
            self.pf_io_do_max_load = self.getFloat(pf_io_cont.GetColumnByName('UOC_DO_Max_Load').Value)
            self.pf_io_ai_points = self.getFloat(pf_io_cont.GetColumnByName('UOC_AI_Points').Value)
            self.pf_io_ao_points = self.getFloat(pf_io_cont.GetColumnByName('UOC_AO_Points').Value)

            ## Container: UOC_CG_Other_IO_Cont
            other_io_cont = Product.GetContainerByName('UOC_CG_Other_IO_Cont').Rows[0]
            self.other_io_univ_ai8 = self.getFloat(other_io_cont.GetColumnByName('UOC_Universal_Analog_Input8').Value)
            self.other_io_univ_ai8_tcrtdmvohm = self.getFloat(other_io_cont.GetColumnByName('UOC_Universal_Analog_Input8_TCRTDmVOhm').Value)
            self.other_io_ai16 = self.getFloat(other_io_cont.GetColumnByName('UOC_Analog_Input16').Value)
            self.other_io_ao4 = self.getFloat(other_io_cont.GetColumnByName('UOC_Analog_Output4').Value)
            self.other_io_ao8_intrnl = self.getFloat(other_io_cont.GetColumnByName('UOC_Analog_Output8_Internal').Value)
            self.other_io_ao8_extrnl = self.getFloat(other_io_cont.GetColumnByName('UOC_Analog_Output8_External').Value)
            self.other_io_di32 = self.getFloat(other_io_cont.GetColumnByName('UOC_Digital_Input32').Value)
            self.other_io_di16_120240vac = self.getFloat(other_io_cont.GetColumnByName('UOC_Digital_Input16_120240VAC').Value)
            self.other_io_di_cntct_type16 = self.getFloat(other_io_cont.GetColumnByName('UOC_Digital_Input_Contact_Type16').Value)
            self.other_io_di_16_125vdc = self.getFloat(other_io_cont.GetColumnByName('UOC_Digital_Input16_125VDC').Value)
            self.other_io_do32 = self.getFloat(other_io_cont.GetColumnByName('UOC_Digital_Output32').Value)
            self.other_io_do8 = self.getFloat(other_io_cont.GetColumnByName('UOC_Digital_Output8').Value)
            self.other_io_do_relay8 = self.getFloat(other_io_cont.GetColumnByName('UOC_Digital_Output_Relay8').Value)
            self.other_io_pulseinput_freq4=self.getFloat(other_io_cont.GetColumnByName('UOC_Pulse_Input_Frequency_point4').Value)

            ## Container: UOC_CG_Additional_Controller_Cont
            addl_ctrlr_cont = Product.GetContainerByName('UOC_CG_Additional_Controller_Cont').Rows[0]
            self.addl_ctrlr_2_pos_term_brd_jmprs = self.getFloat(addl_ctrlr_cont.GetColumnByName('UOC_Two_Pos_Terminal_Board_Jumpers').Value)
            self.addl_ctrlr_10_pos_term_brd_jmprs = self.getFloat(addl_ctrlr_cont.GetColumnByName('UOC_Ten_Pos_Terminal_Board_Jumpers').Value)
            self.addl_ctrlr_mimp_250ohm_resis_kit = self.getFloat(addl_ctrlr_cont.GetColumnByName('UOC_MIMP_250Ohm_Resistor_Kit').Value)
            self.addl_ctrlr_io_mod_label_kit = self.getFloat(addl_ctrlr_cont.GetColumnByName('UOC_IO_Mod_Label_Kit').Value)
            self.addl_ctrlr_fib_opt_conv_multi = self.getFloat(addl_ctrlr_cont.GetColumnByName('UOC_Fiber_Optic_Converter_Multi').Value)
            self.addl_ctrlr_fib_opt_conv_single = self.getFloat(addl_ctrlr_cont.GetColumnByName('UOC_Fiber_Optic_Converter_Single').Value)
            self.addl_ctrlr_addl_ctrlr = self.getFloat(addl_ctrlr_cont.GetColumnByName('UOC_Additonal_Controller').Value)

        ## Product: UOC Remote Group
        elif Product.Name == "UOC Remote Group":
        
            self.plc_or_uoc = 'UOC'
            self.cg_or_rg = 'RG'

            #Inherit attr from parent product
            self.ce_proj_site_volt = Product.Attr('CE_Site_Voltage').GetValue()
            self.comm_q_io_fill_mod = Product.Attr('UOC_IO_Filler_Module').GetValue()
            self.UOC_comm_q_io_spare = self.getFloat(Product.Attr('UOC_IO_Spare').GetValue())/100
            self.UOC_comm_q_io_slot_spare = self.getFloat(Product.Attr('UOC_IO_Slot_Spare').GetValue())/100
            self.comm_q_shielded_term_setup = Product.Attr('UOC_Shielded_Terminal_Strip').GetValue()
            self.comm_q_cabinet_required = Product.Attr('Cabinet_Required_Racks_Mounting').GetValue()
            self.exp_pks_software_release= Product.Attr('Controledge_Exp_PKS_software_release').GetValue()

            ## Container: UOC_RG_Cabinet_Cont
            cabinet_cont = Product.GetContainerByName('UOC_RG_Cabinet_Cont').Rows[0]
            self.cabinet_type = cabinet_cont.GetColumnByName('UOC_Cabinet_Type').Value
            self.cabinet_door_type = cabinet_cont.GetColumnByName('UOC_Cabinet_Door_Type').Value
            self.cabinet_door_keylock = cabinet_cont.GetColumnByName('UOC_Cabinet_Door_Keylock').Value
            self.cabinet_base_size = cabinet_cont.GetColumnByName('UOC_Cabinet_Base_Size').Value
            self.cabinet_pwr_entry = cabinet_cont.GetColumnByName('UOC_Cabinet_Power_Entry').Value
            self.cabinet_spare_space = self.getFloat(cabinet_cont.GetColumnByName('UOC_Cabinet_Spare_Space').Value)/100
            self.cabinet_integ_marshalling = cabinet_cont.GetColumnByName('UOC_Integrated_Marshalling_Cabinet').Value
            self.cabinet_tstat = cabinet_cont.GetColumnByName('UOC_Cabinet_Thermostat').Value
            self.cabinet_light = cabinet_cont.GetColumnByName('UOC_Cabinet_Light').Value

            ## Container: UOC_RG_Controller_Rack_Cont
            ctrl_rack_cont = Product.GetContainerByName('UOC_RG_Controller_Rack_Cont').Rows[0]
            #self.ctrl_rack_ctrl_type = ctrl_rack_cont.GetColumnByName('UOC_Controller_Type').Value
            self.ctrl_rack_io_rack_type = ctrl_rack_cont.GetColumnByName('UOC_IO_Rack_Type').Value
            self.ctrl_rack_pwr_sply = ctrl_rack_cont.GetColumnByName('UOC_Power_Supply').Value.replace(' ','')
            self.ctrl_rack_pwr_input = ctrl_rack_cont.GetColumnByName('UOC_Power_Input').Value
            self.ctrl_rack_pwr_status_mod_red_sply = ctrl_rack_cont.GetColumnByName('UOC_Power_Status_Mod_Redundant_Supply').Value
            self.ctrl_rack_field_wire_didoaoai = ctrl_rack_cont.GetColumnByName('UOC_Field_Wiring_DIDOAOAI_Channel_Mod').Value
            #self.ctrl_rack_field_wire_PIFII = ctrl_rack_cont.GetColumnByName('UOC_Field_Wiring_PIFII_Channel_Mod').Value
            self.ctrl_rack_field_wire_other = ctrl_rack_cont.GetColumnByName('UOC_Field_Wiring_Other_Mod').Value
            self.ctrl_rack_remote_term_cbl_len = ctrl_rack_cont.GetColumnByName('UOC_Remote_Terminal_Cable_Length').Value

            ## Container: UOC_RG_NR_UIO_Cont Non-Redundant
            nr_uio_cont = Product.GetContainerByName('UOC_RG_UIO_Cont').Rows[0]
            self.nr_uio_ai_pts = self.getFloat(nr_uio_cont.GetColumnByName('UOC_AI_Points').Value)
            self.nr_uio_ai_hart_pts = self.getFloat(nr_uio_cont.GetColumnByName('UOC_AI_HART_Points').Value)
            self.nr_uio_ao_100_250 = self.getFloat(nr_uio_cont.GetColumnByName('UOC_AO_100_250').Value)
            self.nr_uio_ao_250_499 = self.getFloat(nr_uio_cont.GetColumnByName('UOC_AO_250_499').Value)
            self.nr_uio_ao_500 = self.getFloat(nr_uio_cont.GetColumnByName('UOC_AO_500').Value)
            self.nr_uio_ao_hart_100_250 = self.getFloat(nr_uio_cont.GetColumnByName('UOC_AO_HART_100_250').Value)
            self.nr_uio_ao_hart_250_499 = self.getFloat(nr_uio_cont.GetColumnByName('UOC_AO_HART_250_499').Value)
            self.nr_uio_ao_hart_500 = self.getFloat(nr_uio_cont.GetColumnByName('UOC_AO_HART_500').Value)
            self.nr_uio_di_pts = self.getFloat(nr_uio_cont.GetColumnByName('UOC_DI_Points').Value)
            self.nr_uio_do_10_250 = self.getFloat(nr_uio_cont.GetColumnByName('UOC_DO_10_250').Value)
            self.nr_uio_do_250_500 = self.getFloat(nr_uio_cont.GetColumnByName('UOC_DO_250_500').Value)

            ## Container: UOC_RG_R_UIO_Cont Redundant
            r_uio_cont = Product.GetContainerByName('UOC_RG_UIO_Cont').Rows[1]
            self.r_uio_ai_pts = self.getFloat(r_uio_cont.GetColumnByName('UOC_AI_Points').Value)
            self.r_uio_ao_100_250 = self.getFloat(r_uio_cont.GetColumnByName('UOC_AO_100_250').Value)
            self.r_uio_ao_250_499 = self.getFloat(r_uio_cont.GetColumnByName('UOC_AO_250_499').Value)
            self.r_uio_ao_500 = self.getFloat(r_uio_cont.GetColumnByName('UOC_AO_500').Value)
            self.r_uio_di_pts = self.getFloat(r_uio_cont.GetColumnByName('UOC_DI_Points').Value)
            self.r_uio_do_10_250 = self.getFloat(r_uio_cont.GetColumnByName('UOC_DO_10_250').Value)
            self.r_uio_do_250_500 = self.getFloat(r_uio_cont.GetColumnByName('UOC_DO_250_500').Value)
            self.r_uio_ai_hart_pts = self.getFloat(r_uio_cont.GetColumnByName('UOC_AI_HART_Points').Value)
            self.r_uio_ao_hart_100_250 = self.getFloat(r_uio_cont.GetColumnByName('UOC_AO_HART_100_250').Value)
            self.r_uio_ao_hart_250_499 = self.getFloat(r_uio_cont.GetColumnByName('UOC_AO_HART_250_499').Value)
            self.r_uio_ao_hart_500 = self.getFloat(r_uio_cont.GetColumnByName('UOC_AO_HART_500').Value)

            ## Container: UOC_RG_PF_IO_Cont
            pf_io_cont = Product.GetContainerByName('UOC_RG_PF_IO_Cont').Rows[0]
            self.pf_io_cab_len = pf_io_cont.GetColumnByName('UOC_PF_Cable_Length').Value
            self.pf_io_ai_hart = self.getFloat(pf_io_cont.GetColumnByName('UOC_AI_Hart').Value)
            self.pf_io_ao_hart = self.getFloat(pf_io_cont.GetColumnByName('UOC_AO_Hart').Value)
            self.pf_io_di_cont = self.getFloat(pf_io_cont.GetColumnByName('UOC_DI_Contact').Value)
            self.pf_io_do_points = self.getFloat(pf_io_cont.GetColumnByName('UOC_DO_Points').Value)
            self.pf_io_do_max_load = self.getFloat(pf_io_cont.GetColumnByName('UOC_DO_Max_Load').Value)
            self.pf_io_ai_points = self.getFloat(pf_io_cont.GetColumnByName('UOC_AI_Points').Value)
            self.pf_io_ao_points = self.getFloat(pf_io_cont.GetColumnByName('UOC_AO_Points').Value)

            ## Container: UOC_RG_Other_IO_Cont
            other_io_cont = Product.GetContainerByName('UOC_RG_Other_IO_Cont').Rows[0]
            self.other_io_univ_ai8 = self.getFloat(other_io_cont.GetColumnByName('UOC_Universal_Analog_Input8').Value)
            self.other_io_univ_ai8_tcrtdmvohm = self.getFloat(other_io_cont.GetColumnByName('UOC_Universal_Analog_Input8_TCRTDmVOhm').Value)
            self.other_io_ai16 = self.getFloat(other_io_cont.GetColumnByName('UOC_Analog_Input16').Value)
            self.other_io_ao4 = self.getFloat(other_io_cont.GetColumnByName('UOC_Analog_Output4').Value)
            self.other_io_ao8_intrnl = self.getFloat(other_io_cont.GetColumnByName('UOC_Analog_Output8_Internal').Value)
            self.other_io_ao8_extrnl = self.getFloat(other_io_cont.GetColumnByName('UOC_Analog_Output8_External').Value)
            self.other_io_di32 = self.getFloat(other_io_cont.GetColumnByName('UOC_Digital_Input32').Value)
            self.other_io_di16_120240vac = self.getFloat(other_io_cont.GetColumnByName('UOC_Digital_Input16_120240VAC').Value)
            self.other_io_di_cntct_type16 = self.getFloat(other_io_cont.GetColumnByName('UOC_Digital_Input_Contact_Type16').Value)
            self.other_io_di_16_125vdc = self.getFloat(other_io_cont.GetColumnByName('UOC_Digital_Input16_125VDC').Value)
            self.other_io_do32 = self.getFloat(other_io_cont.GetColumnByName('UOC_Digital_Output32').Value)
            self.other_io_do8 = self.getFloat(other_io_cont.GetColumnByName('UOC_Digital_Output8').Value)
            self.other_io_do_relay8 = self.getFloat(other_io_cont.GetColumnByName('UOC_Digital_Output_Relay8').Value)
            self.other_io_pulseinput_freq4=self.getFloat(other_io_cont.GetColumnByName('UOC_Pulse_Input_Frequency_point4').Value)
            self.ctrl_operating_temp = Product.Attr('UOC_Operating_Temperature').GetValue()