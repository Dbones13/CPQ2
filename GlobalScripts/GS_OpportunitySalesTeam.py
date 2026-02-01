salesTeam = Quote.GetCustomField('OpportunitySalesTeam').Content
listVal = salesTeam.split(',')
if salesTeam != '':
    count=1
    for a,b in zip(listVal[0].replace('EmployeeId:','').split('-'),listVal[-1].replace('Credit:','').split('-')):
        Trace.Write(a)
        Trace.Write(b)
        Quote.GetCustomField('CF_EID_'+str(count)).Content = a
        Trace.Write("Quote repeate"+str(a))
        Quote.GetCustomField('CF_EID_'+str(count)+'_Rate').Content = b
        Trace.Write("Quote rep"+str(b))
        count = count + 1