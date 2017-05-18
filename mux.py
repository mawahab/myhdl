from myhdl import Signal, Simulation, delay, always_comb, intbv
from random import randrange

def Mux(z, a, b, sel):
    """ Multiplexer.

    z -- mux output
    a, b -- data inputs 
    sel -- control input : select a if asserted, otherwise b

    """

    @always_comb
    def muxLogic():
            if sel == 1: 
                z.next = a
            else:
                z.next = b

    return muxLogic

# Once we've created some signals ...
z, a, b, sel = [Signal(intbv(0)) for i in range(4)]

# ... it can be instantiated as follows 
mux_1 = Mux(z, a, b, sel)

def test(): 

    print "z a b sel"
    for i in range(10):
        a.next, b.next, sel.next = randrange(10), randrange(10), randrange(2)
        yield delay(10)
        print "%s %s %s %s" % (z, a, b, sel)

test_1 = test()
sim = Simulation(mux_1, test_1).run()
