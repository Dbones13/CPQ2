labor_cont = Product.GetContainerByName('PRMS_Additional_Labor_Container')
newRow = labor_cont.AddNewRow(False)
newRow.GetColumnByName('FO Eng').ReferencingAttribute.SelectDisplayValue('SYS CPA-Lead Eng')
newRow.GetColumnByName('Standard Deliverable selection').SetAttributeValue("PEP-PQP-HSE-Org Chart-Schedule")
#newRow['Standard Deliverable selection'] = "PEP-PQP-HSE-Org Chart-Schedule"
newRow.ApplyProductChanges()
newRow.Calculate()
labor_cont.Calculate()