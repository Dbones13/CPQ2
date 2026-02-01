import System.Decimal as D
#CXCPQ-42026 ,CXCPQ-42028 , CXCPQ-42032
def part_qty_CNM(Product, pcntQty, qty):
    CC_INWM01=CC_TNWC01=CC_INWE01=INWM_INWE=0
    if Product.Name == "Series-C Control Group":
        CC_PCF901=qty
        CC_PCNT05=pcntQty
        family_type = Product.Attributes.GetByName("SerC_CG_IO_Family_Type").GetValue()
        Cab_Type = Product.Attributes.GetByName("SerC_CG_Type_of_Controller_Required").GetValue() #CXCPQ-52389
        Network_Mod = Product.Attributes.GetByName("SerC_CG_Control_Networking_Module_Required").GetValue()
        Controller_Mod = Product.Attributes.GetByName("SerC_CG_C300_Controller_Module_Type").GetValue()
        #Controller_Type = Product.Attributes.GetByName("SerC_CG_Controller_Type").GetValue()
        if family_type != 'Series C' and Cab_Type != 'C300 CEE' and Network_Mod != 'Yes' and Controller_Mod != 'C300(PCNT05)':
            return 0, 0, 0, 0

        CF = CC = NM =0
        X = Y = YY = g =0
        CF = int(D.Ceiling(CC_PCF901/2.0))
        Trace.Write('CF = '+str(CF))
        CC = int(CC_PCNT05)
        '''if Controller_Type == 'Redundant':
            CC = 2 * int(CC_PCNT05)
        elif Controller_Type == 'Non Redundant':
            CC = int(CC_PCNT05)'''
        Trace.Write('CC = '+str(CC))
        NM = (CF+CC)/12.0
        Trace.Write('NM = '+str(NM))
        X = int(NM)
        Trace.Write('X = '+str(X))

        if NM<1 and NM>0.4:
            YY= 1
        if NM>0 and NM<1:
            Y= 1
        if NM>1:
            g=NM%int(NM)
            Trace.Write(g)
            if g>0 :
                Y= 1
            if g>0.4 and g<1:
                YY= 1
                Trace.Write("Y : "+str(Y))
                Trace.Write("YY : "+str(YY))

        if family_type == 'Series C' and Cab_Type == 'C300 CEE' and Network_Mod == 'Yes' and Controller_Mod == 'C300(PCNT05)':
            CC_INWM01 = 2 * (X + Y)    #CXCPQ-42026
            CC_TNWC01 = int(CC_INWM01)    #CXCPQ-42026
            CC_INWE01 = 2 * (X + YY)    #CXCPQ-42028
            INWM_INWE = CC_INWM01 - CC_INWE01   #CXCPQ-42032
        return int(CC_INWM01),int(CC_TNWC01),int(CC_INWE01),int(INWM_INWE)
#FinalQty = part_qty_CNM(Product,pcntQty,qty)
#Trace.Write('FinalQty' + str(FinalQty))

