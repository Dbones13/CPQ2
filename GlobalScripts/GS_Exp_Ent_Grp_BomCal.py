import System.Decimal as D
def getFloat(var):
    if var:
        return float(var)
    return 0
#44032
def MountingType(Product):
    flex=""
    Redundancy=""
    if Product.Name == "Experion Enterprise Group":
        Redundancy=Product.Attr('Server Redundancy Requirement?').GetValue()
        #Trace.Write(Redundancy)
        RaceMount=Product.Attr('Rack_Mounting_Type').GetValue()
        #Trace.Write(RaceMount)
        FlexSrvr=Product.Attr('Flex Server Rack Mounting Type').GetValue()
        #Trace.Write(FlexSrvr)
        Ace_Rack=Product.Attr('ACE Node Rack Mount Cabinet').GetValue()
        #Trace.Write("Ace_Rack:"+str(Ace_Rack))
        Ace_RMount=Product.Attr('Rack Mounting Type for_ACE Node').GetValue()
        #Trace.Write(Ace_RMount)
        AceT_Rack=Product.Attr('ACE_T_Node _Rack_Mount_Cabinet').GetValue()
        #Trace.Write(AceT_Rack)
        AceT_RackMount=Product.Attr('Rack Mounting Type for ACE-T Node').GetValue()
        #Trace.Write(AceT_RackMount)
        ExpAppNode=Product.Attr('Experion APP Node - Rack Mount').GetValue()
        #Trace.Write(ExpAppNode)
        EappMount=Product.Attr('EAPP_Mounting_Type').GetValue()
        #Trace.Write(EappMount)
        SimPC=Product.Attr('Simulation PC Furniture').GetValue()
        #Trace.Write(SimPC)
        SimPC_Rack=Product.Attr('Rack Mounting Type for SIM PC Node').GetValue()
        #Trace.Write(SimPC_Rack)
        Additional_srvr=Product.Attr('Additional servers').GetValue()
        #Trace.Write(Additional_srvr)
        Additional_srvr_Cab_Mount=Product.Attr('Additional Server Cabinet Mounting Type').GetValue()
        #Trace.Write(Additional_srvr_Cab_Mount)
        TPSPCMS1=TPSPCMF1=0
        
        qnt11=getFloat(Product.Attr('SIM-ACE Licenses (0-7)').GetValue()) if Product.Attr('SIM-ACE Licenses (0-7)').GetValue()!='' else 0
        qnt12=getFloat(Product.Attr('Sim-Cx00 PC Licenses (0-20)').GetValue()) if Product.Attr('Sim-Cx00 PC Licenses (0-20)').GetValue()!='' else 0
        qnt13=getFloat(Product.Attr('SIM-FFD Licenses (0-125)').GetValue()) if Product.Attr('SIM-FFD Licenses (0-125)').GetValue()!='' else 0
        if Redundancy=="Redundant" and RaceMount == "Fixed Mount":
            TPSPCMF1+=2
        if  Redundancy=="Redundant" and RaceMount == "Slide Mount":
            TPSPCMS1+=2
        if Redundancy=="Non Redundant" and RaceMount == "Fixed Mount":
            TPSPCMF1+=1
        if Redundancy=="Non Redundant" and RaceMount == "Slide Mount":
            TPSPCMS1+=1
        if Redundancy=="Redundant" and FlexSrvr == "Fixed Mount" :
            TPSPCMF1+=2
        if Redundancy=="Redundant" and FlexSrvr == "Slide Mount":
            TPSPCMS1+=2
        if Redundancy=="Non Redundant" and FlexSrvr == "Fixed Mount":
            TPSPCMF1+=1
        if Redundancy=="Non Redundant" and FlexSrvr == "Slide Mount":
            TPSPCMS1+=1
        if Ace_Rack>0 and Ace_RMount=='Fixed Mount':
            TPSPCMF1+=int(Ace_Rack)
        if Ace_Rack>0 and Ace_RMount=='Slide Mount':
            TPSPCMS1+=int(Ace_Rack)
        if AceT_Rack>0 and AceT_RackMount=='Fixed Mount':
            TPSPCMF1+=int(AceT_Rack)
        if AceT_Rack>0 and AceT_RackMount=='Slide Mount':
            TPSPCMS1+=int(AceT_Rack)
        if ExpAppNode>0 and EappMount=='Fixed Mount':
            TPSPCMF1+=int(ExpAppNode)
        if ExpAppNode>0 and EappMount=='Slide Mount':
            TPSPCMS1+=int(ExpAppNode)
        if SimPC=="Cabinet" and SimPC_Rack =='Fixed Mount':
            TPSPCMF1+=D.Ceiling((qnt11+D.Ceiling(float(0.4*qnt12))+D.Ceiling(float(0.1*qnt13)))/4.0)
            #TPSPCMF1+=int(SimPC)
        if SimPC=="Cabinet" and SimPC_Rack=='Slide Mount':
            TPSPCMS1+=D.Ceiling((qnt11+D.Ceiling(getFloat(0.4*qnt12))+D.Ceiling(getFloat(0.1*qnt13)))/4.0)
            #TPSPCMS1+=getFloat(SimPC)
        if Additional_srvr>0 and Additional_srvr_Cab_Mount=='Fixed Mount':
            TPSPCMF1+=int(Additional_srvr)
        if Additional_srvr>0 and Additional_srvr_Cab_Mount=='Slide Mount':
            TPSPCMS1+=int(Additional_srvr)    
    return int(TPSPCMF1),int(TPSPCMS1)
#Shivani=MountingType(Product)
#Trace.Write("Shivani:"+str(Shivani))