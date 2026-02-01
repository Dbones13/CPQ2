if Quote.GetCustomField('cyberProductPresent').Content == 'Yes' or Quote.GetCustomField('cyberparts').Content == 'Yes':
    from GS_CyberGenerateDocument import cyber_proposal
    cyber_proposal(Quote)