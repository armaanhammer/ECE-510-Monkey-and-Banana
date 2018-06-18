from pyswip import Prolog

prolog = Prolog()

prolog.assertz('father(michael, john)')
prolog.assertz('father(michael, gina)')

result = list(prolog.query('father(michael, X)'))

print(result)