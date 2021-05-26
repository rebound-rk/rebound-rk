import gurobipy as gp
from gurobipy import GRB
from sol2tex import *

def modelrk(model,a,b,c):
    model.addConstr(a + b - c >= 0)
    model.addConstr(a - b + c >= 0)
    model.addConstr(- a + b + c >= 0)

def modelrkc(model,a,b,c,rkc):
    model.addConstr(-b - rkc +1 >= 0)
    model.addConstr(c - rkc >= 0)
    model.addConstr(a - rkc >= 0)
    model.addConstr(-a +b -c + rkc + 1 >= 0)




if __name__ == "__main__":
    m = gp.Model("Saturnin_rebound")
    m.Params.Threads = 2
    ROUNDS = 8
    inround = 1
    inbound = 2

    k = m.addVars(2,4,4,vtype=GRB.BINARY, name="k") #Key difference
    x = m.addVars(ROUNDS+1,4,4,vtype=GRB.BINARY, name="x") #State difference before and after Sbox
    y = m.addVars(ROUNDS,4,4,vtype=GRB.BINARY, name="y") #State difference  after MR(or MC)
    p = m.addVars(4,4,vtype=GRB.BINARY, name="p") #Plain difference
    kc = m.addVars(ROUNDS+1,4,4,vtype=GRB.BINARY, name="kc") #is 1 if a cell of key difference cancel a state cell 
    mc = m.addVars(ROUNDS,4,vtype=GRB.INTEGER, name="mc") #the number of cells canceled by MR(or MC)
    mkc = m.addVars(ROUNDS,4,vtype=GRB.INTEGER, name="mkc") #counting the real probability
    free = 0

    #Model AK
    for i in range(0,4):
        for j in range(0,4):
            modelrkc(m,x[0,i,j],p[i,j],k[1,i,j],kc[0,i,j])
    for r in range(0,inround-1):
        for i in range(0,4):
            for j in range(0,4):
                modelrkc(m,x[r+1,i,j],y[r,i,j],k[r%2,i,j],kc[r+1,i,j])
    for r in range(inround+inbound,ROUNDS):
        for i in range(0,4):
            for j in range(0,4):
                modelrkc(m,y[r,i,j],x[r+1,i,j],k[r%2,i,j],kc[r+1,i,j])

    #Model key schedule
    for i in range(0,16):
        m.addConstr(k[1,i//4,i%4] == k[0,((i-5)%16)//4,((i-5)%16)%4])

    #Model whitning key addition
    for i in range(0,4):
        for j in range(0,4):
            modelrk(m,p[i,j],x[0,i,j],k[1,i,j])

    #Model cancellation of input and output
    if ROUNDS%2==0:
        for i in range(0,4):
            for j in range(0,4):
                m.addConstr(x[0,i,j] == y[ROUNDS-1,i,j])
    else:
        for i in range(0,4):
            for j in range(0,4):
                m.addConstr(p[i,j] == x[ROUNDS,i,j])

    #Model round function
    for r in range(0,ROUNDS):
        if r%2 == 0:
            for i in range(0,4):
                expr = 0
                temp = m.addVar(vtype=GRB.BINARY,name='temp_r'+str(r)+'_i'+str(i))
                for j in range(0,4):
                    expr += x[r,i,j] + y[r,i,j]
                    m.addConstr(x[r,i,j] <= temp)
                    m.addConstr(y[r,i,j] <= temp)
                m.addConstr(expr >= 5*temp)
                if r<inround-1:
                    m.addConstr(4*temp-x[r,i,0]-x[r,i,1]-x[r,i,2]-x[r,i,3]==mc[r,i])
                    temp1 = m.addVar(vtype=GRB.INTEGER)
                    temp2 = m.addVar(vtype=GRB.INTEGER)
                    m.addConstr(temp1 == 4*temp-x[r,i,0]-x[r,i,1]-x[r,i,2]-x[r,i,3])
                    m.addConstr(temp2 == x[r+1,i,0]+x[r+1,i,1]+x[r+1,i,2]+x[r+1,i,3])
                    m.addConstr(mkc[r,i] == gp.min_(temp1,temp2))
                    free += mc[r,i] - mkc[r,i]
                elif r>inround+inbound-1:
                    m.addConstr(4*temp-y[r,i,0]-y[r,i,1]-y[r,i,2]-y[r,i,3]==mc[r,i])
                    tempmk1 = m.addVar(vtype=GRB.INTEGER,name='tempmk1_r'+str(r)+"_i"+str(i))
                    tempmk2 = m.addVar(vtype=GRB.INTEGER,name='tempmk2_r'+str(r)+"_i"+str(i))
                    m.addConstr(tempmk1==mc[r,i]+kc[r+1,i,0]+kc[r+1,i,1]+kc[r+1,i,2]+kc[r+1,i,3])
                    m.addConstr(tempmk2==x[r,i,0]+x[r,i,1]+x[r,i,2]+x[r,i,3])
                    m.addConstr(mkc[r,i] == gp.min_(tempmk1,tempmk2))
                    free += tempmk1 - mkc[r,i]
       
            for i in range(0,4):
                for j in range(0,4):
                    modelrk(m,y[r,i,j],x[r+1,i,j],k[r%2,i,j])
        else:
            for j in range(0,4):
                expr = 0
                temp = m.addVar(vtype=GRB.BINARY)
                for i in range(0,4):
                    expr += x[r,i,j] + y[r,i,j]
                    m.addConstr(x[r,i,j] <= temp)
                    m.addConstr(y[r,i,j] <= temp)
                m.addConstr(expr >= 5*temp)
                if r<inround-1:
                    m.addConstr(4*temp-x[r,0,j]-x[r,1,j]-x[r,2,j]-x[r,3,j]==mc[r,j])
                    temp1 = m.addVar(vtype=GRB.INTEGER)
                    temp2 = m.addVar(vtype=GRB.INTEGER)
                    m.addConstr(temp1 == 4*temp-x[r,0,j]-x[r,1,j]-x[r,2,j]-x[r,3,j])
                    m.addConstr(temp2 == x[r+1,0,j]+x[r+1,1,j]+x[r+1,2,j]+x[r+1,3,j])
                    m.addConstr(mkc[r,j] == gp.min_(temp1,temp2))
                    free += mc[r,j] - mkc[r,j]
                elif r>inround+inbound-1:
                    m.addConstr(4*temp-y[r,0,j]-y[r,1,j]-y[r,2,j]-y[r,3,j]==mc[r,j])
                    tempmk1 = m.addVar(vtype=GRB.INTEGER,name='tempmk1_r'+str(r)+"_i"+str(j))
                    tempmk2 = m.addVar(vtype=GRB.INTEGER,name='tempmk2_r'+str(r)+"_i"+str(j))
                    m.addConstr(tempmk1==mc[r,j]+kc[r+1,0,j]+kc[r+1,1,j]+kc[r+1,2,j]+kc[r+1,3,j])
                    m.addConstr(tempmk2==x[r,0,j]+x[r,1,j]+x[r,2,j]+x[r,3,j])
                    m.addConstr(mkc[r,j] == gp.min_(tempmk1,tempmk2))
                    free += tempmk1 - mkc[r,j]

            for i in range(0,4):
                for j in range(0,4):
                    modelrk(m,y[r,i,j],x[r+1,i,j],k[r%2,i,j])

    #At least one input cell is active
    inputdiff = 0
    for i in range(0,4):
        for j in range(0,4):
            inputdiff += x[0,i,j]
    m.addConstr(inputdiff >= 1)

    #Model objective function
    objective = 0
    if ROUNDS%2==0:
        for r in range(0,ROUNDS+1):
            for i in range(0,4):
                if r < ROUNDS :
                    if r>inround:
                        objective += mkc[r,i]
                    else:
                        objective += mkc[r,i]
                for j in range(0,4):
                    if r<inround:
                        objective += kc[r,i,j]
        for i in range(0,4):
            for j in range(0,4):
                objective += x[0,i,j]
    else:
        for r in range(0,ROUNDS+1):
            for i in range(0,4):
                if r < ROUNDS :
                    if r>inround:
                        objective += mkc[r,i]
                    else:
                        objective += mkc[r,i]
                for j in range(0,4):
                    if r<inround:
                        objective += kc[r,i,j]
        for i in range(0,4):
            for j in range(0,4):
                objective += p[i,j]
    m.addConstr(objective <=15)

    #Model degree of freedom of key
    allkeyfree = 0
    for i in range(0,4):
        for j in range(0,4):
            allkeyfree += k[1,i,j]
    m.addConstr(free <=allkeyfree)

    #Non-full super S-box technique
    objective2 =  m.addVar(vtype=GRB.INTEGER)
    for r in range(inround,inround+1):
        temp1 = m.addVars(4,vtype=GRB.INTEGER)
        temp2 = m.addVars(4,vtype=GRB.INTEGER)
        if r%2==0:
            for i in range(0,4):
                m.addConstr(temp1[i] == x[r,i,0]+x[r,i,1]+x[r,i,2]+x[r,i,3]+x[r+1,i,0]+x[r+1,i,1]+x[r+1,i,2]+x[r+1,i,3])
        else:
            for j in range(0,4):
                m.addConstr(temp1[j] == x[r,0,j]+x[r,1,j]+x[r,2,j]+x[r,3,j]+x[r+1,0,j]+x[r+1,1,j]+x[r+1,2,j]+x[r+1,3,j])
        m.addConstr(objective2 == gp.max_(temp1[0],temp1[1],temp1[2],temp1[3]))
    #We can also set a  second priority objective function.
    #m.addConstr(objective2 <=5)

    # objective2 is the max number of active S-boxes in super sbox, so objective2-4 corresponds to the time to solve the inbound part.
    m.setObjective(objective+objective2-4,GRB.MINIMIZE)
    #m.write('Saturnin_rebound_'+str(ROUNDS)+'r.lp')
    m.optimize()
    solfilename = 'Saturnin_rebound_'+str(ROUNDS)+'r.sol'
    m.write(solfilename)
        

    
