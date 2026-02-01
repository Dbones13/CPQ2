labor_cont = Product.GetContainerByName('eServer_Labor_Additional_Cust_Deliverables_con')
labor_cont.Rows[0].Product.Attr('eServer_Labor_FO_Eng').SelectDisplayValue('SYS LE1-Lead Eng')
labor_cont.Rows[0].GetColumnByName('FO Eng').ReferencingAttribute.SelectDisplayValue('SYS LE1-Lead Eng')
labor_cont.Rows[0]['FO Eng']='SYS LE1-Lead Eng'
labor_cont.Rows[0].Product.ApplyRules()
labor_cont.Rows[0].ApplyProductChanges()
labor_cont.Calculate()