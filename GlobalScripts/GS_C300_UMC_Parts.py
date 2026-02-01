import math
#CXCPQ-46424
def get_UPTA01(Product):
    if Product.Name == 'Series-C Control Group':
        A=A1=A2=0
        cg_per_A = 0
        cg_per = int(Product.Attr('SerC_CG_Percent_Installed_Spare').GetValue()) if Product.Attr('SerC_CG_Percent_Installed_Spare').GetValue()!='' else 0
        cg_cont_list= ['C300_C IO MS','C300_CG_Universal_IO_cont_1','C300_CG_Universal_IO_cont_2','SerC_CG_Enhanced_Function_IO_Cont']
        col_val = ['Red_NIS','Future_Red_NIS','Non_Red_NIS']
        cg_IO_val = ['Series-C: DI (32) 24 VDC with Open Wire Detect (0-5000)','Series-C: DI (32) 24VDC SOE (0-5000)','Series-C: DO (32) 24VDC Bus External Power Supply (0-5000)','Series-C: DO (32) 24VDC Bus Internal Power Supply (0-5000)','Series-C: HLAI (13-16) with HART with differential inputs (0-5000)','Series-C: HLAI (13-16) without HART with differential inputs (0-5000)']

        for cont in cg_cont_list:
            for row in Product.GetContainerByName(str(cont)).Rows:
                for col in col_val:
                    A1 += int(row[str(col)]) if row[str(col)] != '' else 0
        Trace.Write(A1)

        # SerC_CG_Enhanced_Function_IO_Cont2
        for row in Product.GetContainerByName('SerC_CG_Enhanced_Function_IO_Cont2').Rows:
            if row['IO_Type'] in cg_IO_val:
                for col in col_val:
                    A2 += int(row[str(col)]) if row[str(col)] != '' else 0
        Trace.Write("Enhance cont:"+str(A2))

        A = A1+A2
        # Percent calcs
        cg_per_A = math.ceil((1+(cg_per/100.0))*A)
        return int(cg_per_A)
    elif Product.Name == 'Series-C Remote Group':
        A=A1=A2=0
        rg_per_A = 0
        rg_per = int(Product.Attr('SerC_RG_Percent_Installed_Spare(0-100%)').GetValue()) if Product.Attr('SerC_RG_Percent_Installed_Spare(0-100%)').GetValue()!='' else 0
        rg_cont_list= ['C300_C IO_RG MS','C300_RG_Universal_IO_cont_1','C300_RG_Universal_IO_cont_2','SerC_RG_Enhanced_Function_IO_Cont']
        col_val = ['Red_NIS','Future_Red_NIS','Non_Red_NIS']
        rg_IO_val = ['Series-C: DI (32) 24 VDC with Open Wire Detect (0-5000)','Series-C: DI (32) 24VDC SOE (0-5000)','Series-C: DO (32) 24VDC Bus External Power Supply (0-5000)','Series-C: DO (32) 24VDC Bus Internal Power Supply (0-5000)','Series-C: HLAI (13-16) with HART with differential inputs (0-5000)','Series-C: HLAI (13-16) without HART with differential inputs (0-5000)']

        for cont in rg_cont_list:
            for row in Product.GetContainerByName(str(cont)).Rows:
                for col in col_val:
                    A1 += int(row[str(col)]) if row[str(col)] != '' else 0
        Trace.Write(A1)

        # SerC_RG_Enhanced_Function_IO_Cont2
        for row in Product.GetContainerByName('SerC_RG_Enhanced_Function_IO_Cont2').Rows:
            if row['IO_Type'] in rg_IO_val:
                for col in col_val:
                    A2 += int(row[str(col)]) if row[str(col)] != '' else 0
        Trace.Write("Enhance cont:"+str(A2))

        A = A1+A2
        # Percent calcs
        rg_per_A = math.ceil((1+(rg_per/100.0))*A)
        return int(rg_per_A)
        
