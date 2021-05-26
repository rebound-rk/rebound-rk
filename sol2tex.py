import os
def sol2tex(solfilename,ROUNDS,inround,inbound):
    v = []
    objectValue = 0
    with open(solfilename, 'r') as f:
        line = f.read()
        lines = line.split('\n')
        objectValue = int(float(lines[1].split(' ')[-1])+0.1)
        for l in range(2,len(lines)-1):
            v.append(int(float(lines[l].split(' ')[-1])+0.1))

    kstates = []
    for r in range(0,2):
        kstate = []
        for i in range(0,4):
            row= []
            for j in range(0,4):
                row.append(int(v[r*16+4*i+j]+0.1))
            kstate.append(row)
        kstates.append(kstate)

    xstates = []
    for r in range(0,ROUNDS+1):
        xstate = []
        for i in range(0,4):
            row= []
            for j in range(0,4):
                row.append(int(v[2*16+r*16+4*i+j]+0.1))
            xstate.append(row)
        xstates.append(xstate)

    ystates = []
    for r in range(0,ROUNDS):
        ystate = []
        for i in range(0,4):
            row= []
            for j in range(0,4):
                row.append(int(v[2*16+(ROUNDS+1)*16+r*16+4*i+j]+0.1))
            ystate.append(row)
        ystates.append(ystate)
    pstate = []
    for i in range(0,4):
        row = []
        for j in range(0,4):
            row.append(int(v[2*16+(ROUNDS+1+ROUNDS)*16+4*i+j]+0.1))
        pstate.append(row)

    texfilename = solfilename +'.tex'
    f = open(texfilename, 'w+')
    head = r'''
    \documentclass{standalone}
\usepackage{tikz}
\usepackage{calc}
\usepackage{pgffor}
\usetikzlibrary{patterns}

\tikzset{%
    base/.style = {draw=black, minimum width=0.02cm, minimum height=0.02cm,
                    align=center, on chain},
myarrows/.style = {-stealth, thick},% <-- added on request in comment
myline/.style = {thick},
input/.style = {rectangle, text width=2em, text centered,
    minimum height=2em, base, fill=purple!30},
shift_bit/.style = {circle, text width=1.5em,
    minimum height=.1em,  base, fill=white!30},
and/.style = {circle, text width=0.4em, text centered, minimum height=0.2em, base, fill=red!30},
xor/.style = {},
    }

\begin{document}

\begin{tikzpicture}[scale=0.3]

\begin{scope}[yshift =0 cm,xshift = 0 cm]

    '''
    print(head,file = f)

    tail=r'''
    %\node[scale=0.8] ()  [xor]  at (7.5, 8)     {$Plaintext$};
    %\node[scale=0.8] ()  [xor]  at (18.5, 8)     {$Kr$};
    %\node[scale=0.8] ()  [xor]  at (32.5, 8)     {$K$};

    %\draw(1,5) grid + (4,4);
    %\draw(13,5) grid + (4,4);
    %\draw(27,5) grid + (4,4);
    \end{scope}
\end{tikzpicture}
\end{document}
'''

    for r in range(0,ROUNDS):
        if r<inround or r > inround +inbound-1:
            for i in range(0,4):
                for j in range(0,4):
                    if kstates[(r+1)%2][i][j] == 1:
                        print(r'\fill[gray]('+str(3+j)+r','+str(1-i-7*r)+r') rectangle +(1,1);',file=f)
                        if r==inround +inbound:
                            print(r'\fill[red]('+str(3+j)+r','+str(1-i-7*r)+r') rectangle +(1,1);',file=f)
                    if xstates[r][i][j] == 1:
                        print(r'\fill[gray]('+str(10+j)+r','+str(1-i-7*r)+r') rectangle +(1,1);',file=f)
                        print(r'\fill[gray]('+str(17+j)+r','+str(1-i-7*r)+r') rectangle +(1,1);',file=f)
                        if r==inround-1:
                            print(r'\fill[red]('+str(17+j)+r','+str(1-i-7*r)+r') rectangle +(1,1);',file=f)
                    if ystates[r][i][j] == 1:
                        print(r'\fill[gray]('+str(24+j)+r','+str(1-i-7*r)+r') rectangle +(1,1);',file=f)
                        if r==inround-1:
                            print(r'\fill[red]('+str(24+j)+r','+str(1-i-7*r)+r') rectangle +(1,1);',file=f)
        else:
            for i in range(0,4):
                for j in range(0,4):
                    if kstates[(r+1)%2][i][j] == 1:
                        print(r'\fill[red]('+str(3+j)+r','+str(1-i-7*r)+r') rectangle +(1,1);',file=f)
                    if xstates[r][i][j] == 1:
                        print(r'\fill[red]('+str(10+j)+r','+str(1-i-7*r)+r') rectangle +(1,1);',file=f)
                        print(r'\fill[red]('+str(17+j)+r','+str(1-i-7*r)+r') rectangle +(1,1);',file=f)
                    if ystates[r][i][j] == 1:
                        print(r'\fill[red]('+str(24+j)+r','+str(1-i-7*r)+r') rectangle +(1,1);',file=f)
        print(r'\node[scale=0.8] ()  [xor]  at (33,'+str(0-7*r) +r')     {$Round\ '+str(r)+r'$};',file = f)
    for r in range(0,ROUNDS):
        for i in range(0,4):
            print(r'\draw('+str(3+7*i)+r','+str(-2-7*r)+r') grid + (4,4);',file = f)
        for i in range(0,3):
            print(r'\draw[myarrows] ('+str(7+7*i)+r','+str(-7*r)+r') to ('+str(10+7*i)+r','+str(-7*r)+r');',file = f)
        print(r'\node[scale=0.8] ()  [xor]  at (8.5, '+str(-1.3-7*r)+r')     {$AK$};',file = f)
        print(r'\node[scale=0.8] ()  [xor]  at (15.5, '+str(-1.3-7*r)+r')     {$S$};',file = f)
        if r%2==0:
            print(r'\node[scale=0.8] ()  [xor]  at (22.5, '+str(-1.3-7*r)+r')     {$MR$};',file = f)
        else:
            print(r'\node[scale=0.8] ()  [xor]  at (22.5, '+str(-1.3-7*r)+r')     {$MC$};',file = f)
    
    for i in range(0,4):
        for j in range(0,4):
            if pstate[i][j] == 1:
                print(r'\fill[gray]('+str(10+j)+r','+str(8-i)+r') rectangle +(1,1);',file=f)
            if kstates[(ROUNDS+1)%2][i][j] ==1:
                print(r'\fill[gray]('+str(3+j)+r','+str(1-7*ROUNDS-i)+r') rectangle +(1,1);',file=f)
            if xstates[ROUNDS][i][j] == 1:
                print(r'\fill[gray]('+str(10+j)+r','+str(1-7*ROUNDS-i)+r') rectangle +(1,1);',file=f)

    print(r'\draw(10,5) grid + (4,4);',file = f)
    print(r'\draw[ thick] (10,7)|- +(-1.5,0) |- +(-1.5,-7);',file = f)


    print(r'\draw('+str(3)+r','+str(-2-7*ROUNDS)+r') grid + (4,4);',file = f)
    print(r'\draw('+str(10)+r','+str(-2-7*ROUNDS)+r') grid + (4,4);',file = f)
    print(r'\node[scale=0.8] ()  [xor]  at (8.5, '+str(-1.3-7*ROUNDS)+r')     {$AK$};',file = f)
    print(r'\draw[myarrows] ('+str(7)+r','+str(-7*ROUNDS)+r') to ('+str(10)+r','+str(-7*ROUNDS)+r');',file = f)
    print(r'\node (XOR1)  [xor]  at ('+str(8.5)+r','+str(-7*ROUNDS)+r')    {$\bigoplus$};',file=f)

    for r in range(0,ROUNDS):
        print(r'    \draw[ thick] (28,'+str(-7*r)+r')|- +(1.5,'+str(0)+r') |- +(-19.5,'+str(-4)+r') |- +(-19.5,'+str(-7)+r');',file=f)
        print(r'\node (XOR1)  [xor]  at ('+str(8.5)+r','+str(-7*r)+r')    {$\bigoplus$};',file=f)
    print(r'\node[scale=0.8] ()  [xor]  at (33,7)     {$Plaintext$};',file = f)
    print(r'\node[scale=0.8] ()  [xor]  at (33,'+str(-7*ROUNDS)+r')     {$Ciphertext$};',file = f)

    print(r'\node[scale=0.8] ()  [xor]  at (3, 8)     {$Canceled\ '+str(objectValue)+ r'$};',file=f)

    print(tail,file = f)
    f.close()

    os.system('xelatex '+texfilename)

