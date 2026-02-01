def getfloat(val):
	if val:
		try:
			return float(val)
		except:
			return 0
	return 0

def getprojectsize(Product):
    ProjectSize=""
    SERRadd=0
    ANTMDadd=0
    ANRMCadd=0
    ATNTMDadd=0
    ATNRMCadd=0
    EAPPTadd=0
    EAPPRadd=0
    MNSadd=0
    ADDseradd=0
    FTE=0
    ser=0

    FSQOadd=0
    FSQDadd=0
    FSQCadd=0
    CSQOadd=0
    CSQCadd=0
    CSQDadd=0
    CSEQOadd=0
    CSEQCadd=0
    CSEQDadd=0
    TPSOadd=0
    TPSCadd=0
    TPSDadd=0
    Addsadd=0
    stn=0
    NLCadd=0
    BSRadd=0
    swt=0


    for row in Product.GetContainerByName("Experion_Enterprise_Cont").Rows:
        y=row.Product

        try:
            SERRav=y.Attributes.GetByName('Server Redundancy Requirement?').SelectedValue.Display
            if SERRav=="Non Redundant":
                SERR="1"
            elif SERRav=="Redundant":
                SERR="2"
        except:
            SERR="0"
        SERRadd=SERRadd+int(SERR)

        try:
            ANTMD=y.Attributes.GetByName('ACE Node Tower Mount Desk').GetValue()
        except:
            ANTMD="0"
        ANTMDadd=ANTMDadd+int(ANTMD)

        try:
            ANRMC=y.Attributes.GetByName('ACE Node Rack Mount Cabinet').GetValue()
        except:
            ANRMC="0"
        ANRMCadd=ANRMCadd+int(ANRMC)

        try:
            ATNTMD=y.Attributes.GetByName('ACE_T_Node _Tower_Mount_Desk').GetValue()
            if ATNTMD=="":
                ATNTMD=0
        except:
            ATNTMD="0"
        ATNTMDadd=ATNTMDadd+int(ATNTMD)

        try:
            ATNRMC=y.Attributes.GetByName('ACE_T_Node _Rack_Mount_Cabinet').GetValue()
            if ATNRMC=="":
                ATNRMC=0
        except:
            ATNRMC="0"
        ATNRMCadd=ATNRMCadd+int(ATNRMC)

        try:
            EAPPT=y.Attributes.GetByName('Experion APP Node - Tower Mount').GetValue()
            if EAPPT=="":
                EAPPT=0
        except:
            EAPPT="0"
        EAPPTadd=EAPPTadd+int(EAPPT)

        try:
            EAPPR=y.Attributes.GetByName('Experion APP Node - Rack Mount').GetValue()
            if EAPPR=="":
                EAPPR=0
        except:
            EAPPR="0"
        EAPPRadd=EAPPRadd+int(EAPPR)

        try:
            MNS=y.Attributes.GetByName('Mobile Server Nodes (0-1)').GetValue()
            if MNS=="":
                MNS=0
        except:
            MNS="0"
        MNSadd=MNSadd+int(MNS)

        try:
            ADDser=y.Attributes.GetByName('Additional Servers').GetValue()
            if ADDser=="":
                ADDser=0
        except:
            ADDser="0"
        ADDseradd=ADDseradd+int(ADDser)



        #Flex Station Qty (0-60)
        try:
            FSQO=y.Attributes.GetByName('Flex Station Qty (0-60)').GetValue()
            if FSQO=="":
                FSQO=0
        except:
            FSQO="0"
        FSQOadd=FSQOadd+int(FSQO)

        try:
            FSQD=y.Attributes.GetByName('DMS Flex Station Qty 0_60').GetValue()
            if FSQD=="":
                FSQD=0
        except:
            FSQD="0"
        FSQDadd=FSQDadd+int(FSQD)

        try:
            FSQC=y.Attributes.GetByName('CMS Flex Station Qty 0_60').GetValue()
            if FSQC=="":
                FSQC=0
        except:
            FSQC="0"
        FSQCadd=FSQCadd+int(FSQC)

        #Console Station Qty (0-20)
        try:
            CSQO=y.Attributes.GetByName('Console Station Qty (0-20)').GetValue()
            if CSQO=="":
                CSQO=0
        except:
            CSQO="0"
        CSQOadd=CSQOadd+int(CSQO)

        try:
            CSQC=y.Attributes.GetByName('CMS Console Station Qty 0_20').GetValue()
            if CSQC=="":
                CSQC=0
        except:
            CSQC="0"
        CSQCadd=CSQCadd+int(CSQC)

        try:
            CSQD=y.Attributes.GetByName('DMS Console Station Qty 0_20').GetValue()
            if CSQD=="":
                CSQD=0
        except:
            CSQD="0"
        CSQDadd=CSQDadd+int(CSQD)

        #Console Station Extension Qty  (0-15)
        try:
            CSEQO=y.Attributes.GetByName('Console Station Extension Qty  (0-15)').GetValue()
            if CSEQO=="":
                CSEQO=0
        except:
            CSEQO="0"
        CSEQOadd=CSEQOadd+int(CSEQO)

        try:
            CSEQD=y.Attributes.GetByName('DMS Console Station Extension Qty 0_15').GetValue()
            if CSEQD=="":
                CSEQD=0
        except:
            CSEQD="0"
        CSEQDadd=CSEQDadd+int(CSEQD)

        try:
            CSEQC=y.Attributes.GetByName('CMS Console Station Extension Qty 0_15').GetValue()
            if CSEQC=="":
                CSEQC=0
        except:
            CSEQC="0"
        CSEQCadd=CSEQCadd+int(CSEQC)

        #TPS Station Qty (0-20)
        try:
            TPSO=y.Attributes.GetByName('TPS Station Qty (0-20)').GetValue()
            if TPSO=="":
                TPSO=0
        except:
            TPSO="0"
        TPSOadd=TPSOadd+int(TPSO)

        try:
            TPSC=y.Attributes.GetByName('CMS TPS Station Qty 0_20').GetValue()
            if TPSC=="":
                TPSC=0
        except:
            TPSC="0"
        TPSCadd=TPSCadd+int(TPSC)

        try:
            TPSD=y.Attributes.GetByName('DMS TPS Station Qty 0_20').GetValue()
            if TPSD=="":
                TPSD=0
        except:
            TPSD="0"
        TPSDadd=TPSDadd+int(TPSD)

        #Additional Stations
        try:
            Adds=y.Attributes.GetByName('Additional Stations').GetValue()
            if Adds=="":
                Adds=0
        except:
            Adds="0"
        Addsadd=Addsadd+int(Adds)

        #number of location cluster
        NLC=y.GetContainerByName("List of Locations/Clusters/Network Groups").Rows.Count
        NLC=int(NLC)*2
        NLCadd=(NLCadd+NLC)

        #Backbone Switch Required
        BSR=y.Attributes.GetByName("Backbone Switch Required").SelectedValue.Display
        if BSR=="Yes":
            BSRadd=BSRadd+2
        elif BSR=="No":
            BSRadd=BSRadd+0

    '''Trace.Write("A: "+str(SERRadd))
    Trace.Write("B: "+str(ANTMDadd))
    Trace.Write("C: "+str(ANRMCadd))
    Trace.Write("D: "+str(ATNTMDadd))
    Trace.Write("E: "+str(ATNRMCadd))
    Trace.Write("F: "+str(EAPPTadd))
    Trace.Write("G: "+str(EAPPRadd))
    Trace.Write("H: "+str(MNSadd))
    Trace.Write("I: "+str(ADDseradd))

    Trace.Write("------------------------------------------")

    Trace.Write("j1: "+str(CSQOadd))
    Trace.Write("j2: "+str(CSQDadd))
    Trace.Write("j3: "+str(CSQCadd))

    Trace.Write("k1: "+str(CSEQOadd))
    Trace.Write("k2: "+str(CSEQDadd))
    Trace.Write("k3: "+str(CSEQCadd))

    Trace.Write("L1: "+str(FSQOadd))
    Trace.Write("L2: "+str(FSQDadd))
    Trace.Write("L3: "+str(FSQCadd))

    Trace.Write("M1: "+str(TPSOadd))
    Trace.Write("M2: "+str(TPSDadd))
    Trace.Write("M3: "+str(TPSCadd))

    Trace.Write("O: "+str(Addsadd))'''

    FTE=Product.Attributes.GetByName('Number of FTE Communities').GetValue()
    ser=SERRadd+ANTMDadd+ANRMCadd+ATNTMDadd+ATNRMCadd+EAPPTadd+EAPPRadd+MNSadd+ADDseradd
    stn=CSQOadd+CSQDadd+CSQCadd+CSEQOadd+CSEQDadd+CSEQCadd+FSQOadd+FSQDadd+FSQCadd+TPSOadd+TPSDadd+TPSCadd+Addsadd
    swt=BSRadd+NLCadd

    FTE=int(getfloat(FTE))
    ser=int(getfloat(ser))
    stn=int(getfloat(stn))
    swt=int(getfloat(swt))

    Trace.Write(swt)
    Trace.Write(ser)
    Trace.Write(stn)
    Trace.Write(FTE)

    if (FTE == 1) and (ser <= 2) and (stn <= 10):
        ProjectSize = "Small Project"
    elif (FTE == 1) and (ser > 2 or stn > 10):
        ProjectSize = "Medium Project"
    elif (FTE <= 3):
        ProjectSize = "Medium Project"
    else:
        ProjectSize = "Large Project"

    return ProjectSize,ser,stn,swt