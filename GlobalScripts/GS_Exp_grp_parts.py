import System.Decimal as D
def get_part(Product):
    if Product.Name == "Experion Enterprise Group":
        Redundancy=Product.Attr('Server Redundancy Requirement?').GetValue()
        Trace.Write(Redundancy)
        val = 0
        server_type = Product.Attr('Experion Server Type').GetValue()
        if server_type == "Server":
            display_size = Product.Attr('Display Size_server').GetValue()
            display_Supplier = Product.Attr('Display Supplier_Server').GetValue()
            Displays = int(Product.Attr('Displays_server01').GetValue()) if Product.Attr('Displays_server01').GetValue()!='' else 0
            Trace.Write(Displays)
            if display_size == "24 inch NTS NEC" and display_Supplier == "Honeywell" and Displays > 0 :
                if Redundancy == "Redundant":
                    val += 2 * Displays
                elif Redundancy == "Non Redundant":
                    val += Displays
        elif server_type == "Flex Server":
            display_size_flex = Product.Attr('Display_Size_FlexServer').GetValue()
            touchscreen = Product.Attr('TouchScreen_FlexServerDesk').GetValue()
            display_Supplier_flex = Product.Attr('Display_Supplier').GetValue()
            Displays_2_flex = int(Product.Attr('Displays_Flex Server in Desk0_2_2').GetValue()) if Product.Attr('Displays_Flex Server in Desk0_2_2').GetValue()!='' else 0
            Displays_flex = int(Product.Attr('Displays_Flex Server in Desk0_2').GetValue()) if Product.Attr('Displays_Flex Server in Desk0_2').GetValue()!='' else 0
            if display_size_flex == "24 inch NTS NEC" and touchscreen == "No" and display_Supplier_flex == "Honeywell" :
                if Redundancy == "Redundant" and (Displays_flex > 0 or Displays_2_flex > 0):
                    val += 2 * Displays_flex
                    val +=  2 * Displays_2_flex
                elif Redundancy == "Non Redundant" and (Displays_flex > 0 or Displays_2_flex > 0):
                    val += Displays_flex
                    val += Displays_2_flex
        return val
#CXCPQ-39104, CXCPQ-39105
def station_1(Product):
    Node_flex=""
    station_qnt1 = station_qnt2 = 0
    if Product.Name == "Experion Enterprise Group":
        Redundancy=Product.Attr('Server Redundancy Requirement?').GetValue()
        #server Question
        question=Product.Attr('Flex Server Node Type').GetValue()
        #Trace.Write("Q:"+str(question))
        # Remote Peripheral Solution Type 
        RPS = Product.Attr('Remote Peripheral Solution Type (RPS) - (Flex Server -Cabinet)').GetValue()
        #Trace.Write("rps:"+str(RPS))
        # hardware question
        hwd_svr = ['SVR_F_PER_DELL_Tower_RAID1','SVR_F_PER_DELL_Rack_RAID1','SVR_F_PER_HP_Tower_RAID1']
        # RPS Mounting Furniture (Flex Server Cabinet)
        RPS_furniture = Product.Attr('RPS Mounting Furniture (Flex Server Cabinet)').GetValue()
        #Trace.Write("RPS_furniture:"+str(RPS_furniture))

        if question in hwd_svr:
            if RPS == "Extio3-Single Mode Fiber" and RPS_furniture == "Icon":
                if Redundancy == "Redundant":
                    station_qnt1 += 2
                elif Redundancy == "Non Redundant":
                    station_qnt1 += 1
            elif RPS == "Extio3-Multi Mode Fiber" and RPS_furniture == "Icon":
                Trace.Write("cond 2 worker")
                if Redundancy == "Redundant":
                    station_qnt2 += 2
                elif Redundancy == "Non Redundant":
                    station_qnt2 += 1

        #station Question
        station1=['CMS Flex Station Hardware Selection','CMS Console Station Hardware Selection','CMS TPS Station Hardware Selection','CMS Console Station Extension Hardware Selection']
        station2=['DMS Flex Station Hardware Selection','DMS Console Station Hardware Selection','DMS TPS Station Hardware Selection','DMS Console Station Extension Hardware Selection']
        #station Question Quantity mapping
        station_mapping1=['CMS Flex Station Qty 0_60','CMS Console Station Qty 0_20','CMS TPS Station Qty 0_20','CMS Console Station Extension Qty 0_15']
        station_mapping2=['DMS Flex Station Qty 0_60','DMS Console Station Qty 0_20','DMS TPS Station Qty 0_20','DMS Console Station Extension Qty 0_15']
        # Remote Peripheral Solution Type 
        cms_RPS = Product.Attr('CMS Remote Peripheral Solution Type RPS').GetValue()
        dms_RPS = Product.Attr('DMS Remote Peripheral Solution Type RPS').GetValue()
        # RPS - Mounting Furniture
        cms_furniture = Product.Attr('CMS RPS Mounting Furniture').GetValue()
        dms_furniture = Product.Attr('DMS RPS Mounting Furniture').GetValue()
        # hardware question
        hwd_que = ['STN_PER_DELL_Tower_RAID1','STN_PER_DELL_Rack_RAID1','STN_PER_HP_Tower_RAID1','STN_STD_DELL_Tower_NonRAID']
        # Required
        cms_required = Product.Attr('CMS Cabinet Mounting Stations required').GetValue()
        dms_required = Product.Attr('DMS Desk Mounting Stations required').GetValue()
        # Furniture Que
        Fur_Q = ['Icon','Z/EZ']

        # CMS
        if cms_required != "No":
            for (i,j) in zip(station1 ,station_mapping1):
                attr_name = str(j)
                Node_flex=Product.Attr(str(i)).GetValue()
                
                if Node_flex in hwd_que and cms_RPS=="Extio3-Single Mode Fiber" and cms_furniture in Fur_Q:
                    # CXCPQ-39104
                    station_qnt1 +=int(Product.Attr(str(attr_name)).GetValue()) if Product.Attr(str(attr_name)).GetValue()!='' else 0
                elif Node_flex in hwd_que and cms_RPS=="Extio3-Multi Mode Fiber" and cms_furniture in Fur_Q:
                    # CXCPQ-39105
                    station_qnt2 +=int(Product.Attr(str(attr_name)).GetValue()) if Product.Attr(str(attr_name)).GetValue()!='' else 0
        # DMS
        if dms_required != "No":
            for (i,j) in zip(station2 ,station_mapping2):
                attr_name = str(j)
                Node_flex=Product.Attr(str(i)).GetValue()
                Trace.Write("Node_flex: "+str(Node_flex))
                if Node_flex in hwd_que and dms_RPS=="Extio3-Single Mode Fiber" and dms_furniture in Fur_Q:
                    # CXCPQ-39104
                    station_qnt1 +=int(Product.Attr(str(attr_name)).GetValue()) if Product.Attr(str(attr_name)).GetValue()!='' else 0
                elif Node_flex in hwd_que and dms_RPS=="Extio3-Multi Mode Fiber" and dms_furniture in Fur_Q:
                    # CXCPQ-39105
                    station_qnt2 +=int(Product.Attr(str(attr_name)).GetValue()) if Product.Attr(str(attr_name)).GetValue()!='' else 0

    return int(station_qnt1), int(station_qnt2)

