labor_cont = Product.GetContainerByName('PM_Additional_Custom_Deliverables_Labor_Container')
labor_cont.Rows[0].Product.Attr('Additional_Project_Deliverables').SelectDisplayValue('PEP-PQP-HSE-Org Chart-Schedule')
labor_cont.Rows[0].Product.Attr('Additional_Project_FOENG_Deliverables').SelectDisplayValue('SYS LE-Lead Eng')
labor_cont.Rows[0].Product.ApplyRules()
labor_cont.Rows[0].ApplyProductChanges()
#labor_cont.Rows[1].Product.ApplyRules()
#labor_cont.Rows[1].ApplyProductChanges()
labor_cont.Calculate()