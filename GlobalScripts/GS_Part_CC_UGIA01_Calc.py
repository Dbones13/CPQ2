#CXCPQ-33048
import System.Decimal as D

class FC_UGDA01:
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

def Part_CC_UGIA01_Calc(Prod, parts_dict):
    Trace.Write("Product Name : "+Prod.Name)
    if Prod.Name=="SM Control Group":
        Marshalling_Option = Prod.GetContainerByName('SM_CG_Cabinet_Details_Cont_Left').Rows[0].GetColumnByName('Marshalling_Option').DisplayValue
        if Marshalling_Option != "Universal Marshalling":
            return parts_dict
        IOComp = IOComponents(Prod)
        UGDA01 = FC_UGDA01(Prod)
        try:
            per_spare = Prod.GetContainerByName('SM_CG_Universal_Marshalling_Cabinet_Details').Rows[0].GetColumnByName("Percentage of Spare Space").Value
        except:
            per_spare = 0
        if not per_spare:
            per_spare = 0
        Trace.Write("per spare = "+str(per_spare))
                   
        # AI
        cont = IOComp.Product.GetContainerByName('SM_IO_Count_Analog_Input_Cont')
        row_index = IOComp.getRowIndex(cont, 'Analog Input Type', 'SAI(1)mA type Current UIO (0-5000)')
        ai_uio = IOComp.getColumnValue(cont, row_index, "Red (IS)")
        ai_uio_nr = IOComp.getColumnValue(cont, row_index, "Non Red (IS)")
               
        row_index = IOComp.getRowIndex(cont, 'Analog Input Type', 'SAI(1)FIRE 2 wire current UIO (0-5000)')
        ai_fire2_uio = IOComp.getColumnValue(cont, row_index, "Red (IS)")
        ai_fire2_uio_nr = IOComp.getColumnValue(cont, row_index, "Non Red (IS)")
        
        row_index = IOComp.getRowIndex(cont, 'Analog Input Type', 'SAI(1)FIRE 3-4 wire current UIO (0-5000)')
        ai_fire34_uio = IOComp.getColumnValue(cont, row_index, "Red (IS)")
        ai_fire34_uio_nr = IOComp.getColumnValue(cont, row_index, "Non Red (IS)")
        
        row_index = IOComp.getRowIndex(cont, 'Analog Input Type', 'SAI(1)FIRE 3-4 wire current Sink UIO (0-5000)')
        ai_fire34_sink_uio = IOComp.getColumnValue(cont, row_index, "Red (IS)")
        ai_fire34_sink_uio_nr = IOComp.getColumnValue(cont, row_index, "Non Red (IS)")
        
        row_index = IOComp.getRowIndex(cont, 'Analog Input Type', 'SAI(1) GAS current UIO (0-5000)')
        ai_gas_uio = IOComp.getColumnValue(cont, row_index, "Red (IS)")
        ai_gas_uio_nr = IOComp.getColumnValue(cont, row_index, "Non Red (IS)")
        
        I_FC_UGAI01 = ai_uio + ai_fire2_uio + ai_fire34_uio + ai_fire34_sink_uio + ai_gas_uio
        J_FC_UGAI01 = ai_uio_nr + ai_fire2_uio_nr + ai_fire34_uio_nr + ai_fire34_sink_uio_nr + ai_gas_uio_nr
        
        # AO
        cont = IOComp.Product.GetContainerByName('SM_IO_Count_Analog_Output_Cont')
        row_index = IOComp.getRowIndex(cont, 'Analog Output Type', 'SAO(1)mA Type UIO (0-5000)')
        I_ao_uio = IOComp.getColumnValue(cont, row_index, "Red (IS)")
        J_ao_uio_nr = IOComp.getColumnValue(cont, row_index, "Non Red (IS)")
        
        UIODIQuestions = ['SDI(1) 24Vdc UIO (0-5000)', 'SDI(1) 24Vdc Line Mon UIO (0-5000)']
        UIODOQuestions = ['SDO(1) 24Vdc 500mA UIO (0-5000)', 'SDO(2)24Vdc 1A UIO (0-5000)', 'SDO(4)24Vdc 2A UIO (0-5000)', 'SDO(7) 24Vdc Line Mon UIO (0-5000)']
        UIODict = {'DIQuestions': UIODIQuestions, 'DOQuestions':UIODOQuestions}
        PDIODIQuestions = ['SDI(1) 24Vdc DIO (0-5000)', 'SDI(1) 24Vdc Line Mon DIO (0-5000)']
        PDIODOQuestions = ['SDO(1) 24Vdc 500mA DIO (0-5000)']
        PDIODict = {'DIQuestions': PDIODIQuestions, 'DOQuestions': PDIODOQuestions}
        IOCount = 0
        for key in UIODict:
            IOCount += UGDA01.getTotalIOCount(UIODict[key], 'Red (IS)')
        I_FC_UGDA01 = IOCount
        IOCount = 0
        for key in UIODict:
            IOCount += UGDA01.getTotalIOCount(UIODict[key], 'Non Red (IS)')
        J_FC_UGDA01 = IOCount
        IOCount = 0
        for key in PDIODict:
            IOCount += UGDA01.getTotalIOCount(PDIODict[key], 'Red (IS)')
        K_FC_UGDA01 = IOCount
        IOCount = 0
        for key in PDIODict:
            IOCount += UGDA01.getTotalIOCount(PDIODict[key], 'Non Red (IS)')
        L_FC_UGDA01 = IOCount      
             
        I_qty = D.Ceiling(((1+float(per_spare)/float(100)) * (I_FC_UGAI01 + I_ao_uio + I_FC_UGDA01))/float(16))
        J_qty = D.Ceiling(((1+float(per_spare)/float(100)) * (J_FC_UGAI01 + J_ao_uio_nr + J_FC_UGDA01))/float(16))
        K_qty = D.Ceiling(((1+float(per_spare)/float(100)) * (K_FC_UGDA01))/float(16))
        L_qty = D.Ceiling(((1+float(per_spare)/float(100)) * (L_FC_UGDA01))/float(16))
        Trace.Write(str(I_qty) + " : " + str(J_qty) + " : " + str(K_qty) + " : " +str(L_qty))
        part_qty = I_qty + J_qty + K_qty + L_qty
        Trace.Write("Parts qty = " + str(part_qty))
        if part_qty > 0:
            parts_dict["CC-UGIA01"] = {'Quantity' : int(part_qty), 'Description': 'GIA - IS Signal Conditioning Assembly'}
    elif Prod.Name=="SM Remote Group":
        Marshalling_Option = Prod.GetContainerByName('SM_RG_Cabinet_Details_Cont_Left').Rows[0].GetColumnByName('Marshalling_Option').DisplayValue
        if Marshalling_Option != "Universal Marshalling":
            return parts_dict
        IOComp = IOComponents(Prod)
        UGDA01 = FC_UGDA01(Prod)
        try:
            per_spare = Prod.GetContainerByName('SM_RG_Universal_Marshalling_Cabinet_Details').Rows[0].GetColumnByName("Percentage of Spare Space").Value
        except:
            per_spare = 0
        if not per_spare:
            per_spare = 0
        Trace.Write("Per spare = "+str(per_spare))
        
        # AI
        cont = IOComp.Product.GetContainerByName('SM_RG_IO_Count_Analog_Input_Cont')
        row_index = IOComp.getRowIndex(cont, 'Analog_Input_Type', 'SAI(1)mA type Current  UIO  (0-5000)')
        ai_uio = IOComp.getColumnValue(cont, row_index, "Red_IS")
        ai_uio_nr = IOComp.getColumnValue(cont, row_index, "Non_Red_IS")
               
        row_index = IOComp.getRowIndex(cont, 'Analog_Input_Type', 'SAI(1)FIRE 2 wire current  UIO   (0-5000)')
        ai_fire2_uio = IOComp.getColumnValue(cont, row_index, "Red_IS")
        ai_fire2_uio_nr = IOComp.getColumnValue(cont, row_index, "Non_Red_IS")
        
        row_index = IOComp.getRowIndex(cont, 'Analog_Input_Type', 'SAI(1)FIRE 3-4 wire current  UIO  (0-5000)')
        ai_fire34_uio = IOComp.getColumnValue(cont, row_index, "Red_IS")
        ai_fire34_uio_nr = IOComp.getColumnValue(cont, row_index, "Non_Red_IS")
        
        row_index = IOComp.getRowIndex(cont, 'Analog_Input_Type', 'SAI(1)FIRE 3-4 wire current  Sink UIO  (0-5000)')
        ai_fire34_sink_uio = IOComp.getColumnValue(cont, row_index, "Red_IS")
        ai_fire34_sink_uio_nr = IOComp.getColumnValue(cont, row_index, "Non_Red_IS")
        
        row_index = IOComp.getRowIndex(cont, 'Analog_Input_Type', 'SAI(1) GAS current  UIO  (0-5000)')
        ai_gas_uio = IOComp.getColumnValue(cont, row_index, "Red_IS")
        ai_gas_uio_nr = IOComp.getColumnValue(cont, row_index, "Non_Red_IS")
        
        I_FC_UGAI01 = ai_uio + ai_fire2_uio + ai_fire34_uio + ai_fire34_sink_uio + ai_gas_uio
        J_FC_UGAI01 = ai_uio_nr + ai_fire2_uio_nr + ai_fire34_uio_nr + ai_fire34_sink_uio_nr + ai_gas_uio_nr
        
        # AO
        cont = IOComp.Product.GetContainerByName('SM_RG_IO_Count_Analog_Output_Cont')
        row_index = IOComp.getRowIndex(cont, 'Analog_Output_Type', 'SAO(1)mA Type UIO   (0-5000)')
        I_ao_uio = IOComp.getColumnValue(cont, row_index, "Red_IS")
        J_ao_uio_nr = IOComp.getColumnValue(cont, row_index, "Non_Red_IS")
        
        UIODIQuestions = ['SDI(1) 24Vdc UIO (0-5000)', 'SDI(1) 24Vdc Line Mon UIO (0-5000)']
        UIODOQuestions = ['SDO(1) 24Vdc 500mA UIO (0-5000)', 'SDO(2)24Vdc 1A UIO (0-5000)', 'SDO(4)24Vdc 2A UIO (0-5000)', 'SDO(7) 24Vdc Line Mon UIO (0-5000)']
        UIODict = {'DIQuestions': UIODIQuestions, 'DOQuestions':UIODOQuestions}
        PDIODIQuestions = ['SDI(1) 24Vdc DIO (0-5000)', 'SDI(1) 24Vdc Line Mon DIO (0-5000)']
        PDIODOQuestions = ['SDO(1) 24Vdc 500mA DIO (0-5000)']
        PDIODict = {'DIQuestions': PDIODIQuestions, 'DOQuestions': PDIODOQuestions}
        IOCount = 0
        for key in UIODict:
            IOCount += UGDA01.getTotalIOCount(UIODict[key], 'Red_IS')
        I_FC_UGDA01 = IOCount
        IOCount = 0
        for key in UIODict:
            IOCount += UGDA01.getTotalIOCount(UIODict[key], 'Non_Red_IS')
        J_FC_UGDA01 = IOCount
        IOCount = 0
        for key in PDIODict:
            IOCount += UGDA01.getTotalIOCount(PDIODict[key], 'Red_IS')
        K_FC_UGDA01 = IOCount
        IOCount = 0
        for key in PDIODict:
            IOCount += UGDA01.getTotalIOCount(PDIODict[key], 'Non_Red_IS')
        L_FC_UGDA01 = IOCount      
             
        I_qty = D.Ceiling(((1+float(per_spare)/float(100)) * (I_FC_UGAI01 + I_ao_uio + I_FC_UGDA01))/float(16))
        J_qty = D.Ceiling(((1+float(per_spare)/float(100)) * (J_FC_UGAI01 + J_ao_uio_nr + J_FC_UGDA01))/float(16))
        K_qty = D.Ceiling(((1+float(per_spare)/float(100)) * (K_FC_UGDA01))/float(16))
        L_qty = D.Ceiling(((1+float(per_spare)/float(100)) * (L_FC_UGDA01))/float(16))
        Trace.Write(str(I_qty) + " : " + str(J_qty) + " : " + str(K_qty) + " : " +str(L_qty))
        part_qty = I_qty + J_qty + K_qty + L_qty
        Trace.Write("Parts qty = " + str(part_qty))
        if part_qty > 0:
            parts_dict["CC-UGIA01"] = {'Quantity' : int(part_qty), 'Description': 'GIA - IS Signal Conditioning Assembly'}
    return parts_dict

#part={}
#x=Part_CC_UGIA01_Calc(Product, part)
#Trace.Write(str(part))