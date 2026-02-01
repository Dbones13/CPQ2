class IOComponents:
    def __init__(self, Product):
        self.Product  = Product
        self.cont_col_mapping = dict()
        self.container_mapping = dict()
        if Product.Name in ["SM Control Group", "R2Q SM Control Group"]:
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

    def getPercentageSpareSpace(self):
        spareSpace = 0
        cont = ''
        if self.Product.Name in ["SM Control Group", "R2Q SM Control Group"]:
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

    def roundup(self, n):
        res = int(n)
        return res if res == n else res+1

    #calculation for components SUMUIONPF and SUMUIORPF
    def getUniversalIOCountRedNonRed(self):
        SUMUIONPF = SUMUIORPF = 0
        questions = []
        columns = ''
        if self.Product.Name in ["SM Control Group", "R2Q SM Control Group"]:
            questions = ['SAI(1)mA Type Current P+F UIO (0-5000)', 'SAO(1)mA Type P+F UIO (0-5000)', 'SDI(1)  24Vdc SIL2 P+F UIO (0-5000)', 'SDI(1)  24Vdc SIL3 P+F UIO (0-5000)', 'SDO(1) 24Vdc SIL3 P+F UIO (0-5000)']
            columns = ['Non Red (IS)', 'Red (IS)']
        elif self.Product.Name == "SM Remote Group":
            questions = ['SAI(1) mA Type Current P+F UIO  (0-5000)', 'SAO(1)mA Type P+F UIO  (0-5000)', 'SDI(1)  24Vdc SIL2 P+F UIO  (0-5000)', 'SDI(1)  24Vdc SIL3 P+F UIO  (0-5000)','SDO(1) 24Vdc SIL3 P+F UIO  (0-5000)']
            columns = ['Non_Red_IS', 'Red_IS']
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
                    #check the column is Red or Non-Red
                    if column_name == columns[0]:
                        SUMUIONPF += inputed_value
                    else:
                        SUMUIORPF += inputed_value

            percenage_spare_space = 1 + self.getPercentageSpareSpace()
            #Trace.Write("SUMUIONPF:{} SUMUIORPF:{}".format(SUMUIONPF, SUMUIORPF))
            #Trace.Write("percent={}".format(percenage_spare_space))
            SUMUIONPF *= percenage_spare_space
            SUMUIORPF *= percenage_spare_space
            #round up the result
            SUMUIONPF = self.roundup(SUMUIONPF)
            SUMUIORPF = self.roundup(SUMUIORPF)
            #Trace.Write("SUMUIONPF:{} SUMUIORPF:{}".format(SUMUIONPF, SUMUIORPF))
        return SUMUIONPF, SUMUIORPF

    #Intermediate calculation for the component SUMRION
    def getSumIOs(self, questions, column_name):
        output = 0
        if self.Product.Name not in ["SM Control Group", "R2Q SM Control Group"]:
            column_name = column_name.replace('(','').replace(')','').replace(' ','_')
        if len(questions):
            for qn in questions:
                container_name = self.getContainerNameByQuestion(qn)
                container = self.Product.GetContainerByName(container_name)
                key_column_name = self.getKeyColumnName(container_name)
                #Trace.Write("key_column_name:{}".format(key_column_name))
                row_index = self.getRowIndex(container, key_column_name, qn)
                inputed_value = self.getColumnValue(container, row_index, column_name)
                output += inputed_value

        return output

    #Intermediate calculation for the component SUMRION
    def getSilRelyNamur(self,  questions, columns):
        output = 0
        container_mapping = {}
        if self.Product.Name in ["SM Control Group", "R2Q SM Control Group"]: 
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
                        output += self.getColumnValue(container, row_index, column_name)
                except Exception as e:
                    Trace.Write("{} is may not be visible".format(container_name))
                    Trace.Write(str(e))
        return output

    #calculation for the component SUMRION
    def getSumRion(self):
        output = 0
        questions = []
        column_name = ''
        UniversalIOTA = ''

        #Non-Redundant IO's for Non IS Points
        if self.Product.Name in ["SM Control Group", "R2Q SM Control Group"]:
            questions = ['SAI(1)mA type Current UIO (0-5000)', 'SAI(1)FIRE 2 wire current UIO (0-5000)', 'SAI(1)FIRE 3-4 wire current UIO (0-5000)', 'SAI(1)FIRE 3-4 wire current Sink UIO (0-5000)', 'SAI(1) GAS current UIO (0-5000)', 'SAO(1)mA Type UIO (0-5000)', 'SDI(1) 24Vdc UIO (0-5000)', 'SDI(1) 24Vdc Line Mon UIO (0-5000)', 'SDI(1) 24Vdc with 5K Resistor UIO (0-5000)', 'SDO(1) 24Vdc 500mA UIO (0-5000)', 'SDO(2)24Vdc 1A UIO (0-5000)', 'SDO(4)24Vdc 2A UIO (0-5000)']
            contCommon = self.Product.GetContainerByName('SM_CG_Common_Questions_Cont')
            if contCommon.Rows.Count > 0:
                UniversalIOTA = contCommon.Rows[0].GetColumnByName('SM_Universal_IOTA').DisplayValue
        elif self.Product.Name == "SM Remote Group":
            questions = ['SDI(1) 24Vdc UIO  (0-5000)', 'SDI(1) 24Vdc Line Mon UIO  (0-5000)', 'SDI(1) 24Vdc with 5K Resistor UIO  (0-5000)', 'SDO(1) 24Vdc 500mA UIO  (0-5000)', 'SDO(2)24Vdc 1A UIO  (0-5000)', 'SDO(4)24Vdc 2A UIO  (0-5000)', 'SAI(1)mA type Current  UIO  (0-5000)', 'SAI(1)FIRE 2 wire current  UIO   (0-5000)', 'SAI(1)FIRE 3-4 wire current  UIO  (0-5000)', 'SAI(1)FIRE 3-4 wire current  Sink UIO  (0-5000)', 'SAI(1) GAS current  UIO  (0-5000)', 'SAO(1)mA Type UIO   (0-5000)']
            UniversalIOTA = self.Product.Attr('SM_Universal_IOTA_Type').GetValue()

        #checking IOTA type
        if UniversalIOTA != 'RUSIO':
            return 0

        output += self.getSumIOs(questions, 'Non Red (NIS)')

        #Non Red (RLY) type IOs
        if self.Product.Name in ["SM Control Group", "R2Q SM Control Group"]:
            questions = ['SDI(1) 24Vdc UIO (0-5000)', 'SDO(1) 24Vdc 500mA UIO (0-5000)']
        elif self.Product.Name == "SM Remote Group":
            questions = ['SDI(1) 24Vdc UIO  (0-5000)', 'SDO(1) 24Vdc 500mA UIO  (0-5000)']
        output += self.getSumIOs(questions, 'Non Red (RLY)')

        #Non Red (SIL2 RLY)type IOs
        output += self.getSilRelyNamur(['SDO(1) 24Vdc 500mA UIO (0-5000)'], ['Non_Red_SIL2_RLY'])

        #Non Red (SIL 3 RLY) type IOs
        output += self.getSilRelyNamur(['SDI(1) 24Vdc UIO (0-5000)', 'SDO(1) 24Vdc 500mA UIO (0-5000)'], ['Non_Red_SIL3_RLY'])

        #Non Red NMR type IOs
        output += self.getSilRelyNamur(['SDI(1) 24Vdc UIO (0-5000)'], ['Non_Red_NMR'])

        #Non Red NMR Safety type IOs
        output += self.getSilRelyNamur(['SDI(1) 24Vdc UIO (0-5000)'], ['Non_Red_NMR_Safety'])

        #Non-Redundant IO's for Non IS Points
        if self.Product.Name in ["SM Control Group", "R2Q SM Control Group"]:
            questions = ['SDO(7) 24Vdc Line Mon UIO (0-5000)']
        elif self.Product.Name == "SM Remote Group":
            questions = ['SDO(7) 24Vdc Line Mon UIO  (0-5000)']

        int_output = self.getSumIOs(questions, 'Non Red (NIS)')
        if int_output > 0:
            int_output_div_by7 = int_output // 7
            if int_output % 7 == 0:
                output += (16 * int_output_div_by7)
            else:
                output += (16 * (int_output_div_by7 + 1))
        if self.Product.Name in ["SM Control Group", "R2Q SM Control Group"]:
            questions = ['SDO(16) SIL 2/3 250Vac/Vdc UIO (0-5000)', 'SDO(16) SIL 2/3 250Vac/Vdc COM UIO (0-5000)']
        elif self.Product.Name == "SM Remote Group":
            questions = ['SDO(16) SIL 2/3 250Vac/Vdc UIO   (0-5000)', 'SDO(16) SIL 2/3 250Vac/Vdc COM UIO  (0-5000)']
        output += self.getSumIOs(questions, 'Non Red (NIS)')

        SUMUIONPF, SUMUIORPF = self.getUniversalIOCountRedNonRed()
        if SUMUIORPF > 0:
            output_div_by16 = SUMUIORPF //16
            if SUMUIORPF % 16 == 0:
                output += (16 * output_div_by16)
            else:
                output += (16 * (output_div_by16 + 1))

        percenage_spare_space = 1 + self.getPercentageSpareSpace()

        output *= percenage_spare_space
        #round up the result
        output  = self.roundup(output)
        return output

    def getTotalIOCount(self, questions, column_name):
        IOCount = 0
        container_name = self.getContainerNameByQuestion(questions[0])
        container = self.Product.GetContainerByName(container_name)
        key_column_name = self.getKeyColumnName(container_name)
        for qn in questions:
            row_index = self.getRowIndexNew(container, key_column_name, qn)
            IOCount += self.getColumnValue(container, row_index, column_name)
        return IOCount

    #CXCPQ-31847 - Calculation for the component SUMMARSH
    def getSumMarsh(self):
        output = 0
        NonRedIOCount = RedIOCount = 0
        UniversalIOTA = MarshallingOption = ''
        if self.Product.Name in ["SM Control Group", "R2Q SM Control Group"]:
            non_red_is = 'Non Red (NIS)'
            red_is = 'Red (NIS)'
            cont = self.Product.GetContainerByName('SM_CG_Common_Questions_Cont')
            if cont.Rows.Count > 0:
                UniversalIOTA = cont.Rows[0].GetColumnByName('SM_Universal_IOTA').DisplayValue
            contCab = self.Product.GetContainerByName('SM_CG_Cabinet_Details_Cont_Left')
            if contCab.Rows.Count > 0:
                MarshallingOption = contCab.Rows[0].GetColumnByName('Marshalling_Option').DisplayValue
        elif self.Product.Name == "SM Remote Group":
            non_red_is = 'Non_Red_NIS'
            red_is = 'Red_NIS'
            UniversalIOTA = self.Product.Attr('SM_Universal_IOTA_Type').GetValue()
            EnclosureType = self.Product.Attr('SM_RG_Enclosure_Type').GetValue()
            contCab = self.Product.GetContainerByName('SM_RG_Cabinet_Details_Cont_Left')
            if contCab.Rows.Count > 0 and EnclosureType == 'Cabinet':
                MarshallingOption = contCab.Rows[0].GetColumnByName('Marshalling_Option').DisplayValue

        if UniversalIOTA == 'RUSIO' and MarshallingOption == 'Hardware Marshalling with Other':
            AIQuestions = ['SAI(1)mA type Current UIO (0-5000)', 'SAI(1)FIRE 2 wire current UIO (0-5000)', 'SAI(1)FIRE 3-4 wire current UIO (0-5000)', 'SAI(1) GAS current UIO (0-5000)']
            AOQuestions = ['SAO(1)mA Type UIO (0-5000)']
            DIQuestions = ['SDI(1) 24Vdc UIO (0-5000)', 'SDI(1) 24Vdc Line Mon UIO (0-5000)']
            DOQuestions = ['SDO(1) 24Vdc 500mA UIO (0-5000)', 'SDO(2)24Vdc 1A UIO (0-5000)', 'SDO(4)24Vdc 2A UIO (0-5000)']
            IODict = {'AIQuestions': AIQuestions, 'AOQuestions': AOQuestions, 'DIQuestions': DIQuestions, 'DOQuestions':DOQuestions}

            for key in IODict:
                NonRedIOCount += self.getTotalIOCount(IODict[key], non_red_is)
            percenage_spare_space = 1 + self.getPercentageSpareSpace()
            NonRedIOCount *= percenage_spare_space

            for key in IODict:
                RedIOCount += self.getTotalIOCount(IODict[key], red_is)
            RedIOCount *= percenage_spare_space
            output = NonRedIOCount + RedIOCount
            #round up the result
            output = self.roundup(output)
        return output

    #CXCPQ-33022 - Number of Universal Pass thru Adapter CC-UPTA01
    def  getPTAQuantity(self):
        UIOAIQuestions = ['SAI(1)mA type Current UIO (0-5000)','SAI(1)FIRE 2 wire current UIO (0-5000)', 'SAI(1) GAS current UIO (0-5000)']
        UIOAOQuestions = ['SAO(1)mA Type UIO (0-5000)']
        UIODIQuestions = ['SDI(1) 24Vdc UIO (0-5000)', 'SDI(1) 24Vdc Line Mon UIO (0-5000)']
        UIODOQuestions = ['SDO(1) 24Vdc 500mA UIO (0-5000)', 'SDO(2)24Vdc 1A UIO (0-5000)', 'SDO(4)24Vdc 2A UIO (0-5000)', 'SDO(7) 24Vdc Line Mon UIO (0-5000)', 'SDO(16) SIL 2/3 250Vac/Vdc UIO (0-5000)', 'SDO(16) SIL 2/3 250Vac/Vdc COM UIO (0-5000)']
        UIODict = {'AIQuestions': UIOAIQuestions, 'AOQuestions': UIOAOQuestions, 'DIQuestions': UIODIQuestions, 'DOQuestions':UIODOQuestions}
        PDIODIQuestions = ['SDI(1) 24Vdc DIO (0-5000)', 'SDI(1) 24Vdc Line Mon DIO (0-5000)']
        PDIODOQuestions = ['SDO(1) 24Vdc 500mA DIO (0-5000)', 'SDO(16) SIL 2/3 250Vac/Vdc DIO (0-5000)', 'SDO(16) SIL 2/3 250Vac/Vdc COM DIO (0-5000)']
        PDIODict = {'AIQuestions': PDIODIQuestions, 'AOQuestions': PDIODOQuestions}

        columns = ['Red_NIS', 'Non_Red_NIS']
        if self.Product.Name in ["SM Control Group", "R2Q SM Control Group"]:
            columns = ['Red (NIS)', 'Non Red (NIS)']
        TotalIOs = 0
        for column in columns:
            IOCount = 0
            for key in UIODict:
                IOCount += self.getTotalIOCount(UIODict[key], column)
            TotalIOs += IOCount
            #Trace.Write("UIOQuestions ({}):{}".format(column,IOCount))
            IOCount = 0
            for key in PDIODict:
                IOCount += self.getTotalIOCount(PDIODict[key], column)
            TotalIOs += IOCount
        return TotalIOs

    #CXCPQ-33024 - Number of AI Adapter, 3 wire FC-UAIA01
    def getAIAdapterQuantity(self):
        UIOAIQuestions = ['SAI(1)FIRE 3-4 wire current UIO (0-5000)']
        UIODict = {'AIQuestions': UIOAIQuestions}
        columns = ['Red_NIS', 'Non_Red_NIS']
        if self.Product.Name in ["SM Control Group", "R2Q SM Control Group"]:
            columns = ['Red (NIS)', 'Non Red (NIS)']
        TotalIOs = 0
        for column in columns:
            IOCount = 0
            for key in UIODict:
                IOCount += self.getTotalIOCount(UIODict[key], column)
            TotalIOs += IOCount
        return TotalIOs

    #CXCPQ-33025 - Number of AI Adapter Sink, 3 wire, FC-UAIS01
    def getAIAdapterSinkQuantity(self):
        UIOAIQuestions = ['SAI(1)FIRE 3-4 wire current Sink UIO (0-5000)']
        UIODict = {'AIQuestions': UIOAIQuestions}
        columns = ['Red_NIS', 'Non_Red_NIS']
        if self.Product.Name in ["SM Control Group", "R2Q SM Control Group"]:
            columns = ['Red (NIS)', 'Non Red (NIS)']
        TotalIOs = 0
        for column in columns:
            IOCount = 0
            for key in UIODict:
                IOCount += self.getTotalIOCount(UIODict[key], column)
            TotalIOs += IOCount
        return TotalIOs