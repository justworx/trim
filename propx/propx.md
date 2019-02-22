


from trix.data.dbgrid import *
q = DBGrid(trix=trix.path('trix').list())
pp = q('select * from trix')

pp.grid()

