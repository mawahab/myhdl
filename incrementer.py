from myhdl import *
from random import randrange

ACTIVE_LOW, INACTIVE_HIGH = 0, 1

def Inc(count, enable, clock, reset, n):

    """ Incrementer with enable. 

    count -- output 
    enable -- control input, increment when 1
    clock -- clock input 
    reset -- asynchronous reset input 
    n -- counter max value 
    """

    @always_seq(clock.posedge, reset = reset)
    def incLogic():
        if enable:
            count.next = (count + 1) % n

    return incLogic

def testbench():
    count, enable, clock = [Signal(intbv(0)) for i in range(3)]
    reset = ResetSignal(0, active=ACTIVE_LOW, async=True)

    inc_1 = Inc(count, enable, clock, reset, n=4)

    HALF_PERIOD = delay(10)

    @always(HALF_PERIOD)
    def clockGen():
        clock.next = not clock

    @instance 
    def stimulus():
        reset.next = ACTIVE_LOW
        yield clock.negedge
        reset.next = INACTIVE_HIGH
        for i in range(12):
            enable.next = min(1, randrange(3))
            yield clock.negedge
        raise StopSimulation

    @instance
    def monitor():
        print "enable count"
        yield reset.posedge
        while 1:
            yield clock.posedge
            yield delay(1)
            print " %s %s" % (enable, count)

    return clockGen, stimulus, inc_1, monitor

tb = testbench()
Simulation(tb).run()
