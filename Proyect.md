## Plan del Proyecto "Yield Curve Creator"

### 1. Objetivos Iniciales

1. Montar la infraestructura básica (repositorio, CI/CD, entornos).
2. Scaffold del backend y frontend con rutas mínimas.
3. Módulo de ingestión y parsing de prospectos.
4. Módulo de cálculo de flujos y TIR.
5. API REST para consultar resultados.
6. UI básica para carga de prospectos y visualización de flujos.

---

### 2. Estructura de Carpetas

```
yield_curve_creator/
├── backend/
│   ├── app/
│   │   ├── main.py        # FastAPI entrypoint
│   │   ├── routers/
│   │   ├── services/      # lógica de parsing y cálculos
│   │   └── models/        # esquemas Pydantic
│   ├── tests/             # pruebas unitarias
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── App.tsx
│   ├── public/
│   ├── package.json
│   └── Dockerfile
├── infra/
│   ├── docker-compose.yml
│   └── k8s/
├── .github/workflows/     # CI/CD pipelines
└── README.md
```

---

### 3. Milestones y Tiempos

| Milestone                      | Descripción                                                | Duración Estimada |
| ------------------------------ | ---------------------------------------------------------- | ----------------- |
| 1. Infraestructura y CI/CD     | Configurar repositorio, linters, tests, pipeline GitHub.   | 2 días            |
| 2. Scaffold Backend & Frontend | Crear FastAPI + React mínimo con rutas de prueba.          | 3 días            |
| 3. Parsing de Prospectos       | Desarrollo de servicio que extrae datos clave de PDF/Word. | 5 días            |
| 4. Cálculos Financieros        | Flujos de caja, TIR, duración, convexidad.                 | 5 días            |
| 5. API de Resultados           | Endpoints para iniciar parseo y obtener resultados.        | 3 días            |
| 6. UI Básica                   | Formulario de carga y sección de resultados en frontend.   | 5 días            |
| 7. Testing & Refinamiento      | Cobertura de tests, validaciones manuales, UX polishing.   | 4 días            |
| 8. Despliegue MVP              | Docker, Kubernetes o Render/Heroku, documentación final.   | 2 días            |

---

### 4. Próximo Paso Inmediato

* **Crear repositorio** en GitHub con la estructura inicial y agregar el primer commit.
* **Configurar entorno local**: README con instrucciones de instalación y activar GitHub Actions para lint & tests.


Estructura inicial en backend/:

css
Copy
Edit
backend/
├── app/
│   └── main.py
├── requirements.txt
└── Dockerfile
backend/app/main.py con FastAPI y un endpoint de prueba:

python
Copy
Edit
from fastapi import FastAPI

app = FastAPI(
    title="Yield Curve Creator API",
    version="0.1.0",
    description="API para parsing de prospectos y cálculos de bonos"
)

@app.get("/health", tags=["Health"])
async def health_check():
    """
    Endpoint de salud para verificar que el servicio está corriendo.
    """
    return {"status": "ok"}

@app.get("/")
async def root():
    return {"message": "¡Bienvenido a Yield Curve Creator API!"}
backend/requirements.txt:

css
Copy
Edit
fastapi
uvicorn[standard]
backend/Dockerfile básico:

dockerfile
Copy
Edit
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
Próximos pasos
Instalar dependencias:

bash
Copy
Edit
cd backend
python3 -m venv venv
source venv/bin/activate   # o venv\Scripts\activate en Windows
pip install -r requirements.txt
Ejecutar y probar:

bash
Copy
Edit
uvicorn app.main:app --reload
Luego, en el navegador o con curl, visita http://localhost:8000/health.

Estructura inicial en backend/:

css
Copy
Edit
backend/
├── app/
│   └── main.py
├── requirements.txt
└── Dockerfile
backend/app/main.py con FastAPI y un endpoint de prueba:

python
Copy
Edit
from fastapi import FastAPI

app = FastAPI(
    title="Yield Curve Creator API",
    version="0.1.0",
    description="API para parsing de prospectos y cálculos de bonos"
)

@app.get("/health", tags=["Health"])
async def health_check():
    """
    Endpoint de salud para verificar que el servicio está corriendo.
    """
    return {"status": "ok"}

@app.get("/")
async def root():
    return {"message": "¡Bienvenido a Yield Curve Creator API!"}
backend/requirements.txt:

css
Copy
Edit
fastapi
uvicorn[standard]
backend/Dockerfile básico:

dockerfile
Copy
Edit
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
Próximos pasos
Instalar dependencias:

bash
Copy
Edit
cd backend
python3 -m venv venv
source venv/bin/activate   # o venv\Scripts\activate en Windows
pip install -r requirements.txt
Ejecutar y probar:

bash
Copy
Edit
uvicorn app.main:app --reload
Luego, en el navegador o con curl, visita http://localhost:8000/health

backend/app/services/calculations.py

Funciones para:

Generar flujos de caja (generate_cashflows)

Calcular TIR (calculate_ytm)

Calcular duración y convexidad (calculate_duration_convexity)

Sensibilidades como DV01 (calculate_dv01)

Un router en
backend/app/routers/calculations.py
con un endpoint:

http
Copy
Edit
POST /calculate
Content-Type: application/json

{
  "face": 1000,
  "coupon_rate": 0.05,
  "frequency": 2,
  "issue_date": "2020-01-01",
  "maturity_date": "2025-01-01",
  "clean_price": 980.0
}
y que devuelva un JSON con:

cashflows: array de { fecha, monto }

ytm

duration_macaulay

duration_modified

convexity

dv01

1. Endpoint para construir la curva spot
Podemos crear un nuevo router, por ejemplo /curve, que reciba un listado de bonos (con sus precios y características) y:

Bootstrap spot rates.

Ajuste por Nelson–Siegel o Svensson.

Devuelva curvas spot y forward.

2. Sensibilidades “what-if”
Un endpoint /sensitivity que:

Tome un shock paralelo o steepening.

Recalcule precios, DV01, TIR bajo ese escenario.

Devuelva un cuadro con los impactos.

3. Integración del módulo de parsing real
Hasta ahora tu parse_prospect es un stub. Habría que:

Leer campos clave del PDF/Word usando Camelot/Tika.

Mapearlos a bond_data con fechas, cupones, cláusulas.

4. Frontend / Dashboard
Una pequeña SPA en React:

Formulario de upload.

Barra de progreso (polling de /jobs/{}).

Gráficos de flujos y curvas (Recharts o D3).

Dime por dónde quieres continuar:

Curva spot y fitting con Nelson–Siegel,

Sensibilidades y “what-if”,

Parser de prospectos,

O montar el frontend para visualizarlo todo.