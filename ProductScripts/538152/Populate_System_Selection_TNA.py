Sys_Sel_Cont = Product.GetContainerByName("SC_WEP_System_Selection_TNA")
Sys_Sel_Cont.Rows.Clear()

Sys_Sel_List = ["APC","CPM","CTE-UOC","Dynamo","EPKS","FDM","Networking","OTS","PHD","QCS","SM","SM-SC","TPS","Virtualization"]

for i in Sys_Sel_List:
    Sys_Sel_row = Sys_Sel_Cont.AddNewRow(False)
    Sys_Sel_row["Selected_System"] = i