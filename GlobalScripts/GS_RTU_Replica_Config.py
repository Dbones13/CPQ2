def multiply_replica_config(Product,parts_dict):
    ttl_replica_configurations = 0
    for cg in Product.GetContainerByName('RTU_ControlGroup_Cont').Rows:
        cab_cont = cg.Product.GetContainerByName('RTU_CG_Controller_Cont')
        ttl_replica_configurations += int(cab_cont.Rows[0].GetColumnByName('Replica_configurations').Value)
    for part in parts_dict:
        if part not in ['SP-EBLDR1','SP-MCALC1']:
            parts_dict[part]['Quantity'] = str(int(parts_dict[part]['Quantity']) * ttl_replica_configurations)
    return parts_dict, ttl_replica_configurations

def multiply_replica_config_cg(Product,parts_dict):
    cab_cont = Product.GetContainerByName('RTU_CG_Controller_Cont') #CXCPQ-30286 Remove SP-LEPIU1 - Himanshu
    ttl_replica_configurations = int(cab_cont.Rows[0].GetColumnByName('Replica_configurations').Value)
    for part in parts_dict:
        if part not in ['SP-EBLDR1','SP-MCALC1']:
            parts_dict[part]['Quantity'] = str(int(parts_dict[part]['Quantity']) * ttl_replica_configurations)
    return parts_dict