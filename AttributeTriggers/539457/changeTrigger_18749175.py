noof_nutanix_singlenode = Product.Attr('Number of Nutanix Standard Clusters in the network').GetValue()
stdcluster_cont = Product.GetContainerByName('Virtualization_Std_Cluster_Conf_transpose')
stdcluster_cont.Rows.Clear()
if noof_nutanix_singlenode and str(noof_nutanix_singlenode)!='0':
    nutanix_count = int(noof_nutanix_singlenode)
    rowscount = stdcluster_cont.Rows.Count
    if rowscount < nutanix_count:
        for i in range(rowscount,nutanix_count):
            r = stdcluster_cont.AddNewRow(False)
        stdcluster_cont.Calculate()
    elif rowscount > nutanix_count:
        flag = 0
        for i in range(nutanix_count,rowscount):
            flag += 1
            stdcluster_cont.DeleteRow(rowscount-flag)
        stdcluster_cont.Calculate()
    '''if Product.Attr('Nutanix License Type') != 'Per VM':
        Product.ParseString('<*CTX( Container(Virtualization_Std_Cluster_Conf_transpose).Column(Number_of_Nutanix_NCIE_Per_VM_25).SetPermission(Hidden) )*>')
    else:
        Product.ParseString('<*CTX( Container(Virtualization_Std_Cluster_Conf_transpose).Column(Number_of_Nutanix_NCIE_Per_VM_25).SetPermission(Hidden) )*>')'''
    for i in stdcluster_cont.Rows:
        if Product.Attr('Virtualization_Platform_Options').GetValue() == 'Premium Platform for Nutanix' and int(nutanix_count)==1:
            i['Number_of_Nutanix_Premium_Platform_16_Core_0_9'] = '4'
            i.Product.Attr('No of Nutanix Premium Platform 16 Core SC').AssignValue('4')
        else:
            i['Number_of_Nutanix_Premium_Platform_16_Core_0_9'] = '3'
            i.Product.Attr('No of Nutanix Premium Platform 16 Core SC').AssignValue('3')
        