"""
FastAPI backend para calcular el dígito de verificación DIAN Colombia.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, field_validator
from typing import Optional

app = FastAPI(
    title="DIAN Colombia - API Dígito de Verificación",
    description="API para calcular el dígito de verificación de NITs colombianos según normas DIAN",
    version="1.0.0"
)

# Configurar CORS para permitir requests desde frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class NITRequest(BaseModel):
    """Modelo para request de cálculo de dígito."""
    nit: str
    
    @field_validator('nit')
    @classmethod
    def validate_nit(cls, v):
        """Valida que el NIT sea numérico."""
        # Remover espacios y guiones
        v = v.strip().replace(" ", "").replace("-", "")
        
        if not v.isdigit():
            raise ValueError("El NIT debe contener solo números")
        
        if len(v) == 0:
            raise ValueError("El NIT no puede estar vacío")
            
        if len(v) > 15:
            raise ValueError("El NIT no puede tener más de 15 dígitos")
        
        return v


class NITResponse(BaseModel):
    """Modelo para response con NIT completo."""
    nit_original: str
    digito_verificacion: int
    nit_completo: str
    formato_display: str


class DIANCalculator:
    """Implementación del algoritmo DIAN para calcular dígito de verificación."""
    
    @staticmethod
    def factores():
        """
        Retorna los factores de ponderación según norma DIAN.
        Array indexado por posición (1-15), igual que en el código PHP original.
        """
        return {
            1: 3,
            2: 7,
            3: 13,
            4: 17,
            5: 19,
            6: 23,
            7: 29,
            8: 37,
            9: 41,
            10: 43,
            11: 47,
            12: 53,
            13: 59,
            14: 67,
            15: 71,
        }
    
    @staticmethod
    def calcular_digito(nit: str) -> int:
        """
        Calcula el dígito de verificación para un NIT dado.
        Implementación idéntica al código PHP original en src/DIAN.php
        
        Args:
            nit: Número de identificación tributaria (solo dígitos)
            
        Returns:
            Dígito de verificación (0-9)
        """
        factores = DIANCalculator.factores()
        longitud_nit = len(nit)
        suma = 0
        
        # Calcular suma ponderada (igual que en PHP)
        # El bucle va de 0 a longitud_nit-1, y accede a factores[longitud_nit - i]
        for i in range(longitud_nit):
            digito = int(nit[i])
            factor_posicion = longitud_nit - i
            suma += digito * factores[factor_posicion]
        
        # Calcular residuo y dígito de verificación (igual que en PHP)
        residuo = suma % 11
        digito_verificacion = (11 - residuo) if residuo > 1 else residuo
        
        return digito_verificacion


@app.get("/")
async def root():
    """Endpoint raíz con información de la API."""
    return {
        "message": "API DIAN Colombia - Dígito de Verificación",
        "version": "1.0.0",
        "endpoints": {
            "calcular": "/calcular (POST)",
            "health": "/health (GET)",
            "docs": "/docs"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.post("/calcular", response_model=NITResponse)
async def calcular_digito_verificacion(request: NITRequest):
    """
    Calcula el dígito de verificación para un NIT dado.
    
    Args:
        request: Objeto con el NIT a validar
        
    Returns:
        NITResponse con el NIT completo y dígito de verificación
        
    Raises:
        HTTPException: Si el NIT es inválido
    """
    try:
        nit = request.nit
        digito = DIANCalculator.calcular_digito(nit)
        
        return NITResponse(
            nit_original=nit,
            digito_verificacion=digito,
            nit_completo=f"{nit}{digito}",
            formato_display=f"{nit}-{digito}"
        )
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@app.get("/ejemplo")
async def ejemplo():
    """Endpoint de ejemplo con NITs de prueba."""
    ejemplos = [
        "1003618585",
        "890903938",
        "800197268"
    ]
    
    resultados = []
    for nit in ejemplos:
        digito = DIANCalculator.calcular_digito(nit)
        resultados.append({
            "nit": nit,
            "digito": digito,
            "completo": f"{nit}-{digito}"
        })
    
    return {
        "ejemplos": resultados,
        "nota": "Estos son NITs de ejemplo con sus dígitos de verificación calculados"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
