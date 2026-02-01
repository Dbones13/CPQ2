[IF]([AND]([EQ](<*VALUE(SC_QCS_Site_to_Cloud_Method)*>,Edge Device Virtual Machine),[EQ](<*ATTSEL(SC_QCS_One Time Service Charges)*>,1))
){<*SELECTVALUE(SC_QCS_Qty_Honeywell_Edge_Device_VM:&nbsp)*>}{<*RESETVALUE(SC_QCS_Qty_Honeywell_Edge_Device_VM:&nbsp)*>}[ENDIF]
[IF]([AND]([EQ](<*VALUE(SC_QCS_Site_to_Cloud_Method)*>,MSS-VSE/VPE (Service Node)),[EQ](<*ATTSEL(SC_QCS_One Time Service Charges)*>,1))
){<*SELECTVALUE(SC_QCS_Quantity_Honeywell_Service_Node:&nbsp)*>}{<*RESETVALUE(SC_QCS_Quantity_Honeywell_Service_Node:&nbsp)*>}[ENDIF]

[IF]([EQ](<*VALUE(SC_QCS_Site_to_Cloud_Method)*>,Edge Device)){[IF]([IN](<*VALUE(SC_QCS_Number of Machines)*>,1,2,3)){<*ASSIGNVALUE(SC_QCS_Qty_Honeywell_Edge_Device:1)*>}{}[ENDIF]
[IF]([IN](<*VALUE(SC_QCS_Number of Machines)*>,4,5,6)){<*ASSIGNVALUE(SC_QCS_Qty_Honeywell_Edge_Device:2)*>}{}[ENDIF]
[IF]([IN](<*VALUE(SC_QCS_Number of Machines)*>,7,8)){<*ASSIGNVALUE(SC_QCS_Qty_Honeywell_Edge_Device:3)*>}{}[ENDIF]
}{[IF]([EQ](<*VALUE(SC_QCS_Site_to_Cloud_Method)*>,Edge Device Virtual Machine)){<*ASSIGNVALUE(SC_QCS_Qty_Honeywell_Edge_Device:1)*>}{<*ASSIGNVALUE(SC_QCS_Qty_Honeywell_Edge_Device:0)*>}[ENDIF]}[ENDIF]