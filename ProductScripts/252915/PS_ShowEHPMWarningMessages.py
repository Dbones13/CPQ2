def getContainer(Name):
    return Product.GetContainerByName(Name)

Product.Messages.Clear()
query = SqlHelper.GetList("select * from MIGRATON_EHPM_WARNING_MESSAGES")
if query is not None:
    for entry in query:
        for row in getContainer(entry.Container1).Rows:
            if row[entry.Con_Col_Name1] == entry.Con_Col_Value1 and row[entry.Con_Col_Name2] == entry.Con_Col_Value2:
                if row["xPM_Is_FTE_Network_Infrastructure_Existing"] == "Yes":
                    message = entry.Message +", "+ "System Architecture Drawing for existing FTE Required"
                    Product.Messages.Add(message)
                    break
                else:
                    Product.Messages.Add(entry.Message)
                    break