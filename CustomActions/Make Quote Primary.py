import GS_CommonModule as cm

if cm.getCFValue(Quote, "IsPrimaryAllowed") == "1":
    cm.setCFValue(Quote, "IsPrimary", '1')
    Quote.RefreshActions()
    Quote.Save(False)