class AttrStorage:
    def get_column_value(self, row, col):
        return row.GetColumnByName(col).Value
    def __init__(self, Product):
        if Product.Name== "SM Control Group":
            try:
                self.percent_spare_io = Product.GetContainerByName('SM_CG_Cabinet_Details_Cont_Right').Rows[0].GetColumnByName('Percent_Installed_Spare_IOs').Value
            except:
                self.percent_spare_io = 0
            try:
                self.current_uio_RD_NIS = Product.GetContainerByName('SM_IO_Count_Analog_Input_Cont').Rows[0].GetColumnByName('Red (NIS)').Value
            except:
                self.current_uio_RD_NIS=0
            try:
                self.fire2_RD_NIS=Product.GetContainerByName('SM_IO_Count_Analog_Input_Cont').Rows[1].GetColumnByName('Red (NIS)').Value
            except:
                self.fire2_RD_NIS=0
            try:
                self.fire3and4_RD_NIS=Product.GetContainerByName('SM_IO_Count_Analog_Input_Cont').Rows[2].GetColumnByName('Red (NIS)').Value
            except:
                self.fire3and4_RD_NIS=0
            try:
                self.fire3and4_sink_RD_NIS=Product.GetContainerByName('SM_IO_Count_Analog_Input_Cont').Rows[3].GetColumnByName('Red (NIS)').Value
            except:
                self.fire3and4_sink_RD_NIS=0
            try:
                self.gas_RD_NIS=Product.GetContainerByName('SM_IO_Count_Analog_Input_Cont').Rows[4].GetColumnByName('Red (NIS)').Value
            except:
                self.gas_RD_NIS=0
            try:
                self.type_uio_RD_NIS=Product.GetContainerByName('SM_IO_Count_Analog_Output_Cont').Rows[0].GetColumnByName('Red (NIS)').Value
            except:
                self.type_uio_RD_NIS=0
            try:
                self.uio_do_RD_NIS=Product.GetContainerByName('SM_IO_Count_Digital_Output_Cont').Rows[0].GetColumnByName('Red (NIS)').Value
            except:
                self.uio_do_RD_NIS=0
            try:
                self.line_mon_uio_do_RD_NIS=Product.GetContainerByName('SM_IO_Count_Digital_Output_Cont').Rows[1].GetColumnByName('Red (NIS)').Value
            except:
                self.line_mon_uio_do_RD_NIS=0
            try:
                self.sil_2_3_uio_do_RD_NIS=Product.GetContainerByName('SM_IO_Count_Digital_Output_Cont').Rows[2].GetColumnByName('Red (NIS)').Value
            except:
                self.sil_2_3_uio_do_RD_NIS=0
            try:
                self.sil_2_3_com_uio_do_RD_NIS=Product.GetContainerByName('SM_IO_Count_Digital_Output_Cont').Rows[3].GetColumnByName('Red (NIS)').Value
            except:
                self.sil_2_3_com_uio_do_RD_NIS=0
            try:
                self.uio_di_RD_NIS=Product.GetContainerByName('SM_IO_Count_Digital_Input_Cont').Rows[0].GetColumnByName('Red (NIS)').Value
            except:
                self.uio_di_RD_NIS=0
            try:
                self.line_mon_uio_di_RD_NIS=Product.GetContainerByName('SM_IO_Count_Digital_Input_Cont').Rows[1].GetColumnByName('Red (NIS)').Value
            except:
                self.line_mon_uio_di_RD_NIS=0
            try:
                self.with_5k_resistor_uio_di_RD_NIS=Product.GetContainerByName('SM_IO_Count_Digital_Input_Cont').Rows[2].GetColumnByName('Red (NIS)').Value
            except:
                self.with_5k_resistor_uio_di_RD_NIS=0
            try:
                self.uio_di_rly=Product.GetContainerByName('SM_IO_Count_Digital_Input_Cont').Rows[0].GetColumnByName('Red (RLY)').Value
            except:
                self.uio_di_rly=0
            try:
                self.uio_do_rly=Product.GetContainerByName('SM_IO_Count_Digital_Output_Cont').Rows[0].GetColumnByName('Red (RLY)').Value
            except:
                self.uio_do_rly=0
            try:
                self.uio_do_sil2_rly=Product.GetContainerByName('SM_CG_DO_RLY_NMR_Cont').Rows[0].GetColumnByName('Red (SIL2 RLY)').Value
            except:
                self.uio_do_sil2_rly=0
            try:
                self.uio_di_sil3_rly=Product.GetContainerByName('SM_CG_DI_RLY_NMR_Cont').Rows[0].GetColumnByName('Red (SIL3 RLY)').Value
            except:
                self.uio_di_sil3_rly=0
            try:
                self.uio_do_sil3_rly=Product.GetContainerByName('SM_CG_DO_RLY_NMR_Cont').Rows[0].GetColumnByName('Red (SIL3 RLY)').Value
            except:
                self.uio_do_sil3_rly=0
            try:
                self.uio_di_nmr=Product.GetContainerByName('SM_CG_DI_RLY_NMR_Cont').Rows[0].GetColumnByName('Red (NMR)').Value
            except:
                self.uio_di_nmr=0
            try:
                self.uio_di_nmr_safety=Product.GetContainerByName('SM_CG_DI_RLY_NMR_Cont').Rows[0].GetColumnByName('Red (NMR  Safety)').Value
            except:
                self.uio_di_nmr_safety=0

                
                
        elif Product.Name== "SM Remote Group":
            try:
                self.percent_spare_io = Product.GetContainerByName('SM_RG_Cabinet_Details_Cont').Rows[0].GetColumnByName('SM_Percent_Installed_Spare_IO').Value
            except:
                self.percent_spare_io = 0
            try:
                self.current_uio_RD_NIS = Product.GetContainerByName('SM_RG_IO_Count_Analog_Input_Cont').Rows[0].GetColumnByName('Red_NIS').Value
            except:
                self.current_uio_RD_NIS=0
            try:
                self.fire2_RD_NIS=Product.GetContainerByName('SM_RG_IO_Count_Analog_Input_Cont').Rows[1].GetColumnByName('Red_NIS').Value
            except:
                self.fire2_RD_NIS=0
            try:
                self.fire3and4_RD_NIS=Product.GetContainerByName('SM_RG_IO_Count_Analog_Input_Cont').Rows[2].GetColumnByName('Red_NIS').Value
            except:
                self.fire3and4_RD_NIS=0
            try:
                self.fire3and4_sink_RD_NIS=Product.GetContainerByName('SM_RG_IO_Count_Analog_Input_Cont').Rows[3].GetColumnByName('Red_NIS').Value
            except:
                self.fire3and4_sink_RD_NIS=0
            try:
                self.gas_RD_NIS=Product.GetContainerByName('SM_RG_IO_Count_Analog_Input_Cont').Rows[4].GetColumnByName('Red_NIS').Value
            except:
                self.gas_RD_NIS=0
            try:
                self.type_uio_RD_NIS=Product.GetContainerByName('SM_RG_IO_Count_Analog_Output_Cont').Rows[0].GetColumnByName('Red_NIS').Value
            except:
                self.type_uio_RD_NIS=0
            try:
                self.uio_do_RD_NIS=Product.GetContainerByName('SM_RG_IO_Count_Digital_Output_Cont').Rows[0].GetColumnByName('Red_NIS').Value
            except:
                self.uio_do_RD_NIS=0
            try:
                self.line_mon_uio_do_RD_NIS=Product.GetContainerByName('SM_RG_IO_Count_Digital_Output_Cont').Rows[1].GetColumnByName('Red_NIS').Value
            except:
                self.line_mon_uio_do_RD_NIS=0
            try:
                self.sil_2_3_uio_do_RD_NIS=Product.GetContainerByName('SM_RG_IO_Count_Digital_Output_Cont').Rows[2].GetColumnByName('Red_NIS').Value
            except:
                self.sil_2_3_uio_do_RD_NIS=0
            try:
                self.sil_2_3_com_uio_do_RD_NIS=Product.GetContainerByName('SM_RG_IO_Count_Digital_Output_Cont').Rows[3].GetColumnByName('Red_NIS').Value
            except:
                self.sil_2_3_com_uio_do_RD_NIS=0
            try:
                self.uio_di_RD_NIS=Product.GetContainerByName('SM_RG_IO_Count_Digital_Input_Cont').Rows[0].GetColumnByName('Red_NIS').Value
            except:
                self.uio_di_RD_NIS=0
            try:
                self.line_mon_uio_di_RD_NIS=Product.GetContainerByName('SM_RG_IO_Count_Digital_Input_Cont').Rows[1].GetColumnByName('Red_NIS').Value
            except:
                self.line_mon_uio_di_RD_NIS=0
            try:
                self.with_5k_resistor_uio_di_RD_NIS=Product.GetContainerByName('SM_RG_IO_Count_Digital_Input_Cont').Rows[2].GetColumnByName('Red_NIS').Value
            except:
                self.with_5k_resistor_uio_di_RD_NIS=0
            try:
                self.uio_di_rly=Product.GetContainerByName('SM_RG_IO_Count_Digital_Input_Cont').Rows[0].GetColumnByName('Red_RLY').Value
            except:
                self.uio_di_rly=0
            try:
                self.uio_do_rly=Product.GetContainerByName('SM_RG_IO_Count_Digital_Output_Cont').Rows[0].GetColumnByName('Red_RLY').Value
            except:
                self.uio_do_rly=0
            try:
                self.uio_do_sil2_rly=Product.GetContainerByName('SM_CG_DO_RLY_NMR_Cont').Rows[0].GetColumnByName('Red_SIL2_RLY').Value
            except:
                self.uio_do_sil2_rly=0
            try:
                self.uio_di_sil3_rly=Product.GetContainerByName('SM_CG_DI_RLY_NMR_Cont').Rows[0].GetColumnByName('Red_SIL3_RLY)').Value
            except:
                self.uio_di_sil3_rly=0
            try:
                self.uio_do_sil3_rly=Product.GetContainerByName('SM_CG_DO_RLY_NMR_Cont').Rows[0].GetColumnByName('Red_SIL3_RLY').Value
            except:
                self.uio_do_sil3_rly=0
            try:
                self.uio_di_nmr=Product.GetContainerByName('SM_CG_DI_RLY_NMR_Cont').Rows[0].GetColumnByName('Red_NMR').Value
            except:
                self.uio_di_nmr=0
            try:
                self.uio_di_nmr_safety=Product.GetContainerByName('SM_CG_DI_RLY_NMR_Cont').Rows[0].GetColumnByName('Red_NMR_Safety').Value
            except:
                self.uio_di_nmr_safety=0