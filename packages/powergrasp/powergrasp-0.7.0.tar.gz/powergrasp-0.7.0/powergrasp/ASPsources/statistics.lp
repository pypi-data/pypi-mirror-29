%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Perform integrity tests on input data (edge/2)
% Returns atoms that describes possibles problems,
%  and the edge/2, corrected.
%
% revised version:  01/07/2015   L. Bourneuf
%
% Input:
%       - edge(X,Y): there exists an edge between X and Y in the graph
% Output:
%       - edge(X,Y): there exists a corrected and oriented edge between X and Y in the graph
%       - nb(edge,N): 
%       - nb(node,N): 
%       - nb(input_edge,N): 
%       - nb(repeatition,N): 
%       - membercc(CC,N): node N belongs to connected component CC
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


inter(X,Y) ; inter(Y,X):- edge(X,Y).
oedge(X,Y):- inter(X,Y) ; X<Y.
oedge(X,Y):- inter(Y,X) ; X<Y.
node(X):- edge(X,_).
node(Y):- edge(_,Y).

nb(node,N):-       N={node(X)   }.
nb(edge,N):-       N={oedge(_,_)}.
nb(input_edge,N):- N={edge(_,_) }.
nb(repeatition,K-L):- nb(edge,L) ; nb(input_edge,K).
bad(node, k):- node( k).  %  k is a constant used for step number
bad(node,cc):- node(cc).  % cc is a constant used for connected component reference


% Connected paths starting with minimal element X
% connected(Minimum element,Element connected to the minimum)
% connectedpath(X,Y):- oedge(X,Y).
% connectedpath(X,Z):- connectedpath(X,Y) ; inter(Y,Z) ; X<Z.

% Connected components are identified by their smaller element.
% Connected components are identified by their smaller element.
% Choose them, on by one.
% 1{ cc(X): node(X) , not connectedpath(_,X) }1.
% membercc(CC,N):- cc(CC) ; connectedpath(CC,N).

% bipartite:- inter(X,Y).

#show.
#show nb/2.
#show bad/2.
% #show cc/1.
% #show bipartite:bipartite.