def get_UDIA01(Product):
    IO_familyType=Product.Attr('SerC_CG_IO_Family_Type').GetValue()
    if Product.Name == 'Series-C Control Group':
        A=0
        cg_per_HV_A = 0
        col_val=[]
        cg_IO_val={}
        cg_per = int(Product.Attr('SerC_CG_Percent_Installed_Spare').GetValue()) if Product.Attr('SerC_CG_Percent_Installed_Spare').GetValue()!='' else 0
        if IO_familyType=="Series C":
            col_val   = ['Red_HV_RLY','Future_Red_HV_RLY','Non_Red_HV_RLY']
            cg_IO_val = {'C300_CG_Universal_IO_cont_2':['Series-C: UIO (32) Digital Input (0-5000)'],'SerC_CG_Enhanced_Function_IO_Cont2':['Series-C: DI (32) 24 VDC with Open Wire Detect (0-5000)','Series-C: DI (32) 24VDC SOE (0-5000)']}
        elif IO_familyType=="Series-C Mark II":
            col_val   = ['Red_HV_Rly','Future_HV_Rly','Non_Red_HV_Rly']
            cg_IO_val = {'C300_C IO MS3':['SCM: DI (32) 24VDC (0-5000)','SCM: DI (32) 24VDC SOE (0-5000)'],'C300_CG_Universal_IO_Mark_2':['SCM: UIO (32) Digital Input (0-5000)'],'C300_SerC_Enhanced_Function_IO_Mark_Group_CG_Cont1':['SCM: DI (32) 24 VDC with Open Wire Detect (0-5000)']}
        if len(col_val)>0 and len(cg_IO_val)>0:
            for cont,IO_vals in cg_IO_val.items():
                for row in Product.GetContainerByName(str(cont)).Rows:
                    if row['IO_Type'] in IO_vals:
                        for col in col_val:
                            A += int(row[str(col)]) if row[str(col)] != '' else 0

        # Percent calcs
        cg_per_HV_A = math.ceil((1+(cg_per/100.0))*A)
        return int(cg_per_HV_A)
    elif Product.Name == 'Series-C Remote Group':
        A=0
        rg_per_HV_A = 0
        col_val=[]
        rg_IO_val={}
        rg_per = int(Product.Attr('SerC_RG_Percent_Installed_Spare(0-100%)').GetValue()) if Product.Attr('SerC_RG_Percent_Installed_Spare(0-100%)').GetValue()!='' else 0
        if IO_familyType=="Series C":
            col_val   = ['Red_HV_RLY','Future_Red_HV_RLY','Non_Red_HV_RLY']
            rg_IO_val = {'C300_RG_Universal_IO_cont_2':['Series-C: UIO (32) Digital Input (0-5000)'],'SerC_RG_Enhanced_Function_IO_Cont2':['Series-C: DI (32) 24 VDC with Open Wire Detect (0-5000)','Series-C: DI (32) 24VDC SOE (0-5000)']}
        elif IO_familyType=="Series-C Mark II":
            col_val   = ['Red_HV_Rly','Future_HV_Rly','Non_Red_HV_Rly']
            rg_IO_val = {'C300_C IO_RG MS3':['SCM: DI (32) 24VDC (0-5000)','SCM: DI (32) 24VDC SOE (0-5000)'],'C300_CG_Universal_IO_Mark_2':['SCM: UIO (32) Digital Input (0-5000)'],'C300_SerC_Enhanced_Function_IO_Mark_Group_RG_Cont1':['SCM: DI (32) 24 VDC with Open Wire Detect (0-5000)']}
        if len(col_val)>0 and len(rg_IO_val)>0:
            for cont,IO_vals in rg_IO_val.items():
                for row in Product.GetContainerByName(str(cont)).Rows:
                    if row['IO_Type'] in IO_vals:
                        for col in col_val:
                            A += int(row[str(col)]) if row[str(col)] != '' else 0

        # Percent calcs
        rg_per_HV_A = math.ceil((1+(rg_per/100.0))*A)
        return int(rg_per_HV_A)
    
