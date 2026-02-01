def dictUpdate(container, msidAttributeDict):
    if container.Name == "IAA Inputs_Cont":
        for row in container.Rows:
            msidAttributeDict[row["IAA_Assessment_Type"]]=row["IAA_Quantity"]
    elif container.Name == "IAA Inputs_Cont_2":
        for row in container.Rows:
            msidAttributeDict[row["Name"]]=row["Quantity"]
    elif container.Name == "IAA Pricing":
        for row in container.Rows:
            msidAttributeDict[row["Name"]]=row["Price"]