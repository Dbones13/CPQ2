import System.Decimal as D
#CXCPQ-38872
def get_55(Product):
    if Product.Name == "Experion Enterprise Group":
        Redundancy=Product.Attr('Server Redundancy Requirement?').GetValue()
        Trace.Write(Redundancy)
        val = 0
        server_type = Product.Attr('Experion Server Type').GetValue()
        if server_type == "Flex Server":
            display_size_flex = Product.Attr('Display_Size_FlexServer').GetValue()
            touchscreen = Product.Attr('TouchScreen_FlexServerDesk').GetValue()
            display_Supplier_flex = Product.Attr('Display_Supplier').GetValue()
            Displays_2_flex = int(Product.Attr('Displays_Flex Server in Desk0_2_2').GetValue()) if Product.Attr('Displays_Flex Server in Desk0_2_2').GetValue()!='' else 0
            Displays_flex = int(Product.Attr('Displays_Flex Server in Desk0_2').GetValue()) if Product.Attr('Displays_Flex Server in Desk0_2').GetValue()!='' else 0
            if display_size_flex == "55 inch NTS" and touchscreen == "No" and display_Supplier_flex == "Honeywell" :
                if Redundancy == "Redundant" and (Displays_flex > 0 or Displays_2_flex > 0):
                    val += 2 * Displays_flex
                    val +=  2 * Displays_2_flex
                elif Redundancy == "Non Redundant" and (Displays_flex > 0 or Displays_2_flex > 0):
                    val += Displays_flex
                    val += Displays_2_flex
                    
        ## CMS
        cms_stations=['CMS Flex Station Qty 0_60','CMS Console Station Qty 0_20','CMS TPS Station Qty 0_20','CMS Console Station Extension Qty 0_15']
        cms_required = Product.Attr('CMS Cabinet Mounting Stations required').GetValue()
        cms_size = Product.Attr('Cabinet_Display_size').GetValue()
        cms_supplier = Product.Attr('Cabinet_Display_Supplier').GetValue()
        cms_touchscreen = Product.Attr('Cabinet_Touch_Screen_required').GetValue()
        cms_displays = int(Product.Attr('Cabinet_No_of_Displays (0-4)').GetValue()) if Product.Attr('Cabinet_No_of_Displays (0-4)').GetValue()!='' else 0
        cms_val=0
        
        if cms_required != "No":
            if cms_size == "55 inch NTS" and cms_supplier == "Honeywell" and cms_displays > 0 and cms_touchscreen == "No Touch Screen":
                for i in cms_stations:
                    cms_val += int(Product.Attr(str(i)).GetValue()) if Product.Attr(str(i)).GetValue()!='' else 0
                if cms_displays > 0 :
                    val += cms_val * cms_displays

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
            if dms_size == "55 inch NTS" and dms_supplier == "Honeywell" and (dms_displays1 > 0 or dms_displays2 > 0) and dms_touchscreen == "No Touch Screen":
                for i in dms_stations:
                    dms_val += int(Product.Attr(str(i)).GetValue()) if Product.Attr(str(i)).GetValue()!='' else 0
                if dms_displays1 > 0 :
                    val += dms_val * dms_displays1
                elif dms_displays2 > 0:
                    val += dms_val * dms_displays2

        ## Orion
        orion_required = Product.Attr('Orion Stations required').GetValue()
        orion_2Pos = int(Product.Attr('Orion Console 2Position Base Unit (0-20)').GetValue()) if Product.Attr('Orion Console 2Position Base Unit (0-20)').GetValue()!='' else 0
        orion_3Pos = int(Product.Attr('Orion Console 3Position Base Unit (0-20)').GetValue()) if Product.Attr('Orion Console 3Position Base Unit (0-20)').GetValue()!='' else 0
        orion_size = Product.Attr('Orion Console Display Size').GetValue()
        orion_supplier = Product.Attr('Orion Console Display Supplier').GetValue()
        orion_val = 0
        if orion_required != "No":
            if orion_size == "55 inch NTS" and orion_supplier == "Honeywell":
                orion_val = (2 * orion_2Pos) + (3 * orion_3Pos)
                val += orion_val

        return val
