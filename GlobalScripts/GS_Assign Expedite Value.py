def getCFValue( field):
    return Quote.GetCustomField(field).Content

def setCFValue(cfName, Value):
    Quote.GetCustomField(cfName).Content = Value

if getCFValue("Sales Area") == '736P_INR':
    setCFValue("Expedite Fee", "0" )