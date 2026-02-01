tabs = [tab.Name for tab in Product.Tabs if tab.IsSelected]
allowed_count = 0
expected_count = 4
#condition to run the below script only on Labor Deliverables tab
if 'Labor Deliverables' in tabs:
    years_list = Product.Attr('Hardware_Engineering_Execution_Year').Values
    for year in years_list:
        allowed_count = allowed_count + 1 if year.Allowed else allowed_count
    #condition to run the below script only when the year attribute has more than the expected (4) items
    if allowed_count > expected_count:
        import datetime
        current_year = datetime.datetime.now().year
        #hide years which are less the current year or greater than current year + 4
        def hide_year(Product, current_year, attribute_name, expected_count, max_year ):
            years_list = Product.Attr(attribute_name).Values
            for year in years_list:
                if int(year.ValueCode) in range(current_year + 4, max_year):
                    Product.DisallowAttrValues(attribute_name, year.ValueCode)
                elif int(year.ValueCode) < current_year:
                    Product.DisallowAttrValues(attribute_name, year.ValueCode)

        max_year = 2037
        for attribute_name in ['Hardware_Engineering_Execution_Year']:
            hide_year(Product, current_year, attribute_name, expected_count, max_year)