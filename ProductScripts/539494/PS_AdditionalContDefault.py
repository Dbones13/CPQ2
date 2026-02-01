labor_cont = Product.GetContainerByName('MXPro_Labor_Additional_Cust_Deliverables_con')
labor_cont.Rows[0].Product.Attr('MXPro_Labor_FO_Eng').SelectDisplayValue('SYS QCS-Lead Engineer')
labor_cont.Rows[0].GetColumnByName('FO Eng').ReferencingAttribute.SelectDisplayValue('SYS QCS-Lead Engineer')
labor_cont['FO Eng']='SYS QCS-Lead Engineer'
labor_cont.Rows[0].Product.ApplyRules()
labor_cont.Rows[0].ApplyProductChanges()
labor_cont.Calculate()