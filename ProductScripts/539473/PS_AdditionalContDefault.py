# Set attribute value by default if it is empty and required
import GS_DropDown_Implementation
labor_cont = Product.GetContainerByName('ESDC_Labor_Additional_Cust_Deliverables_con')
labor_cont.Rows[0].Product.Attr('ESDC_Labor_FO_Eng').SelectDisplayValue('SYS LE1-Lead Eng')
labor_cont.Rows[0].GetColumnByName('FO Eng').ReferencingAttribute.SelectDisplayValue('SYS LE1-Lead Eng')
labor_cont.Rows[0].Product.ApplyRules()
labor_cont.Rows[0].ApplyProductChanges()
labor_cont.Calculate()
GS_DropDown_Implementation.SetDropDownDefaultvalue(Product)