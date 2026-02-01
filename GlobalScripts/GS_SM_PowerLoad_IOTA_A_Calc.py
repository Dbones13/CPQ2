#CXCPQ-31144
class IOComponents:
    def __init__(self, Product):
        self.Product  = Product
        
    def getRowIndex(self, container, column_name, column_value):
        row_index = -1
        for cont_row in container.Rows:
            if column_value == cont_row.GetColumnByName(column_name).Value:
                row_index = cont_row.RowIndex
                break
        return row_index

    def getColumnValue(self, container, row_index, column_name):
        val = 0
        if row_index < 0:
            return 0
        try:
            if container.Rows.Count:
                val = container.Rows[row_index].GetColumnByName(column_name).Value
                if val:
                    val = float(val)
                else:
                    val = 0
        except Exception as e:
            Trace.Write(str(e))
            return 0
        return val

def PowerLoad_IOTA_A_Calc(Prod):
    if Prod.Name == "SM Control Group":
        IOComp = IOComponents(Prod)
        Trace.Write("SM Control Group")
        '''cg_cont_list = ['SM_IO_Count_Digital_Input_Cont', 'SM_IO_Count_Digital_Output_Cont', 'SM_IO_Count_Analog_Input_Cont', 'SM_IO_Count_Analog_Output_Cont']
        type_ques_list = {'Analog Input Type' : ['SAI(1)mA type Current UIO (0-5000)', 'SAI(1)FIRE 2 wire current UIO (0-5000)', 'SAI(1)FIRE 3-4 wire current UIO (0-5000)', 'SAI(1)FIRE 3-4 wire current Sink UIO (0-5000)', 'SAI(1) GAS current UIO (0-5000)'],
        'Analog Output Type' : ['SAO(1)mA Type UIO (0-5000)'],
        'Digital Input Type' : ['SDI(1) 24Vdc UIO (0-5000)', 'SDI(1) 24Vdc with 5K Resistor UIO (0-5000)', 'SDI(1) 24Vdc Line Mon UIO (0-5000)'],
        'Digital Output Type' : ['SDO(1) 24Vdc 500mA UIO (0-5000)', 'SDO(7) 24Vdc Line Mon UIO (0-5000)', 'SDO(16) SIL 2/3 250Vac/Vdc UIO (0-5000)', 'SDO(16) SIL 2/3 250Vac/Vdc COM UIO (0-5000)']
        }'''
        
        #power_supply = Prod.GetContainerByName('SM_CG_Cabinet_Details_Cont_Left').Rows[0].GetColumnByName("Power_Supply").DisplayValue
        try:
            unit_load = Prod.GetContainerByName('SM_CG_Cabinet_Details_Cont_Right').Rows[0].GetColumnByName("SDO_24Vdc_500mA_UIO_DIO_UnitLoad1mA-500mA").Value
        except:
            unit_load = ""
        try:
            di_do_relay = Prod.GetContainerByName('SM_CG_Cabinet_Details_Cont_Right').Rows[0].GetColumnByName("DI/DO_SIL2/3_Relay_Adapter_UMC").DisplayValue
        except:
            di_do_relay = ""
        try:
            namur = Prod.GetContainerByName('SM_CG_Cabinet_Details_Cont_Right').Rows[0].GetColumnByName("DI_NAMUR_proximity_Switches_Adapter_UMC").DisplayValue
        except:
            namur = ""
        
        
        # AI
        cont = IOComp.Product.GetContainerByName('SM_IO_Count_Analog_Input_Cont')
        row_index = IOComp.getRowIndex(cont, 'Analog Input Type', 'SAI(1)mA type Current UIO (0-5000)')
        ai_uio = IOComp.getColumnValue(cont, row_index, "Red (IS)")
        Trace.Write("AI uio = "+str(ai_uio))
        ai_uio_nis = IOComp.getColumnValue(cont, row_index, "Red (NIS)")
        ai_uio_nr = IOComp.getColumnValue(cont, row_index, "Non Red (IS)")
        ai_uio_nis_nr = IOComp.getColumnValue(cont, row_index, "Non Red (NIS)")
        
        row_index = IOComp.getRowIndex(cont, 'Analog Input Type', 'SAI(1)FIRE 2 wire current UIO (0-5000)')
        ai_fire2_uio = IOComp.getColumnValue(cont, row_index, "Red (IS)")
        Trace.Write("AI fire 2 uio = "+str(ai_fire2_uio))
        ai_fire2_uio_nis = IOComp.getColumnValue(cont, row_index, "Red (NIS)")
        ai_fire2_uio_nr = IOComp.getColumnValue(cont, row_index, "Non Red (IS)")
        ai_fire2_uio_nis_nr = IOComp.getColumnValue(cont, row_index, "Non Red (NIS)")
        
        row_index = IOComp.getRowIndex(cont, 'Analog Input Type', 'SAI(1)FIRE 3-4 wire current UIO (0-5000)')
        ai_fire34_uio = IOComp.getColumnValue(cont, row_index, "Red (IS)")
        Trace.Write("AI fire 34 uio = "+str(ai_fire34_uio))
        ai_fire34_uio_nis = IOComp.getColumnValue(cont, row_index, "Red (NIS)")
        ai_fire34_uio_nr = IOComp.getColumnValue(cont, row_index, "Non Red (IS)")
        ai_fire34_uio_nis_nr = IOComp.getColumnValue(cont, row_index, "Non Red (NIS)")
        
        row_index = IOComp.getRowIndex(cont, 'Analog Input Type', 'SAI(1)FIRE 3-4 wire current Sink UIO (0-5000)')
        ai_fire34_sink_uio = IOComp.getColumnValue(cont, row_index, "Red (IS)")
        Trace.Write("AI fire 34 sink uio = "+str(ai_fire34_sink_uio))
        ai_fire34_sink_uio_nis = IOComp.getColumnValue(cont, row_index, "Red (NIS)")
        ai_fire34_sink_uio_nr = IOComp.getColumnValue(cont, row_index, "Non Red (IS)")
        ai_fire34_sink_uio_nis_nr = IOComp.getColumnValue(cont, row_index, "Non Red (NIS)")
        
        row_index = IOComp.getRowIndex(cont, 'Analog Input Type', 'SAI(1) GAS current UIO (0-5000)')
        ai_gas_uio = IOComp.getColumnValue(cont, row_index, "Red (IS)")
        Trace.Write("AI gas uio = "+str(ai_gas_uio))
        ai_gas_uio_nis = IOComp.getColumnValue(cont, row_index, "Red (NIS)")
        ai_gas_uio_nr = IOComp.getColumnValue(cont, row_index, "Non Red (IS)")
        ai_gas_uio_nis_nr = IOComp.getColumnValue(cont, row_index, "Non Red (NIS)")
                
        # AO
        cont = IOComp.Product.GetContainerByName('SM_IO_Count_Analog_Output_Cont')
        row_index = IOComp.getRowIndex(cont, 'Analog Output Type', 'SAO(1)mA Type UIO (0-5000)')
        ao_uio = IOComp.getColumnValue(cont, row_index, "Red (IS)")
        Trace.Write("AO uio = "+str(ao_uio))
        ao_uio_nis = IOComp.getColumnValue(cont, row_index, "Red (NIS)")
        ao_uio_nr = IOComp.getColumnValue(cont, row_index, "Non Red (IS)")
        ao_uio_nis_nr = IOComp.getColumnValue(cont, row_index, "Non Red (NIS)")
                
        #DI
        cont = IOComp.Product.GetContainerByName('SM_IO_Count_Digital_Input_Cont')
        row_index = IOComp.getRowIndex(cont, 'Digital Input Type', 'SDI(1) 24Vdc UIO (0-5000)')
        di_uio = IOComp.getColumnValue(cont, row_index, "Red (IS)")
        Trace.Write("DI uio = "+str(di_uio))
        di_uio_nis = IOComp.getColumnValue(cont, row_index, "Red (NIS)")
        di_uio_nr = IOComp.getColumnValue(cont, row_index, "Non Red (IS)")
        di_uio_nis_nr = IOComp.getColumnValue(cont, row_index, "Non Red (NIS)")
        di_uio_rly = IOComp.getColumnValue(cont, row_index, "Red (RLY)")
        di_uio_rly_nr = IOComp.getColumnValue(cont, row_index, "Non Red (RLY)")
        
        if di_do_relay == 'Yes' or namur == 'Yes':
            Trace.Write("DI/DO and Namur set to Yes")
            cont = IOComp.Product.GetContainerByName('SM_CG_DI_RLY_NMR_Cont')
            row_index = IOComp.getRowIndex(cont, 'Digital Input Type', 'SDI(1) 24Vdc UIO (0-5000)')
            di_uio_sil2_rly = IOComp.getColumnValue(cont, row_index, "Red_SIL2_RLY")
            Trace.Write("DI Sil2 rly uio = "+str(di_uio_sil2_rly))
            di_uio_sil3_rly = IOComp.getColumnValue(cont, row_index, "Red_SIL3_RLY")
            di_uio_nmr_rly = IOComp.getColumnValue(cont, row_index, "Red_NMR")
            di_uio_nmr_safety_rly = IOComp.getColumnValue(cont, row_index, "Red_NMR_Safety")
            di_uio_sil2_rly_nr = IOComp.getColumnValue(cont, row_index, "Non_Red_SIL2_RLY")
            di_uio_sil3_rly_nr = IOComp.getColumnValue(cont, row_index, "Non_Red_SIL3_RLY")
            di_uio_nmr_rly_nr = IOComp.getColumnValue(cont, row_index, "Non_Red_NMR")
            di_uio_nmr_safety_rly_nr = IOComp.getColumnValue(cont, row_index, "Non_Red_NMR_Safety")
        else:
            di_uio_sil2_rly = 0
            di_uio_sil3_rly = 0
            di_uio_nmr_rly = 0
            di_uio_nmr_safety_rly = 0
            di_uio_sil2_rly_nr = 0
            di_uio_sil3_rly_nr = 0
            di_uio_nmr_rly_nr = 0
            di_uio_nmr_safety_rly_nr = 0
        
        cont = IOComp.Product.GetContainerByName('SM_IO_Count_Digital_Input_Cont')
        row_index = IOComp.getRowIndex(cont, 'Digital Input Type', 'SDI(1) 24Vdc with 5K Resistor UIO (0-5000)')
        di_5k_resistor_uio = IOComp.getColumnValue(cont, row_index, "Red (IS)")
        Trace.Write("DI 5K resistor uio = "+str(di_5k_resistor_uio))
        di_5k_resistor_uio_nis = IOComp.getColumnValue(cont, row_index, "Red (NIS)")
        di_5k_resistor_uio_rly = IOComp.getColumnValue(cont, row_index, "Red (RLY)")
        di_5k_resistor_uio_nr = IOComp.getColumnValue(cont, row_index, "Non Red (IS)")
        di_5k_resistor_uio_nis_nr = IOComp.getColumnValue(cont, row_index, "Non Red (NIS)")
        di_5k_resistor_uio_rly_nr = IOComp.getColumnValue(cont, row_index, "Non Red (RLY)")
                
        
        row_index = IOComp.getRowIndex(cont, 'Digital Input Type', 'SDI(1) 24Vdc Line Mon UIO (0-5000)')
        di_linemon_uio = IOComp.getColumnValue(cont, row_index, "Red (IS)")
        Trace.Write("DI Linemon uio = "+str(di_linemon_uio))
        di_linemon_uio_nis = IOComp.getColumnValue(cont, row_index, "Red (NIS)")
        di_linemon_uio_nr = IOComp.getColumnValue(cont, row_index, "Non Red (IS)")
        di_linemon_uio_nis_nr = IOComp.getColumnValue(cont, row_index, "Non Red (NIS)")
        
        #DO
        cont = IOComp.Product.GetContainerByName('SM_IO_Count_Digital_Output_Cont')
        row_index = IOComp.getRowIndex(cont, 'Digital Output Type', 'SDO(1) 24Vdc 500mA UIO (0-5000)')
        do_uio = IOComp.getColumnValue(cont, row_index, "Red (IS)")
        Trace.Write("DO uio = "+str(do_uio))
        do_uio_nis = IOComp.getColumnValue(cont, row_index, "Red (NIS)")
        do_uio_rly = IOComp.getColumnValue(cont, row_index, "Red (RLY)")
        do_uio_nr = IOComp.getColumnValue(cont, row_index, "Non Red (IS)")
        do_uio_nis_nr = IOComp.getColumnValue(cont, row_index, "Non Red (NIS)")
        do_uio_rly_nr = IOComp.getColumnValue(cont, row_index, "Non Red (RLY)")
        
        row_index = IOComp.getRowIndex(cont, 'Digital Output Type', 'SDO(7) 24Vdc Line Mon UIO (0-5000)')
        do_linemon_uio = IOComp.getColumnValue(cont, row_index, "Red (IS)")
        Trace.Write("DO Linemon uio = "+str(do_linemon_uio))
        do_linemon_uio_nis = IOComp.getColumnValue(cont, row_index, "Red (NIS)")
        do_linemon_uio_nr = IOComp.getColumnValue(cont, row_index, "Non Red (IS)")
        do_linemon_uio_nis_nr = IOComp.getColumnValue(cont, row_index, "Non Red (NIS)")
        
        row_index = IOComp.getRowIndex(cont, 'Digital Output Type', 'SDO(16) SIL 2/3 250Vac/Vdc UIO (0-5000)')
        do_sil23_uio_nis = IOComp.getColumnValue(cont, row_index, "Red (NIS)")
        Trace.Write("DO Sil23 uio = "+str(do_sil23_uio_nis))
        do_sil23_uio_nis_nr = IOComp.getColumnValue(cont, row_index, "Non Red (NIS)")
        
        row_index = IOComp.getRowIndex(cont, 'Digital Output Type', 'SDO(16) SIL 2/3 250Vac/Vdc COM UIO (0-5000)')
        do_sil23_com_uio_nis = IOComp.getColumnValue(cont, row_index, "Red (NIS)")
        Trace.Write("DO Sil23 Com uio = "+str(do_sil23_com_uio_nis))
        do_sil23_com_uio_nis_nr = IOComp.getColumnValue(cont, row_index, "Non Red (NIS)")
                
        powerload_A_cg = 0.0
        val_1 = float((ai_uio + ai_uio_nis)*25)
        val_2 = float((ai_fire2_uio + ai_fire2_uio_nis)*25)
        val_3 = float((ai_fire34_uio + ai_fire34_uio_nis + ai_fire34_sink_uio + ai_fire34_sink_uio_nis)*25)
        val_4 = float((ai_gas_uio + ai_gas_uio_nis)*25)
        val_5 = float((ao_uio + ao_uio_nis)*25)
        val_6 = float((di_uio + di_uio_nis + di_uio_rly + di_uio_sil2_rly + di_uio_sil3_rly + di_uio_nmr_rly + di_uio_nmr_safety_rly + di_5k_resistor_uio + di_5k_resistor_uio_nis + di_5k_resistor_uio_rly)*7)
        val_7 = float((di_linemon_uio + di_linemon_uio_nis)*7)
        if unit_load:
            ul = int(unit_load)
        else:
            ul = 250
        Trace.Write("Unit Load = "+str(ul))
        val_8 = float((do_uio + do_uio_nis)*ul)
        val_9 = float((do_linemon_uio + do_linemon_uio_nis)*30)
        val_10 = float(do_sil23_uio_nis*40)
        val_11 = float(do_sil23_com_uio_nis*40)
        val_red = val_1 + val_2 + val_3 + val_4 + val_5 + val_6 + val_7 + val_8 + val_9 + val_10 + val_11
        if val_red > 0:
            powerload_A_cg = val_red + 600
        
        val_1 = float((ai_uio_nr + ai_uio_nis_nr)*25)
        val_2 = float((ai_fire2_uio_nr + ai_fire2_uio_nis_nr)*25)
        val_3 = float((ai_fire34_uio_nr + ai_fire34_uio_nis_nr + ai_fire34_sink_uio_nr + ai_fire34_sink_uio_nis_nr)*25)
        val_4 = float((ai_gas_uio_nr + ai_gas_uio_nis_nr)*25)
        val_5 = float((ao_uio_nr + ao_uio_nis_nr)*25)
        val_6 = float((di_uio_nr + di_uio_nis_nr + di_uio_rly_nr + di_uio_sil2_rly_nr + di_uio_sil3_rly_nr + di_uio_nmr_rly_nr + di_uio_nmr_safety_rly_nr + di_5k_resistor_uio_nr + di_5k_resistor_uio_nis_nr + di_5k_resistor_uio_rly_nr)*7)
        val_7 = float((di_linemon_uio_nr + di_linemon_uio_nis_nr)*7)
        Trace.Write("Unit Load = "+str(ul))
        val_8 = float((do_uio_nr + do_uio_nis_nr)*ul)
        val_9 = float((do_linemon_uio_nr + do_linemon_uio_nis_nr)*30)
        val_10 = float(do_sil23_uio_nis_nr*40)
        val_11 = float(do_sil23_com_uio_nis_nr*40)
        val_non_red = val_1 + val_2 + val_3 + val_4 + val_5 + val_6 + val_7 + val_8 + val_9 + val_10 + val_11
        if val_non_red > 0:
            powerload_A_cg = powerload_A_cg + val_non_red + 300
                        
        return round(powerload_A_cg, 2)
    elif Prod.Name == "SM Remote Group":
        Trace.Write("SM Remote Group")
        IOComp = IOComponents(Prod)
        #power_supply = Prod.GetContainerByName('SM_RG_Cabinet_Details_Cont_Left').Rows[0].GetColumnByName("Power_Supply").DisplayValue
        try:
            unit_load = Prod.GetContainerByName('SM_RG_Cabinet_Details_Cont').Rows[0].GetColumnByName("SM_SDO_UIO_DIO").Value
        except:
            unit_load = ""
        try:
            di_do_relay = Prod.GetContainerByName('SM_RG_Cabinet_Details_Cont').Rows[0].GetColumnByName("SM_DI_DORelay_Adapter_UMC").DisplayValue
        except:
            di_do_relay = ""
        try:
            namur = Prod.GetContainerByName('SM_RG_Cabinet_Details_Cont').Rows[0].GetColumnByName("SM_DI_NAMUR_Switches_Adapter_UMC").DisplayValue
        except:
            namur = ""
        # AI
        cont = IOComp.Product.GetContainerByName('SM_RG_IO_Count_Analog_Input_Cont')
        row_index = IOComp.getRowIndex(cont, 'Analog_Input_Type', 'SAI(1)mA type Current  UIO  (0-5000)')
        ai_uio = IOComp.getColumnValue(cont, row_index, "Red_IS")
        Trace.Write("AI uio = "+str(ai_uio))
        ai_uio_nis = IOComp.getColumnValue(cont, row_index, "Red_NIS")
        ai_uio_nr = IOComp.getColumnValue(cont, row_index, "Non_Red_IS")
        ai_uio_nis_nr = IOComp.getColumnValue(cont, row_index, "Non_Red_NIS")
        
        row_index = IOComp.getRowIndex(cont, 'Analog_Input_Type', 'SAI(1)FIRE 2 wire current  UIO   (0-5000)')
        ai_fire2_uio = IOComp.getColumnValue(cont, row_index, "Red_IS")
        Trace.Write("AI fire 2 uio = "+str(ai_fire2_uio))
        ai_fire2_uio_nis = IOComp.getColumnValue(cont, row_index, "Red_NIS")
        ai_fire2_uio_nr = IOComp.getColumnValue(cont, row_index, "Non_Red_IS")
        ai_fire2_uio_nis_nr = IOComp.getColumnValue(cont, row_index, "Non_Red_NIS")
        
        row_index = IOComp.getRowIndex(cont, 'Analog_Input_Type', 'SAI(1)FIRE 3-4 wire current  UIO  (0-5000)')
        ai_fire34_uio = IOComp.getColumnValue(cont, row_index, "Red_IS")
        Trace.Write("AI fire 34 uio = "+str(ai_fire34_uio))
        ai_fire34_uio_nis = IOComp.getColumnValue(cont, row_index, "Red_NIS")
        ai_fire34_uio_nr = IOComp.getColumnValue(cont, row_index, "Non_Red_IS")
        ai_fire34_uio_nis_nr = IOComp.getColumnValue(cont, row_index, "Non_Red_NIS")
        
        row_index = IOComp.getRowIndex(cont, 'Analog_Input_Type', 'SAI(1)FIRE 3-4 wire current  Sink UIO  (0-5000)')
        ai_fire34_sink_uio = IOComp.getColumnValue(cont, row_index, "Red_IS")
        Trace.Write("AI fire 34 sink uio = "+str(ai_fire34_sink_uio))
        ai_fire34_sink_uio_nis = IOComp.getColumnValue(cont, row_index, "Red_NIS")
        ai_fire34_sink_uio_nr = IOComp.getColumnValue(cont, row_index, "Non_Red_IS")
        ai_fire34_sink_uio_nis_nr = IOComp.getColumnValue(cont, row_index, "Non_Red_NIS")
        
        row_index = IOComp.getRowIndex(cont, 'Analog_Input_Type', 'SAI(1) GAS current  UIO  (0-5000)')
        ai_gas_uio = IOComp.getColumnValue(cont, row_index, "Red_IS")
        Trace.Write("AI gas uio = "+str(ai_gas_uio))
        ai_gas_uio_nis = IOComp.getColumnValue(cont, row_index, "Red_NIS")
        ai_gas_uio_nr = IOComp.getColumnValue(cont, row_index, "Non_Red_IS")
        ai_gas_uio_nis_nr = IOComp.getColumnValue(cont, row_index, "Non_Red_NIS")
                
        # AO
        cont = IOComp.Product.GetContainerByName('SM_RG_IO_Count_Analog_Output_Cont')
        row_index = IOComp.getRowIndex(cont, 'Analog_Output_Type', 'SAO(1)mA Type UIO   (0-5000)')
        ao_uio = IOComp.getColumnValue(cont, row_index, "Red_IS")
        Trace.Write("AO uio = "+str(ao_uio))
        ao_uio_nis = IOComp.getColumnValue(cont, row_index, "Red_NIS")
        ao_uio_nr = IOComp.getColumnValue(cont, row_index, "Non_Red_IS")
        ao_uio_nis_nr = IOComp.getColumnValue(cont, row_index, "Non_Red_NIS")
                
        #DI
        cont = IOComp.Product.GetContainerByName('SM_RG_IO_Count_Digital_Input_Cont')
        row_index = IOComp.getRowIndex(cont, 'Digital_Input_Type', 'SDI(1) 24Vdc UIO  (0-5000)')
        di_uio = IOComp.getColumnValue(cont, row_index, "Red_IS")
        Trace.Write("DI uio = "+str(di_uio))
        di_uio_nis = IOComp.getColumnValue(cont, row_index, "Red_NIS")
        di_uio_nr = IOComp.getColumnValue(cont, row_index, "Non_Red_IS")
        di_uio_nis_nr = IOComp.getColumnValue(cont, row_index, "Non_Red_NIS")
        di_uio_rly = IOComp.getColumnValue(cont, row_index, "Red_RLY")
        di_uio_rly_nr = IOComp.getColumnValue(cont, row_index, "Non_Red_RLY")
        
        if di_do_relay == 'Yes' or namur == 'Yes':
            Trace.Write("DI/DO and Namur set to Yes")
            cont = IOComp.Product.GetContainerByName('SM_RG_DI_RLY_NMR_Cont')
            row_index = IOComp.getRowIndex(cont, 'Digital Input Type', 'SDI(1) 24Vdc UIO (0-5000)')
            di_uio_sil2_rly = IOComp.getColumnValue(cont, row_index, "Red_SIL2_RLY")
            Trace.Write("DI Sil2 rly uio = "+str(di_uio_sil2_rly))
            di_uio_sil3_rly = IOComp.getColumnValue(cont, row_index, "Red_SIL3_RLY")
            Trace.Write("DI Sil3 rly uio = "+str(di_uio_sil3_rly))
            di_uio_nmr_rly = IOComp.getColumnValue(cont, row_index, "Red_NMR")
            di_uio_nmr_safety_rly = IOComp.getColumnValue(cont, row_index, "Red_NMR_Safety")
            di_uio_sil2_rly_nr = IOComp.getColumnValue(cont, row_index, "Non_Red_SIL2_RLY")
            di_uio_sil3_rly_nr = IOComp.getColumnValue(cont, row_index, "Non_Red_SIL3_RLY")
            di_uio_nmr_rly_nr = IOComp.getColumnValue(cont, row_index, "Non_Red_NMR")
            di_uio_nmr_safety_rly_nr = IOComp.getColumnValue(cont, row_index, "Non_Red_NMR_Safety")
        else:
            di_uio_sil2_rly = 0
            di_uio_sil3_rly = 0
            di_uio_nmr_rly = 0
            di_uio_nmr_safety_rly = 0
            di_uio_sil2_rly_nr = 0
            di_uio_sil3_rly_nr = 0
            di_uio_nmr_rly_nr = 0
            di_uio_nmr_safety_rly_nr = 0
        
        cont = IOComp.Product.GetContainerByName('SM_RG_IO_Count_Digital_Input_Cont')
        row_index = IOComp.getRowIndex(cont, 'Digital_Input_Type', 'SDI(1) 24Vdc with 5K Resistor UIO  (0-5000)')
        di_5k_resistor_uio = IOComp.getColumnValue(cont, row_index, "Red_IS")
        Trace.Write("DI 5K resistor uio = "+str(di_5k_resistor_uio))
        di_5k_resistor_uio_nis = IOComp.getColumnValue(cont, row_index, "Red_NIS")
        di_5k_resistor_uio_rly = IOComp.getColumnValue(cont, row_index, "Red_RLY")
        di_5k_resistor_uio_nr = IOComp.getColumnValue(cont, row_index, "Non_Red_IS")
        di_5k_resistor_uio_nis_nr = IOComp.getColumnValue(cont, row_index, "Non_Red_NIS")
        di_5k_resistor_uio_rly_nr = IOComp.getColumnValue(cont, row_index, "Non_Red_RLY")
                
        
        row_index = IOComp.getRowIndex(cont, 'Digital_Input_Type', 'SDI(1) 24Vdc Line Mon UIO  (0-5000)')
        di_linemon_uio = IOComp.getColumnValue(cont, row_index, "Red_IS")
        Trace.Write("DI Linemon uio = "+str(di_linemon_uio))
        di_linemon_uio_nis = IOComp.getColumnValue(cont, row_index, "Red_NIS")
        di_linemon_uio_nr = IOComp.getColumnValue(cont, row_index, "Non_Red_IS")
        di_linemon_uio_nis_nr = IOComp.getColumnValue(cont, row_index, "Non_Red_NIS")
        
        #DO
        cont = IOComp.Product.GetContainerByName('SM_RG_IO_Count_Digital_Output_Cont')
        row_index = IOComp.getRowIndex(cont, 'Digital_Output_Type', 'SDO(1) 24Vdc 500mA UIO  (0-5000)')
        do_uio = IOComp.getColumnValue(cont, row_index, "Red_IS")
        Trace.Write("DO uio = "+str(do_uio))
        do_uio_nis = IOComp.getColumnValue(cont, row_index, "Red_NIS")
        do_uio_rly = IOComp.getColumnValue(cont, row_index, "Red_RLY")
        do_uio_nr = IOComp.getColumnValue(cont, row_index, "Non_Red_IS")
        do_uio_nis_nr = IOComp.getColumnValue(cont, row_index, "Non_Red_NIS")
        do_uio_rly_nr = IOComp.getColumnValue(cont, row_index, "Non_Red_RLY")
        
        row_index = IOComp.getRowIndex(cont, 'Digital_Output_Type', 'SDO(7) 24Vdc Line Mon UIO  (0-5000)')
        do_linemon_uio = IOComp.getColumnValue(cont, row_index, "Red_IS")
        Trace.Write("DO Linemon uio = "+str(do_linemon_uio))
        do_linemon_uio_nis = IOComp.getColumnValue(cont, row_index, "Red_NIS")
        do_linemon_uio_nr = IOComp.getColumnValue(cont, row_index, "Non_Red_IS")
        do_linemon_uio_nis_nr = IOComp.getColumnValue(cont, row_index, "Non_Red_NIS")
        
        row_index = IOComp.getRowIndex(cont, 'Digital_Output_Type', 'SDO(16) SIL 2/3 250Vac/Vdc UIO   (0-5000)')
        do_sil23_uio_nis = IOComp.getColumnValue(cont, row_index, "Red_NIS")
        Trace.Write("DO Sil23 uio = "+str(do_sil23_uio_nis))
        do_sil23_uio_nis_nr = IOComp.getColumnValue(cont, row_index, "Non_Red_NIS")
        
        row_index = IOComp.getRowIndex(cont, 'Digital_Output_Type', 'SDO(16) SIL 2/3 250Vac/Vdc COM UIO  (0-5000)')
        do_sil23_com_uio_nis = IOComp.getColumnValue(cont, row_index, "Red_NIS")
        Trace.Write("DO Sil23 Com uio = "+str(do_sil23_com_uio_nis))
        do_sil23_com_uio_nis_nr = IOComp.getColumnValue(cont, row_index, "Non_Red_NIS")
                
        powerload_A_rg = 0.0
        val_1 = float((ai_uio + ai_uio_nis)*25)
        val_2 = float((ai_fire2_uio + ai_fire2_uio_nis)*25)
        val_3 = float((ai_fire34_uio + ai_fire34_uio_nis + ai_fire34_sink_uio + ai_fire34_sink_uio_nis)*25)
        val_4 = float((ai_gas_uio + ai_gas_uio_nis)*25)
        val_5 = float((ao_uio + ao_uio_nis)*25)
        val_6 = float((di_uio + di_uio_nis + di_uio_rly + di_uio_sil2_rly + di_uio_sil3_rly + di_uio_nmr_rly + di_uio_nmr_safety_rly + di_5k_resistor_uio + di_5k_resistor_uio_nis + di_5k_resistor_uio_rly)*7)
        val_7 = float((di_linemon_uio + di_linemon_uio_nis)*7)
        if unit_load:
            ul = int(unit_load)
        else:
            ul = 250
        Trace.Write("Unit Load = "+str(ul))
        val_8 = float((do_uio + do_uio_nis)*ul)
        val_9 = float((do_linemon_uio + do_linemon_uio_nis)*30)
        val_10 = float(do_sil23_uio_nis*40)
        val_11 = float(do_sil23_com_uio_nis*40)
        val_red = val_1 + val_2 + val_3 + val_4 + val_5 + val_6 + val_7 + val_8 + val_9 + val_10 + val_11
        if val_red > 0:
            powerload_A_rg = val_red + 600
        
        val_1 = float((ai_uio_nr + ai_uio_nis_nr)*25)
        val_2 = float((ai_fire2_uio_nr + ai_fire2_uio_nis_nr)*25)
        val_3 = float((ai_fire34_uio_nr + ai_fire34_uio_nis_nr + ai_fire34_sink_uio_nr + ai_fire34_sink_uio_nis_nr)*25)
        val_4 = float((ai_gas_uio_nr + ai_gas_uio_nis_nr)*25)
        val_5 = float((ao_uio_nr + ao_uio_nis_nr)*25)
        val_6 = float((di_uio_nr + di_uio_nis_nr + di_uio_rly_nr + di_uio_sil2_rly_nr + di_uio_sil3_rly_nr + di_uio_nmr_rly_nr + di_uio_nmr_safety_rly_nr + di_5k_resistor_uio_nr + di_5k_resistor_uio_nis_nr + di_5k_resistor_uio_rly_nr)*7)
        val_7 = float((di_linemon_uio_nr + di_linemon_uio_nis_nr)*7)
        Trace.Write("Unit Load = "+str(ul))
        val_8 = float((do_uio_nr + do_uio_nis_nr)*ul)
        val_9 = float((do_linemon_uio_nr + do_linemon_uio_nis_nr)*30)
        val_10 = float(do_sil23_uio_nis_nr*40)
        val_11 = float(do_sil23_com_uio_nis_nr*40)
        val_non_red = val_1 + val_2 + val_3 + val_4 + val_5 + val_6 + val_7 + val_8 + val_9 + val_10 + val_11
        if val_non_red > 0:
            powerload_A_rg = powerload_A_rg + val_non_red + 300
                
        return round(powerload_A_rg, 2)
        
    else:
        Trace.Write("Product is neither SM Control Group nor SM Remote Group")
        return 0.0