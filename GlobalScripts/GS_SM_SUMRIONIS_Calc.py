#CXCPQ-31165
import System.Decimal as D
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

def SUMRIONIS_Calc(Prod):
    if Prod.Name == "SM Control Group":
        Trace.Write("SM Control Group")
        iota_type = ''
        if Prod.GetContainerByName('SM_CG_Common_Questions_Cont').Rows.Count > 0:
            iota_type = Prod.GetContainerByName('SM_CG_Common_Questions_Cont').Rows[0].GetColumnByName("SM_Universal_IOTA").Value
        if iota_type != 'RUSIO':
            Trace.Write("Universal IOTA is not RUSIO. Returning 0")
            return 0
        sumrionis_cg = 0.0
        IOComp = IOComponents(Prod)

        # AI
        cont = IOComp.Product.GetContainerByName('SM_IO_Count_Analog_Input_Cont')
        row_index = IOComp.getRowIndex(cont, 'Analog Input Type', 'SAI(1)mA type Current UIO (0-5000)')
        sai_current_uio_val = IOComp.getColumnValue(cont, row_index, "Non Red (IS)")
        Trace.Write("AI uio = "+str(sai_current_uio_val))

        row_index = IOComp.getRowIndex(cont, 'Analog Input Type', 'SAI(1)FIRE 2 wire current UIO (0-5000)')
        sai_fire2_val = IOComp.getColumnValue(cont, row_index, "Non Red (IS)")
        Trace.Write("AI fire 2 uio = "+str(sai_fire2_val))

        row_index = IOComp.getRowIndex(cont, 'Analog Input Type', 'SAI(1)FIRE 3-4 wire current UIO (0-5000)')
        sai_fire34_val = IOComp.getColumnValue(cont, row_index, "Non Red (IS)")
        Trace.Write("AI fire 34 uio = "+str(sai_fire34_val))

        row_index = IOComp.getRowIndex(cont, 'Analog Input Type', 'SAI(1)FIRE 3-4 wire current Sink UIO (0-5000)')
        sai_fire34_sink_val = IOComp.getColumnValue(cont, row_index, "Non Red (IS)")
        Trace.Write("AI fire 34 sink uio = "+str(sai_fire34_sink_val))

        row_index = IOComp.getRowIndex(cont, 'Analog Input Type', 'SAI(1) GAS current UIO (0-5000)')
        sai_gas_current_sink_uio_val = IOComp.getColumnValue(cont, row_index, "Non Red (IS)")
        Trace.Write("AI gas uio = "+str(sai_gas_current_sink_uio_val))

        #AO
        cont = IOComp.Product.GetContainerByName('SM_IO_Count_Analog_Output_Cont')
        row_index = IOComp.getRowIndex(cont, 'Analog Output Type', 'SAO(1)mA Type UIO (0-5000)')
        sao_uio_val = IOComp.getColumnValue(cont, row_index, "Non Red (IS)")
        Trace.Write("AO uio = "+str(sao_uio_val))

        #DI
        cont = IOComp.Product.GetContainerByName('SM_IO_Count_Digital_Input_Cont')
        row_index = IOComp.getRowIndex(cont, 'Digital Input Type', 'SDI(1) 24Vdc UIO (0-5000)')
        di_24v_uio_val = IOComp.getColumnValue(cont, row_index, "Non Red (IS)")
        Trace.Write("DI uio = "+str(di_24v_uio_val))

        row_index = IOComp.getRowIndex(cont, 'Digital Input Type', 'SDI(1) 24Vdc Line Mon UIO (0-5000)')
        di_24v_linemon_uio_val = IOComp.getColumnValue(cont, row_index, "Non Red (IS)")
        Trace.Write("DI Linemon uio = "+str(di_24v_linemon_uio_val))

        #DO
        cont = IOComp.Product.GetContainerByName('SM_IO_Count_Digital_Output_Cont')
        row_index = IOComp.getRowIndex(cont, 'Digital Output Type', 'SDO(1) 24Vdc 500mA UIO (0-5000)')
        do_24v_uio_val = IOComp.getColumnValue(cont, row_index, "Non Red (IS)")
        Trace.Write("DO uio = "+str(do_24v_uio_val))

        row_index = IOComp.getRowIndex(cont, 'Digital Output Type', 'SDO(7) 24Vdc Line Mon UIO (0-5000)')
        do_24v_linemon_uio_val = IOComp.getColumnValue(cont, row_index, "Non Red (IS)")
        Trace.Write("DO Linemon uio = "+str(do_24v_linemon_uio_val))

        try:
            percent_spare_space = Prod.GetContainerByName('SM_CG_Cabinet_Details_Cont_Right').Rows[0].GetColumnByName("Percent_Installed_Spare_IOs").Value
        except:
            percent_spare_space = 0
        if not percent_spare_space:
            percent_spare_space = 0
        Trace.Write("percent_spare_space = "+str(percent_spare_space))

        sumrionis_cg = (sai_current_uio_val + sai_fire2_val + sai_fire34_val + sai_fire34_sink_val + sai_gas_current_sink_uio_val + sao_uio_val + di_24v_uio_val + di_24v_linemon_uio_val + do_24v_uio_val + (16 * D.Ceiling(do_24v_linemon_uio_val/float(7))))*(1 + float(float(percent_spare_space)/100))

        return round(sumrionis_cg)
    elif Prod.Name == "SM Remote Group":
        Trace.Write("SM Remote Group")
        iota_type = Prod.Attr('SM_Universal_IOTA_Type').GetValue()
        if iota_type != 'RUSIO':
            Trace.Write("Universal IOTA is not RUSIO. Returning 0")
            return 0
        sumrionis_rg = 0.0
        IOComp = IOComponents(Prod)

        # AI
        cont = IOComp.Product.GetContainerByName('SM_RG_IO_Count_Analog_Input_Cont')
        row_index = IOComp.getRowIndex(cont, 'Analog_Input_Type', 'SAI(1)mA type Current  UIO  (0-5000)')
        sai_current_uio_val = IOComp.getColumnValue(cont, row_index, "Non_Red_IS")
        Trace.Write("AI uio = "+str(sai_current_uio_val))

        row_index = IOComp.getRowIndex(cont, 'Analog_Input_Type', 'SAI(1)FIRE 2 wire current  UIO   (0-5000)')
        sai_fire2_val = IOComp.getColumnValue(cont, row_index, "Non_Red_IS")
        Trace.Write("AI fire 2 uio = "+str(sai_fire2_val))

        row_index = IOComp.getRowIndex(cont, 'Analog_Input_Type', 'SAI(1)FIRE 3-4 wire current  UIO  (0-5000)')
        sai_fire34_val = IOComp.getColumnValue(cont, row_index, "Non_Red_IS")
        Trace.Write("AI fire 34 uio = "+str(sai_fire34_val))

        row_index = IOComp.getRowIndex(cont, 'Analog_Input_Type', 'SAI(1)FIRE 3-4 wire current  Sink UIO  (0-5000)')
        sai_fire34_sink_val = IOComp.getColumnValue(cont, row_index, "Non_Red_IS")
        Trace.Write("AI fire 34 sink uio = "+str(sai_fire34_sink_val))

        row_index = IOComp.getRowIndex(cont, 'Analog_Input_Type', 'SAI(1) GAS current  UIO  (0-5000)')
        sai_gas_current_sink_uio_val = IOComp.getColumnValue(cont, row_index, "Non_Red_IS")
        Trace.Write("AI gas uio = "+str(sai_gas_current_sink_uio_val))

        #AO
        cont = IOComp.Product.GetContainerByName('SM_RG_IO_Count_Analog_Output_Cont')
        row_index = IOComp.getRowIndex(cont, 'Analog_Output_Type', 'SAO(1)mA Type UIO   (0-5000)')
        sao_uio_val = IOComp.getColumnValue(cont, row_index, "Non_Red_IS")
        Trace.Write("AO uio = "+str(sao_uio_val))

        #DI
        cont = IOComp.Product.GetContainerByName('SM_RG_IO_Count_Digital_Input_Cont')
        row_index = IOComp.getRowIndex(cont, 'Digital_Input_Type', 'SDI(1) 24Vdc UIO  (0-5000)')
        di_24v_uio_val = IOComp.getColumnValue(cont, row_index, "Non_Red_IS")
        Trace.Write("DI uio = "+str(di_24v_uio_val))

        row_index = IOComp.getRowIndex(cont, 'Digital_Input_Type', 'SDI(1) 24Vdc Line Mon UIO  (0-5000)')
        di_24v_linemon_uio_val = IOComp.getColumnValue(cont, row_index, "Non_Red_IS")
        Trace.Write("DI Linemon uio = "+str(di_24v_linemon_uio_val))

        #DO
        cont = IOComp.Product.GetContainerByName('SM_RG_IO_Count_Digital_Output_Cont')
        row_index = IOComp.getRowIndex(cont, 'Digital_Output_Type', 'SDO(1) 24Vdc 500mA UIO  (0-5000)')
        do_24v_uio_val = IOComp.getColumnValue(cont, row_index, "Non_Red_IS")
        Trace.Write("DO uio = "+str(do_24v_uio_val))

        row_index = IOComp.getRowIndex(cont, 'Digital_Output_Type', 'SDO(7) 24Vdc Line Mon UIO  (0-5000)')
        do_24v_linemon_uio_val = IOComp.getColumnValue(cont, row_index, "Non_Red_IS")
        Trace.Write("DO Linemon uio = "+str(do_24v_linemon_uio_val))

        try:
            percent_spare_space = Prod.GetContainerByName('SM_RG_Cabinet_Details_Cont').Rows[0].GetColumnByName("SM_Percent_Installed_Spare_IO").Value
        except:
            percent_spare_space = 0
        if not percent_spare_space:
            percent_spare_space = 0
        Trace.Write("percent_spare_space = "+str(percent_spare_space))

        sumrionis_rg = (sai_current_uio_val + sai_fire2_val + sai_fire34_val + sai_fire34_sink_val + sai_gas_current_sink_uio_val + sao_uio_val + di_24v_uio_val + di_24v_linemon_uio_val + do_24v_uio_val + (16 * D.Ceiling(do_24v_linemon_uio_val/float(7))))*(1 + float(float(percent_spare_space)/100))

        return round(sumrionis_rg)
    else:
        Trace.Write("Product is neither SM Control Group nor SM Remote Group")
        return 0

#Trace.Write("sumrionis = "+str(SUMRIONIS_Calc(Product)))