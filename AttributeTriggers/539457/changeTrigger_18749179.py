noof_nutanix_singlenode = Product.Attr('No of Nutanix Single Node Clusters in the network').GetValue()
single_node_cont = Product.GetContainerByName('Virtualization_Single_Node_Cluster_Conf_transpose')
if noof_nutanix_singlenode and str(noof_nutanix_singlenode)!='0':
    nutanix_count = int(noof_nutanix_singlenode)
    rowscount =single_node_cont.Rows.Count
    if rowscount < nutanix_count:
        for i in range(rowscount,nutanix_count):
            r = single_node_cont.AddNewRow(False)
    elif rowscount > nutanix_count:
        flag = 0
        for i in range(nutanix_count,rowscount):
            flag += 1
            single_node_cont.DeleteRow(rowscount-flag)
    single_node_cont.Calculate()