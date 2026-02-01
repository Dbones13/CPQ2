tabs = [tab.Name for tab in Product.Tabs if tab.IsSelected]
if ('Part Summary' in tabs):
    import GS_RTU_ReadAttrs
    import GS_RTU_Software_Calcs
    import GS_RTU_Part_Update
    import GS_RTU_Replica_Config
    Trace.Write("PS_RTU_Part_Summary")
    try:
        attrs = GS_RTU_ReadAttrs.AttrStorage(Product)
    except Exception,e:
        attrs = None
        Product.ErrorMessages.Add("Error when Reading RTU System Attributes: " + str(e))
    parts_dict = {}

    if attrs or attrs is not None:
        try:
            parts_dict = GS_RTU_Software_Calcs.calc_software_rtu_system(attrs, parts_dict)
        except Exception,e:
            Product.ErrorMessages.Add("Error in GS_RTU_Software_Calcs: " + str(e))
        '''try:
            parts_dict = GS_RTU_Replica_Config.multiply_replica_config(Product, parts_dict)
        except Exception,e:
            Product.ErrorMessages.Add("Error in GS_RTU_Replica_Config: " + str(e))'''

        Trace.Write("debugging: " + str(parts_dict))
        GS_RTU_Part_Update.execute(Product, 'RTU_PartSummary_Cont', parts_dict)