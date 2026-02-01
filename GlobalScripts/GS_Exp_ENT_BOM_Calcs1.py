import System.Decimal as D
def Node_station(Product,ServerNode):
    Node_flex=""
    Redundancy=""
    attr_mapping =[]
    question=[]
    if Product.Name == "Experion Enterprise Group":
        server_qnt=0
        Redundancy=Product.Attr('Server Redundancy Requirement?').GetValue()
        ServerType=Product.Attr('Experion Server Type').GetValue()
        question=['Server_NodeType','Server Node Type_desk']
        node_supplier = ['Node_Supplier_Server','Node Supplier_server']
        TPM = ['TrustedPlatformModule_TPM','Trusted Platform Module1']
     
        for (i,j,k) in zip(question,node_supplier,TPM):
            Node_flex=Product.Attr(str(i)).GetValue()
            ns = Product.Attr(str(j)).GetValue()
            tpm = Product.Attr(str(k)).GetValue()
            if Redundancy=="Redundant" and Node_flex == ServerNode and ns == "Honeywell" and ServerType in ('Server', 'Server TPS','Flex Server') and tpm == "Yes":
                server_qnt=2
            elif Redundancy=="Non Redundant" and Node_flex == ServerNode and ns == "Honeywell" and ServerType in ('Server', 'Server TPS','Flex Server') and tpm=="Yes":
                server_qnt=1
    return server_qnt
    
