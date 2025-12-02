"""
Script para verificar el cálculo del dígito de verificación paso a paso.
"""

nit = '1003618585'
factores = {1:3, 2:7, 3:13, 4:17, 5:19, 6:23, 7:29, 8:37, 9:41, 10:43, 11:47, 12:53, 13:59, 14:67, 15:71}
longitud = len(nit)
suma = 0

print(f'NIT: {nit}')
print(f'Longitud: {longitud}')
print('\nCálculo paso a paso:')
print('-' * 80)

for i in range(longitud):
    digito = int(nit[i])
    posicion = longitud - i
    factor = factores[posicion]
    producto = digito * factor
    suma += producto
    print(f'Pos {i}: dígito={digito}, factor[{posicion}]={factor:2d}, producto={producto:3d}, suma acum={suma:4d}')

residuo = suma % 11
dv = (11 - residuo) if residuo > 1 else residuo

print('-' * 80)
print(f'\nSuma total: {suma}')
print(f'Residuo (suma % 11): {residuo}')
print(f'Dígito de verificación: {dv}')
print(f'\nNIT completo: {nit}-{dv}')
