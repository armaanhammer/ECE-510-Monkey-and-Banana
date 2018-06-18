from pyswip import Prolog

prolog = Prolog()

prolog.consult('family.pl')

result = list(prolog.query('father(michael, X)'))

print(result)