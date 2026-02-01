def getCF(quote , cfName):
	return quote.GetCustomField(cfName)

def getCFValue(quote , cfName):
	return getCF(quote , cfName).Content

def hideCF(customField):
	customField.Visible = False
    
def showCF(customField):
	customField.Visible = True
    
Contract = ['Contract New','Contract Renewal']
if Quote.GetCustomField('Quote Type').Content in Contract:
    if getCFValue(Quote , "Booking LOB") == "LSS":
        #hideCF(getCF(Quote , "EGAP_Do_Want_to_Chanage_Ans_of_Func_Ques"))
        #hideCF(getCF(Quote , "Project_Release_Flag"))
        #hideCF(getCF(Quote , "CF_ProjectId"))
        #hideCF(getCF(Quote , "Booking Country"))
        #hideCF(getCF(Quote , "Functional Currency of Entity"))
        #hideCF(getCF(Quote , "MPA Price Plan"))
        #hideCF(getCF(Quote , "MPA Threshold"))
        #hideCF(getCF(Quote , "Discount Request Reason"))
        #hideCF(getCF(Quote , "MPA Validity"))
        #hideCF(getCF(Quote , "EGAP_Project_Type"))
        #hideCF(getCF(Quote , "Parent Firm Revision"))
        #hideCF(getCF(Quote , "Booking Revision"))
        #showCF(getCF(Quote , "EGAP_Proposal_Type"))
        Quote.GetCustomField('EGAP_Proposal_Type').Rank = 10
        Quote.GetCustomField("EGAP_Contract_Start_Date").Label = "Multi Year Start Date"
        Quote.GetCustomField("EGAP_Contract_End_Date").Label = "Multi Year End Date"
        Quote.GetCustomField("EGAP_Project_Duration_Months").Label = "Contract Duration(Months) #N# Multi Year End Date -Multi Year Start date (In Months)"
        Quote.GetCustomField('EGAP_Contract_Start_Date').Rank = 40
        Quote.GetCustomField('EGAP_Contract_End_Date').Rank = 41
        Quote.GetCustomField('EGAP_Project_Duration_Months').Rank = 51
        #if Quote.OrderStatus.Name == 'Preparing':
            #Quote.GetCustomField('EGAP_Contract_Start_Date').Required = True
            #Quote.GetCustomField('EGAP_Contract_End_Date').Required = True
            #Quote.GetCustomField('EGAP_Proposal_Type').Required = True