#CXCPQ-38880,(CXCPQ-38876,CXCPQ-38875),CXCPQ-38882
def get_parts(Product):
    if Product.Name == "Experion Enterprise Group":
        Redundancy=Product.Attr('Server Redundancy Requirement?').GetValue()
        Trace.Write(Redundancy)
        val = val1 = val2 = 0
        server_type = Product.Attr('Experion Server Type').GetValue()
        if server_type == "Server" or server_type == "Server TPS":
            display_size = Product.Attr('Display Size_server').GetValue()
            display_Supplier = Product.Attr('Display Supplier_Server').GetValue()
            Displays = int(Product.Attr('Displays_server01').GetValue()) if Product.Attr('Displays_server01').GetValue()!='' else 0
            if display_size == "27 inch NTS NEC" and display_Supplier == "Honeywell" and Displays > 0 :
                if Redundancy == "Redundant":
                    val += 2 * Displays
                elif Redundancy == "Non Redundant":
                    val += Displays
            elif display_size == "21.33 inch NTS" and display_Supplier == "Honeywell" and Displays > 0 :
                if Redundancy == "Redundant":
                    val1 += 2 * Displays
                    #val2 += 2 * Displays
                elif Redundancy == "Non Redundant":
                    val1 += Displays
                    #val2 += Displays
        elif server_type == "Flex Server":
            display_size_flex = Product.Attr('Display_Size_FlexServer').GetValue()
            touchscreen = Product.Attr('TouchScreen_FlexServerDesk').GetValue()
            display_Supplier_flex = Product.Attr('Display_Supplier').GetValue()
            Displays_2_flex = int(Product.Attr('Displays_Flex Server in Desk0_2_2').GetValue()) if Product.Attr('Displays_Flex Server in Desk0_2_2').GetValue()!='' else 0
            Displays_flex = int(Product.Attr('Displays_Flex Server in Desk0_2').GetValue()) if Product.Attr('Displays_Flex Server in Desk0_2').GetValue()!='' else 0
            if display_size_flex == "27 inch NTS NEC" and touchscreen == "No" and display_Supplier_flex == "Honeywell" :
                if Redundancy == "Redundant" and (Displays_flex > 0 or Displays_2_flex > 0):
                    val += 2 * Displays_flex
                    val +=  2 * Displays_2_flex
                elif Redundancy == "Non Redundant" and (Displays_flex > 0 or Displays_2_flex > 0):
                    val += Displays_flex
                    val += Displays_2_flex
            elif display_size_flex == "21.33 inch NTS" and touchscreen == "No" and display_Supplier_flex == "Honeywell" :
                if Redundancy == "Redundant" and (Displays_flex > 0 or Displays_2_flex > 0):
                    val1 += 2 * Displays_flex
                    val1 +=  2 * Displays_2_flex
                elif Redundancy == "Non Redundant" and (Displays_flex > 0 or Displays_2_flex > 0):
                    val1 += Displays_flex
                    val1 += Displays_2_flex
            elif display_size_flex == "21.33 inch Touch" and touchscreen == "Yes" and display_Supplier_flex == "Honeywell" :
                if Redundancy == "Redundant" and (Displays_flex > 0 or Displays_2_flex > 0):
                    val2 += 2 * Displays_flex
                    val2 +=  2 * Displays_2_flex
                elif Redundancy == "Non Redundant" and (Displays_flex > 0 or Displays_2_flex > 0):
                    Trace.Write("Condition worked")
                    val2 += Displays_flex
                    val2 += Displays_2_flex
        ## ACE-APP node desk
        # Display Size
        size_list = ['Display Size _ACE_desk_pre','Display Size (ACE-T)','Display Size_EAPP']
        # Dispay Supplier
        supplier_list = ['Display Supplier (ACE)','Display Supplier (ACE-T)','Display Supplier_EAPP']
        # Input Question
        Node_list = ['ACE Node Tower Mount Desk','ACE_T_Node _Tower_Mount_Desk','Experion APP Node - Tower Mount']
        Display_list = ['Displays_ace_desk_pre','Displays (ACE-T)(0-1)','Displays_EAPP']

        for (i,j,k,l) in zip(size_list,supplier_list,Node_list,Display_list):
            size = Product.Attr(str(i)).GetValue()
            supplier = Product.Attr(str(j)).GetValue()
            node = int(Product.Attr(str(k)).GetValue()) if Product.Attr(str(k)).GetValue()!='' else 0
            if node > 0 and size == "27 inch NTS NEC" and supplier == "Honeywell":
                val += node * int(Product.Attr(str(l)).GetValue()) if Product.Attr(str(l)).GetValue()!='' else 0
            elif node > 0 and size == "21.33 inch NTS" and supplier == "Honeywell":
                val1 += node * int(Product.Attr(str(l)).GetValue()) if Product.Attr(str(l)).GetValue()!='' else 0
                #val2 += node * int(Product.Attr(str(l)).GetValue()) if Product.Attr(str(l)).GetValue()!='' else 0
        
        ## SIM PC CALCULATION
        sim_val = 0
        sim_size = Product.Attr('Display Size (Sim PC)').GetValue()
        sim_supplier = Product.Attr('Display Supplier (Sim PC)').GetValue()
        qnt1=int(Product.Attr('SIM-ACE Licenses (0-7)').GetValue()) if Product.Attr('SIM-ACE Licenses (0-7)').GetValue()!='' else 0
        qnt2=int(Product.Attr('Sim-Cx00 PC Licenses (0-20)').GetValue()) if Product.Attr('Sim-Cx00 PC Licenses (0-20)').GetValue()!='' else 0
        qnt3=int(Product.Attr('SIM-FFD Licenses (0-125)').GetValue()) if Product.Attr('SIM-FFD Licenses (0-125)').GetValue()!='' else 0
        if sim_size == "27 inch NTS NEC" and sim_supplier == "Honeywell":
            sim_val=D.Ceiling((qnt1+D.Ceiling(0.4*qnt2)+D.Ceiling(0.1*qnt3))/4.0)
            val+=sim_val
            Trace.Write("SIM: "+str(sim_val))
        elif sim_size == "21.33 inch NTS" and sim_supplier == "Honeywell":
            sim_val=D.Ceiling((qnt1+D.Ceiling(0.4*qnt2)+D.Ceiling(0.1*qnt3))/4.0)
            val1+=sim_val
            #val2+=sim_val
            Trace.Write("SIM1: "+str(sim_val))
            

        ## Mobile Server Node
        mobile_svr = int(Product.Attr('Mobile Server Nodes (0-1)').GetValue()) if Product.Attr('Mobile Server Nodes (0-1)').GetValue()!='' else 0
        mobile_size = Product.Attr('Display Size (Mobile Server)').GetValue()
        mobile_supplier = Product.Attr('Display Supplier (Mobile Server)').GetValue()
        if mobile_svr > 0:
            if mobile_size == "27 inch NTS NEC" and mobile_supplier == "Honeywell":
                val += mobile_svr 
            elif mobile_size == "21.33 inch NTS" and mobile_supplier == "Honeywell":
                val1 += mobile_svr
                #val2 += mobile_svr
            
        ## DMS
        dms_required = Product.Attr('DMS Desk Mounting Stations required').GetValue()
        dms_stations=['DMS Flex Station Qty 0_60','DMS Console Station Qty 0_20','DMS TPS Station Qty 0_20','DMS Console Station Extension Qty 0_15']
        dms_displays1 = int(Product.Attr('DMS No of Displays 0_4').GetValue()) if Product.Attr('DMS No of Displays 0_4').GetValue()!='' else 0
        dms_displays2 = int(Product.Attr('DMS No of Displays 0_4_2').GetValue()) if Product.Attr('DMS No of Displays 0_4_2').GetValue()!='' else 0
        dms_size = Product.Attr('DMS Display size').GetValue()
        dms_supplier = Product.Attr('DMS Display Supplier').GetValue()
        dms_touchscreen = Product.Attr('DMS Touch Screen required?').GetValue()
        dms_val = 0
        if dms_required != "No":
            if dms_size == "27 inch NTS NEC" and dms_supplier == "Honeywell" and (dms_displays1 > 0 or dms_displays2 > 0) and dms_touchscreen == "No Touch Screen":
                for i in dms_stations:
                    dms_val += int(Product.Attr(str(i)).GetValue()) if Product.Attr(str(i)).GetValue()!='' else 0
                if dms_displays1 > 0 :
                    val += dms_val * dms_displays1
                elif dms_displays2 > 0:
                    val += dms_val * dms_displays2
            elif dms_size == "21.33 inch NTS" and dms_supplier == "Honeywell" and (dms_displays1 > 0 or dms_displays2 > 0) and dms_touchscreen == "No Touch Screen":
                for i in dms_stations:
                    dms_val += int(Product.Attr(str(i)).GetValue()) if Product.Attr(str(i)).GetValue()!='' else 0
                if dms_displays1 > 0 :
                    val1 += dms_val * dms_displays1
                elif dms_displays2 > 0:
                    val1 += dms_val * dms_displays2
            elif dms_size == "21.33 inch Touch" and dms_supplier == "Honeywell" and (dms_displays1 > 0 or dms_displays2 > 0) and dms_touchscreen == "Touch Screen":
                for i in dms_stations:
                    dms_val += int(Product.Attr(str(i)).GetValue()) if Product.Attr(str(i)).GetValue()!='' else 0
                if dms_displays1 > 0 :
                    val2 += dms_val * dms_displays1
                elif dms_displays2 > 0:
                    val2 += dms_val * dms_displays2
        return int(val),int(val1),int(val2)
