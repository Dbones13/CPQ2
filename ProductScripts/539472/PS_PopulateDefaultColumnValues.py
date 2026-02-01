def getContainer(Name):
    return Product.GetContainerByName(Name)

lmToELMM3Party = getContainer('LM_to_ELMM_3rd_Party_Items')
for row in lmToELMM3Party.Rows:
    if row.RowIndex > 1:
        break
    row['LM_to_ELMM_3rd_Party_Hardware_Weidmuller'] = '0'
    row['LM_to_ELMM_3rd_Party_Hardware_Interposing_Relays'] = '0'
    row['LM_to_ELMM_3rd_Party_Hardware_Others'] = '0'
    row['LM_to_ELMM_3rd_Party_Hardware_Cabinet'] = '0'
lmToELMM3Party.Calculate()