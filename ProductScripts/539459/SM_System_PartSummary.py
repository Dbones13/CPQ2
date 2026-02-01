tabs = [tab.Name for tab in Product.Tabs if tab.IsSelected]
if 'Part Summary' in tabs:
    import GS_SM_Part_Update
    import GS_SM_System_PartSumary_Calcs
    import GS_SM_Hardware_Safety_Parts
    '''try:
        attrs = GS_RTU_ReadAttrs.AttrStorage(Product)
    except Exception,e:
        attrs = None
        Product.ErrorMessages.Add("Error when Reading RTU System Attributes: " + str(e) + " Line Number: " + str(sys.exc_traceback.tb_next.tb_lineno))
        Trace.Write("Error when Reading RTU System Attributes: " + str(e) + " Line Number: " + str(sys.exc_traceback.tb_next.tb_lineno))'''
    parts_dict = {}

    try:
        parts_dict = GS_SM_System_PartSumary_Calcs.get_System_parts(Product,parts_dict)
    except Exception,e:
        Trace.Write("Error in GS_SM_System_PartSumary_Calcs: " + str(e) + " Line Number: " + str(sys.exc_traceback.tb_next.tb_lineno))
        '''try:
            parts_dict = GS_RTU_Replica_Config.multiply_replica_config(Product, parts_dict)
        except Exception,e:
            Product.ErrorMessages.Add("Error in GS_RTU_Replica_Config: " + str(e) + " Line Number: " + str(sys.exc_traceback.tb_next.tb_lineno))'''

    try:
        parts_dict = GS_SM_Hardware_Safety_Parts.getSMSystemParts(Product,parts_dict)
    except Exception,e:
        Trace.Write(str(e))

    Trace.Write("debugging: " + str(parts_dict))
    GS_SM_Part_Update.execute(Product, 'SM_System_PartSummary_Cont', parts_dict)