#For story CXCPQ-37962
import System.Decimal as D
def Node_server(Product):
    Node_flex=""
    Redundancy=""
    attr_mapping =[]
    question=[]
    if Product.Name == "Experion Enterprise Group":
        u2serever_qnt=u3serever_qnt=u4serever_qnt=0
        Redundancy=Product.Attr('Server Redundancy Requirement?').GetValue()
        question=['Flex Server Node Type','Server_NodeType']
        attr_mapping2U = ['SVR_PER_HP_Rack_RAID5','SVR_STD_DELL_Rack_RAID1','SVR_PER_DELL_Rack_RAID5','SVR_PER_DELL_Rack_RAID1_RUG','SVR_PER_DELL_Rack_RAID1_XE']
        attr_mapping3U = ['SVR_PER_DELL_Rack_RAID1','SVR_F_PER_DELL_Rack_RAID1','STN_PER_DELL_Rack_RAID1']
        attr_mapping4U = ['SVR_STD_DELL_Tower_RAID1','SVR_PER_DELL_Tower_RAID1','SVR_F_PER_DELL_Tower_RAID1','SVR_F_PER_HP_Tower_RAID1','STN_PER_DELL_Tower_RAID1','STN_PER_HP_Tower_RAID1','STN_STD_DELL_Tower_NonRAID']
        #Trace.Write(Redundancy)
        for i in question:
            Node_flex=Product.Attr(str(i)).GetValue()
            #Trace.Write(Node_flex)
            if Redundancy=="Redundant" and Node_flex in attr_mapping2U:
                u2serever_qnt +=2
            elif Redundancy=="Redundant" and Node_flex in attr_mapping3U:
                u3serever_qnt +=2
            elif Redundancy=="Redundant" and Node_flex in attr_mapping4U:
                #Trace.Write('Test')
                u4serever_qnt +=2
            if Redundancy=="Non Redundant" and Node_flex in attr_mapping2U:
                u2serever_qnt +=1
                #Trace.Write(u2serever_qnt)
            elif Redundancy=="Non Redundant" and Node_flex in attr_mapping3U:
                u3serever_qnt +=1
                #Trace.Write(u3serever_qnt)
            elif Redundancy=="Non Redundant" and Node_flex in attr_mapping4U:
                u4serever_qnt +=1
                #Trace.Write(u4serever_qnt)
    return u2serever_qnt,u3serever_qnt,u4serever_qnt