#CXCPQ-44627 ,CXCPQ-44628 , CXCPQ-44630
#Tion13=float(TagParserProduct.ParseString('<* GetAtvQty(Series_C_RG_Part_Summary:CC-TION13) *>'))
#Tion11=float(TagParserProduct.ParseString('<* GetAtvQty(Series_C_RG_Part_Summary:CC-TION11) *>'))
#CNM44627_qty=float(TagParserProduct.ParseString('<* GetAtvQty(Series_C_RG_Part_Summary:CC-INWE01) *>'))
#CNM44630_qty=float(TagParserProduct.ParseString('<* GetAtvQty(Series_C_RG_Part_Summary:CC-INWE01) *>'))
def part_qty_RG_CNM(Product,Tion13_446,Tion11_446):
    CC_INWM01=CC_TNWC01=CC_INWE01=INWM_INWE=0
    if Product.Name == "Series-C Remote Group":
        Trace.Write('Tion13_446 = '+str(Tion13_446))
        Trace.Write('Tion11_446 = '+str(Tion11_446))
        CN100=int(Tion11_446)+int(Tion13_446)
        family_type = Product.Attributes.GetByName("SerC_CG_IO_Family_Type").GetValue()
        Network_Mod = Product.Attributes.GetByName("SerC_CG_Control_Networking_Module_Required").GetValue()
        Controller_Mod = Product.Attributes.GetByName("SerC_CG_C300_Controller_Module_Type").GetValue()
        Cab_Type = Product.Attributes.GetByName("SerC_CG_Type_of_Controller_Required").GetValue()#CXCPQ-52331
        IO_Mount = Product.Attributes.GetByName("SerC_IO_Mounting_Solution").GetValue()#CXCPQ-52331
        if family_type != 'Series C' and Network_Mod != 'Yes' and Cab_Type != 'C300 CEE' and Controller_Mod != 'C300(PCNT05)' and (IO_Mount != 'Cabinet' or IO_Mount != 'Mounting Panel'):
            return 0, 0, 0, 0

        CN =0
        X = Y = YY = g = 0
        CN = int(D.Ceiling(CN100))
        Trace.Write('CN = '+str(CN))
        NM = (CN)/12.0
        Trace.Write('NM = '+str(NM))
        X = int(NM)
        Trace.Write('X = '+str(X))

        if NM<1 and NM>0.4:
            YY= 1
            Trace.Write("YY : "+str(YY))
        if NM !=X:
            Y= 1
        if NM>1:
            g=NM%int(NM)
            Trace.Write(g)
            if g>0 :
                Y= 1
            if g>0.4 and g<1:
                YY= 1
                Trace.Write("Y : "+str(Y))
                Trace.Write("YY : "+str(YY))
        if family_type == 'Series C' and Network_Mod == 'Yes' and Cab_Type == 'C300 CEE' and Controller_Mod == 'C300(PCNT05)' and (IO_Mount == 'Cabinet' or IO_Mount == 'Mounting Panel'):
            CC_INWM01 = 2 * (X + Y)    #CXCPQ-44627
            CC_TNWC01 = int(CC_INWM01)    #CXCPQ-44627
            CC_INWE01 = 2 * (X + YY)    #CXCPQ-44628
            INWM_INWE = CC_INWM01 - CC_INWE01   #CXCPQ-44630
            Trace.Write('# family_type:'+str(family_type))
            Trace.Write('# Network_Mod:'+str(Network_Mod))
            Trace.Write('# Controller_Mod:'+str(Controller_Mod))
        return int(CC_INWM01),int(CC_TNWC01),int(CC_INWE01),int(INWM_INWE)
#A,B,C,D = part_qty_RG_CNM(Product,Tion13_446,Tion11_446)
#Trace.Write('A :'+str(A))
#Trace.Write('B :'+str(B))
#Trace.Write('C :'+str(C))
#Trace.Write('D :'+str(D))

#CXCPQ-52390
#Tion11=float(TagParserProduct.ParseString('<* GetAtvQty(Series_C_CG_Part_Summary:CC-TION11) *>'))
def CG_CNM52390(Product,Tion11):
    CC_INWM01=CC_TNWC01=CC_INWE01=INWM_INWE=0
    if Product.Name == "Series-C Control Group":
        CC_TION11=Tion11
        family_type = Product.Attributes.GetByName("SerC_CG_IO_Family_Type").GetValue()
        Cab_Type = Product.Attributes.GetByName("SerC_CG_Type_of_Controller_Required").GetValue()
        Network_Mod = Product.Attributes.GetByName("SerC_CG_Control_Networking_Module_Required").GetValue()
        Trace.Write('# family_type:'+str(family_type))
        Trace.Write('# Cab_Type:'+str(Cab_Type))
        Trace.Write('# Network_Mod:'+str(Network_Mod))
        
        if family_type != 'Series C' and Cab_Type != 'CN100 CEE' and Network_Mod != 'Yes':
            return 0, 0, 0, 0

        NM=X = Y = YY = g =0
        NM = int(CC_TION11)/12.0
        Trace.Write('NM = '+str(NM))
        X = int(NM)
        Trace.Write('X = '+str(X))

        if NM<1 and NM>0.4:
            YY= 1
            Trace.Write("YY : "+str(YY))
        if NM>0 and NM<1:
            Y= 1
            Trace.Write("Y : "+str(Y))
        if NM>1:
            g=NM%int(NM)
            Trace.Write('g :'+str(g))
            if g>0 :
                Y= 1
                Trace.Write("Y : "+str(Y))
            if g>0.4 and g<1:
                YY= 1
                Trace.Write("Y : "+str(Y))
                Trace.Write("YY : "+str(YY))

        if family_type == 'Series C' and Cab_Type == 'CN100 CEE' and Network_Mod == 'Yes':
            CC_INWM01 = 2 * (X + Y)
            CC_TNWC01 = int(CC_INWM01)
            CC_INWE01 = 2 * (X + YY)
            INWM_INWE = CC_INWM01 - CC_INWE01
        return int(CC_INWM01),int(CC_TNWC01),int(CC_INWE01),int(INWM_INWE)