#CXCPQ-38883,CXCPQ-38879
def get_23(Product):
    if Product.Name == "Experion Enterprise Group":
        Redundancy=Product.Attr('Server Redundancy Requirement?').GetValue()
        Trace.Write(Redundancy)
        val = val2 = 0
        server_type = Product.Attr('Experion Server Type').GetValue()
        if server_type == "Flex Server":
            display_size_flex = Product.Attr('Display_Size_FlexServer').GetValue()
            touchscreen = Product.Attr('TouchScreen_FlexServerDesk').GetValue()
            display_Supplier_flex = Product.Attr('Display_Supplier').GetValue()
            Displays_2_flex = int(Product.Attr('Displays_Flex Server in Desk0_2_2').GetValue()) if Product.Attr('Displays_Flex Server in Desk0_2_2').GetValue()!='' else 0
            Displays_flex = int(Product.Attr('Displays_Flex Server in Desk0_2').GetValue()) if Product.Attr('Displays_Flex Server in Desk0_2').GetValue()!='' else 0
            if display_size_flex == "23 inch" and touchscreen == "Yes" and display_Supplier_flex == "Honeywell" :
                if Redundancy == "Redundant" and (Displays_flex > 0 or Displays_2_flex > 0):
                    val += 2 * Displays_flex
                    val +=  2 * Displays_2_flex
                elif Redundancy == "Non Redundant" and (Displays_flex > 0 or Displays_2_flex > 0):
                    val += Displays_flex
                    val += Displays_2_flex
            elif display_size_flex == "23 inch NTS" and touchscreen == "No" and display_Supplier_flex == "Honeywell" :
                if Redundancy == "Redundant" and (Displays_flex > 0 or Displays_2_flex > 0):
                    val2 += 2 * Displays_flex
                    val2 +=  2 * Displays_2_flex
                elif Redundancy == "Non Redundant" and (Displays_flex > 0 or Displays_2_flex > 0):
                    val2 += Displays_flex
                    val2 += Displays_2_flex
        ## ACE-APP node desk
        # Display Size
        size_list = ['Display Size _ACE_desk_pre','Display Size (ACE-T)','Display Size_EAPP']
        # Dispay Supplier
        supplier_list = ['Display Supplier (ACE)','Display Supplier (ACE-T)','Display Supplier_EAPP']
        # Input Question
        Node_list = ['ACE Node Tower Mount Desk','ACE_T_Node _Tower_Mount_Desk','Experion APP Node - Tower Mount']
        Display_list = ['Displays_ace_desk_pre','Displays (ACE-T)(0-1)','Displays_EAPP']

        for (i,j,k,l) in zip(size_list,supplier_list,Node_list,Display_list):
            size = Product.Attr(str(i)).GetValue()
            supplier = Product.Attr(str(j)).GetValue()
            node = int(Product.Attr(str(k)).GetValue()) if Product.Attr(str(k)).GetValue()!='' else 0
            if node > 0 and size == "23 inch" and supplier == "Honeywell":
                #val += node * int(Product.Attr(str(l)).GetValue()) if Product.Attr(str(l)).GetValue()!='' else 0
                val2 += node * int(Product.Attr(str(l)).GetValue()) if Product.Attr(str(l)).GetValue()!='' else 0
        
        ## SIM PC CALCULATION
        sim_val = 0
        sim_size = Product.Attr('Display Size (Sim PC)').GetValue()
        sim_supplier = Product.Attr('Display Supplier (Sim PC)').GetValue()
        qnt1=int(Product.Attr('SIM-ACE Licenses (0-7)').GetValue()) if Product.Attr('SIM-ACE Licenses (0-7)').GetValue()!='' else 0
        qnt2=int(Product.Attr('Sim-Cx00 PC Licenses (0-20)').GetValue()) if Product.Attr('Sim-Cx00 PC Licenses (0-20)').GetValue()!='' else 0
        qnt3=int(Product.Attr('SIM-FFD Licenses (0-125)').GetValue()) if Product.Attr('SIM-FFD Licenses (0-125)').GetValue()!='' else 0
        if sim_size == "23 inch" and sim_supplier == "Honeywell":
            sim_val=D.Ceiling((qnt1+D.Ceiling(0.4*qnt2)+D.Ceiling(0.1*qnt3))/4.0)
            #val+=sim_val
            val2+=sim_val
            Trace.Write("SIM: "+str(sim_val))

        ## Mobile Server Node
        mobile_svr = int(Product.Attr('Mobile Server Nodes (0-1)').GetValue()) if Product.Attr('Mobile Server Nodes (0-1)').GetValue()!='' else 0
        mobile_size = Product.Attr('Display Size (Mobile Server)').GetValue()
        mobile_supplier = Product.Attr('Display Supplier (Mobile Server)').GetValue()
        if mobile_svr > 0:
            if mobile_size == "23 inch" and mobile_supplier == "Honeywell":
                #val += mobile_svr
                val2 += mobile_svr
            
        ## DMS
        dms_required = Product.Attr('DMS Desk Mounting Stations required').GetValue()
        dms_stations=['DMS Flex Station Qty 0_60','DMS Console Station Qty 0_20','DMS TPS Station Qty 0_20','DMS Console Station Extension Qty 0_15']
        dms_displays1 = int(Product.Attr('DMS No of Displays 0_4').GetValue()) if Product.Attr('DMS No of Displays 0_4').GetValue()!='' else 0
        dms_displays2 = int(Product.Attr('DMS No of Displays 0_4_2').GetValue()) if Product.Attr('DMS No of Displays 0_4_2').GetValue()!='' else 0
        dms_size = Product.Attr('DMS Display size').GetValue()
        dms_supplier = Product.Attr('DMS Display Supplier').GetValue()
        dms_touchscreen = Product.Attr('DMS Touch Screen required?').GetValue()
        dms_val = 0
        if dms_required != "No":
            if dms_size == "23 inch" and dms_supplier == "Honeywell" and (dms_displays1 > 0 or dms_displays2 > 0) and dms_touchscreen == "Touch Screen":
                for i in dms_stations:
                    dms_val += int(Product.Attr(str(i)).GetValue()) if Product.Attr(str(i)).GetValue()!='' else 0
                if dms_displays1 > 0 :
                    val += dms_val * dms_displays1
                elif dms_displays2 > 0:
                    val += dms_val * dms_displays2
            elif dms_size == "23 inch NTS" and dms_supplier == "Honeywell" and (dms_displays1 > 0 or dms_displays2 > 0) and dms_touchscreen == "No Touch Screen":
                for i in dms_stations:
                    dms_val += int(Product.Attr(str(i)).GetValue()) if Product.Attr(str(i)).GetValue()!='' else 0
                if dms_displays1 > 0 :
                    val2 += dms_val * dms_displays1
                elif dms_displays2 > 0:
                    val2 += dms_val * dms_displays2

        ## Orion
        orion_required = Product.Attr('Orion Stations required').GetValue()
        orion_2Pos = int(Product.Attr('Orion Console 2Position Base Unit (0-20)').GetValue()) if Product.Attr('Orion Console 2Position Base Unit (0-20)').GetValue()!='' else 0
        orion_3Pos = int(Product.Attr('Orion Console 3Position Base Unit (0-20)').GetValue()) if Product.Attr('Orion Console 3Position Base Unit (0-20)').GetValue()!='' else 0
        orion_size = Product.Attr('Orion Console Display Size').GetValue()
        orion_supplier = Product.Attr('Orion Console Display Supplier').GetValue()
        orion_display = int(Product.Attr('Orion Console Display Devices (0-4)').GetValue()) if Product.Attr('Orion Console Display Devices (0-4)').GetValue()!='' else 0
        orion_val = 0
        if orion_required != "No":
            if orion_size == "23 inch NTS" and orion_supplier == "Honeywell":
                orion_val = (2 * orion_2Pos * orion_display) + (3 * orion_3Pos * orion_display)
                #val += orion_val
                val2 += orion_val
        return int(val),int(val2)
