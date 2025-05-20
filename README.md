# yield_curve_creator

**Yield Curve Creator** es una aplicación para analizar bonos y generar curvas de rendimiento a partir de prospectos. Permite extraer datos de emisión, calcular flujos de caja, TIR, duración, convexidad y construir curvas spot/forward con métodos avanzados.

---

## 🚀 Características Principales

1. **Ingestión y parsing**  
   - Soporte para PDF/Word  
   - Extracción automática de: fecha de emisión/vencimiento, tipo de cupón, calendario de pagos, valor nominal y cláusulas especiales (call/put, step-up/down)  

2. **Motor de cálculos financieros**  
   - Generación de flujos de caja (cupones y amortizaciones)  
   - Valoración teórica con curva de descuento  
   - Cálculo de TIR exigida (YTM) via Newton–Raphson  
   - Duración (Macaulay y modificada) y convexidad  
   - Sensibilidades (DV01/PV01, tablas “what-if”)  

3. **Construcción de curvas y benchmarking**  
   - Bootstrap de curva spot con bonos comparables  
   - Derivación de tasas forward implícitas  
   - Fitting de curvas (Nelson-Siegel, Svensson, splines)  
   - Análisis cross-section entre bonos del mismo emisor  

4. **Reporting y visualización**  
   - Dashboard interactivo con gráficos (D3.js, Recharts)  
   - Exportes a PDF y Excel  
   - Alertas “what-if” y notificaciones de oportunidades  

---

## 🛠️ Instalación

1. Clona el repositorio:  
```bash
   git clone https://github.com/tu-usuario/yield_curve_creator.git
   cd yield_curve_creator
``` 
2. Crea y activa un entorno virtual:
```bash
    python3 -m venv venv
    source venv/bin/activate   # Linux / macOS
    venv\Scripts\activate      # Windows
```
3. Instala dependencias:
```bash
    pip install -r requirements.txt
```

⚙️ Uso
Arranca el servidor backend:

```bash
    uvicorn app.main:app --reload
```

Abre el frontend en modo desarrollo:
```bash
    cd frontend
    npm install
    npm start
```

Desde la UI:

    Sube tu prospecto de bono

    Confirma o corrige los datos extraídos

    Consulta flujos, TIR, duración y curvas

    Descarga tu reporte en PDF/Excel

📚 Tecnologías
    
    Backend: Python, FastAPI, pandas, NumPy, SciPy, QuantLib (opcional)

    Parsing: Camelot, PyPDF2, Tika

    Base de datos: PostgreSQL (PostGIS opcional)

    Frontend: React, TypeScript, Material-UI / Tailwind, Recharts, D3.js

Infraestructura: Docker, Kubernetes / Render, Celery + RabbitMQ

🏗️ Arquitectura
    
    Microservicios

    Servicio de parsing (Celery/RabbitMQ)

    Servicio de cálculos financieros

    Servicio de gestión de datos

    Colas y jobs asíncronos para parseo y bootstrap de curvas

    API RESTful con endpoints para subir prospectos, consultar resultados y generar reportes

    CI/CD con tests unitarios (Black, Flake8) y despliegue automático

📅 Roadmap
    
    Bonos con opciones embebidas (OAS, volatilidad)

    Simulaciones Monte Carlo para rangos de precio

    Integración de datos en tiempo real (Refinitiv, Bloomberg)

    Módulo de crédito y análisis de impago

    Back-testing de estrategias de renta fija

    Plantillas automáticas de Word/PowerPoint

🤝 Contribuir
    
    Haz un fork del repositorio

    Crea una rama (git checkout -b feature/mi-nueva-funcionalidad)

    Haz tus cambios y commitea (git commit -m "Agrega nueva funcionalidad")

    Sube tu rama (git push origin feature/mi-nueva-funcionalidad)

    Abre un pull request y describe tus cambios

📄 Licencia
    
    Este proyecto está bajo la licencia MIT.