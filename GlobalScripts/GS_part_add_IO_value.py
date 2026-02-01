class IOvalues:
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
    def getSilRelyNamur(self,  questions, columns):
        output = 0
        container_mapping = {}
        if self.Product.Name == "SM Control Group": 
            container_mapping = {'SDO': 'SM_IO_Count_Digital_Output_Cont'}
        elif self.Product.Name == "SM Remote Group": 
            container_mapping = {'SDO': 'SM_RG_IO_Count_Digital_Output_Cont'}
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
                        #Trace.Write("{}{}={}".format(qn,column_name,SUMDION3))
                except Exception as e:
                    Trace.Write("{} is may not be visible".format(container_name))
                    Trace.Write(str(e))
        return output

    def io_mon(self):
        red_is = red_nis=nred_is=nred_nis=0
        questions = []
        column_name = ''
        if self.Product.Name == "SM Control Group":
            red_is = self.getSilRelyNamur(['SDO(7) 24Vdc Line Mon UIO (0-5000)'], ['Red (IS)'])
            Trace.Write(red_is)
            red_nis = self.getSilRelyNamur(['SDO(7) 24Vdc Line Mon UIO (0-5000)'], ['Red (NIS)'])
            Trace.Write(red_nis)
            nred_is = self.getSilRelyNamur(['SDO(7) 24Vdc Line Mon UIO (0-5000)'], ['Non Red (IS)'])
            Trace.Write(nred_is)
            nred_nis = self.getSilRelyNamur(['SDO(7) 24Vdc Line Mon UIO (0-5000)'], ['Non Red (NIS)'])
            Trace.Write(nred_nis)
        elif self.Product.Name == "SM Remote Group":
            red_is = self.getSilRelyNamur(['SDO(7) 24Vdc Line Mon UIO  (0-5000)'], ['Red_IS'])
            Trace.Write(red_is)
            red_nis = self.getSilRelyNamur(['SDO(7) 24Vdc Line Mon UIO  (0-5000)'], ['Red_NIS'])
            Trace.Write(red_nis)
            nred_is = self.getSilRelyNamur(['SDO(7) 24Vdc Line Mon UIO  (0-5000)'], ['Non_Red_IS'])
            Trace.Write(nred_is)
            nred_nis = self.getSilRelyNamur(['SDO(7) 24Vdc Line Mon UIO  (0-5000)'], ['Non_Red_NIS'])
            Trace.Write(nred_nis)
        return red_is,red_nis,nred_is,nred_nis
#atr=IOvalues(Product)
#a,b,c,d=atr.io_mon()
#TDOL = ((a+c)/7)+((b+d)/7)