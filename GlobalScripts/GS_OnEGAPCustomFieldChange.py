'''Trace.Write("Lable {}".format(sender.Label))
Trace.Write("NewValue {} OldValue{}".format(arg.NewValue, arg.OldValue))'''
if Quote.GetCustomField('EGAP_Ques_CR1a').Label == sender.Label:
    Trace.Write("Payment_Terms {}".format(Quote.GetCustomField('EGAP_Credit_Payment_Terms').Content))
    Trace.Write("NewValue {} OldValue{}".format(arg.NewValue, arg.OldValue))
    creditPaymentTerms = Quote.GetCustomField('EGAP_Credit_Terms_Months').Content
    if creditPaymentTerms is not None and creditPaymentTerms.strip() != '':
        creditPaymentTerms = int(creditPaymentTerms)
    else:
        creditPaymentTerms = 0
    Quote.GetCustomField('EGAP_Risk_Count_CR1a').Content = Quote.GetCustomField('EGAP_Risk_Count_CR1b').Content = '0'
    if arg.NewValue == 'Yes' or creditPaymentTerms >= 60:
        Quote.GetCustomField('EGAP_Risk_Count_CR1a').Content = Quote.GetCustomField('EGAP_Risk_Count_CR1b').Content = '1'
elif Quote.GetCustomField('EGAP_Ques_CR3a').Label == sender.Label or Quote.GetCustomField('EGAP_Ques_CR3b').Label == sender.Label:
    cR3a = Quote.GetCustomField('EGAP_Ques_CR3a').Content
    cR3b = Quote.GetCustomField('EGAP_Ques_CR3b').Content
    Quote.GetCustomField('EGAP_Risk_Count_CR3a').Content = Quote.GetCustomField('EGAP_Risk_Count_CR3b').Content = Quote.GetCustomField('EGAP_Risk_Count_CR3c').Content = Quote.GetCustomField('EGAP_Risk_Count_CR3d').Content = '0'
    if cR3a == 'Yes':
        Quote.GetCustomField('EGAP_Risk_Count_CR3a').Content = Quote.GetCustomField('EGAP_Risk_Count_CR3b').Content = Quote.GetCustomField('EGAP_Risk_Count_CR3c').Content = Quote.GetCustomField('EGAP_Risk_Count_CR3d').Content = '4'
    elif cR3b == 'Yes':
        Quote.GetCustomField('EGAP_Risk_Count_CR3a').Content = Quote.GetCustomField('EGAP_Risk_Count_CR3b').Content = Quote.GetCustomField('EGAP_Risk_Count_CR3c').Content = Quote.GetCustomField('EGAP_Risk_Count_CR3d').Content = '1'
    else:
        Quote.GetCustomField('EGAP_Risk_Count_CR3a').Content = Quote.GetCustomField('EGAP_Risk_Count_CR3b').Content = Quote.GetCustomField('EGAP_Risk_Count_CR3c').Content = Quote.GetCustomField('EGAP_Risk_Count_CR3d').Content = '0'
elif Quote.GetCustomField('EGAP_Ques_CR4a').Label == sender.Label or Quote.GetCustomField('EGAP_Ques_CR4b').Label == sender.Label:
    cR4a = Quote.GetCustomField('EGAP_Ques_CR4a').Content
    cR4b = Quote.GetCustomField('EGAP_Ques_CR4b').Content
    cR4c = Quote.GetCustomField('EGAP_Ques_CR4c').Content
    Quote.GetCustomField('EGAP_Risk_Count_CR4a').Content = Quote.GetCustomField('EGAP_Risk_Count_CR4b').Content = Quote.GetCustomField('EGAP_Risk_Count_CR4c').Content = '0'
    if cR4a == 'No' and cR4b == 'No' and cR4c == 'Yes':
        Quote.GetCustomField('EGAP_Risk_Count_CR4a').Content = Quote.GetCustomField('EGAP_Risk_Count_CR4b').Content = Quote.GetCustomField('EGAP_Risk_Count_CR4c').Content = '1'
elif Quote.GetCustomField('EGAP_Ques_CR5a').Label == sender.Label or Quote.GetCustomField('EGAP_Ques_CR5b').Label == sender.Label:
    cR5a = Quote.GetCustomField('EGAP_Ques_CR5a').Content
    cR5b = Quote.GetCustomField('EGAP_Ques_CR5b').Content
    Quote.GetCustomField('EGAP_Risk_Count_CR5a').Content = Quote.GetCustomField('EGAP_Risk_Count_CR5b').Content = Quote.GetCustomField('EGAP_Risk_Count_CR5c').Content = '0'
    if cR5a == cR5b and cR5a == 'No':
        Quote.GetCustomField('EGAP_Risk_Count_CR5a').Content = Quote.GetCustomField('EGAP_Risk_Count_CR5b').Content = Quote.GetCustomField('EGAP_Risk_Count_CR5c').Content = '1'