def station_qnt1(Product,ServerNode,StationNode):
    Node_flex=""
    question1=[]
    station_qnt_cms=station_qnt_dms=station_qnt_ori=station_qnt_add=station_qnt_mobile=station_qnt_additional=station_qnt_EAAP_Tower=station_qnt_EAAP_Rack=station_qnt_Sim_PC_Lic=0
    if Product.Name == "Experion Enterprise Group":
        server_qnt=Node_station(Product,ServerNode)
        station_qnt = 0
        station1=['ACE Node Tower Mount Desk']
        station2=['ACE Node Rack Mount Cabinet']
        station3=['ACE_T_Node _Tower_Mount_Desk']
        station4=['ACE_T_Node _Rack_Mount_Cabinet']
        station5=['Mobile Server Nodes (0-1)']
        station6=['Additional Servers']
        station7=['Experion APP Node - Tower Mount']
        station8=['Experion APP Node - Rack Mount']
        station_mapping1=['Hardware Design Selection_ ACE_Node']
        TPM1 = ['Trusted Platform Module_TPM_ACE_desk']
        station_mapping2=['Hardware Design Selection_ACE Node']
        TPM2 =['Trusted Platform Module_TPM_ACE_Node']
        station_mapping3=['Hardware Design Selection_ACE_T_Node']
        TPM3 = ['Trusted Platform Module_TPM_ACE_T']
        station_mapping4=['Hardware Design Selection']
        TPM4 = ['Ent_ace_t_Cab_tpm']
        station_mapping5=['Hardware Selection']
        TPM5 = ['Ent_ace_t_desk_tpm']
        station_mapping6=['Server Type1']
        TPM6 = ['Trusted Platform Module_TPM']
        station_mapping7=['Hardware Design Selection - EAPP Node']
        TPM7 = ['Ent_app_desk_tpm']
        station_mapping8=['Hardware_Design_Selection - EAPP Node']
        TPM8 =['Ent_app_cab_tpm']
        ACE_Tower_node=Product.Attr('Node Supplier_ACE1').GetValue()
        ACE_Rack_node=Product.Attr('Node Supplier_ACE').GetValue()
        ACE_T_Tower_node=Product.Attr('Node_Supplier_ACE_T').GetValue()
        ACE_T_Rack_node=Product.Attr('Node Supplier_ACE_T').GetValue()
        Mobile_node=Product.Attr('Node Supplier Server1').GetValue()
        Add_node=Product.Attr('Node Supplier Server').GetValue()
        EAAP_Tower_node=Product.Attr('Node Supplier_EAPP').GetValue()
        EAAP_Rack_node=Product.Attr('Node_Supplier_EAPP').GetValue()
       
        for (i1,j1,k1) in zip(station1 ,station_mapping1,TPM1):
            attr_name = str(i1)
            Node_flex=Product.Attr(str(j1)).GetValue()
            tpm = Product.Attr(str(k1)).GetValue()
            if Node_flex == StationNode and ACE_Tower_node=="Honeywell" and tpm == "Yes":
                station_qnt_cms +=int(Product.Attr(str(attr_name)).GetValue()) if Product.Attr(str(attr_name)).GetValue()!='' else 0

        for (i2,j2,k2) in zip(station2 ,station_mapping2,TPM2):
            attr_name = str(i2)
            Node_flex=Product.Attr(str(j2)).GetValue()
            tpm = Product.Attr(str(k2)).GetValue()
            if Node_flex == StationNode and ACE_Rack_node=="Honeywell" and tpm=="Yes":
                station_qnt_dms +=int(Product.Attr(str(attr_name)).GetValue()) if Product.Attr(str(attr_name)).GetValue()!='' else 0

        for (i3,j3,k3) in zip(station3 ,station_mapping3,TPM3):
            attr_name = str(i3)
            Node_flex=Product.Attr(str(j3)).GetValue()
            tpm = Product.Attr(str(k3)).GetValue()
            if Node_flex == StationNode and ACE_T_Tower_node=="Honeywell" and tpm=="Yes":
                station_qnt_ori +=int(Product.Attr(str(attr_name)).GetValue()) if Product.Attr(str(attr_name)).GetValue()!='' else 0

        for (i4,j4,k4) in zip(station4 ,station_mapping4,TPM4):
            attr_name = str(i4)
            Node_flex=Product.Attr(str(j4)).GetValue()
            tpm = Product.Attr(str(k4)).GetValue()
            if Node_flex == StationNode and ACE_T_Rack_node=="Honeywell" and tpm == "Yes":
                station_qnt_add +=int(Product.Attr(str(attr_name)).GetValue()) if Product.Attr(str(attr_name)).GetValue()!='' else 0
        for (i5,j5,k5) in zip(station5 ,station_mapping5,TPM5):
            attr_name = str(i5)
            Node_flex=Product.Attr(str(j5)).GetValue()
            tpm = Product.Attr(str(k5)).GetValue()
            if Node_flex == StationNode and Mobile_node=="Honeywell" and tpm == "Yes":
                station_qnt_mobile +=int(Product.Attr(str(attr_name)).GetValue()) if Product.Attr(str(attr_name)).GetValue()!='' else 0
        for (i6,j6,k6) in zip(station6 ,station_mapping6,TPM6):
            attr_name = str(i6)
            Node_flex=Product.Attr(str(j6)).GetValue()
            tpm = Product.Attr(str(k6)).GetValue()
            if Node_flex == StationNode and Add_node=="Honeywell" and tpm=="Yes":
                station_qnt_additional +=int(Product.Attr(str(attr_name)).GetValue()) if Product.Attr(str(attr_name)).GetValue()!='' else 0
        for (i7,j7,k7) in zip(station7 ,station_mapping7,TPM7):
            attr_name = str(i7)
            Node_flex=Product.Attr(str(j7)).GetValue()
            tpm = Product.Attr(str(k7)).GetValue()
            if Node_flex == StationNode and EAAP_Tower_node=="Honeywell" and tpm=="Yes":
                station_qnt_EAAP_Tower +=int(Product.Attr(str(attr_name)).GetValue()) if Product.Attr(str(attr_name)).GetValue()!='' else 0
        for (i8,j8,k8) in zip(station8 ,station_mapping8,TPM8):
            attr_name = str(i8)
            Node_flex=Product.Attr(str(j8)).GetValue()
            tpm = Product.Attr(str(k8)).GetValue()
            if Node_flex == StationNode and EAAP_Rack_node=="Honeywell" and tpm == "Yes":
                station_qnt_EAAP_Rack +=int(Product.Attr(str(attr_name)).GetValue()) if Product.Attr(str(attr_name)).GetValue()!='' else 0
        Sim_PC_Lic_node=Product.Attr('Node Supplier (Sim PC)').GetValue()
        Node_flex=Product.Attr(str('Hardware Design Selection - Sim PC Node1')).GetValue()
        Tpm_desk = Product.Attr(str('Ent_sim_desk_tpm')).GetValue()
        Sim_PC_Lic_node_cab=Product.Attr('Node Supplier (Sim PC)1').GetValue()
        Node_flex_cab=Product.Attr(str('Hardware Design Selection - Sim PC Node')).GetValue()
        Tpm_cab = Product.Attr(str('Ent_sim_cab_tpm')).GetValue()
        if (Node_flex == StationNode and Sim_PC_Lic_node=="Honeywell" and Tpm_desk =="Yes") or (Node_flex_cab == StationNode and Sim_PC_Lic_node_cab=="Honeywell" and Tpm_cab == "Yes"):
            qnt_SIM_ACE = qnt_Sim_Cx = qnt_SIM_FFD = 0
            if int(Product.Attr(str('SIM-ACE Licenses (0-7)')).GetValue()) > 0:
                qnt_SIM_ACE = int(Product.Attr(str('SIM-ACE Licenses (0-7)')).GetValue())
            if int(Product.Attr(str('Sim-Cx00 PC Licenses (0-20)')).GetValue()) > 0:
                qnt_Sim_Cx = int(Product.Attr(str('Sim-Cx00 PC Licenses (0-20)')).GetValue())
            if int(Product.Attr(str('SIM-FFD Licenses (0-125)')).GetValue()) > 0:
                qnt_SIM_FFD = int(Product.Attr(str('SIM-FFD Licenses (0-125)')).GetValue())
            station_qnt_Sim_PC_Lic = D.Ceiling((qnt_SIM_ACE+D.Ceiling(0.4*qnt_Sim_Cx)+D.Ceiling(0.1*qnt_SIM_FFD))/4.0)
        station_qnt = station_qnt_cms + station_qnt_dms + station_qnt_ori + station_qnt_add + station_qnt_mobile + station_qnt_additional+station_qnt_EAAP_Tower+station_qnt_EAAP_Rack+station_qnt_Sim_PC_Lic
        
    return int(server_qnt + station_qnt)