#CXCPQ-38880,(CXCPQ-38876,CXCPQ-38875),CXCPQ-38882
def get_parts(Product,displaysize):
    if Product.Name == "Experion Enterprise Group":
        Redundancy=Product.Attr('Server Redundancy Requirement?').GetValue()
        Trace.Write(Redundancy)
        val = val1 = val2 = 0
        server_type = Product.Attr('Experion Server Type').GetValue()
        if server_type == "Server" or server_type == "Server TPS":
            display_size = Product.Attr('Display Size_server').GetValue()
            display_Supplier = Product.Attr('Display Supplier_Server').GetValue()
            Displays = int(Product.Attr('Displays_server01').GetValue()) if Product.Attr('Displays_server01').GetValue()!='' else 0
            if display_size == displaysize and display_Supplier == "Honeywell" and Displays > 0 :
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
            if display_size_flex == displaysize and touchscreen == "No" and display_Supplier_flex == "Honeywell" :
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
            if node > 0 and size == displaysize and supplier == "Honeywell":
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
        if sim_size == displaysize and sim_supplier == "Honeywell":
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
            if mobile_size == displaysize and mobile_supplier == "Honeywell":
                val += mobile_svr 
            elif mobile_size == "21.33 inch NTS" and mobile_supplier == "Honeywell":
                val1 += mobile_svr
                #val2 += mobile_svr
        ## CMS
        cms_stations=['CMS Flex Station Qty 0_60','CMS Console Station Qty 0_20','CMS TPS Station Qty 0_20','CMS Console Station Extension Qty 0_15']
        cms_required = Product.Attr('CMS Cabinet Mounting Stations required').GetValue()
        cms_size = Product.Attr('Cabinet_Display_size').GetValue()
        cms_supplier = Product.Attr('Cabinet_Display_Supplier').GetValue()
        cms_touchscreen = Product.Attr('Cabinet_Touch_Screen_required').GetValue()
        cms_displays = int(Product.Attr('Cabinet_No_of_Displays (0-4)').GetValue()) if Product.Attr('Cabinet_No_of_Displays (0-4)').GetValue()!='' else 0
        cms_val=0
        if cms_required != "No":
            if cms_size == displaysize and cms_supplier == "Honeywell" and cms_displays > 0 and cms_touchscreen == "No Touch Screen":
                for i in cms_stations:
                    cms_val += int(Product.Attr(str(i)).GetValue()) if Product.Attr(str(i)).GetValue()!='' else 0
                if cms_displays > 0 :
                    val += cms_val * cms_displays
            elif cms_size == "21.33 inch NTS" and cms_supplier == "Honeywell" and cms_displays > 0 and cms_touchscreen == "No Touch Screen":
                for i in cms_stations:
                    cms_val += int(Product.Attr(str(i)).GetValue()) if Product.Attr(str(i)).GetValue()!='' else 0
                if cms_displays > 0 :
                    val1 += cms_val * cms_displays
            elif cms_size == "21.33 inch Touch" and cms_supplier == "Honeywell" and cms_displays > 0 and cms_touchscreen == "Touch Screen":
                for i in cms_stations:
                    cms_val += int(Product.Attr(str(i)).GetValue()) if Product.Attr(str(i)).GetValue()!='' else 0
                if cms_displays:
                    val2 += cms_val * cms_displays
            
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
            if dms_size == displaysize and dms_supplier == "Honeywell" and (dms_displays1 > 0 or dms_displays2 > 0) and dms_touchscreen == "No Touch Screen":
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
#CXCPQ-38883,CXCPQ-38879,CXCPQ-57394
def get_23(Product,displaysize):
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
            if display_size_flex == displaysize and touchscreen == "Yes" and display_Supplier_flex == "Honeywell" :
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
        ## CMS
        cms_stations=['CMS Flex Station Qty 0_60','CMS Console Station Qty 0_20','CMS TPS Station Qty 0_20','CMS Console Station Extension Qty 0_15']
        cms_required = Product.Attr('CMS Cabinet Mounting Stations required').GetValue()
        cms_size = Product.Attr('Cabinet_Display_size').GetValue()
        cms_supplier = Product.Attr('Cabinet_Display_Supplier').GetValue()
        cms_touchscreen = Product.Attr('Cabinet_Touch_Screen_required').GetValue()
        cms_displays = int(Product.Attr('Cabinet_No_of_Displays (0-4)').GetValue()) if Product.Attr('Cabinet_No_of_Displays (0-4)').GetValue()!='' else 0
        cms_val=0
        if cms_required != "No":
            if cms_size == displaysize and cms_supplier == "Honeywell" and cms_displays > 0 and cms_touchscreen == "Touch Screen":
                for i in cms_stations:
                    cms_val += int(Product.Attr(str(i)).GetValue()) if Product.Attr(str(i)).GetValue()!='' else 0
                if cms_displays > 0 :
                    val += cms_val * cms_displays
            elif cms_size == "23 inch NTS" and cms_supplier == "Honeywell" and cms_displays > 0 and cms_touchscreen == "No Touch Screen":
                for i in cms_stations:
                    cms_val += int(Product.Attr(str(i)).GetValue()) if Product.Attr(str(i)).GetValue()!='' else 0
                if cms_displays > 0 :
                    val2 += cms_val * cms_displays
        
            
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
            if dms_size == displaysize and dms_supplier == "Honeywell" and (dms_displays1 > 0 or dms_displays2 > 0) and dms_touchscreen == "Touch Screen":
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
            #CXCPQ-41692 
            if cms_ikb == 'IKB w/o Trackball' and cms_node_supplier == "Honeywell":
                for i in cms_stations:
                    cms_val += int(Product.Attr(str(i)).GetValue()) if Product.Attr(str(i)).GetValue()!='' else 0
                val += cms_val
            #CXCPQ-41693
            if cms_ikb == 'IKB with Trackball' and cms_node_supplier == "Honeywell":
                for i in cms_stations:
                    cms_val += int(Product.Attr(str(i)).GetValue()) if Product.Attr(str(i)).GetValue()!='' else 0
                val1 += cms_val
            #CXCPQ-41694
            if cms_ikb == 'OEP' and cms_node_supplier == "Honeywell":
                for i in cms_stations:
                    cms_val += int(Product.Attr(str(i)).GetValue()) if Product.Attr(str(i)).GetValue()!='' else 0
                val2 += cms_val
            #CXCPQ-41695
            if cms_ikb == 'IKB non USB' and cms_node_supplier == "Honeywell":
                for i in cms_stations:
                    cms_val += int(Product.Attr(str(i)).GetValue()) if Product.Attr(str(i)).GetValue()!='' else 0
                val3 += cms_val

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
            #CXCPQ-41692, 38911
            if orion_ikb == 'IKB w/o Trackball' and orion_node == "Honeywell":
                orion_val = (2 * orion_2Pos) + (3 * orion_3Pos)
                val += orion_val
            #CXCPQ-41693, 38912
            if orion_ikb == 'IKB with Trackball' and orion_node == "Honeywell":
                orion_val = (2 * orion_2Pos) + (3 * orion_3Pos)
                val1 += orion_val
            #CXCPQ-41694, 38913
            if orion_ikb == 'OEP' and orion_node == "Honeywell":
                orion_val = (2 * orion_2Pos) + (3 * orion_3Pos)
                val2 += orion_val
            #CXCPQ-41695, 38914
            if orion_ikb == 'IKB non USB' and orion_node == "Honeywell":
                orion_val = (2 * orion_2Pos) + (3 * orion_3Pos)
                val3 += orion_val

    return val,val1,val2,val3
