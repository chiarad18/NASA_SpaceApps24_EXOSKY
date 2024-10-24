class Exo:
    def __init__(self, idnum, ra, dec, dist):
        self._id = idnum
        self._ra = ra
        self._dec = dec
        self._dist = dist

    def get_id(self):
        return self._id

    def get_ra(self):
        return self._ra

    def get_dec(self):
        return self._dec

    def get_dist(self):
        return self._dist


