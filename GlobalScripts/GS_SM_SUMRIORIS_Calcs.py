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
            self.cont_col_mapping = {'SM_RG_IO_Count_Analog_Input_Cont':'Analog_Input_Type', 'SM_RG_IO_Count_Analog_Output_Cont': 'Analog_Output_Type', 'SM_RG_IO_Count_Digital_Input_Cont': 'Digital_Input_Type', 'SM_RG_IO_Count_Digital_Output_Cont':'Digital_Output_Type'}
            self.container_mapping = {'SAI': 'SM_RG_IO_Count_Analog_Input_Cont', 'SAO':'SM_RG_IO_Count_Analog_Output_Cont', 'SDI': 'SM_RG_IO_Count_Digital_Input_Cont', 'SDO':'SM_RG_IO_Count_Digital_Output_Cont'}

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
    def get_RedIS(self):
        val = 0
        questions = []
        columns = ''
        if self.Product.Name == "SM Control Group":
            questions =  ['SAI(1)mA type Current UIO (0-5000)','SAI(1)FIRE 2 wire current UIO (0-5000)','SAI(1)FIRE 3-4 wire current UIO (0-5000)','SAI(1)FIRE 3-4 wire current Sink UIO (0-5000)','SAI(1) GAS current UIO (0-5000)','SAO(1)mA Type UIO (0-5000)','SDI(1) 24Vdc UIO (0-5000)','SDI(1) 24Vdc Line Mon UIO (0-5000)','SDO(1) 24Vdc 500mA UIO (0-5000)']
            columns = ['Red (IS)']
        elif self.Product.Name == "SM Remote Group":
            questions = ['SAI(1)mA type Current  UIO  (0-5000)','SAI(1)FIRE 2 wire current  UIO   (0-5000)','SAI(1)FIRE 3-4 wire current  UIO  (0-5000)','SAI(1)FIRE 3-4 wire current  Sink UIO  (0-5000)','SAI(1) GAS current  UIO  (0-5000)','SAO(1)mA Type UIO   (0-5000)','SDI(1) 24Vdc UIO  (0-5000)','SDI(1) 24Vdc Line Mon UIO  (0-5000)','SDO(1) 24Vdc 500mA UIO  (0-5000)']
            columns = ['Red_IS']
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
                    Trace.Write("{}{}={}".format(qn,column_name,inputed_value))
                    val += inputed_value
        return val
    def get_sdo_line_mon(self):
        SUMDION2 = 0
        questions1 = []
        columns1 = ''
        if self.Product.Name == "SM Control Group":
            questions1 =  ['SDO(7) 24Vdc Line Mon UIO (0-5000)']
            columns1 = ['Red (IS)']
        elif self.Product.Name == "SM Remote Group":
            questions1 = ['SDO(7) 24Vdc Line Mon UIO  (0-5000)']
            columns1 = ['Red_IS']
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

    def SUMRIORIS_value(self):
        SUMRIORIS=0
        if self.Product.Name == "SM Control Group":
            if self.Product.GetContainerByName("SM_CG_Common_Questions_Cont").Rows[0].GetColumnByName("SM_Universal_IOTA").DisplayValue=="RUSIO":
                sum1 = self.get_RedIS()
                sum2 = self.get_sdo_line_mon()
                final = sum1 + d.Ceiling(16 * d.Ceiling(sum2/7.0))
                installed_spare = self.getPercentageSpareSpace()
                SUMRIORIS = d.Ceiling(final * (1 + installed_spare))
        if self.Product.Name == "SM Remote Group":
            if self.Product.Attr("SM_Universal_IOTA_Type").GetValue()=="RUSIO":
                sum1 = self.get_RedIS()
                sum2 = self.get_sdo_line_mon()
                final = sum1 + d.Ceiling(16 * d.Ceiling(sum2/7.0))
                installed_spare = self.getPercentageSpareSpace()
                SUMRIORIS = d.Ceiling(final * (1 + installed_spare))
        return SUMRIORIS
#test = IOComponents(Product)
#Trace.Write("SUMRIORIS: "+str(test.SUMRIORIS_value()))
#Trace.Write(str(test.get_RedIS()))