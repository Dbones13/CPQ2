def GS_Labor_Engineering_Calcs(attrs):
    ai = attrs.AI
    ao = attrs.AO
    di = attrs.DI
    do = attrs.DO
    mdb = float(attrs.marshalling_db)
    A = float(attrs.num_rg)
    mdb = 0
    C = ai + ao + di + do
    if attrs.marshalling_db == 'Yes':
        mdb = 1
    elif attrs.marshalling_db == 'No':
        mdb = 0
    if C <=400:
        base = 8
    elif C>400 and C<=2000:
        base = 16
    elif C>2000 and C<=5000:
        base = 40
    elif C>5000:
        base = 80
    HW = (0.19 * (1.1 * (C / 200  + 2 * A / (A+ 1) + (1 + 3 * mdb)**2 )))
    Hrs = HW + base
    return Hrs