import System.Decimal as d
class IOComponents:
    def __init__(self, Product):
        self.Product  = Product
        self.cont_col_mapping = dict()
        self.container_mapping = dict()
        if Product.Name == "SM Control Group":
            self.cont_col_mapping = {'SM_IO_Count_Analog_Input_Cont':'Analog Input Type', 'SM_IO_Count_Analog_Output_Cont': 'Analog Output Type', 'SM_IO_Count_Digital_Input_Cont': 'Digital Input Type', 'SM_IO_Count_Digital_Output_Cont':'Digital Output Type', 'SM_CG_DI_RLY_NMR_Cont': 'Digital Input Type', 'SM_CG_DO_RLY_NMR_Cont':'Digital Output Type'}
            self.container_mapping = {'SAI': 'SM_IO_Count_Analog_Input_Cont', 'SAO':'SM_IO_Count_Analog_Output_Cont', 'SDI': 'SM_IO_Count_Digital_Input_Cont', 'SDO':'SM_IO_Count_Digital_Output_Cont', 'DIR':'SM_CG_DI_RLY_NMR_Cont', 'DOR':'SM_CG_DO_RLY_NMR_Cont'}
        elif Product.Name == "SM Remote Group":
            self.cont_col_mapping = {'SM_RG_IO_Count_Analog_Input_Cont':'Analog_Input_Type', 'SM_RG_IO_Count_Analog_Output_Cont': 'Analog_Output_Type', 'SM_RG_IO_Count_Digital_Input_Cont': 'Digital_Input_Type', 'SM_RG_IO_Count_Digital_Output_Cont':'Digital_Output_Type', 'SM_RG_DI_RLY_NMR_Cont': 'Digital Input Type', 'SM_RG_DO_RLY_NMR_Cont':'Digital Output Type'}
            self.container_mapping = {'SAI': 'SM_RG_IO_Count_Analog_Input_Cont', 'SAO':'SM_RG_IO_Count_Analog_Output_Cont', 'SDI': 'SM_RG_IO_Count_Digital_Input_Cont', 'SDO':'SM_RG_IO_Count_Digital_Output_Cont', 'DIR':'SM_RG_DI_RLY_NMR_Cont', 'DOR':'SM_RG_DO_RLY_NMR_Cont'}

    def getRowIndex(self, container, column_name, column_value):
        row_index = -1
        for cont_row in container.Rows:
            if column_value == cont_row.GetColumnByName(column_name).Value:
                row_index = cont_row.RowIndex
                break
                #Trace.Write(row_index)
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
            #Trace.Write(str(e))
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
            #Trace.Write(str(e))
            return ''

    def getKeyColumnName(self, container):
        try:
            return self.cont_col_mapping[container]
        except Exception as e:
            #Trace.Write("{} {}".format(container, str(e)))
            return ''

    def getPercentageSpareSpace(self):
        spareSpace = 0
        cont = ''
        if self.Product.Name == "SM Control Group":
            cont = 'SM_CG_Cabinet_Details_Cont_Right'
            colName = 'Percent_Installed_Spare_IOs'
        elif self.Product.Name == "SM Remote Group":
            cont = 'SM_RG_Cabinet_Details_Cont'
            colName = 'SM_Percent_Installed_Spare_IO'
        if cont != '':
            try:
                if self.Product.GetContainerByName(cont).Rows.Count > 0:
                    val = self.Product.GetContainerByName(cont).Rows[0].GetColumnByName(colName).Value
                    if val:
                        spareSpace = float(val)
            except Exception as e:
                Trace.Write(str(e))
                return 0

        return float(spareSpace)* 0.01

    #calculation for components SUMDION
    def getUniversalIOCountNonRedNIS(self):
        SUMDION1 = 0
        questions = []
        columns = ''
        if self.Product.Name == "SM Control Group":
            questions =  ['SDI(1) 24Vdc DIO (0-5000)', 'SDI(1) 24Vdc Line Mon DIO (0-5000)', 'SDI(1) 24Vdc with 5K Resistor DIO (0-5000)', 'SDO(1) 24Vdc 500mA DIO (0-5000)', 'SDO(16) SIL 2/3 250Vac/Vdc DIO (0-5000)','SDO(16) SIL 2/3 250Vac/Vdc COM DIO (0-5000)']
            columns = ['Non Red (NIS)']
        elif self.Product.Name == "SM Remote Group":
            questions = ['SDI(1) 24Vdc DIO  (0-5000)', 'SDI(1) 24Vdc Line Mon DIO (0-5000)', 'SDI(1) 24Vdc with 5K Resistor DIO  (0-5000)', 'SDO(1) 24Vdc 500mA DIO  (0-5000)', 'SDO(16) SIL 2/3 250Vac/Vdc DIO  (0-5000)','SDO(16) SIL 2/3 250Vac/Vdc COM DIO  (0-5000)']
            columns = ['Non_Red_NIS']
        if len(questions):
            for qn in questions:
                container_name = self.getContainerNameByQuestion(qn)
                container = self.Product.GetContainerByName(container_name)
                key_column_name = self.getKeyColumnName(container_name)
                #Trace.Write("key_column_name:{}".format(key_column_name))
                row_index = self.getRowIndex(container, key_column_name, qn)
                #Trace.Write("RowIndex={}".format(row_index))
                for column_name in columns:
                    inputed_value = self.getColumnValue(container, row_index, column_name)
                    #Trace.Write("{}{}={}".format(qn,column_name,inputed_value))
                    SUMDION1 += inputed_value
        return SUMDION1

    #Intermediate calculation for the component SUMDION for nmr/sil2/sil3
    def getSilRelyNamur(self,  questions, columns):
        SUMDION3 = 0
        container_mapping = {}
        if self.Product.Name == "SM Control Group": 
            container_mapping = {'SDI': 'SM_CG_DI_RLY_NMR_Cont', 'SDO': 'SM_CG_DO_RLY_NMR_Cont'}
        elif self.Product.Name == "SM Remote Group": 
            container_mapping = {'SDI': 'SM_RG_DI_RLY_NMR_Cont', 'SDO': 'SM_RG_DO_RLY_NMR_Cont'}
        if len(questions):
            for qn in questions:
                prefix = qn[0:3]
                container_name = container_mapping[prefix]
                try:
                    container = self.Product.GetContainerByName(container_name)
                    #Trace.Write(container_name)
                    key_column_name = self.getKeyColumnName(container_name)
                    #Trace.Write(key_column_name)
                    row_index = self.getRowIndex(container, key_column_name, qn)
                    for column_name in columns:
                        SUMDION3 += self.getColumnValue(container, row_index, column_name)
                        #Trace.Write("{}{}={}".format(qn,column_name,SUMDION3))
                except Exception as e:
                    Trace.Write("{} is may not be visible".format(container_name))
                    Trace.Write(str(e))
        return SUMDION3

    def get_Sumdion(self):
        SUMDION3 = 0
        questions = []
        column_name = ''
        if self.Product.Name == "SM Control Group":
            try:
                di_do_relay = self.Product.GetContainerByName('SM_CG_Cabinet_Details_Cont_Right').Rows[0].GetColumnByName("DI/DO_SIL2/3_Relay_Adapter_UMC").DisplayValue
            except:
                di_do_relay= 'No'
            try:
                namur = self.Product.GetContainerByName('SM_CG_Cabinet_Details_Cont_Right').Rows[0].GetColumnByName("DI_NAMUR_proximity_Switches_Adapter_UMC").DisplayValue
            except:
                namur = 'No'
            if self.Product.GetContainerByName('SM_CG_Cabinet_Details_Cont_Left').Rows[0].GetColumnByName('Marshalling_Option').DisplayValue=="Universal Marshalling" and (di_do_relay=="Yes" or namur=="Yes"):
                #'Red (SIL2 RLY)type IOs
                SUMDION3 += self.getSilRelyNamur(['SDO(1) 24Vdc 500mA DIO (0-5000)'], ['Non_Red_SIL2_RLY'])
                #Trace.Write(SUMDION3)
                #Red (SIL 3 RLY) type IOs
                SUMDION3 += self.getSilRelyNamur(['SDI(1) 24Vdc DIO (0-5000)', 'SDO(1) 24Vdc 500mA DIO (0-5000)'], ['Non_Red_SIL3_RLY'])
                #Trace.Write(SUMDION3)
                #Red NMR type IOs
                SUMDION3 += self.getSilRelyNamur(['SDI(1) 24Vdc DIO (0-5000)'], ['Non_Red_NMR'])
                #Trace.Write(SUMDION3)
                #Red NMR Safety type IOs
                SUMDION3 += self.getSilRelyNamur(['SDI(1) 24Vdc DIO (0-5000)'], ['Non_Red_NMR_Safety'])

        elif self.Product.Name == "SM Remote Group":
            if self.Product.GetContainerByName('SM_RG_ATEX Compliance_and_Enclosure_Type_Cont').Rows[0].GetColumnByName('Enclosure_Type').DisplayValue=="Cabinet":
                try:
                    di_do_relay = self.Product.GetContainerByName('SM_RG_Cabinet_Details_Cont').Rows[0].GetColumnByName("SM_DI_DORelay_Adapter_UMC").DisplayValue
                    namur = self.Product.GetContainerByName('SM_RG_Cabinet_Details_Cont').Rows[0].GetColumnByName("SM_DI_NAMUR_Switches_Adapter_UMC").DisplayValue
                except:
                    di_do_relay = 'No'
                    namur = 'No'
                if self.Product.GetContainerByName('SM_RG_Cabinet_Details_Cont_Left').Rows[0].GetColumnByName('Marshalling_Option').DisplayValue=="Universal Marshalling" and (di_do_relay=="Yes" or namur=="Yes"):
                    #'Red (SIL2 RLY)type IOs
                    SUMDION3 += self.getSilRelyNamur(['SDO(1) 24Vdc 500mA DIO (0-5000)'], ['Non_Red_SIL2_RLY'])
                    #Trace.Write(SUMDION3)
                    #Red (SIL 3 RLY) type IOs
                    SUMDION3 += self.getSilRelyNamur(['SDI(1) 24Vdc DIO (0-5000)', 'SDO(1) 24Vdc 500mA DIO (0-5000)'], ['Non_Red_SIL3_RLY'])
                    #Trace.Write(SUMDION3)
                    #Red NMR type IOs
                    SUMDION3 += self.getSilRelyNamur(['SDI(1) 24Vdc DIO (0-5000)'], ['Non_Red_NMR'])
                    #Trace.Write(SUMDION3)
                    #Red NMR Safety type IOs
                    SUMDION3 += self.getSilRelyNamur(['SDI(1) 24Vdc DIO (0-5000)'], ['Non_Red_NMR_Safety'])
        return SUMDION3
        #Non Red Rly value populating
    def getUniversalIOCountNonRedRLY(self):
        SUMDION2 = 0
        questions1 = []
        columns1 = ''
        if self.Product.Name == "SM Control Group":
            questions1 =  ['SDI(1) 24Vdc DIO (0-5000)','SDO(1) 24Vdc 500mA DIO (0-5000)']
            columns1 = ['Non Red (RLY)']
        elif self.Product.Name == "SM Remote Group":
            questions1 = ['SDI(1) 24Vdc DIO  (0-5000)','SDO(1) 24Vdc 500mA DIO  (0-5000)']
            columns1 = ['Non_Red_RLY']
        if len(questions1):
            for qn in questions1:
                container_name = self.getContainerNameByQuestion(qn)
                container = self.Product.GetContainerByName(container_name)
                key_column_name = self.getKeyColumnName(container_name)
                #Trace.Write("key_column_name:{}".format(key_column_name))
                row_index = self.getRowIndex(container, key_column_name, qn)
                #Trace.Write("RowIndex={}".format(row_index))
                for column_name in columns1:
                    inputed_value = self.getColumnValue(container, row_index, column_name)
                    #Trace.Write("{}{}={}".format(qn,column_name,inputed_value))
                    SUMDION2 += inputed_value
        return SUMDION2

    def SUMDION_value(self):
        SUMDION=0
        if self.Product.Name == "SM Control Group":
            sum1 = self.getUniversalIOCountNonRedRLY()
            sum2 = self.getUniversalIOCountNonRedNIS()
            sum3 = self.get_Sumdion()
            sumf = sum2 + sum1 + sum3
            installed_spare =self.getPercentageSpareSpace()
            SUMDION = d.Ceiling(sumf * (1 + installed_spare))
        if self.Product.Name == "SM Remote Group":
            sum1 = self.getUniversalIOCountNonRedRLY()
            sum2 = self.getUniversalIOCountNonRedNIS()
            sum3 = self.get_Sumdion()
            sumf = sum2 + sum1 + sum3
            installed_spare =self.getPercentageSpareSpace()
            SUMDION = d.Ceiling(sumf * (1 + installed_spare))
        return SUMDION
#atr=IOComponents(Product)
#red=atr.SUMDION_value()
#Trace.Write(red)