def get_UDOA01(Product):
    IO_familyType=Product.Attr('SerC_CG_IO_Family_Type').GetValue()
    if Product.Name == 'Series-C Control Group':
        A=0
        cg_per_HV_A = 0
        col_val=[]
        cg_IO_val={}
        cg_per = int(Product.Attr('SerC_CG_Percent_Installed_Spare').GetValue()) if Product.Attr('SerC_CG_Percent_Installed_Spare').GetValue()!='' else 0
        if IO_familyType=="Series C":
            col_val = ['Red_HV_RLY','Future_Red_HV_RLY','Non_Red_HV_RLY']
            cg_IO_val = {'C300_CG_Universal_IO_cont_2':['Series-C: UIO (32) Digital Output (0-5000)'],'SerC_CG_Enhanced_Function_IO_Cont2':['Series-C: DO (32) 24VDC Bus External Power Supply (0-5000)','Series-C: DO (32) 24VDC Bus Internal Power Supply (0-5000)']}
        elif IO_familyType=="Series-C Mark II":
            col_val = ['Red_HV_Rly','Future_HV_Rly','Non_Red_HV_Rly']
            cg_IO_val={'C300_SerC_Enhanced_Function_IO_Mark_Group_CG_Cont1':['SCM: DO (32) 24VDC Bus External Power Supply (0-5000)','SCM: DO (32) 24VDC Bus Internal Power Supply (0-5000)'],'C300_C IO MS3':['SCM: DO (32) 24VDC Bus External Power Supply (0-5000)','SCM: DO (32) 24VDC Bus Internal Power Supply  (0-5000)'],'C300_CG_Universal_IO_Mark_2':['SCM: UIO (32) Digital Output (0-5000)']}
            
        if len(col_val)>0 and len(cg_IO_val)>0:
            for cont,IO_vals in cg_IO_val.items():
                for row in Product.GetContainerByName(str(cont)).Rows:
                    if row['IO_Type'] in IO_vals:
                        for col in col_val:
                            A += int(row[str(col)]) if row[str(col)] != '' else 0
        
        # Percent calcs
        cg_per_HV_A = math.ceil((1+(cg_per/100.0))*A)
        return int(cg_per_HV_A)
    elif Product.Name == 'Series-C Remote Group':
        A=0
        rg_per_HV_A = 0
        col_val=[]
        rg_IO_val={}
        rg_per = int(Product.Attr('SerC_RG_Percent_Installed_Spare(0-100%)').GetValue()) if Product.Attr('SerC_RG_Percent_Installed_Spare(0-100%)').GetValue()!='' else 0
        if IO_familyType=="Series C":
            col_val = ['Red_HV_RLY','Future_Red_HV_RLY','Non_Red_HV_RLY']
            rg_IO_val = {'C300_RG_Universal_IO_cont_2':['Series-C: UIO (32) Digital Output (0-5000)'],'SerC_RG_Enhanced_Function_IO_Cont2':['Series-C: DO (32) 24VDC Bus External Power Supply (0-5000)','Series-C: DO (32) 24VDC Bus Internal Power Supply (0-5000)']}
        elif IO_familyType=="Series-C Mark II":
            col_val = ['Red_HV_Rly','Future_HV_Rly','Non_Red_HV_Rly']
            rg_IO_val = {'C300_SerC_Enhanced_Function_IO_Mark_Group_RG_Cont1':['SCM: DO (32) 24VDC Bus External Power Supply (0-5000)','SCM: DO (32) 24VDC Bus Internal Power Supply (0-5000)'],'C300_C IO_RG MS3':['SCM: DO (32) 24VDC Bus External Power Supply (0-5000)','SCM: DO (32) 24VDC Bus Internal Power Supply  (0-5000)'],'C300_CG_Universal_IO_Mark_2':['SCM: UIO (32) Digital Output (0-5000)']}
        if len(col_val)>0 and len(rg_IO_val)>0:
            for cont,IO_vals in rg_IO_val.items():
                for row in Product.GetContainerByName(str(cont)).Rows:
                    if row['IO_Type'] in IO_vals:
                        for col in col_val:
                            A += int(row[str(col)]) if row[str(col)] != '' else 0

        # Percent calcs
        rg_per_HV_A = math.ceil((1+(rg_per/100.0))*A)
        return int(rg_per_HV_A)
        