#CXCPQ-39069,CXCPQ-39114,CXCPQ-57394
def get_IKB(Product):
    if Product.Name == "Experion Enterprise Group":
        Redundancy=Product.Attr('Server Redundancy Requirement?').GetValue()
        Trace.Write(Redundancy)
        val = 0
        ikb_value = ['IKB w/o Trackball','IKB with Trackball','OEP','IKB non USB']
        server_type = Product.Attr('Experion Server Type').GetValue()
        if server_type == "Flex Server":
            NodeSupplier = Product.Attr('NodeSupplier_FlexServer').GetValue()
            svr_ikb = Product.Attr('IKBorOEP_FlexServer').GetValue()
            if svr_ikb in ikb_value and NodeSupplier == "Honeywell" :
                if Redundancy == "Redundant":
                    val += 2
                elif Redundancy == "Non Redundant":
                    val += 1

        ##CMS
        cms_required = Product.Attr('CMS Cabinet Mounting Stations required').GetValue()
        cms_stations=['CMS Flex Station Qty 0_60','CMS Console Station Qty 0_20','CMS TPS Station Qty 0_20','CMS Console Station Extension Qty 0_15']
        cms_node_supplier = Product.Attr('CMS Node Supplier').GetValue()
        cms_ikb = Product.Attr('Cabinet_IKB_or_OEP').GetValue()
        cms_val=0
        if cms_required != "No":
            if cms_ikb in ikb_value and cms_node_supplier == "Honeywell":
                for i in cms_stations:
                    cms_val += int(Product.Attr(str(i)).GetValue()) if Product.Attr(str(i)).GetValue()!='' else 0
                val +=cms_val


        ## DMS
        dms_required = Product.Attr('DMS Desk Mounting Stations required').GetValue()
        dms_stations=['DMS Flex Station Qty 0_60','DMS Console Station Qty 0_20','DMS TPS Station Qty 0_20','DMS Console Station Extension Qty 0_15']
        dms_node_supplier = Product.Attr('DMS Node Supplier').GetValue()
        dms_ikb = Product.Attr('DMS IKB or OEP').GetValue()
        dms_val = 0
        if dms_required != "No":
            if dms_ikb in ikb_value and dms_node_supplier == "Honeywell":
                for i in dms_stations:
                    dms_val += int(Product.Attr(str(i)).GetValue()) if Product.Attr(str(i)).GetValue()!='' else 0
                val += dms_val

        ## Orion
        orion_required = Product.Attr('Orion Stations required').GetValue()
        orion_2Pos = int(Product.Attr('Orion Console 2Position Base Unit (0-20)').GetValue()) if Product.Attr('Orion Console 2Position Base Unit (0-20)').GetValue()!='' else 0
        orion_3Pos = int(Product.Attr('Orion Console 3Position Base Unit (0-20)').GetValue()) if Product.Attr('Orion Console 3Position Base Unit (0-20)').GetValue()!='' else 0
        orion_ikb = Product.Attr('Orion Console Membrane KB Type').GetValue()
        orion_val = 0
        if orion_required != "No":
            if orion_ikb in ikb_value:
                orion_val = (2 * orion_2Pos) + (3 * orion_3Pos)
                val += orion_val
        return val

