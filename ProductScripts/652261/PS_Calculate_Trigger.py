Calculate_Trigger=False
sysContainer = Product.GetContainerByName("TPS_PRDContainerSys")
if sysContainer:
    for sysProd in sysContainer.Rows:
        if sysProd.Product.Attr('Calculation Button Trigger').GetValue() == 'Yes':
            Calculate_Trigger=True
if Calculate_Trigger:
    Product.Attr('Calculation Button Trigger').AssignValue('Yes')
else:
    Product.Attr('Calculation Button Trigger').AssignValue('No')