elif Quote.GetCustomField('EGAP_Ques_CR6a').Label == sender.Label or Quote.GetCustomField('EGAP_Ques_CR6b').Label == sender.Label:
    cR6a = Quote.GetCustomField('EGAP_Ques_CR6a').Content
    cR6b = Quote.GetCustomField('EGAP_Ques_CR6b').Content
    Quote.GetCustomField('EGAP_Risk_Count_CR6a').Content = Quote.GetCustomField('EGAP_Risk_Count_CR6b').Content = '0'
    if cR6a ==  'Yes' or cR6b == 'Yes':
        Quote.GetCustomField('EGAP_Risk_Count_CR6a').Content = Quote.GetCustomField('EGAP_Risk_Count_CR6b').Content = '1'
elif Quote.GetCustomField('EGAP_Ques_CR7a').Label == sender.Label or Quote.GetCustomField('EGAP_Ques_CR7b').Label == sender.Label or Quote.GetCustomField('EGAP_Ques_CR7c').Label == sender.Label:
    cR7a = Quote.GetCustomField('EGAP_Ques_CR7a').Content
    cR7b = Quote.GetCustomField('EGAP_Ques_CR7b').Content
    cR7c = Quote.GetCustomField('EGAP_Ques_CR7c').Content
    Quote.GetCustomField('EGAP_Risk_Count_CR7a').Content = Quote.GetCustomField('EGAP_Risk_Count_CR7b').Content = Quote.GetCustomField('EGAP_Risk_Count_CR7c').Content = '0'
    if cR7a == 'Yes' and (cR7b ==  'Yes' or cR7c == 'Yes'):
        Quote.GetCustomField('EGAP_Risk_Count_CR7a').Content = Quote.GetCustomField('EGAP_Risk_Count_CR7b').Content = Quote.GetCustomField('EGAP_Risk_Count_CR7c').Content = '1'
elif Quote.GetCustomField('EGAP_Ques_CR8a').Label == sender.Label:
    Quote.GetCustomField('EGAP_Risk_Count_CR8a').Content = '0'
    if Quote.GetCustomField('EGAP_Ques_CR8a').Content == 'Yes':
        Quote.GetCustomField('EGAP_Risk_Count_CR8a').Content = '1'
elif Quote.GetCustomField('EGAP_Ques_CR9a').Label == sender.Label or Quote.GetCustomField('EGAP_Ques_CR9b').Label == sender.Label:
    cR9a = Quote.GetCustomField('EGAP_Ques_CR9a').Content
    cR9b = Quote.GetCustomField('EGAP_Ques_CR9b').Content
    Quote.GetCustomField('EGAP_Risk_Count_CR9a').Content = Quote.GetCustomField('EGAP_Risk_Count_CR9b').Content = '0'
    if cR9a == cR9b and cR9a == 'Yes':
        Quote.GetCustomField('EGAP_Risk_Count_CR9a').Content = Quote.GetCustomField('EGAP_Risk_Count_CR9b').Content = '1'
elif Quote.GetCustomField('EGAP_CFR4_Ques').Label == sender.Label:
    Quote.GetCustomField('EGAP_ETR_Number').Editable = False
    Quote.GetCustomField('EGAP_ETR_Number').Required = False
    if arg.NewValue == 'Yes':
        Quote.GetCustomField('EGAP_ETR_Number').Editable = True
        #Quote.GetCustomField('EGAP_ETR_Number').Required = True
elif Quote.GetCustomField('EGAP_CTFR6_Ques').Label == sender.Label:
    Quote.GetCustomField('EGAP_CTFR7_Ques').Editable = Quote.GetCustomField('EGAP_CTFR8_Ques').Editable = False
    if arg.NewValue == 'Yes':
        Quote.GetCustomField('EGAP_CTFR7_Ques').Editable = Quote.GetCustomField('EGAP_CTFR8_Ques').Editable = True
elif Quote.GetCustomField('EGAP_RAFR1_Ques').Label == sender.Label:
    Quote.GetCustomField('EGAP_RAFR1_RQUP_Number').Editable = False
    Quote.GetCustomField('EGAP_RAFR1_RQUP_Number').Required = False
    if arg.NewValue == 'Yes':
        Quote.GetCustomField('EGAP_RAFR1_RQUP_Number').Editable = True
        #Quote.GetCustomField('EGAP_RAFR1_RQUP_Number').Required = True
elif Quote.GetCustomField('EGAP_RAFR2_Ques').Label == sender.Label:
    Quote.GetCustomField('EGAP_RAFR2_RQUP_Number').Editable = False
    Quote.GetCustomField('EGAP_RAFR2_RQUP_Number').Required = False
    if arg.NewValue == 'Yes':
        Quote.GetCustomField('EGAP_RAFR2_RQUP_Number').Editable = True