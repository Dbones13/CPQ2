noof_nutanix_singlenode = Product.Attr('Number of Nutanix Standard Clusters in the network').GetValue()
stdcluster_cont = Product.GetContainerByName('Virtualization_Std_Cluster_Conf_transpose')
if noof_nutanix_singlenode and str(noof_nutanix_singlenode)!='0':
	if Product.GetGlobal('NutanixCount')=='':
		Product.SetGlobal('NutanixCount', noof_nutanix_singlenode)
	nutanix_count = int(noof_nutanix_singlenode)	
	rowscount = stdcluster_cont.Rows.Count
	if rowscount > nutanix_count:
		flag = 0
		for i in range(nutanix_count,rowscount):
			flag += 1
			stdcluster_cont.DeleteRow(rowscount-flag)
			if int(Product.GetGlobal('NutanixCount') or 0)>1 and nutanix_count==1:
				r = stdcluster_cont.Rows[0]
				r['Number_of_Nutanix_Premium_Platform_16_Core_0_9'] = '4'
				r.Product.Attr('No of Nutanix Premium Platform 16 Core SC').AssignValue('4')
			
	if rowscount < nutanix_count:
		for i in range(rowscount,nutanix_count):
			r = stdcluster_cont.AddNewRow(False)
			if Product.Attr('Virtualization_Platform_Options').GetValue() == 'Premium Platform for Nutanix' and int(nutanix_count)==1:
				r['Number_of_Nutanix_Premium_Platform_16_Core_0_9'] = '4'
				r.Product.Attr('No of Nutanix Premium Platform 16 Core SC').AssignValue('4')
			else:
				r['Number_of_Nutanix_Premium_Platform_16_Core_0_9'] = '3'
				r.Product.Attr('No of Nutanix Premium Platform 16 Core SC').AssignValue('3')
	if int(Product.GetGlobal('NutanixCount') or 0)==1 and nutanix_count>1:
		for i in stdcluster_cont.Rows:
			i['Number_of_Nutanix_Premium_Platform_16_Core_0_9'] = '3'
			i.Product.Attr('No of Nutanix Premium Platform 16 Core SC').AssignValue('3')

	Product.SetGlobal('NutanixCount', noof_nutanix_singlenode)
	
	
	stdcluster_cont.Calculate()
	for i in stdcluster_cont.Rows:
		cluster_cnt = int(i['No_of_Nutanix_Premium_Platform_32_Core_SC'])+int(i['Number_of_Nutanix_Premium_Platform_16_Core_0_9'])
		Product.Attr('Nutanix_cluster_Message1').AssignValue('')
		Product.Attr('Nutanix_cluster_Message2').AssignValue('')
		if int(noof_nutanix_singlenode)==1:
			Trace.Write('count in -')
			if cluster_cnt<4 or cluster_cnt>9:
				Trace.Write('2345')
				Product.Attr('Nutanix_cluster_Message1').AssignValue('1')
				break
		else:
			if cluster_cnt<3 or cluster_cnt>9:
				Product.Attr('Nutanix_cluster_Message2').AssignValue('1')
				break
