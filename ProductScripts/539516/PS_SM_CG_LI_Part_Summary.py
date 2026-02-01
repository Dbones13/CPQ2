sm_cont = Product.GetContainerByName('SM_CG_PartSummary_Cont')
#Product.Messages.Clear()
errorFlag = False
if sm_cont:
    for row in sm_cont.Rows:
        finalQuantity = int(row['CE_Final_Quantity'])
        if finalQuantity < 0:
            errorFlag = True
            break
    Trace.Write("Error Flag: " + str(errorFlag))
    if errorFlag:
        #Product.ErrorMessages.Add("Please check part number with -ve qty in Final Quantity Column and update value in '+/- Adj Quantity' column")
        Product.Attr('PartSummaryErrorMsg').AssignValue('True')
        Trace.Write('Error Flag True: ' + str(errorFlag))
    else:
        Trace.Write('Error Flag False: ' + str(errorFlag))
        Product.Attr('PartSummaryErrorMsg').AssignValue('False')
    #Product.Messages.Clear()
    sm_li_cont = Product.GetContainerByName('SM_CG_PartSummary_LI_Cont')
    if sm_li_cont:
        sm_li_cont.Rows.Clear()
    if sm_cont:
        for row in sm_cont.Rows:
            part = row['CE_Part_Number']
            quantity = row['CE_Part_Qty']
            part_description = row['CE_Part_Description']
            adjQuantity = row['CE_Adj_Quantity'] if row['CE_Adj_Quantity'] else 0
            comments = row['CE_Comments']
            finalQuantity = int(row['CE_Final_Quantity'])
            if finalQuantity > 0:
                row = sm_li_cont.AddNewRow(part, False)
                row.GetColumnByName("CE_Part_Qty").Value = quantity
                row.GetColumnByName("CE_Part_Description").Value = part_description
                row.GetColumnByName("CE_Adj_Quantity").Value = str(adjQuantity)
                row.GetColumnByName("CE_Final_Quantity").ReferencingAttribute.AssignValue(str(finalQuantity))
                row.GetColumnByName("CE_Comments").Value = comments
                row.Calculate()
    if sm_li_cont:
        sm_li_cont.Calculate()
#Product.ApplyRules()