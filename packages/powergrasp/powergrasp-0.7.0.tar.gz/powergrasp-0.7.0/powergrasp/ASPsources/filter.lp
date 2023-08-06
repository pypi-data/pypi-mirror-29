%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Perform post-processing of the data at each steps.
%  its not a stand alone program, but a set of rules that needs to be grounded with
%  find best clique and find best biclique program
%
% Input (from findbestclique or findbestbiclique):
%       - newconcept(cc,k,T,X): X is the member of the set T in the concept cc at step k.
%       - clique(cc,k): concept is a clique.
%       - star(cc,k,T): set T of concept is a star.
% Output:
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%



% avoid any non-validated model
% :- not valid.

% valid.

% #script (python)
% import gringo


% def validated(model):
    % first, second = [], []
    % for atom in model.atoms:
        % if atom.predicate == 'newconcept':
            % cc, k, t, x = atom.args()
            % (first if t == 1 else second).append(x)
    % return 'YBL087C' in first

% def main(prg):
    % prg.ground([("base", [])])
    % prg.solve(on_model=validated)

% #end.
% valid(N) :- N=@echo(1).
