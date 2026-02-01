Acc = Product.Attr('Virtualization_Acceptance_Test_requested').GetValue()
laborCont = Product.GetContainerByName('Virtualization_Labor_Deliverable')
for row in laborCont.Rows:
    deliverable = row.GetColumnByName("Deliverable").Value
    Trace.Write("deliv ------"+str(deliverable))
    if Acc == 'SAT' and deliverable == 'FAT':
        row['Final Hrs'] = '0'
        break
    elif Acc == 'FAT' and deliverable == 'SAT':
        row['Final Hrs'] = '0'
        break
ScriptExecutor.Execute('PS_Virtual_Labor_Deliverable_Container_Populate')
laborCont.Calculate()