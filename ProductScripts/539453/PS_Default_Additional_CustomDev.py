labor_cont = Product.GetContainerByName('Additional_CustomDev_Labour_Container')
labor_cont.Rows[0].Product.Attr('Additional_CustomDev_Standard_Dev').SelectDisplayValue('PEP-PQP-HSE-Org Chart-Schedule')
labor_cont.Rows[0].Product.Attr('Additional_CustomDev_FO_Eng').SelectDisplayValue('SYS LE1-Lead Eng')
#labor_cont.Rows[0].Product.Attr('Additional_CustomDev_GES_Eng').SelectDisplayValue('SYS GES Eng-BO-IN')
labor_cont.Rows[0]['FO Eng']='SYS LE1-Lead Eng'
labor_cont.Rows[0].Product.ApplyRules()
labor_cont.Rows[0].ApplyProductChanges()
labor_cont.Calculate()