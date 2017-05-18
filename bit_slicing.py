from myhdl import intbv, concat 

COSET = 0x55

def calculateHex(header):
    """ Return hec for an ATM header, represented as an intbv.

    The hec plynomial is 1 + x + x**2 + x**9.
    """
    hec = intbv(0)
    for bit in header[32:]:
        hec[8:] = concat(hec[7:2],
                        bit ^ hec[1] ^ hec[7],
                        bit ^ hec[0] ^ hec[7],
                        bit ^hec[7]
                        )

        return hec ^ COSET
