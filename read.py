#!/usr/bin/env python
# coding=utf8

import spidev
import time, datetime


""" {{{ """

class PCD:
    """
    /////////////////////////////////////////////////////////////////////
    //MF522命令字
    /////////////////////////////////////////////////////////////////////
    """
    IDLE       = 0x00 #取消当前命令
    MEM        = 0x01
    AUTHENT    = 0x0E #验证密钥
    RECEIVE    = 0x08 #接收数据
    TRANSMIT   = 0x04 #发送数据
    TRANSCEIVE = 0x0C #发送并接收数据
    RESETPHASE = 0x0F #复位
    CALCCRC    = 0x03 #CRC计算

class PICC:
    """
    /////////////////////////////////////////////////////////////////////
    //Mifare_One卡片命令字
    /////////////////////////////////////////////////////////////////////
    """
    REQIDL    = 0x26 #寻天线区内未进入休眠状态
    REQALL    = 0x52 #寻天线区内全部卡
    ANTICOLL1 = 0x93 #防冲撞
    ANTICOLL2 = 0x95 #防冲撞
    AUTHENT1A = 0x60 #验证A密钥
    AUTHENT1B = 0x61 #验证B密钥
    READ      = 0x30 #读块
    WRITE     = 0xA0 #写块
    DECREMENT = 0xC0 #扣款
    INCREMENT = 0xC1 #充值
    RESTORE   = 0xC2 #调块数据到缓冲区
    TRANSFER  = 0xB0 #保存缓冲区中数据
    HALT      = 0x50 #休眠

class MF522:
    """
    /////////////////////////////////////////////////////////////////////
    //MF522寄存器定义
    /////////////////////////////////////////////////////////////////////
    """
    # PAGE 0
    RFU00               = 0x00    
    CommandReg          = 0x01    
    ComIEnReg           = 0x02    
    DivlEnReg           = 0x03    
    ComIrqReg           = 0x04    
    DivIrqReg           = 0x05
    ErrorReg            = 0x06    
    Status1Reg          = 0x07    
    Status2Reg          = 0x08    
    FIFODataReg         = 0x09
    FIFOLevelReg        = 0x0A
    WaterLevelReg       = 0x0B
    ControlReg          = 0x0C
    BitFramingReg       = 0x0D
    CollReg             = 0x0E
    RFU0F               = 0x0F
      
    # PAGE 1
    RFU10               = 0x10
    ModeReg             = 0x11
    TxModeReg           = 0x12
    RxModeReg           = 0x13
    TxControlReg        = 0x14
    TxAutoReg           = 0x15
    TxSelReg            = 0x16
    RxSelReg            = 0x17
    RxThresholdReg      = 0x18
    DemodReg            = 0x19
    RFU1A               = 0x1A
    RFU1B               = 0x1B
    MifareReg           = 0x1C
    RFU1D               = 0x1D
    RFU1E               = 0x1E
    SerialSpeedReg      = 0x1F
     
    # PAGE 2
    RFU20               = 0x20  
    CRCResultRegM       = 0x21
    CRCResultRegL       = 0x22
    RFU23               = 0x23
    ModWidthReg         = 0x24
    RFU25               = 0x25
    RFCfgReg            = 0x26
    GsNReg              = 0x27
    CWGsCfgReg          = 0x28
    ModGsCfgReg         = 0x29
    TModeReg            = 0x2A
    TPrescalerReg       = 0x2B
    TReloadRegH         = 0x2C
    TReloadRegL         = 0x2D
    TCounterValueRegH   = 0x2E
    TCounterValueRegL   = 0x2F
       
    # PAGE 3
    RFU30               = 0x30
    TestSel1Reg         = 0x31
    TestSel2Reg         = 0x32
    TestPinEnReg        = 0x33
    TestPinValueReg     = 0x34
    TestBusReg          = 0x35
    AutoTestReg         = 0x36
    VersionReg          = 0x37
    AnalogTestReg       = 0x38
    TestDAC1Reg         = 0x39  
    TestDAC2Reg         = 0x3A   
    TestADCReg          = 0x3B   
    RFU3C               = 0x3C   
    RFU3D               = 0x3D   
    RFU3E               = 0x3E   
    RFU3F               = 0x3F

""" }}} """

VERBOSE = False

