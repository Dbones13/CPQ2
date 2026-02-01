#CXCPQ-31183 Added by Shivani
def getInt(var):
    if var:
        return int(var)
    return 0.0
def GS_SM_PowerLoad_IOTA_A_Calc(Product):
    if Product.Name == "SM Control Group":
        Trace.Write("SM Control Group")
        powerload_A_cg = 0.0
        power_supply = Product.GetContainerByName('SM_CG_Cabinet_Details_Cont_Left').Rows[0].GetColumnByName("Power_Supply").DisplayValue
        unit_load = Product.GetContainerByName('SM_CG_Cabinet_Details_Cont_Right').Rows[0].GetColumnByName("SDO_24Vdc_500mA_UIO_DIO_UnitLoad1mA-500mA").Value
        ui_L_1 = Product.GetContainerByName('SM_CG_Cabinet_Details_Cont_Right').Rows[0].GetColumnByName("SDO_2_24Vdc1A_UIO_Unit_Load_501mA_1000mA").Value
        ui_L_2 = Product.GetContainerByName('SM_CG_Cabinet_Details_Cont_Right').Rows[0].GetColumnByName("SDO_4_24Vdc2A_UIO_Unit_Load_1001mA_2000mA").Value
        di_do_relay = Product.GetContainerByName('SM_CG_Cabinet_Details_Cont_Right').Rows[0].GetColumnByName("DI/DO_SIL2/3_Relay_Adapter_UMC").DisplayValue
        namur = Product.GetContainerByName('SM_CG_Cabinet_Details_Cont_Right').Rows[0].GetColumnByName("DI_NAMUR_proximity_Switches_Adapter_UMC").DisplayValue
        # AI
        ai_uio = getInt(Product.GetContainerByName('SM_IO_Count_Analog_Input_Cont').Rows[0].GetColumnByName("Red (IS)").Value)
        ai_uio_nis = getInt(Product.GetContainerByName('SM_IO_Count_Analog_Input_Cont').Rows[0].GetColumnByName("Red (NIS)").Value)
        
        ai_uio_nr = getInt(Product.GetContainerByName('SM_IO_Count_Analog_Input_Cont').Rows[0].GetColumnByName("Non Red (IS)").Value)
        ai_uio_nis_nr = getInt(Product.GetContainerByName('SM_IO_Count_Analog_Input_Cont').Rows[0].GetColumnByName("Non Red (NIS)").Value)
        
        ai_fire2_uio = getInt(Product.GetContainerByName('SM_IO_Count_Analog_Input_Cont').Rows[1].GetColumnByName("Red (IS)").Value)
        ai_fire2_uio_nis = getInt(Product.GetContainerByName('SM_IO_Count_Analog_Input_Cont').Rows[1].GetColumnByName("Red (NIS)").Value)
        ai_fire2_uio_nr = getInt(Product.GetContainerByName('SM_IO_Count_Analog_Input_Cont').Rows[1].GetColumnByName("Non Red (IS)").Value)
        ai_fire2_uio_nis_nr = getInt(Product.GetContainerByName('SM_IO_Count_Analog_Input_Cont').Rows[1].GetColumnByName("Non Red (NIS)").Value)
        
        ai_fire34_uio = getInt(Product.GetContainerByName('SM_IO_Count_Analog_Input_Cont').Rows[2].GetColumnByName("Red (IS)").Value)
        ai_fire34_uio_nis = getInt(Product.GetContainerByName('SM_IO_Count_Analog_Input_Cont').Rows[2].GetColumnByName("Red (NIS)").Value)
        ai_fire34_uio_nr = getInt(Product.GetContainerByName('SM_IO_Count_Analog_Input_Cont').Rows[2].GetColumnByName("Non Red (IS)").Value)
        ai_fire34_uio_nis_nr = getInt(Product.GetContainerByName('SM_IO_Count_Analog_Input_Cont').Rows[2].GetColumnByName("Non Red (NIS)").Value)
        
        ai_fire34_sink_uio = getInt(Product.GetContainerByName('SM_IO_Count_Analog_Input_Cont').Rows[3].GetColumnByName("Red (IS)").Value)
        ai_fire34_sink_uio_nis = getInt(Product.GetContainerByName('SM_IO_Count_Analog_Input_Cont').Rows[3].GetColumnByName("Red (NIS)").Value)
        ai_fire34_sink_uio_nr = getInt(Product.GetContainerByName('SM_IO_Count_Analog_Input_Cont').Rows[3].GetColumnByName("Non Red (IS)").Value)
        ai_fire34_sink_uio_nis_nr = getInt(Product.GetContainerByName('SM_IO_Count_Analog_Input_Cont').Rows[3].GetColumnByName("Non Red (NIS)").Value)
        
        ai_gas_uio = getInt(Product.GetContainerByName('SM_IO_Count_Analog_Input_Cont').Rows[4].GetColumnByName("Red (IS)").Value)
        ai_gas_uio_nis = getInt(Product.GetContainerByName('SM_IO_Count_Analog_Input_Cont').Rows[4].GetColumnByName("Red (NIS)").Value)
        ai_gas_uio_nr = getInt(Product.GetContainerByName('SM_IO_Count_Analog_Input_Cont').Rows[4].GetColumnByName("Non Red (IS)").Value)
        ai_gas_uio_nis_nr = getInt(Product.GetContainerByName('SM_IO_Count_Analog_Input_Cont').Rows[4].GetColumnByName("Non Red (NIS)").Value)
        
        # AO
        ao_uio = getInt(Product.GetContainerByName('SM_IO_Count_Analog_Output_Cont').Rows[0].GetColumnByName("Red (IS)").Value)
        ao_uio_nis = getInt(Product.GetContainerByName('SM_IO_Count_Analog_Output_Cont').Rows[0].GetColumnByName("Red (NIS)").Value)
        ao_uio_nr = getInt(Product.GetContainerByName('SM_IO_Count_Analog_Output_Cont').Rows[0].GetColumnByName("Non Red (IS)").Value)
        ao_uio_nis_nr = getInt(Product.GetContainerByName('SM_IO_Count_Analog_Output_Cont').Rows[0].GetColumnByName("Non Red (NIS)").Value)
        
        #DI
        di_uio = getInt(Product.GetContainerByName('SM_IO_Count_Digital_Input_Cont').Rows[0].GetColumnByName("Red (IS)").Value)
        di_uio_nis = getInt(Product.GetContainerByName('SM_IO_Count_Digital_Input_Cont').Rows[0].GetColumnByName("Red (NIS)").Value)
        di_uio_rly = getInt(Product.GetContainerByName('SM_IO_Count_Digital_Input_Cont').Rows[0].GetColumnByName("Red (RLY)").Value)
        if di_do_relay == 'Yes' or namur == 'Yes':
            di_uio_sil2_rly = getInt(Product.GetContainerByName('SM_CG_DI_RLY_NMR_Cont').Rows[0].GetColumnByName("Red_SIL2_RLY").Value)
            di_uio_sil3_rly = getInt(Product.GetContainerByName('SM_CG_DI_RLY_NMR_Cont').Rows[0].GetColumnByName("Red_SIL3_RLY").Value)
            di_uio_nmr_rly = getInt(Product.GetContainerByName('SM_CG_DI_RLY_NMR_Cont').Rows[0].GetColumnByName("Red_NMR").Value)
            di_uio_nmr_safety_rly = getInt(Product.GetContainerByName('SM_CG_DI_RLY_NMR_Cont').Rows[0].GetColumnByName("Red_NMR_Safety").Value)
            di_uio_sil2_rly_nr = getInt(Product.GetContainerByName('SM_CG_DI_RLY_NMR_Cont').Rows[0].GetColumnByName("Non_Red_SIL2_RLY").Value)
            di_uio_sil3_rly_nr = getInt(Product.GetContainerByName('SM_CG_DI_RLY_NMR_Cont').Rows[0].GetColumnByName("Non_Red_SIL3_RLY").Value)
            di_uio_nmr_rly_nr = getInt(Product.GetContainerByName('SM_CG_DI_RLY_NMR_Cont').Rows[0].GetColumnByName("Non_Red_NMR").Value)
            di_uio_nmr_safety_rly_nr = getInt(Product.GetContainerByName('SM_CG_DI_RLY_NMR_Cont').Rows[0].GetColumnByName("Non_Red_NMR_Safety").Value)
        else:
            di_uio_sil2_rly = 0
            di_uio_sil3_rly = 0
            di_uio_nmr_rly = 0
            di_uio_nmr_safety_rly = 0
            di_uio_sil2_rly_nr = 0
            di_uio_sil3_rly_nr = 0
            di_uio_nmr_rly_nr = 0
            di_uio_nmr_safety_rly_nr = 0
        di_uio_nr = getInt(Product.GetContainerByName('SM_IO_Count_Digital_Input_Cont').Rows[0].GetColumnByName("Non Red (IS)").Value)
        di_uio_nis_nr = getInt(Product.GetContainerByName('SM_IO_Count_Digital_Input_Cont').Rows[0].GetColumnByName("Non Red (NIS)").Value)
        di_uio_rly_nr = getInt(Product.GetContainerByName('SM_IO_Count_Digital_Input_Cont').Rows[0].GetColumnByName("Non Red (RLY)").Value)
        
        di_5k_resistor_uio = getInt(Product.GetContainerByName('SM_IO_Count_Digital_Input_Cont').Rows[2].GetColumnByName("Red (IS)").Value)
        di_5k_resistor_uio_nis = getInt(Product.GetContainerByName('SM_IO_Count_Digital_Input_Cont').Rows[2].GetColumnByName("Red (NIS)").Value)
        di_5k_resistor_uio_rly = getInt(Product.GetContainerByName('SM_IO_Count_Digital_Input_Cont').Rows[2].GetColumnByName("Red (RLY)").Value)
        di_5k_resistor_uio_nr = getInt(Product.GetContainerByName('SM_IO_Count_Digital_Input_Cont').Rows[2].GetColumnByName("Non Red (IS)").Value)
        di_5k_resistor_uio_nis_nr = getInt(Product.GetContainerByName('SM_IO_Count_Digital_Input_Cont').Rows[2].GetColumnByName("Non Red (NIS)").Value)
        di_5k_resistor_uio_rly_nr = getInt(Product.GetContainerByName('SM_IO_Count_Digital_Input_Cont').Rows[2].GetColumnByName("Non Red (RLY)").Value)
        
        di_linemon_uio = getInt(Product.GetContainerByName('SM_IO_Count_Digital_Input_Cont').Rows[1].GetColumnByName("Red (IS)").Value)
        di_linemon_uio_nis = getInt(Product.GetContainerByName('SM_IO_Count_Digital_Input_Cont').Rows[1].GetColumnByName("Red (NIS)").Value)
        di_linemon_uio_nr = getInt(Product.GetContainerByName('SM_IO_Count_Digital_Input_Cont').Rows[1].GetColumnByName("Non Red (IS)").Value)
        di_linemon_uio_nis_nr = getInt(Product.GetContainerByName('SM_IO_Count_Digital_Input_Cont').Rows[1].GetColumnByName("Non Red (NIS)").Value)
        
        #DO
        do_uio = getInt(Product.GetContainerByName('SM_IO_Count_Digital_Output_Cont').Rows[0].GetColumnByName("Red (IS)").Value)
        do_uio_nis = getInt(Product.GetContainerByName('SM_IO_Count_Digital_Output_Cont').Rows[0].GetColumnByName("Red (NIS)").Value)
        do_uio_rly = getInt(Product.GetContainerByName('SM_IO_Count_Digital_Output_Cont').Rows[0].GetColumnByName("Red (RLY)").Value)
        do_uio_nr = getInt(Product.GetContainerByName('SM_IO_Count_Digital_Output_Cont').Rows[0].GetColumnByName("Non Red (IS)").Value)
        do_uio_nis_nr = getInt(Product.GetContainerByName('SM_IO_Count_Digital_Output_Cont').Rows[0].GetColumnByName("Non Red (NIS)").Value)
        do_uio_rly_nr = getInt(Product.GetContainerByName('SM_IO_Count_Digital_Output_Cont').Rows[0].GetColumnByName("Non Red (RLY)").Value)
        
        do_linemon_uio = getInt(Product.GetContainerByName('SM_IO_Count_Digital_Output_Cont').Rows[3].GetColumnByName("Red (IS)").Value)
        do_linemon_uio_nis = getInt(Product.GetContainerByName('SM_IO_Count_Digital_Output_Cont').Rows[3].GetColumnByName("Red (NIS)").Value)
        do_linemon_uio_nr = getInt(Product.GetContainerByName('SM_IO_Count_Digital_Output_Cont').Rows[3].GetColumnByName("Non Red (IS)").Value)
        do_linemon_uio_nis_nr = getInt(Product.GetContainerByName('SM_IO_Count_Digital_Output_Cont').Rows[3].GetColumnByName("Non Red (NIS)").Value)

        do_sil23_uio_is = getInt(Product.GetContainerByName('SM_IO_Count_Digital_Output_Cont').Rows[4].GetColumnByName("Red (IS)").Value)
        
        do_sil23_uio_nis = getInt(Product.GetContainerByName('SM_IO_Count_Digital_Output_Cont').Rows[4].GetColumnByName("Red (NIS)").Value)
        do_sil23_uio_nis_nr = getInt(Product.GetContainerByName('SM_IO_Count_Digital_Output_Cont').Rows[4].GetColumnByName("Non Red (NIS)").Value)
        
        do_sil23_com_uio_nis = getInt(Product.GetContainerByName('SM_IO_Count_Digital_Output_Cont').Rows[5].GetColumnByName("Red (NIS)").Value)
        do_sil23_com_uio_nis_nr = getInt(Product.GetContainerByName('SM_IO_Count_Digital_Output_Cont').Rows[5].GetColumnByName("Non Red (NIS)").Value)

        
        #Adding logic for #31183
        do_1A_io_nis = getInt(Product.GetContainerByName('SM_IO_Count_Digital_Output_Cont').Rows[1].GetColumnByName("Red (NIS)").Value)
        do_1A_io_nis_nr = getInt(Product.GetContainerByName('SM_IO_Count_Digital_Output_Cont').Rows[1].GetColumnByName("Non Red (NIS)").Value)

        do_2A_io_nis = getInt(Product.GetContainerByName('SM_IO_Count_Digital_Output_Cont').Rows[2].GetColumnByName("Red (NIS)").Value)
        do_2A_io_nis_nr = getInt(Product.GetContainerByName('SM_IO_Count_Digital_Output_Cont').Rows[2].GetColumnByName("Non Red (NIS)").Value)

        powerload_A_cg = 0.0
        if power_supply == "Redundant":
            val_1 = float(((ai_uio + ai_uio_nis)*25) + 600)
            val_2 = float(((ai_fire2_uio + ai_fire2_uio_nis)*25) + 600)
            val_3 = float(((ai_fire34_uio + ai_fire34_uio_nis + ai_fire34_sink_uio + ai_fire34_sink_uio_nis)*25) + 600)
            val_4 = float(((ai_gas_uio + ai_gas_uio_nis)*25) + 600)
            val_5 = float(((ao_uio + ao_uio_nis)*25) + 600)
            val_6 = float(((di_uio + di_uio_nis + di_uio_rly + di_uio_sil2_rly + di_uio_sil3_rly + di_uio_nmr_rly + di_uio_nmr_safety_rly + di_5k_resistor_uio + di_5k_resistor_uio_nis + di_5k_resistor_uio_rly)*7) + 600)
            val_7 = float(((di_linemon_uio + di_linemon_uio_nis)*7) + 600)
            if unit_load:
                ul = int(unit_load)
            else:
                ul = 250
            if ui_L_1:
                unit_Load1 = int(ui_L_1)
            else:
                unit_Load1 = 750
            if ui_L_2:
                unit_Load2 = int(ui_L_2)
            else:
                unit_Load2 = 1500
            val_8 = float(((do_uio + do_uio_nis)*ul) + 600)
            val_9 = float(((do_linemon_uio + do_linemon_uio_nis)*30) + 600)
            val_10 = float((do_sil23_uio_nis*40) + 600)
            val_11 = float((do_sil23_com_uio_nis*40) + 600)
            val_12 = float(((do_1A_io_nis) *unit_Load1) + 600)
            val_13 = float(((do_2A_io_nis) *unit_Load2) + 600)
            powerload_A_cg = val_1 + val_2 + val_3 + val_4 + val_5 + val_6 + val_7 + val_8 + val_9 + val_10 + val_11 + val_12 + val_13
        elif power_supply == "Non Redundant":
            val_1 = float(((ai_uio_nr + ai_uio_nis_nr)*25) + 300)
            val_2 = float(((ai_fire2_uio_nr + ai_fire2_uio_nis_nr)*25) + 300)
            val_3 = float(((ai_fire34_uio_nr + ai_fire34_uio_nis_nr + ai_fire34_sink_uio_nr + ai_fire34_sink_uio_nis_nr)*25) + 300)
            val_4 = float(((ai_gas_uio_nr + ai_gas_uio_nis_nr)*25) + 300)
            val_5 = float(((ao_uio_nr + ao_uio_nis_nr)*25) + 300)
            val_6 = float(((di_uio_nr + di_uio_nis_nr + di_uio_rly_nr + di_uio_sil2_rly_nr + di_uio_sil3_rly_nr + di_uio_nmr_rly_nr + di_uio_nmr_safety_rly_nr + di_5k_resistor_uio_nr + di_5k_resistor_uio_nis_nr + di_5k_resistor_uio_rly_nr)*7) + 300)
            val_7 = float(((di_linemon_uio_nr + di_linemon_uio_nis_nr)*7) + 300)
            if unit_load:
                ul = int(unit_load)
            else:
                ul = 250
            if ui_L_1:
                unit_Load1 = int(ui_L_1)
            else:
                unit_Load1 = 750
            if ui_L_2:
                unit_Load2 = int(ui_L_2)
            else:
                unit_Load2 = 1500
            val_8 = float(((do_uio_nr + do_uio_nis_nr)*ul) + 300)
            val_9 = float(((do_linemon_uio_nr + do_linemon_uio_nis_nr)*30) + 300)
            val_10 = float((do_sil23_uio_nis_nr*40) + 300)
            val_11 = float((do_sil23_com_uio_nis_nr*40) + 300)
            val_12 = float(((do_1A_io_nis_nr)*unit_Load1) + 300)
            val_13 = float(((do_2A_io_nis_nr) *unit_Load2) + 300)
            powerload_A_cg = val_1 + val_2 + val_3 + val_4 + val_5 + val_6 + val_7 + val_8 + val_9 + val_10 + val_11 +val_12 + val_13
                
        return round(powerload_A_cg, 2)
    elif Prod.Name == "SM Remote Group":
        Trace.Write("SM Control Group")
        power_supply = Prod.GetContainerByName('SM_RG_Cabinet_Details_Cont_Left').Rows[0].GetColumnByName("Power_Supply").DisplayValue
        unit_load = Prod.GetContainerByName('SM_RG_Cabinet_Details_Cont').Rows[0].GetColumnByName("SM_SDO_UIO_DIO").Value
        ui_L_1 = Prod.GetContainerByName('SM_RG_Cabinet_Details_Cont').Rows[0].GetColumnByName("SM_SDO_UIO_UnitLoad").Value
        ui_L_2 = Prod.GetContainerByName('SM_RG_Cabinet_Details_Cont').Rows[0].GetColumnByName("SM_SDO_UIO_Unit_Load").Value
        di_do_relay = Prod.GetContainerByName('SM_RG_Cabinet_Details_Cont').Rows[0].GetColumnByName("SM_DI_DORelay_Adapter_UMC").DisplayValue
        namur = Prod.GetContainerByName('SM_RG_Cabinet_Details_Cont').Rows[0].GetColumnByName("SM_DI_NAMUR_Switches_Adapter_UMC").DisplayValue
        # AI
        ai_uio = getInt(Product.GetContainerByName('SM_RG_IO_Count_Analog_Input_Cont').Rows[0].GetColumnByName("Red_IS").Value)
        ai_uio_nis = getInt(Product.GetContainerByName('SM_RG_IO_Count_Analog_Input_Cont').Rows[0].GetColumnByName("Red_NIS").Value)
        ai_uio_nr = getInt(Product.GetContainerByName('SM_RG_IO_Count_Analog_Input_Cont').Rows[0].GetColumnByName("Non_Red_IS").Value)
        ai_uio_nis_nr = getInt(Product.GetContainerByName('SM_RG_IO_Count_Analog_Input_Cont').Rows[0].GetColumnByName("Non_Red_NIS").Value)
        
        ai_fire2_uio = getInt(Product.GetContainerByName('SM_RG_IO_Count_Analog_Input_Cont').Rows[1].GetColumnByName("Red_IS").Value)
        ai_fire2_uio_nis = getInt(Product.GetContainerByName('SM_RG_IO_Count_Analog_Input_Cont').Rows[1].GetColumnByName("Red_NIS").Value)
        ai_fire2_uio_nr = getInt(Product.GetContainerByName('SM_RG_IO_Count_Analog_Input_Cont').Rows[1].GetColumnByName("Non_Red_IS").Value)
        ai_fire2_uio_nis_nr = getInt(Product.GetContainerByName('SM_RG_IO_Count_Analog_Input_Cont').Rows[1].GetColumnByName("Non_Red_NIS").Value)
        
        ai_fire34_uio = getInt(Product.GetContainerByName('SM_RG_IO_Count_Analog_Input_Cont').Rows[2].GetColumnByName("Red_IS").Value)
        ai_fire34_uio_nis = getInt(Product.GetContainerByName('SM_RG_IO_Count_Analog_Input_Cont').Rows[2].GetColumnByName("Red_NIS").Value)
        ai_fire34_uio_nr = getInt(Product.GetContainerByName('SM_RG_IO_Count_Analog_Input_Cont').Rows[2].GetColumnByName("Non_Red_IS").Value)
        ai_fire34_uio_nis_nr = getInt(Product.GetContainerByName('SM_RG_IO_Count_Analog_Input_Cont').Rows[2].GetColumnByName("Non_Red_NIS").Value)
        
        ai_fire34_sink_uio = getInt(Product.GetContainerByName('SM_RG_IO_Count_Analog_Input_Cont').Rows[3].GetColumnByName("Red_IS").Value)
        ai_fire34_sink_uio_nis = getInt(Product.GetContainerByName('SM_RG_IO_Count_Analog_Input_Cont').Rows[3].GetColumnByName("Red_NIS").Value)
        ai_fire34_sink_uio_nr = getInt(Product.GetContainerByName('SM_RG_IO_Count_Analog_Input_Cont').Rows[3].GetColumnByName("Non_Red_IS").Value)
        ai_fire34_sink_uio_nis_nr = getInt(Product.GetContainerByName('SM_RG_IO_Count_Analog_Input_Cont').Rows[3].GetColumnByName("Non_Red_NIS").Value)
        
        ai_gas_uio = getInt(Product.GetContainerByName('SM_RG_IO_Count_Analog_Input_Cont').Rows[4].GetColumnByName("Red_IS").Value)
        ai_gas_uio_nis = getInt(Product.GetContainerByName('SM_RG_IO_Count_Analog_Input_Cont').Rows[4].GetColumnByName("Red_NIS").Value)
        ai_gas_uio_nr = getInt(Product.GetContainerByName('SM_RG_IO_Count_Analog_Input_Cont').Rows[4].GetColumnByName("Non_Red_IS").Value)
        ai_gas_uio_nis_nr = getInt(Product.GetContainerByName('SM_RG_IO_Count_Analog_Input_Cont').Rows[4].GetColumnByName("Non_Red_NIS").Value)
        
        # AO
        ao_uio = getInt(Product.GetContainerByName('SM_RG_IO_Count_Analog_Output_Cont').Rows[0].GetColumnByName("Red_IS").Value)
        ao_uio_nis = getInt(Product.GetContainerByName('SM_RG_IO_Count_Analog_Output_Cont').Rows[0].GetColumnByName("Red_NIS").Value)
        ao_uio_nr = getInt(Product.GetContainerByName('SM_RG_IO_Count_Analog_Output_Cont').Rows[0].GetColumnByName("Non_Red_IS").Value)
        ao_uio_nis_nr = getInt(Product.GetContainerByName('SM_RG_IO_Count_Analog_Output_Cont').Rows[0].GetColumnByName("Non_Red_NIS").Value)
        
        #DI
        di_uio = getInt(Product.GetContainerByName('SM_RG_IO_Count_Digital_Input_Cont').Rows[0].GetColumnByName("Red_IS").Value)
        di_uio_nis = getInt(Product.GetContainerByName('SM_RG_IO_Count_Digital_Input_Cont').Rows[0].GetColumnByName("Red_NIS").Value)
        di_uio_rly = getInt(Product.GetContainerByName('SM_RG_IO_Count_Digital_Input_Cont').Rows[0].GetColumnByName("Red_RLY").Value)
        di_uio_sil2_rly = 0
        di_uio_sil3_rly = 0
        di_uio_nmr_rly = 0
        di_uio_nmr_safety_rly = 0
        di_uio_nr = getInt(Product.GetContainerByName('SM_RG_IO_Count_Digital_Input_Cont').Rows[0].GetColumnByName("Non_Red_IS").Value)
        di_uio_nis_nr = getInt(Product.GetContainerByName('SM_RG_IO_Count_Digital_Input_Cont').Rows[0].GetColumnByName("Non_Red_NIS").Value)
        di_uio_rly_nr = getInt(Product.GetContainerByName('SM_RG_IO_Count_Digital_Input_Cont').Rows[0].GetColumnByName("Non_Red_RLY").Value)
        di_uio_sil2_rly_nr = 0
        di_uio_sil3_rly_nr = 0
        di_uio_nmr_rly_nr = 0
        di_uio_nmr_safety_rly_nr = 0
        
        di_5k_resistor_uio = getInt(Product.GetContainerByName('SM_RG_IO_Count_Digital_Input_Cont').Rows[2].GetColumnByName("Red_IS").Value)
        di_5k_resistor_uio_nis = getInt(Product.GetContainerByName('SM_RG_IO_Count_Digital_Input_Cont').Rows[2].GetColumnByName("Red_NIS").Value)
        di_5k_resistor_uio_rly = getInt(Product.GetContainerByName('SM_RG_IO_Count_Digital_Input_Cont').Rows[2].GetColumnByName("Red_RLY").Value)
        di_5k_resistor_uio_nr = getInt(Product.GetContainerByName('SM_RG_IO_Count_Digital_Input_Cont').Rows[2].GetColumnByName("Non_Red_IS").Value)
        di_5k_resistor_uio_nis_nr = getInt(Product.GetContainerByName('SM_RG_IO_Count_Digital_Input_Cont').Rows[2].GetColumnByName("Non_Red_NIS").Value)
        di_5k_resistor_uio_rly_nr = getInt(Product.GetContainerByName('SM_RG_IO_Count_Digital_Input_Cont').Rows[2].GetColumnByName("Non_Red_RLY").Value)
        
        di_linemon_uio = getInt(Product.GetContainerByName('SM_RG_IO_Count_Digital_Input_Cont').Rows[1].GetColumnByName("Red_IS").Value)
        di_linemon_uio_nis = getInt(Product.GetContainerByName('SM_RG_IO_Count_Digital_Input_Cont').Rows[1].GetColumnByName("Red_NIS").Value)
        di_linemon_uio_nr = getInt(Product.GetContainerByName('SM_RG_IO_Count_Digital_Input_Cont').Rows[1].GetColumnByName("Non_Red_IS").Value)
        di_linemon_uio_nis_nr = getInt(Product.GetContainerByName('SM_RG_IO_Count_Digital_Input_Cont').Rows[1].GetColumnByName("Non_Red_NIS").Value)
        
        #DO
        do_uio = getInt(Product.GetContainerByName('SM_RG_IO_Count_Digital_Output_Cont').Rows[0].GetColumnByName("Red_IS").Value)
        do_uio_nis = getInt(Product.GetContainerByName('SM_RG_IO_Count_Digital_Output_Cont').Rows[0].GetColumnByName("Red_NIS").Value)
        do_uio_rly = getInt(Product.GetContainerByName('SM_RG_IO_Count_Digital_Output_Cont').Rows[0].GetColumnByName("Red_RLY").Value)
        do_uio_nr = getInt(Product.GetContainerByName('SM_RG_IO_Count_Digital_Output_Cont').Rows[0].GetColumnByName("Non_Red_IS").Value)
        do_uio_nis_nr = getInt(Product.GetContainerByName('SM_RG_IO_Count_Digital_Output_Cont').Rows[0].GetColumnByName("Non_Red_NIS").Value)
        do_uio_rly_nr = getInt(Product.GetContainerByName('SM_RG_IO_Count_Digital_Output_Cont').Rows[0].GetColumnByName("Non_Red_RLY").Value)
        
        do_linemon_uio = getInt(Product.GetContainerByName('SM_RG_IO_Count_Digital_Output_Cont').Rows[3].GetColumnByName("Red_IS").Value)
        do_linemon_uio_nis = getInt(Product.GetContainerByName('SM_RG_IO_Count_Digital_Output_Cont').Rows[3].GetColumnByName("Red_NIS").Value)
        do_linemon_uio_nr = getInt(Product.GetContainerByName('SM_RG_IO_Count_Digital_Output_Cont').Rows[3].GetColumnByName("Non_Red_IS").Value)
        do_linemon_uio_nis_nr = getInt(Product.GetContainerByName('SM_RG_IO_Count_Digital_Output_Cont').Rows[3].GetColumnByName("Non_Red_NIS").Value)
        
        do_sil23_uio_nis = getInt(Product.GetContainerByName('SM_RG_IO_Count_Digital_Output_Cont').Rows[4].GetColumnByName("Red_NIS").Value)
        do_sil23_uio_nis_nr = getInt(Product.GetContainerByName('SM_RG_IO_Count_Digital_Output_Cont').Rows[4].GetColumnByName("Non_Red_NIS").Value)
        
        do_sil23_com_uio_nis = getInt(Product.GetContainerByName('SM_RG_IO_Count_Digital_Output_Cont').Rows[5].GetColumnByName("Red_NIS").Value)
        do_sil23_com_uio_nis_nr = getInt(Product.GetContainerByName('SM_RG_IO_Count_Digital_Output_Cont').Rows[5].GetColumnByName("Non_Red_NIS").Value)

        do_1A_io_nis = getInt(Product.GetContainerByName('SM_RG_IO_Count_Digital_Output_Cont').Rows[1].GetColumnByName("Red_NIS").Value)
        do_1A_io_nis_nr = getInt(Product.GetContainerByName('SM_RG_IO_Count_Digital_Output_Cont').Rows[1].GetColumnByName("Non_Red_NIS").Value)

        do_2A_io_nis = getInt(Product.GetContainerByName('SM_RG_IO_Count_Digital_Output_Cont').Rows[2].GetColumnByName("Red_NIS").Value)
        do_2A_io_nis_nr = getInt(Product.GetContainerByName('SM_RG_IO_Count_Digital_Output_Cont').Rows[2].GetColumnByName("Non_Red_NIS").Value)
        
        powerload_A_rg = 0.0
        if power_supply == "Redundant":
            val_1 = float(((ai_uio + ai_uio_nis)*25) + 600)
            val_2 = float(((ai_fire2_uio + ai_fire2_uio_nis)*25) + 600)
            val_3 = float(((ai_fire34_uio + ai_fire34_uio_nis + ai_fire34_sink_uio + ai_fire34_sink_uio_nis)*25) + 600)
            val_4 = float(((ai_gas_uio + ai_gas_uio_nis)*25) + 600)
            val_5 = float(((ao_uio + ao_uio_nis)*25) + 600)
            val_6 = float(((di_uio + di_uio_nis + di_uio_rly + di_uio_sil2_rly + di_uio_sil3_rly + di_uio_nmr_rly + di_uio_nmr_safety_rly + di_5k_resistor_uio + di_5k_resistor_uio_nis + di_5k_resistor_uio_rly)*7) + 600)
            val_7 = float(((di_linemon_uio + di_linemon_uio_nis)*7) + 600)
            if unit_load:
                ul = int(unit_load)
            else:
                ul = 250
            if ui_L_1:
                unit_Load1 = int(ui_L_1)
            else:
                unit_Load1 = 750
            if ui_L_2:
                unit_Load2 = int(ui_L_2)
            else:
                unit_Load2 = 1500
            val_8 = float(((do_uio + do_uio_nis)*ul) + 600)
            val_9 = float(((do_linemon_uio + do_linemon_uio_nis)*30) + 600)
            val_10 = float((do_sil23_uio_nis*40) + 600)
            val_11 = float((do_sil23_com_uio_nis*40) + 600)
            val_12 = float(((do_1A_io_nis) *unit_Load1) + 600)
            val_13 = float(((do_2A_io_nis) *unit_Load2) + 600)
            powerload_A_rg = val_1 + val_2 + val_3 + val_4 + val_5 + val_6 + val_7 + val_8 + val_9 + val_10 +val_11 +val_12 + val_13
        elif power_supply == "Non Redundant":
            val_1 = float(((ai_uio_nr + ai_uio_nis_nr)*25) + 300)
            val_2 = float(((ai_fire2_uio_nr + ai_fire2_uio_nis_nr)*25) + 300)
            val_3 = float(((ai_fire34_uio_nr + ai_fire34_uio_nis_nr + ai_fire34_sink_uio_nr + ai_fire34_sink_uio_nis_nr)*25) + 300)
            val_4 = float(((ai_gas_uio_nr + ai_gas_uio_nis_nr)*25) + 300)
            val_5 = float(((ao_uio_nr + ao_uio_nis_nr)*25) + 300)
            val_6 = float(((di_uio_nr + di_uio_nis_nr + di_uio_rly_nr + di_uio_sil2_rly_nr + di_uio_sil3_rly_nr + di_uio_nmr_rly_nr + di_uio_nmr_safety_rly_nr + di_5k_resistor_uio_nr + di_5k_resistor_uio_nis_nr + di_5k_resistor_uio_rly_nr)*7) + 300)
            val_7 = float(((di_linemon_uio_nr + di_linemon_uio_nis_nr)*7) + 300)
            if unit_load:
                ul = int(unit_load)
            else:
                ul = 250
            if ui_L_1:
                unit_Load1 = int(ui_L_1)
            else:
                unit_Load1 = 750
            if ui_L_2:
                unit_Load2 = int(ui_L_2)
            else:
                unit_Load2 = 1500
            val_8 = float(((do_uio_nr + do_uio_nis_nr)*ul) + 300)
            val_9 = float(((do_linemon_uio_nr + do_linemon_uio_nis_nr)*30) + 300)
            val_10 = float((do_sil23_uio_nis_nr*40) + 300)
            val_11 = float((do_sil23_com_uio_nis_nr*40) + 300)
            val_12 = float(((do_1A_io_nis_nr)*unit_Load1) + 300)
            val_13 = float(((do_2A_io_nis_nr) *unit_Load2) + 300)
            powerload_A_rg = val_1 + val_2 + val_3 + val_4 + val_5 + val_6 + val_7 + val_8 + val_9 + val_10 + val_11+val_12 +val_13
        
        return round(powerload_A_rg, 2)
    else:
        Trace.Write("Product is neither SM Control Group nor SM Remote Group")
        return 0.0