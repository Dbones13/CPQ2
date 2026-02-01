import GS_ItemCalculations as ic

def setCFValue(field, value):
    Quote.GetCustomField(field).Content = value

totalExpedite = 0.0
ic.calculateExpediteFee(Quote , Item)
for item in Quote.Items:
    totalExpedite = float(totalExpedite) + float(item['QI_Expedite_Fees'].Value)
setCFValue('Expedite Fee', str(totalExpedite))