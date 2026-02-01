#CXCPQ-40104
import System.Decimal as D
import GS_Get_Set_AtvQty
class IOComponents:
    def __init__(self, Product):
        self.Product  = Product
        self.cont_col_mapping = dict()
        self.container_mapping = dict()
        if Product.Name == "Series-C Control Group":
            self.cont_col_mapping = {'C300_CG_Universal_IO_cont_1':'IO_Type', 'C300_CG_Universal_IO_cont_2': 'IO_Type'}
            self.container_mapping = {'Analog': 'C300_CG_Universal_IO_cont_1', 'Digital':'C300_CG_Universal_IO_cont_2'}
        elif Product.Name == "Series-C Remote Group":
            self.cont_col_mapping = {'C300_RG_Universal_IO_cont_1':'IO_Type', 'C300_RG_Universal_IO_cont_2': 'IO_Type'}
            self.container_mapping = {'Analog': 'C300_RG_Universal_IO_cont_1', 'Digital':'C300_RG_Universal_IO_cont_2'}

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
            container_mapping = {'Series-C: UIO (32) Analog': 'C300_CG_Universal_IO_cont_1', 'Series-C: UIO (32) Digita':'C300_CG_Universal_IO_cont_2'}
        if self.Product.Name == "Series-C Remote Group": 
            container_mapping = {'Series-C: UIO (32) Analog': 'C300_RG_Universal_IO_cont_1', 'Series-C: UIO (32) Digita':'C300_RG_Universal_IO_cont_2'}
        if len(questions):
            for qn in questions:
                prefix = qn[0:25]
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

    def C300_Rail(self):
        Product = self.Product
        A61=B61=C61=A81=B81=C81=A91=B91=C91=D11=E11=F11=0  #FOR IS
        A62=B62=C62=A82=B82=C82=A92=B92=C92=D12=E12=F12=0  #FOR NIS
        A63=B63=C63=A73=B73=C73=A83=B83=C83=A93=B93=C93=D13=E13=F13=0  #FOR ISLTR
        A94=B94=C94=D14=E14=F14=0 #for RLy
        GG11=HH11=II11=GG21=HH21=II21=0  #for HV_RLy
        XX61=XX62=XX63=XX71=XX72=XX73=XX81=XX82=XX83=0 #FOR MINMAX CALCS
        var1=var2=var3=var4=var5=var7=var8=var9=var10=var11=var6=var12=var13=var14=var15=var16=var17=var18=0 # cals var
        cal1=cal2=cal3=cal4=cal5=cal7=cal8=cal9=cal10=cal11=cal6=cal12=cal13=cal14=cal15=cal16=cal17=cal18=0 #calcs Var minmax
        PUIO31=TUIO41=TUIO31=Amp_A=0 # part qnt var
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
            if family=="Series C":
                ## Assigning user inputed value to pertivular veriable
                #A/D Part IS
                AA61A = self.getrailvalue(['Series-C: UIO (32) Analog Input (HLAI Adapt) (0-5000)'], ['Red_IS'])
                A61=D.Ceiling(float(AA61A)*(1+(Percent_Installed_Spare/100)))
                Trace.Write(A61)
                AA81A= self.getrailvalue(['Series-C: UIO (32) Analog Output (0-5000)'], ['Red_IS'])
                A81=D.Ceiling(float(AA81A)*(1+(Percent_Installed_Spare/100)))
                Trace.Write(A81)
                AA91A = self.getrailvalue(['Series-C: UIO (32) Digital Input (0-5000)'], ['Red_IS'])
                A91=D.Ceiling(float(AA91A)*(1+(Percent_Installed_Spare/100)))
                Trace.Write(A91)
                DD11A = self.getrailvalue(['Series-C: UIO (32) Digital Output (0-5000)'], ['Red_IS'])
                D11=D.Ceiling(float(DD11A)*(1+(Percent_Installed_Spare/100)))
                Trace.Write(D11)

                #B/E part IS
                BB61A = self.getrailvalue(['Series-C: UIO (32) Analog Input (HLAI Adapt) (0-5000)'], ['Future_Red_IS'])
                B61=D.Ceiling(float(BB61A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(BB61A)
                BB81A = self.getrailvalue(['Series-C: UIO (32) Analog Output (0-5000)'], ['Future_Red_IS'])
                B81=D.Ceiling(float(BB81A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(BB81A)
                BB91A = self.getrailvalue(['Series-C: UIO (32) Digital Input (0-5000)'], ['Future_Red_IS'])
                B91=D.Ceiling(float(BB91A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(BB91A)
                EE11A = self.getrailvalue(['Series-C: UIO (32) Digital Output (0-5000)'], ['Future_Red_IS'])
                E11=D.Ceiling(float(EE11A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(EE11A)

                #C/F  part IS
                CC61A = self.getrailvalue(['Series-C: UIO (32) Analog Input (HLAI Adapt) (0-5000)'], ['Non_Red_IS'])
                C61=D.Ceiling(float(CC61A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(CC61A)
                CC81A= self.getrailvalue(['Series-C: UIO (32) Analog Output (0-5000)'], ['Non_Red_IS'])
                C81=D.Ceiling(float(CC81A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(CC81A)
                CC91A = self.getrailvalue(['Series-C: UIO (32) Digital Input (0-5000)'], ['Non_Red_IS'])
                C91=D.Ceiling(float(CC91A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(CC91A)
                FF11A = self.getrailvalue(['Series-C: UIO (32) Digital Output (0-5000)'], ['Non_Red_IS'])
                F11=D.Ceiling(float(FF11A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(FF11A)

                ##NIS
                #A/D Part NIS
                AA62A = self.getrailvalue(['Series-C: UIO (32) Analog Input (HLAI Adapt) (0-5000)'], ['Red_NIS'])
                A62=D.Ceiling(float(AA62A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(AA62A)
                AA82A = self.getrailvalue(['Series-C: UIO (32) Analog Output (0-5000)'], ['Red_NIS'])
                A82=D.Ceiling(float(AA82A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(AA82A)
                AA92A = self.getrailvalue(['Series-C: UIO (32) Digital Input (0-5000)'], ['Red_NIS'])
                A92=D.Ceiling(float(AA92A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(AA92A)
                DD12A = self.getrailvalue(['Series-C: UIO (32) Digital Output (0-5000)'], ['Red_NIS'])
                D12=D.Ceiling(float(DD12A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(DD12A)

                #B/E part NIS
                BB62A = self.getrailvalue(['Series-C: UIO (32) Analog Input (HLAI Adapt) (0-5000)'], ['Future_Red_NIS'])
                B62=D.Ceiling(float(BB62A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(BB62A)
                BB82A= self.getrailvalue(['Series-C: UIO (32) Analog Output (0-5000)'], ['Future_Red_NIS'])
                B82=D.Ceiling(float(BB82A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(BB82A)
                BB92A = self.getrailvalue(['Series-C: UIO (32) Digital Input (0-5000)'], ['Future_Red_NIS'])
                B92=D.Ceiling(float(BB92A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(BB92A)
                EE12A = self.getrailvalue(['Series-C: UIO (32) Digital Output (0-5000)'], ['Future_Red_NIS'])
                E12=D.Ceiling(float(EE12A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(EE12A)

                #C/F part NIS
                CC62A = self.getrailvalue(['Series-C: UIO (32) Analog Input (HLAI Adapt) (0-5000)'], ['Non_Red_NIS'])
                C62=D.Ceiling(float(CC62A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(CC62A)
                CC82A = self.getrailvalue(['Series-C: UIO (32) Analog Output (0-5000)'], ['Non_Red_NIS'])
                C82=D.Ceiling(float(CC82A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(CC82A)
                CC92A = self.getrailvalue(['Series-C: UIO (32) Digital Input (0-5000)'], ['Non_Red_NIS'])
                C92=D.Ceiling(float(CC92A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(CC92A)
                FF12A = self.getrailvalue(['Series-C: UIO (32) Digital Output (0-5000)'], ['Non_Red_NIS'])
                F12=D.Ceiling(float(FF12A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(FF12A)

                ##ISLTR
                #A/D Part ISLTR
                AA63A = self.getrailvalue(['Series-C: UIO (32) Analog Input (HLAI Adapt) (0-5000)'], ['Red_ISLTR'])
                A63=D.Ceiling(float(AA63A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(AA63A)
                AA73A = self.getrailvalue(['Series-C: UIO (32) Analog Input (LLAI Adapt) (0-5000)'], ['Red_ISLTR'])
                A73=D.Ceiling(float(AA73A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(AA73A)
                AA83A= self.getrailvalue(['Series-C: UIO (32) Analog Output (0-5000)'], ['Red_ISLTR'])
                A83=D.Ceiling(float(AA83A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(AA83A)
                AA93A = self.getrailvalue(['Series-C: UIO (32) Digital Input (0-5000)'], ['Red_ISLTR'])
                A93=D.Ceiling(float(AA93A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(AA93A)
                DD13A = self.getrailvalue(['Series-C: UIO (32) Digital Output (0-5000)'], ['Red_ISLTR'])
                D13=D.Ceiling(float(DD13A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(DD13A)

                #B/E Part ISLTR
                BB63A = self.getrailvalue(['Series-C: UIO (32) Analog Input (HLAI Adapt) (0-5000)'], ['Future_Red_ISLTR'])
                B63=D.Ceiling(float(BB63A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(BB63A)
                BB73A = self.getrailvalue(['Series-C: UIO (32) Analog Input (LLAI Adapt) (0-5000)'], ['Future_Red_ISLTR'])
                B73=D.Ceiling(float(BB73A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(BB63A)
                BB83A = self.getrailvalue(['Series-C: UIO (32) Analog Output (0-5000)'], ['Future_Red_ISLTR'])
                B83=D.Ceiling(float(BB83A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(BB83A)
                BB93A = self.getrailvalue(['Series-C: UIO (32) Digital Input (0-5000)'], ['Future_Red_ISLTR'])
                B93=D.Ceiling(float(BB93A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(BB93A)
                EE13A = self.getrailvalue(['Series-C: UIO (32) Digital Output (0-5000)'], ['Future_Red_ISLTR'])
                E13=D.Ceiling(float(EE13A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(EE13A)

                #C/F Part ISLTR
                CC63A = self.getrailvalue(['Series-C: UIO (32) Analog Input (HLAI Adapt) (0-5000)'], ['Non_Red_ISLTR'])
                C63=D.Ceiling(float(CC63A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(CC63A)
                CC73A = self.getrailvalue(['Series-C: UIO (32) Analog Input (LLAI Adapt) (0-5000)'], ['Non_Red_ISLTR'])
                C73=D.Ceiling(float(CC73A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(CC73A)
                CC83A = self.getrailvalue(['Series-C: UIO (32) Analog Output (0-5000)'], ['Non_Red_ISLTR'])
                C83=D.Ceiling(float(CC83A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(CC83A)
                CC93A = self.getrailvalue(['Series-C: UIO (32) Digital Input (0-5000)'], ['Non_Red_ISLTR'])
                C93=D.Ceiling(float(CC93A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(CC93A)
                FF13A = self.getrailvalue(['Series-C: UIO (32) Digital Output (0-5000)'], ['Non_Red_ISLTR'])
                F13=D.Ceiling(float(FF13A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(FF13A)

                #RLY only container
                #A/D part
                AA94A = self.getrailvalue(['Series-C: UIO (32) Digital Input (0-5000)'], ['Red_RLY'])
                A94=D.Ceiling(float(AA94A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(AA94A)
                DD14A= self.getrailvalue(['Series-C: UIO (32) Digital Output (0-5000)'], ['Red_RLY'])
                D14=D.Ceiling(float(DD14A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(DD14A)

                #B/E part
                BB94A = self.getrailvalue(['Series-C: UIO (32) Digital Input (0-5000)'], ['Future_Red_RLY'])
                B94=D.Ceiling(float(BB94A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(BB94A)
                EE14A = self.getrailvalue(['Series-C: UIO (32) Digital Output (0-5000)'], ['Future_Red_RLY'])
                E14=D.Ceiling(float(EE14A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(EE14A)

                #D/F part
                CC94A = self.getrailvalue(['Series-C: UIO (32) Digital Input (0-5000)'], ['Non_Red_RLY'])
                C94=D.Ceiling(float(CC94A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(CC94A)
                FF14A = self.getrailvalue(['Series-C: UIO (32) Digital Output (0-5000)'], ['Non_Red_RLY'])
                F14=D.Ceiling(float(FF14A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(FF14A)'''

                #HV RLY
                #G part Red
                GG11 = self.getrailvalue(['Series-C: UIO (32) Digital Input (0-5000)'], ['Red_HV_RLY'])
                GG11 = D.Ceiling(float(GG11)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(GG11)
                GG21 = self.getrailvalue(['Series-C: UIO (32) Digital Output (0-5000)'], ['Red_HV_RLY'])
                GG21 = D.Ceiling(float(GG21)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(GG21)
                
                #H part Future Red
                HH11 = self.getrailvalue(['Series-C: UIO (32) Digital Input (0-5000)'], ['Future_Red_HV_RLY'])
                HH11 = D.Ceiling(float(HH11)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(HH11)
                HH21 = self.getrailvalue(['Series-C: UIO (32) Digital Output (0-5000)'], ['Future_Red_HV_RLY'])
                HH21 = D.Ceiling(float(HH21)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(HH21)
                
                #I part Non Red
                II11 = self.getrailvalue(['Series-C: UIO (32) Digital Input (0-5000)'], ['Non_Red_HV_RLY'])
                II11 = D.Ceiling(float(II11)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(II11)
                II21 = self.getrailvalue(['Series-C: UIO (32) Digital Output (0-5000)'], ['Non_Red_HV_RLY'])
                II21 = D.Ceiling(float(II21)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(II21)
                
                #calcs for min max
                # XX61 calcs
                var1 =(A61+A81+A91)*25
                Trace.Write("var1:"+str(var1))
                var2 =D11* int(Do_point)
                Trace.Write("var2:"+str(var2))
                cal1 =D.Ceiling((var1 + var2)/9600.0)
                cal2 =D.Ceiling((A61+A81+A91+D11)/32.0)
                Trace.Write("cal1:"+str(cal1))
                Trace.Write("cal2:"+str(cal2))
                XX61=max(cal1,cal2)
                # XX62 calcs
                var3=(A62+A82+A92+A94+GG11)*25
                var4=(D12+D14+GG21)* int(Do_point)
                cal3 = D.Ceiling((var3 + var4)/9600.0)
                cal4 = D.Ceiling ((A62+A82+A92+A94+D12+D14+GG11+GG21)/32.0)
                XX62= max(cal3,cal4)
                # XX63 calcs
                var5=(A63+A73+A83+A93)*25
                var6 =D13* int(Do_point)
                cal5 =D.Ceiling((var5 + var6)/9600.0)
                cal6 =D.Ceiling((A63+A73+A83+A93+D13)/32.0)
                XX63=max(cal5,cal6)
                # XX81 calcs
                var7=(C61+C81+C91)*25
                var8=F11* int(Do_point)
                cal7 = D.Ceiling((var7 + var8)/9600.0)
                cal8 = D.Ceiling ((C61+C81+C91+F11)/32.0)
                XX81= max(cal7,cal8)
                # XX82 calcs
                var9=(C62+C82+C92+C94+II11)*25
                var10=(F12+F14+II21)* int(Do_point)
                cal9 = D.Ceiling((var9 + var10)/9600.0)
                cal10 = D.Ceiling ((C62+C82+C92+C94+F12+F14+II11+II21)/32.0)
                XX82= max(cal9,cal10)
                # XX83 calcs
                var11=(C63+C73+C83+C93)*25
                var12=F13* int(Do_point)
                cal11 = D.Ceiling((var11 + var12)/9600.0)
                cal12 = D.Ceiling ((C63+C73+C83+C93+F13)/32.0)
                XX83= max(cal11,cal12)
                # XX71 calcs
                var13=(B61+B81+B91)*25
                var14=E11* int(Do_point)
                cal13= D.Ceiling((var13 + var14)/9600.0)
                cal14= D.Ceiling ((B61+B81+B91+E11)/32.0)
                XX71= max(cal13,cal14)
                # XX72 calcs
                var15=(B62+B82+B92+B94+HH11)*25
                var16=(E12+E14+HH21)* int(Do_point)
                cal15 = D.Ceiling((var15 + var16)/9600.0)
                cal16 = D.Ceiling ((B62+B82+B92+B94+E12+E14+HH11+HH21)/32.0)
                XX72= max(cal15,cal16)
                # XX73 calcs
                var17=(B63+B73+B83+B93)*25
                var18=E13* int(Do_point)
                Trace.Write("var18 "+str(var18))
                Trace.Write("var17 "+str(var17))
                cal17 = D.Ceiling((var17 + var18)/9600.0)
                Trace.Write("calcs17 "+str(cal17))
                cal18 = D.Ceiling ((B63+B73+B83+B93+E13)/32.0)
                Trace.Write("calcs18 "+str(cal18))
                XX73= max(cal17,cal18)
                Trace.Write("XX73 "+str(XX73))
                #Trace.Write("ab "+str(XX61))
                Trace.Write("XX61: "+str(XX61))
                Trace.Write("XX62: "+str(XX62))
                Trace.Write("XX63: "+str(XX63))
                Trace.Write("XX81: "+str(XX81))
                Trace.Write("XX82: "+str(XX82))
                Trace.Write("XX83: "+str(XX83))
                Trace.Write("XX71: "+str(XX71))
                Trace.Write("XX72: "+str(XX72))
                Trace.Write("XX73: "+str(XX73))

                GS_Get_Set_AtvQty.setAtvQty(Product, 'SerC_IO_Params', 'X61', XX61)
                GS_Get_Set_AtvQty.setAtvQty(Product, 'SerC_IO_Params', 'X62', XX62)
                GS_Get_Set_AtvQty.setAtvQty(Product, 'SerC_IO_Params', 'X63', XX63)
                GS_Get_Set_AtvQty.setAtvQty(Product, 'SerC_IO_Params', 'X81', XX81)
                GS_Get_Set_AtvQty.setAtvQty(Product, 'SerC_IO_Params', 'X82', XX82)
                GS_Get_Set_AtvQty.setAtvQty(Product, 'SerC_IO_Params', 'X83', XX83)
                GS_Get_Set_AtvQty.setAtvQty(Product, 'SerC_IO_Params', 'X71', XX71)
                GS_Get_Set_AtvQty.setAtvQty(Product, 'SerC_IO_Params', 'X72', XX72)
                GS_Get_Set_AtvQty.setAtvQty(Product, 'SerC_IO_Params', 'X73', XX73)
                #Parts qnt calcs using above calcs
                Amp_A = D.Ceiling((var1+var2)/1000.0)+D.Ceiling((var3+var4)/1000.0)+D.Ceiling((var5+var6)/1000.0)+D.Ceiling((var7+var8)/1000.0)+D.Ceiling((var9+var10)/1000.0)+D.Ceiling((var11+var12)/1000.0)+D.Ceiling((var13+var14)/1000.0)+D.Ceiling((var15+var16)/1000.0)+D.Ceiling((var17+var18)/1000.0)
                PUIO31 = (2*(XX61+XX62+XX63)+(XX71 + XX72 + XX73 + XX81 + XX82 + XX83))
                TUIO41 = (XX61+XX62+XX63) + (XX71 + XX72 + XX73)
                TUIO31 = (XX81 + XX82 + XX83)
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
            if family=="Series C":
                ## Assigning user inputed value to pertivular veriable
                #A/D Part IS
                AA61A = self.getrailvalue(['Series-C: UIO (32) Analog Input (HLAI Adapt) (0-5000)'], ['Red_IS'])
                A61=D.Ceiling(float(AA61A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(AA61A)
                AA81A= self.getrailvalue(['Series-C: UIO (32) Analog Output (0-5000)'], ['Red_IS'])
                A81=D.Ceiling(float(AA81A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(AA81A)
                AA91A = self.getrailvalue(['Series-C: UIO (32) Digital Input (0-5000)'], ['Red_IS'])
                A91=D.Ceiling(float(AA91A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(AA91A)
                DD11A = self.getrailvalue(['Series-C: UIO (32) Digital Output (0-5000)'], ['Red_IS'])
                D11=D.Ceiling(float(DD11A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(DD11A)

                #B/E part IS
                BB61A = self.getrailvalue(['Series-C: UIO (32) Analog Input (HLAI Adapt) (0-5000)'], ['Future_Red_IS'])
                B61=D.Ceiling(float(BB61A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(BB61A)
                BB81A = self.getrailvalue(['Series-C: UIO (32) Analog Output (0-5000)'], ['Future_Red_IS'])
                B81=D.Ceiling(float(BB81A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(BB81A)
                BB91A = self.getrailvalue(['Series-C: UIO (32) Digital Input (0-5000)'], ['Future_Red_IS'])
                B91=D.Ceiling(float(BB91A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(BB91A)
                EE11A = self.getrailvalue(['Series-C: UIO (32) Digital Output (0-5000)'], ['Future_Red_IS'])
                E11=D.Ceiling(float(EE11A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(EE11A)

                #C/F  part IS
                CC61A = self.getrailvalue(['Series-C: UIO (32) Analog Input (HLAI Adapt) (0-5000)'], ['Non_Red_IS'])
                C61=D.Ceiling(float(CC61A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(CC61A)
                CC81A= self.getrailvalue(['Series-C: UIO (32) Analog Output (0-5000)'], ['Non_Red_IS'])
                C81=D.Ceiling(float(CC81A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(CC81A)
                CC91A = self.getrailvalue(['Series-C: UIO (32) Digital Input (0-5000)'], ['Non_Red_IS'])
                C91=D.Ceiling(float(CC91A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(CC91A)
                FF11A = self.getrailvalue(['Series-C: UIO (32) Digital Output (0-5000)'], ['Non_Red_IS'])
                F11=D.Ceiling(float(FF11A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(FF11A)

                ##NIS
                #A/D Part NIS
                AA62A = self.getrailvalue(['Series-C: UIO (32) Analog Input (HLAI Adapt) (0-5000)'], ['Red_NIS'])
                A62=D.Ceiling(float(AA62A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(AA62A)
                AA82A = self.getrailvalue(['Series-C: UIO (32) Analog Output (0-5000)'], ['Red_NIS'])
                A82=D.Ceiling(float(AA82A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(AA82A)
                AA92A = self.getrailvalue(['Series-C: UIO (32) Digital Input (0-5000)'], ['Red_NIS'])
                A92=D.Ceiling(float(AA92A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(AA92A)
                DD12A = self.getrailvalue(['Series-C: UIO (32) Digital Output (0-5000)'], ['Red_NIS'])
                D12=D.Ceiling(float(DD12A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(DD12A)

                #B/E part NIS
                BB62A = self.getrailvalue(['Series-C: UIO (32) Analog Input (HLAI Adapt) (0-5000)'], ['Future_Red_NIS'])
                B62=D.Ceiling(float(BB62A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(BB62A)
                BB82A= self.getrailvalue(['Series-C: UIO (32) Analog Output (0-5000)'], ['Future_Red_NIS'])
                B82=D.Ceiling(float(BB82A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(BB82A)
                BB92A = self.getrailvalue(['Series-C: UIO (32) Digital Input (0-5000)'], ['Future_Red_NIS'])
                B92=D.Ceiling(float(BB92A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(BB92A)
                EE12A = self.getrailvalue(['Series-C: UIO (32) Digital Output (0-5000)'], ['Future_Red_NIS'])
                E12=D.Ceiling(float(EE12A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(EE12A)

                #C/F part NIS
                CC62A = self.getrailvalue(['Series-C: UIO (32) Analog Input (HLAI Adapt) (0-5000)'], ['Non_Red_NIS'])
                C62=D.Ceiling(float(CC62A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(CC62A)
                CC82A = self.getrailvalue(['Series-C: UIO (32) Analog Output (0-5000)'], ['Non_Red_NIS'])
                C82=D.Ceiling(float(CC82A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(CC82A)
                CC92A = self.getrailvalue(['Series-C: UIO (32) Digital Input (0-5000)'], ['Non_Red_NIS'])
                C92=D.Ceiling(float(CC92A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(CC92A)
                FF12A = self.getrailvalue(['Series-C: UIO (32) Digital Output (0-5000)'], ['Non_Red_NIS'])
                F12=D.Ceiling(float(FF12A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(FF12A)

                ##ISLTR
                #A/D Part ISLTR
                AA63A = self.getrailvalue(['Series-C: UIO (32) Analog Input (HLAI Adapt) (0-5000)'], ['Red_ISLTR'])
                A63=D.Ceiling(float(AA63A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(AA63A)
                AA73A = self.getrailvalue(['Series-C: UIO (32) Analog Input (LLAI Adapt) (0-5000)'], ['Red_ISLTR'])
                A73=D.Ceiling(float(AA73A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(AA73A)
                AA83A= self.getrailvalue(['Series-C: UIO (32) Analog Output (0-5000)'], ['Red_ISLTR'])
                A83=D.Ceiling(float(AA83A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(AA83A)
                AA93A = self.getrailvalue(['Series-C: UIO (32) Digital Input (0-5000)'], ['Red_ISLTR'])
                A93=D.Ceiling(float(AA93A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(AA93A)
                DD13A = self.getrailvalue(['Series-C: UIO (32) Digital Output (0-5000)'], ['Red_ISLTR'])
                D13=D.Ceiling(float(DD13A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(DD13A)

                #B/E Part ISLTR
                BB63A = self.getrailvalue(['Series-C: UIO (32) Analog Input (HLAI Adapt) (0-5000)'], ['Future_Red_ISLTR'])
                B63=D.Ceiling(float(BB63A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(BB63A)
                BB73A = self.getrailvalue(['Series-C: UIO (32) Analog Input (LLAI Adapt) (0-5000)'], ['Future_Red_ISLTR'])
                B73=D.Ceiling(float(BB73A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(BB63A)
                BB83A = self.getrailvalue(['Series-C: UIO (32) Analog Output (0-5000)'], ['Future_Red_ISLTR'])
                B83=D.Ceiling(float(BB83A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(BB83A)
                BB93A = self.getrailvalue(['Series-C: UIO (32) Digital Input (0-5000)'], ['Future_Red_ISLTR'])
                B93=D.Ceiling(float(BB93A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(BB93A)
                EE13A = self.getrailvalue(['Series-C: UIO (32) Digital Output (0-5000)'], ['Future_Red_ISLTR'])
                E13=D.Ceiling(float(EE13A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(EE13A)

                #C/F Part ISLTR
                CC63A = self.getrailvalue(['Series-C: UIO (32) Analog Input (HLAI Adapt) (0-5000)'], ['Non_Red_ISLTR'])
                C63=D.Ceiling(float(CC63A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(CC63A)
                CC73A = self.getrailvalue(['Series-C: UIO (32) Analog Input (LLAI Adapt) (0-5000)'], ['Non_Red_ISLTR'])
                C73=D.Ceiling(float(CC73A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(CC73A)
                CC83A = self.getrailvalue(['Series-C: UIO (32) Analog Output (0-5000)'], ['Non_Red_ISLTR'])
                C83=D.Ceiling(float(CC83A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(CC83A)
                CC93A = self.getrailvalue(['Series-C: UIO (32) Digital Input (0-5000)'], ['Non_Red_ISLTR'])
                C93=D.Ceiling(float(CC93A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(CC93A)
                FF13A = self.getrailvalue(['Series-C: UIO (32) Digital Output (0-5000)'], ['Non_Red_ISLTR'])
                F13=D.Ceiling(float(FF13A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(FF13A)

                #RLY only container
                #A/D part
                AA94A = self.getrailvalue(['Series-C: UIO (32) Digital Input (0-5000)'], ['Red_RLY'])
                A94=D.Ceiling(float(AA94A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(AA94A)
                DD14A= self.getrailvalue(['Series-C: UIO (32) Digital Output (0-5000)'], ['Red_RLY'])
                D14=D.Ceiling(float(DD14A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(DD14A)

                #B/E part
                BB94A = self.getrailvalue(['Series-C: UIO (32) Digital Input (0-5000)'], ['Future_Red_RLY'])
                B94=D.Ceiling(float(BB94A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(BB94A)
                EE14A = self.getrailvalue(['Series-C: UIO (32) Digital Output (0-5000)'], ['Future_Red_RLY'])
                E14=D.Ceiling(float(EE14A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(EE14A)

                #D/F part
                CC94A = self.getrailvalue(['Series-C: UIO (32) Digital Input (0-5000)'], ['Non_Red_RLY'])
                C94=D.Ceiling(float(CC94A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(CC94A)
                FF14A = self.getrailvalue(['Series-C: UIO (32) Digital Output (0-5000)'], ['Non_Red_RLY'])
                F14=D.Ceiling(float(FF14A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(FF14A)

                #HV RLY
                #G part Red
                GG11 = self.getrailvalue(['Series-C: UIO (32) Digital Input (0-5000)'], ['Red_HV_RLY'])
                GG11 = D.Ceiling(float(GG11)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(GG11)
                GG21 = self.getrailvalue(['Series-C: UIO (32) Digital Output (0-5000)'], ['Red_HV_RLY'])
                GG21 = D.Ceiling(float(GG21)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(GG21)
                
                #H part Future Red
                HH11 = self.getrailvalue(['Series-C: UIO (32) Digital Input (0-5000)'], ['Future_Red_HV_RLY'])
                HH11 = D.Ceiling(float(HH11)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(HH11)
                HH21 = self.getrailvalue(['Series-C: UIO (32) Digital Output (0-5000)'], ['Future_Red_HV_RLY'])
                HH21 = D.Ceiling(float(HH21)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(HH21)
                
                #I part Non Red
                II11 = self.getrailvalue(['Series-C: UIO (32) Digital Input (0-5000)'], ['Non_Red_HV_RLY'])
                II11 = D.Ceiling(float(II11)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(II11)
                II21 = self.getrailvalue(['Series-C: UIO (32) Digital Output (0-5000)'], ['Non_Red_HV_RLY'])
                II21 = D.Ceiling(float(II21)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(II21)
                
                #calcs for min max
                # XX61 calcs
                var1 =(A61+A81+A91)*25
                var2 =D11* int(Do_point)
                cal1 =D.Ceiling((var1 + var2)/9600.0)
                cal2 =D.Ceiling((A61+A81+A91+D11)/32.0)
                XX61=max(cal1,cal2)
                # XX62 calcs
                var3=(A62+A82+A92+A94+GG11)*25
                var4=(D12+D14+GG21)* int(Do_point)
                cal3 = D.Ceiling((var3 + var4)/9600.0)
                cal4 = D.Ceiling ((A62+A82+A92+A94+D12+D14+GG11+GG21)/32.0)
                XX62= max(cal3,cal4)
                # XX63 calcs
                var5=(A63+A73+A83+A93)*25
                var6 =D13* int(Do_point)
                cal5 =D.Ceiling((var5 + var6)/9600.0)
                cal6 =D.Ceiling((A63+A73+A83+A93+D13)/32.0)
                XX63=max(cal5,cal6)
                # XX81 calcs
                var7=(C61+C81+C91)*25
                var8=F11* int(Do_point)
                cal7 = D.Ceiling((var7 + var8)/9600.0)
                cal8 = D.Ceiling ((C61+C81+C91+F11)/32.0)
                XX81= max(cal7,cal8)
                # XX82 calcs
                var9=(C62+C82+C92+C94+II11)*25
                var10=(F12+F14+II21)* int(Do_point)
                cal9 = D.Ceiling((var9 + var10)/9600.0)
                cal10 = D.Ceiling ((C62+C82+C92+C94+F12+F14+II11+II21)/32.0)
                XX82= max(cal9,cal10)
                # XX83 calcs
                var11=(C63+C73+C83+C93)*25
                var12=F13* int(Do_point)
                cal11 = D.Ceiling((var11 + var12)/9600.0)
                cal12 = D.Ceiling ((C63+C73+C83+C93+F13)/32.0)
                XX83= max(cal11,cal12)
                # XX71 calcs
                var13=(B61+B81+B91)*25
                var14=E11* int(Do_point)
                cal13= D.Ceiling((var13 + var14)/9600.0)
                cal14= D.Ceiling ((B61+B81+B91+E11)/32.0)
                XX71= max(cal13,cal14)
                # XX72 calcs
                var15=(B62+B82+B92+B94+HH11)*25
                var16=(E12+E14+HH21)* int(Do_point)
                cal15 = D.Ceiling((var15 + var16)/9600.0)
                cal16 = D.Ceiling ((B62+B82+B92+B94+E12+E14+HH11+HH21)/32.0)
                XX72= max(cal15,cal16)
                # XX73 calcs
                var17=(B63+B73+B83+B93)*25
                var18=E13* int(Do_point)
                Trace.Write("var18 "+str(var18))
                Trace.Write("var17 "+str(var17))
                cal17 = D.Ceiling((var17 + var18)/9600.0)
                Trace.Write("calcs17 "+str(cal17))
                cal18 = D.Ceiling ((B63+B73+B83+B93+E13)/32.0)
                Trace.Write("calcs18 "+str(cal18))
                XX73= max(cal17,cal18)
                Trace.Write("XX73 "+str(XX73))
                #Trace.Write("ab "+str(XX61))
                Trace.Write("XX61: "+str(XX61))
                Trace.Write("XX62: "+str(XX62))
                Trace.Write("XX63: "+str(XX63))
                Trace.Write("XX81: "+str(XX81))
                Trace.Write("XX82: "+str(XX82))
                Trace.Write("XX83: "+str(XX83))
                Trace.Write("XX71: "+str(XX71))
                Trace.Write("XX72: "+str(XX72))
                Trace.Write("XX73: "+str(XX73))
                GS_Get_Set_AtvQty.setAtvQty(Product, 'SerC_IO_Params', 'X61', XX61)
                GS_Get_Set_AtvQty.setAtvQty(Product, 'SerC_IO_Params', 'X62', XX62)
                GS_Get_Set_AtvQty.setAtvQty(Product, 'SerC_IO_Params', 'X63', XX63)
                GS_Get_Set_AtvQty.setAtvQty(Product, 'SerC_IO_Params', 'X81', XX81)
                GS_Get_Set_AtvQty.setAtvQty(Product, 'SerC_IO_Params', 'X82', XX82)
                GS_Get_Set_AtvQty.setAtvQty(Product, 'SerC_IO_Params', 'X83', XX83)
                GS_Get_Set_AtvQty.setAtvQty(Product, 'SerC_IO_Params', 'X71', XX71)
                GS_Get_Set_AtvQty.setAtvQty(Product, 'SerC_IO_Params', 'X72', XX72)
                GS_Get_Set_AtvQty.setAtvQty(Product, 'SerC_IO_Params', 'X73', XX73)
                #Parts qnt calcs using above calcs
                Amp_A = D.Ceiling((var1+var2)/1000.0)+D.Ceiling((var3+var4)/1000.0)+D.Ceiling((var5+var6)/1000.0)+D.Ceiling((var7+var8)/1000.0)+D.Ceiling((var9+var10)/1000.0)+D.Ceiling((var11+var12)/1000.0)+D.Ceiling((var13+var14)/1000.0)+D.Ceiling((var15+var16)/1000.0)+D.Ceiling((var17+var18)/1000.0)
                PUIO31 = (2*(XX61+XX62+XX63)+(XX71 + XX72 + XX73 + XX81 + XX82 + XX83))
                TUIO41 = (XX61+XX62+XX63) + (XX71 + XX72 + XX73)
                TUIO31 = (XX81 + XX82 + XX83)
        
        return int(PUIO31),int(TUIO41),int(TUIO31),Amp_A