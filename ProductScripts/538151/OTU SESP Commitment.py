otu_msid = Product.GetContainerByName("OTU_SESP commitment")
sesp_commitment = ['1-Year SESP commitment','3-Year SESP commitment','5-Year SESP commitment']
for i in sesp_commitment:
    row = otu_msid.AddNewRow(True)
    row['SESP commitment']= i