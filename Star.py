class Star:
    def __init__(self, idnum, ra, dec, dist, r_mag, g_mag, b_mag):
        self._id = idnum
        self._ra = ra
        self._dec = dec
        self._dist = dist
        self._rmag = r_mag
        self._gmag = g_mag
        self._bmag = b_mag

    def get_id(self):
        return self._id

    def get_ra(self):
        return self._ra

    def get_dec(self):
        return self._dec

    def get_dist(self):
        return self._dist

    def get_rmag(self):
        return self._rmag

    def get_gmag(self):
        return self._gmag

    def get_bmag(self):
        return self._bmag

    def get_color(self):
        return convert_rgbmag(self.get_rmag(), self.get_gmag(), self.get_bmag()) 

def convert_rgbmag(r, g, b) {
    mx = max(r, g, b)
    if mx == r:
        return 'r'
    elif mx = g:
        return 'g'
    else:
        return 'b'
}
