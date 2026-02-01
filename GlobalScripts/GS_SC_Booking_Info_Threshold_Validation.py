Threshold = Quote.GetCustomField('SC_CF_Threshold').Content.strip()
if Threshold.isnumeric() == True and (int(Threshold) >= 0 and int(Threshold) < 101):
    Quote.GetCustomField('SC_CF_Threshold').Content = Threshold
else:
    Quote.GetCustomField('SC_CF_Threshold').Content = "20"