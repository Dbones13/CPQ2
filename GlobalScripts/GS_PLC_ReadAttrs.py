def float_cast(n):
    if n == '' or n is None:
        Log.Write("Invalid argument for cast to float, returned 0.00")
        return float(0)
    else:
        return float(n)

class AttrStorage:
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

        ## Product: PLC System
        elif Product.Name in ["ControlEdge PLC System","ControlEdge PLC System Migration"]:

            self.plc_or_uoc = 'PLC'

            #Inherit attr from parent product
            self.ce_proj_site_volt = Product.Attr('CE_Site_Voltage').GetValue()


            ## Container: PLC_Software_Question_Cont
            plc_soft_q_cont = Product.GetContainerByName('PLC_Software_Question_Cont').Rows[0]
            self.plc_soft_q_soft_release = plc_soft_q_cont.GetColumnByName('PLC_Software_Release').Value
            self.plc_soft_q_med_deliv = plc_soft_q_cont.GetColumnByName('PLC_Media_Delivery').Value
            self.plc_soft_q_ce_build_client = float_cast(plc_soft_q_cont.GetColumnByName('PLC_CE_Builder_Client').Value)
            self.plc_soft_q_mig_tool_usr_lic = float_cast(plc_soft_q_cont.GetColumnByName('PLC_Migration_Tool_User_License').Value)
            self.plc_soft_q_subsea_mdis_intf = float_cast(plc_soft_q_cont.GetColumnByName('PLC_Subsea_MDIS_Interface').Value)
            self.plc_soft_q_cabinet_required = plc_soft_q_cont.GetColumnByName('PLC_Cabinet_Required_Racks_Mounting').Value

            ## Container: PLC_Common_Questions_Cont
            plc_comm_q_cont = Product.GetContainerByName('PLC_Common_Questions_Cont').Rows[0]
            self.plc_comm_q_shielded_term_setup = plc_comm_q_cont.GetColumnByName('PLC_Shielded_Terminal_Strip').Value
            self.plc_comm_q_io_fill_mod = plc_comm_q_cont.GetColumnByName('PLC_IO_Filler_Module').Value
            self.plc_comm_q_io_spare = float_cast(plc_comm_q_cont.GetColumnByName('PLC_IO_Spare').Value)/100
            self.plc_comm_q_io_slot_spare = float_cast(plc_comm_q_cont.GetColumnByName('PLC_IO_Slot_Spare').Value)/100
            #self.plc_comm_q_cabinet_required = plc_comm_q_cont.GetColumnByName('Cabinet_Required_Racks_Mounting').Value
            
            
            ## Container: CE_PLC_System_Hardware
            plc_sys_hardware = Product.GetContainerByName('CE_PLC_System_Hardware').Rows[0]
            self.plc_eng_station_model = plc_sys_hardware.GetColumnByName('PLC_Engineering_Station_Model').Value
            self.plc_eng_station_qty = plc_sys_hardware.GetColumnByName('PLC_Engineering_Station_Qty').Value

            ## Container: PLC_PartSummary_Cont
            #plc_partsumm_cont = Product.GetContainerByName('PLC_PartSummary_Cont').Rows[0]

            ## Container: PLC_ControlGroup_Cont
            #plc_ctrlgrp_cont = Product.GetContainerByName('PLC_ControlGroup_Cont').Rows[0]

        ## Product: PLC Control Group
        elif Product.Name == "CE PLC Control Group":

            self.plc_or_uoc = 'PLC'
            self.cg_or_rg = 'CG'
            
            #Inherit attr from parent product
            self.ce_proj_site_volt = Product.Attr('CE_Site_Voltage').GetValue()
            self.comm_q_io_fill_mod = Product.Attr('PLC_IO_Filler_Module').GetValue()
            self.plc_comm_q_io_spare = float_cast(Product.Attr('PLC_IO_Spare').GetValue())/100
            self.plc_comm_q_io_slot_spare = float_cast(Product.Attr('PLC_IO_Slot_Spare').GetValue())/100
            self.comm_q_shielded_term_setup = Product.Attr('PLC_Shielded_Terminal_Strip').GetValue()
            self.comm_q_cabinet_required = Product.Attr('PLC_Cabinet_Required_Racks_Mounting').GetValue()

            ## Container: PLC_CG_Software_Cont
            if Product.GetContainerByName('PLC_CG_Software_Cont'):
                group_software_cont_count = Product.GetContainerByName('PLC_CG_Software_Cont').Rows.Count
                if group_software_cont_count:
                    group_software_cont = Product.GetContainerByName('PLC_CG_Software_Cont').Rows[0]
                    self.grp_software_ce_elmm_license = float_cast(group_software_cont.GetColumnByName('PLC_CE_ELMM_License').Value)
                    self.grp_software_ce_pl_profinet_usage = float_cast(group_software_cont.GetColumnByName('PLC_CE_PL_Profinet_Usage').Value)

            ## Container: PLC_CG_Cabinet_Cont
            if Product.GetContainerByName('PLC_CG_Cabinet_Cont'):
                cabinet_cont_count=Product.GetContainerByName('PLC_CG_Cabinet_Cont').Rows.Count
                if cabinet_cont_count:
                    cabinet_cont = Product.GetContainerByName('PLC_CG_Cabinet_Cont').Rows[0]
                    self.cabinet_type = cabinet_cont.GetColumnByName('PLC_Cabinet_Type').Value
                    self.cabinet_door_type = cabinet_cont.GetColumnByName('PLC_Cabinet_Door_Type').Value
                    self.cabinet_door_keylock = cabinet_cont.GetColumnByName('PLC_Cabinet_Door_Keylock').Value
                    self.cabinet_base_size = cabinet_cont.GetColumnByName('PLC_Cabinet_Base_Size').Value
                    self.cabinet_pwr_entry = cabinet_cont.GetColumnByName('PLC_Cabinet_Power_Entry').Value
                    self.cabinet_spare_space = float_cast(cabinet_cont.GetColumnByName('PLC_Cabinet_Spare_Space').Value)/100
                    self.cabinet_integ_marshalling = cabinet_cont.GetColumnByName('PLC_Integrated_Marshalling_Cabinet').Value
                    self.cabinet_tstat = cabinet_cont.GetColumnByName('PLC_Cabinet_Thermostat').Value
                    self.cabinet_light = cabinet_cont.GetColumnByName('PLC_Cabinet_Light').Value

            ## Container: PLC_CG_Controller_Rack_Cont
            if Product.GetContainerByName('PLC_CG_Controller_Rack_Cont'):
                ctrl_rack_cont_count = Product.GetContainerByName('PLC_CG_Controller_Rack_Cont').Rows.Count
                if ctrl_rack_cont_count:
                    ctrl_rack_cont = Product.GetContainerByName('PLC_CG_Controller_Rack_Cont').Rows[0]
                    self.ctrl_rack_ctrl_type = ctrl_rack_cont.GetColumnByName('PLC_Controller_Type').Value
                    self.ctrl_rack_io_rack_type = ctrl_rack_cont.GetColumnByName('PLC_IO_Rack_Type').Value
                    self.ctrl_rack_pwr_sply = ctrl_rack_cont.GetColumnByName('PLC_Power_Supply').Value
                    self.ctrl_rack_pwr_input = ctrl_rack_cont.GetColumnByName('PLC_Power_Input').Value
                    self.ctrl_rack_pwr_status_mod_red_sply = ctrl_rack_cont.GetColumnByName('PLC_Power_Status_Mod_Redudant_Supply').Value
                    self.ctrl_rack_field_wire_didoaoai = ctrl_rack_cont.GetColumnByName('PLC_Field_Wiring_DIDOAOAI_Channel_Mod').Value
                    self.ctrl_rack_field_wire_PIFII = ctrl_rack_cont.GetColumnByName('PLC_Field_Wiring_PIFII_Channel_Mod').Value
                    self.ctrl_rack_field_wire_other = ctrl_rack_cont.GetColumnByName('PLC_Field_Wiring_Other_Mod').Value
                    self.ctrl_rack_remote_term_cbl_len = ctrl_rack_cont.GetColumnByName('PLC_Remote_Terminal_Cable_Length').Value
                    self.ctrl_rack_network_topo = ctrl_rack_cont.GetColumnByName('PLC_Network_Topology').Value
                    self.ctrl_rack_ether_swtch_splyr = ctrl_rack_cont.GetColumnByName('PLC_Ethernet_Switch_Supplier').Value
                    self.ctrl_rack_ether_swtch_type = ctrl_rack_cont.GetColumnByName('PLC_Ethernet_Switch_Type').Value
                    self.ctrl_rack_g3_opt_ether_swtch = ctrl_rack_cont.GetColumnByName('PLC_G3_Option_Ethernet_Switch').Value
                    self.ctrl_operating_temp = ctrl_rack_cont.GetColumnByName('PLC_Operating_Temperature').Value

            ## Container: PLC_RG_NR_UIO_Cont Non-Redundant
            if Product.GetContainerByName('PLC_CG_UIO_Cont'):
                nr_uio_cont_Count = Product.GetContainerByName('PLC_CG_UIO_Cont').Rows.Count
                if nr_uio_cont_Count:
                    nr_uio_cont = Product.GetContainerByName('PLC_CG_UIO_Cont').Rows[0]
                    self.nr_uio_ai_pts = float_cast(nr_uio_cont.GetColumnByName('PLC_AI_Points').Value)
                    self.nr_uio_ai_hart_pts = float_cast(nr_uio_cont.GetColumnByName('PLC_AI_HART_Points').Value)
                    self.nr_uio_ao_100_250 = float_cast(nr_uio_cont.GetColumnByName('PLC_AO_100_250').Value)
                    self.nr_uio_ao_250_499 = float_cast(nr_uio_cont.GetColumnByName('PLC_AO_250_499').Value)
                    self.nr_uio_ao_500 = float_cast(nr_uio_cont.GetColumnByName('PLC_AO_500').Value)
                    self.nr_uio_ao_hart_100_250 = float_cast(nr_uio_cont.GetColumnByName('PLC_AO_HART_100_250').Value)
                    self.nr_uio_ao_hart_250_499 = float_cast(nr_uio_cont.GetColumnByName('PLC_AO_HART_250_499').Value)
                    self.nr_uio_ao_hart_500 = float_cast(nr_uio_cont.GetColumnByName('PLC_AO_HART_500').Value)
                    self.nr_uio_di_pts = float_cast(nr_uio_cont.GetColumnByName('PLC_DI_Points').Value)
                    self.nr_uio_do_10_250 = float_cast(nr_uio_cont.GetColumnByName('PLC_DO_10_250').Value)
                    self.nr_uio_do_250_500 = float_cast(nr_uio_cont.GetColumnByName('PLC_DO_250_500').Value)

            ## Container: PLC_RG_R_UIO_Cont Redundant
            if Product.GetContainerByName('PLC_CG_UIO_Cont'):
                r_uio_cont_count = Product.GetContainerByName('PLC_CG_UIO_Cont').Rows.Count
                if r_uio_cont_count:
                    r_uio_cont = Product.GetContainerByName('PLC_CG_UIO_Cont').Rows[1]
                    self.r_uio_ai_pts = float_cast(r_uio_cont.GetColumnByName('PLC_AI_Points').Value)
                    self.r_uio_ao_100_250 = float_cast(r_uio_cont.GetColumnByName('PLC_AO_100_250').Value)
                    self.r_uio_ao_250_499 = float_cast(r_uio_cont.GetColumnByName('PLC_AO_250_499').Value)
                    self.r_uio_ao_500 = float_cast(r_uio_cont.GetColumnByName('PLC_AO_500').Value)
                    self.r_uio_di_pts = float_cast(r_uio_cont.GetColumnByName('PLC_DI_Points').Value)
                    self.r_uio_do_10_250 = float_cast(r_uio_cont.GetColumnByName('PLC_DO_10_250').Value)
                    self.r_uio_do_250_500 = float_cast(r_uio_cont.GetColumnByName('PLC_DO_250_500').Value)
                    self.r_uio_ai_hart_pts = float_cast(r_uio_cont.GetColumnByName('PLC_AI_HART_Points').Value)
                    self.r_uio_ao_hart_100_250 = float_cast(r_uio_cont.GetColumnByName('PLC_AO_HART_100_250').Value)
                    self.r_uio_ao_hart_250_499 = float_cast(r_uio_cont.GetColumnByName('PLC_AO_HART_250_499').Value)
                    self.r_uio_ao_hart_500 = float_cast(r_uio_cont.GetColumnByName('PLC_AO_HART_500').Value)

            ## Container: PLC_CG_Comm_Interface_Cont
            if Product.GetContainerByName('PLC_CG_Comm_Interface_Cont'):
                comm_intf_cont_count= Product.GetContainerByName('PLC_CG_Comm_Interface_Cont').Rows.Count
                if comm_intf_cont_count:
                    comm_intf_cont = Product.GetContainerByName('PLC_CG_Comm_Interface_Cont').Rows[0]
                    self.comm_intf_cda_ctrlrs = float_cast(comm_intf_cont.GetColumnByName('PLC_CDA_Controllers').Value)
                    self.comm_intf_opc_srvrs = float_cast(comm_intf_cont.GetColumnByName('PLC_OPC_Servers').Value)
                    self.comm_intf_opc_clnts = float_cast(comm_intf_cont.GetColumnByName('PLC_OPC_Clients').Value)
                    self.comm_intf_modbus_slvs = float_cast(comm_intf_cont.GetColumnByName('PLC_Modbus_Slaves').Value)
                    self.comm_intf_modbus_mstr = float_cast(comm_intf_cont.GetColumnByName('PLC_Modbus_Master').Value)

            ## Container: PLC_CG_Other_IO_Cont
            if Product.GetContainerByName('PLC_CG_Other_IO_Cont'):
                other_io_cont_count = Product.GetContainerByName('PLC_CG_Other_IO_Cont').Rows.Count
                if other_io_cont_count:
                    other_io_cont = Product.GetContainerByName('PLC_CG_Other_IO_Cont').Rows[0]
                    self.other_io_univ_ai8 = float_cast(other_io_cont.GetColumnByName('PLC_Universal_Analog_Input8').Value)
                    self.other_io_univ_ai8_tcrtdmvohm = float_cast(other_io_cont.GetColumnByName('PLC_Universal_Analog_Input8_TCRTDmVOhm').Value)
                    self.other_io_ai16 = float_cast(other_io_cont.GetColumnByName('PLC_Analog_Input16').Value)
                    self.other_io_ao4 = float_cast(other_io_cont.GetColumnByName('PLC_Analog_Output4').Value)
                    self.other_io_ao8_intrnl = float_cast(other_io_cont.GetColumnByName('PLC_Analog_Output8_Internal').Value)
                    self.other_io_ao8_extrnl = float_cast(other_io_cont.GetColumnByName('PLC_Analog_Output8_External').Value)
                    self.other_io_di32 = float_cast(other_io_cont.GetColumnByName('PLC_Digital_Input32').Value)
                    self.other_io_di16_120240vac = float_cast(other_io_cont.GetColumnByName('PLC_Digital_Input16_120240VAC').Value)
                    self.other_io_di_cntct_type16 = float_cast(other_io_cont.GetColumnByName('PLC_Digital_Input_Contact_Type16').Value)
                    self.other_io_di_16_125vdc = float_cast(other_io_cont.GetColumnByName('PLC_Digital_Input16_125VDC').Value)
                    self.other_io_do32 = float_cast(other_io_cont.GetColumnByName('PLC_Digital_Output32').Value)
                    self.other_io_do8 = float_cast(other_io_cont.GetColumnByName('PLC_Digital_Output8').Value)
                    self.other_io_do_relay8 = float_cast(other_io_cont.GetColumnByName('PLC_Digital_Output_Relay8').Value)
                    self.other_io_pulse_inp_freq_inp4 = float_cast(other_io_cont.GetColumnByName('PLC_Pulse_Input_Freq_Input4').Value)
                    self.other_io_quad_inp = float_cast(other_io_cont.GetColumnByName('PLC_Quadrature_Input').Value)
                    self.other_io_pulse_outp4 = float_cast(other_io_cont.GetColumnByName('PLC_Pulse_Output4').Value)
                    self.other_io_comm_intf_mod_485232 = float_cast(other_io_cont.GetColumnByName('PLC_Communication_Interface_Mod_485232').Value)

            ## Container: PLC_CG_Additional_Controller_Cont
            if Product.GetContainerByName('PLC_CG_Additional_Controller_Cont'):
                addl_ctrlr_cont_count = Product.GetContainerByName('PLC_CG_Additional_Controller_Cont').Rows.Count
                if addl_ctrlr_cont_count:
                    addl_ctrlr_cont = Product.GetContainerByName('PLC_CG_Additional_Controller_Cont').Rows[0]
                    self.addl_ctrlr_2_pos_term_brd_jmprs = float_cast(addl_ctrlr_cont.GetColumnByName('PLC_Two_Pos_Terminal_Board_Jumpers').Value)
                    self.addl_ctrlr_10_pos_term_brd_jmprs = float_cast(addl_ctrlr_cont.GetColumnByName('PLC_Ten_Pos_Terminal_Board_Jumpers').Value)
                    self.addl_ctrlr_mimp_250ohm_resis_kit = float_cast(addl_ctrlr_cont.GetColumnByName('PLC_MIMP_250Ohm_Resistor_Kit').Value)
                    self.addl_ctrlr_io_mod_label_kit = float_cast(addl_ctrlr_cont.GetColumnByName('PLC_IO_Mod_Label_Kit').Value)
                    self.addl_ctrlr_fib_opt_conv_multi = float_cast(addl_ctrlr_cont.GetColumnByName('PLC_Fiber_Optic_Converter_Multi').Value)
                    self.addl_ctrlr_fib_opt_conv_single = float_cast(addl_ctrlr_cont.GetColumnByName('PLC_Fiber_Optic_Converter_Single').Value)
                    self.addl_ctrlr_fib_opt_conv_multi_g3 = float_cast(addl_ctrlr_cont.GetColumnByName('PLC_Fiber_Optic_Converter_Multi_G3').Value)
                    #self.addl_ctrlr_fib_opt_conv_single_g3 = float_cast(addl_ctrlr_cont.GetColumnByName('PLC_Fiber_Optic_Converter_Single_G3').Value)
                    #self.addl_ctrlr_addl_ctrlr = float_cast(addl_ctrlr_cont.GetColumnByName('PLC_Additonal_Controller').Value)

        ## Product: PLC Remote Group
        elif Product.Name == "CE PLC Remote Group":
        
            self.plc_or_uoc = 'PLC'
            self.cg_or_rg = 'RG'

            #Inherit attr from parent product
            self.ce_proj_site_volt = Product.Attr('CE_Site_Voltage').GetValue()
            self.comm_q_io_fill_mod = Product.Attr('PLC_IO_Filler_Module').GetValue()
            self.plc_comm_q_io_spare = float_cast(Product.Attr('PLC_IO_Spare').GetValue())/100
            self.plc_comm_q_io_slot_spare = float_cast(Product.Attr('PLC_IO_Slot_Spare').GetValue())/100
            self.comm_q_shielded_term_setup = Product.Attr('PLC_Shielded_Terminal_Strip').GetValue()
            self.comm_q_cabinet_required = Product.Attr('PLC_Cabinet_Required_Racks_Mounting').GetValue()

            ## Container: PLC_RG_Cabinet_Cont
            cabinet_cont = Product.GetContainerByName('PLC_RG_Cabinet_Cont').Rows[0]
            self.cabinet_type = cabinet_cont.GetColumnByName('PLC_Cabinet_Type').Value
            self.cabinet_door_type = cabinet_cont.GetColumnByName('PLC_Cabinet_Door_Type').Value
            self.cabinet_door_keylock = cabinet_cont.GetColumnByName('PLC_Cabinet_Door_Keylock').Value
            self.cabinet_base_size = cabinet_cont.GetColumnByName('PLC_Cabinet_Base_Size').Value
            self.cabinet_pwr_entry = cabinet_cont.GetColumnByName('PLC_Cabinet_Power_Entry').Value
            self.cabinet_spare_space = float_cast(cabinet_cont.GetColumnByName('PLC_Cabinet_Spare_Space').Value)/100
            self.cabinet_integ_marshalling = cabinet_cont.GetColumnByName('PLC_Integrated_Marshalling_Cabinet').Value
            self.cabinet_tstat = cabinet_cont.GetColumnByName('PLC_Cabinet_Thermostat').Value
            self.cabinet_light = cabinet_cont.GetColumnByName('PLC_Cabinet_Light').Value

            ## Container: PLC_RG_Controller_Rack_Cont
            ctrl_rack_cont = Product.GetContainerByName('PLC_RG_Controller_Rack_Cont').Rows[0]
            self.ctrl_rack_io_rack_type = ctrl_rack_cont.GetColumnByName('PLC_IO_Rack_Type').Value
            self.ctrl_rack_pwr_sply = ctrl_rack_cont.GetColumnByName('PLC_Power_Supply').Value
            self.ctrl_rack_pwr_input = ctrl_rack_cont.GetColumnByName('PLC_Power_Input').Value
            self.ctrl_rack_pwr_status_mod_red_sply = ctrl_rack_cont.GetColumnByName('PLC_Power_Status_Mod_Redudant_Supply').Value
            self.ctrl_rack_field_wire_didoaoai = ctrl_rack_cont.GetColumnByName('PLC_Field_Wiring_DIDOAOAI_Channel_Mod').Value
            self.ctrl_rack_field_wire_PIFII = ctrl_rack_cont.GetColumnByName('PLC_Field_Wiring_PIFII_Channel_Mod').Value
            self.ctrl_rack_field_wire_other = ctrl_rack_cont.GetColumnByName('PLC_Field_Wiring_Other_Mod').Value
            self.ctrl_rack_remote_term_cbl_len = ctrl_rack_cont.GetColumnByName('PLC_Remote_Terminal_Cable_Length').Value

            ## Container: PLC_RG_NR_UIO_Cont Non-Redundant
            nr_uio_cont = Product.GetContainerByName('PLC_RG_UIO_Cont').Rows[0]
            self.nr_uio_ai_pts = float_cast(nr_uio_cont.GetColumnByName('PLC_AI_Points').Value)
            self.nr_uio_ai_hart_pts = float_cast(nr_uio_cont.GetColumnByName('PLC_AI_HART_Points').Value)
            self.nr_uio_ao_100_250 = float_cast(nr_uio_cont.GetColumnByName('PLC_AO_100_250').Value)
            self.nr_uio_ao_250_499 = float_cast(nr_uio_cont.GetColumnByName('PLC_AO_250_499').Value)
            self.nr_uio_ao_500 = float_cast(nr_uio_cont.GetColumnByName('PLC_AO_500').Value)
            self.nr_uio_ao_hart_100_250 = float_cast(nr_uio_cont.GetColumnByName('PLC_AO_HART_100_250').Value)
            self.nr_uio_ao_hart_250_499 = float_cast(nr_uio_cont.GetColumnByName('PLC_AO_HART_250_499').Value)
            self.nr_uio_ao_hart_500 = float_cast(nr_uio_cont.GetColumnByName('PLC_AO_HART_500').Value)
            self.nr_uio_di_pts = float_cast(nr_uio_cont.GetColumnByName('PLC_DI_Points').Value)
            self.nr_uio_do_10_250 = float_cast(nr_uio_cont.GetColumnByName('PLC_DO_10_250').Value)
            self.nr_uio_do_250_500 = float_cast(nr_uio_cont.GetColumnByName('PLC_DO_250_500').Value)

            ## Container: PLC_RG_R_UIO_Cont Redundant
            r_uio_cont = Product.GetContainerByName('PLC_RG_UIO_Cont').Rows[1]
            self.r_uio_ai_pts = float_cast(r_uio_cont.GetColumnByName('PLC_AI_Points').Value)
            self.r_uio_ao_100_250 = float_cast(r_uio_cont.GetColumnByName('PLC_AO_100_250').Value)
            self.r_uio_ao_250_499 = float_cast(r_uio_cont.GetColumnByName('PLC_AO_250_499').Value)
            self.r_uio_ao_500 = float_cast(r_uio_cont.GetColumnByName('PLC_AO_500').Value)
            self.r_uio_di_pts = float_cast(r_uio_cont.GetColumnByName('PLC_DI_Points').Value)
            self.r_uio_do_10_250 = float_cast(r_uio_cont.GetColumnByName('PLC_DO_10_250').Value)
            self.r_uio_do_250_500 = float_cast(r_uio_cont.GetColumnByName('PLC_DO_250_500').Value)
            self.r_uio_ai_hart_pts = float_cast(r_uio_cont.GetColumnByName('PLC_AI_HART_Points').Value)
            self.r_uio_ao_hart_100_250 = float_cast(r_uio_cont.GetColumnByName('PLC_AO_HART_100_250').Value)
            self.r_uio_ao_hart_250_499 = float_cast(r_uio_cont.GetColumnByName('PLC_AO_HART_250_499').Value)
            self.r_uio_ao_hart_500 = float_cast(r_uio_cont.GetColumnByName('PLC_AO_HART_500').Value)

            ## Container: PLC_RG_Comm_Interface_Cont
            comm_intf_cont = Product.GetContainerByName('PLC_RG_Comm_Interface_Cont').Rows[0]
            self.comm_intf_cda_ctrlrs = float_cast(comm_intf_cont.GetColumnByName('PLC_CDA_Controllers').Value)
            self.comm_intf_opc_srvrs = float_cast(comm_intf_cont.GetColumnByName('PLC_OPC_Servers').Value)
            self.comm_intf_opc_clnts = float_cast(comm_intf_cont.GetColumnByName('PLC_OPC_Clients').Value)
            self.comm_intf_modbus_slvs = float_cast(comm_intf_cont.GetColumnByName('PLC_Modbus_Slaves').Value)
            self.comm_intf_modbus_mstr = float_cast(comm_intf_cont.GetColumnByName('PLC_Modbus_Master').Value)

            ## Container: PLC_RG_Other_IO_Cont
            other_io_cont = Product.GetContainerByName('PLC_RG_Other_IO_Cont').Rows[0]
            self.other_io_univ_ai8 = float_cast(other_io_cont.GetColumnByName('PLC_Universal_Analog_Input8').Value)
            self.other_io_univ_ai8_tcrtdmvohm = float_cast(other_io_cont.GetColumnByName('PLC_Universal_Analog_Input8_TCRTDmVOhm').Value)
            self.other_io_ai16 = float_cast(other_io_cont.GetColumnByName('PLC_Analog_Input16').Value)
            self.other_io_ao4 = float_cast(other_io_cont.GetColumnByName('PLC_Analog_Output4').Value)
            self.other_io_ao8_intrnl = float_cast(other_io_cont.GetColumnByName('PLC_Analog_Output8_Internal').Value)
            self.other_io_ao8_extrnl = float_cast(other_io_cont.GetColumnByName('PLC_Analog_Output8_External').Value)
            self.other_io_di32 = float_cast(other_io_cont.GetColumnByName('PLC_Digital_Input32').Value)
            self.other_io_di16_120240vac = float_cast(other_io_cont.GetColumnByName('PLC_Digital_Input16_120240VAC').Value)
            self.other_io_di_cntct_type16 = float_cast(other_io_cont.GetColumnByName('PLC_Digital_Input_Contact_Type16').Value)
            self.other_io_di_16_125vdc = float_cast(other_io_cont.GetColumnByName('PLC_Digital_Input16_125VDC').Value)
            self.other_io_do32 = float_cast(other_io_cont.GetColumnByName('PLC_Digital_Output32').Value)
            self.other_io_do8 = float_cast(other_io_cont.GetColumnByName('PLC_Digital_Output8').Value)
            self.other_io_do_relay8 = float_cast(other_io_cont.GetColumnByName('PLC_Digital_Output_Relay8').Value)
            self.other_io_pulse_inp_freq_inp4 = float_cast(other_io_cont.GetColumnByName('PLC_Pulse_Input_Freq_Input4').Value)
            self.other_io_quad_inp = float_cast(other_io_cont.GetColumnByName('PLC_Quadrature_Input').Value)
            self.other_io_pulse_outp4 = float_cast(other_io_cont.GetColumnByName('PLC_Pulse_Output4').Value)
            self.other_io_comm_intf_mod_485232 = float_cast(other_io_cont.GetColumnByName('PLC_Communication_Interface_Mod_485232').Value)

            ## Container: PLC_RG_Additional_Controller_Cont
            addl_ctrlr_cont = Product.GetContainerByName('PLC_RG_Additional_Controller_Cont').Rows[0]
            self.addl_ctrlr_2_pos_term_brd_jmprs = float_cast(addl_ctrlr_cont.GetColumnByName('PLC_Two_Pos_Terminal_Board_Jumpers').Value)
            self.addl_ctrlr_10_pos_term_brd_jmprs = float_cast(addl_ctrlr_cont.GetColumnByName('PLC_Ten_Pos_Terminal_Board_Jumpers').Value)
            self.addl_ctrlr_mimp_250ohm_resis_kit = float_cast(addl_ctrlr_cont.GetColumnByName('PLC_MIMP_250Ohm_Resistor_Kit').Value)
            self.addl_ctrlr_io_mod_label_kit = float_cast(addl_ctrlr_cont.GetColumnByName('PLC_IO_Mod_Label_Kit').Value)
            self.addl_ctrlr_fib_opt_conv_multi = float_cast(addl_ctrlr_cont.GetColumnByName('PLC_Fiber_Optic_Converter_Multi').Value)
            self.addl_ctrlr_fib_opt_conv_single = float_cast(addl_ctrlr_cont.GetColumnByName('PLC_Fiber_Optic_Converter_Single').Value)
            self.addl_ctrlr_fib_opt_conv_multi_g3 = float_cast(addl_ctrlr_cont.GetColumnByName('PLC_Fiber_Optic_Converter_Multi_G3').Value)
            self.addl_ctrlr_fib_opt_conv_single_g3 = float_cast(addl_ctrlr_cont.GetColumnByName('PLC_Fiber_Optic_Converter_Single_G3').Value)
            #self.addl_ctrlr_addl_ctrlr = float_cast(addl_ctrlr_cont.GetColumnByName('PLC_Additonal_Controller').Value)
            
            self.ctrl_operating_temp = Product.Attr('PLC_Operating_Temperature').GetValue()