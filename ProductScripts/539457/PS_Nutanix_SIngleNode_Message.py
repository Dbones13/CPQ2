cluster_single=Product.Attr('No of Nutanix Single Node Clusters in the network').GetValue()
cluster_std=Product.Attr('Number of Nutanix Standard Clusters in the network').GetValue()
single_node_cont = Product.GetContainerByName('Virtualization_Single_Node_Cluster_Conf_transpose')
std_node_cont=Product.GetContainerByName('Virtualization_Std_Cluster_Conf_transpose')
if cluster_single == '0':
    single_node_cont.Clear()
if cluster_std =='0':
    std_node_cont.Clear()



single_node_cont_rows = Product.GetContainerByName('Virtualization_Single_Node_Cluster_Conf_transpose').Rows
platform_options=Product.Attr('Virtualization_Platform_Options').GetValue()
for row in single_node_cont_rows:

    if platform_options == "Premium Platform for Nutanix":
        pltfrm_32_core = row['No_of_Nutanix_Premium_Platform_32_Core_SC']
        pltfrm_16_core = row['Number_of_Nutanix_Premium_Platform_16_Core_0_1']
        if (int(pltfrm_32_core) + int(pltfrm_16_core)) > 1 or (int(pltfrm_32_core) + int(pltfrm_16_core)) < 1:
            Product.Attr('Message_val').AssignValue('1')
            break
        else:
            Product.Attr('Message_val').AssignValue('0')
    else:
        Product.Attr('Message_val').AssignValue('0')

Product.Attr('Virt_software_docattr').AssignValue('False')
Product.Attr('Virt_hardware_docattr').AssignValue('False')
hw_attr = ['Virtualization_Number_of_R640XL_Management_Servers','Virtualization_Number_of_R640XL_Standard_Servers','Virtualization_Number_R740XL_Performance_A_Servers','Virtualization_Number_R740XL_Performance_B_Servers','Virtualization_Number_P_&_F_BTC12_Dual_Thin_Client','Virtualization_of_P&F_BTC14_Quad_Video_Thin_Client','Virtualization_OPTIPLEX_3000_Thin_Client','Virtualization_Number_Storage_Device_Standard','Virtualization_Number_Storage_Device_Performance','Virtualization_Number_of_vSphere_Client_Node','Virtualization_vSphere_Client_Node_Type','Virtualization_vSphere_Client_Node_OS_Type','Virtualization_CISCO_Virtual_Management_Switch','Virtualization_Giga_Byte_C2960X_CISCO_Switch','Virtualization_Adapter_for_Redundant_FTE_Networks']
for i in hw_attr:
    if int(Product.Attr(i).GetValue() or 0) >0:
        Product.Attr('Virt_hardware_docattr').AssignValue('True')
        break
sw_attr = ['Virtualization_Windows_Server_2016_COA_Licenses','Virtualization_Windows_Server_2019_COA_Licenses','Virtualization_Windows_Server_2022_COA_Licenses','Virtualization_Experion_Virtualization_Server_CAL','Virtualization_Experion_Virtualization_Client_CAL','Virtualization_FDM_Virtualization_Server_CAL','Virtualization_FDM_Virtualization_Client_CAL','Virtualization_Windows_RDS_CAL','Virtualization_Microsoft_SQL_Client_Access_Lic']
for i in sw_attr:
    if int(Product.Attr(i).GetValue() or 0) >0:
        Product.Attr('Virt_software_docattr').AssignValue('True')
        break