spi = spidev.SpiDev()
spi.open(0,0)
# spi.cshigh = True
# spi.max_speed_hz = 488000

def wr(addr, val):
    a = ( ( addr << 1 ) & 0x7e )
    v = [a, val]
    if VERBOSE:
        print '>>>' , hexf(v)

    r = spi.xfer(v)
    if VERBOSE:
        print '<<<' , hexf(r)

def wr2(addr, vall):
    a = ( ( addr << 1 ) & 0x7e )
    v = [a] + vall
    if VERBOSE:
        print '>>>' , hexf(v)

    r = spi.xfer(v)
    if VERBOSE:
        print '<<<' , hexf(r)


def rd(addr):
    a = ( ( ( addr<<1 ) & 0x7e ) | 0x80 )
    v = [a, 0x00]
    if VERBOSE:
        print '>>>' , hexf(v)

    r = spi.xfer(v)
    if VERBOSE:
        print '<<<' , hexf(r)

    d = r[1]
    return d

def xfer(addr, vall):
    a = ( ( addr << 1 ) & 0x7e )
    b = [a] + vall
    if VERBOSE:
        print '>>>' , hexf( b )

    r = spi.xfer(b)
    if VERBOSE:
        print '<<<' , hexf([r])

    return r

def clearBitMask(reg, mask):
    tmp = rd(reg)
    wr(reg, tmp & ~mask)

def setBitMask(reg, mask):
    tmp = rd(reg)
    wr(reg, tmp | mask)


def hexf(r):
    return [('%02x' % i ) for i in r]


def reset():

    print 'reset'
    wr(MF522.CommandReg, 0x0f)

    wr(MF522.ModeReg, 0x3d)

    wr(MF522.TReloadRegL, 0x1e)
    wr(MF522.TReloadRegH, 0x00)

    wr(MF522.TModeReg, 0x8d)

    wr(MF522.TPrescalerReg, 0x3e)

    wr(MF522.TxAutoReg, 0x40)

def antennaOff():
    print 'antenna off'
    clearBitMask(MF522.TxControlReg, 0x03)

def antennaOn():
    print 'antenna on'
    i = rd(MF522.TxControlReg)
    if(not(i & 0x03)) :
        print 'set antenna on'
        setBitMask(MF522.TxControlReg, 0x03)
    # rd(MF522.TxControlReg)

def configISOType():
    print 'config type'
    clearBitMask(MF522.Status2Reg, 0x08)
    
    wr(MF522.ModeReg      , 0x3d)
    wr(MF522.RxSelReg     , 0x86)
    wr(MF522.RFCfgReg     , 0x7f)
    wr(MF522.TReloadRegL  , 0x1e)
    wr(MF522.TReloadRegH  , 0x00)
    wr(MF522.TModeReg     , 0x8d)
    wr(MF522.TPrescalerReg, 0x3e)
    
    antennaOn()

def cmd(command, req):
    status = False

    n = 0x00
    irqEn = 0x00
    waitFor = 0x00

    if command == PCD.AUTHENT :
        irqEn = 0x12
        waitFor = 0x10
    elif command == PCD.TRANSCEIVE :
        irqEn = 0x77
        waitFor = 0x30

    wr(MF522.ComIEnReg,irqEn|0x80)
    clearBitMask(MF522.ComIrqReg, 0x80)
    wr(MF522.CommandReg, PCD.IDLE)
    setBitMask(MF522.FIFOLevelReg, 0x80)
    
    wr2(MF522.FIFODataReg, req)
    wr(MF522.CommandReg, command)
   
    if command == PCD.TRANSCEIVE :
        setBitMask(MF522.BitFramingReg, 0x80)  

    i = 100
    while True:
        n = rd(MF522.ComIrqReg)   
        i = i - 1
        if ( i > 0 ) and ( not ( n & 0x01 ) ) and ( not ( n & waitFor ) ) :
            continue
        else:
            break
    # print 'n', n

    e = rd(MF522.ErrorReg)
    # print 'e', e

    clearBitMask(MF522.BitFramingReg, 0x80)

    # print 'i', i
    if i > 0 :
        e = rd(MF522.ErrorReg)
        # print 'e', e
        if not ( e & 0x1b ) :
            status = True

            if n & irqEn & 0x01 :
                status = [] # no tag

            elif command == PCD.TRANSCEIVE :
                n = rd(MF522.FIFOLevelReg)
                # print 'fifo level', n
                lastBits = rd(MF522.ControlReg) & 0x07
                
                status = []
                n = max(min(n, 18), 1)
                for k in xrange(n) :
                    v = rd(MF522.FIFODataReg)
                    status.append(v)

        else:
            status = False

    setBitMask(MF522.ControlReg, 0x80)
    wr(MF522.CommandReg, PCD.IDLE)

    return status

