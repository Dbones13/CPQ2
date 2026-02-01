import System.Decimal as D
def Node_server(Product,que,TPM):
    Node_flex=""
    Redundancy=""
    attr_mapping =[]
    question=[]
    if Product.Name == "Experion Enterprise Group":
        server_qnt=0
        Redundancy=Product.Attr('Server Redundancy Requirement?').GetValue()
        Trace.Write(Redundancy)
        question=['Server_NodeType','Server Node Type_desk']
        # node supplier and TPM
        node_supplier = ['Node_Supplier_Server','Node Supplier_server']
        trusted_platform_module = ['TrustedPlatformModule_TPM','Trusted Platform Module1']
        # kaousalya
        quantity=["Additional Servers", "ACE Node Tower Mount Desk" ,"ACE Node Rack Mount Cabinet", "Mobile Server Nodes (0-1)", "Experion APP Node - Tower Mount", "Experion APP Node - Rack Mount", "ACE_T_Node _Tower_Mount_Desk", "ACE_T_Node _Rack_Mount_Cabinet"]
        question1= ["Server Type1", "Hardware Design Selection_ ACE_Node", "Hardware Design Selection_ACE Node", "Hardware Selection", "Hardware Design Selection - EAPP Node", "Hardware_Design_Selection - EAPP Node", "Hardware Design Selection_ACE_T_Node", "Hardware Design Selection"]
        nodeSupliers=["Node Supplier Server","Node Supplier_ACE1", "Node Supplier_ACE", "Node Supplier Server1", "Node Supplier_EAPP", "Node_Supplier_EAPP", "Node_Supplier_ACE_T", "Node Supplier_ACE_T"]
        trustedPlatformModules=["Trusted Platform Module_TPM", "Trusted Platform Module_TPM_ACE_desk", "Trusted Platform Module_TPM_ACE_Node", "Ent_ace_t_desk_tpm", "Ent_app_desk_tpm", "Ent_app_cab_tpm", "Trusted Platform Module_TPM_ACE_T", "Ent_ace_t_Cab_tpm"]
        
        sim_server1=['Hardware Design Selection - Sim PC Node', 'Hardware Design Selection - Sim PC Node1']
        sim_Node1=['Node Supplier (Sim PC)1', 'Node Supplier (Sim PC)']
        sim_trustedPlatformModules=["Ent_sim_cab_tpm", "Ent_sim_desk_tpm"]
        
        for (i,j,k,l) in zip(quantity,question1,nodeSupliers,trustedPlatformModules):
            qty=Product.Attr(str(i)).GetValue()
            Node=Product.Attr(str(j)).GetValue()
            nds=Product.Attr(str(k)).GetValue()
            tstpm=Product.Attr(str(l)).GetValue()
            if qty!="":
                if int(qty)>0 and Node in que and nds=="Honeywell" and tstpm==TPM:
                    server_qnt+=int(qty)
        for (i,j,k) in zip(sim_server1,sim_Node1,sim_trustedPlatformModules):
            sim_server1Value = Product.Attr(str(i)).GetValue()
            sim_Node1Value   = Product.Attr(str(j)).GetValue()
            sim_tpmValue     = Product.Attr(str(k)).GetValue()
            if sim_server1Value in que and sim_Node1Value=="Honeywell" and sim_tpmValue==TPM:
                qnt11=int(Product.Attr('SIM-ACE Licenses (0-7)').GetValue()) if Product.Attr('SIM-ACE Licenses (0-7)').GetValue()!='' else 0
                qnt12=int(Product.Attr('Sim-Cx00 PC Licenses (0-20)').GetValue()) if Product.Attr('Sim-Cx00 PC Licenses (0-20)').GetValue()!='' else 0
                qnt13=int(Product.Attr('SIM-FFD Licenses (0-125)').GetValue()) if Product.Attr('SIM-FFD Licenses (0-125)').GetValue()!='' else 0
                server_qnt+=D.Ceiling((qnt11+D.Ceiling(0.4*qnt12)+D.Ceiling(0.1*qnt13))/4.0)
                
        #CXCPQ-37560,37562,37563,37564
        for (i,j,k) in zip(question,node_supplier,trusted_platform_module):
            Node_flex=Product.Attr(str(i)).GetValue()
            ns = Product.Attr(str(j)).GetValue()
            tpm = Product.Attr(str(k)).GetValue()
            #Trace.Write(Node_flex)
            if Redundancy=="Redundant" and Node_flex in que and ns == "Honeywell" and tpm == TPM:
                server_qnt+=2
            elif Redundancy=="Non Redundant" and Node_flex in que and ns == "Honeywell" and tpm == TPM:
                server_qnt+=1
    return server_qnt

def total_servers_and_stations(Product):
    servers_stations = ('Displays_server01','Mobile Server Nodes (0-1)','Additional Servers','Additional Stations','CMS Flex Station Qty 0_60','CMS Console Station Qty 0_20','CMS TPS Station Qty 0_20','CMS Console Station Extension Qty 0_15','DMS Flex Station Qty 0_60','DMS Console Station Qty 0_20','DMS TPS Station Qty 0_20','DMS Console Station Extension Qty 0_15','Flex Station Qty (0-60)','Console Station Qty (0-20)','TPS Station Qty (0-20)','Console Station Extension Qty  (0-15)')
    total_servers_stations_qty = 0
    for attr_name in servers_stations:
        total_servers_stations_qty +=int(Product.Attr(str(attr_name)).GetValue()) if Product.Attr(str(attr_name)).GetValue()!='' else 0
    return total_servers_stations_qty