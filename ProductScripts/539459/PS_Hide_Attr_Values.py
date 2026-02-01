tabs = [tab.Name for tab in Product.Tabs if tab.IsSelected]
allowed_count = 0
expected_count = 4
#condition to run the below script only on Labor Deliverables tab
if 'Labor Deliverables' in tabs:
    years_list = Product.Attr('SM_Labor_Execution_Year').Values
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
        for attribute_name in ['SM_Labor_Execution_Year', 'SM_Labor_Execution_Year_adc']:
            hide_year(Product, current_year, attribute_name, expected_count, max_year)

def disallow(location, dropdownlist):
    if location:
        for i in dropdownlist:
            if i.Display in location:
                Trace.Write(i.Display)
                i.Allowed = False
            elif i.Display not in location:
                i.Allowed = True
def allow(location, dropdownlist):
    if location:
        for i in dropdownlist:
            if i.Display in location:
                Trace.Write(i.Display)
                i.Allowed = True
            elif i.Display not in location:
                i.Allowed = False

switch_io = Product.GetContainerByName('SM_Common_Questions').Rows[0].GetColumnByName("Experion Software Release").Value if Product.GetContainerByName('SM_Common_Questions').Rows.Count > 0 else ''
if Product.GetContainerByName('SM_Hardware_Simulation_Station_Cont').Rows.Count > 0 or Product.GetContainerByName('SM_Hardware_Builder_Station_Cont').Rows.Count > 0 or Product.GetContainerByName('SM_Hardware_Historian_Station_Cont').Rows.Count > 0:
    row = Product.GetContainerByName('SM_Hardware_Simulation_Station_Cont').Rows[0]
    row1 = Product.GetContainerByName('SM_Hardware_Builder_Station_Cont').Rows[0]
    row2 = Product.GetContainerByName('SM_Hardware_Historian_Station_Cont').Rows[0]
    list = row.GetColumnByName('Station_Type')
    list1 = row1.GetColumnByName('Station_Type')
    list2 = row2.GetColumnByName('Station_Type')
    value_list = list.ReferencingAttribute.Values
    value_list1 = list1.ReferencingAttribute.Values
    value_list2 = list2.ReferencingAttribute.Values
    location=['STN_PER_DELL_Tower_RAID1','STN_PER_DELL_Rack_RAID1','STN_STD_DELL_Tower_NonRAID','STN_PER_HP_Tower_RAID1']
    location1=['None']
    raid2_location = ['STN_PER_DELL_Tower_RAID2']
    if switch_io =="R530":
        allow(location, value_list)
        allow(location, value_list1)
        allow(location, value_list2)
        disallow(location1+raid2_location, value_list)
        disallow(location1+raid2_location, value_list1)
        disallow(location1+raid2_location, value_list2)
    elif switch_io =="R520":
        disallow(location+location1, value_list)
        disallow(location+location1, value_list1)
        disallow(location+location1, value_list2)
        allow(raid2_location, value_list)
        allow(raid2_location, value_list1)
        allow(raid2_location, value_list2)
    else:
        disallow(location+raid2_location, value_list)
        disallow(location+raid2_location, value_list1)
        disallow(location+raid2_location, value_list2)
        allow(location1, value_list)
        allow(location1, value_list1)
        allow(location1, value_list2)
Trace.Write('Rows Count5   '+str(Product.GetContainerByName('Labor_PriceCost_Cont').Rows.Count))