def reqidl_cmd():
    clearBitMask(MF522.Status2Reg, 0x08)
    wr(MF522.BitFramingReg, 0x07)
    setBitMask(MF522.TxControlReg, 0x03)

    status = cmd(PCD.TRANSCEIVE, [PICC.REQIDL])

    return status

def anticoll_cmd():
    clearBitMask(MF522.Status2Reg,0x08)
    wr(MF522.BitFramingReg,0x00)
    clearBitMask(MF522.CollReg,0x80)

    status = cmd(PCD.TRANSCEIVE, [PICC.ANTICOLL1, 0x20])

    setBitMask(MF522.CollReg, 0x80)

    if len(status) == 5 :
        snr_check = 0
        for i in xrange(4):
            snr_check ^= status[i] 
        print 'snr_check', snr_check
        if snr_check != status[4] :
            # what's this ?
            status = False
        else :
            status = status[:4]

    return status

def select_cmd(card_no):

    msg = [0] * 9
    msg[0] = PICC.ANTICOLL1
    msg[1] = 0x70
    msg[6] = 0x00
    for i in xrange(4):
        msg[i+2] = card_no[i]
        msg[6]  ^= card_no[i]

    msg[7], msg[8] = cal_crc(msg[:7])

    clearBitMask(MF522.Status2Reg, 0x08)

    status = cmd(PCD.TRANSCEIVE, msg)

    return status

def cal_crc(data):
    clearBitMask(MF522.DivIrqReg, 0x04)
    wr(MF522.CommandReg, PCD.IDLE)
    setBitMask(MF522.FIFOLevelReg, 0x80)

    for v in data:
        wr(MF522.FIFODataReg, v)

    wr(MF522.CommandReg, PCD.CALCCRC)

    i = 0xff
    while True :
        n = rd(MF522.DivIrqReg)
        i = i - 1
        if ( i > 0 ) and (not ( n & 0x04 ) ):
            continue
        else :
            break

    l = rd(MF522.CRCResultRegL)
    m = rd(MF522.CRCResultRegM)

    return (l, m)

# def selftest():
#     ''' not working... '''
#     print 'start self test'
#     e = rd(MF522.CommandReg)
#     e = rd(MF522.ComIEnReg)
# 
#     time.sleep(5)
#     return
# 
#     wr(MF522.CommandReg, PCD.RESETPHASE)
#     e = rd(MF522.ErrorReg)
# 
# 
#     wr(MF522.CommandReg, PCD.MEM)
#     for i in xrange(25):
#         wr(MF522.FIFODataReg, 0x00)
#     
#     wr(MF522.AutoTestReg, 0x09)
#     wr(MF522.FIFODataReg, 0x00)
#     wr(MF522.CommandReg, PCD.CALCCRC)
#     time.sleep(1)
#     print 'result'
#     for i in xrange(64) :
#         n = rd(MF522.FIFODataReg)
# 
#     time.sleep(5)

while True:
    print 'run'
    time.sleep(1)

    """
    selftest()
    continue
    """

    """
    wr(MF522.CommandReg, 0x0f)

    e = rd(MF522.CommandReg)
    e = rd(MF522.ErrorReg)
    e = rd(MF522.ErrorReg)
    continue
    """

    reset()    
    # time.sleep(1)


    antennaOff()
    # time.sleep(1)
    antennaOn()
    # time.sleep(1)
    #configISOType()
    # time.sleep(1)

    card_type = reqidl_cmd()
    # res = request_cmd(PICC.REQALL)
    print 'card type', card_type
    if card_type :
        card_no = anticoll_cmd()
        print 'coll no', card_no
        if card_no :
            sel = select_cmd(card_no)
            print 'sel', sel
    time.sleep(1)

    antennaOff()

    print 'next...'
    time.sleep(5)

