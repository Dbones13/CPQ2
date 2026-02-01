import math as m
def getint(x):
    if x=="":
        x=0
    return int(x)

def getebrparts(Product):
    E1=0
    E2=0
    E3=0
    E4=0
    E5=0
    
    y=Product
    CMSF=y.Attributes.GetByName('CMS Flex Station Qty 0_60').GetValue()
    CMSF=getint(CMSF)
    DMSF=y.Attributes.GetByName('DMS Flex Station Qty 0_60').GetValue()
    DMSF=getint(DMSF)

    CCSQ=y.Attributes.GetByName('CMS Console Station Qty 0_20').GetValue()
    CCSQ=getint(CCSQ)
    DCSQ=y.Attributes.GetByName('DMS Console Station Qty 0_20').GetValue()
    DCSQ=getint(DCSQ)

    CCSEQ=y.Attributes.GetByName('CMS Console Station Extension Qty 0_15').GetValue()
    CCSEQ=getint(CCSEQ)
    DCSEQ=y.Attributes.GetByName('DMS Console Station Extension Qty 0_15').GetValue()
    DCSEQ=getint(DCSEQ)

    CMST=y.Attributes.GetByName('CMS TPS Station Qty 0_20').GetValue()
    CMST=getint(CMST)
    DMST=y.Attributes.GetByName('DMS TPS Station Qty 0_20').GetValue()
    DMST=getint(DMST)



    #E1
    if y.Attributes.GetByName('Experion Backup & Restore (Experion Server)').GetValue()=="Yes" or y.Attributes.GetByName('Experion Backup & Restore (Experion TPS Server)').GetValue()=="Yes":
        if y.Attributes.GetByName('Experion Server Type').GetValue()=="Flex Server":
            if y.Attributes.GetByName('Server Redundancy Requirement?').GetValue()=="Redundant":
                E1=E1+2+int(y.Attributes.GetByName("Additional Stations").GetValue())
            elif y.Attributes.GetByName('Server Redundancy Requirement?').GetValue()=="Non Redundant":
                E1=E1+1+int(y.Attributes.GetByName("Additional Stations").GetValue())
    #E2
    if y.Attributes.GetByName('Experion Backup & Restore (Flex Station ES-F)').GetValue()=="Yes" or y.Attributes.GetByName('Experion Backup & Restore (Flex Station ES-F)1').GetValue()=="Yes":
        E2=E2+CMSF+DMSF
    
    #E3
    if y.Attributes.GetByName('Experion Backup & Restore (TPS Station ES-T)').GetValue()=="Yes":
        E3=E3+CMST+DMST

    #E4
    if y.Attributes.GetByName('Experion Backup & Restore (Console Station ES-C)').GetValue()=="Yes":
        E4=E4+CCSQ+DCSQ

    #E5
    if y.Attributes.GetByName('Experion Backup & Restore (Console)').GetValue()=="Yes" or y.Attributes.GetByName('Experion Backup & Restore ConsoleStation Extension').GetValue()=="Yes":
        E5=E5+CCSEQ+DCSEQ

    qnt=E1+E2+E3+E4+E5
    Trace.Write(qnt)
    return qnt

def getebrpartsNode(Product):
    B1=0
    B2=0
    B3=0
    B4=0
    B5=0
    B6=0
    
    y=Product

    ANTMD=y.Attributes.GetByName('ACE Node Tower Mount Desk').GetValue()
    ANTMD=getint(ANTMD)
    ANRMC=y.Attributes.GetByName('ACE Node Rack Mount Cabinet').GetValue()
    ANRMC=getint(ANRMC)

    ATNTMD=y.Attributes.GetByName('ACE_T_Node _Tower_Mount_Desk').GetValue()
    ATNTMD=getint(ATNTMD)
    ATNRMC=y.Attributes.GetByName('ACE_T_Node _Rack_Mount_Cabinet').GetValue()
    ATNRMC=getint(ATNRMC)

    EAPPT=y.Attributes.GetByName('Experion APP Node - Tower Mount').GetValue()
    EAPPT=getint(EAPPT)
    EAPPR=y.Attributes.GetByName('Experion APP Node - Rack Mount').GetValue()
    EAPPR=getint(EAPPR)

    MSN=y.Attributes.GetByName('Mobile Server Nodes (0-1)').GetValue()
    MSN=getint(MSN)

    SAL=y.Attributes.GetByName('SIM-ACE Licenses (0-7)').GetValue()
    SAL=getint(SAL)

    SXOO=y.Attributes.GetByName('Sim-Cx00 PC Licenses (0-20)').GetValue()
    SXOO=getint(SXOO)

    SFED=y.Attributes.GetByName('SIM-FFD Licenses (0-125)').GetValue()
    SFED=getint(SFED)

    #B1
    if y.Attributes.GetByName('Experion Backup & Restore (Experion Server)').GetValue()=="Yes" or y.Attributes.GetByName('Experion Backup & Restore (Experion TPS Server)').GetValue()=="Yes":
        if y.Attributes.GetByName('Experion Server Type').GetValue()=="Server" or y.Attributes.GetByName('Experion Server Type').GetValue()=="Server TPS":
            if y.Attributes.GetByName('Server Redundancy Requirement?').GetValue()=="Redundant":
                B1=B1+2+int(y.Attributes.GetByName("Additional Stations").GetValue())
            elif y.Attributes.GetByName('Server Redundancy Requirement?').GetValue()=="Non Redundant":
                B1=B1+1+int(y.Attributes.GetByName("Additional Stations").GetValue())
    #B2
    if y.Attributes.GetByName('Experion Backup & Restore (ACE)').GetValue()=="Yes" or y.Attributes.GetByName('Experion Backup & Restore (ACE)1').GetValue()=="Yes":
        B2=B2+ANTMD+ANRMC

    #B3
    if y.Attributes.GetByName('Experion Backup & Restore (ACE-T)').GetValue()=="Yes":
        B3=B3+ATNTMD+ATNRMC

    #B4
    if y.Attributes.GetByName('Experion Backup & Restore (Experion APP)').GetValue()=="Yes":
        B4=B4+EAPPT+EAPPR

    #B5
    if y.Attributes.GetByName('Experion Backup & Restore (Mobile Terminal Server)').GetValue()=="Yes":
        B5=B5+MSN

    #B6
    if y.Attributes.GetByName('Experion Backup & Restore (Simulation PC)').GetValue()=="Yes" or y.Attributes.GetByName('Experion Backup & Restore (Simulation PC)1').GetValue()=="Yes":
        B6= B6 + m.ceil ((SAL + m.ceil(0.4 * SXOO) + m.ceil(0.1 * SFED))/4.0)

    addall=B1+B2+B3+B4+B5+B6
    Trace.Write(addall)
    return addall