#CXCPQ-46430,CXCPQ-46433
def get_UAIA01(Product):
    if Product.Name == 'Series-C Control Group':
        C=E=0
        cg_per_C = 0
        cg_per_E = 0
        cg_per = int(Product.Attr('SerC_CG_Percent_Installed_Spare').GetValue()) if Product.Attr('SerC_CG_Percent_Installed_Spare').GetValue()!='' else 0
        col_val = ['Red_ISLTR','Future_Red_ISLTR','Non_Red_ISLTR']
        # Cont-Col map
        Cont_IO_C = {'C300_C IO MS':['Series-C: HLAI (16) 4-20mA (0-5000)','Series-C: HLAI (16) HART Config/Status (0-5000)'],'C300_CG_Universal_IO_cont_1':['Series-C: UIO (32) Analog Input (HLAI Adapt) (0-5000)'],'SerC_CG_Enhanced_Function_IO_Cont':['Series-C: HLAI (16) with HART with differential inputs (0-5000)','Series-C: HLAI (16) without HART with differential inputs (0-5000)','Series-C: HLAI (13-16) with HART with differential inputs (0-5000)','Series-C: HLAI (13-16) without HART with differential inputs (0-5000)']}
        Cont_IO_E = {'C300_C IO MS':['Series-C: AO (16) (0-5000)','Series-C: AO (16) HART Config/Status (0-5000)'],'C300_CG_Universal_IO_cont_1':['Series-C: UIO (32) Analog Output (0-5000)'],'SerC_CG_Enhanced_Function_IO_Cont':['Series-C: AO (16) HART (0-5000)']}

        for cont,IO_vals in Cont_IO_C.items():
            for row in Product.GetContainerByName(str(cont)).Rows:
                if row['IO_Type'] in IO_vals:
                    for col in col_val:
                        C += int(row[str(col)]) if row[str(col)] != '' else 0

        for cont,IO_vals in Cont_IO_E.items():
            for row in Product.GetContainerByName(str(cont)).Rows:
                if row['IO_Type'] in IO_vals:
                    for col in col_val:
                        E += int(row[str(col)]) if row[str(col)] != '' else 0
        Trace.Write(E)
        # Percent calcs
        cg_per_C = math.ceil(round(((1+(cg_per/100.0))*C),10))
        cg_per_E = math.ceil(round(((1+(cg_per/100.0))*E),10))
        return int(cg_per_C), int(cg_per_E)
    elif Product.Name == 'Series-C Remote Group':
        C=E=0
        rg_per_C = 0
        rg_per_E = 0
        rg_per = int(Product.Attr('SerC_RG_Percent_Installed_Spare(0-100%)').GetValue()) if Product.Attr('SerC_RG_Percent_Installed_Spare(0-100%)').GetValue()!='' else 0
        col_val = ['Red_ISLTR','Future_Red_ISLTR','Non_Red_ISLTR']
        # Cont-Col map
        Cont_IO_C = {'C300_C IO_RG MS':['Series-C: HLAI (16) 4-20mA (0-5000)','Series-C: HLAI (16) HART Config/Status (0-5000)'],'C300_RG_Universal_IO_cont_1':['Series-C: UIO (32) Analog Input (HLAI Adapt) (0-5000)'],'SerC_RG_Enhanced_Function_IO_Cont':['Series-C: HLAI (16) with HART with differential inputs (0-5000)','Series-C: HLAI (16) without HART with differential inputs (0-5000)','Series-C: HLAI (13-16) with HART with differential inputs (0-5000)','Series-C: HLAI (13-16) without HART with differential inputs (0-5000)']}

        Cont_IO_E = {'C300_C IO_RG MS':['Series-C: AO (16) (0-5000)','Series-C: AO (16) HART Config/Status (0-5000)'],'C300_RG_Universal_IO_cont_1':['Series-C: UIO (32) Analog Output (0-5000)'],'SerC_RG_Enhanced_Function_IO_Cont':['Series-C: AO (16) HART (0-5000)']}

        for cont,IO_vals in Cont_IO_C.items():
            for row in Product.GetContainerByName(str(cont)).Rows:
                if row['IO_Type'] in IO_vals:
                    for col in col_val:
                        C += int(row[str(col)]) if row[str(col)] != '' else 0
        Trace.Write(C)
        for cont,IO_vals in Cont_IO_E.items():
            for row in Product.GetContainerByName(str(cont)).Rows:
                if row['IO_Type'] in IO_vals:
                    for col in col_val:
                        E += int(row[str(col)]) if row[str(col)] != '' else 0
        Trace.Write(E)
        # Percent calcs
        rg_per_C = math.ceil(round(((1+(rg_per/100.0))*C),10))
        rg_per_E = math.ceil(round(((1+(rg_per/100.0))*E),10))
        return int(rg_per_C),int(rg_per_E)
