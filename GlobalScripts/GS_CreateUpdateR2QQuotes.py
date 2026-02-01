def AddRows(rowCount, container):
    for i in range(rowCount):
        if container.Name == 'CE_SystemGroup_Cont':
            row = container.AddNewRow(False)
            row.Product.Attr("Sys_Group_Name").AssignValue('System Group 1')
            row.Product.Attr("CE_System_Index").AssignValue(str(row.RowIndex + 1))
            row.Product.Attr('CE_Scope_Choices').SelectDisplayValue(Product.Attr('CE_Scope_Choices').GetValue())
            
            r2qParentProductContainer=Product.GetContainerByName('R2Q Container')
            selectedProducts= r2qParentProductContainer
            selVal=[]
            for value in selectedProducts.Rows:
                selVal.append(value.Product.Name)
            
            Product.Attr('CE_Product_Choices').SelectDisplayValues(*selVal)
            row.Product.ApplyRules()
            row.ApplyProductChanges()
            row.Calculate()
        else:
            container.AddNewRow(False)

#Clear CE_SystemGroup_Cont in "General Input Tab"
systemContainer = Product.GetContainerByName('CE_SystemGroup_Cont')
systemContainer.Clear()

if Product.Name == "R2Q New / Expansion Project":
    #SG_cont = Product.GetContainerByName('Number_System_Groups').Rows[0]
    SG_rowCount = 1
    SG_rowCount = int(SG_rowCount) if SG_rowCount else 0
    CE_SystemGroup_Cont = Product.GetContainerByName('CE_SystemGroup_Cont')
    try:
        AddRows(SG_rowCount, CE_SystemGroup_Cont)
    except :
        Product.Attr('ExceededLimit').AssignValue('True')
        pass
    row = Product.GetContainerByName('CE_SystemGroup_Cont').Rows[0]
    row.IsSelected = True

cont1=Product.GetContainerByName('CE_Project_Questions_Cont')
cont1.Rows[0].Columns['Project Categorization'].SetAttributeValue(Product.Attr('Exp_Project_Categorization').SelectedValue.Display)
#Add product selection from "R2Q Container" in R2Q General Inputs Tab
systemContainer = Product.GetContainerByName('CE_SystemGroup_Cont')
r2qParentProduct=Product
r2qParentProductContainer=r2qParentProduct.GetContainerByName('R2Q Container')
selectedProducts= r2qParentProductContainer
#selectedProducts = Product.Attr('CE_Product_Choices').SelectedValues
for row in systemContainer.Rows:
    if row.IsSelected:
        systemGroupProduct = row.Product
        productContainer = systemGroupProduct.GetContainerByName('CE_System_Cont')
        for value in selectedProducts.Rows:
            newRow = productContainer.AddNewRow(value.Product.SystemId , True)
            newRow['Product Name'] = value.Product.Name
            #Set Default MIB configuration attribut value
            if value.Product.Name == 'Experion Enterprise System':
                newRow['MIB Configuration Required?'] = 'Yes'
                newRow.Product.Attr("MIB Configuration Required?").SelectValue('Yes')
                newRow.ApplyProductChanges()
            productContainer.Calculate()
            systemGroupProduct.ApplyRules()
            row.ApplyProductChanges()
systemContainer.Calculate()
Product.Messages.Add('Products are successfully applied against the Selected System')

#Product creation and initialization logic for products in System Container
if Quote.GetCustomField('isR2QRequest').Content == 'Yes':
    r2qParentProduct=Product
    r2qParentProductContainer=r2qParentProduct.GetContainerByName('R2Q Container')
    for r2qParentProductContainerRow in r2qParentProductContainer.Rows:
        if r2qParentProductContainerRow.Columns['Part Number'].Value in ["C300 System"]:
            ScriptExecutor.Execute('GS_R2Q_NewExpansion_C300_Config')
    r2qParentProduct.AddToQuote()