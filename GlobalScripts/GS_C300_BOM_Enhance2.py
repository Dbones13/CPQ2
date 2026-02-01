#CXCPQ-44473
import System.Decimal as D
import GS_Get_Set_AtvQty
class IOComponents:
    def __init__(self, Product):
        self.Product = Product
        self.cont_col_mapping = dict()
        self.container_mapping = dict()
        if Product.Name == "Series-C Control Group":
            self.cont_col_mapping = {'C300_SerC_Enhanced_Function_IO_Mark_Group_CG_Cont1':'IO_Type'}
            self.container_mapping = {'Analog': 'C300_SerC_Enhanced_Function_IO_Mark_Group_CG_Cont1'}
        elif Product.Name == "Series-C Remote Group":
            self.cont_col_mapping = {'C300_SerC_Enhanced_Function_IO_Mark_Group_RG_Cont1':'IO_Type'}
            self.container_mapping = {'Analog': 'C300_SerC_Enhanced_Function_IO_Mark_Group_RG_Cont1'}

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
            container_mapping = {'SCM: DI (32) 24 VDC': 'C300_SerC_Enhanced_Function_IO_Mark_Group_CG_Cont1'}
        if self.Product.Name == "Series-C Remote Group":
            container_mapping = {'SCM: DI (32) 24 VDC': 'C300_SerC_Enhanced_Function_IO_Mark_Group_RG_Cont1'}
        if len(questions):
            for qn in questions:
                prefix = qn[0:19]
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
        D81=E81=F81=0  #FOR IS
        D82=E82=F82=0  #FOR NIS
        D83=E83=F83=0  #FOR ISLTR
        D84=E84=F84=0  #FOR RLY
        S71=S72=S73=0  #FOR HV RLY
        
        Y81=Y81=Y83=0 #FOR MINMAX CALCS
        PDIL01=TDIL11=TDIL01=0 # part qnt var
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
                DD81 = self.getrailvalue(['SCM: DI (32) 24 VDC with Open Wire Detect (0-5000)'], ['Red_IS'])
                D81=D.Ceiling(float(DD81)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(D81)
                EE81 = self.getrailvalue(['SCM: DI (32) 24 VDC with Open Wire Detect (0-5000)'], ['Future_Red_IS'])
                E81=D.Ceiling(float(EE81)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(E81)
                #C/F  part IS
                FF81 = self.getrailvalue(['SCM: DI (32) 24 VDC with Open Wire Detect (0-5000)'], ['Non_Red_IS'])
                F81=D.Ceiling(float(FF81)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(F81)

                DD82 = self.getrailvalue(['SCM: DI (32) 24 VDC with Open Wire Detect (0-5000)'], ['Red_NIS'])
                D82=D.Ceiling(float(DD82)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(D82)
                EE82 = self.getrailvalue(['SCM: DI (32) 24 VDC with Open Wire Detect (0-5000)'], ['Future_Red_NIS'])
                E82=D.Ceiling(float(EE82)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(E82)
                #C/F  part NIS
                FF82 = self.getrailvalue(['SCM: DI (32) 24 VDC with Open Wire Detect (0-5000)'], ['Non_Red_NIS'])
                F82=D.Ceiling(float(FF82)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(F82)

                DD83 = self.getrailvalue(['SCM: DI (32) 24 VDC with Open Wire Detect (0-5000)'], ['Red_ISLTR'])
                D83=D.Ceiling(float(DD83)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(D83)
                EE83 = self.getrailvalue(['SCM: DI (32) 24 VDC with Open Wire Detect (0-5000)'], ['Future_Red_ISLTR'])
                E83=D.Ceiling(float(EE83)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(E83)
                #ISLTR
                FF83 = self.getrailvalue(['SCM: DI (32) 24 VDC with Open Wire Detect (0-5000)'], ['Non_Red_ISLTR'])
                F83=D.Ceiling(float(FF83)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(F83)

                DD84 = self.getrailvalue(['SCM: DI (32) 24 VDC with Open Wire Detect (0-5000)'], ['Red_RLY'])
                D84=D.Ceiling(float(DD84)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(D84)
                EE84 = self.getrailvalue(['SCM: DI (32) 24 VDC with Open Wire Detect (0-5000)'], ['Future_Red_RLY'])
                E84=D.Ceiling(float(EE84)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(E84)
                #RLY
                FF84 = self.getrailvalue(['SCM: DI (32) 24 VDC with Open Wire Detect (0-5000)'], ['Non_Red_RLY'])
                F84=D.Ceiling(float(FF84)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(F84)
                
                SS71 = self.getrailvalue(['SCM: DI (32) 24 VDC with Open Wire Detect (0-5000)'], ['Red_HV_Rly'])
                S71=D.Ceiling(float(SS71)*(1+(Percent_Installed_Spare/100)))
                
                SS72 = self.getrailvalue(['SCM: DI (32) 24 VDC with Open Wire Detect (0-5000)'], ['Future_HV_Rly'])
                S72=D.Ceiling(float(SS72)*(1+(Percent_Installed_Spare/100)))
                
                SS73 = self.getrailvalue(['SCM: DI (32) 24 VDC with Open Wire Detect (0-5000)'], ['Non_Red_HV_Rly'])
                S73=D.Ceiling(float(SS73)*(1+(Percent_Installed_Spare/100)))
                
                #calcs for min max
                Y81 = D.Ceiling(D81/32.0) + D.Ceiling(D82/32.0) + D.Ceiling(D83/32.0) + D.Ceiling(D84/32.0) + D.Ceiling(S71/32.0)
                Y82 = D.Ceiling(E81/32.0) + D.Ceiling(E82/32.0) + D.Ceiling(E83/32.0) + D.Ceiling(E84/32.0) + D.Ceiling(S72/32.0)
                Y83 = D.Ceiling(F81/32.0) + D.Ceiling(F82/32.0) + D.Ceiling(F83/32.0) + D.Ceiling(F84/32.0) + D.Ceiling(S73/32.0)

                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'Y81', Y81)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'Y82', Y82)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'Y83', Y83)

                #Parts qnt calcs using above calcs
                PDIL01 = (2 * int(Y81))+int(Y82)+int(Y83)
                TDIL11 = int(Y81) + int(Y82)
                TDIL01 = int(Y83)
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
                DD81 = self.getrailvalue(['SCM: DI (32) 24 VDC with Open Wire Detect (0-5000)'], ['Red_IS'])
                D81=D.Ceiling(float(DD81)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(D81)
                EE81 = self.getrailvalue(['SCM: DI (32) 24 VDC with Open Wire Detect (0-5000)'], ['Future_Red_IS'])
                E81=D.Ceiling(float(EE81)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(E81)
                #C/F  part IS
                FF81 = self.getrailvalue(['SCM: DI (32) 24 VDC with Open Wire Detect (0-5000)'], ['Non_Red_IS'])
                F81=D.Ceiling(float(FF81)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(F81)

                DD82 = self.getrailvalue(['SCM: DI (32) 24 VDC with Open Wire Detect (0-5000)'], ['Red_NIS'])
                D82=D.Ceiling(float(DD82)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(D82)
                EE82 = self.getrailvalue(['SCM: DI (32) 24 VDC with Open Wire Detect (0-5000)'], ['Future_Red_NIS'])
                E82=D.Ceiling(float(EE82)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(E82)
                #C/F  part NIS
                FF82 = self.getrailvalue(['SCM: DI (32) 24 VDC with Open Wire Detect (0-5000)'], ['Non_Red_NIS'])
                F82=D.Ceiling(float(FF82)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(F82)

                DD83 = self.getrailvalue(['SCM: DI (32) 24 VDC with Open Wire Detect (0-5000)'], ['Red_ISLTR'])
                D83=D.Ceiling(float(DD83)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(D83)
                EE83 = self.getrailvalue(['SCM: DI (32) 24 VDC with Open Wire Detect (0-5000)'], ['Future_Red_ISLTR'])
                E83=D.Ceiling(float(EE83)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(E83)
                #ISLTR
                FF83 = self.getrailvalue(['SCM: DI (32) 24 VDC with Open Wire Detect (0-5000)'], ['Non_Red_ISLTR'])
                F83=D.Ceiling(float(FF83)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(F83)

                DD84 = self.getrailvalue(['SCM: DI (32) 24 VDC with Open Wire Detect (0-5000)'], ['Red_RLY'])
                D84=D.Ceiling(float(DD84)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(D84)
                EE84 = self.getrailvalue(['SCM: DI (32) 24 VDC with Open Wire Detect (0-5000)'], ['Future_Red_RLY'])
                E84=D.Ceiling(float(EE84)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(E84)
                #RLY
                FF84 = self.getrailvalue(['SCM: DI (32) 24 VDC with Open Wire Detect (0-5000)'], ['Non_Red_RLY'])
                F84=D.Ceiling(float(FF84)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(F84)
                
                SS71 = self.getrailvalue(['SCM: DI (32) 24 VDC with Open Wire Detect (0-5000)'], ['Red_HV_Rly'])
                S71=D.Ceiling(float(SS71)*(1+(Percent_Installed_Spare/100)))
                
                SS72 = self.getrailvalue(['SCM: DI (32) 24 VDC with Open Wire Detect (0-5000)'], ['Future_HV_Rly'])
                S72=D.Ceiling(float(SS72)*(1+(Percent_Installed_Spare/100)))
                
                SS73 = self.getrailvalue(['SCM: DI (32) 24 VDC with Open Wire Detect (0-5000)'], ['Non_Red_HV_Rly'])
                S73=D.Ceiling(float(SS73)*(1+(Percent_Installed_Spare/100)))

                #calcs for min max
                Y81 = D.Ceiling(D81/32.0) + D.Ceiling(D82/32.0) + D.Ceiling(D83/32.0) + D.Ceiling(D84/32.0) + D.Ceiling(S71/32.0)
                Y82 = D.Ceiling(E81/32.0) + D.Ceiling(E82/32.0) + D.Ceiling(E83/32.0) + D.Ceiling(E84/32.0) + D.Ceiling(S72/32.0)
                Y83 = D.Ceiling(F81/32.0) + D.Ceiling(F82/32.0) + D.Ceiling(F83/32.0) + D.Ceiling(F84/32.0) + D.Ceiling(S73/32.0)

                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'Y81', Y81)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'Y82', Y82)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'Y83', Y83)

                #Parts qnt calcs using above calcs
                PDIL01 = (2 * int(Y81))+int(Y82)+int(Y83)
                TDIL11 = int(Y81) + int(Y82)
                TDIL01 = int(Y83)
        return int(PDIL01),int(TDIL11),int(TDIL01)
#test = IOComponents(Product)
#val = test.C300_Mark2()
#Trace.Write(val)