def cabinet_qnt1(Product):
    Node_flex=""
    Redundancy=""
    attr_mapping =[]
    #question1_mapping={}
    question2=[]
    if Product.Name == "Experion Enterprise Group":
        u2serever_qnt1=u3serever_qnt1=u4serever_qnt1=u2station_qnt1=u3station_qnt1=u4station_qnt1=0
        station=['CMS Flex Station Hardware Selection','CMS Console Station Hardware Selection','CMS TPS Station Hardware Selection','CMS Console Station Extension Hardware Selection','Station Type']
        server=['Hardware Design Selection_ACE Node','Hardware Design Selection','Hardware_Design_Selection - EAPP Node','Hardware Selection','Server Type1']
        station1=['Flex Station Hardware Selection TPS','Console Station Hardware Selection','TPS Station Hardware Selection','Console Station Extension Hardware Selection']
        station1_mapping=['Flex Station Qty (0-60)','Console Station Qty (0-20)','TPS Station Qty (0-20)','Console Station Extension Qty  (0-15)']
        Server_mapping=['ACE Node Rack Mount Cabinet','ACE_T_Node _Rack_Mount_Cabinet','Experion APP Node - Rack Mount','Mobile Server Nodes (0-1)','Additional Servers']
        Station_mapping=['CMS Flex Station Qty 0_60','CMS Console Station Qty 0_20','CMS TPS Station Qty 0_20','CMS Console Station Extension Qty 0_15','Additional Stations']
        attr_mapping2U1 = ['SVR_PER_HP_Rack_RAID5','SVR_STD_DELL_Rack_RAID1','SVR_PER_DELL_Rack_RAID5','SVR_PER_DELL_Rack_RAID1_RUG','SVR_PER_DELL_Rack_RAID1_XE']
        attr_mapping3U1 = ['SVR_PER_DELL_Rack_RAID1','SVR_F_PER_DELL_Rack_RAID1','STN_PER_DELL_Rack_RAID1']
        attr_mapping4U1 = ['SVR_STD_DELL_Tower_RAID1','SVR_PER_DELL_Tower_RAID1','SVR_F_PER_DELL_Tower_RAID1','SVR_F_PER_HP_Tower_RAID1','STN_PER_DELL_Tower_RAID1','STN_PER_HP_Tower_RAID1','STN_STD_DELL_Tower_NonRAID']
        #Trace.Write(Redundancy)
        for (i,j) in zip(server ,Server_mapping):
        #for qn in question1_mapping:
            attr_name = str(j)
            Node_flex=Product.Attr(str(i)).GetValue()
            #Trace.Write(Node_flex)
            #Trace.Write(i)
            #Trace.Write('attr_name: '+str(attr_name))
            if Node_flex in attr_mapping2U1:
                u2serever_qnt1 +=int(Product.Attr(str(attr_name)).GetValue()) if Product.Attr(str(attr_name)).GetValue()!='' else 0
            elif Node_flex in attr_mapping3U1:
                u3serever_qnt1 +=int(Product.Attr(str(attr_name)).GetValue()) if Product.Attr(str(attr_name)).GetValue()!='' else 0
            elif Node_flex in attr_mapping4U1:
                #Trace.Write('Test')
                u4serever_qnt1 +=int(Product.Attr(str(attr_name)).GetValue()) if Product.Attr(str(attr_name)).GetValue()!='' else 0
        for (i,j) in zip(station ,Station_mapping):
        #for qn in question1_mapping:
            attr_name = str(j)
            Node_flex=Product.Attr(str(i)).GetValue()
            #Trace.Write(Node_flex)
            #Trace.Write(i)
            #Trace.Write('attr_name: '+str(attr_name))
            if Node_flex in attr_mapping2U1:
                u2station_qnt1 +=int(Product.Attr(str(attr_name)).GetValue()) if Product.Attr(str(attr_name)).GetValue()!='' else 0
            elif Node_flex in attr_mapping3U1:
                u3station_qnt1 +=int(Product.Attr(str(attr_name)).GetValue()) if Product.Attr(str(attr_name)).GetValue()!='' else 0
            elif Node_flex in attr_mapping4U1:
                #Trace.Write('Test')
                u4station_qnt1 +=int(Product.Attr(str(attr_name)).GetValue()) if Product.Attr(str(attr_name)).GetValue()!='' else 0
        for i in station1:
            u4station_qntor=u2station_qntor=u3station_qntor=0
            Node_flex=Product.Attr(str(i)).GetValue()
            #Trace.Write(Node_flex)
            if Node_flex=='STN_PER_DELL_Rack_RAID1':
                for (i,j) in zip(station1 ,station1_mapping):
                    attr_name = str(j)
                    Node_flex=Product.Attr(str(i)).GetValue()
                    #Trace.Write(Node_flex)
                    #Trace.Write(i)
                    #Trace.Write('attr_name: '+str(attr_name))
                    if Node_flex in attr_mapping2U1:
                        u2station_qnt1 +=int(Product.Attr(str(attr_name)).GetValue()) if Product.Attr(str(attr_name)).GetValue()!='' else 0
                    elif Node_flex in attr_mapping3U1:
                        u3station_qnt1 +=int(Product.Attr(str(attr_name)).GetValue()) if Product.Attr(str(attr_name)).GetValue()!='' else 0
                    elif Node_flex in attr_mapping4U1:
                        #Trace.Write('Test')
                        u4station_qnt1 +=int(Product.Attr(str(attr_name)).GetValue()) if Product.Attr(str(attr_name)).GetValue()!='' else 0
                break
    return u2serever_qnt1,u3serever_qnt1,u4serever_qnt1,u2station_qnt1,u3station_qnt1,u4station_qnt1
