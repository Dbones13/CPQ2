labor_cont = Product.GetContainerByName('Simulation_Labor_Additional_Cust_Deliverables_con')
labor_cont.Rows[0].Product.Attr('Simulation_Labor_FO_Eng').SelectDisplayValue('SYS LE1-Lead Eng')
labor_cont.Rows[0].GetColumnByName('FO Eng').ReferencingAttribute.SelectDisplayValue('SYS LE1-Lead Eng')
#labor_cont.Rows[0].Product.ApplyRules()
#labor_cont.Rows[0].ApplyProductChanges()
labor_cont.Calculate()