#CXCPQ-39206 + CXCPQ-45647
def get_license(Product):
    # Flex station
    flex_station = ['CMS Flex Station Qty 0_60','DMS Flex Station Qty 0_60','Flex Station Qty (0-60)','How many Experion Panel PCs required? 0_30','Additional Flex Station Licenses']
    #Experion node to be installed on each Panel PC
    exp_val = Product.Attr('Experion node to be installed on each Panel PC').GetValue()
    add_flex = int(Product.Attr('Additional Flex Station Licenses').GetValue()) if Product.Attr('Additional Flex Station Licenses').GetValue()!='' else 0
    qty = rem = 0
    qty_10 = qty_5 = qty_1 = 0
    
    # Flex calculation
    if exp_val != "Flex Station":
        Trace.Write("Not Flex!")
        if add_flex>0:
            qty = add_flex
            Trace.Write("ADD_FLEX: "+str(qty))
            if qty >= 10:
                qty_10 = qty//10
                rem = qty % 10
                if rem >= 5:
                    qty_5 = rem//5
                    rem = qty % 5
                    if rem > 0:
                        qty_1 = rem
                elif rem > 0:
                    qty_1 = rem
            elif qty >= 5:
                qty_5 = qty//5
                rem = qty % 5
                if rem > 0:
                    qty_1 = rem
            else:
                qty_1 = qty
            return qty_10,qty_5,qty_1
        else:
            return 0,0,0
    else:
        for i in flex_station:
            qty += int(Product.Attr(str(i)).GetValue()) if Product.Attr(str(i)).GetValue()!='' else 0
        Trace.Write("QT: "+str(qty))
        if qty == 0:
            return 0,0,0
        if qty >= 10:
            qty_10 = qty//10
            rem = qty % 10
            if rem >= 5:
                qty_5 = rem//5
                rem = qty % 5
                if rem > 0:
                    qty_1 = rem
            elif rem > 0:
                qty_1 = rem
        elif qty >= 5:
            qty_5 = qty//5
            rem = qty % 5
            if rem > 0:
                qty_1 = rem
        else:
            qty_1 = qty

        return qty_10,qty_5,qty_1
