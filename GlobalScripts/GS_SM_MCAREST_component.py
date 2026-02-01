import math as m
import System.Decimal as D
def roundup(n):
    res = int(n)
    return res if res == n else res+1
def get_int(val):
    if val:
        return int(val)
    return 0

def get_MCAREST(SUMUIONIS,SUMUION,SUMUIORIS,SUMUIOR,SUMDIONIS,SUMDION,SUMDIORIS,SUMDIOR,TCNT11):
    MCAREST = roundup((roundup(SUMUIONIS/32.0) + roundup(SUMUION/32.0) + roundup(SUMUIORIS/32.0) + roundup(SUMUIOR/32.0) + roundup(SUMDIONIS/32.0) + roundup(SUMDION/32.0) + roundup(SUMDIORIS/32.0) + roundup(SUMDIOR/32.0))/3.0) + roundup(TCNT11/2.0)
    Trace.Write("-----------------------------")
    Trace.Write("SUMUIONIS:"+str(SUMUIONIS))
    Trace.Write("SUMUION:"+str(SUMUION))
    Trace.Write("SUMUIORIS: "+str(SUMUIORIS))
    Trace.Write("SUMUIOR: "+str(SUMUIOR))
    Trace.Write("SUMDIONIS: "+str(SUMDIONIS))
    Trace.Write("SUMDION: "+str(SUMDION))
    Trace.Write("SUMDIORIS: "+str(SUMDIORIS))
    Trace.Write("SUMDIOR: "+str(SUMDIOR))
    Trace.Write("TCNT11:"+str(TCNT11))
    return D.Ceiling(MCAREST)
#CXCPQ-31082

def get_BCUFREST(MCAREST):
    BCUFREST = 0
    BCUFREST = D.Ceiling(MCAREST/7.0)
    return BCUFREST
#CXCPQ-31131
def get_FDBCUFR(BCUFREST):
    FDBCUFR = 0
    FDBCUFR = get_int(5*BCUFREST)
    return FDBCUFR
#CXCPQ-31134
def get_FC_PUIO01(FDBCUFR,SUMUION,SUMUIONIS,SUMUIOR,SUMUIORIS):
    p1=m.ceil((FDBCUFR+SUMUION+SUMUIONIS)/32.0)
    if SUMUION+SUMUIONIS==0:
        qnt=p1+2*m.ceil((SUMUIOR+SUMUIORIS)/32.0)
    elif SUMUION+SUMUIONIS>0:
        qnt=p1+2*m.ceil((SUMUIOR+SUMUIORIS)/32.0)
    return int(qnt)
#CXCPQ- 31136
def get_FC_PDIO01(FDBCUFR,SUMDION,SUMDIONIS,SUMDIOR,SUMDIORIS):
    FC_PDIO01 = 0
    FC_PDIO01 = m.ceil((SUMDION+SUMDIONIS)/32.0)
    if SUMDION+SUMDIONIS== 0:
        FC_PDIO01 += 2*(m.ceil((SUMDIOR+SUMDIORIS)/32.0))
    elif SUMDION+SUMDIONIS>0:
        FC_PDIO01 += 2*(m.ceil((SUMDIOR+SUMDIORIS)/32.0))
    return (int(FC_PDIO01))
#CXCPQ-31139
def get_FC_TUIO11(FDBCUFR,SUMUION,SUMUIONIS,SUMUIOR,SUMUIORIS):
    Trace.Write("FDBCUFR:"+str(FDBCUFR))
    Trace.Write("SUMUION: "+str(SUMUION))
    Trace.Write("SUMUIONIS :"+str(SUMUIONIS))
    Trace.Write("SUMUIOR "+str(SUMUIOR))
    Trace.Write("SUMUIORIS "+str(SUMUIORIS))
    FC_TUIO11=0
    FC_TUIO11+=D.Ceiling((FDBCUFR+SUMUION+SUMUIONIS)/32.0)
    Trace.Write("b1:"+str(FC_TUIO11))
    if int(SUMUION)==0 and int(SUMUIONIS)==0 and int(SUMUIOR)==0 and int(SUMUIORIS)==0:
        FC_TUIO11+=D.Ceiling((FDBCUFR)/32.0)
    Trace.Write("c1:"+str(FC_TUIO11))
    if SUMUION+SUMUIONIS==0:
        FC_TUIO11+=D.Ceiling((SUMUIOR+SUMUIORIS)/32.0)
    else:
        FC_TUIO11+=D.Ceiling((SUMUIOR+SUMUIORIS)/32.0)
    Trace.Write("f1:"+str(FC_TUIO11))
    return (int(FC_TUIO11))
#CXCPQ-31140
def get_FC_TDIO11(FDBCUFR,SUMDION,SUMDIONIS,SUMDIOR,SUMDIORIS):
    Trace.Write("FDBCUFR:"+str(FDBCUFR))
    Trace.Write("SUMDION:"+str(SUMDION))
    Trace.Write("SUMDIONIS:"+str(SUMDIONIS))
    Trace.Write("SUMDIOR"+str(SUMDIOR))
    Trace.Write("SUMDIORIS:"+str(SUMDIORIS))
    FC_TDIO11=0
    FC_TDIO11=D.Ceiling((SUMDION+SUMDIONIS)/32.0)
    Trace.Write("a1: "+str(FC_TDIO11))
    '''if int(SUMDIOR)==0 and int(SUMDIORIS)==0 and int(SUMDION)==0 and int(SUMDIONIS)==0:
        FC_TDIO11+=D.Ceiling((FDBCUFR)/32.0)'''
    Trace.Write("e:"+str(FC_TDIO11))
    if (SUMDION+SUMDIONIS)==0:
        Trace.Write("f:"+str(FC_TDIO11))
        FC_TDIO11+=D.Ceiling((SUMDIOR+SUMDIORIS)/32.0)
        Trace.Write("d2:"+str(FC_TDIO11))
    else:
        FC_TDIO11+=D.Ceiling((SUMDIOR+SUMDIORIS)/32.0)
    Trace.Write("d1:"+str(FC_TDIO11))
    return (int(FC_TDIO11))