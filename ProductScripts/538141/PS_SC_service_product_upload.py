QCS_Cont = Product.GetContainerByName('SC_QCS_Product_Container')
QCS_Cont.Clear()
QCS_Cont.Calculate()
Tier = Product.Attr('SC_QCS_Subscription Tier').GetValue()
i = QCS_Cont.AddNewRow()
i['Service Product'] =  'QCS 4.0'
i['Entitlement'] = Tier
i['ServiceProductEntitlementPair'] = i['Service Product'] + '|' + i['Entitlement']
#QCS_Cont = Product.GetContainerByName('SC_QCS_Product_Container')
SC = int(Product.ParseString("<* AttSel(SC_QCS_Support_Center_Select) *>"))
if SC == 1:
    i = QCS_Cont.AddNewRow()
    i['Service Product'] =  'QCS Support Center'
    i['Entitlement'] = 'QCS Support Center Support'
    i['ServiceProductEntitlementPair'] = i['Service Product'] + '|' + i['Entitlement']
#if SC == 0:
#    Product.GetContainerByName('SC_QCS_Product_Container').DeleteRow(1)
QCS_Cont.Calculate()