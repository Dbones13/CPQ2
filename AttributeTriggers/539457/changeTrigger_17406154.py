[IF]([EQ](<*VALUE(Virtualization_Platform_Options)*>,Essentials Platforms-Dell Servers)){<*ASSIGNVALUE(Virtualization_Number_of_R640XL_Management_Servers:0)*>
<*ASSIGNVALUE(Virtualization_Number_of_R640XL_Standard_Servers:0)*>
<*ASSIGNVALUE(Virtualization_Number_R740XL_Performance_A_Servers:0)*>
<*ASSIGNVALUE(Virtualization_Number_R740XL_Performance_B_Servers:0)*>
<*ASSIGNVALUE(Virtualization_for_Hosts_and_Switches:0)*>
<*ASSIGNVALUE(Virtualization_VMWare_Essentials_Plus_Licenses:0)*>
<*ASSIGNVALUE(Virtualization_vSphere_Single_Socket_Host_Licenses:0)*>
<*ASSIGNVALUE(Virtualization_VMWare_vSphere_Dual_Socket:0)*>
[IF]([EQ](<*VALUE(R2QRequest)*>,Yes)){}{<*ASSIGNVALUE(Virtualization_CISCO_Virtual_Management_Switch:1)*>}[ENDIF]}{<*ASSIGNVALUE(Virtualization_VSAN_Single_Socket_Host_Licenses:0)*>
<*ASSIGNVALUE(Virtualization_VMWare_vSphere_Plus_Single_Socket:0)*>
<*ASSIGNVALUE(Virtualization_VMWare_VSAN_Dual_Socket_Host:0)*>
<*ASSIGNVALUE(Virtualization_vSphere_ENT_Plus_Dual_Socket_Host:0)*>
[IF]([EQ](<*VALUE(R2QRequest)*>,Yes)){}{<*ASSIGNVALUE(Virtualization_CISCO_Virtual_Management_Switch:2)*>}[ENDIF]}[ENDIF]

[IF]([EQ](<*VALUE(Virtualization_Platform_Options)*>,Premium Platforms Gen 3 - 2 node cluster)){
<*ASSIGNVALUE(Virtualization_Number_of_Premium_Platforms_Gen:0)*>
<*ASSIGNVALUE(Virtualization_OnSite_Activities_hours:0)*>}[ENDIF]

[IF]([EQ](<*VALUE(Virtualization_Platform_Options)*>,Premium Platforms Gen 3 - Performance A/B)){
<*ASSIGNVALUE(Virtualization_Number_of_Clusters_in_the_network:0)*>
<*ASSIGNVALUE(Virtualization_OnSite_Activities_hours:0)*>}[ENDIF]