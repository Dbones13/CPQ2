class IAA:
    def __init__(self, Product):
        self.product = Product
        if Product.Name in ['MSID','Integrated Automation Assessment']:
            self.max_quantity = 1
        else:
            self.max_quantity = 200
    def ConvertToInt(self,val):
        if val == "":
            val = 0
        else:
            val=float(val)
            #val = int(val)
        Trace.Write("returned value--" + str(val))
        return val
    def PopulateIAAPricingContainerRows(self, pricing_list):
        containerName = "IAA Pricing"
        container = self.product.GetContainerByName(containerName)
        if container:
            for item in pricing_list:
                newRow = container.AddNewRow(False)
                newRow["Name"] = item
                container.Calculate()
    def ValidationForAssessment(self):
        iaa_input_cont = self.product.GetContainerByName("IAA Inputs_Cont")
        iaa_input_cont_2 = self.product.GetContainerByName("IAA Inputs_Cont_2")
        Trace.Write("MAX Quantity: " + str(self.max_quantity))
        for row in iaa_input_cont.Rows:
            if self.ConvertToInt(row['IAA_Quantity']) > self.max_quantity or self.ConvertToInt(row['IAA_Quantity']) < 0:
                row['IAA_Quantity'] = "0"
                row.Calculate()
                iaa_input_cont.Calculate()

        for row in iaa_input_cont_2.Rows:
            if self.ConvertToInt(row['Quantity']) > self.max_quantity or self.ConvertToInt(row['Quantity']) < 0:
                row['Quantity'] = "0"
                row.Calculate()
                iaa_input_cont_2.Calculate()
    def PopulateAssessmentRows(self):
        container = self.product.GetContainerByName("IAA Inputs_Cont")
        if container:
            assessments = ['Experion Standard IAA (0-{})'.format(self.max_quantity), 'LCN/TPS Standard IAA (0-{})'.format(self.max_quantity), 'Experion with TPS Standard IAA (0-{})'.format(self.max_quantity), 'Experion System Performance Baseline (0-{})'.format(self.max_quantity), 'LCN/TPS System Performance Baseline (0-{})'.format(self.max_quantity)]
            for assessment in assessments:
                row = container.AddNewRow(False)
                row["IAA_Assessment_Type"] = assessment
                container.Calculate()
        iaa_container_2 = self.product.GetContainerByName("IAA Inputs_Cont_2")
        if iaa_container_2:
            newRow = iaa_container_2.AddNewRow(False)
            newRow['Name'] = 'How many SPBs did the customer purchase in the last 12 months? (0-{})'.format(self.max_quantity)
            newRow['Quantity'] = "0"