R2Qrequest = True if Quote.GetCustomField('IsR2QRequest').Content else False
if R2Qrequest:
	platform_opt = Product.Attr('VS_Platform_Options').GetValue()
	if platform_opt == 'Essentials - Lifecycle Bid':
		VS_License = Product.Attr('VS_Use_Own_OS_License').GetValue()
		if VS_License == 'Yes':
			Product.Attr('Virtualization_DataCenter_OS_to_be_offered').SelectDisplayValue('No')
		else:
			Product.Attr('Virtualization_DataCenter_OS_to_be_offered').SelectDisplayValue('Yes')
			Product.Attr('Virtualization_Platform_Options').SelectDisplayValue('Essentials Platforms-Dell Servers')
	
	elif platform_opt in ['Number of Performance A Servers (0-9 per cluster)', 'Number of Performance B Servers (0-9 per cluster)']:
		Product.Attr('Virtualization_Platform_Options').SelectDisplayValue('Premium Platforms Gen 3 - Performance A/B')
		Product.Attr('VS_Use_Own_OS_License').SelectDisplayValue('No')
		Product.Attr('Virtualization_DataCenter_OS_to_be_offered').SelectDisplayValue('Yes')
		vs_24port = Product.Attr('VS_24Port_Rack_Required').GetValue()
		vs_48port = Product.Attr('VS_48Port_Rack_Required').GetValue()
		vs_cluster = Product.Attr('VS_Number_of_Clusters_in_the_network').GetValue()
		if vs_cluster :
			Product.Attr('Virtualization_Number_of_Clusters_in_the_network').AssignValue(str(vs_cluster))
		else:
			Product.Attr('Virtualization_Number_of_Clusters_in_the_network').AssignValue('1')
		
		cluster_container = Product.GetContainerByName('Virtualization_cluster_transpose')
		cluster_container_count = Product.GetContainerByName('Virtualization_cluster_transpose').Rows.Count
		cluster_container_clear = Product.GetContainerByName('Virtualization_cluster_transpose').Rows.Clear()
		for i in range(0,int(vs_cluster)):
			if vs_cluster != cluster_container_count:
				thlevelcontainerRows = cluster_container.AddNewRow()
				thlevelcontainerRows.Product.Attr('Virtualization_of_24_Port_Top_of_Rack_Switch').AssignValue(str(vs_24port))
				thlevelcontainerRows.Product.Attr('Virtualization_of_48_Port_Top_of_Rack_Switch').AssignValue(str(vs_48port))
				if platform_opt == 'Number of Performance A Servers (0-9 per cluster)':
					thlevelcontainerRows.Product.Attr('Virtualization_Number_of_B_VxRail_E660_Servers').AssignValue('0')
				if platform_opt == 'Number of Performance B Servers (0-9 per cluster)':
					thlevelcontainerRows.Product.Attr('Virtualization_Number_of_A_VxRail_E660_Servers').AssignValue('0')
				thlevelcontainerRows.Calculate()

	elif platform_opt == 'Premium Platforms 2 node pair (0-4)':
		Product.Attr('Virtualization_Platform_Options').SelectDisplayValue('Premium Platforms Gen 3 - 2 node cluster')
		VS_License = Product.Attr('VS_Use_Own_OS_License').GetValue()
		if VS_License == 'Yes':
			Product.Attr('Virtualization_DataCenter_OS_to_be_offered').SelectDisplayValue('No')
		else:
			Product.Attr('Virtualization_DataCenter_OS_to_be_offered').SelectDisplayValue('Yes')



	BTC12_val = BTC14_val = dell_val = Uni_val = 0
	count=0
	VSContainer = Product.GetContainerByName('Virtualization_System_WorkLoad_Cont')
	for row in VSContainer.Rows:
		thin_value = ''
		number = 0
		flag = 0
		count+=1
		if count >=6 and count <=30:
			for col in row.Columns:
				if col.Name == 'Thin_Client_Requirements' and col.Value in ('BTC12', 'BTC14', 'DELL OPTIPLEX 3000', 'Universal'):
					thin_value = str(col.Value)
				if col.Name == 'Number':
					number = col.Value
				if thin_value != '' and number != 0 and flag == 0:
					flag = 1
					if thin_value == 'BTC12':
						BTC12_val += int(number)
					elif thin_value == 'BTC14':
						BTC14_val += int(number)
					elif thin_value == 'DELL OPTIPLEX 3000':
						dell_val += int(number)
					elif thin_value == 'Universal':
						Uni_val += int(number)

	Product.Attr('Virtualization_Number_P_&_F_BTC12_Dual_Thin_Client').AssignValue(str(BTC12_val))
	Product.Attr('Virtualization_of_P&F_BTC14_Quad_Video_Thin_Client').AssignValue(str(BTC14_val))
	#Product.Attr('Virtualization_5070_Universal_Thin_Client_for_5').AssignValue(str(Uni_val))
	Product.Attr('Virtualization_OPTIPLEX_3000_Thin_Client').AssignValue(str(dell_val))

	# Uncomment if rule-based fields must be recalculated
	# Product.ApplyRules()
