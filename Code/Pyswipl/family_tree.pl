/*
  Matt Fleetwood
  ECE 410/510
  Family Tree Program
  6/9/2018
  
  A family tree program from the second week of class.
  This program demonstrates a simple Prolog program that can define familial relationships.
  Modified from source: https://bernardopires.com/2013/10/try-logic-programming-a-gentle-introduction-to-prolog/
*/

mother(helen, victoria).
mother(helen, tracy).
mother(helen, tim).
mother(helen, heidi).
mother(helen, sherri).
mother(victoria, matthew). 
mother(victoria, jon).
mother(victoria, tommy).
mother(victoria, kat).
mother(kat, arlo). 
mother(alex, stella).
mother(alex, oliver).
mother(patti, kristina).
father(steve, kristina).
father(bob, victoria). 
father(bob, tracy).
father(bob, tim).
father(bob, heidi).
father(bob, sherri).
father(mike, matthew).
father(mike, jon).
father(mike, tommy).
father(mike, kat).
father(matt, arlo).
father(jon, stella).
father(jon, oliver).
sibling(victoria, tim).
sibling(victoria, tracy).
sibling(tracy, sherri).
sibling(sherri, heidi).
sibling(mike, steve).
sibling(steve, mike).
sibling(mike, allan).
sibling(mike, karen).
sibling(heidi, victoria).
sibling(tim, victoria).
sibling(tommy, kat).
sibling(kat, tommy).
sibling(matthew, kat).
sibling(kat, matthew).
sibling(jon, tommy).
male(tim).
male(matthew).
male(jon).
male(tommy).
male(arlo).
male(oliver).
male(mike).
male(steve).
male(allan).
male(priyam).
female(helen).
female(victoria).
female(tracy).
female(heidi).
female(sherri).
female(kat).
female(stella).
female(karen).
daughter(X, Y) :-
	female(X),
	parent(Y, X).
son(X, Y) :-
	male(X),
	parent(Y, X).
brother(X, Y) :-
	male(X),
	sibling(X, Y).
sister(X, Y) :-
	female(X),
	sibling(X, Y).
parent(X, Y) :- mother(X, Y). 
parent(X, Y) :- father(X, Y).
grandparent(X, Y) :-
	parent(X, Z),
	parent(Z, Y).
greatgrandparent(X, Y) :-
	grandparent(X, Z), 
	parent(Z, Y).
uncle(X, Y) :-
	brother(X, Z),
	parent(Z, Y).
aunt(X, Y) :-
	sister(X, Z),
	parent(Z, Y).
cousin(X, Y) :-
	parent(A, X),
	parent(B, Y),
	sibling(A, B).
related(X, Y) :-
	parent(Y, X);
	grandparent(X, Y);
	grandparent(Y, X);
	greatgrandparent(X, Y);
	greatgrandparent(Y, X);
	sibling(X, Y);
	aunt(X, Y);
	aunt(Y, X);
	uncle(X, Y);
	uncle(Y, X);
	sibling(Y, X).
