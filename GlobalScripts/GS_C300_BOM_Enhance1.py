#CXCPQ-44166
import System.Decimal as D
import GS_Get_Set_AtvQty
class IOComponents:
    def __init__(self, Product):
        self.Product  = Product
        self.cont_col_mapping = dict()
        self.container_mapping = dict()
        if Product.Name == "Series-C Control Group":
            self.cont_col_mapping = {'C300_SerC_Enhanced_Function_IO_Mark_Group_CG_Cont':'IO_Type'}
            self.container_mapping = {'Analog': 'C300_SerC_Enhanced_Function_IO_Mark_Group_CG_Cont'}
        elif Product.Name == "Series-C Remote Group":
            self.cont_col_mapping = {'C300_SerC_Enhanced_Function_IO_Mark_Group_RG_Cont':'IO_Type'}
            self.container_mapping = {'Analog': 'C300_SerC_Enhanced_Function_IO_Mark_Group_RG_Cont'}

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
            container_mapping = {'SCM: AO (16)': 'C300_SerC_Enhanced_Function_IO_Mark_Group_CG_Cont'}
        if self.Product.Name == "Series-C Remote Group":
            container_mapping = {'SCM: AO (16)': 'C300_SerC_Enhanced_Function_IO_Mark_Group_RG_Cont'}
        if len(questions):
            for qn in questions:
                prefix = qn[0:12]
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

    def C300_Mark(self):
        D71=E71=F71=0  #FOR IS
        D72=E72=F72=0  #FOR NIS
        D73=E73=F73=0  #FOR ISLTR

        Y71=Y71=Y73=0 #FOR MINMAX CALCS
        PAOH01=TAOX11=TAOX01=0 # part qnt var
        questions = []
        column_name = ''
        if self.Product.Name == "Series-C Control Group":
            Percent_Installed_Spare=float(self.Product.Attributes.GetByName("SerC_CG_Percent_Installed_Spare").GetValue()) if self.Product.Attributes.GetByName("SerC_CG_Percent_Installed_Spare").GetValue() !='' else 0.0
            Trace.Write('Percent_Installed_Spare'+str(Percent_Installed_Spare))
            Do_point = int(self.Product.Attr('General_Question_Average_current_DO').GetValue()) if self.Product.Attr('General_Question_Average_current_DO').GetValue() !='' else 0
            Trace.Write("Do_point "+str(Do_point))
            try:
                family = self.Product.Attr('SerC_CG_IO_Family_Type').GetValue()
            except:
                family= 'No'
            if family=="Series-C Mark II":
                ## UI Fields
                #Part IS
                DD71 = self.getrailvalue(['SCM: AO (16) HART (0-5000)'], ['Red_IS'])
                D71=D.Ceiling(float(DD71)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(D71)
                EE71 = self.getrailvalue(['SCM: AO (16) HART (0-5000)'], ['Future_Red_IS'])
                E71=D.Ceiling(float(EE71)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(E71)
                #C/F  part IS
                FF71 = self.getrailvalue(['SCM: AO (16) HART (0-5000)'], ['Non_Red_IS'])
                F71=D.Ceiling(float(FF71)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(F71)

                DD72 = self.getrailvalue(['SCM: AO (16) HART (0-5000)'], ['Red_NIS'])
                D72=D.Ceiling(float(DD72)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(D72)
                EE72 = self.getrailvalue(['SCM: AO (16) HART (0-5000)'], ['Future_Red_NIS'])
                E72=D.Ceiling(float(EE72)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(E72)
                #C/F  part NIS
                FF72 = self.getrailvalue(['SCM: AO (16) HART (0-5000)'], ['Non_Red_NIS'])
                F72=D.Ceiling(float(FF72)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(F72)

                DD73 = self.getrailvalue(['SCM: AO (16) HART (0-5000)'], ['Red_ISLTR'])
                D73=D.Ceiling(float(DD73)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(D73)
                EE73 = self.getrailvalue(['SCM: AO (16) HART (0-5000)'], ['Future_Red_ISLTR'])
                E73=D.Ceiling(float(EE73)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(E73)
                #ISLTR
                FF73 = self.getrailvalue(['SCM: AO (16) HART (0-5000)'], ['Non_Red_ISLTR'])
                F73=D.Ceiling(float(FF73)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(F73)

                #calcs for min max
                Y71 = D.Ceiling(D71/16.0) + D.Ceiling(D72/16.0) + D.Ceiling(D73/16.0)
                Y72 = D.Ceiling(E71/16.0) + D.Ceiling(E72/16.0) + D.Ceiling(E73/16.0)
                Y73 = D.Ceiling(F71/16.0) + D.Ceiling(F72/16.0) + D.Ceiling(F73/16.0)

                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'Y71', Y71)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'Y72', Y72)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'Y73', Y73)

                #Parts qnt calcs using above calcs
                PAOH01 = (2 * int(Y71))+int(Y72)+int(Y73)
                TAOX11 = int(Y71) + int(Y72)
                TAOX01 = int(Y73)
        elif self.Product.Name == "Series-C Remote Group":
            Percent_Installed_Spare=float(self.Product.Attributes.GetByName("SerC_RG_Percent_Installed_Spare(0-100%)").GetValue()) if self.Product.Attributes.GetByName("SerC_RG_Percent_Installed_Spare(0-100%)").GetValue() !='' else 0.0
            Trace.Write('Percent_Installed_Spare'+str(Percent_Installed_Spare))
            Do_point = int(self.Product.Attr('General_Question_Average_current_DO').GetValue()) if self.Product.Attr('General_Question_Average_current_DO').GetValue() !='' else 0
            Trace.Write('Do_point'+str(Do_point))
            try:
                family = self.Product.Attr('SerC_CG_IO_Family_Type').GetValue()
            except:
                family= 'No'
            Trace.Write("family:"+str(family))
            if family=="Series-C Mark II":
                ## Assigning user inputed value to pertivular veriable
                ## UI Fields
                #Part IS
                DD71 = self.getrailvalue(['SCM: AO (16) HART (0-5000)'], ['Red_IS'])
                D71=D.Ceiling(float(DD71)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(D71)
                EE71 = self.getrailvalue(['SCM: AO (16) HART (0-5000)'], ['Future_Red_IS'])
                E71=D.Ceiling(float(EE71)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(E71)
                #C/F  part IS
                FF71 = self.getrailvalue(['SCM: AO (16) HART (0-5000)'], ['Non_Red_IS'])
                F71=D.Ceiling(float(FF71)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(F71)

                DD72 = self.getrailvalue(['SCM: AO (16) HART (0-5000)'], ['Red_NIS'])
                D72=D.Ceiling(float(DD72)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(D72)
                EE72 = self.getrailvalue(['SCM: AO (16) HART (0-5000)'], ['Future_Red_NIS'])
                E72=D.Ceiling(float(EE72)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(E72)
                #C/F  part NIS
                FF72 = self.getrailvalue(['SCM: AO (16) HART (0-5000)'], ['Non_Red_NIS'])
                F72=D.Ceiling(float(FF72)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(F72)

                DD73 = self.getrailvalue(['SCM: AO (16) HART (0-5000)'], ['Red_ISLTR'])
                D73=D.Ceiling(float(DD73)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(D73)
                EE73 = self.getrailvalue(['SCM: AO (16) HART (0-5000)'], ['Future_Red_ISLTR'])
                E73=D.Ceiling(float(EE73)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(E73)
                #ISLTR
                FF73 = self.getrailvalue(['SCM: AO (16) HART (0-5000)'], ['Non_Red_ISLTR'])
                F73=D.Ceiling(float(FF73)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(F73)

                #calcs for min max
                Y71 = D.Ceiling(D71/16.0) + D.Ceiling(D72/16.0) + D.Ceiling(D73/16.0)
                Y72 = D.Ceiling(E71/16.0) + D.Ceiling(E72/16.0) + D.Ceiling(E73/16.0)
                Y73 = D.Ceiling(F71/16.0) + D.Ceiling(F72/16.0) + D.Ceiling(F73/16.0)

                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'Y71', Y71)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'Y72', Y72)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'Y73', Y73)

                #Parts qnt calcs using above calcs
                PAOH01 = (2 * int(Y71))+int(Y72)+int(Y73)
                TAOX11 = int(Y71) + int(Y72)
                TAOX01 = int(Y73)
        return int(PAOH01),int(TAOX11),int(TAOX01)
#test = IOComponents(Product)
#val = test.C300_Mark()
#Trace.Write(val)