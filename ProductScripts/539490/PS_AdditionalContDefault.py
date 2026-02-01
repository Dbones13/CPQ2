labor_cont = Product.GetContainerByName('Experion_mx_labor_Additional_Cust_Deliverables_con')
if labor_cont.Rows.Count > 0:
    labor_cont.Rows[0].Product.Attr('Experion_mx_Labor_FO_Eng').SelectDisplayValue('SYS QCS-Lead Engineer')
    labor_cont.Rows[0].GetColumnByName('FO Eng').ReferencingAttribute.SelectDisplayValue('SYS QCS-Lead Engineer')
    labor_cont.Rows[0].Item['FO Eng']='SYS QCS-Lead Engineer'
    labor_cont.Rows[0].Product.ApplyRules()
    labor_cont.Rows[0].ApplyProductChanges()
    labor_cont.Calculate()