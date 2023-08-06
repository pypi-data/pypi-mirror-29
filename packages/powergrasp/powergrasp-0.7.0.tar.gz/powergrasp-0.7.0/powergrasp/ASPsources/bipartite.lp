%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Find best biclique from preprocessed information on the non-covered graph
% Input graph should be a bipartite graph.
%
% Constants:
%       - cc: treated connected component. (cc/1 gives existing cc)
%       -  k: current step of treatment (first step is 1)
% Input:
%       - inter(X,Y): there exist an edge linking X and Y in cc.
%       - edge(X,Y): there exist an edge linking X and Y in cc, with X in the
%                    first set of the graph, and Y in the second.
%       - membercc(Y): Y is a member of cc.
% Output:
%       - newconcept(cc,k,T,X): X is the member of the set T in the concept cc at step k.
%       - star(cc,k,T): set T of concept is a star.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Symetric edges.
inter(X,Y):- edge(X,Y).
inter(X,Y):- inter(Y,X).

% Two nodes are likely to be in the same set if having a common neighbor.
linked2(X,Y):- edge(X,Z) ; edge(Y,Z) ; X<Y.

% Choice of the minimum of the concept
1{minobj(cc,k,X): membercc(X), edge(X,_) }1.

% Choice of elements in set 1
newconcept(cc,k,1,X):- minobj(cc,k,X).
0 { newconcept(cc,k,1,X): linked2(Min,X) } max_set1_size :- minobj(cc,k,Min).

% Choice of elements in set 2
1 { newconcept(cc,k,2,Y): edge(Min,Y), Min<Y } max_set2_size :- minobj(cc,k,Min).

% An element in a set can't be in the other set.
:- newconcept(cc,k,1,X) ; newconcept(cc,k,2,X).

% A node can't be in a set if not linked to a node of other set
:- newconcept(cc,k,1,X) ; newconcept(cc,k,2,Y) ; not edge(X,Y).


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%% CONCEPT PROPERTIES %%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% a star is a biclique with one powernode composed of only one node
%star(cc,k,T):- 1 { newconcept(cc,k,T,X): weight(X,1) } 1 ; T=1..2.
star(cc,k,T):- 1 { newconcept(cc,k,T,X) } 1 ; T=1..2.
:- star(cc,k,3-T) ; star(cc,k,T) ; T=1..2. % link between two nodes will not be treated as a interesting case
