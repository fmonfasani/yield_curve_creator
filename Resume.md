1. **Módulos principales**  
   - **Ingestión y parsing de prospectos**  
     - **Carga de PDF/Word**: permite al usuario subir el prospecto del bono.  
     - **Extracción de datos clave** (OCR/NLP: Camelot, PyPDF2, Tika):  
       - Fecha de emisión y vencimiento  
       - Tipo de cupón (fijo, variable, cero cupón) y frecuencia  
       - Calendario de pagos  
       - Valor nominal  
       - Cláusulas especiales (call/put, step-up/down)  

   - **Motor de cálculos financieros**  
     - **Flujos de caja**: genera automáticamente la tabla de cupones y amortizaciones.  
     - **Valoración básica**: precio teórico según una curva de descuento ingresada o estimada.  
     - **TIR exigida (YTM)**: cálculo iterativo (Newton–Raphson) para hallar la tasa que iguala VAN a cero.  
     - **Duración y convexidad**: Macaulay, modificada y convexidad.  
     - **Sensibilidades**:  
       - DV01 / PV01  
       - Tablas “what-if” para movimientos paralelos/steepening de la curva.  

   - **Curvas y benchmarking**  
     - **Construcción de curva spot**: bootstrap usando bonos comparables (mismos emisores, plazos).  
     - **Curva forward**: derivación de tasas forward implícitas.  
     - **Fitting de curva**: Nelson-Siegel, Svensson o splines cúbicos.  
     - **Análisis cross-section**: compara bonos similares (emitidos en la misma fecha) con distintos cupones/duration.  

   - **Reporting y visualización**  
     - **Dashboard interactivo**: gráficos de flujos, sensibilidad, comparación de curvas (D3.js, Recharts).  
     - **Exportes**: PDF/Excel con tablas y gráficos listos para presentar.  
     - **Alertas y “what-if”**: notificaciones si la TIR supera umbrales o hay oportunidad de arbitraje.  

2. **Funcionalidades avanzadas / roadmap**  
   - Bonos con opciones embebidas: valoración OAS y análisis de volatilidad.  
   - Simulaciones de escenarios: Monte Carlo para rangos de precio ante cambios en tasas o volatilidad.  
   - Integración de datos en tiempo real: API de mercado (Refinitiv, Bloomberg, Yahoo Finance) para actualizar curvas.  
   - Módulo de crédito: cálculo de spreads sobre tasa libre de riesgo y análisis de riesgo de impago.  
   - Back-testing de estrategias: históricos de curva para evaluar rendimiento de bonos a lo largo del tiempo.  
   - Biblioteca de plantillas: genera presentaciones o informes en Word/PowerPoint.  

3. **Tecnología y stack sugerido**  
   - **Backend**  
     - Python con FastAPI o Flask  
     - Bibliotecas: pandas, NumPy, SciPy (root finding), QuantLib (opcional)  
     - Parser de PDF: Camelot, PyPDF2, Tika  
   - **Base de datos**  
     - PostgreSQL (con PostGIS si se geoposicionan emisores)  
   - **Frontend**  
     - React + TypeScript  
     - Componentes UI: Material-UI o Tailwind  
     - Gráficos: Recharts, D3.js  
   - **Despliegue**  
     - Docker + Kubernetes, o Render/Heroku para MVP  
   - **Autenticación y roles**  
     - JWT + OAuth2 si hay usuarios corporativos y públicos  

4. **Arquitectura y escalabilidad**  
   - **Microservicios**  
     - Servicio de parsing (Celery/RabbitMQ)  
     - Servicio de cálculos financieros  
     - Servicio de gestión de datos (bonos, curvas)  
   - **Colas y jobs asíncronos**  
     - Parseo de prospectos en background  
     - Cálculos pesados (bootstrap de curva)  
   - **API RESTful**  
     - Endpoints para:  
       - Subir prospecto & obtener job_id  
       - Consultar resultados (flujos, TIR, duración)  
       - Generar y descargar reportes  
   - **CI/CD**  
     - Tests unitarios de cálculo (alta cobertura)  
     - Linter & formateo (black, flake8)  
     - Despliegue automático en staging/producción  

5. **UX/UI y experiencia de usuario**  
   - **Wizard de carga**: paso a paso (subir, confirmar extracción, ajustes manuales).  
   - **Vista previa de datos**: corrige fechas o montos que el parser no detectó bien.  
   - **Interactividad**: sliders “what-if” y draggable para ajustar manualmente puntos de la curva.  
   - **Historial de análisis**: prospectos guardados con resultados para consulta y comparación.  