#CXCPQ-46091,CXCPQ-43585
def get_RLY(Product):
    if Product.Name == 'Series-C Control Group':
        J=I=0
        cg_per_J = 0
        cg_per_I = 0
        cg_per = int(Product.Attr('SerC_CG_Percent_Installed_Spare').GetValue()) if Product.Attr('SerC_CG_Percent_Installed_Spare').GetValue()!='' else 0
        col_val = ['Red_RLY','Future_Red_RLY','Non_Red_RLY']
        Cont_IO_J = {'C300_CG_Universal_IO_cont_2':['Series-C: UIO (32) Digital Output (0-5000)'],'SerC_CG_Enhanced_Function_IO_Cont2':['Series-C: DO (32) 24VDC Bus External Power Supply (0-5000)','Series-C: DO (32) 24VDC Bus Internal Power Supply (0-5000)']}
        Cont_IO_I = {'C300_CG_Universal_IO_cont_2':['Series-C: UIO (32) Digital Input (0-5000)'],'SerC_CG_Enhanced_Function_IO_Cont2':['Series-C: DI (32) 24 VDC with Open Wire Detect (0-5000)','Series-C: DI (32) 24VDC SOE (0-5000)']}

        for cont,IO_vals in Cont_IO_J.items():
            for row in Product.GetContainerByName(str(cont)).Rows:
                if row['IO_Type'] in IO_vals:
                    for col in col_val:
                        J += int(row[str(col)]) if row[str(col)] != '' else 0
        Trace.Write(J)
        for cont,IO_vals in Cont_IO_I.items():
            for row in Product.GetContainerByName(str(cont)).Rows:
                if row['IO_Type'] in IO_vals:
                    for col in col_val:
                        I += int(row[str(col)]) if row[str(col)] != '' else 0
        Trace.Write(I)
        # Percent calcs
        cg_per_J = math.ceil((1+(cg_per/100.0))*J)
        cg_per_I = math.ceil((1+(cg_per/100.0))*I)
        return int(cg_per_J),int(cg_per_I)
    elif Product.Name == 'Series-C Remote Group':
        J=I=0
        rg_per_J = 0
        rg_per_I = 0
        rg_per = int(Product.Attr('SerC_RG_Percent_Installed_Spare(0-100%)').GetValue()) if Product.Attr('SerC_RG_Percent_Installed_Spare(0-100%)').GetValue()!='' else 0
        col_val = ['Red_RLY','Future_Red_RLY','Non_Red_RLY']
        # Cont-Col map
        Cont_IO_J = {'C300_RG_Universal_IO_cont_2':['Series-C: UIO (32) Digital Output (0-5000)'],'SerC_RG_Enhanced_Function_IO_Cont2':['Series-C: DO (32) 24VDC Bus External Power Supply (0-5000)','Series-C: DO (32) 24VDC Bus Internal Power Supply (0-5000)']}
        Cont_IO_I = {'C300_RG_Universal_IO_cont_2':['Series-C: UIO (32) Digital Input (0-5000)'],'SerC_RG_Enhanced_Function_IO_Cont2':['Series-C: DI (32) 24 VDC with Open Wire Detect (0-5000)','Series-C: DI (32) 24VDC SOE (0-5000)']}

        for cont,IO_vals in Cont_IO_J.items():
            for row in Product.GetContainerByName(str(cont)).Rows:
                if row['IO_Type'] in IO_vals:
                    for col in col_val:
                        J += int(row[str(col)]) if row[str(col)] != '' else 0
        Trace.Write(J)
        for cont,IO_vals in Cont_IO_I.items():
            for row in Product.GetContainerByName(str(cont)).Rows:
                if row['IO_Type'] in IO_vals:
                    for col in col_val:
                        I += int(row[str(col)]) if row[str(col)] != '' else 0
        Trace.Write(I)
        # Percent calcs
        rg_per_J = math.ceil((1+(rg_per/100.0))*J)
        rg_per_I = math.ceil((1+(rg_per/100.0))*I)
        return int(rg_per_J),int(rg_per_I)