#CXCPQ-39210
def get_Console(Product):
    qty = rem = 0
    qty_10 = qty_5 = qty_1 = 0
    # Console Station
    console_station = ['CMS Console Station Qty 0_20','DMS Console Station Qty 0_20','Console Station Qty (0-20)']
    
    # Console calculation
    for i in console_station:
        qty += int(Product.Attr(str(i)).GetValue()) if Product.Attr(str(i)).GetValue()!='' else 0
    Trace.Write("QT: "+str(qty))
    if qty == 0:
        return 0,0,0
    if qty >= 10:
        qty_10 = qty//10
        rem = qty % 10
        if rem >= 5:
            qty_5 = rem//5
            rem = qty % 5
            if rem > 0:
                qty_1 = rem
        elif rem > 0:
            qty_1 = rem
    elif qty >= 5:
        qty_5 = qty//5
        rem = qty % 5
        if rem > 0:
            qty_1 = rem
    else:
        qty_1 = qty

    return qty_10,qty_5,qty_1
#CXCPQ-39211
def get_Ext(Product):
    qty = 0
    # Console Station Extension
    console_station_ext = ['CMS Console Station Extension Qty 0_15','DMS Console Station Extension Qty 0_15','Console Station Extension Qty  (0-15)']
    #Experion node to be installed on each Panel PC
    exp_val = Product.Attr('Experion node to be installed on each Panel PC').GetValue()
    exp_qty = int(Product.Attr('How many Experion Panel PCs required? 0_30').GetValue()) if Product.Attr('How many Experion Panel PCs required? 0_30').GetValue()!='' else 0
    # Console calculation
    if exp_val == "Console Extension":
        qty += exp_qty
        Trace.Write("exp_qty:"+str(qty))
    for i in console_station_ext:
        qty += int(Product.Attr(str(i)).GetValue()) if Product.Attr(str(i)).GetValue()!='' else 0
    return qty
