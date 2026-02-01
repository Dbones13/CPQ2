def labor_Calculated_hrs(attrs):
    #CXCPQ-25774 Saqlain Malik
    proT = attrs.project_type
    ai = attrs.AI
    ao = attrs.AO
    di = attrs.DI
    do = attrs.DO
    unP = attrs.unreleased_product
    pcl = attrs.num_cim
    mdb = attrs.marshalling_db
    A = attrs.num_rg
    proT = 0
    unP = 0
    mdb = 0
    C = ai + ao + di + do
    if attrs.project_type == 'New':
        proT = 0
    elif attrs.project_type == 'Expansion':
        proT = 1
    #base
    if C <=400:
        base = 8
    elif C>400 and C<=2000:
        base = 16
    elif C>2000 and C<=5000:
        base = 40
    elif C>=5000:
        base = 40
    HW =HW ="{0:.2f}".format((0.1 * (1.1 * (48 +float( C) / 200 + 2 * pcl + 0.5) + 2 * float(A) / float((A+ 1)) + 1 + float((1 + 3 * mdb)**2) + 4 * float(unP))) + 10 *float(proT))
    Hrs = float(HW) + float(base)
    
    return Hrs