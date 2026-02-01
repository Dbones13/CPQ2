Contract = ['Contract New','Contract Renewal']
l_QuoteType=Quote.GetCustomField('Quote Type').Content
if l_QuoteType in Contract:
    #16/11/2023 CXCPQ-60167
    #Start
    Contract_Name = Quote.GetCustomField('Account Name').Content[0:10] + '-' + Quote.GetCustomField('Account Site').Content[0:5] + '-' + Quote.GetCustomField('SC_CF_LOCAL_REF').Content
    #Added if-else block to add prefix to contract name for renewal quotes #CXCPQ-92749
    if l_QuoteType=='Contract New':
        Quote.GetCustomField('SC_CF_CONTRACT_NAME').Content = Contract_Name
    else:#contract Renewal
        Quote.GetCustomField('SC_CF_CONTRACT_NAME').Content = 'Q-'+ Contract_Name 
    #End