#CXCPQ-50181
def get_QUAD13(Product):
    HWD = 'STN_PER_DELL_Rack_RAID1'
    RPS = ["Extio3-Single Mode Fiber","Extio3-Multi Mode Fiber"]
    #station Question
    cms_hw=['CMS Flex Station Hardware Selection','CMS Console Station Hardware Selection','CMS TPS Station Hardware Selection','CMS Console Station Extension Hardware Selection']
    dms_hw=['DMS Flex Station Hardware Selection','DMS Console Station Hardware Selection','DMS TPS Station Hardware Selection','DMS Console Station Extension Hardware Selection']
    orion_hw = ['Flex Station Hardware Selection TPS','Console Station Hardware Selection','TPS Station Hardware Selection','Console Station Extension Hardware Selection']
    # Required
    cms_required = Product.Attr('CMS Cabinet Mounting Stations required').GetValue()
    dms_required = Product.Attr('DMS Desk Mounting Stations required').GetValue()
    orion_required = Product.Attr('Orion Stations required').GetValue()
    #station Question Quantity mapping
    cms_station=['CMS Flex Station Qty 0_60','CMS Console Station Qty 0_20','CMS TPS Station Qty 0_20','CMS Console Station Extension Qty 0_15']
    dms_station=['DMS Flex Station Qty 0_60','DMS Console Station Qty 0_20','DMS TPS Station Qty 0_20','DMS Console Station Extension Qty 0_15']
    orion_station = ['Flex Station Qty (0-60)','Console Station Qty (0-20)','TPS Station Qty (0-20)','Console Station Extension Qty  (0-15)']
    # Remote Peripheral Solution Type
    cms_RPS = Product.Attr('CMS Remote Peripheral Solution Type RPS').GetValue()
    dms_RPS = Product.Attr('DMS Remote Peripheral Solution Type RPS').GetValue()
    orion_RPS = Product.Attr('Orion Console Remote Periph Sol Type (RPS)').GetValue()

    cms_qty = dms_qty = orion_qty = 0
    qty = 0
    ##CMS
    if cms_required != "No" and cms_RPS in RPS:
        for h,s in zip(cms_hw,cms_station):
            hwd_val = Product.Attr(str(h)).GetValue()
            if hwd_val == HWD:
                cms_qty += int(Product.Attr(str(s)).GetValue()) if Product.Attr(str(s)).GetValue()!='' else 0
    ##DMS
    if dms_required != "No" and dms_RPS in RPS:
        for h,s in zip(dms_hw,dms_station):
            hwd_val = Product.Attr(str(h)).GetValue()
            if hwd_val == HWD:
                dms_qty += int(Product.Attr(str(s)).GetValue()) if Product.Attr(str(s)).GetValue()!='' else 0
    ##ORION
    if orion_required != "No" and orion_RPS in RPS:
        for h,s in zip(orion_hw,orion_station):
            hwd_val = Product.Attr(str(h)).GetValue()
            if hwd_val == HWD:
                orion_qty += int(Product.Attr(str(s)).GetValue()) if Product.Attr(str(s)).GetValue()!='' else 0
                
    qty = cms_qty + dms_qty + orion_qty
    return qty
