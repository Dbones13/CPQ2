import math as m
class AttrStorage:
    def get_column_value(self, row, col):
        return row.GetColumnByName(col).Value
        Trace.Write(row.GetColumnByName(col).Value)
    def __init__(self, Product):
        if Product.Name=="SM Control Group":
            Marshalling_Option = Product.GetContainerByName('SM_CG_Cabinet_Details_Cont_Left').Rows[0].GetColumnByName('Marshalling_Option').DisplayValue
            if Marshalling_Option =="Universal Marshalling":
                # CONTROL GROUP LEVEL
                #CXCPQ-CXCPQ-30864
                #AI
                try:
                    self.sai1_uio_nrd_nis = Product.GetContainerByName('SM_IO_Count_Analog_Input_Cont').Rows[0].GetColumnByName('Non Red (NIS)').Value
                except:
                    self.sai1_uio_nrd_nis = 0
                try:
                    self.sai1_fire2_wire_uio_nrd_nis = Product.GetContainerByName('SM_IO_Count_Analog_Input_Cont').Rows[1].GetColumnByName('Non Red (NIS)').Value
                except:
                    self.sai1_fire2_wire_uio_nrd_nis = 0
                try:
                    self.sai1_fire34_wire_uio_nrd_nis = Product.GetContainerByName('SM_IO_Count_Analog_Input_Cont').Rows[2].GetColumnByName('Non Red (NIS)').Value
                except:
                    self.sai1_fire34_wire_uio_nrd_nis = 0
                try:
                    self.sai1_fire34_wire_sink_uio_nrd_nis = Product.GetContainerByName('SM_IO_Count_Analog_Input_Cont').Rows[3].GetColumnByName('Non Red (NIS)').Value
                except:
                    self.sai1_fire34_wire_sink_uio_nrd_nis = 0
                try:
                    self.sai1_gas_uio_nrd_nis = Product.GetContainerByName('SM_IO_Count_Analog_Input_Cont').Rows[4].GetColumnByName('Non Red (NIS)').Value
                except:
                    self.sai1_gas_uio_nrd_nis = 0
                #AO
                try:
                    self.sao1_uio_nrd_nis = Product.GetContainerByName('SM_IO_Count_Analog_Output_Cont').Rows[0].GetColumnByName('Non Red (NIS)').Value
                except:
                    self.sao1_uio_nrd_nis = 0
                #DI
                try:
                    self.percent_spare_io = Product.GetContainerByName('SM_CG_Cabinet_Details_Cont_Right').Rows[0].GetColumnByName('Percent_Installed_Spare_IOs').Value
                except:
                    self.percent_spare_io = 0
                try:
                    self.sdi1_uio_nrd_nis = Product.GetContainerByName('SM_IO_Count_Digital_Input_Cont').Rows[0].GetColumnByName('Non Red (NIS)').Value
                except:
                    self.sdi1_uio_nrd_nis = 0
                try:
                    self.sdi1_line_mon_uio_nrd_nis = Product.GetContainerByName('SM_IO_Count_Digital_Input_Cont').Rows[1].GetColumnByName('Non Red (NIS)').Value
                except:
                    self.sdi1_line_mon_uio_nrd_nis = 0
                try:
                    self.sdi1_5k_resistor_uio_nrd_nis = Product.GetContainerByName('SM_IO_Count_Digital_Input_Cont').Rows[2].GetColumnByName('Non Red (NIS)').Value
                except:
                    self.sdi1_5k_resistor_uio_nrd_nis = 0
                #DO
                try:
                    self.sdo1_uio_nrd_nis = Product.GetContainerByName('SM_IO_Count_Digital_Output_Cont').Rows[0].GetColumnByName('Non Red (NIS)').Value
                except:
                    self.sdo1_uio_nrd_nis = 0
                try:
                    self.sdo7_line_mon_uio_nrd_nis = Product.GetContainerByName('SM_IO_Count_Digital_Output_Cont').Rows[1].GetColumnByName('Non Red (NIS)').Value
                except:
                    self.sdo7_line_mon_uio_nrd_nis = 0
                try:
                    self.sdo16_sil23_uio_nrd_nis = Product.GetContainerByName('SM_IO_Count_Digital_Output_Cont').Rows[2].GetColumnByName('Non Red (NIS)').Value
                except:
                    self.sdo16_sil23_uio_nrd_nis = 0
                try:
                    self.sdo12_sil23_com_uio_nrd_nis = Product.GetContainerByName('SM_IO_Count_Digital_Output_Cont').Rows[3].GetColumnByName('Non Red (NIS)').Value
                except:
                    self.sdo12_sil23_com_uio_nrd_nis = 0
                #NR Relay
                try:
                    self.sdi1_uio_nrd_rly = Product.GetContainerByName('SM_IO_Count_Digital_Input_Cont').Rows[0].GetColumnByName('Non Red (RLY)').Value
                except:
                    self.sdi1_uio_nrd_rly = 0
                try:
                    self.sdo1_uio_nrd_rly = Product.GetContainerByName('SM_IO_Count_Digital_Output_Cont').Rows[0].GetColumnByName('Non Red (RLY)').Value
                except:
                    self.sdo1_uio_nrd_rly = 0
                # Non REd SIL 2 RLY
                try:
                    self.sdo1_uio_nrd_sil2_rly = Product.GetContainerByName('SM_CG_DO_RLY_NMR_Cont').Rows[0].GetColumnByName('Non_Red_SIL2_RLY').Value
                except:
                    self.sdo1_uio_nrd_sil2_rly = 0
                # Non REd SIL 3 RLY
                try:
                    self.sdi1_uio_nrd_sil3_rly = Product.GetContainerByName('SM_CG_DI_RLY_NMR_Cont').Rows[0].GetColumnByName('Non_Red_SIL3_RLY').Value
                except:
                    self.sdi1_uio_nrd_sil3_rly = 0
                try:
                    self.sdo1_uio_nrd_sil3_rly = Product.GetContainerByName('SM_CG_DO_RLY_NMR_Cont').Rows[0].GetColumnByName('Non_Red_SIL3_RLY').Value
                except:
                    self.sdo1_uio_nrd_sil3_rly = 0
                 # Non REd nmr
                try:
                    self.sdi1_uio_nrd_nmr = Product.GetContainerByName('SM_CG_DI_RLY_NMR_Cont').Rows[0].GetColumnByName('Non_Red_NMR').Value
                except:
                    self.sdi1_uio_nrd_nmr =0
                # Non REd NMR Safety
                try:
                    self.sdi1_uio_nrd_nmr_safety = Product.GetContainerByName('SM_CG_DI_RLY_NMR_Cont').Rows[0].GetColumnByName('Non_Red_NMR_Safety').Value
                except:
                    self.sdi1_uio_nrd_nmr_safety = 0
            elif Marshalling_Option =="Hardware Marshalling with P+F":
                #AI
                try:
                    self.sai1_uio_nrd_nis = Product.GetContainerByName('SM_IO_Count_Analog_Input_Cont').Rows[0].GetColumnByName('Non Red (NIS)').Value
                except:
                    self.sai1_uio_nrd_nis = 0
                try:
                    self.sai1_fire2_wire_uio_nrd_nis = Product.GetContainerByName('SM_IO_Count_Analog_Input_Cont').Rows[2].GetColumnByName('Non Red (NIS)').Value
                except:
                    self.sai1_fire2_wire_uio_nrd_nis = 0
                try:
                    self.sai1_fire34_wire_uio_nrd_nis = Product.GetContainerByName('SM_IO_Count_Analog_Input_Cont').Rows[3].GetColumnByName('Non Red (NIS)').Value
                except:
                    self.sai1_fire34_wire_uio_nrd_nis = 0
                try:
                    self.sai1_fire34_wire_sink_uio_nrd_nis = Product.GetContainerByName('SM_IO_Count_Analog_Input_Cont').Rows[1].GetColumnByName('Non Red (NIS)').Value
                except:
                    self.sai1_fire34_wire_sink_uio_nrd_nis = 0
                try:
                    self.sai1_gas_uio_nrd_nis = Product.GetContainerByName('SM_IO_Count_Analog_Input_Cont').Rows[4].GetColumnByName('Non Red (NIS)').Value
                except:
                    self.sai1_gas_uio_nrd_nis = 0
                #AO
                try:
                    self.sao1_uio_nrd_nis = Product.GetContainerByName('SM_IO_Count_Analog_Output_Cont').Rows[0].GetColumnByName('Non Red (NIS)').Value
                except:
                    self.sao1_uio_nrd_nis = 0
                #DI
                try:
                    self.percent_spare_io = Product.GetContainerByName('SM_CG_Cabinet_Details_Cont_Right').Rows[0].GetColumnByName('Percent_Installed_Spare_IOs').Value
                except:
                    self.percent_spare_io = 0
                try:
                    self.sdi1_uio_nrd_nis = Product.GetContainerByName('SM_IO_Count_Digital_Input_Cont').Rows[0].GetColumnByName('Non Red (NIS)').Value
                except:
                    self.sdi1_uio_nrd_nis = 0
                try:
                    self.sdi1_line_mon_uio_nrd_nis = Product.GetContainerByName('SM_IO_Count_Digital_Input_Cont').Rows[3].GetColumnByName('Non Red (NIS)').Value
                except:
                    self.sdi1_line_mon_uio_nrd_nis = 0
                try:
                    self.sdi1_5k_resistor_uio_nrd_nis = Product.GetContainerByName('SM_IO_Count_Digital_Input_Cont').Rows[2].GetColumnByName('Non Red (NIS)').Value
                except:
                    self.sdi1_5k_resistor_uio_nrd_nis = 0
                #DO
                try:
                    self.sdo1_uio_nrd_nis = Product.GetContainerByName('SM_IO_Count_Digital_Output_Cont').Rows[0].GetColumnByName('Non Red (NIS)').Value
                except:
                    self.sdo1_uio_nrd_nis = 0
                try:
                    self.sdo7_line_mon_uio_nrd_nis = Product.GetContainerByName('SM_IO_Count_Digital_Output_Cont').Rows[2].GetColumnByName('Non Red (NIS)').Value
                except:
                    self.sdo7_line_mon_uio_nrd_nis = 0
                try:
                    self.sdo16_sil23_uio_nrd_nis = Product.GetContainerByName('SM_IO_Count_Digital_Output_Cont').Rows[3].GetColumnByName('Non Red (NIS)').Value
                except:
                    self.sdo16_sil23_uio_nrd_nis = 0
                try:
                    self.sdo12_sil23_com_uio_nrd_nis = Product.GetContainerByName('SM_IO_Count_Digital_Output_Cont').Rows[4].GetColumnByName('Non Red (NIS)').Value
                except:
                    self.sdo12_sil23_com_uio_nrd_nis = 0
                #NR Relay
                try:
                    self.sdi1_uio_nrd_rly = Product.GetContainerByName('SM_IO_Count_Digital_Input_Cont').Rows[0].GetColumnByName('Non Red (RLY)').Value
                except:
                    self.sdi1_uio_nrd_rly = 0
                try:
                    self.sdo1_uio_nrd_rly = Product.GetContainerByName('SM_IO_Count_Digital_Output_Cont').Rows[0].GetColumnByName('Non Red (RLY)').Value
                except:
                    self.sdo1_uio_nrd_rly = 0
                # Non REd SIL 2 RLY
                try:
                    self.sdo1_uio_nrd_sil2_rly = Product.GetContainerByName('SM_CG_DO_RLY_NMR_Cont').Rows[0].GetColumnByName('Non_Red_SIL2_RLY').Value
                except:
                    self.sdo1_uio_nrd_sil2_rly = 0
                # Non REd SIL 3 RLY
                try:
                    self.sdi1_uio_nrd_sil3_rly = Product.GetContainerByName('SM_CG_DI_RLY_NMR_Cont').Rows[0].GetColumnByName('Non_Red_SIL3_RLY').Value
                except:
                    self.sdi1_uio_nrd_sil3_rly = 0
                try:
                    self.sdo1_uio_nrd_sil3_rly = Product.GetContainerByName('SM_CG_DO_RLY_NMR_Cont').Rows[0].GetColumnByName('Non_Red_SIL3_RLY').Value
                except:
                    self.sdo1_uio_nrd_sil3_rly = 0
                 # Non REd nmr
                try:
                    self.sdi1_uio_nrd_nmr = Product.GetContainerByName('SM_CG_DI_RLY_NMR_Cont').Rows[0].GetColumnByName('Non_Red_NMR').Value
                except:
                    self.sdi1_uio_nrd_nmr =0
                # Non REd NMR Safety
                try:
                    self.sdi1_uio_nrd_nmr_safety = Product.GetContainerByName('SM_CG_DI_RLY_NMR_Cont').Rows[0].GetColumnByName('Non_Red_NMR_Safety').Value
                except:
                    self.sdi1_uio_nrd_nmr_safety = 0
            elif Marshalling_Option =="Hardware Marshalling with Other":
                #AI
                try:
                    self.sai1_uio_nrd_nis = Product.GetContainerByName('SM_IO_Count_Analog_Input_Cont').Rows[0].GetColumnByName('Non Red (NIS)').Value
                except:
                    self.sai1_uio_nrd_nis = 0
                try:
                    self.sai1_fire2_wire_uio_nrd_nis = Product.GetContainerByName('SM_IO_Count_Analog_Input_Cont').Rows[1].GetColumnByName('Non Red (NIS)').Value
                except:
                    self.sai1_fire2_wire_uio_nrd_nis = 0
                try:
                    self.sai1_fire34_wire_uio_nrd_nis = Product.GetContainerByName('SM_IO_Count_Analog_Input_Cont').Rows[2].GetColumnByName('Non Red (NIS)').Value
                except:
                    self.sai1_fire34_wire_uio_nrd_nis = 0
                try:
                    self.sai1_fire34_wire_sink_uio_nrd_nis = Product.GetContainerByName('SM_IO_Count_Analog_Input_Cont').Rows[5].GetColumnByName('Non Red (NIS)').Value
                except:
                    self.sai1_fire34_wire_sink_uio_nrd_nis = 0
                try:
                    self.sai1_gas_uio_nrd_nis = Product.GetContainerByName('SM_IO_Count_Analog_Input_Cont').Rows[3].GetColumnByName('Non Red (NIS)').Value
                except:
                    self.sai1_gas_uio_nrd_nis = 0
                #AO
                try:
                    self.sao1_uio_nrd_nis = Product.GetContainerByName('SM_IO_Count_Analog_Output_Cont').Rows[0].GetColumnByName('Non Red (NIS)').Value
                except:
                    self.sao1_uio_nrd_nis = 0
                #DI
                try:
                    self.percent_spare_io = Product.GetContainerByName('SM_CG_Cabinet_Details_Cont_Right').Rows[0].GetColumnByName('Percent_Installed_Spare_IOs').Value
                except:
                    self.percent_spare_io = 0
                try:
                    self.sdi1_uio_nrd_nis = Product.GetContainerByName('SM_IO_Count_Digital_Input_Cont').Rows[0].GetColumnByName('Non Red (NIS)').Value
                except:
                    self.sdi1_uio_nrd_nis = 0
                try:
                    self.sdi1_line_mon_uio_nrd_nis = Product.GetContainerByName('SM_IO_Count_Digital_Input_Cont').Rows[1].GetColumnByName('Non Red (NIS)').Value
                except:
                    self.sdi1_line_mon_uio_nrd_nis = 0
                try:
                    self.sdi1_5k_resistor_uio_nrd_nis = Product.GetContainerByName('SM_IO_Count_Digital_Input_Cont').Rows[5].GetColumnByName('Non Red (NIS)').Value
                except:
                    self.sdi1_5k_resistor_uio_nrd_nis = 0
                #DO
                try:
                    self.sdo1_uio_nrd_nis = Product.GetContainerByName('SM_IO_Count_Digital_Output_Cont').Rows[0].GetColumnByName('Non Red (NIS)').Value
                except:
                    self.sdo1_uio_nrd_nis = 0
                try:
                    self.sdo7_line_mon_uio_nrd_nis = Product.GetContainerByName('SM_IO_Count_Digital_Output_Cont').Rows[1].GetColumnByName('Non Red (NIS)').Value
                except:
                    self.sdo7_line_mon_uio_nrd_nis = 0
                try:
                    self.sdo16_sil23_uio_nrd_nis = Product.GetContainerByName('SM_IO_Count_Digital_Output_Cont').Rows[2].GetColumnByName('Non Red (NIS)').Value
                except:
                    self.sdo16_sil23_uio_nrd_nis = 0
                try:
                    self.sdo12_sil23_com_uio_nrd_nis = Product.GetContainerByName('SM_IO_Count_Digital_Output_Cont').Rows[3].GetColumnByName('Non Red (NIS)').Value
                except:
                    self.sdo12_sil23_com_uio_nrd_nis = 0
                #NR Relay
                try:
                    self.sdi1_uio_nrd_rly = Product.GetContainerByName('SM_IO_Count_Digital_Input_Cont').Rows[0].GetColumnByName('Non Red (RLY)').Value
                except:
                    self.sdi1_uio_nrd_rly = 0
                try:
                    self.sdo1_uio_nrd_rly = Product.GetContainerByName('SM_IO_Count_Digital_Output_Cont').Rows[0].GetColumnByName('Non Red (RLY)').Value
                except:
                    self.sdo1_uio_nrd_rly = 0
                # Non REd SIL 2 RLY
                try:
                    self.sdo1_uio_nrd_sil2_rly = Product.GetContainerByName('SM_CG_DO_RLY_NMR_Cont').Rows[0].GetColumnByName('Non_Red_SIL2_RLY').Value
                except:
                    self.sdo1_uio_nrd_sil2_rly = 0
                # Non REd SIL 3 RLY
                try:
                    self.sdi1_uio_nrd_sil3_rly = Product.GetContainerByName('SM_CG_DI_RLY_NMR_Cont').Rows[0].GetColumnByName('Non_Red_SIL3_RLY').Value
                except:
                    self.sdi1_uio_nrd_sil3_rly = 0
                try:
                    self.sdo1_uio_nrd_sil3_rly = Product.GetContainerByName('SM_CG_DO_RLY_NMR_Cont').Rows[0].GetColumnByName('Non_Red_SIL3_RLY').Value
                except:
                    self.sdo1_uio_nrd_sil3_rly = 0
                 # Non REd nmr
                try:
                    self.sdi1_uio_nrd_nmr = Product.GetContainerByName('SM_CG_DI_RLY_NMR_Cont').Rows[0].GetColumnByName('Non_Red_NMR').Value
                except:
                    self.sdi1_uio_nrd_nmr =0
                # Non REd NMR Safety
                try:
                    self.sdi1_uio_nrd_nmr_safety = Product.GetContainerByName('SM_CG_DI_RLY_NMR_Cont').Rows[0].GetColumnByName('Non_Red_NMR_Safety').Value
                except:
                    self.sdi1_uio_nrd_nmr_safety = 0

        if Product.Name=="SM Remote Group":
            Enclosure_Type = Product.GetContainerByName('SM_RG_ATEX Compliance_and_Enclosure_Type_Cont').Rows[0].GetColumnByName('Enclosure_Type').DisplayValue
            if Enclosure_Type == "Cabinet":
                Marshalling_Option = Product.GetContainerByName('SM_RG_Cabinet_Details_Cont_Left').Rows[0].GetColumnByName('Marshalling_Option').DisplayValue
                if Marshalling_Option =="Universal Marshalling":
                    #CXCPQ-CXCPQ-30864
                    try:
                        self.percent_spare_io = Product.GetContainerByName('SM_RG_Cabinet_Details_Cont').Rows[0].GetColumnByName('SM_Percent_Installed_Spare_IO').Value
                    except:
                        self.percent_spare_io = 0
                    #AI
                    try:
                        self.sai1_uio_nrd_nis = Product.GetContainerByName('SM_RG_IO_Count_Analog_Input_Cont').Rows[0].GetColumnByName('Non_Red_NIS').Value
                    except:
                        self.sai1_uio_nrd_nis = 0
                    try:
                        self.sai1_fire2_wire_uio_nrd_nis = Product.GetContainerByName('SM_RG_IO_Count_Analog_Input_Cont').Rows[1].GetColumnByName('Non_Red_NIS').Value
                    except:
                        self.sai1_fire2_wire_uio_nrd_nis = 0
                    try:
                        self.sai1_fire34_wire_uio_nrd_nis = Product.GetContainerByName('SM_RG_IO_Count_Analog_Input_Cont').Rows[2].GetColumnByName('Non_Red_NIS').Value
                    except:
                        self.sai1_fire34_wire_uio_nrd_nis = 0
                    try:
                        self.sai1_fire34_wire_sink_uio_nrd_nis = Product.GetContainerByName('SM_RG_IO_Count_Analog_Input_Cont').Rows[3].GetColumnByName('Non_Red_NIS').Value
                    except:
                        self.sai1_fire34_wire_sink_uio_nrd_nis = 0
                    try:
                        self.sai1_gas_uio_nrd_nis = Product.GetContainerByName('SM_RG_IO_Count_Analog_Input_Cont').Rows[4].GetColumnByName('Non_Red_NIS').Value
                    except:
                        self.sai1_gas_uio_nrd_nis = 0
                    #AO
                    try:
                        self.sao1_uio_nrd_nis = Product.GetContainerByName('SM_RG_IO_Count_Analog_Output_Cont').Rows[0].GetColumnByName('Non_Red_NIS').Value
                    except:
                        self.sao1_uio_nrd_nis = 0
                    #DI
                    try:
                        self.sdi1_uio_nrd_nis = Product.GetContainerByName('SM_RG_IO_Count_Digital_Input_Cont').Rows[0].GetColumnByName('Non_Red_NIS').Value
                    except:
                        self.sdi1_uio_nrd_nis = 0
                    try:
                        self.sdi1_line_mon_uio_nrd_nis = Product.GetContainerByName('SM_RG_IO_Count_Digital_Input_Cont').Rows[1].GetColumnByName('Non_Red_NIS').Value
                    except:
                        self.sdi1_line_mon_uio_nrd_nis = 0
                    try:
                        self.sdi1_5k_resistor_uio_nrd_nis = Product.GetContainerByName('SM_RG_IO_Count_Digital_Input_Cont').Rows[2].GetColumnByName('Non_Red_NIS').Value
                    except:
                        self.sdi1_5k_resistor_uio_nrd_nis = 0
                    #DO
                    try:
                        self.sdo1_uio_nrd_nis = Product.GetContainerByName('SM_RG_IO_Count_Digital_Output_Cont').Rows[0].GetColumnByName('Non_Red_NIS').Value
                    except:
                        self.sdo1_uio_nrd_nis = 0
                    try:
                        self.sdo7_line_mon_uio_nrd_nis = Product.GetContainerByName('SM_RG_IO_Count_Digital_Output_Cont').Rows[1].GetColumnByName('Non_Red_NIS').Value
                    except:
                        self.sdo7_line_mon_uio_nrd_nis = 0
                    try:
                        self.sdo16_sil23_uio_nrd_nis = Product.GetContainerByName('SM_RG_IO_Count_Digital_Output_Cont').Rows[2].GetColumnByName('Non_Red_NIS').Value
                    except:
                        self.sdo16_sil23_uio_nrd_nis = 0
                    try:
                        self.sdo12_sil23_com_uio_nrd_nis = Product.GetContainerByName('SM_RG_IO_Count_Digital_Output_Cont').Rows[3].GetColumnByName('Non_Red_NIS').Value
                    except:
                        self.sdo12_sil23_com_uio_nrd_nis = 0
                    #NR Relay
                    try:
                        self.sdi1_uio_nrd_rly = Product.GetContainerByName('SM_RG_IO_Count_Digital_Input_Cont').Rows[0].GetColumnByName('Non_Red_RLY').Value
                    except:
                        self.sdi1_uio_nrd_rly = 0
                    try:
                        self.sdo1_uio_nrd_rly = Product.GetContainerByName('SM_RG_IO_Count_Digital_Output_Cont').Rows[0].GetColumnByName('Non_Red_RLY').Value
                    except:
                        self.sdo1_uio_nrd_rly = 0
                    # Non REd SIL 2 RLY
                    try:
                        self.sdo1_uio_nrd_sil2_rly = Product.GetContainerByName('SM_RG_DO_RLY_NMR_Cont').Rows[0].GetColumnByName('Non_Red_SIL2_RLY').Value
                    except:
                        self.sdo1_uio_nrd_sil2_rly = 0
                    # Non REd SIL 3 RLY
                    try:
                        self.sdi1_uio_nrd_sil3_rly = Product.GetContainerByName('SM_RG_DI_RLY_NMR_Cont').Rows[0].GetColumnByName('Non_Red_SIL3_RLY').Value
                    except:
                        self.sdi1_uio_nrd_sil3_rly = 0
                    try:
                        self.sdo1_uio_nrd_sil3_rly = Product.GetContainerByName('SM_RG_DO_RLY_NMR_Cont').Rows[0].GetColumnByName('Non_Red_SIL3_RLY').Value
                    except:
                        self.sdo1_uio_nrd_sil3_rly = 0
                     # Non REd nmr
                    try:
                        self.sdi1_uio_nrd_nmr = Product.GetContainerByName('SM_RG_DI_RLY_NMR_Cont').Rows[0].GetColumnByName('Non_Red_NMR').Value
                    except:
                        self.sdi1_uio_nrd_nmr =0
                    # Non REd NMR Safety
                    try:
                        self.sdi1_uio_nrd_nmr_safety = Product.GetContainerByName('SM_RG_DI_RLY_NMR_Cont').Rows[0].GetColumnByName('Non_Red_NMR_Safety').Value
                    except:
                        self.sdi1_uio_nrd_nmr_safety = 0
                    # Marshalling_Option =="Universal Marshalling"
                elif Marshalling_Option =="Hardware Marshalling with P+F":
                    #percent 
                    try:
                        self.percent_spare_io = Product.GetContainerByName('SM_RG_Cabinet_Details_Cont').Rows[0].GetColumnByName('SM_Percent_Installed_Spare_IO').Value
                    except:
                        self.percent_spare_io = 0
                    #AI
                    try:
                        self.sai1_uio_nrd_nis = Product.GetContainerByName('SM_RG_IO_Count_Analog_Input_Cont').Rows[0].GetColumnByName('Non_Red_NIS').Value
                    except:
                        self.sai1_uio_nrd_nis = 0
                    try:
                        self.sai1_fire2_wire_uio_nrd_nis = Product.GetContainerByName('SM_RG_IO_Count_Analog_Input_Cont').Rows[2].GetColumnByName('Non_Red_NIS').Value
                    except:
                        self.sai1_fire2_wire_uio_nrd_nis = 0
                    try:
                        self.sai1_fire34_wire_uio_nrd_nis = Product.GetContainerByName('SM_RG_IO_Count_Analog_Input_Cont').Rows[3].GetColumnByName('Non_Red_NIS').Value
                    except:
                        self.sai1_fire34_wire_uio_nrd_nis = 0
                    try:
                        self.sai1_fire34_wire_sink_uio_nrd_nis = Product.GetContainerByName('SM_RG_IO_Count_Analog_Input_Cont').Rows[1].GetColumnByName('Non_Red_NIS').Value
                    except:
                        self.sai1_fire34_wire_sink_uio_nrd_nis = 0
                    try:
                        self.sai1_gas_uio_nrd_nis = Product.GetContainerByName('SM_RG_IO_Count_Analog_Input_Cont').Rows[4].GetColumnByName('Non_Red_NIS').Value
                    except:
                        self.sai1_gas_uio_nrd_nis = 0
                    #AO
                    try:
                        self.sao1_uio_nrd_nis = Product.GetContainerByName('SM_RG_IO_Count_Analog_Output_Cont').Rows[0].GetColumnByName('Non_Red_NIS').Value
                    except:
                        self.sao1_uio_nrd_nis = 0
                    #DI
                    try:
                        self.sdi1_uio_nrd_nis = Product.GetContainerByName('SM_RG_IO_Count_Digital_Input_Cont').Rows[0].GetColumnByName('Non_Red_NIS').Value
                    except:
                        self.sdi1_uio_nrd_nis = 0
                    try:
                        self.sdi1_line_mon_uio_nrd_nis = Product.GetContainerByName('SM_RG_IO_Count_Digital_Input_Cont').Rows[3].GetColumnByName('Non_Red_NIS').Value
                    except:
                        self.sdi1_line_mon_uio_nrd_nis = 0
                    try:
                        self.sdi1_5k_resistor_uio_nrd_nis = Product.GetContainerByName('SM_RG_IO_Count_Digital_Input_Cont').Rows[2].GetColumnByName('Non_Red_NIS').Value
                    except:
                        self.sdi1_5k_resistor_uio_nrd_nis = 0
                    #DO
                    try:
                        self.sdo1_uio_nrd_nis = Product.GetContainerByName('SM_RG_IO_Count_Digital_Output_Cont').Rows[0].GetColumnByName('Non_Red_NIS').Value
                    except:
                        self.sdo1_uio_nrd_nis = 0
                    try:
                        self.sdo7_line_mon_uio_nrd_nis = Product.GetContainerByName('SM_RG_IO_Count_Digital_Output_Cont').Rows[2].GetColumnByName('Non_Red_NIS').Value
                    except:
                        self.sdo7_line_mon_uio_nrd_nis = 0
                    try:
                        self.sdo16_sil23_uio_nrd_nis = Product.GetContainerByName('SM_RG_IO_Count_Digital_Output_Cont').Rows[3].GetColumnByName('Non_Red_NIS').Value
                    except:
                        self.sdo16_sil23_uio_nrd_nis = 0
                    try:
                        self.sdo12_sil23_com_uio_nrd_nis = Product.GetContainerByName('SM_RG_IO_Count_Digital_Output_Cont').Rows[4].GetColumnByName('Non_Red_NIS').Value
                    except:
                        self.sdo12_sil23_com_uio_nrd_nis = 0
                    #NR Relay
                    try:
                        self.sdi1_uio_nrd_rly = Product.GetContainerByName('SM_RG_IO_Count_Digital_Input_Cont').Rows[0].GetColumnByName('Non_Red_RLY').Value
                    except:
                        self.sdi1_uio_nrd_rly = 0
                    try:
                        self.sdo1_uio_nrd_rly = Product.GetContainerByName('SM_RG_IO_Count_Digital_Output_Cont').Rows[0].GetColumnByName('Non_Red_RLY').Value
                    except:
                        self.sdo1_uio_nrd_rly = 0
                    # Non REd SIL 2 RLY
                    try:
                        self.sdo1_uio_nrd_sil2_rly = Product.GetContainerByName('SM_RG_DO_RLY_NMR_Cont').Rows[0].GetColumnByName('Non_Red_SIL2_RLY').Value
                    except:
                        self.sdo1_uio_nrd_sil2_rly = 0
                    # Non REd SIL 3 RLY
                    try:
                        self.sdi1_uio_nrd_sil3_rly = Product.GetContainerByName('SM_RG_DI_RLY_NMR_Cont').Rows[0].GetColumnByName('Non_Red_SIL3_RLY').Value
                    except:
                        self.sdi1_uio_nrd_sil3_rly = 0
                    try:
                        self.sdo1_uio_nrd_sil3_rly = Product.GetContainerByName('SM_RG_DO_RLY_NMR_Cont').Rows[0].GetColumnByName('Non_Red_SIL3_RLY').Value
                    except:
                        self.sdo1_uio_nrd_sil3_rly = 0
                     # Non REd nmr
                    try:
                        self.sdi1_uio_nrd_nmr = Product.GetContainerByName('SM_RG_DI_RLY_NMR_Cont').Rows[0].GetColumnByName('Non_Red_NMR').Value
                    except:
                        self.sdi1_uio_nrd_nmr =0
                    # Non REd NMR Safety
                    try:
                        self.sdi1_uio_nrd_nmr_safety = Product.GetContainerByName('SM_RG_DI_RLY_NMR_Cont').Rows[0].GetColumnByName('Non_Red_NMR_Safety').Value
                    except:
                        self.sdi1_uio_nrd_nmr_safety = 0
                elif Marshalling_Option =="Hardware Marshalling with Other":
                    try:
                        self.percent_spare_io = Product.GetContainerByName('SM_RG_Cabinet_Details_Cont').Rows[0].GetColumnByName('SM_Percent_Installed_Spare_IO').Value
                    except:
                        self.percent_spare_io = 0
                    #AI
                    try:
                        self.sai1_uio_nrd_nis = Product.GetContainerByName('SM_RG_IO_Count_Analog_Input_Cont').Rows[0].GetColumnByName('Non_Red_NIS').Value
                    except:
                        self.sai1_uio_nrd_nis = 0
                    try:
                        self.sai1_fire2_wire_uio_nrd_nis = Product.GetContainerByName('SM_RG_IO_Count_Analog_Input_Cont').Rows[1].GetColumnByName('Non_Red_NIS').Value
                    except:
                        self.sai1_fire2_wire_uio_nrd_nis = 0
                    try:
                        self.sai1_fire34_wire_uio_nrd_nis = Product.GetContainerByName('SM_RG_IO_Count_Analog_Input_Cont').Rows[2].GetColumnByName('Non_Red_NIS').Value
                    except:
                        self.sai1_fire34_wire_uio_nrd_nis = 0
                    try:
                        self.sai1_fire34_wire_sink_uio_nrd_nis = Product.GetContainerByName('SM_RG_IO_Count_Analog_Input_Cont').Rows[5].GetColumnByName('Non_Red_NIS').Value
                    except:
                        self.sai1_fire34_wire_sink_uio_nrd_nis = 0
                    try:
                        self.sai1_gas_uio_nrd_nis = Product.GetContainerByName('SM_RG_IO_Count_Analog_Input_Cont').Rows[3].GetColumnByName('Non_Red_NIS').Value
                    except:
                        self.sai1_gas_uio_nrd_nis = 0
                    #AO
                    try:
                        self.sao1_uio_nrd_nis = Product.GetContainerByName('SM_RG_IO_Count_Analog_Output_Cont').Rows[0].GetColumnByName('Non_Red_NIS').Value
                    except:
                        self.sao1_uio_nrd_nis = 0
                    #DI
                    try:
                        self.sdi1_uio_nrd_nis = Product.GetContainerByName('SM_RG_IO_Count_Digital_Input_Cont').Rows[0].GetColumnByName('Non_Red_NIS').Value
                    except:
                        self.sdi1_uio_nrd_nis = 0
                    try:
                        self.sdi1_line_mon_uio_nrd_nis = Product.GetContainerByName('SM_RG_IO_Count_Digital_Input_Cont').Rows[1].GetColumnByName('Non_Red_NIS').Value
                    except:
                        self.sdi1_line_mon_uio_nrd_nis = 0
                    try:
                        self.sdi1_5k_resistor_uio_nrd_nis = Product.GetContainerByName('SM_RG_IO_Count_Digital_Input_Cont').Rows[5].GetColumnByName('Non_Red_NIS').Value
                    except:
                        self.sdi1_5k_resistor_uio_nrd_nis = 0
                    #DO
                    try:
                        self.sdo1_uio_nrd_nis = Product.GetContainerByName('SM_RG_IO_Count_Digital_Output_Cont').Rows[0].GetColumnByName('Non_Red_NIS').Value
                    except:
                        self.sdo1_uio_nrd_nis = 0
                    try:
                        self.sdo7_line_mon_uio_nrd_nis = Product.GetContainerByName('SM_RG_IO_Count_Digital_Output_Cont').Rows[1].GetColumnByName('Non_Red_NIS').Value
                    except:
                        self.sdo7_line_mon_uio_nrd_nis = 0
                    try:
                        self.sdo16_sil23_uio_nrd_nis = Product.GetContainerByName('SM_RG_IO_Count_Digital_Output_Cont').Rows[2].GetColumnByName('Non_Red_NIS').Value
                    except:
                        self.sdo16_sil23_uio_nrd_nis = 0
                    try:
                        self.sdo12_sil23_com_uio_nrd_nis = Product.GetContainerByName('SM_RG_IO_Count_Digital_Output_Cont').Rows[3].GetColumnByName('Non_Red_NIS').Value
                    except:
                        self.sdo12_sil23_com_uio_nrd_nis = 0
                    #NR Relay
                    try:
                        self.sdi1_uio_nrd_rly = Product.GetContainerByName('SM_RG_IO_Count_Digital_Input_Cont').Rows[0].GetColumnByName('Non_Red_RLY').Value
                    except:
                        self.sdi1_uio_nrd_rly = 0
                    try:
                        self.sdo1_uio_nrd_rly = Product.GetContainerByName('SM_RG_IO_Count_Digital_Output_Cont').Rows[0].GetColumnByName('Non_Red_RLY').Value
                    except:
                        self.sdo1_uio_nrd_rly = 0
                    # Non REd SIL 2 RLY
                    try:
                        self.sdo1_uio_nrd_sil2_rly = Product.GetContainerByName('SM_RG_DO_RLY_NMR_Cont').Rows[0].GetColumnByName('Non_Red_SIL2_RLY').Value
                    except:
                        self.sdo1_uio_nrd_sil2_rly = 0
                    # Non REd SIL 3 RLY
                    try:
                        self.sdi1_uio_nrd_sil3_rly = Product.GetContainerByName('SM_RG_DI_RLY_NMR_Cont').Rows[0].GetColumnByName('Non_Red_SIL3_RLY').Value
                    except:
                        self.sdi1_uio_nrd_sil3_rly = 0
                    try:
                        self.sdo1_uio_nrd_sil3_rly = Product.GetContainerByName('SM_RG_DO_RLY_NMR_Cont').Rows[0].GetColumnByName('Non_Red_SIL3_RLY').Value
                    except:
                        self.sdo1_uio_nrd_sil3_rly = 0
                     # Non REd nmr
                    try:
                        self.sdi1_uio_nrd_nmr = Product.GetContainerByName('SM_RG_DI_RLY_NMR_Cont').Rows[0].GetColumnByName('Non_Red_NMR').Value
                    except:
                        self.sdi1_uio_nrd_nmr =0
                    # Non REd NMR Safety
                    try:
                        self.sdi1_uio_nrd_nmr_safety = Product.GetContainerByName('SM_RG_DI_RLY_NMR_Cont').Rows[0].GetColumnByName('Non_Red_NMR_Safety').Value
                    except:
                        self.sdi1_uio_nrd_nmr_safety = 0