#CXCPQ-46429,CXCPQ-46431,CXCPQ-46800
def get_IS(Product):
    if Product.Name == 'Series-C Control Group':
        B=D=G=H=0
        cg_per_B = 0
        cg_per_D = 0
        cg_per_G = 0
        cg_per_H = 0
        cg_per = int(Product.Attr('SerC_CG_Percent_Installed_Spare').GetValue()) if Product.Attr('SerC_CG_Percent_Installed_Spare').GetValue()!='' else 0
        col_val = ['Red_IS','Future_Red_IS','Non_Red_IS']
        # Cont-Col map
        #CXDEV-8238 Split G value into G and H
        Cont_IO_B = {'C300_C IO MS':['Series-C: HLAI (16) 4-20mA (0-5000)','Series-C: HLAI (16) HART Config/Status (0-5000)'],'C300_CG_Universal_IO_cont_1':['Series-C: UIO (32) Analog Input (HLAI Adapt) (0-5000)'],'SerC_CG_Enhanced_Function_IO_Cont':['Series-C: HLAI (16) with HART with differential inputs (0-5000)','Series-C: HLAI (16) without HART with differential inputs (0-5000)','Series-C: HLAI (13-16) with HART with differential inputs (0-5000)','Series-C: HLAI (13-16) without HART with differential inputs (0-5000)']}
        Cont_IO_D = {'C300_C IO MS':['Series-C: AO (16) (0-5000)','Series-C: AO (16) HART Config/Status (0-5000)'],'C300_CG_Universal_IO_cont_1':['Series-C: UIO (32) Analog Output (0-5000)'],'SerC_CG_Enhanced_Function_IO_Cont':['Series-C: AO (16) HART (0-5000)']}
        Cont_IO_G = {'C300_CG_Universal_IO_cont_2':['Series-C: UIO (32) Digital Output (0-5000)']}
        IO_G = ['Series-C: DO (32) 24VDC Bus External Power Supply (0-5000)','Series-C: DO (32) 24VDC Bus Internal Power Supply (0-5000)']
        Cont_IO_H = {'C300_CG_Universal_IO_cont_2':['Series-C: UIO (32) Digital Input (0-5000)']}
        IO_H = ['Series-C: DI (32) 24 VDC with Open Wire Detect (0-5000)','Series-C: DI (32) 24VDC SOE (0-5000)']
        for cont,IO_vals in Cont_IO_B.items():
            for row in Product.GetContainerByName(str(cont)).Rows:
                if row['IO_Type'] in IO_vals:
                    for col in col_val:
                        B += int(row[str(col)]) if row[str(col)] != '' else 0
        Trace.Write(B)
        for cont,IO_vals in Cont_IO_D.items():
            for row in Product.GetContainerByName(str(cont)).Rows:
                if row['IO_Type'] in IO_vals:
                    for col in col_val:
                        D += int(row[str(col)]) if row[str(col)] != '' else 0
        Trace.Write(D)
        for cont,IO_vals in Cont_IO_G.items():
            for row in Product.GetContainerByName(str(cont)).Rows:
                if row['IO_Type'] in IO_vals:
                    for col in col_val:
                        G += int(row[str(col)]) if row[str(col)] != '' else 0
        Trace.Write("G1:"+str(G))
        for row in Product.GetContainerByName('SerC_CG_Enhanced_Function_IO_Cont2').Rows:
            if row['IO_Type'] in IO_G:
                G += int(row['Red_IS']) if row['Red_IS'] != '' else 0
        Trace.Write(G)
        for cont,IO_vals in Cont_IO_H.items():
            for row in Product.GetContainerByName(str(cont)).Rows:
                if row['IO_Type'] in IO_vals:
                    for col in col_val:
                        H += int(row[str(col)]) if row[str(col)] != '' else 0
                        Trace.Write("H1:"+str(H))
        for row in Product.GetContainerByName('SerC_CG_Enhanced_Function_IO_Cont2').Rows:
            if row['IO_Type'] in IO_H:
                H += int(row['Red_IS']) if row['Red_IS'] != '' else 0 

        Trace.Write(H)
        # Percent calcs
        cg_per_B = math.ceil(round(((1+(cg_per/100.0))*B),10))
        cg_per_D = math.ceil(round(((1+(cg_per/100.0))*D),10))
        cg_per_G = math.ceil(round(((1+(cg_per/100.0))*G),10))
        cg_per_H = math.ceil(round(((1+(cg_per/100.0))*H),10))
        return int(cg_per_B),int(cg_per_D),int(cg_per_G),int(cg_per_H)
    elif Product.Name == 'Series-C Remote Group':
        B=D=G=H=0
        rg_per_B = 0
        rg_per_D = 0
        rg_per_G = 0
        rg_per_H = 0
        rg_per = int(Product.Attr('SerC_RG_Percent_Installed_Spare(0-100%)').GetValue()) if Product.Attr('SerC_RG_Percent_Installed_Spare(0-100%)').GetValue()!='' else 0
        col_val = ['Red_IS','Future_Red_IS','Non_Red_IS']
        # Cont-Col map
        #CXDEV-8238 Split G value into G and H
        Cont_IO_B = {'C300_C IO_RG MS':['Series-C: HLAI (16) 4-20mA (0-5000)','Series-C: HLAI (16) HART Config/Status (0-5000)'],'C300_RG_Universal_IO_cont_1':['Series-C: UIO (32) Analog Input (HLAI Adapt) (0-5000)'],'SerC_RG_Enhanced_Function_IO_Cont':['Series-C: HLAI (16) with HART with differential inputs (0-5000)','Series-C: HLAI (16) without HART with differential inputs (0-5000)','Series-C: HLAI (13-16) with HART with differential inputs (0-5000)','Series-C: HLAI (13-16) without HART with differential inputs (0-5000)']}
        Cont_IO_D = {'C300_C IO_RG MS':['Series-C: AO (16) (0-5000)','Series-C: AO (16) HART Config/Status (0-5000)'],'C300_RG_Universal_IO_cont_1':['Series-C: UIO (32) Analog Output (0-5000)'],'SerC_RG_Enhanced_Function_IO_Cont':['Series-C: AO (16) HART (0-5000)']}
        Cont_IO_G = {'C300_RG_Universal_IO_cont_2':['Series-C: UIO (32) Digital Output (0-5000)']}
        IO_G = ['Series-C: DO (32) 24VDC Bus External Power Supply (0-5000)','Series-C: DO (32) 24VDC Bus Internal Power Supply (0-5000)']
        Cont_IO_H = {'C300_RG_Universal_IO_cont_2':['Series-C: UIO (32) Digital Input (0-5000)']}
        IO_H = ['Series-C: DI (32) 24 VDC with Open Wire Detect (0-5000)','Series-C: DI (32) 24VDC SOE (0-5000)']
        for cont,IO_vals in Cont_IO_B.items():
            for row in Product.GetContainerByName(str(cont)).Rows:
                if row['IO_Type'] in IO_vals:
                    for col in col_val:
                        B += int(row[str(col)]) if row[str(col)] != '' else 0
        Trace.Write(B)
        for cont,IO_vals in Cont_IO_D.items():
            for row in Product.GetContainerByName(str(cont)).Rows:
                if row['IO_Type'] in IO_vals:
                    for col in col_val:
                        D += int(row[str(col)]) if row[str(col)] != '' else 0
        Trace.Write(D)
        for cont,IO_vals in Cont_IO_G.items():
            for row in Product.GetContainerByName(str(cont)).Rows:
                if row['IO_Type'] in IO_vals:
                    for col in col_val:
                        G += int(row[str(col)]) if row[str(col)] != '' else 0
        Trace.Write("G1:"+str(G))
        for row in Product.GetContainerByName('SerC_RG_Enhanced_Function_IO_Cont2').Rows:
            if row['IO_Type'] in IO_G:
                G += int(row['Red_IS']) if row['Red_IS'] != '' else 0
        Trace.Write(G)
        for cont,IO_vals in Cont_IO_H.items():
            for row in Product.GetContainerByName(str(cont)).Rows:
                if row['IO_Type'] in IO_vals:
                    for col in col_val:
                        H += int(row[str(col)]) if row[str(col)] != '' else 0
        Trace.Write("H1:"+str(G))
        for row in Product.GetContainerByName('SerC_RG_Enhanced_Function_IO_Cont2').Rows:
            if row['IO_Type'] in IO_H:
                H += int(row['Red_IS']) if row['Red_IS'] != '' else 0
        Trace.Write(H)
        # Percent calcs
        rg_per_B = math.ceil(round(((1+(rg_per/100.0))*B),10))
        rg_per_D = math.ceil(round(((1+(rg_per/100.0))*D),10))
        rg_per_G = math.ceil(round(((1+(rg_per/100.0))*G),10))
        rg_per_H = math.ceil(round(((1+(rg_per/100.0))*H),10))
        return int(rg_per_B),int(rg_per_D),int(rg_per_G),int(rg_per_H)
