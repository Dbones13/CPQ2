labor_cont = Product.GetContainerByName('CE UOC Additional Custom Deliverables')
labor_cont.Rows[0].GetColumnByName('FO Eng').SetAttributeValue('SYS LE1-Lead Eng')
labor_cont.Rows[0]['FO Eng']='SYS LE1-Lead Eng'
labor_cont.Rows[0].Product.ApplyRules()
labor_cont.Rows[0].ApplyProductChanges()
labor_cont.Calculate()