#FinalQty = CG_CNM52390(Product,Tion11)
#Trace.Write('FinalQty' + str(FinalQty))

#CXCPQ-52419
#pcntQty=float(TagParserProduct.ParseString('<* GetAtvQty(Series_C_CG_Part_Summary:CC-PCNT05) *>'))
#Tion11=float(TagParserProduct.ParseString('<* GetAtvQty(Series_C_CG_Part_Summary:CC-TION11) *>'))
def CG_CNM52419(Product, pcntQty, Tion11):
    CC_INWM01=CC_TNWC01=CC_INWE01=INWM_INWE=0
    if Product.Name == "Series-C Control Group":
        CC_PCNT05=pcntQty
        CN=Tion11
        family_type = Product.Attributes.GetByName("SerC_CG_IO_Family_Type").GetValue()
        Cab_Type = Product.Attributes.GetByName("SerC_CG_Type_of_Controller_Required").GetValue()
        Network_Mod = Product.Attributes.GetByName("SerC_CG_Control_Networking_Module_Required").GetValue()
        Controller_Mod = Product.Attributes.GetByName("SerC_CG_C300_Controller_Module_Type").GetValue()
        Controller_Type = Product.Attributes.GetByName("SerC_CG_Controller_Type").GetValue()
        if family_type != 'Series C' and (Cab_Type != 'Control HIVE - Physical' or Cab_Type != 'Control HIVE - Virtual') and Network_Mod != 'Yes':
            return 0, 0, 0, 0

        CC = NM =0
        X = Y = YY = g =0
        CC = int(CC_PCNT05)
        Trace.Write('CC = '+str(CC))
        NM = (CN+CC)/12.0
        Trace.Write('NM = '+str(NM))
        X = int(NM)
        Trace.Write('X = '+str(X))

        if NM<1 and NM>0.4:
            YY= 1
        if NM>0 and NM<1:
            Y= 1
        if NM>1:
            g=NM%int(NM)
            Trace.Write(g)
            if g>0 :
                Y= 1
            if g>0.4 and g<1:
                YY= 1
                Trace.Write("Y : "+str(Y))
                Trace.Write("YY : "+str(YY))

        if family_type == 'Series C' and (Cab_Type == 'Control HIVE - Physical' or Cab_Type == 'Control HIVE - Virtual') and Network_Mod == 'Yes':
            CC_INWM01 = 2 * (X + Y)
            CC_TNWC01 = int(CC_INWM01)
            CC_INWE01 = 2 * (X + YY)
            INWM_INWE = CC_INWM01 - CC_INWE01
        return int(CC_INWM01),int(CC_TNWC01),int(CC_INWE01),int(INWM_INWE)
#FinalQty = CG_CNM52419(Product, pcntQty, qty)
#Trace.Write('FinalQty' + str(FinalQty))

