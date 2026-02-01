def sortRow(cont,rank,new_row_index):
    sort_needed = True
    if new_row_index == 0:
        return
    while sort_needed == True:
        #Trace.Write("rank of previous row: {0}, new_row_index: {1}".format(cont.Rows[new_row_index-1].GetColumnByName('Rank').Value, new_row_index))
        if int(cont.Rows[new_row_index-1].GetColumnByName('Rank').Value) > int(rank):
            cont.MoveRowUp(new_row_index, False)
            new_row_index -= 1
            if new_row_index == 0:
                break
        else:
            sort_needed = False

Product.ExecuteRulesOnce = True #This is to improve performance. We keep triggering product rules execution with each change to each container cell. Sets back to False at end of script.

disallow_lst = []
x = Product.Attr("Terminal_Mode_of_Transport").Values
for value in x:
    if value.Display == "Truck loading/unloading":
        if value.IsSelected == False:
            disallow_lst.append("Entry Gate")
            disallow_lst.append("Reporting Office")
            disallow_lst.append("Bay Que")
            disallow_lst.append("Weigh Bridge (IN)")
            disallow_lst.append("Weigh Bridge (OUT)")
            disallow_lst.append("BoL Office")
            disallow_lst.append("Exit Gate")
            disallow_lst.append("PC DET")
            disallow_lst.append("Mercury Terminal")



Worflow_Query = SqlHelper.GetList("select Element,Rank from Terminal_Manager_Scope where Scope = '{}'".format("Workflow"))
Workflow_Container =  Product.GetContainerByName('Terminal_Workflow_Scope')


list = []
rows_to_delete = []
for row in Workflow_Container.Rows:
    list.append(row.GetColumnByName('Element').Value)

for row in Worflow_Query:
    if row.Element not in disallow_lst and row.Element not in list:
        new_row = Workflow_Container.AddNewRow(False)
        new_row["Element"] = row.Element
        new_row.GetColumnByName('Complexity').SetAttributeValue("Simple")
        new_row.GetColumnByName('Type').SetAttributeValue("Standard")
        new_row["Rank"] = str(row.Rank)
        sortRow(Workflow_Container,row.Rank,new_row.RowIndex)
    elif row.Element in disallow_lst and row.Element in list:
        for cont_row in Workflow_Container.Rows:
            if row.Element == cont_row.GetColumnByName('Element').Value:
                rows_to_delete.append(cont_row.RowIndex)
Workflow_Container.Calculate()
rows_to_delete.sort(reverse=True)

for x in rows_to_delete:
    Workflow_Container.DeleteRow(x)


Product.ExecuteRulesOnce = False