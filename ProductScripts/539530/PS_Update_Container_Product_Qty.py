cont = Product.GetContainerByName('MXP_CD_partsummary_cont')
if cont.Rows.Count > 0:
    for row in cont.Rows:
        update=False
        if int(row["CE_Final_Quantity"]) > 0:
            if row.IsSelected == False:
                row.IsSelected = True
                row.Calculate()
                update=True
            if row.Product.Attributes.GetByName('ItemQuantity'):
                if int(row["CE_Final_Quantity"]) !=  row.Product.Attr('ItemQuantity').GetValue():
                    row.Product.Attr('ItemQuantity').AssignValue(row["CE_Final_Quantity"])
                    update=True
            else:
                Product.ErrorMessages.Add('Item Quantity missing from part number {}, please contact the Admin'.format(row.Product.PartNumber))
            if update==True:
                row.ApplyProductChanges()
        else:
            if row.IsSelected == True:
                row.IsSelected = False