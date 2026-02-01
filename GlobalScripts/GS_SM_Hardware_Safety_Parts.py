def getSMSystemParts(Product,parts_dict):
    A=0
    B=0
    C=0

    P=0
    Q=0
    R=0

    X=0
    Y=0
    Z=0

    L=0
    M=0
    N=0
    
    E=0
    F=0
    G=0

    SBSR = Product.GetContainerByName("SM_Hardware_Builder_Station_Cont").Rows[0].GetColumnByName("SM_Builder_Station_Required").Value
    SBSST = Product.GetContainerByName("SM_Hardware_Builder_Station_Cont").Rows[0].GetColumnByName("Station_Type").Value
    SBSNS = Product.GetContainerByName("SM_Hardware_Builder_Station_Cont").Rows[0].GetColumnByName("Node_Supplier").Value
    Trace.Write(SBSR)
    Trace.Write(SBSST)
    Trace.Write(SBSNS)

    SSSR = Product.GetContainerByName("SM_Hardware_Simulation_Station_Cont").Rows[0].GetColumnByName("SM_Simulation_Station_Required").Value
    SSST = Product.GetContainerByName("SM_Hardware_Simulation_Station_Cont").Rows[0].GetColumnByName("Station_Type").Value
    SSNT = Product.GetContainerByName("SM_Hardware_Simulation_Station_Cont").Rows[0].GetColumnByName("Node_Supplier").Value
    Trace.Write(SSSR)
    Trace.Write(SSST)
    Trace.Write(SSNT)

    SHSR = Product.GetContainerByName("SM_Hardware_Historian_Station_Cont").Rows[0].GetColumnByName("SM_Historian_Station_Required").Value
    SHST = Product.GetContainerByName("SM_Hardware_Historian_Station_Cont").Rows[0].GetColumnByName("Station_Type").Value
    SHNT = Product.GetContainerByName("SM_Hardware_Historian_Station_Cont").Rows[0].GetColumnByName("Node_Supplier").Value
    Release = Product.GetContainerByName("SM_Common_Questions").Rows[0].GetColumnByName("Experion Software Release").Value
    Trace.Write(SHSR)
    Trace.Write(SHST)
    Trace.Write(SHNT)

    #CXCPQ-42706
    if int(SBSR) > 0 and SBSST=="STN_PER_DELL_Rack_RAID1" and SBSNS=="Honeywell" and Release=='R530':
        A=int(SBSR)
    else:
        A=0
    Trace.Write("A: "+str(A))


    if int(SSSR) > 0 and SSST=="STN_PER_DELL_Rack_RAID1" and SSNT=="Honeywell" and Release=='R530':
        B=int(SSSR)
    else:
        B=0

    Trace.Write("B: "+str(B))

    if int(SHSR) > 0 and SHST=="STN_PER_DELL_Rack_RAID1" and SHNT=="Honeywell" and Release=='R530':
        C=int(SHSR)
    else:
        C=0

    Trace.Write("C: "+str(C))

    add= int(A)+int(B)+int(C)
    Trace.Write("add: "+str(add))
    #------------------------------------------------------

    #CXCPQ-42704
    if int(SBSR) > 0 and SBSST=="STN_PER_HP_Tower_RAID1" and SBSNS=="Honeywell" and Release=='R530':
        P=int(SBSR)
    else:
        P=0
    Trace.Write("P: "+str(P))


    if int(SSSR) > 0 and SSST=="STN_PER_HP_Tower_RAID1" and SSNT=="Honeywell" and Release=='R530':
        Q=int(SSSR)
    else:
        Q=0

    Trace.Write("Q: "+str(Q))

    if int(SHSR) > 0 and SHST=="STN_PER_HP_Tower_RAID1" and SHNT=="Honeywell" and Release=='R530':
        R=int(SHSR)
    else:
        R=0

    Trace.Write("R: "+str(R))

    add2= int(P)+int(Q)+int(R)
    Trace.Write("add2: "+str(add2))
    #---------------------------------------------------------

    #CXCPQ-42702
    if int(SBSR) > 0 and SBSST=="STN_PER_DELL_Tower_RAID1" and SBSNS=="Honeywell" and Release=='R530':
        X=int(SBSR)
    else:
        X=0
    Trace.Write("X: "+str(X))


    if int(SSSR) > 0 and SSST=="STN_PER_DELL_Tower_RAID1" and SSNT=="Honeywell" and Release=='R530':
        Y=int(SSSR)
    else:
        Y=0

    Trace.Write("Y: "+str(Y))

    if int(SHSR) > 0 and SHST=="STN_PER_DELL_Tower_RAID1" and SHNT=="Honeywell" and Release=='R530':
        Z=int(SHSR)
    else:
        Z=0

    Trace.Write("Z: "+str(Z))

    add3= int(X)+int(Y)+int(Z)
    Trace.Write("add3: "+str(add3))
    #-----------------------------------------------------------

    ##CXCPQ-42701
    if int(SBSR) > 0 and SBSST=="STN_STD_DELL_Tower_NonRAID" and SBSNS=="Honeywell":
        L=int(SBSR)
    else:
        L=0
    Trace.Write("L: "+str(L))


    if int(SSSR) > 0 and SSST=="STN_STD_DELL_Tower_NonRAID" and SSNT=="Honeywell":
        M=int(SSSR)
    else:
        M=0

    Trace.Write("M: "+str(M))

    if int(SHSR) > 0 and SHST=="STN_STD_DELL_Tower_NonRAID" and SHNT=="Honeywell":
        N=int(SHSR)
    else:
        N=0

    Trace.Write("N: "+str(N))

    add4= int(L)+int(M)+int(N)
    Trace.Write("add4: "+str(add4))
  
    if int(SBSR) > 0 and SBSST=="STN_PER_DELL_Tower_RAID2" and SBSNS=="Honeywell":
        E=int(SBSR)
    else:
        E=0
    Trace.Write("L: "+str(L))


    if int(SSSR) > 0 and SSST=="STN_PER_DELL_Tower_RAID2" and SSNT=="Honeywell":
        F=int(SSSR)
    else:
        F=0

    Trace.Write("M: "+str(M))

    if int(SHSR) > 0 and SHST=="STN_PER_DELL_Tower_RAID2" and SHNT=="Honeywell":
        G=int(SHSR)
    else:
        G=0

    Trace.Write("N: "+str(N))

    add5= int(E)+int(F)+int(G)

    if add>0:
        #parts_dict["MZ-PCWS77"] = {'Quantity' : add, 'Description': 'WKS PC DELL R7920XL RAID1 RACK'}
        parts_dict["MZ-PCWR01"] = {'Quantity' : add, 'Description': 'WKS PC DELL R7960XL RAID1 RACK'}

    if add2>0:
        #parts_dict["MZ-PCWS84"] = {'Quantity' : add2, 'Description': 'WKS PC HP Z4 G4 RAID1 TOWER'}
        parts_dict["MZ-PCWS86"] = {'Quantity' : add2, 'Description': 'WKS PC HP Z4 G5 RAID1 TOWER'}

    if add3>0:
        #parts_dict["MZ-PCWS94"] = {'Quantity' : add3, 'Description': 'WKS PC DELL T5820XL RAID1 TOWER MLK'}
        parts_dict["MZ-PCWT01"] = {'Quantity' : add3, 'Description': 'WKS PC DELL T5860XL RAID1 TOWER'}
        
    if add4>0:
        #parts_dict["MZ-PCWS14"] = {'Quantity' : add4, 'Description': 'WKS HW OPTIPLEX XE3 TWR WIN10 LTSC 2019'}
        parts_dict["MZ-PCWS15"] = {'Quantity' : add4, 'Description': 'WKS HW OPTIPLEX XE4 TWR WIN10 LTSC 2021'}

    if add5>0:
          parts_dict["MZ-PCWT02"] = {'Quantity' : add5, 'Description': 'WKS DELL T160 RAID1 TOWER'}
          parts_dict["EP-COAS19"] = {'Quantity' : add5, 'Description': 'Windows Server Standard 2019 COA'}
          parts_dict["MZ-SQLCL4"] = {'Quantity' : add5, 'Description': 'Microsoft SQL Client Access License'}
          parts_dict["TP-FPW241"] = {'Quantity' : add5, 'Description': 'NEC MultiSync E243WMi Display 24 inch'}

    #CXCPQ-42833,CXCPQ-42707
    def getQty1(parts_dict,partName):
        try:
            return int(parts_dict[partName]['Quantity'])
        except KeyError:
            return 0

    MZPCWS14Q=getQty1(parts_dict,'MZ-PCWS15')
    MZPCWS94Q=getQty1(parts_dict,'MZ-PCWT01')
    MZPCWS84Q=getQty1(parts_dict,'MZ-PCWS86')
    MZPCWS77Q=getQty1(parts_dict,'MZ-PCWR01')
    MZP = MZPCWS94Q + MZPCWS84Q + MZPCWS77Q
    if MZP>0 or MZPCWS14Q>0:
        if Product.GetContainerByName("SM_Common_Questions").Rows[0].GetColumnByName("Experion Software Release").Value=="R530":
            parts_dict["TP-FPW241"] = {'Quantity' : MZP+MZPCWS14Q, 'Description': 'NEC MultiSync E243WMi Display 24 inch'}
            parts_dict["MZ-SQLCL4"] = {'Quantity' : MZP+MZPCWS14Q, 'Description': 'Microsoft SQL Client Access License'}
            parts_dict["EP-COAW21"] = {'Quantity' : MZP, 'Description': 'MSFT WINDOWS 10 IOT ENT LTSC 2021 COA'}
        #elif Product.GetContainerByName("SM_Common_Questions").Rows[0].GetColumnByName("Experion Software Release").Value=="R520":
            #parts_dict["EP-COAW19"] = {'Quantity' : MZP, 'Description': 'WINDOWS 10 IOT ENT LTSC 2019 COA'}
        #elif Product.GetContainerByName("SM_Common_Questions").Rows[0].GetColumnByName("Experion Software Release").Value=="R511":
            #parts_dict["EP-COAW10"] = {'Quantity' : MZP, 'Description': 'Windows 10 COA'}
        #elif Product.GetContainerByName("SM_Common_Questions").Rows[0].GetColumnByName("Experion Software Release").Value=="R510":
            #parts_dict["EP-COAW10"] = {'Quantity' : MZP, 'Description': 'Windows 10 COA'}
    return parts_dict