#CXCPQ-41692,CXCPQ-41693,CXCPQ-41694,CXCPQ-41695
def get_Vals(Product):
    if Product.Name == "Experion Enterprise Group":
        Redundancy=Product.Attr('Server Redundancy Requirement?').GetValue()
        Trace.Write(Redundancy)
        val = val1 = val2 = val3 = 0
        #ikb_value = ['IKB w/o Trackball','IKB with Trackball','OEP','IKB non USB']
        server_type = Product.Attr('Experion Server Type').GetValue()
        if server_type == "Flex Server":
            NodeSupplier = Product.Attr('NodeSupplier_FlexServer').GetValue()
            svr_ikb = Product.Attr('IKBorOEP_FlexServer').GetValue()
            #CXCPQ-41692
            if svr_ikb == 'IKB w/o Trackball' and NodeSupplier == "Honeywell":
                if Redundancy == "Redundant":
                    val += 2
                elif Redundancy == "Non Redundant":
                    val += 1
            #CXCPQ-41693
            if svr_ikb == 'IKB with Trackball' and NodeSupplier == "Honeywell":
                if Redundancy == "Redundant":
                    val1 += 2
                elif Redundancy == "Non Redundant":
                    val1 += 1
            #CXCPQ-41694
            if svr_ikb == 'OEP' and NodeSupplier == "Honeywell":
                if Redundancy == "Redundant":
                    val2 += 2
                elif Redundancy == "Non Redundant":
                    val2 += 1
            #CXCPQ-41695
            if svr_ikb == 'IKB non USB' and NodeSupplier == "Honeywell":
                if Redundancy == "Redundant":
                    val3 += 2
                elif Redundancy == "Non Redundant":
                    val3 += 1
                    
        ## CMS
        cms_stations=['CMS Flex Station Qty 0_60','CMS Console Station Qty 0_20','CMS TPS Station Qty 0_20','CMS Console Station Extension Qty 0_15']
        cms_required = Product.Attr('CMS Cabinet Mounting Stations required').GetValue()
        cms_node_supplier = Product.Attr('CMS Node Supplier').GetValue()
        cms_ikb = Product.Attr('Cabinet_IKB_or_OEP').GetValue()
        cms_val=0
        if cms_required != "No":
            if cms_ikb == 'IKB w/o Trackball' and cms_node_supplier == "Honeywell":
                for i in cms_stations:
                    cms_val += int(Product.Attr(str(i)).GetValue()) if Product.Attr(str(i)).GetValue()!='' else 0
                val+=cms_val
            if cms_ikb == 'IKB with Trackball' and cms_node_supplier == "Honeywell":
                for i in cms_stations:
                    cms_val += int(Product.Attr(str(i)).GetValue()) if Product.Attr(str(i)).GetValue()!='' else 0
                val1+=cms_val
            if cms_ikb == 'OEP' and cms_node_supplier == "Honeywell":
                for i in cms_stations:
                    cms_val += int(Product.Attr(str(i)).GetValue()) if Product.Attr(str(i)).GetValue()!='' else 0
                val2+=cms_val
            if cms_ikb == 'IKB non USB' and cms_node_supplier == "Honeywell":
                for i in cms_stations:
                    cms_val += int(Product.Attr(str(i)).GetValue()) if Product.Attr(str(i)).GetValue()!='' else 0
                val3+=cms_val
        ## DMS
        dms_required = Product.Attr('DMS Desk Mounting Stations required').GetValue()
        dms_stations=['DMS Flex Station Qty 0_60','DMS Console Station Qty 0_20','DMS TPS Station Qty 0_20','DMS Console Station Extension Qty 0_15']
        dms_node_supplier = Product.Attr('DMS Node Supplier').GetValue()
        dms_ikb = Product.Attr('DMS IKB or OEP').GetValue()
        dms_val = 0
        if dms_required != "No":
            #CXCPQ-41692, 
            if dms_ikb == 'IKB w/o Trackball' and dms_node_supplier == "Honeywell":
                for i in dms_stations:
                    dms_val += int(Product.Attr(str(i)).GetValue()) if Product.Attr(str(i)).GetValue()!='' else 0
                val += dms_val
            #CXCPQ-41693
            if dms_ikb == 'IKB with Trackball' and dms_node_supplier == "Honeywell":
                for i in dms_stations:
                    dms_val += int(Product.Attr(str(i)).GetValue()) if Product.Attr(str(i)).GetValue()!='' else 0
                val1 += dms_val
            #CXCPQ-41694
            if dms_ikb == 'OEP' and dms_node_supplier == "Honeywell":
                for i in dms_stations:
                    dms_val += int(Product.Attr(str(i)).GetValue()) if Product.Attr(str(i)).GetValue()!='' else 0
                val2 += dms_val
            #CXCPQ-41695
            if dms_ikb == 'IKB non USB' and dms_node_supplier == "Honeywell":
                for i in dms_stations:
                    dms_val += int(Product.Attr(str(i)).GetValue()) if Product.Attr(str(i)).GetValue()!='' else 0
                val3 += dms_val

        ## Orion
        orion_required = Product.Attr('Orion Stations required').GetValue()
        orion_2Pos = int(Product.Attr('Orion Console 2Position Base Unit (0-20)').GetValue()) if Product.Attr('Orion Console 2Position Base Unit (0-20)').GetValue()!='' else 0
        orion_3Pos = int(Product.Attr('Orion Console 3Position Base Unit (0-20)').GetValue()) if Product.Attr('Orion Console 3Position Base Unit (0-20)').GetValue()!='' else 0
        orion_ikb = Product.Attr('Orion Console Membrane KB Type').GetValue()
        orion_node = Product.Attr('Node Supplier').GetValue()
        orion_val = 0
        if orion_required != "No":
            #CXCPQ-41692
            if orion_ikb == 'IKB w/o Trackball' and orion_node == "Honeywell":
                orion_val = (2 * orion_2Pos) + (3 * orion_3Pos)
                val += orion_val
            #CXCPQ-41693
            if orion_ikb == 'IKB with Trackball' and orion_node == "Honeywell":
                orion_val = (2 * orion_2Pos) + (3 * orion_3Pos)
                val1 += orion_val
            #CXCPQ-41694
            if orion_ikb == 'OEP' and orion_node == "Honeywell":
                orion_val = (2 * orion_2Pos) + (3 * orion_3Pos)
                val2 += orion_val
            #CXCPQ-41695
            if orion_ikb == 'IKB non USB' and orion_node == "Honeywell":
                orion_val = (2 * orion_2Pos) + (3 * orion_3Pos)
                val3 += orion_val

    return val,val1,val2,val3

