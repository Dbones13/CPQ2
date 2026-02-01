import GS_SerC_parts
CurrentTab=Product.Tabs.GetByName('Part Summary').IsSelected
if CurrentTab==True:
    Product.Attr('CurrentTab_Is_partsummery').AssignValue('Part Summary')
    Trace.Write("correct")
    Product.ApplyRules()
else:
    Product.Attr('CurrentTab_Is_partsummery').AssignValue('OtherTab')