def calcular_digito_verificacion(nit: str) -> int:
    """
    Calcula el dígito de verificación DIAN para un NIT colombiano.
    Basado en la lógica del repositorio oficial DIAN (PHP).
    """
    # Pesos oficiales DIAN (de derecha a izquierda)
    factores = [71, 67, 59, 53, 47, 43, 41, 37, 29, 23, 19, 17, 13, 7, 3]
    nit = nit.strip()
    if not nit.isdigit():
        return None
    suma = 0
    nit_reversed = nit[::-1]
    for i, digito in enumerate(nit_reversed):
        if i >= len(factores):
            break
        suma += int(digito) * factores[len(factores) - 1 - i]
    residuo = suma % 11
    if residuo > 1:
        return 11 - residuo
    else:
        return residuo

# Ejemplo de uso:
if __name__ == "__main__":
    ejemplo_nit = "900437270"
    digito = calcular_digito_verificacion(ejemplo_nit)
    print(f"NIT: {ejemplo_nit}, Dígito de verificación: {digito}")
