function R = pelvisDefGlobal( LASIS, RASIS, LPSIS, RPSIS, side )

%Sistema di riferimento anatomico per la pelvi ( vedi cappozzo, '95 )
% LASIS = spina iliaca anteriore superiore sinistra
% RASIS = spina iliaca anteriore superiore destra
% LPSIS = spina iliaca posteriore superiore sinistra
% RPSIS = spina iliaca posteriore superiore destra

Op = ( RASIS + LASIS )/2;

x = RASIS-LASIS;
x = x/norm(x);

switch side
    case 'Right'
        z = cross(x, RASIS - ( LPSIS + RPSIS )/2 );
        z = z/norm(z);
    case 'Left'
        z = cross(x, LASIS - ( LPSIS + RPSIS )/2 );
        z = z/norm(z);
end

y = cross( z, x );
y = y/norm(y);

R =[x' y' z'];
