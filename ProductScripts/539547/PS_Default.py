labor_cont = Product.GetContainerByName('SCADA_Additional_Custom_Deliverables_Container')
labor_cont.Rows[0].Product.Attr('SCADA_Labor_FO_Eng').SelectDisplayValue('SYS HMI-Lead Eng')
labor_cont.Rows[0].GetColumnByName('FO Eng').ReferencingAttribute.SelectDisplayValue('SYS HMI-Lead Eng')
labor_cont.Rows[0]['FO Eng']='SYS HMI-Lead Eng'
labor_cont.Rows[0].Product.ApplyRules()
labor_cont.Rows[0].ApplyProductChanges()
labor_cont.Calculate()