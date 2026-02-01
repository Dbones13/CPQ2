#to add a row in Scope summary Product Container:
QCS_Cont = Product.GetContainerByName('SC_QCS_Product_Container')
QCS_Cont.Clear()
Tier = Product.Attr('SC_QCS_Subscription Tier').GetValue()
i = QCS_Cont.AddNewRow()
i['Service Product'] =  'QCS 4.0'
i['Entitlement'] = Tier
i['ServiceProductEntitlementPair'] = i['Service Product'] + '|' + i['Entitlement']
QCS_Cont.Calculate()
#Change product status as incomplete
Product.Attr('SC_Product_Status').AssignValue("0")
#ScriptExecutor.Execute('PS_QCS_Scope_Summary_2nd_container_populate')