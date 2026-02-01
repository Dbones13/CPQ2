def applyProductSelection(Product):
    systemContainer = Product.GetContainerByName('CE_SystemGroup_Cont')
    selectedProducts = Product.Attr('CE_Product_Choices').SelectedValues

    for row in systemContainer.Rows:
        if row.IsSelected:
            systemGroupProduct = row.Product
            productContainer = systemGroupProduct.GetContainerByName('CE_System_Cont')
            for value in selectedProducts:
                newRow = productContainer.AddNewRow(value.ValueCode + '_cpq' , True)
                newRow['Product Name'] = value.Display
                #Set Default MIB configuration attribut value
                if value.Display == 'Experion Enterprise System':
                    newRow['MIB Configuration Required?'] = 'Yes'
                    newRow.Product.Attr("MIB Configuration Required?").SelectValue('Yes')
                newRow.ApplyProductChanges()
            productContainer.Calculate()
            systemGroupProduct.ApplyRules()
            row.ApplyProductChanges()
    systemContainer.Calculate()
    Product.Messages.Add('Products are successfully applied against the Selected System')

applyProductSelection(Product)