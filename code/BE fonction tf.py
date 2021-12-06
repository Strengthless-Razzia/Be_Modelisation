def getTf(Kv, Ka ): #plus les param de la fct de calcul de la loi de mvmt
    maxv = 0
    maxa = 0
    tf=0,1
    
    #programme de Auré doit tourner pour récup Mv[] et Ma[] qui contiennent les données d'accélération et de vitesse
    
    for i in range(len(Mv)):
        if(Mv[i]>maxv):
            mavx = Mv[i]
    for j in range(len(Ma)):
        if(Ma[j]>maxa):
            maxa = Ma[j]
    if(maxv > Kv or maxa > Ka):
        tf = tf+0,1
    else :
        return tf
    