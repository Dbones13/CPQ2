labor_cont = Product.GetContainerByName('DVM_Additional_Labour_Container')
newRow = labor_cont.AddNewRow(False)
newRow.GetColumnByName('FO Eng').ReferencingAttribute.SelectDisplayValue('SYS CPA-Lead Eng')
newRow['FO Eng']='SYS CPA-Lead Eng'
newRow.GetColumnByName('Standard Deliverable').SetAttributeValue("PEP-PQP-HSE-Org Chart-Schedule")
newRow['Standard Deliverable'] = "PEP-PQP-HSE-Org Chart-Schedule"
newRow.ApplyProductChanges()
newRow.Calculate()
labor_cont.Calculate()
if Quote.GetCustomField("isR2QRequest").Content =='Yes':
    Product.Attr('R2QRequest').AssignValue('Yes')
    Product.Attr("R2Q_QuoteNumber").AssignValue(str(Quote.CompositeNumber))