#CXCPQ-52402
#pcntQty=float(TagParserProduct.ParseString('<* GetAtvQty(Series_C_CG_Part_Summary:CC-PCNT05) *>'))
#qty=float(TagParserProduct.ParseString('<* GetAtvQty(Series_C_CG_Part_Summary:CC-PCF901) *>'))
#Tion11=float(TagParserProduct.ParseString('<* GetAtvQty(Series_C_CG_Part_Summary:CC-TION11) *>'))
def CG_CNM52402(Product, pcntQty, qty,Tion11):
    CC_INWM01=CC_TNWC01=CC_INWE01=INWM_INWE=0
    if Product.Name == "Series-C Control Group":
        CC_PCF901=qty
        CC_PCNT05=pcntQty
        CN=Tion11
        family_type = Product.Attributes.GetByName("SerC_CG_IO_Family_Type").GetValue()
        Cab_Type = Product.Attributes.GetByName("SerC_CG_Type_of_Controller_Required").GetValue()
        Network_Mod = Product.Attributes.GetByName("SerC_CG_Control_Networking_Module_Required").GetValue()
        Controller_Mod = Product.Attributes.GetByName("SerC_CG_C300_Controller_Module_Type").GetValue()
        #Controller_Type = Product.Attributes.GetByName("SerC_CG_Controller_Type").GetValue()
        if family_type != 'Series C' and Cab_Type != 'CN100 I/O HIVE - C300 CEE' and Network_Mod != 'Yes':
            return 0, 0, 0, 0

        CF=CC=NM=0
        X = Y = YY = g =0
        CF = int(D.Ceiling(CC_PCF901/2.0))
        Trace.Write('CF = '+str(CF))
        Trace.Write('CN = '+str(CN))
        CC = int(CC_PCNT05)
        '''if Controller_Type == 'Redundant':
            CC = 2 * int(CC_PCNT05)
        elif Controller_Type == 'Non Redundant':
            CC = int(CC_PCNT05)'''
        Trace.Write('CC = '+str(CC))
        NM = (CF+CC+CN)/12.0
        Trace.Write('NM = '+str(NM))
        X = int(NM)
        Trace.Write('X = '+str(X))

        if NM<1 and NM>0.4:
            YY= 1
        if NM>0 and NM<1:
            Y= 1
        if NM>1:
            g=NM%int(NM)
            Trace.Write(g)
            if g>0 :
                Y= 1
            if g>0.4 and g<1:
                YY= 1
                Trace.Write("Y : "+str(Y))
                Trace.Write("YY : "+str(YY))

        if family_type == 'Series C' and Cab_Type == 'CN100 I/O HIVE - C300 CEE' and Network_Mod == 'Yes':
            CC_INWM01 = 2 * (X + Y)
            CC_TNWC01 = int(CC_INWM01)
            CC_INWE01 = 2 * (X + YY)
            INWM_INWE = CC_INWM01 - CC_INWE01
        return int(CC_INWM01),int(CC_TNWC01),int(CC_INWE01),int(INWM_INWE)
#FinalQty = CG_CNM52402(Product, pcntQty, qty,Tion11)
#Trace.Write('FinalQty' + str(FinalQty))

#CXCPQ-52403
#Tion11=float(TagParserProduct.ParseString('<* GetAtvQty(Series_C_RG_Part_Summary:CC-TION11) *>'))
def RG_CNM52403(Product,Tion11):
    CC_INWM01=CC_TNWC01=CC_INWE01=INWM_INWE=0
    if Product.Name == "Series-C Remote Group":
        CC_TION11=Tion11
        family_type = Product.Attributes.GetByName("SerC_CG_IO_Family_Type").GetValue()
        Cab_Type = Product.Attributes.GetByName("SerC_CG_Type_of_Controller_Required").GetValue()
        Network_Mod = Product.Attributes.GetByName("SerC_CG_Control_Networking_Module_Required").GetValue()
        Controller_Mod = Product.Attributes.GetByName("SerC_CG_C300_Controller_Module_Type").GetValue()
        IO_Hive = Product.Attributes.GetByName("SerC_CG_CN100_IO_HIVE_Redundancy").GetValue()
        IO_Mount = Product.Attributes.GetByName("SerC_IO_Mounting_Solution").GetValue()#CXCPQ-52331
        if family_type != 'Series C' and Cab_Type != 'CN100 I/O HIVE - C300 CEE' and Controller_Mod != 'C300(PCNT05)' and (IO_Hive!='Redundant' or IO_Hive!='Non Redundant') and Network_Mod!='Yes' and (IO_Mount != 'Cabinet' or IO_Mount != 'Mounting Panel'):
            return 0, 0, 0, 0

        NM=X = Y = YY = g =0
        NM = int(CC_TION11)/12.0
        Trace.Write('NM = '+str(NM))
        X = int(NM)
        Trace.Write('X = '+str(X))

        if NM<1 and NM>0.4:
            YY= 1
        if NM>0 and NM<1:
            Y= 1
        if NM>1:
            g=NM%int(NM)
            Trace.Write(g)
            if g>0 :
                Y= 1
            if g>0.4 and g<1:
                YY= 1
                Trace.Write("Y : "+str(Y))
                Trace.Write("YY : "+str(YY))

        if family_type == 'Series C' and Cab_Type == 'CN100 I/O HIVE - C300 CEE' and Controller_Mod == 'C300(PCNT05)' and (IO_Hive=='Redundant' or IO_Hive=='Non Redundant') and Network_Mod=='Yes' and (IO_Mount == 'Cabinet' or IO_Mount == 'Mounting Panel'):
            CC_INWM01 = 2 * (X + Y)
            CC_TNWC01 = int(CC_INWM01)
            CC_INWE01 = 2 * (X + YY)
            INWM_INWE = CC_INWM01 - CC_INWE01
        return int(CC_INWM01),int(CC_TNWC01),int(CC_INWE01),int(INWM_INWE)
