


from ...util.dq import *
dd = {'A':{'b':[9,8,7]}}
assert(dq(dd, ['A']) == {'b':[9,8,7]})
assert(dq(dd, '/A/b/1') == 8)


