import connect
import testUI
import pulldata
import genseq

def deflist():
    test_name = 'default'
    channelmode = 0
    channelmin = 1
    channelmax = 92
    channelfix = channelmin
    channelgap = 1
    channelcyc = 1
    channelseq = []
    pwrmode = 0
    (dummy16, pwrmin) = it.opsl()
    pwrmin = int(pwrmin)
    (dummy15, pwrmax) = it.opsh()
    pwrmax = int(pwrmax)
    pwrfix = pwrmax
    pwrgap = 1
    pwrcyc = 1
    pwrseq = []
    samplingL = 600
    samplingP = 1
    return ([test_name,channelmode,channelmin,channelmax,channelfix,\
channelgap,channelcyc,channelseq,pwrmode,pwrmin,pwrmax,pwrfix,pwrgap,pwrcyc,\
pwrseq,samplingL,samplingP])

if __name__ == '__main__':

    print 'Running connect.py'
    connect = open('connect.py','r')
    exec connect
    connect.close()
    

    print 'Running pulldata.py'
    pd = open('pulldata.py','r')
    exec pd
    pd.close()

    print 'Running genseq.py'
    gs = open('genseq.py','r')
    exec gs
    gs.close()    

    #parameters
    paramLs = []
    loadfromfile = input('load parameter(UI:0,file:1)')
    if loadfromfile:
        print'load from file'
        genfile = input('generate new file?(n:0,y:1):')
        if genfile:
            print'generate new file'
            gen_name = input('write to file name(put "" around):')
            gen_file= open("%s.csv"%(gen_name),"w")
            gen_file.write("testname,channelmode,channelmin,channelmax,channelfix,\
channelgap,channelcyc,channelseq,pwrmode,pwrmin,pwrmax,pwrfix,pwrgap,pwrcyc,\
pwrseq,samplingL,samplingP")
            gen_file.close()
            print'finish generating %s.csv'%(gen_name)
        else:
            print'using existing file'
            
        #open file
        try:
            test_name = input('read from file name(put "" around):')
            print'read from %s.csv'%(test_name)
            try:
                test_file = open("%s.csv"%(test_name),"r")
                lines = test_file.readlines()
                test_file.close()
            except:
                raise 'file is opened in another program'
        except:
            raise 'remember to put ""'
        lines = lines[1:]
        for line in lines:
            line = line.strip('\n')
            line = line.split(',')

            parseq = line[7]
            parseq = parseq.split(' ')
            intseq = []
            if parseq[0]:
                for i in range(len(parseq)):
                    numb = int(parseq[i])
                    intseq.append(numb)
            line[7]=intseq
    
            paramLs.append(line)
    else:
        print 'starting UI'
        print 'Running testUI.py'
        tUI = open('testUI.py','r')
        exec tUI
        tUI.close()
        x = testUI()
        paramLs = [x.startUI()]
        
    for paramL in paramLs:
        defln = deflist()
        for i in range(0,len(paramL)):
            if paramL[i]=='':
                paramL[i]=defln[i]
            elif type(paramL[i])==str:
                try:paramL[i]=int(paramL[i])
                except:pass
        print 'test parameters:',paramL                
        y = genseq()
        seq = y.maTH(paramL)
        print 'test sequence:',seq
        #starttest = input('start test?(abort:0,start test:1):')
        if 1:
        #if starttest:
            z = pulldata()
            z.record(seq)
        else:
            break

        

        