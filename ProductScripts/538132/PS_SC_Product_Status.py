tabs = [tab.Name for tab in Product.Tabs if tab.IsSelected]
if 'Scope Summary' in tabs:
    Product.Attr('SC_Product_Status').AssignValue("1")