def checkSol8r(solfilename):
    ROUNDS = 8
    v = []
    objectValue = 0
    with open(solfilename, 'r') as f:
        line = f.read()
        lines = line.split('\n')
        objectValue = int(float(lines[1].split(' ')[-1])+0.1)
        for l in range(2,len(lines)-1):
            v.append(int(float(lines[l].split(' ')[-1])+0.1))

    kstates = []
    for r in range(0,2):
        kstate = []
        for i in range(0,4):
            row= []
            for j in range(0,4):
                row.append(int(v[r*16+4*i+j]+0.1))
            kstate.append(row)
        kstates.append(kstate)

    xstates = []
    for r in range(0,ROUNDS+1):
        xstate = []
        for i in range(0,4):
            row= []
            for j in range(0,4):
                row.append(int(v[2*16+r*16+4*i+j]+0.1))
            xstate.append(row)
        xstates.append(xstate)

    ystates = []
    for r in range(0,ROUNDS):
        ystate = []
        for i in range(0,4):
            row= []
            for j in range(0,4):
                row.append(int(v[2*16+(ROUNDS+1)*16+r*16+4*i+j]+0.1))
            ystate.append(row)
        ystates.append(ystate)
    pstate = []
    for i in range(0,4):
        row = []
        for j in range(0,4):
            row.append(int(v[2*16+(ROUNDS+1+ROUNDS)*16+4*i+j]+0.1))
        pstate.append(row)
    flag = 1
    ans = [kstates,xstates,ystates]

    if flag==1:
        r0 = []
        r4 = []
        r6 = []
        for j in range(0,4):
            if xstates[0][3][j] == 0:
                r0.append(1)
            else:
                r0.append(0)
            if xstates[4][3][j] == 0:
                r4.append(1)
            else:
                r4.append(0)
            if xstates[6][3][j] == 0:
                r6.append(1)
            else:
                r6.append(0)
        for j in range(0,4):
            if kstates[0][3][j] == 1 and xstates[1][3][j] == 0:
                r0.append(1)
            else:
                r0.append(0)
            if kstates[0][3][j] == 1 and xstates[5][3][j] == 0:
                r4.append(1)
            else:
                r4.append(0)
            if kstates[0][3][j] == 1 and xstates[7][3][j] == 0:
                r6.append(1)
            else:
                r6.append(0)
        rr = 0
        for i in range(0,8):
            rr+=r0[i]*r4[i]
        if rr>=4:
            if (r0!=r4):
                flag = 0
        rr = 0
        for i in range(0,8):
            rr+=r0[i]*r6[i]
        if rr>=4:
            if (r0!=r6):
                flag = 0
        rr = 0
        for i in range(0,8):
            rr+=r4[i]*r6[i]
        if rr>=4:
            if (r4!=r6):
                flag = 0
    if flag==1:
        r0 = []
        r4 = []
        r6 = []
        for j in range(0,4):
            if xstates[0][2][j] == 0:
                r0.append(1)
            else:
                r0.append(0)
            if xstates[4][2][j] == 0:
                r4.append(1)
            else:
                r4.append(0)
            if xstates[6][2][j] == 0:
                r6.append(1)
            else:
                r6.append(0)
        for j in range(0,4):
            if kstates[0][2][j] == 1 and xstates[1][2][j] == 0:
                r0.append(1)
            else:
                r0.append(0)
            if kstates[0][2][j] == 1 and xstates[5][2][j] == 0:
                r4.append(1)
            else:
                r4.append(0)
            if kstates[0][2][j] == 1 and xstates[7][2][j] == 0:
                r6.append(1)
            else:
                r6.append(0)
        rr = 0
        for i in range(0,8):
            rr+=r0[i]*r4[i]
        if rr>=4:
            if (r0!=r4):
                flag = 0
        rr = 0
        for i in range(0,8):
            rr+=r0[i]*r6[i]
        if rr>=4:
            if (r0!=r6):
                flag = 0
        rr = 0
        for i in range(0,8):
            rr+=r4[i]*r6[i]
        if rr>=4:
            if (r4!=r6):
                flag = 0
        
    if flag==1:
        r0 = []
        r4 = []
        r6 = []
        for j in range(0,4):
            if xstates[0][1][j] == 0:
                r0.append(1)
            else:
                r0.append(0)
            if xstates[4][1][j] == 0:
                r4.append(1)
            else:
                r4.append(0)
            if xstates[6][1][j] == 0:
                r6.append(1)
            else:
                r6.append(0)
        for j in range(0,4):
            if kstates[0][1][j] == 1 and xstates[1][1][j] == 0:
                r0.append(1)
            else:
                r0.append(0)
            if kstates[0][1][j] == 1 and xstates[5][1][j] == 0:
                r4.append(1)
            else:
                r4.append(0)
            if kstates[0][1][j] == 1 and xstates[7][1][j] == 0:
                r6.append(1)
            else:
                r6.append(0)
        rr = 0
        for i in range(0,8):
            rr+=r0[i]*r4[i]
        if rr>=4:
            if (r0!=r4):
                flag = 0
        rr = 0
        for i in range(0,8):
            rr+=r0[i]*r6[i]
        if rr>=4:
            if (r0!=r6):
                flag = 0
        rr = 0
        for i in range(0,8):
            rr+=r4[i]*r6[i]
        if rr>=4:
            if (r4!=r6):
                flag = 0

    if flag==1:
        r0 = []
        r4 = []
        r6 = []
        for j in range(0,4):
            if xstates[0][0][j] == 0:
                r0.append(1)
            else:
                r0.append(0)
            if xstates[4][0][j] == 0:
                r4.append(1)
            else:
                r4.append(0)
            if xstates[6][0][j] == 0:
                r6.append(1)
            else:
                r6.append(0)
        for j in range(0,4):
            if kstates[0][0][j] == 1 and xstates[1][0][j] == 0:
                r0.append(1)
            else:
                r0.append(0)
            if kstates[0][0][j] == 1 and xstates[5][0][j] == 0:
                r4.append(1)
            else:
                r4.append(0)
            if kstates[0][0][j] == 1 and xstates[7][0][j] == 0:
                r6.append(1)
            else:
                r6.append(0)
        rr = 0
        for i in range(0,8):
            rr+=r0[i]*r4[i]
        if rr>=4:
            if (r0!=r4):
                flag = 0
        rr = 0
        for i in range(0,8):
            rr+=r0[i]*r6[i]
        if rr>=4:
            if (r0!=r6):
                flag = 0
        rr = 0
        for i in range(0,8):
            rr+=r4[i]*r6[i]
        if rr>=4:
            if (r4!=r6):
                flag = 0
    return flag

if __name__ == "__main__":
    sol2tex("Saturnin_rebound_7r.sol",7,3,2)

