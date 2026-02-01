labor_cont = Product.GetContainerByName('SM_Additional_Custom_Deliverables_Labor_Container')
labor_cont.Rows[0].Product.Attr('SM_Labor_FO_Eng').SelectDisplayValue('SYS LE1-Lead Eng')
labor_cont.Rows[0]['FO Eng']='SYS LE1-Lead Eng'
labor_cont.Rows[0].Product.ApplyRules()
labor_cont.Rows[0].ApplyProductChanges()
labor_cont.Calculate()
# Set attribute value by default if it is empty and required
import GS_DropDown_Implementation
GS_DropDown_Implementation.SetDropDownDefaultvalue(Product)

#Hide the calculate button when the product is loaded