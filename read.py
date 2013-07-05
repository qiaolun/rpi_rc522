#!/usr/bin/env python
# coding=utf8

import time, datetime

import reader

reader = reader.Reader()
reader.open(0, 0)

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

    reader.reset()    
    # time.sleep(1)


    reader.antennaOff()
    # time.sleep(1)
    reader.antennaOn()
    # time.sleep(1)
    #reader.configISOType()
    # time.sleep(1)

    card_type = reader.reqidl_cmd()
    # res = request_cmd(PICC.REQALL)
    print 'card type', card_type
    if card_type :
        card_no = reader.anticoll_cmd()
        print 'coll no', card_no
        if card_no :
            sel = reader.select_cmd(card_no)
            print 'sel', sel
    time.sleep(1)

    reader.antennaOff()

    print 'next...'
    time.sleep(5)

