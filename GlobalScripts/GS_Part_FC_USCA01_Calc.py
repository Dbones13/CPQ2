#CXCPQ-33046
import System.Decimal as D

class CC_UPTA01:
    def __init__(self, Product):
        self.Product  = Product
        self.cont_col_mapping = dict()
        self.container_mapping = dict()
        if Product.Name == "SM Control Group":
            self.cont_col_mapping = {'SM_IO_Count_Analog_Input_Cont':'Analog Input Type', 'SM_IO_Count_Analog_Output_Cont': 'Analog Output Type', 'SM_IO_Count_Digital_Input_Cont': 'Digital Input Type', 'SM_IO_Count_Digital_Output_Cont':'Digital Output Type', 'SM_CG_DI_RLY_NMR_Cont': 'Digital Input Type', 'SM_CG_DO_RLY_NMR_Cont':'Digital Output Type'}
            self.container_mapping = {'SAI': 'SM_IO_Count_Analog_Input_Cont', 'SAO':'SM_IO_Count_Analog_Output_Cont', 'SDI': 'SM_IO_Count_Digital_Input_Cont', 'SDO':'SM_IO_Count_Digital_Output_Cont', 'DIR':'SM_CG_DI_RLY_NMR_Cont', 'DOR':'SM_CG_DO_RLY_NMR_Cont'}
        elif Product.Name == "SM Remote Group":
            self.cont_col_mapping = {'SM_RG_IO_Count_Analog_Input_Cont':'Analog_Input_Type', 'SM_RG_IO_Count_Analog_Output_Cont': 'Analog_Output_Type', 'SM_RG_IO_Count_Digital_Input_Cont': 'Digital_Input_Type', 'SM_RG_IO_Count_Digital_Output_Cont':'Digital_Output_Type', 'SM_RG_DI_RLY_NMR_Cont': 'Digital Input Type', 'SM_RG_DO_RLY_NMR_Cont':'Digital Output Type'}
            self.container_mapping = {'SAI': 'SM_RG_IO_Count_Analog_Input_Cont', 'SAO':'SM_RG_IO_Count_Analog_Output_Cont', 'SDI': 'SM_RG_IO_Count_Digital_Input_Cont', 'SDO':'SM_RG_IO_Count_Digital_Output_Cont'}

    def getRowIndex(self, container, column_name, column_value):
        row_index = -1
        for cont_row in container.Rows:
            if column_value == cont_row.GetColumnByName(column_name).Value:
                row_index = cont_row.RowIndex
                break
        return row_index

    def removeUnwantedSpaces(self, input_string):
        input_string =  " ".join(input_string.split())
        return input_string

    def getRowIndexNew(self, container, column_name, column_value):
        row_index = -1
        for cont_row in container.Rows:
            if column_value == self.removeUnwantedSpaces(cont_row.GetColumnByName(column_name).Value):
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

    def getContainerNameByQuestion(self, ui_question):
        prefix = ui_question[0:3]
        try:
            return self.container_mapping[prefix]
        except Exception as e:
            return ''

    def getContainerNameByKeyword(self, keyword):
        try:
            return self.container_mapping[keyword]
        except Exception as e:
            Trace.Write(str(e))
            return ''

    def getKeyColumnName(self, container):
        try:
            return self.cont_col_mapping[container]
        except Exception as e:
            Trace.Write("{} {}".format(container, str(e)))
            return ''

    def getTotalIOCount(self, questions, column_name):
        IOCount = 0
        container_name = self.getContainerNameByQuestion(questions[0])
        container = self.Product.GetContainerByName(container_name)
        key_column_name = self.getKeyColumnName(container_name)
        for qn in questions:
            row_index = self.getRowIndexNew(container, key_column_name, qn)
            IOCount += self.getColumnValue(container, row_index, column_name)
        return IOCount

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