#FinalQty = RG_CNM52403(Product,Tion11)
#Trace.Write('FinalQty = ' + str(FinalQty))

#CXCPQ-52426
#Tion11=float(TagParserProduct.ParseString('<* GetAtvQty(Series_C_RG_Part_Summary:CC-TION11) *>'))
def RG_CNM52426(Product,Tion11):
    CC_INWM01=CC_TNWC01=CC_INWE01=INWM_INWE=0
    if Product.Name == "Series-C Remote Group":
        CN=Tion11
        family_type = Product.Attributes.GetByName("SerC_CG_IO_Family_Type").GetValue()
        Network_Mod = Product.Attributes.GetByName("SerC_CG_Control_Networking_Module_Required").GetValue()
        Controller_Mod = Product.Attributes.GetByName("SerC_CG_C300_Controller_Module_Type").GetValue()
        Cab_Type = Product.Attributes.GetByName("SerC_CG_Type_of_Controller_Required").GetValue()
        IO_Mount = Product.Attributes.GetByName("SerC_IO_Mounting_Solution").GetValue()#CXCPQ-52331
        if family_type != 'Series C' and (Cab_Type != 'Control HIVE - Physical' or Cab_Type != 'Control HIVE - Virtual') and Network_Mod != 'Yes' and (IO_Mount != 'Cabinet' or IO_Mount != 'Mounting Panel'):
            return 0, 0, 0, 0

        X = Y = YY = g = 0
        #CN=int(CN100)
        Trace.Write('CN = '+str(CN))
        NM = int(CN)/12.0
        Trace.Write('NM = '+str(NM))
        X = int(NM)
        Trace.Write('X = '+str(X))

        if NM<1 and NM>0.4:
            YY= 1
        if NM !=X:
            Y= 1
            #Trace.Write("Y : "+str(Y))
        if NM>1:
            g=NM%int(NM)
            Trace.Write(g)
            if g>0 :
                Y= 1
            if g>0.4 and g<1:
                YY= 1
                Trace.Write("Y : "+str(Y))
                Trace.Write("YY : "+str(YY))
        if family_type == 'Series C' and (Cab_Type == 'Control HIVE - Physical' or Cab_Type == 'Control HIVE - Virtual') and Network_Mod== 'Yes' and (IO_Mount == 'Cabinet' or IO_Mount == 'Mounting Panel'):
            CC_INWM01 = 2 * (X + Y)
            CC_TNWC01 = int(CC_INWM01)
            CC_INWE01 = 2 * (X + YY)
            INWM_INWE = CC_INWM01 - CC_INWE01
        return int(CC_INWM01),int(CC_TNWC01),int(CC_INWE01),int(INWM_INWE)
#FinalQty = RG_CNM52426(Product,Tion11)
#Trace.Write('FinalQty' + str(FinalQty))