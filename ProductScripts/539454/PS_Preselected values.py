def getattvalue(attName):
    return Product.Attr(attName)

expHwSelect = getattvalue('OPM_Experion_Server_Hardware_Selection')
attr1 = getattvalue('OPM_ACET_EAPP_Server_Hardware_Selection')
attr2 = getattvalue('OPM_EST_Tower_Hardware_Selection')
attr3 = getattvalue('OPM_ESC_ESF_or_ESCE_Tower_Hardware_Selection')
attr4 = getattvalue('OPM_Other_Servers_Hardware_Selection')
attr5 = getattvalue('OPM_RESS_Server_configuration')
attr6 = getattvalue('OPM_Select_RESS_platform_configuration')
attr7 = getattvalue('ATT_OPMNUMRESS')

if expHwSelect.GetValue() == '':
    defaultValue = 'HP DL 320 G11'
    firstAllowedValue = ''
    for value in expHwSelect.Values:
        if value.Allowed and firstAllowedValue == '':
            firstAllowedValue = value.Display
        if value.Allowed and value.Display in (defaultValue):
            expHwSelect.SelectDisplayValue(defaultValue)
    if expHwSelect.GetValue() == '':
        expHwSelect.SelectDisplayValue(firstAllowedValue)

if attr1.GetValue() == '':
    defaultValue = 'HP DL 320 G11'
    firstAllowedValue = ''
    for value in attr1.Values:
        if value.Allowed and firstAllowedValue == '':
            firstAllowedValue = value.Display
        if value.Allowed and value.Display in (defaultValue):
            attr1.SelectDisplayValue(defaultValue)
    if attr1.GetValue() == '':
        attr1.SelectDisplayValue(firstAllowedValue)
        
if attr2.GetValue() == '':
    defaultValue = 'Dell T5860XL'
    firstAllowedValue = ''
    for value in attr2.Values:
        if value.Allowed and firstAllowedValue == '':
            firstAllowedValue = value.Display
        if value.Allowed and value.Display in (defaultValue):
            attr2.SelectDisplayValue(defaultValue)
    if attr2.GetValue() == '':
        attr2.SelectDisplayValue(firstAllowedValue)
        
if attr3.GetValue() == '':
    defaultValue = 'Dell T5860XL'
    firstAllowedValue = ''
    for value in attr3.Values:
        if value.Allowed and firstAllowedValue == '':
            firstAllowedValue = value.Display
        if value.Allowed and value.Display in (defaultValue):
            attr3.SelectDisplayValue(defaultValue)
    if attr3.GetValue() == '':
        attr3.SelectDisplayValue(firstAllowedValue)
        
if attr4.GetValue() == '':
    defaultValue = 'HP DL 320 G11'
    firstAllowedValue = ''
    for value in attr4.Values:
        if value.Allowed and firstAllowedValue == '':
            firstAllowedValue = value.Display
        if value.Allowed and value.Display in (defaultValue):
            attr4.SelectDisplayValue(defaultValue)
    if attr4.GetValue() == '':
        attr4.SelectDisplayValue(firstAllowedValue)
        
if attr5.GetValue() == '':
    defaultValue = 'Physical'
    firstAllowedValue = ''
    for value in attr5.Values:
        if value.Allowed and firstAllowedValue == '':
            firstAllowedValue = value.Display
        if value.Allowed and value.Display in (defaultValue):
            attr5.SelectDisplayValue(defaultValue)
    if attr5.GetValue() == '':
        attr5.SelectDisplayValue(firstAllowedValue) 

if attr6.GetValue() == '':
    defaultValue = 'DELL R360 MLK'
    firstAllowedValue = ''
    for value in attr6.Values:
        if value.Allowed and firstAllowedValue == '':
            firstAllowedValue = value.Display
        if value.Allowed and value.Display in (defaultValue):
            attr6.SelectDisplayValue(defaultValue)
    if attr6.GetValue() == '':
        attr6.SelectDisplayValue(firstAllowedValue)

if attr7.GetValue() == '':
    defaultValue = '0'
    firstAllowedValue = ''
    for value in attr7.Values:
        if value.Allowed and firstAllowedValue == '':
            firstAllowedValue = value.Display
        if value.Allowed and value.Display in (defaultValue):
            attr7.SelectDisplayValue(defaultValue)
    if attr7.GetValue() == '':
        attr7.SelectDisplayValue(firstAllowedValue)