def Part_FC_USCA01_Calc(Prod, parts_dict):
    Trace.Write("Product Name : "+Prod.Name)
    if Prod.Name=="SM Control Group":
        Marshalling_Option = Prod.GetContainerByName('SM_CG_Cabinet_Details_Cont_Left').Rows[0].GetColumnByName('Marshalling_Option').DisplayValue
        if Marshalling_Option != "Universal Marshalling":
            return parts_dict
        IOComp = IOComponents(Prod)
        UPTA01 = CC_UPTA01(Prod)
        try:
            per_spare = Prod.GetContainerByName('SM_CG_Universal_Marshalling_Cabinet_Details').Rows[0].GetColumnByName("Percentage of Spare Space").Value
        except:
            per_spare = 0
        if not per_spare:
            per_spare = 0
        di_do_relay = Prod.GetContainerByName('SM_CG_Cabinet_Details_Cont_Right').Rows[0].GetColumnByName("DI/DO_SIL2/3_Relay_Adapter_UMC").DisplayValue
        namur = Prod.GetContainerByName('SM_CG_Cabinet_Details_Cont_Right').Rows[0].GetColumnByName("DI_NAMUR_proximity_Switches_Adapter_UMC").DisplayValue
        Trace.Write(str(per_spare) + " : " + str(di_do_relay) + " : " + str(namur))
        if di_do_relay == 'Yes' or namur == 'Yes':
            Trace.Write("DI/DO and Namur set to Yes")
            cont = IOComp.Product.GetContainerByName('SM_CG_DO_RLY_NMR_Cont')
            row_index = IOComp.getRowIndex(cont, 'Digital Output Type', 'SDO(1) 24Vdc 500mA UIO (0-5000)')
            E_do_uio_sil2_rly = IOComp.getColumnValue(cont, row_index, "Red_SIL2_RLY")
            F_do_uio_sil2_rly_nr = IOComp.getColumnValue(cont, row_index, "Non_Red_SIL2_RLY")

            row_index = IOComp.getRowIndex(cont, 'Digital Output Type', 'SDO(1) 24Vdc 500mA DIO (0-5000)')
            G_do_dio_sil2_rly = IOComp.getColumnValue(cont, row_index, "Red_SIL2_RLY")
            H_do_dio_sil2_rly_nr = IOComp.getColumnValue(cont, row_index, "Non_Red_SIL2_RLY")

        else:
            E_do_uio_sil2_rly = 0
            F_do_uio_sil2_rly_nr = 0
            G_do_dio_sil2_rly = 0
            H_do_dio_sil2_rly_nr = 0

        UIOAIQuestions = ['SAI(1)mA type Current UIO (0-5000)','SAI(1)FIRE 2 wire current UIO (0-5000)', 'SAI(1) GAS current UIO (0-5000)']
        UIOAOQuestions = ['SAO(1)mA Type UIO (0-5000)']
        UIODIQuestions = ['SDI(1) 24Vdc UIO (0-5000)', 'SDI(1) 24Vdc Line Mon UIO (0-5000)']
        UIODOQuestions = ['SDO(1) 24Vdc 500mA UIO (0-5000)', 'SDO(2)24Vdc 1A UIO (0-5000)', 'SDO(4)24Vdc 2A UIO (0-5000)', 'SDO(7) 24Vdc Line Mon UIO (0-5000)', 'SDO(16) SIL 2/3 250Vac/Vdc UIO (0-5000)', 'SDO(16) SIL 2/3 250Vac/Vdc COM UIO (0-5000)']
        UIODict = {'AIQuestions': UIOAIQuestions, 'AOQuestions': UIOAOQuestions, 'DIQuestions': UIODIQuestions, 'DOQuestions':UIODOQuestions}
        PDIODIQuestions = ['SDI(1) 24Vdc DIO (0-5000)', 'SDI(1) 24Vdc Line Mon DIO (0-5000)']
        PDIODOQuestions = ['SDO(1) 24Vdc 500mA DIO (0-5000)', 'SDO(16) SIL 2/3 250Vac/Vdc DIO (0-5000)', 'SDO(16) SIL 2/3 250Vac/Vdc COM DIO (0-5000)']
        PDIODict = {'AIQuestions': PDIODIQuestions, 'AOQuestions': PDIODOQuestions}
        IOCount = 0
        for key in UIODict:
            IOCount += UPTA01.getTotalIOCount(UIODict[key], 'Red (NIS)')
        E_CC_UPTA01 = IOCount
        IOCount = 0
        for key in UIODict:
            IOCount += UPTA01.getTotalIOCount(UIODict[key], 'Non Red (NIS)')
        F_CC_UPTA01 = IOCount
        IOCount = 0
        for key in PDIODict:
            IOCount += UPTA01.getTotalIOCount(PDIODict[key], 'Red (NIS)')
        G_CC_UPTA01 = IOCount
        IOCount = 0
        for key in PDIODict:
            IOCount += UPTA01.getTotalIOCount(PDIODict[key], 'Non Red (NIS)')
        H_CC_UPTA01 = IOCount

        # AI
        cont = IOComp.Product.GetContainerByName('SM_IO_Count_Analog_Input_Cont')
        row_index = IOComp.getRowIndex(cont, 'Analog Input Type', 'SAI(1)FIRE 3-4 wire current UIO (0-5000)')
        E_ai_fire34_uio = IOComp.getColumnValue(cont, row_index, "Red (NIS)")
        F_ai_fire34_uio = IOComp.getColumnValue(cont, row_index, "Non Red (NIS)")

        row_index = IOComp.getRowIndex(cont, 'Analog Input Type', 'SAI(1)FIRE 3-4 wire current Sink UIO (0-5000)')
        E_ai_fire34_sink_uio_nis = IOComp.getColumnValue(cont, row_index, "Red (NIS)")
        F_ai_fire34_sink_uio_nis_nr = IOComp.getColumnValue(cont, row_index, "Non Red (NIS)")

        E_qty = D.Ceiling(((1+float(per_spare)/float(100)) * (E_CC_UPTA01 + E_do_uio_sil2_rly + E_ai_fire34_uio + E_ai_fire34_sink_uio_nis))/float(16))
        F_qty = D.Ceiling(((1+float(per_spare)/float(100)) * (F_CC_UPTA01 + F_do_uio_sil2_rly_nr + F_ai_fire34_uio + F_ai_fire34_sink_uio_nis_nr))/float(16))
        G_qty = D.Ceiling(((1+float(per_spare)/float(100)) * (G_CC_UPTA01 + G_do_dio_sil2_rly))/float(16))
        H_qty = D.Ceiling(((1+float(per_spare)/float(100)) * (H_CC_UPTA01 + H_do_dio_sil2_rly_nr))/float(16))
        Trace.Write(str(E_qty) + " : " + str(F_qty) + " : " + str(G_qty) + " : " +str(H_qty))
        part_qty = E_qty + F_qty + G_qty + H_qty
        Trace.Write("Parts qty = " + str(part_qty))
        if part_qty > 0:
            pass
            #parts_dict["FC-USCA01"] = {'Quantity' : int(part_qty), 'Description': 'INTEGRATED FTA-HIGH CURRENT'}
    elif Prod.Name=="SM Remote Group":
        Marshalling_Option = Prod.GetContainerByName('SM_RG_Cabinet_Details_Cont_Left').Rows[0].GetColumnByName('Marshalling_Option').DisplayValue
        if Marshalling_Option != "Universal Marshalling":
            return parts_dict
        IOComp = IOComponents(Prod)
        UPTA01 = CC_UPTA01(Prod)
        try:
            per_spare = Prod.GetContainerByName('SM_RG_Universal_Marshalling_Cabinet_Details').Rows[0].GetColumnByName("Percentage of Spare Space").Value
        except:
            per_spare = 0
        if not per_spare:
            per_spare = 0
        try:
            di_do_relay = Prod.GetContainerByName('SM_RG_Cabinet_Details_Cont').Rows[0].GetColumnByName("SM_DI_DORelay_Adapter_UMC").DisplayValue
            namur = Prod.GetContainerByName('SM_RG_Cabinet_Details_Cont').Rows[0].GetColumnByName("SM_DI_NAMUR_Switches_Adapter_UMC").DisplayValue
        except:
            di_do_relay = 'No'
            namur = 'No'
        Trace.Write(str(per_spare) + " : " + str(di_do_relay) + " : " + str(namur))
        if di_do_relay == 'Yes' or namur == 'Yes':
            Trace.Write("DI/DO and Namur set to Yes")
            cont = IOComp.Product.GetContainerByName('SM_RG_DO_RLY_NMR_Cont')
            row_index = IOComp.getRowIndex(cont, 'Digital Output Type', 'SDO(1) 24Vdc 500mA UIO (0-5000)')
            E_do_uio_sil2_rly = IOComp.getColumnValue(cont, row_index, "Red_SIL2_RLY")
            F_do_uio_sil2_rly_nr = IOComp.getColumnValue(cont, row_index, "Non_Red_SIL2_RLY")

            row_index = IOComp.getRowIndex(cont, 'Digital Output Type', 'SDO(1) 24Vdc 500mA DIO (0-5000)')
            G_do_dio_sil2_rly = IOComp.getColumnValue(cont, row_index, "Red_SIL2_RLY")
            H_do_dio_sil2_rly_nr = IOComp.getColumnValue(cont, row_index, "Non_Red_SIL2_RLY")

        else:
            E_do_uio_sil2_rly = 0
            F_do_uio_sil2_rly_nr = 0
            G_do_dio_sil2_rly = 0
            H_do_dio_sil2_rly_nr = 0

        UIOAIQuestions = ['SAI(1)mA type Current UIO (0-5000)','SAI(1)FIRE 2 wire current UIO (0-5000)', 'SAI(1) GAS current UIO (0-5000)']
        UIOAOQuestions = ['SAO(1)mA Type UIO (0-5000)']
        UIODIQuestions = ['SDI(1) 24Vdc UIO (0-5000)', 'SDI(1) 24Vdc Line Mon UIO (0-5000)']
        UIODOQuestions = ['SDO(1) 24Vdc 500mA UIO (0-5000)', 'SDO(2)24Vdc 1A UIO (0-5000)', 'SDO(4)24Vdc 2A UIO (0-5000)', 'SDO(7) 24Vdc Line Mon UIO (0-5000)', 'SDO(16) SIL 2/3 250Vac/Vdc UIO (0-5000)', 'SDO(16) SIL 2/3 250Vac/Vdc COM UIO (0-5000)']
        UIODict = {'AIQuestions': UIOAIQuestions, 'AOQuestions': UIOAOQuestions, 'DIQuestions': UIODIQuestions, 'DOQuestions':UIODOQuestions}
        PDIODIQuestions = ['SDI(1) 24Vdc DIO (0-5000)', 'SDI(1) 24Vdc Line Mon DIO (0-5000)']
        PDIODOQuestions = ['SDO(1) 24Vdc 500mA DIO (0-5000)', 'SDO(16) SIL 2/3 250Vac/Vdc DIO (0-5000)', 'SDO(16) SIL 2/3 250Vac/Vdc COM DIO (0-5000)']
        PDIODict = {'AIQuestions': PDIODIQuestions, 'AOQuestions': PDIODOQuestions}
        IOCount = 0
        for key in UIODict:
            IOCount += UPTA01.getTotalIOCount(UIODict[key], 'Red_NIS')
        E_CC_UPTA01 = IOCount
        IOCount = 0
        for key in UIODict:
            IOCount += UPTA01.getTotalIOCount(UIODict[key], 'Non_Red_NIS')
        F_CC_UPTA01 = IOCount
        IOCount = 0
        for key in PDIODict:
            IOCount += UPTA01.getTotalIOCount(PDIODict[key], 'Red_NIS')
        G_CC_UPTA01 = IOCount
        IOCount = 0
        for key in PDIODict:
            IOCount += UPTA01.getTotalIOCount(PDIODict[key], 'Non_Red_NIS')
        H_CC_UPTA01 = IOCount

        # AI
        cont = IOComp.Product.GetContainerByName('SM_RG_IO_Count_Analog_Input_Cont')
        row_index = IOComp.getRowIndex(cont, 'Analog_Input_Type', 'SAI(1)FIRE 3-4 wire current  UIO  (0-5000)')
        E_ai_fire34_uio = IOComp.getColumnValue(cont, row_index, "Red_NIS")
        F_ai_fire34_uio = IOComp.getColumnValue(cont, row_index, "Non_Red_NIS")

        row_index = IOComp.getRowIndex(cont, 'Analog_Input_Type', 'SAI(1)FIRE 3-4 wire current  Sink UIO  (0-5000)')
        E_ai_fire34_sink_uio_nis = IOComp.getColumnValue(cont, row_index, "Red_NIS")
        F_ai_fire34_sink_uio_nis_nr = IOComp.getColumnValue(cont, row_index, "Non_Red_NIS")

        E_qty = D.Ceiling(((1+float(per_spare)/float(100)) * (E_CC_UPTA01 + E_do_uio_sil2_rly + E_ai_fire34_uio + E_ai_fire34_sink_uio_nis))/float(16))
        F_qty = D.Ceiling(((1+float(per_spare)/float(100)) * (F_CC_UPTA01 + F_do_uio_sil2_rly_nr + F_ai_fire34_uio + F_ai_fire34_sink_uio_nis_nr))/float(16))
        G_qty = D.Ceiling(((1+float(per_spare)/float(100)) * (G_CC_UPTA01 + G_do_dio_sil2_rly))/float(16))
        H_qty = D.Ceiling(((1+float(per_spare)/float(100)) * (H_CC_UPTA01 + H_do_dio_sil2_rly_nr))/float(16))
        Trace.Write(str(E_qty) + " : " + str(F_qty) + " : " + str(G_qty) + " : " +str(H_qty))
        part_qty = E_qty + F_qty + G_qty + H_qty
        Trace.Write("Parts qty = " + str(part_qty))
        if part_qty > 0:
            pass
            #parts_dict["FC-USCA01"] = {'Quantity' : int(part_qty), 'Description': 'INTEGRATED FTA-HIGH CURRENT'}
    return parts_dict

#part={}
#x=Part_FC_USCA01_Calc(Product, part)
#Trace.Write(str(part))