#CXCPQ-44532
def count_occurs(qty, qty_count):
    count = 0
    for q in qty:
        if q == qty_count:
            count += 1
    return count


def get_QVCS(Product):
    qvcs = Product.Attr('QVCS Support').GetValue()
    qty = int(Product.Attr('Experion Process Points (0 - 45000)').GetValue()) if Product.Attr('Experion Process Points (0 - 45000)').GetValue()!='' else 0
    qty_10k = qty_5k = qty_2k = qty_1k = qty_100 = 0
    qty_dict = {}
    Trace.Write("EXperion process: "+str(qty))
    buff_token = []
    tokens = [10000,5000,2000,1000,100]
    
    if qty%100!=0:
        qty = ((qty//100)+1)*100
    Trace.Write("QTY:"+str(qty))
    # QVCS Calcs
    if qvcs != "Yes":
        return qty_10k, qty_5k, qty_2k, qty_1k, qty_100
    else:
        for i in tokens:
            while (qty>=i):
                qty -= i
                buff_token.append(i)

        for i in tokens:
            Final_qty = count_occurs(buff_token,i)
            qty_dict[i]=Final_qty
        for k in qty_dict:
            Trace.Write(qty_dict[k])
            if str(k) == "10000":
                qty_10k = qty_dict[k]
            elif str(k) == "5000":
                qty_5k = qty_dict[k]
            elif str(k) == "2000":
                qty_2k = qty_dict[k]
            elif str(k) == "1000":
                qty_1k = qty_dict[k]
            elif str(k) == "100":
                qty_100 = qty_dict[k]
        return qty_10k, qty_5k, qty_2k, qty_1k, qty_100