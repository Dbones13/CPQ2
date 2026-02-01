#CXCPQ-39951
import System.Decimal as D
class IOComponents:
    def __init__(self, Product):
        self.Product = Product
        self.cont_col_mapping = dict()
        self.container_mapping = dict()
        if Product.Name == "Series-C Control Group":
            self.cont_col_mapping = {'C300_C IO MS':'IO_Type'}
            self.container_mapping = {'Analog': 'C300_C IO MS'}
        elif Product.Name == "Series-C Remote Group":
            self.cont_col_mapping = {'C300_C IO_RG MS':'IO_Type'}
            self.container_mapping = {'Analog': 'C300_C IO_RG MS'}

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
        prefix = ui_question[0:7]
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

    #Intermediate calculation for the C300 rail cont RG
    def getrailvalue(self,  questions, columns):
        QSN = 0
        container_mapping = {}
        if self.Product.Name == "Series-C Control Group": 
            container_mapping = {'Series-C: LLAI (16) (0-5000)': 'C300_C IO MS'}
        if self.Product.Name == "Series-C Remote Group": 
            container_mapping = {'Series-C: LLAI (16) (0-5000)': 'C300_C IO_RG MS'}
        if len(questions):
            for qn in questions:
                prefix = qn[0:28]
                container_name = container_mapping[prefix]
                try:
                    container = self.Product.GetContainerByName(container_name)
                    #Trace.Write(container_name)
                    key_column_name = self.getKeyColumnName(container_name)
                    #Trace.Write(key_column_name)
                    row_index = self.getRowIndex(container, key_column_name, qn)
                    for column_name in columns:
                        QSN = self.getColumnValue(container, row_index, column_name)
                except Exception as e:
                    Trace.Write("{} is may not be visible".format(container_name))
                    Trace.Write(str(e))
        return QSN

    def C300_Mark2(self):
        
        C32=0  #FOR NIS
        X33=0 #FOR MINMAX CALCS
        CC_PAIL511=CC_TAIL511=0 # part qnt var
        questions = []
        column_name = ''
        if self.Product.Name == "Series-C Control Group":
            Percent_Installed_Spare=float(self.Product.Attributes.GetByName("SerC_CG_Percent_Installed_Spare").GetValue()) if self.Product.Attributes.GetByName("SerC_CG_Percent_Installed_Spare").GetValue() !='' else 0.0
            Trace.Write('Percent_Installed_Spare'+str(Percent_Installed_Spare))
            try:
                family = self.Product.Attr('SerC_CG_IO_Family_Type').GetValue()
            except:
                family= 'No'
            if family=="Series C":
                #Calculation of Part For first Row
                CC32 = self.getrailvalue(['Series-C: LLAI (16) (0-5000)'], ['Non_Red_NIS'])
                C32=D.Ceiling(float(CC32)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(C32)
                #calcs for min max
                X33 = D.Ceiling(C32/16.0)
                
                #Parts qnt calcs using above calcs
                CC_PAIL511=CC_TAIL511=X33
        elif self.Product.Name == "Series-C Remote Group":
            Percent_Installed_Spare=float(self.Product.Attributes.GetByName("SerC_RG_Percent_Installed_Spare(0-100%)").GetValue()) if self.Product.Attributes.GetByName("SerC_RG_Percent_Installed_Spare(0-100%)").GetValue() !='' else 0.0
            Trace.Write('Percent_Installed_Spare'+str(Percent_Installed_Spare))
            #Do_point = int(self.Product.Attr('General_Question_Average_current_DO').GetValue()) if self.Product.Attr('General_Question_Average_current_DO').GetValue() !='' else 0
            #Trace.Write('Do_point'+str(Do_point))
            try:
                family = self.Product.Attr('SerC_CG_IO_Family_Type').GetValue()
            except:
                family= 'No'
            Trace.Write("family:"+str(family))
            if family=="Series C":
                #Calculation of Part For first Row
                CC32 = self.getrailvalue(['Series-C: LLAI (16) (0-5000)'], ['Non_Red_NIS'])
                C32=D.Ceiling(float(CC32)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(C32)
                #calcs for min max
                X33 = D.Ceiling(C32/16.0)
                
                #Parts qnt calcs using above calcs
                CC_PAIL511=CC_TAIL511=X33
        return int(CC_PAIL511),int(CC_TAIL511)
#test = IOComponents(Product)
#val = test.C300_Mark2()
#Trace.Write(val)