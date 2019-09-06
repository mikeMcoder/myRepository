import time
if __name__ == '__main__':
    #parameters
    com_port = input('COM_PORT :')
    print 'connect to COM_PORT %d '%(com_port)
    it.connect(com_port)
    
    #clear buffer, calling it.release() max 6 times 
    for i in range(1,7):
        try:
            itR =it.release()
        except:
            raise'Error : cannot call it.release'
        try:
            if itR[0] == 'OK':
                print 'buffer cleared in %d calls: %s'%(i,itR)
                break
        except:
            raise 'Error : itR[0]'
        
    if (i==6)&(itR[0]!='OK'):
        raise 'Error : ',itR
    it.resena(1)
    '''
    STalarm = time.time()
    TLalarm = 0.0
    while TLalarm < 60:
        TLalarm = time.time()-STalarm
        time.sleep(3)
        print '.',
        sys.stdout.flush()
        dummy11 = it.statusW()
        try:
            flagalarm = int(dummy11[1].fieldAlm().value())
        except:
            raise'cannot receive it.statusW()'
        if not flagalarm:
            print 'alarm cleared'
            break
    if (not(TLalarm < 60)) & flagalarm:
        raise 'alarm no cleared'
    STfatal = time.time()
    TLfatal = 0.0
    while TLfatal < 60:
        TLfatal = time.time()-STfatal
        time.sleep(3)
        print '.',
        sys.stdout.flush()
        dummy11 = it.statusF()
        try:
            flagfatal = int(dummy11[1].fieldFatal().value())
        except:
            raise'cannot receive it.statusF()'
        if not flagfatal:
            print 'fatal cleared'
            break
    if (not(TLfatal < 60)) & flagfatal:
        raise 'fatal no cleared'
    '''