#CXCPQ-46436
def get_ULLI01(Product):
    if Product.Name == 'Series-C Control Group':
        F=0
        cg_per_F = 0
        cg_per = int(Product.Attr('SerC_CG_Percent_Installed_Spare').GetValue()) if Product.Attr('SerC_CG_Percent_Installed_Spare').GetValue()!='' else 0
        col_val = ['Red_ISLTR','Future_Red_ISLTR','Non_Red_ISLTR']
        IO_val = ['Series-C: UIO (32) Analog Input (LLAI Adapt) (0-5000)']
        # Cont-Col map
        for row in Product.GetContainerByName('C300_CG_Universal_IO_cont_1').Rows:
            if row['IO_Type'] in IO_val:
                for col in col_val:
                    F += int(row[str(col)]) if row[str(col)] != '' else 0
        Trace.Write(F)
        # Percent calcs
        cg_per_F = math.ceil((1+(cg_per/100.0))*F)
        return int(cg_per_F)
    elif Product.Name == 'Series-C Remote Group':
        F=0
        rg_per_F = 0
        rg_per = int(Product.Attr('SerC_RG_Percent_Installed_Spare(0-100%)').GetValue()) if Product.Attr('SerC_RG_Percent_Installed_Spare(0-100%)').GetValue()!='' else 0
        col_val = ['Red_ISLTR','Future_Red_ISLTR','Non_Red_ISLTR']
        IO_val = ['Series-C: UIO (32) Analog Input (LLAI Adapt) (0-5000)']
        # Cont-Col map
        for row in Product.GetContainerByName('C300_RG_Universal_IO_cont_1').Rows:
            if row['IO_Type'] in IO_val:
                for col in col_val:
                    F += int(row[str(col)]) if row[str(col)] != '' else 0
        Trace.Write(F)
        # Percent calcs
        rg_per_F = math.ceil((1+(rg_per/100.0))*F)
        return int(rg_per_F)

