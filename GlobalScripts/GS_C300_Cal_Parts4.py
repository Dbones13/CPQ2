#CXCPQ-44050
import System.Decimal as D
import GS_Get_Set_AtvQty
class IOComponents:
    def __init__(self, Product):
        self.Product = Product
        self.cont_col_mapping = dict()
        self.container_mapping = dict()
        if Product.Name == "Series-C Control Group":
            self.cont_col_mapping = {'C300_C IO MS2':'IO_Type'}
            self.container_mapping = {'Analog': 'C300_C IO MS2'}
        elif Product.Name == "Series-C Remote Group":
            self.cont_col_mapping = {'C300_C IO_RG MS2':'IO_Type'}
            self.container_mapping = {'Analog': 'C300_C IO_RG MS2'}

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
            container_mapping = {'SCM: AO (16) (0-5000)': 'C300_C IO MS2','SCM: AO (16) HART Config/Status (0-5000)': 'C300_C IO MS2'}
        if self.Product.Name == "Series-C Remote Group":
            container_mapping = {'SCM: AO (16) (0-5000)': 'C300_C IO_RG MS2','SCM: AO (16) HART Config/Status (0-5000)': 'C300_C IO_RG MS2'}
        if len(questions):
            for qn in questions:
                prefix = qn[0:40]
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
        M11=N11=O11=P11=Q11=R11=0  #FOR IS
        M12=N12=O12=P12=Q12=R12=0  #FOR NIS
        M13=N13=O13=P13=Q13=R13=0  #FOR ISLTR

        W41=W42=W43=W51=W52=W53=0 #FOR MINMAX CALCS
        PAON01=PAOH51=TAOX61=TAOX51=0 # part qnt var
        questions = []
        column_name = ''
        if self.Product.Name == "Series-C Control Group":
            Percent_Installed_Spare=float(self.Product.Attributes.GetByName("SerC_CG_Percent_Installed_Spare").GetValue()) if self.Product.Attributes.GetByName("SerC_CG_Percent_Installed_Spare").GetValue() !='' else 0.0
            Trace.Write('Percent_Installed_Spare'+str(Percent_Installed_Spare))
            #Do_point = int(self.Product.Attr('General_Question_Average_current_DO').GetValue()) if self.Product.Attr('General_Question_Average_current_DO').GetValue() !='' else 0
            #Trace.Write("Do_point "+str(Do_point))
            try:
                family = self.Product.Attr('SerC_CG_IO_Family_Type').GetValue()
            except:
                family= 'No'
            if family=="Series-C Mark II":
                ## UI Fields
                #Calculation of Part For first Row
                MM11 = self.getrailvalue(['SCM: AO (16) (0-5000)'], ['Red_IS'])
                M11=D.Ceiling(float(MM11)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(M11)
                NN11 = self.getrailvalue(['SCM: AO (16) (0-5000)'], ['Future_Red_IS'])
                N11=D.Ceiling(float(NN11)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(N11)
                OO11 = self.getrailvalue(['SCM: AO (16) (0-5000)'], ['Non_Red_IS'])
                O11=D.Ceiling(float(OO11)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(O11)
                PP11 = self.getrailvalue(['SCM: AO (16) HART Config/Status (0-5000)'], ['Red_IS'])
                P11=D.Ceiling(float(PP11)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(P11)
                QQ11 = self.getrailvalue(['SCM: AO (16) HART Config/Status (0-5000)'], ['Future_Red_IS'])
                Q11=D.Ceiling(float(QQ11)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(Q11)
                #C/F  part IS
                RR11 = self.getrailvalue(['SCM: AO (16) HART Config/Status (0-5000)'], ['Non_Red_IS'])
                R11=D.Ceiling(float(RR11)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(R11)

                MM12 = self.getrailvalue(['SCM: AO (16) (0-5000)'], ['Red_NIS'])
                M12=D.Ceiling(float(MM12)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(M12)
                NN12 = self.getrailvalue(['SCM: AO (16) (0-5000)'], ['Future_Red_NIS'])
                N12=D.Ceiling(float(NN12)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(N12)
                #C/F  part NIS
                OO12 = self.getrailvalue(['SCM: AO (16) (0-5000)'], ['Non_Red_NIS'])
                O12=D.Ceiling(float(OO12)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(O12)
                PP12 = self.getrailvalue(['SCM: AO (16) HART Config/Status (0-5000)'], ['Red_NIS'])
                P12=D.Ceiling(float(PP12)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(P12)
                QQ12 = self.getrailvalue(['SCM: AO (16) HART Config/Status (0-5000)'], ['Future_Red_NIS'])
                Q12=D.Ceiling(float(QQ12)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(Q12)
                #C/F  part NIS
                RR12 = self.getrailvalue(['SCM: AO (16) HART Config/Status (0-5000)'], ['Non_Red_NIS'])
                R12=D.Ceiling(float(RR12)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(R12)

                MM13 = self.getrailvalue(['SCM: AO (16) (0-5000)'], ['Red_ISLTR'])
                M13=D.Ceiling(float(MM13)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(M13)
                NN13 = self.getrailvalue(['SCM: AO (16) (0-5000)'], ['Future_Red_ISLTR'])
                N13=D.Ceiling(float(NN13)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(N13)
                OO13 = self.getrailvalue(['SCM: AO (16) (0-5000)'], ['Non_Red_ISLTR'])
                O13=D.Ceiling(float(OO13)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(O13)
                PP13 = self.getrailvalue(['SCM: AO (16) HART Config/Status (0-5000)'], ['Red_ISLTR'])
                P13=D.Ceiling(float(PP13)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(P13)
                QQ13 = self.getrailvalue(['SCM: AO (16) HART Config/Status (0-5000)'], ['Future_Red_ISLTR'])
                Q13=D.Ceiling(float(QQ13)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(Q13)
                RR13 = self.getrailvalue(['SCM: AO (16) HART Config/Status (0-5000)'], ['Non_Red_ISLTR'])
                R13=D.Ceiling(float(RR13)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(R13)


                #calcs for min max
                W41 = D.Ceiling(M11/16.0) + D.Ceiling(M12/16.0) + D.Ceiling(M13/16.0)
                W42 = D.Ceiling(N11/16.0) + D.Ceiling(N12/16.0) + D.Ceiling(N13/16.0)
                W43 = D.Ceiling(O11/16.0) + D.Ceiling(O12/16.0) + D.Ceiling(O13/16.0)
                W51 = D.Ceiling(P11/16.0) + D.Ceiling(P12/16.0) + D.Ceiling(P13/16.0)
                W52 = D.Ceiling(Q11/16.0) + D.Ceiling(Q12/16.0) + D.Ceiling(Q13/16.0)
                W53 = D.Ceiling(R11/16.0) + D.Ceiling(R12/16.0) + D.Ceiling(R13/16.0)

                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'X41', W41)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'X42', W42)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'X43', W43)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'X51', W51)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'X52', W52)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'X53', W53)

                #Parts qnt calcs using above calcs
                PAON01=2*(int(W41)) + int(W42) + int(W43)
                PAOH51=2*(int(W51)) + int(W52) + int(W53)
                TAOX61 = int(W41) + int(W42) +int(W51) + int(W52)
                TAOX51 = int(W43) + int(W53)
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
            if family=="Series-C Mark II":
                ## Assigning user inputed value to pertivular veriable
                ## UI Fields
                #Part IS
                MM11 = self.getrailvalue(['SCM: AO (16) (0-5000)'], ['Red_IS'])
                M11=D.Ceiling(float(MM11)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(M11)
                NN11 = self.getrailvalue(['SCM: AO (16) (0-5000)'], ['Future_Red_IS'])
                N11=D.Ceiling(float(NN11)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(N11)
                OO11 = self.getrailvalue(['SCM: AO (16) (0-5000)'], ['Non_Red_IS'])
                O11=D.Ceiling(float(OO11)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(O11)
                PP11 = self.getrailvalue(['SCM: AO (16) HART Config/Status (0-5000)'], ['Red_IS'])
                P11=D.Ceiling(float(PP11)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(P11)
                QQ11 = self.getrailvalue(['SCM: AO (16) HART Config/Status (0-5000)'], ['Future_Red_IS'])
                Q11=D.Ceiling(float(QQ11)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(Q11)
                #C/F  part IS
                RR11 = self.getrailvalue(['SCM: AO (16) HART Config/Status (0-5000)'], ['Non_Red_IS'])
                R11=D.Ceiling(float(RR11)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(R11)

                MM12 = self.getrailvalue(['SCM: AO (16) (0-5000)'], ['Red_NIS'])
                M12=D.Ceiling(float(MM12)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(M12)
                NN12 = self.getrailvalue(['SCM: AO (16) (0-5000)'], ['Future_Red_NIS'])
                N12=D.Ceiling(float(NN12)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(N12)
                #C/F  part NIS
                OO12 = self.getrailvalue(['SCM: AO (16) (0-5000)'], ['Non_Red_NIS'])
                O12=D.Ceiling(float(OO12)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(O12)
                PP12 = self.getrailvalue(['SCM: AO (16) HART Config/Status (0-5000)'], ['Red_NIS'])
                P12=D.Ceiling(float(PP12)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(P12)
                QQ12 = self.getrailvalue(['SCM: AO (16) HART Config/Status (0-5000)'], ['Future_Red_NIS'])
                Q12=D.Ceiling(float(QQ12)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(Q12)
                #C/F  part NIS
                RR12 = self.getrailvalue(['SCM: AO (16) HART Config/Status (0-5000)'], ['Non_Red_NIS'])
                R12=D.Ceiling(float(RR12)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(R12)

                MM13 = self.getrailvalue(['SCM: AO (16) (0-5000)'], ['Red_ISLTR'])
                M13=D.Ceiling(float(MM13)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(M13)
                NN13 = self.getrailvalue(['SCM: AO (16) (0-5000)'], ['Future_Red_ISLTR'])
                N13=D.Ceiling(float(NN13)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(N13)
                OO13 = self.getrailvalue(['SCM: AO (16) (0-5000)'], ['Non_Red_ISLTR'])
                O13=D.Ceiling(float(OO13)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(O13)
                PP13 = self.getrailvalue(['SCM: AO (16) HART Config/Status (0-5000)'], ['Red_ISLTR'])
                P13=D.Ceiling(float(PP13)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(P13)
                QQ13 = self.getrailvalue(['SCM: AO (16) HART Config/Status (0-5000)'], ['Future_Red_ISLTR'])
                Q13=D.Ceiling(float(QQ13)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(Q13)
                RR13 = self.getrailvalue(['SCM: AO (16) HART Config/Status (0-5000)'], ['Non_Red_ISLTR'])
                R13=D.Ceiling(float(RR13)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(R13)


                #calcs for min max
                W41 = D.Ceiling(M11/16.0) + D.Ceiling(M12/16.0) + D.Ceiling(M13/16.0)
                W42 = D.Ceiling(N11/16.0) + D.Ceiling(N12/16.0) + D.Ceiling(N13/16.0)
                W43 = D.Ceiling(O11/16.0) + D.Ceiling(O12/16.0) + D.Ceiling(O13/16.0)
                W51 = D.Ceiling(P11/16.0) + D.Ceiling(P12/16.0) + D.Ceiling(P13/16.0)
                W52 = D.Ceiling(Q11/16.0) + D.Ceiling(Q12/16.0) + D.Ceiling(Q13/16.0)
                W53 = D.Ceiling(R11/16.0) + D.Ceiling(R12/16.0) + D.Ceiling(R13/16.0)

                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'X41', W41)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'X42', W42)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'X43', W43)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'X51', W51)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'X52', W52)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'X53', W53)

                #Parts qnt calcs using above calcs
                PAON01=2*(int(W41)) + int(W42) + int(W43)
                PAOH51=2*(int(W51)) + int(W52) + int(W53)
                TAOX61 = int(W41) + int(W42) +int(W51) + int(W52)
                TAOX51 = int(W43) + int(W53)
        return int(PAON01),int(PAOH51),int(TAOX61),int(TAOX51)
#test = IOComponents(Product)
#val = test.C300_Mark2()
#Trace.Write(val)