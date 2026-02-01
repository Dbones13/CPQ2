def checkPartsManagement(cont,Pole,flag):
    if cont and cont.Rows.Count:
        for row in cont.Rows:
            if row["Service_Product"] == "Parts Holding P2":
                query = SqlHelper.GetFirst("select PartStatus,Replacement_Status,Replacement_Part from P1P2_PART_STATUS where PartNumber = '{}' and Pole = '{}'".format(row["Part_Number"],Pole))
                if query is not None:
                    if query.PartStatus != row["Part_Status"] or query.Replacement_Status != row["Replacement_Status"] or query.Replacement_Part != row["Replacement_Part"]:
                        flag = True
                else:
                    if row["Part_Status"] != "" or row["Replacement_Status"] != "" or row["Replacement_Part"] != "":
                        flag = True
    return flag


if Quote.GetCustomField("Quote Type").Content == "Contract Renewal":
    flag = False
    for item in Quote.MainItems:
        if item.PartNumber == "Parts Management" and item.QI_SC_ItemFlag.Value == "Hidden":
            cont = item.SelectedAttributes.GetContainerByName("SC_P1P2_Parts_Details")
            Pole = Quote.GetCustomField("Pole").Content
            BookingCountry = Quote.GetCustomField("Booking Country").Content
            if Pole == "APAC":
                Pole = "JP" if BookingCountry == "japan" else "SG"
            flag = checkPartsManagement(cont,Pole,flag)
            break
    if Quote.GetCustomField("SC_CF_IS_STATUS_CHECK").Content == '1':
        if flag == True:
            Quote.Messages.Add('Change in Parts status configuration - User has to go configuration Parts Management Module & correct it.')
        else:
            Quote.Messages.Add('There is no change in Parts status configuration.')
            #WorkflowContext.BreakWorkflowExecution = True

