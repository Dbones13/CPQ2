if Product.Attr('PERF_ExecuteScripts').GetValue() != '':
    import GS_PS_Exp_Ent_BOM

    ABCC = int(Product.Attr('Additional Backup Control Center Server Location').GetValue())

    if ABCC == 0:
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","EP-RBCC01", 0)
    else:
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","EP-RBCC01", ABCC)

        #Additional quantity for SQL License
        GS_PS_Exp_Ent_BOM.addAtvQty(Product,"Exp_Ent_Grp_Part_Summary","MZ-SQLCL4", 2*ABCC)

        #Additional quantity for Server Node
        server_mount = Product.Attr('Server Mounting').GetValue()
        if server_mount == 'Desk':
            node_supplier = Product.Attr('Node Supplier_server').GetValue()
            TPM = Product.Attr('Trusted Platform Module1').GetValue()
            node_type = Product.Attr('Server Node Type_desk').GetValue()
        elif server_mount == 'Cabinet':
            node_supplier = Product.Attr('Node_Supplier_Server').GetValue()
            TPM = Product.Attr('TrustedPlatformModule_TPM').GetValue()
            node_type = Product.Attr('Server_NodeType').GetValue()

        if node_supplier == 'Honeywell':
            if node_type == 'SVR_STD_DELL_Tower_RAID1':
                GS_PS_Exp_Ent_BOM.addAtvQty(Product,'Exp_Ent_Grp_Part_Summary','MZ-PCST03', 2*ABCC)
            if node_type == 'SVR_PER_DELL_Tower_RAID1':
                GS_PS_Exp_Ent_BOM.addAtvQty(Product,'Exp_Ent_Grp_Part_Summary','MZ-PCST04', 2*ABCC)
            if node_type == 'SVR_STD_DELL_Rack_RAID1':
                GS_PS_Exp_Ent_BOM.addAtvQty(Product,'Exp_Ent_Grp_Part_Summary','MZ-PCSR05', 2*ABCC)
            if node_type == 'SVR_PER_DELL_Rack_RAID1':
                GS_PS_Exp_Ent_BOM.addAtvQty(Product,'Exp_Ent_Grp_Part_Summary','MZ-PCSR06', 2*ABCC)
            if node_type == 'SVR_PER_DELL_Rack_RAID1_RUG' and TPM == 'Yes':
                GS_PS_Exp_Ent_BOM.addAtvQty(Product,'Exp_Ent_Grp_Part_Summary','MZ-PCIS02', 2*ABCC)
            if node_type == 'SVR_PER_DELL_Rack_RAID1_XE' and TPM == 'Yes':
                GS_PS_Exp_Ent_BOM.addAtvQty(Product,'Exp_Ent_Grp_Part_Summary','MZ-PCSR03', 2*ABCC)
            if node_type == 'SVR_PER_DELL_Rack_RAID5' and TPM == 'Yes':
                GS_PS_Exp_Ent_BOM.addAtvQty(Product,'Exp_Ent_Grp_Part_Summary','MZ-PCSR04', 2*ABCC)
            if node_type == 'SVR_PER_HP_Rack_RAID5':
                GS_PS_Exp_Ent_BOM.addAtvQty(Product,'Exp_Ent_Grp_Part_Summary','MZ-PCSV85', 2*ABCC)

        #Additional quantity for OS License
        soft_release = Product.Attr('Experion Software Release').GetValue()
        if soft_release == 'R530':
            GS_PS_Exp_Ent_BOM.addAtvQty(Product,'Exp_Ent_Grp_Part_Summary','EP-COAS22', 2*ABCC)
        elif soft_release == 'R520':
            GS_PS_Exp_Ent_BOM.addAtvQty(Product,'Exp_Ent_Grp_Part_Summary','EP-COAS19', 2*ABCC)

        #Additonal quantity for Display
        display = int(Product.Attr('Displays_server01').GetValue())
        display_supplier = Product.Attr('Display Supplier_Server').GetValue()
        if server_mount == 'Desk' and display == 1 and display_supplier == 'Honeywell':
            display_size = Product.Attr('Display Size_server').GetValue()
            if display_size == '21.33 inch NTS':
                voltage = Product.Attr('CE_Site_Voltage').GetValue()
                if voltage == '120V':
                    GS_PS_Exp_Ent_BOM.addAtvQty(Product,'Exp_Ent_Grp_Part_Summary','TP-FPD211-100', 2*ABCC)
                elif voltage == '240V':
                    GS_PS_Exp_Ent_BOM.addAtvQty(Product,'Exp_Ent_Grp_Part_Summary','TP-FPD211-200', 2*ABCC)
            if display_size == '24 inch NTS NEC':
                GS_PS_Exp_Ent_BOM.addAtvQty(Product,'Exp_Ent_Grp_Part_Summary','TP-FPW241', 2*ABCC)
            if display_size == '24 inch NTS DELL':
                GS_PS_Exp_Ent_BOM.addAtvQty(Product,'Exp_Ent_Grp_Part_Summary','TP-FPW242', 2*ABCC)
            if display_size == '27 inch NTS NEC':
                GS_PS_Exp_Ent_BOM.addAtvQty(Product,'Exp_Ent_Grp_Part_Summary','TP-FPW271', 2*ABCC)
            if display_size == '27 inch NTS DELL':
                GS_PS_Exp_Ent_BOM.addAtvQty(Product,'Exp_Ent_Grp_Part_Summary','TP-FPW272', 2*ABCC)
    qtySQLCL4=Product.AttrValue('Exp_Ent_Grp_Part_Summary', 'MZ-SQLCL4').Quantity
    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","CF-CTD001", qtySQLCL4)