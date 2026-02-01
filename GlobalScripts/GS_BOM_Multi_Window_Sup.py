def Node_station(Product):
    Redundancy=""
    qty = 0
    if Product.Name == "Experion Enterprise Group":
        Redundancy=Product.Attr('Server Redundancy Requirement?').GetValue()
        Trace.Write(Redundancy)
        ##Rack Mount Flex Server
        mw_rack = Product.Attr('Multi Window Support (Flex Server)').GetValue()
        if Redundancy=="Redundant" and mw_rack == "Yes":
            qty += 2
        elif Redundancy=="Non Redundant" and mw_rack == "Yes":
            qty += 1
        ##Desk Mount Flex Server
        mw_desk = Product.Attr('Multi_WindowSupportFlex_Server').GetValue()
        if Redundancy=="Redundant" and mw_desk == "Yes":
            qty += 2
        elif Redundancy=="Non Redundant" and mw_desk == "Yes":
            qty += 1    
        ##cabinet
        displays =int(Product.Attr('Cabinet_No_of_Displays (0-4)').GetValue()) if (Product.Attr('Cabinet_No_of_Displays (0-4)').GetValue()) != "" else 0
        cab_flex = int(Product.Attr('CMS Flex Station Qty 0_60').GetValue()) if (Product.Attr('CMS Flex Station Qty 0_60').GetValue()) != "" else 0
        cab_tps = int(Product.Attr('CMS TPS Station Qty 0_20').GetValue()) if (Product.Attr('CMS TPS Station Qty 0_20').GetValue()) != "" else 0
        cab_mw = Product.Attr('CMS Multi Window Support Option Required?').GetValue()
        if (displays>1 or cab_mw == "Yes") and ((cab_flex > 0) or(cab_tps > 0)):
            qty += cab_flex
            qty += cab_tps
        ##Desk
        DMS_display = int(Product.Attr('DMS No of Displays 0_4').GetValue()) if (Product.Attr('DMS No of Displays 0_4').GetValue()) != "" else 0
        desk_flex = int(Product.Attr('DMS Flex Station Qty 0_60').GetValue()) if (Product.Attr('DMS Flex Station Qty 0_60').GetValue()) != "" else 0
        desk_tps = int(Product.Attr('DMS TPS Station Qty 0_20').GetValue()) if (Product.Attr('DMS TPS Station Qty 0_20').GetValue()) != "" else 0
        desk_mw = Product.Attr('DMS Multi Window Support Option Required?').GetValue()
        if (DMS_display>1 or desk_mw == "Yes") and ((desk_flex > 0) or(desk_tps > 0)):
            qty += desk_flex
            qty += desk_tps
        ##orion
        orion_flex = int(Product.Attr('Flex Station Qty (0-60)').GetValue()) if (Product.Attr('Flex Station Qty (0-60)').GetValue()) != "" else 0
        orion_tps = int(Product.Attr('TPS Station Qty (0-20)').GetValue()) if (Product.Attr('TPS Station Qty (0-20)').GetValue()) != "" else 0
        orion_mw = Product.Attr('Multi-Window Support Option Required?').GetValue()
        if orion_mw == "Yes" and ((orion_flex > 0) or(orion_tps > 0)):
            qty += orion_flex
            qty += orion_tps      
    return qty
#test = Node_station(Product)
#Trace.Write("Qty: "+str(test))