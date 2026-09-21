import os
import requests
from fastapi import HTTPException

# La API Key debe obtenerse exclusivamente de una variable de entorno (nunca hardcodeada ni expuesta al frontend)
STEAM_API_KEY = os.getenv("STEAM_API_KEY", "TU_STEAM_API_KEY_AQUI")

def obtener_biblioteca_steam(steam_id: str):
    """
    Consulta la Steam Web API para obtener los juegos y horas jugadas de un usuario.
    Endpoint oficial: IPlayerService/GetOwnedGames
    """
    url = "https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/"
    params = {
        "key": STEAM_API_KEY,
        "steamid": steam_id,
        "format": "json",
        "include_appinfo": True, # Para traer el nombre de los juegos además del app_id
        "include_played_free_games": True
    }

    try:
        response = requests.get(url, params=params)
        
        if response.status_code != 200:
            raise HTTPException(
                status_code=502, 
                detail="Error al comunicarse con la Steam Web API. Verifica tu SteamID o API Key."
            )

        data = response.json()
        games_response = data.get("response", {})
        
        # Si el perfil es privado o el SteamID no existe
        if not games_response or "games" not in games_response:
            return {
                "steam_id": steam_id,
                "total_games_owned": 0,
                "games": [],
                "message": "El perfil de Steam es privado o el ID no es válido."
            }

        juegos_crudos = games_response.get("games", [])
        
        # Procesamos y filtramos la información relevante para nuestro recomendador
        biblioteca_procesada = []
        for jg in juegos_crudos:
            # Convertimos los minutos jugados a horas
            horas_jugadas = round(jg.get("playtime_forever", 0) / 60.0, 2)
            biblioteca_procesada.append({
                "app_id": jg.get("appid"),
                "title": jg.get("name"),
                "hours_played": horas_jugadas
            })

        # Ordenamos los juegos por los más jugados (perfil de preferencias)
        biblioteca_procesada.sort(key=lambda x: x["hours_played"], reverse=True)

        return {
            "steam_id": steam_id,
            "total_games_owned": games_response.get("game_count", 0),
            "top_played_games": biblioteca_procesada[:10] # Top 10 juegos con más horas
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))