#CXCPQ-44037
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
            container_mapping = {'SCM: HLAI (16) 4-20mA (0-5000)': 'C300_C IO MS2','SCM: HLAI (16) HART Config/Status (0-5000)': 'C300_C IO MS2'}
        if self.Product.Name == "Series-C Remote Group":
            container_mapping = {'SCM: HLAI (16) 4-20mA (0-5000)': 'C300_C IO_RG MS2','SCM: HLAI (16) HART Config/Status (0-5000)': 'C300_C IO_RG MS2'}
        if len(questions):
            for qn in questions:
                prefix = qn[0:42]
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
        A11=B11=C11=A21=B21=C21=0  #FOR IS
        A12=B12=C12=A22=B22=C22=0  #FOR NIS
        A13=B13=C13=A23=B23=C23=0  #FOR ISLTR

        X11=X12=X13=X21=X22=X23=0 #FOR MINMAX CALCS
        PAIN01=PAIH51=TAIX61=TAIX51=0 # part qnt var
        questions = []
        column_name = ''
        if self.Product.Name == "Series-C Control Group":
            Percent_Installed_Spare=float(self.Product.Attributes.GetByName("SerC_CG_Percent_Installed_Spare").GetValue()) if self.Product.Attributes.GetByName("SerC_CG_Percent_Installed_Spare").GetValue() !='' else 0.0
            Trace.Write('Percent_Installed_Spare'+str(Percent_Installed_Spare))
            try:
                family = self.Product.Attr('SerC_CG_IO_Family_Type').GetValue()
            except:
                family= 'No'
            if family=="Series-C Mark II":
                ## UI Fields
                #Calculation of Part For first Row
                AA11 = self.getrailvalue(['SCM: HLAI (16) 4-20mA (0-5000)'], ['Red_IS'])
                A11=D.Ceiling(float(AA11)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(A11)
                BB11 = self.getrailvalue(['SCM: HLAI (16) 4-20mA (0-5000)'], ['Future_Red_IS'])
                B11=D.Ceiling(float(BB11)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(B11)
                CC11 = self.getrailvalue(['SCM: HLAI (16) 4-20mA (0-5000)'], ['Non_Red_IS'])
                C11=D.Ceiling(float(CC11)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(C11)
                AA21 = self.getrailvalue(['SCM: HLAI (16) HART Config/Status (0-5000)'], ['Red_IS'])
                A21=D.Ceiling(float(AA21)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(A21)
                BB21 = self.getrailvalue(['SCM: HLAI (16) HART Config/Status (0-5000)'], ['Future_Red_IS'])
                B21=D.Ceiling(float(BB21)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(B21)
                CC21 = self.getrailvalue(['SCM: HLAI (16) HART Config/Status (0-5000)'], ['Non_Red_IS'])
                C21=D.Ceiling(float(CC21)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(C21)

                AA12 = self.getrailvalue(['SCM: HLAI (16) 4-20mA (0-5000)'], ['Red_NIS'])
                A12=D.Ceiling(float(AA12)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(A12)
                BB12 = self.getrailvalue(['SCM: HLAI (16) 4-20mA (0-5000)'], ['Future_Red_NIS'])
                B12=D.Ceiling(float(BB12)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(B12)
                CC12 = self.getrailvalue(['SCM: HLAI (16) 4-20mA (0-5000)'], ['Non_Red_NIS'])
                C12=D.Ceiling(float(CC12)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(C12)
                AA22 = self.getrailvalue(['SCM: HLAI (16) HART Config/Status (0-5000)'], ['Red_NIS'])
                A22=D.Ceiling(float(AA22)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(A22)
                BB22 = self.getrailvalue(['SCM: HLAI (16) HART Config/Status (0-5000)'], ['Future_Red_NIS'])
                B22=D.Ceiling(float(BB22)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(B22)
                CC22 = self.getrailvalue(['SCM: HLAI (16) HART Config/Status (0-5000)'], ['Non_Red_NIS'])
                C22=D.Ceiling(float(CC22)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(C22)

                AA13 = self.getrailvalue(['SCM: HLAI (16) 4-20mA (0-5000)'], ['Red_ISLTR'])
                A13=D.Ceiling(float(AA13)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(A13)
                BB13 = self.getrailvalue(['SCM: HLAI (16) 4-20mA (0-5000)'], ['Future_Red_ISLTR'])
                B13=D.Ceiling(float(BB13)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(B13)
                CC13 = self.getrailvalue(['SCM: HLAI (16) 4-20mA (0-5000)'], ['Non_Red_ISLTR'])
                C13=D.Ceiling(float(CC13)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(C13)
                AA23 = self.getrailvalue(['SCM: HLAI (16) HART Config/Status (0-5000)'], ['Red_ISLTR'])
                A23=D.Ceiling(float(AA23)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(A23)
                BB23 = self.getrailvalue(['SCM: HLAI (16) HART Config/Status (0-5000)'], ['Future_Red_ISLTR'])
                B23=D.Ceiling(float(BB23)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(B23)
                CC23 = self.getrailvalue(['SCM: HLAI (16) HART Config/Status (0-5000)'], ['Non_Red_ISLTR'])
                C23=D.Ceiling(float(CC23)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(C23)


                #calcs for min max
                X11 = D.Ceiling(A11/16.0) + D.Ceiling(A12/16.0) + D.Ceiling(A13/16.0)
                X12 = D.Ceiling(B11/16.0) + D.Ceiling(B12/16.0) + D.Ceiling(B13/16.0)
                X13 = D.Ceiling(C11/16.0) + D.Ceiling(C12/16.0) + D.Ceiling(C13/16.0)
                X21 = D.Ceiling(A21/16.0) + D.Ceiling(A22/16.0) + D.Ceiling(A23/16.0)
                X22 = D.Ceiling(B21/16.0) + D.Ceiling(B22/16.0) + D.Ceiling(B23/16.0)
                X23 = D.Ceiling(C21/16.0) + D.Ceiling(C22/16.0) + D.Ceiling(C23/16.0)

                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'X11', X11)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'X12', X12)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'X13', X13)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'X21', X21)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'X22', X22)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'X23', X23)

                #Parts qnt calcs using above calcs
                PAIN01=(2 * int(X11)) + int(X12) + int(X13)
                PAIH51=(2 * int(X21)) + int(X22) + int(X23)
                TAIX61=int(X11) + int(X12) +int(X21) + int(X22)
                TAIX51=int(X13) + int(X23)
        elif self.Product.Name == "Series-C Remote Group":
            Percent_Installed_Spare=float(self.Product.Attributes.GetByName("SerC_RG_Percent_Installed_Spare(0-100%)").GetValue()) if self.Product.Attributes.GetByName("SerC_RG_Percent_Installed_Spare(0-100%)").GetValue() !='' else 0.0
            Trace.Write('Percent_Installed_Spare'+str(Percent_Installed_Spare))
            try:
                family = self.Product.Attr('SerC_CG_IO_Family_Type').GetValue()
            except:
                family= 'No'
            Trace.Write("family:"+str(family))
            if family=="Series-C Mark II":
                #Calculation of Part For first Row
                AA11 = self.getrailvalue(['SCM: HLAI (16) 4-20mA (0-5000)'], ['Red_IS'])
                A11=D.Ceiling(float(AA11)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(A11)
                BB11 = self.getrailvalue(['SCM: HLAI (16) 4-20mA (0-5000)'], ['Future_Red_IS'])
                B11=D.Ceiling(float(BB11)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(B11)
                CC11 = self.getrailvalue(['SCM: HLAI (16) 4-20mA (0-5000)'], ['Non_Red_IS'])
                C11=D.Ceiling(float(CC11)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(C11)
                AA21 = self.getrailvalue(['SCM: HLAI (16) HART Config/Status (0-5000)'], ['Red_IS'])
                A21=D.Ceiling(float(AA21)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(A21)
                BB21 = self.getrailvalue(['SCM: HLAI (16) HART Config/Status (0-5000)'], ['Future_Red_IS'])
                B21=D.Ceiling(float(BB21)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(B21)
                CC21 = self.getrailvalue(['SCM: HLAI (16) HART Config/Status (0-5000)'], ['Non_Red_IS'])
                C21=D.Ceiling(float(CC21)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(C21)

                AA12 = self.getrailvalue(['SCM: HLAI (16) 4-20mA (0-5000)'], ['Red_NIS'])
                A12=D.Ceiling(float(AA12)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(A12)
                BB12 = self.getrailvalue(['SCM: HLAI (16) 4-20mA (0-5000)'], ['Future_Red_NIS'])
                B12=D.Ceiling(float(BB12)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(B12)
                CC12 = self.getrailvalue(['SCM: HLAI (16) 4-20mA (0-5000)'], ['Non_Red_NIS'])
                C12=D.Ceiling(float(CC12)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(C12)
                AA22 = self.getrailvalue(['SCM: HLAI (16) HART Config/Status (0-5000)'], ['Red_NIS'])
                A22=D.Ceiling(float(AA22)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(A22)
                BB22 = self.getrailvalue(['SCM: HLAI (16) HART Config/Status (0-5000)'], ['Future_Red_NIS'])
                B22=D.Ceiling(float(BB22)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(B22)
                CC22 = self.getrailvalue(['SCM: HLAI (16) HART Config/Status (0-5000)'], ['Non_Red_NIS'])
                C22=D.Ceiling(float(CC22)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(C22)

                AA13 = self.getrailvalue(['SCM: HLAI (16) 4-20mA (0-5000)'], ['Red_ISLTR'])
                A13=D.Ceiling(float(AA13)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(A13)
                BB13 = self.getrailvalue(['SCM: HLAI (16) 4-20mA (0-5000)'], ['Future_Red_ISLTR'])
                B13=D.Ceiling(float(BB13)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(B13)
                CC13 = self.getrailvalue(['SCM: HLAI (16) 4-20mA (0-5000)'], ['Non_Red_ISLTR'])
                C13=D.Ceiling(float(CC13)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(C13)
                AA23 = self.getrailvalue(['SCM: HLAI (16) HART Config/Status (0-5000)'], ['Red_ISLTR'])
                A23=D.Ceiling(float(AA23)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(A23)
                BB23 = self.getrailvalue(['SCM: HLAI (16) HART Config/Status (0-5000)'], ['Future_Red_ISLTR'])
                B23=D.Ceiling(float(BB23)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(B23)
                CC23 = self.getrailvalue(['SCM: HLAI (16) HART Config/Status (0-5000)'], ['Non_Red_ISLTR'])
                C23=D.Ceiling(float(CC23)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(C23)


                #calcs for min max
                X11 = D.Ceiling(A11/16.0) + D.Ceiling(A12/16.0) + D.Ceiling(A13/16.0)
                X12 = D.Ceiling(B11/16.0) + D.Ceiling(B12/16.0) + D.Ceiling(B13/16.0)
                X13 = D.Ceiling(C11/16.0) + D.Ceiling(C12/16.0) + D.Ceiling(C13/16.0)
                X21 = D.Ceiling(A21/16.0) + D.Ceiling(A22/16.0) + D.Ceiling(A23/16.0)
                X22 = D.Ceiling(B21/16.0) + D.Ceiling(B22/16.0) + D.Ceiling(B23/16.0)
                X23 = D.Ceiling(C21/16.0) + D.Ceiling(C22/16.0) + D.Ceiling(C23/16.0)

                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'X11', X11)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'X12', X12)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'X13', X13)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'X21', X21)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'X22', X22)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'X23', X23)

                #Parts qnt calcs using above calcs
                PAIN01=(2 * int(X11)) + int(X12) + int(X13)
                PAIH51=(2 * int(X21)) + int(X22) + int(X23)
                TAIX61=int(X11) + int(X12) +int(X21) + int(X22)
                TAIX51=int(X13) + int(X23)
        return int(PAIN01),int(PAIH51),int(TAIX61),int(TAIX51)
#test = IOComponents(Product)
#val = test.C300_Mark2()
#Trace.Write(val)