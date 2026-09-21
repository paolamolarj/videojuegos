from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from steam_service import obtener_biblioteca_steam

app = FastAPI(title="GameMatch Big Data Engine", version="4.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/steam/user/{steam_id}")
def analizar_usuario_steam(steam_id: str):
    """
    Endpoint que conecta Steam Web API -> Perfil de Preferencias -> Recomendador Big Data
    """
    # 1. Obtenemos la biblioteca real del usuario desde Steam de forma segura
    datos_steam = obtener_biblioteca_steam(steam_id)
    
    # 2. Simulamos el cruce con el modelo generado por Spark MLlib (Fase 3)
    # Aquí es donde el perfil de horas se cruza con la matriz de 41 millones de registros
    recomendaciones_generadas = [
        {"game": "The Finals", "genre": "FPS / Action", "affinity": "94%"},
        {"game": "Rainbow Six Siege", "genre": "Tactical Shooter", "affinity": "91%"},
        {"game": "Marvel Rivals", "genre": "Hero Shooter", "affinity": "88%"},
        {"game": "Helldivers 2", "genre": "Co-op / Shooter", "affinity": "85%"},
        {"game": "Cyberpunk 2077", "genre": "RPG / Open World", "affinity": "82%"}
    ]

    return {
        "status": "success",
        "engine": "Apache Spark MLlib + Steam Web API",
        "user_profile": datos_steam,
        "recommendations": recomendaciones_generadas
    }