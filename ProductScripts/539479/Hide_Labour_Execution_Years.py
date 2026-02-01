#hide years which are less the current year or greater than current year + 4
def hide_year(Product, current_year, attribute_name, expected_count, max_year ):
    years_list = Product.Attr(attribute_name).Values
    for year in years_list:
        if int(year.ValueCode) in range(current_year + 4, max_year):
            Product.DisallowAttrValues(attribute_name, year.ValueCode)
        elif int(year.ValueCode) < current_year:
            Product.DisallowAttrValues(attribute_name, year.ValueCode)

def process_attrs():
    allowed_count = 0
    expected_count = 4
    execution_year_attrs = ["C300_Engineering_Execution_Year", "C300_Addnl_Cust_Del_Execution_Year"]
    for attr in execution_year_attrs:
        years_list = Product.Attr(attr).Values
        for year in years_list:
            allowed_count = allowed_count + 1 if year.Allowed else allowed_count

        #condition to run the below script only when the year attribute has more than the expected (4) items
        if allowed_count > expected_count:
            current_year = DateTime().Now.Year

            max_year = 2037
            for attribute_name in [attr]:
                hide_year(Product, current_year, attribute_name, expected_count, max_year)

tabs = [tab.Name for tab in Product.Tabs if tab.IsSelected]

#condition to run the below script only on Labor Deliverables tab
if 'Labor Deliverables' in tabs:
    process_attrs()