def Simulation_PC(Product):
    u2serever_qnt3=u3serever_qnt3=u4serever_qnt3=0
    Node_flex=""
    Redundancy=""
    attr_mapping =[]
    #question1_mapping={}
    question2=[]
    if Product.Name == "Experion Enterprise Group":
        u2serever_qnt1=u3serever_qnt1=u3serever_qnt3=0
        server1=['Hardware Design Selection - Sim PC Node']
        attr_mapping2U1 = ['SVR_PER_HP_Rack_RAID5','SVR_STD_DELL_Rack_RAID1','SVR_PER_DELL_Rack_RAID5','SVR_PER_DELL_Rack_RAID1_RUG','SVR_PER_DELL_Rack_RAID1_XE']
        attr_mapping3U1 = ['SVR_PER_DELL_Rack_RAID1','SVR_F_PER_DELL_Rack_RAID1','STN_PER_DELL_Rack_RAID1']
        attr_mapping4U1 = ['SVR_STD_DELL_Tower_RAID1','SVR_PER_DELL_Tower_RAID1','SVR_F_PER_DELL_Tower_RAID1','SVR_F_PER_HP_Tower_RAID1','STN_PER_DELL_Tower_RAID1','STN_PER_HP_Tower_RAID1','STN_STD_DELL_Tower_NonRAID']
        #Trace.Write(Redundancy)
        for i in server1:
            Node_flex=Product.Attr(str(i)).GetValue()
            if Node_flex in attr_mapping2U1:
                #Trace.Write('test1')
                qnt1=int(Product.Attr('SIM-ACE Licenses (0-7)').GetValue()) if Product.Attr('SIM-ACE Licenses (0-7)').GetValue()!='' else 0
                qnt2=int(Product.Attr('Sim-Cx00 PC Licenses (0-20)').GetValue()) if Product.Attr('Sim-Cx00 PC Licenses (0-20)').GetValue()!='' else 0
                qnt3=int(Product.Attr('SIM-FFD Licenses (0-125)').GetValue()) if Product.Attr('SIM-FFD Licenses (0-125)').GetValue()!='' else 0
                u2serever_qnt3=D.Ceiling((qnt1+D.Ceiling(0.4*qnt2)+D.Ceiling(0.1*qnt3))/4.0)
            elif Node_flex in attr_mapping3U1:
                #Trace.Write('test2')
                qnt1=int(Product.Attr('SIM-ACE Licenses (0-7)').GetValue()) if Product.Attr('SIM-ACE Licenses (0-7)').GetValue()!='' else 0
                qnt2=int(Product.Attr('Sim-Cx00 PC Licenses (0-20)').GetValue()) if Product.Attr('Sim-Cx00 PC Licenses (0-20)').GetValue()!='' else 0
                qnt3=int(Product.Attr('SIM-FFD Licenses (0-125)').GetValue()) if Product.Attr('SIM-FFD Licenses (0-125)').GetValue()!='' else 0
                u3serever_qnt3=D.Ceiling((qnt1+D.Ceiling(0.4*qnt2)+D.Ceiling(0.1*qnt3))/4.0)
            elif Node_flex in attr_mapping4U1:
                #Trace.Write('testing value3')
                qnt1=int(Product.Attr('SIM-ACE Licenses (0-7)').GetValue()) if Product.Attr('SIM-ACE Licenses (0-7)').GetValue()!='' else 0
                #Trace.Write(qnt1)
                qnt2=int(Product.Attr('Sim-Cx00 PC Licenses (0-20)').GetValue()) if Product.Attr('Sim-Cx00 PC Licenses (0-20)').GetValue()!='' else 0
                #Trace.Write(qnt2)
                qnt3=int(Product.Attr('SIM-FFD Licenses (0-125)').GetValue()) if Product.Attr('SIM-FFD Licenses (0-125)').GetValue()!='' else 0
                #Trace.Write(qnt3)
                u4serever_qnt3=D.Ceiling((qnt1+D.Ceiling(0.4*qnt2)+D.Ceiling(0.1*qnt3))/4.0)
        return u2serever_qnt3,u3serever_qnt3,u4serever_qnt3
def Cab_qnt(Product):
    u2serever_qnt,u3serever_qnt,u4serever_qnt=Node_server(Product)
    u2serever_qnt1,u3serever_qnt1,u4serever_qnt1,u2station_qnt1,u3station_qnt1,u4station_qnt1=cabinet_qnt1(Product)
    u2serever_qnt3,u3serever_qnt3,u4serever_qnt3=Simulation_PC(Product)
    U2Server=u2serever_qnt+u2serever_qnt1+u2serever_qnt3
    Trace.Write('U2Serverqnt : '+str(U2Server))
    U3Server=u3serever_qnt+u3serever_qnt1+u3serever_qnt3
    Trace.Write('U3Serverqnt : '+str(U3Server))
    U4Server=u4serever_qnt+u4serever_qnt1+u4serever_qnt3
    Trace.Write('U4Serverqnt : '+str(U4Server))
    U2Station=u2station_qnt1
    #Trace.Write('U2Serverqnt : '+str(U2Station))
    U3Station=u3station_qnt1
    Trace.Write('U3Station : '+str(U3Station))
    U4Station=u4station_qnt1
    Trace.Write('U4Station : '+str(U4Station))
    Req2us=(U2Server*2)+U2Server
    Req3us=(U3Server*3)+U3Server
    Req4us=(U4Server*4)+U4Server
    Req2ust=(U2Station*2)+U2Station
    Req3ust=(U3Station*3)+U3Station
    Req4ust=(U4Station*4)+U4Station
    KVM_Monitor=1*2
    Total_server=U2Server+U3Server+U4Server
    Bottam_Space=1*2
    Total_U=Req2us+Req3us+Req4us+Req2ust+Req3ust+Req4ust
    if Total_U > 0:
        Total_U=Req2us+Req3us+Req4us+Req2ust+Req3ust+Req4ust+KVM_Monitor+Bottam_Space
    else:
        Total_U=0
    svr_mounting = Product.Attr('Server Mounting').GetValue()
    if svr_mounting == "Cabinet":
        cab_qnt=D.Ceiling(Total_U/24.0)
    else:
        cab_qnt = 0
        Total_U = 0
    return Total_U,cab_qnt
#U,cab,Total_server=Cab_qnt(Product)
#Trace.Write('Total U : '+str(U))
#Trace.Write('Cab_qnt : '+str(cab))
#Trace.Write('Total_server : '+str(Total_server))