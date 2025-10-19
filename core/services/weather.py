"""
Service météo utilisant l'API OpenWeatherMap
"""

import requests
from django.conf import settings
from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)


class WeatherService:
    """
    Service pour récupérer les données météo d'OpenWeatherMap
    """
    
    BASE_URL = "https://api.openweathermap.org/data/2.5"
    
    # Coordonnées de Jarny, France
    JARNY_LAT = 49.1586
    JARNY_LON = 5.8808
    
    def __init__(self):
        self.api_key = settings.OPENWEATHER_API_KEY
        #print(f"🔑 API Key chargée : '{self.api_key}'")
        #print(f"🔑 Longueur de la clé : {len(self.api_key)}")
        
    def get_current_weather(self):
        """
        Récupère la météo actuelle pour Jarny
        Mise en cache pendant 30 minutes
        """
        cache_key = 'weather_current_jarny'
        cached_data = cache.get(cache_key)
        
        if cached_data:
            #print("📦 Données météo depuis le cache")
            return cached_data
        
        try:
            url = f"{self.BASE_URL}/weather"
            params = {
                'lat': self.JARNY_LAT,
                'lon': self.JARNY_LON,
                'appid': self.api_key,
                'units': 'metric',  # Celsius
                'lang': 'fr'
            }
            
            #print(f"🌐 URL API : {url}")
            #print(f"📍 Params : {params}")

            response = requests.get(url, params=params, timeout=5)
            #print(f"📡 Status Code : {response.status_code}")
            #print(f"📄 Response : {response.text[:200]}")

            response.raise_for_status()
            
            data = response.json()
            
            # Formatage des données
            weather_data = {
                'temperature': round(data['main']['temp']),
                'feels_like': round(data['main']['feels_like']),
                'description': data['weather'][0]['description'].capitalize(),
                'icon': data['weather'][0]['icon'],
                'humidity': data['main']['humidity'],
                'pressure': data['main']['pressure'],
                'wind_speed': round(data['wind']['speed'] * 3.6),  # m/s vers km/h
                'wind_direction': data['wind']['deg'],
                'clouds': data['clouds']['all'],
                'visibility': data.get('visibility', 0) / 1000,  # mètres vers km
                'city': 'Jarny',
                'success': True
            }

            #print("✅ Données formatées :")
            #print(weather_data)

            # Mise en cache pour 30 minutes
            cache.set(cache_key, weather_data, 60 * 30)
            
            return weather_data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Erreur API météo : {e}")
            #print(f"❌ EXCEPTION CAPTURÉE : {e}")
            #print(f"❌ Type : {type(e)}")
            return {
                'success': False,
                'error': 'Impossible de récupérer les données météo'
            }
        except Exception as e:  # ← AJOUT
            logger.error(f"Erreur inattendue : {e}")  # ← AJOUT
            #print(f"❌ EXCEPTION GÉNÉRALE : {e}")  # ← AJOUT
            import traceback  # ← AJOUT
            traceback.print_exc()  # ← AJOUT
            return {
                'success': False,
                'error': f'Erreur inattendue : {str(e)}'
            }
    
    def get_forecast(self, days=5):
        """
        Récupère les prévisions météo pour les prochains jours
        Mise en cache pendant 1 heure
        """
        cache_key = f'weather_forecast_jarny_{days}d'
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return cached_data
        
        try:
            url = f"{self.BASE_URL}/forecast"
            params = {
                'lat': self.JARNY_LAT,
                'lon': self.JARNY_LON,
                'appid': self.api_key,
                'units': 'metric',
                'lang': 'fr',
                'cnt': days * 8  # 8 prévisions par jour (toutes les 3h)
            }
            
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            
            # Grouper les prévisions par jour
            daily_forecasts = {}
            
            for item in data['list']:
                from datetime import datetime
                date = datetime.fromtimestamp(item['dt']).date()
                
                if date not in daily_forecasts:
                    daily_forecasts[date] = {
                        'date': date,
                        'temp_min': item['main']['temp_min'],
                        'temp_max': item['main']['temp_max'],
                        'description': item['weather'][0]['description'],
                        'icon': item['weather'][0]['icon'],
                        'wind_speed': item['wind']['speed'] * 3.6,
                        'humidity': item['main']['humidity'],
                    }
                else:
                    # Mettre à jour min/max
                    daily_forecasts[date]['temp_min'] = min(
                        daily_forecasts[date]['temp_min'],
                        item['main']['temp_min']
                    )
                    daily_forecasts[date]['temp_max'] = max(
                        daily_forecasts[date]['temp_max'],
                        item['main']['temp_max']
                    )
            
            forecast_data = {
                'forecasts': [
                    {
                        'date': forecast['date'],
                        'temp_min': round(forecast['temp_min']),
                        'temp_max': round(forecast['temp_max']),
                        'description': forecast['description'].capitalize(),
                        'icon': forecast['icon'],
                        'wind_speed': round(forecast['wind_speed']),
                        'humidity': forecast['humidity'],
                    }
                    for forecast in list(daily_forecasts.values())[:days]
                ],
                'success': True
            }
            
            # Mise en cache pour 1 heure
            cache.set(cache_key, forecast_data, 60 * 60)
            
            return forecast_data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Erreur API météo prévisions : {e}")
            return {
                'success': False,
                'error': 'Impossible de récupérer les prévisions météo'
            }
    
    def get_wind_direction_text(self, degrees):
        """
        Convertit les degrés en direction cardinale
        """
        directions = [
            'N', 'NNE', 'NE', 'ENE',
            'E', 'ESE', 'SE', 'SSE',
            'S', 'SSO', 'SO', 'OSO',
            'O', 'ONO', 'NO', 'NNO'
        ]
        index = round(degrees / 22.5) % 16
        return directions[index]
    
    def is_good_flying_conditions(self, weather_data):
        """
        Détermine si les conditions sont bonnes pour voler
        Critères :
        - Vent < 25 km/h
        - Pas de pluie
        - Visibilité > 5 km
        """
        if not weather_data.get('success'):
            return None
        
        wind_ok = weather_data['wind_speed'] < 25
        visibility_ok = weather_data['visibility'] > 5
        
        # Vérifier s'il pleut (codes météo commençant par 2, 3, 5)
        # On suppose que l'icône contient 'd' pour jour ou 'n' pour nuit
        icon_code = weather_data['icon'][:2]
        no_rain = icon_code not in ['09', '10', '11', '13']
        
        return wind_ok and visibility_ok and no_rain