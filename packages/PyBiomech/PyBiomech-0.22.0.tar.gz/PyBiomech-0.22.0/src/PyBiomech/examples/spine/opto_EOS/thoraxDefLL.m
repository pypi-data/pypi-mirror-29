function [ T ] =  thoraxDefLL( IJ, PX, C7, T8 )

% INPUT: VETTORI RIGA
% Questo programma implementa il codice per il calcolo del sdr di torace come descritto nell'ISG proposal 
% Versione utilizzata per consistenza con i segmenti inferiori
% Si ricorda che i vettori di ingresso devono essere 1x3

yt = (IJ + C7)/2 - (T8 + PX)/2;  yt = yt/norm(yt); % longitudinale
zt = cross(yt,T8-PX);  zt = zt/norm(zt); % medio laterale che punta verso l'arto destro
xt = cross(yt,zt); xt = xt/norm(xt); % antero posteriore verso avanti

T = [xt' yt' zt'];% trasformo i vettori in colonna



% 
% % Questo programma implementa il codice per il calcolo del sdr di torace come descritto nell'ISG proposal 
% % Si ricorda che i vettori di ingresso devono essere 1x3
% 
% yt = (IJ + C7)/2 - (T8 + PX)/2;  yt = yt/norm(yt); % longitudinale
% xt = cross(yt,T8-PX);  xt = xt/norm(xt); % medio laterale
% zt = cross(xt,yt); zt = zt/norm(zt); % antero posteriore verso il retro
% 
% T = [xt' yt' zt'];