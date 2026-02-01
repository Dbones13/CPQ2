def getpartSYSTEMLABEL(Product):
    x=Product.Attr('C300_RG_UPC_Specify_Id_Modifier').GetValue()
    qnt=Product.Attr('C300_RG_UPC_Cab_Count').GetValue()
    if qnt=="":
        qnt=0
    qnt=int(qnt)
    count=0
    count2=0
    count3=0
    count4=0
    count5=0
    count6=0
    count7=0
    count8=0
    count9=0
    count10=0
    if x=="Yes" and len(Product.Attr('C300_RG_UPC_Id_Modifier').GetValue())>21:
        code=str(Product.Attr('C300_RG_UPC_Id_Modifier').GetValue())
        code=code.replace("-","")
        Trace.Write(code)
        #CXCPQ-45357
        if code[1]=="S"	and code[2]=="B" and code[10]=="N" and code[11]=="2" and code[12]=="0" and code[18]=="A" and code[19]=="R" and code[22]=="Y":
            count=qnt
        elif code[1]=="S"	and code[2]=="B" and code[10]=="N" and code[11]=="2" and code[12]=="2" and code[18]=="A" and code[19]=="R" and code[22]=="Y":
            count=qnt
        elif code[1]=="S"	and code[2]=="B" and code[10]=="N" and code[11]=="2" and code[12]=="4" and code[18]=="A" and code[19]=="R" and code[22]=="Y":
            count=qnt
        elif code[1]=="S"	and code[2]=="B" and code[10]=="N" and code[11]=="2" and code[12]=="6" and code[18]=="A" and code[19]=="R" and code[22]=="Y":
            count=qnt
        elif code[1]=="S"	and code[2]=="B" and code[10]=="N" and code[11]=="4" and code[12]=="0" and code[18]=="A" and code[19]=="R" and code[22]=="Y":
            count=qnt
        elif code[1]=="S"	and code[2]=="B" and code[10]=="N" and code[11]=="4" and code[12]=="2" and code[18]=="A" and code[19]=="R" and code[22]=="Y":
            count=qnt
        elif code[1]=="S"	and code[2]=="B" and code[10]=="N" and code[11]=="4" and code[12]=="4" and code[18]=="A" and code[19]=="R" and code[22]=="Y":
            count=qnt
        elif code[1]=="S"	and code[2]=="B" and code[10]=="N" and code[11]=="4" and code[12]=="6" and code[18]=="A" and code[19]=="R" and code[22]=="Y":
            count=qnt
        elif code[1]=="S"	and code[2]=="B" and code[10]=="N" and code[11]=="6" and code[12]=="0" and code[18]=="A" and code[19]=="R" and code[22]=="Y":
            count=qnt
        elif code[1]=="S"	and code[2]=="B" and code[10]=="N" and code[11]=="6" and code[12]=="2" and code[18]=="A" and code[19]=="R" and code[22]=="Y":
            count=qnt
        elif code[1]=="S"	and code[2]=="B" and code[10]=="N" and code[11]=="6" and code[12]=="4" and code[18]=="A" and code[19]=="R" and code[22]=="Y":
            count=qnt
        elif code[1]=="S"	and code[2]=="B" and code[10]=="N" and code[11]=="6" and code[12]=="6" and code[18]=="A" and code[19]=="R" and code[22]=="Y":
            count=qnt
        
        #XCPQ-45374
        if code[1]=="S"	and code[2]=="A" and code[10]=="N" and code[11]=="2" and code[12]=="0" and code[18]=="D" and code[19]=="R" and code[22]=="Y":
            count4=qnt
        elif code[1]=="S"	and code[2]=="A" and code[10]=="N" and code[11]=="2" and code[12]=="2" and code[18]=="D" and code[19]=="R" and code[22]=="Y":
            count4=qnt
        elif code[1]=="S"	and code[2]=="A" and code[10]=="N" and code[11]=="2" and code[12]=="4" and code[18]=="D" and code[19]=="R" and code[22]=="Y":
            count4=qnt
        elif code[1]=="S"	and code[2]=="A" and code[10]=="N" and code[11]=="2" and code[12]=="6" and code[18]=="D" and code[19]=="R" and code[22]=="Y":
            count4=qnt
        elif code[1]=="S"	and code[2]=="A" and code[10]=="N" and code[11]=="4" and code[12]=="0" and code[18]=="D" and code[19]=="R" and code[22]=="Y":
            count4=qnt
        elif code[1]=="S"	and code[2]=="A" and code[10]=="N" and code[11]=="4" and code[12]=="2" and code[18]=="D" and code[19]=="R" and code[22]=="Y":
            count4=qnt
        elif code[1]=="S"	and code[2]=="A" and code[10]=="N" and code[11]=="4" and code[12]=="4" and code[18]=="D" and code[19]=="R" and code[22]=="Y":
            count4=qnt
        elif code[1]=="S"	and code[2]=="A" and code[10]=="N" and code[11]=="4" and code[12]=="6" and code[18]=="D" and code[19]=="R" and code[22]=="Y":
            count4=qnt
        elif code[1]=="S"	and code[2]=="A" and code[10]=="N" and code[11]=="6" and code[12]=="0" and code[18]=="D" and code[19]=="R" and code[22]=="Y":
            count4=qnt
        elif code[1]=="S"	and code[2]=="A" and code[10]=="N" and code[11]=="6" and code[12]=="2" and code[18]=="D" and code[19]=="R" and code[22]=="Y":
            count4=qnt
        elif code[1]=="S"	and code[2]=="A" and code[10]=="N" and code[11]=="6" and code[12]=="4" and code[18]=="D" and code[19]=="R" and code[22]=="Y":
            count4=qnt
        elif code[1]=="S"	and code[2]=="A" and code[10]=="N" and code[11]=="6" and code[12]=="6" and code[18]=="D" and code[19]=="R" and code[22]=="Y":
            count4=qnt

        #CXCPQ-45323
        if code[1]=="S"	and code[2]=="A" and code[10]=="N" and code[11]=="2" and code[12]=="0" and code[18]=="Q" and code[19]=="R" and code[22]=="N" :
            count6=qnt
        elif code[1]=="S"	and code[2]=="A" and code[10]=="N" and code[11]=="2" and code[12]=="2" and code[18]=="Q" and code[19]=="R" and code[22]=="N":
            count6=qnt
        elif code[1]=="S"	and code[2]=="A" and code[10]=="N" and code[11]=="2" and code[12]=="4" and code[18]=="Q" and code[19]=="R" and code[22]=="N":
            count6=qnt
        elif code[1]=="S"	and code[2]=="A" and code[10]=="N" and code[11]=="2" and code[12]=="6" and code[18]=="Q" and code[19]=="R" and code[22]=="N":
            count6=qnt
        elif code[1]=="S"	and code[2]=="A" and code[10]=="N" and code[11]=="4" and code[12]=="0" and code[18]=="Q" and code[19]=="R" and code[22]=="N":
            count6=qnt
        elif code[1]=="S"	and code[2]=="A" and code[10]=="N" and code[11]=="4" and code[12]=="2" and code[18]=="Q" and code[19]=="R" and code[22]=="N":
            count6=qnt
        elif code[1]=="S"	and code[2]=="A" and code[10]=="N" and code[11]=="4" and code[12]=="4" and code[18]=="Q" and code[19]=="R" and code[22]=="N":
            count6=qnt
        elif code[1]=="S"	and code[2]=="A" and code[10]=="N" and code[11]=="4" and code[12]=="6" and code[18]=="Q" and code[19]=="R" and code[22]=="N":
            count6=qnt
        elif code[1]=="S"	and code[2]=="A" and code[10]=="N" and code[11]=="6" and code[12]=="0" and code[18]=="Q" and code[19]=="R" and code[22]=="N":
            count6=qnt
        elif code[1]=="S"	and code[2]=="A" and code[10]=="N" and code[11]=="6" and code[12]=="2" and code[18]=="Q" and code[19]=="R" and code[22]=="N":
            count6=qnt
        elif code[1]=="S"	and code[2]=="A" and code[10]=="N" and code[11]=="6" and code[12]=="4" and code[18]=="Q" and code[19]=="R" and code[22]=="N":
            count6=qnt
        elif code[1]=="S"	and code[2]=="A" and code[10]=="N" and code[11]=="6" and code[12]=="6" and code[18]=="Q" and code[19]=="R" and code[22]=="N":
            count6=qnt

        #CXCPQ-45014
        if code[3]=="M":
            count8=2*qnt
        elif code[3]=="T":
            count8=2*qnt
        elif code[3]=="A"	and code[6]=="Y" and code[7]=="Y" and code[8]=="B":
            count8=2*qnt
        elif code[3]=="B"	and code[6]=="Y" and code[7]=="Y" and code[8]=="B":
            count8=2*qnt
        elif code[3]=="A"	and code[6]=="Y" and code[7]=="N" and code[8]=="B":
            count8=2*qnt
        elif code[3]=="B"	and code[6]=="Y" and code[7]=="N" and code[8]=="B":
            count8=2*qnt

        #CXCPQ-45052
        if code[10]=="N" and code[11]=="2" and code[12]=="0" and code[14]=="3":
            count10=qnt
        elif code[10]=="N" and code[11]=="2" and code[12]=="0" and code[14]=="6":
            count10=qnt
        elif code[10]=="N" and code[11]=="2" and code[12]=="0" and code[14]=="9":
            count10=qnt
        elif code[10]=="N" and code[11]=="4" and code[12]=="0" and code[14]=="3":
            count10=qnt
        elif code[10]=="N" and code[11]=="4" and code[12]=="0" and code[14]=="6":
            count10=qnt
        elif code[10]=="N" and code[11]=="4" and code[12]=="0" and code[14]=="9":
            count10=qnt
        elif code[10]=="N" and code[11]=="6" and code[12]=="0" and code[14]=="3":
            count10=qnt
        elif code[10]=="N" and code[11]=="6" and code[12]=="0" and code[14]=="6":
            count10=qnt
        elif code[10]=="N" and code[11]=="6" and code[12]=="0" and code[14]=="9":
            count10=qnt

        #CXCPQ-45807
        if code[2]=="B":
            count9=qnt
        
        #CXCPQ-46098
        if code[4]=="S":
            count5=qnt*2
        elif code[4]=="T":
            count5=qnt*4

        #CXCPQ-45311
        if code[10]=="N" and code[11]=="0" and (code[12]=="0" or code[12]=="2" or code[12]=="4" or code[12]=="6") :
            if code[2]=="A"  and code[18]=="Q" and code[22]=="N":
                count2=qnt
        elif code[10]=="G" and (code[11]=="0" or code[11]=="2" or code[11]=="4" or code[11]=="6"):
            if code[2]=="A"  and code[17]=="Q" and code[21]=="N":
                count2=qnt
        elif code[10]=="X":
            if code[2]=="A"  and code[16]=="Q" and code[20]=="N":
                count2=qnt

        #CXCPQ-45889
        try:
            if code[10]=="N":
                if int(code[16])<9:
                    count3=int(code[16])*qnt
            elif code[10]=="G":
                if int(code[15])<9:
                    count3=int(code[15])*qnt
            elif code[10]=="M" or code[10]=="X":
                if int(code[14])<9:
                    count3=int(code[14])*qnt
            else:
                count3=0
        except:
            count3=0

        #CXCPQ-45334
        if code[10]=="N" and code[11]=="0" and (code[12]=="0" or code[12]=="2" or code[12]=="4" or code[12]=="6"):
            if code[1]=="S"	and code[2]=="A"  and code[18]=="D"  and code[22]=="Y":
                count7=qnt
        elif code[10]=="G" and (code[11]=="0" or code[11]=="2" or code[11]=="4" or code[11]=="6"):
            if code[1]=="S"	and code[2]=="A"  and code[17]=="D"  and code[21]=="Y":
                count7=qnt
        elif code[10]=="X" :
            if code[1]=="S"	and code[2]=="A"  and code[16]=="D"  and code[20]=="Y":
                count7=qnt

        

    elif x=="No":
        #CXCPQ-45357
        Tempr=Product.Attr('C300_RG_UPC_Ambient_Temp_Range').GetValue()
        FTA=Product.Attr('C300_RG_UPC_FTA').GetValue()
        UGIA=Product.Attr('C300_RG_UPC_GIIS_Bases_Universal_Marshalling_Count').GetValue()
        USCA=Product.Attr('C300_RG_UPC_Non_GIIS_Universal_Marshalling_Count').GetValue()
        PST=Product.Attr('C300_RG_UPC_Pwr_Supp_Type').GetValue()
        ABD=Product.Attr('C300_RG_UPC_Abu_Dhabi_Bld_Loc').GetValue()
        LLAI=Product.Attr('C300_RG_UPC_LLAI_Count').GetValue()
        FOX=Product.Attr('C300_RG_UPC_Fiber_Optic_Extender').GetValue()
        CN100=Product.Attr('C300_RG_UPC_CN100_IO_HIVE').GetValue()
        CNM=Product.Attr('C300_RG_UPC_CNM').GetValue()
        CNMexp=Product.Attr('C300_RG_UPC_CNM_Exp_Module').GetValue()
        CNMup=Product.Attr('C300_RG_UPC_CNM_Uplink_SFP_Type').GetValue()
        UIO=Product.Attr("C300_RG_UPC_Universal_IO_Count").GetValue()

        if Tempr== "With Fan, Max Ambient +55°C" and FTA=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and UGIA=="2" and USCA=="0"	and PST=="25A AC/DC ATDI Supply" and ABD=="Yes":
            count=qnt
        elif Tempr== "With Fan, Max Ambient +55°C" and FTA=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and UGIA=="2" and USCA=="2"	and PST=="25A AC/DC ATDI Supply" and ABD=="Yes":
            count=qnt
        elif Tempr== "With Fan, Max Ambient +55°C" and FTA=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and UGIA=="2" and USCA=="4"	and PST=="25A AC/DC ATDI Supply" and ABD=="Yes":
            count=qnt
        elif Tempr== "With Fan, Max Ambient +55°C" and FTA=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and UGIA=="2" and USCA=="6"	and PST=="25A AC/DC ATDI Supply" and ABD=="Yes":
            count=qnt
        elif Tempr== "With Fan, Max Ambient +55°C" and FTA=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and UGIA=="4" and USCA=="0"	and PST=="25A AC/DC ATDI Supply" and ABD=="Yes":
            count=qnt
        elif Tempr== "With Fan, Max Ambient +55°C" and FTA=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and UGIA=="4" and USCA=="2"	and PST=="25A AC/DC ATDI Supply" and ABD=="Yes":
            count=qnt
        elif Tempr== "With Fan, Max Ambient +55°C" and FTA=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and UGIA=="4" and USCA=="4"	and PST=="25A AC/DC ATDI Supply" and ABD=="Yes":
            count=qnt
        elif Tempr== "With Fan, Max Ambient +55°C" and FTA=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and UGIA=="4" and USCA=="6"	and PST=="25A AC/DC ATDI Supply" and ABD=="Yes":
            count=qnt
        elif Tempr== "With Fan, Max Ambient +55°C" and FTA=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and UGIA=="6" and USCA=="0"	and PST=="25A AC/DC ATDI Supply" and ABD=="Yes":
            count=qnt
        elif Tempr== "With Fan, Max Ambient +55°C" and FTA=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and UGIA=="6" and USCA=="2"	and PST=="25A AC/DC ATDI Supply" and ABD=="Yes":
            count=qnt
        elif Tempr== "With Fan, Max Ambient +55°C" and FTA=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and UGIA=="6" and USCA=="4"	and PST=="25A AC/DC ATDI Supply" and ABD=="Yes":
            count=qnt
        elif Tempr== "With Fan, Max Ambient +55°C" and FTA=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and UGIA=="6" and USCA=="6"	and PST=="25A AC/DC ATDI Supply" and ABD=="Yes":
            count=qnt

        #CXCPQ-45374
        if Tempr== "Without Fan, Max Ambient +40°C" and FTA=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and UGIA=="2" and USCA=="0"	and PST=="20A DC/DC QUINT4+ Supply" and ABD=="Yes":
            count4=qnt
        elif Tempr== "Without Fan, Max Ambient +40°C" and FTA=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and UGIA=="2" and USCA=="2"	and PST=="20A DC/DC QUINT4+ Supply" and ABD=="Yes":
            count4=qnt
        elif Tempr== "Without Fan, Max Ambient +40°C" and FTA=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and UGIA=="2" and USCA=="4"	and PST=="20A DC/DC QUINT4+ Supply" and ABD=="Yes":
            count4=qnt
        elif Tempr== "Without Fan, Max Ambient +40°C" and FTA=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and UGIA=="2" and USCA=="6"	and PST=="20A DC/DC QUINT4+ Supply" and ABD=="Yes":
            count4=qnt
        elif Tempr== "Without Fan, Max Ambient +40°C" and FTA=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and UGIA=="4" and USCA=="0"	and PST=="20A DC/DC QUINT4+ Supply" and ABD=="Yes":
            count4=qnt
        elif Tempr== "Without Fan, Max Ambient +40°C" and FTA=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and UGIA=="4" and USCA=="2"	and PST=="20A DC/DC QUINT4+ Supply" and ABD=="Yes":
            count4=qnt
        elif Tempr== "Without Fan, Max Ambient +40°C" and FTA=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and UGIA=="4" and USCA=="4"	and PST=="20A DC/DC QUINT4+ Supply" and ABD=="Yes":
            count4=qnt
        elif Tempr== "Without Fan, Max Ambient +40°C" and FTA=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and UGIA=="4" and USCA=="6"	and PST=="20A DC/DC QUINT4+ Supply" and ABD=="Yes":
            count4=qnt
        elif Tempr== "Without Fan, Max Ambient +40°C" and FTA=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and UGIA=="6" and USCA=="0"	and PST=="20A DC/DC QUINT4+ Supply" and ABD=="Yes":
            count4=qnt
        elif Tempr== "Without Fan, Max Ambient +40°C" and FTA=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and UGIA=="6" and USCA=="2"	and PST=="20A DC/DC QUINT4+ Supply" and ABD=="Yes":
            count4=qnt
        elif Tempr== "Without Fan, Max Ambient +40°C" and FTA=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and UGIA=="6" and USCA=="4"	and PST=="20A DC/DC QUINT4+ Supply" and ABD=="Yes":
            count4=qnt
        elif Tempr== "Without Fan, Max Ambient +40°C" and FTA=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and UGIA=="6" and USCA=="6"	and PST=="20A DC/DC QUINT4+ Supply" and ABD=="Yes":
            count4=qnt

        #CXCPQ-45323
        if Tempr== "Without Fan, Max Ambient +40°C" and FTA=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and UGIA=="2" and USCA=="0"	and PST=="20A AC/DC QUINT4+ Supply" and ABD=="No":
            count6=qnt
        elif Tempr== "Without Fan, Max Ambient +40°C" and FTA=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and UGIA=="2" and USCA=="2"	and PST=="20A AC/DC QUINT4+ Supply" and ABD=="No":
            count6=qnt
        elif Tempr== "Without Fan, Max Ambient +40°C" and FTA=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and UGIA=="2" and USCA=="4"	and PST=="20A AC/DC QUINT4+ Supply" and ABD=="No":
            count6=qnt
        elif Tempr== "Without Fan, Max Ambient +40°C" and FTA=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and UGIA=="2" and USCA=="6"	and PST=="20A AC/DC QUINT4+ Supply" and ABD=="No":
            count6=qnt
        elif Tempr== "Without Fan, Max Ambient +40°C" and FTA=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and UGIA=="4" and USCA=="0"	and PST=="20A AC/DC QUINT4+ Supply" and ABD=="No":
            count6=qnt
        elif Tempr== "Without Fan, Max Ambient +40°C" and FTA=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and UGIA=="4" and USCA=="2"	and PST=="20A AC/DC QUINT4+ Supply" and ABD=="No":
            count6=qnt
        elif Tempr== "Without Fan, Max Ambient +40°C" and FTA=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and UGIA=="4" and USCA=="4"	and PST=="20A AC/DC QUINT4+ Supply" and ABD=="No":
            count6=qnt
        elif Tempr== "Without Fan, Max Ambient +40°C" and FTA=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and UGIA=="4" and USCA=="6"	and PST=="20A AC/DC QUINT4+ Supply" and ABD=="No":
            count6=qnt
        elif Tempr== "Without Fan, Max Ambient +40°C" and FTA=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and UGIA=="6" and USCA=="0"	and PST=="20A AC/DC QUINT4+ Supply" and ABD=="No":
            count6=qnt
        elif Tempr== "Without Fan, Max Ambient +40°C" and FTA=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and UGIA=="6" and USCA=="2"	and PST=="20A AC/DC QUINT4+ Supply" and ABD=="No":
            count6=qnt
        elif Tempr== "Without Fan, Max Ambient +40°C" and FTA=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and UGIA=="6" and USCA=="4"	and PST=="20A AC/DC QUINT4+ Supply" and ABD=="No":
            count6=qnt
        elif Tempr== "Without Fan, Max Ambient +40°C" and FTA=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and UGIA=="6" and USCA=="6"	and PST=="20A AC/DC QUINT4+ Supply" and ABD=="No":
            count6=qnt

        #CXCPQ-45014
        if CN100=="Non-Redundant with MM SFP":
            count8=2*qnt
        elif CN100=="Redundant with MM SFP":
            count8=2*qnt
        elif CN100=="Non-Redundant"	and CNM=="Red Pair CNM" and CNMexp=="No Expansion Module" and CNMup=="Red Pair CNM with MM 10/100M SFP, 2Km":
            count8=2*qnt
        elif CN100=="Redundant"	and CNM=="Red Pair CNM" and CNMexp=="No Expansion Module" and CNMup=="Red Pair CNM with MM 10/100M SFP, 2Km":
            count8=2*qnt
        elif CN100=="Non-Redundant"	and CNM=="Red Pair CNM" and CNMexp=="2x Expansion Modules" and CNMup=="Red Pair CNM with MM 10/100M SFP, 2Km":
            count8=2*qnt
        elif CN100=="Redundant"	and CNM=="Red Pair CNM" and CNMexp=="2x Expansion Modules" and CNMup=="Red Pair CNM with MM 10/100M SFP, 2Km":
            count8=2*qnt

        #CXCPQ-45052
        if FTA=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and UGIA=="2" and USCA=="0" and UIO=="32":
            count10=qnt
        elif FTA=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and UGIA=="2" and USCA=="0" and UIO=="64":
            count10=qnt
        elif FTA=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and UGIA=="2" and USCA=="0" and UIO=="96":
            count10=qnt
        elif FTA=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and UGIA=="4" and USCA=="0" and UIO=="32":
            count10=qnt
        elif FTA=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and UGIA=="4" and USCA=="0" and UIO=="64":
            count10=qnt
        elif FTA=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and UGIA=="4" and USCA=="0" and UIO=="96":
            count10=qnt
        elif FTA=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and UGIA=="6" and USCA=="0" and UIO=="32":
            count10=qnt
        elif FTA=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and UGIA=="6" and USCA=="0" and UIO=="64":
            count10=qnt
        elif FTA=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and UGIA=="6" and USCA=="0" and UIO=="96":
            count10=qnt 

        #CXCPQ-46098
        if FOX== "Single Mode x2":
            count5=qnt*2
        elif FOX== "Single Mode x4":
            count5=qnt*4

        #CXCPQ-45311
        if Tempr== "Without Fan, Max Ambient +40°C" and ((FTA=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and UGIA=="0") or FTA=="Universal Marshalling, GI only (0-6)" or FTA=="No Treatment") and PST=="20A AC/DC QUINT4+ Supply" and ABD=="No":
            count2=qnt
        
        #CXCPQ-45889
        count3=int(LLAI)*qnt

        #CXCPQ-45334
        if Tempr== "Without Fan, Max Ambient +40°C" and ((FTA=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and UGIA=="0") or FTA=="Universal Marshalling, GI only (0-6)" or FTA=="No Treatment") and PST=="20A DC/DC QUINT4+ Supply" and ABD=="Yes":
            count7=qnt

        #CXCPQ-45807
        if Tempr== "With Fan, Max Ambient +55°C":
            count9=qnt
    
    return int(count),int(count2),int(count3),int(count4),int(count5),int(count6),int(count7),int(count8),int(count9),int(count10)

#a=getpartSYSTEMLABEL(Product)
#Trace.Write(a)