Product.Attr('CMS Flex Station Qty 0_60').AssignValue('0')
Product.Attr('Cabinet_No_of_Displays (0-4)').AssignValue('1')
Product.Attr('CMS Console Station Qty 0_20').AssignValue('0')
Product.Attr('CMS Console Station Extension Qty 0_15').AssignValue('0')
Product.Attr('Cabinet_Trackball_required').SelectDisplayValue('No')
Product.Attr('Cabinet_Display_size').SelectDisplayValue('27 inch NTS NEC')
Product.Attr('CMS Flex Station Hardware Selection').SelectDisplayValue('STN_PER_DELL_Tower_RAID1')
Product.Attr('CMS Console Station Hardware Selection').SelectDisplayValue('STN_PER_DELL_Tower_RAID1')
Product.Attr('CMS TPS Station Hardware Selection').SelectDisplayValue('STN_PER_DELL_Rack_RAID1')
Product.Attr('CMS Console Station Extension Hardware Selection').SelectDisplayValue('STN_PER_DELL_Tower_RAID1')
ScriptExecutor.Execute('PS_CXDEV-7712')
ScriptExecutor.Execute('DMS HIde Cluster Cabinet Mounting Station')
ScriptExecutor.Execute('HIde Cluster Cabinet Mounting Station')
ScriptExecutor.Execute('PS_Cabinet_Display_Size')
ScriptExecutor.Execute('PS_Cab_desk_defaults')