#CXCPQ-49966
def get_555(Product):
    if Product.Name == "Experion Enterprise Group":
        # Rack-Desk-flex-TPS
        server_type = Product.Attr('Experion Server Type').GetValue()
        Redundancy=Product.Attr('Server Redundancy Requirement?').GetValue()
        Trace.Write(Redundancy)
        val = 0
        servers = ["Server","Flex Server","Server TPS"]
        if server_type in servers:
            if Redundancy == "Redundant":
                val += 2
            elif Redundancy == "Non Redundant":
                val += 1
        ## CMS
        cms_stations=['CMS Flex Station Qty 0_60','CMS Console Station Qty 0_20','CMS TPS Station Qty 0_20','CMS Console Station Extension Qty 0_15']
        cms_required = Product.Attr('CMS Cabinet Mounting Stations required').GetValue()
        cms_val=0
        if cms_required != "No":
            for i in cms_stations:
                cms_val += int(Product.Attr(str(i)).GetValue()) if Product.Attr(str(i)).GetValue()!='' else 0
        val+=cms_val
        Trace.Write("cms_val:"+str(cms_val))
        ## DMS
        dms_required = Product.Attr('DMS Desk Mounting Stations required').GetValue()
        dms_stations=['DMS Flex Station Qty 0_60','DMS Console Station Qty 0_20','DMS TPS Station Qty 0_20','DMS Console Station Extension Qty 0_15']
        dms_val = 0
        if dms_required != "No":
            for i in dms_stations:
                dms_val += int(Product.Attr(str(i)).GetValue()) if Product.Attr(str(i)).GetValue()!='' else 0
        val+=dms_val
        Trace.Write("dms_val:"+str(dms_val))
        ## ACE-APP node desk
        '''Node_list = ['ACE Node Tower Mount Desk','ACE_T_Node _Tower_Mount_Desk','Experion APP Node - Tower Mount']
        Display_list = ['Displays_ace_desk_pre','Displays (ACE-T)(0-1)','Displays_EAPP']
        ace=0
        for i,j in zip(Node_list,Display_list):
            node = int(Product.Attr(str(i)).GetValue()) if Product.Attr(str(i)).GetValue()!='' else 0
            if node > 0:
                ace += int(Product.Attr(str(j)).GetValue()) if Product.Attr(str(j)).GetValue()!='' else 0
        Trace.Write("ace:"+str(ace))'''
        Node_list = ['ACE Node Tower Mount Desk','ACE_T_Node _Tower_Mount_Desk','Experion APP Node - Tower Mount']
        ace=0
        for i in Node_list:
            ace += int(Product.Attr(str(i)).GetValue()) if Product.Attr(str(i)).GetValue()!='' else 0
        val+=ace
        Trace.Write("ace:"+str(ace))
        ## SIM PC CALCULATION
        sim_val = 0
        qnt1=int(Product.Attr('SIM-ACE Licenses (0-7)').GetValue()) if Product.Attr('SIM-ACE Licenses (0-7)').GetValue()!='' else 0
        qnt2=int(Product.Attr('Sim-Cx00 PC Licenses (0-20)').GetValue()) if Product.Attr('Sim-Cx00 PC Licenses (0-20)').GetValue()!='' else 0
        qnt3=int(Product.Attr('SIM-FFD Licenses (0-125)').GetValue()) if Product.Attr('SIM-FFD Licenses (0-125)').GetValue()!='' else 0
        sim_val=D.Ceiling((qnt1+D.Ceiling(0.4*qnt2)+D.Ceiling(0.1*qnt3))/4.0)
        val+=sim_val
        Trace.Write("sim_val:"+str(sim_val))
        ## Additional
        val+=int(Product.Attr('Additional Servers').GetValue()) if Product.Attr('Additional Servers').GetValue()!='' else 0

    return val