#CXCPQ-46802
def get_UDXA01(Product):
    if Product.Name == 'Series-C Control Group':
        H=0
        cg_per_H = 0
        cg_per = int(Product.Attr('SerC_CG_Percent_Installed_Spare').GetValue()) if Product.Attr('SerC_CG_Percent_Installed_Spare').GetValue()!='' else 0
        col_val = ['Red_ISLTR','Future_Red_ISLTR','Non_Red_ISLTR']
        col_val1 = ['Future_Red_IS','Non_Red_IS','Red_ISLTR','Future_Red_ISLTR','Non_Red_ISLTR']
        # Cont-col map
        Cont_IO_H = {'C300_CG_Universal_IO_cont_2':['Series-C: UIO (32) Digital Input (0-5000)','Series-C: UIO (32) Digital Output (0-5000)'],'SerC_CG_Enhanced_Function_IO_Cont2':['Series-C: DI (32) 24 VDC with Open Wire Detect (0-5000)','Series-C: DI (32) 24VDC SOE (0-5000)','Series-C: DO (32) 24VDC Bus External Power Supply (0-5000)','Series-C: DO (32) 24VDC Bus Internal Power Supply (0-5000)']}

        for cont,IO_vals in Cont_IO_H.items():
            if cont != 'SerC_CG_Enhanced_Function_IO_Cont2':
                for row in Product.GetContainerByName(str(cont)).Rows:
                    if row['IO_Type'] in IO_vals:
                        for col in col_val:
                            H += int(row[str(col)]) if row[str(col)] != '' else 0
            else:
                for row in Product.GetContainerByName(str(cont)).Rows:
                    if row['IO_Type'] in IO_vals:
                        for col in col_val1:
                            H += int(row[str(col)]) if row[str(col)] != '' else 0
        Trace.Write(H)
        # Percent calcs
        cg_per_H = math.ceil((1+(cg_per/100.0))*H)
        return int(cg_per_H)
    elif Product.Name == 'Series-C Remote Group':
        H=0
        rg_per_H = 0
        rg_per = int(Product.Attr('SerC_RG_Percent_Installed_Spare(0-100%)').GetValue()) if Product.Attr('SerC_RG_Percent_Installed_Spare(0-100%)').GetValue()!='' else 0
        col_val = ['Red_ISLTR','Future_Red_ISLTR','Non_Red_ISLTR']
        col_val1 = ['Future_Red_IS','Non_Red_IS','Red_ISLTR','Future_Red_ISLTR','Non_Red_ISLTR']
        # Cont-col map
        Cont_IO_H = {'C300_RG_Universal_IO_cont_2':['Series-C: UIO (32) Digital Input (0-5000)','Series-C: UIO (32) Digital Output (0-5000)'],'SerC_RG_Enhanced_Function_IO_Cont2':['Series-C: DI (32) 24 VDC with Open Wire Detect (0-5000)','Series-C: DI (32) 24VDC SOE (0-5000)','Series-C: DO (32) 24VDC Bus External Power Supply (0-5000)','Series-C: DO (32) 24VDC Bus Internal Power Supply (0-5000)']}

        for cont,IO_vals in Cont_IO_H.items():
            if cont != 'SerC_RG_Enhanced_Function_IO_Cont2':
                for row in Product.GetContainerByName(str(cont)).Rows:
                    if row['IO_Type'] in IO_vals:
                        for col in col_val:
                            H += int(row[str(col)]) if row[str(col)] != '' else 0
            else:
                for row in Product.GetContainerByName(str(cont)).Rows:
                    if row['IO_Type'] in IO_vals:
                        for col in col_val1:
                            H += int(row[str(col)]) if row[str(col)] != '' else 0
        Trace.Write(H)
        # Percent calcs
        rg_per_H = math.ceil((1+(rg_per/100.0))*H)
        return int(rg_per_H)