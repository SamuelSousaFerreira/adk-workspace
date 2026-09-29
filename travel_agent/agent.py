"""
Agente de viagens com ferramentas de função personalizadas
Demonstra o funcionamento conjunto de várias ferramentas personalizadas.
Referência: https://google.github.io/adk-docs/tools-custom/function-tools/
"""
from google.adk.agents import LlmAgent

# Ferramenta 1: pesquisar voos

def search_flights(destination: str, departure_date: str) -> dict:
    """Busca voos disponíveis para um destino em uma data específica.
    Utilize esta ferramenta quando um cliente quiser saber as opções de voo.
    Argumentos:
        destination (str): a cidade de destino (ex: "Paris", "Tóquio").
        departure_date (str): data de partida no formato AAAA-MM-DD.
    Retorna:
        dict: resultados da pesquisa de voos.
        Em caso de sucesso: {'status': 'success', 'flights': [...], 'count': N}
        Em caso de erro: {'status': 'error', 'error_message': 'explanation'}
    """
    # Dados de voo simulados
    available_flights = {
            "paris": [
                {"flight_number": "AF123", "price_usd": 450, "duration_hours": 8},
                {"flight_number": "BA456", "price_usd": 480, "duration_hours": 7.5},
            ],
            "tokyo": [
                {"flight_number": "JL789", "price_usd": 850, "duration_hours": 13},
                {"flight_number": "ANA101", "price_usd": 820, "duration_hours": 12.5},
            ],
    }
    
    dest_key = destination.lower()
    
    if dest_key not in available_flights:
        return {
            "status": "error",
            "error_message": f"Nenhum voo encontrado para {destination}. Tente Paris ou Tóquio."
        }
    return {
        "status": "success",
        "destination": destination,
        "departure_date": departure_date,
        "flights": available_flights[dest_key],
        "count": len(available_flights[dest_key])
        }

# Ferramenta 2: pesquisar hotéis
def search_hotels(city: str, check_in_date: str) -> dict:
    """Busca hotéis disponíveis em uma cidade para uma data de check-in específica.
    Utilize esta ferramenta quando um cliente precisar de acomodação.
    Argumentos:
    city (str): o nome da cidade (ex: "Paris", "Tóquio").
    check_in_date (str): data de check-in no formato AAAA-MM-DD.
    Retorna:
    dict: resultados da pesquisa de hotéis.
    Em caso de sucesso: {'status': 'success', 'hotels': [...], 'count': N}
    Em caso de erro: {'status': 'error', 'error_message': 'explanation'}
    """
    # Dados simulados de hotel
    available_hotels = {
        "paris": [
            {"name": "Hotel Eiffel", "price_per_night_usd": 150, "rating": 4.5},
            {"name": "Louvre Inn", "price_per_night_usd": 120, "rating": 4.2},
        ],
        "tokyo": [
            {"name": "Shibuya Grand", "price_per_night_usd": 180, "rating": 4.7},
            {"name": "Tokyo Bay Hotel", "price_per_night_usd": 140, "rating": 4.3},
        ],
    }
    
    city_key = city.lower()
    
    if city_key not in available_hotels:
        return {
            "status": "error",
            "error_message": f"Nenhum hotel encontrado em {city}. Tente Paris ou Tóquio."
        }
    return {
        "status": "success",
        "city": city,
        "check_in_date": check_in_date,
        "hotels": available_hotels[city_key],
        "count": len(available_hotels[city_key])
    }

# Ferramenta 3: calcular o orçamento da viagem
def calculate_trip_budget(flight_price: float, hotel_price: float, num_nights: int) -> dict:
    """Calcula o orçamento total da viagem, incluindo voos e hospedagem.
    Use esta ferramenta após encontrar os preços de voos e hotéis para fornecer ao
    cliente uma estimativa do valor total.
    Argumentos:
    flight_price (float): custo de uma passagem aérea de ida e volta em USD.
    hotel_price (float): custo do hotel por noite em USD.
    num_nights (int): número de noites de estadia.
    Retorna:
    dict: detalhamento do orçamento.
    Sempre retorna: {'status': 'success', 'total_usd': X, 'breakdown': {...}}
    """
    hotel_total = hotel_price * num_nights
    total = flight_price + hotel_total
    return {
        "status": "success",
        "total_usd": round(total, 2),
        "breakdown": {
            "flight_cost": flight_price,
            "hotel_cost_per_night": hotel_price,
            "num_nights": num_nights,
            "hotel_total": round(hotel_total, 2)
        }
    }
    
# Criar um agente de viagens com todas as três ferramentas
root_agent = LlmAgent(
    model='gemini-3.5-flash',
    name='travel_agent',
    description='Ajuda os usuários a planejar viagens, encontrando voos e hotéis.',
    instruction="""
    Você é um assistente de agente de viagens prestativo.
    Suas capacidades:
    - Pesquisar voos usando search_flights(destination, departure_date)
    - Pesquisar hotéis usando search_hotels(city, check_in_date)
    - Calcular o orçamento da viagem usando calculate_trip_budget(flight_price,
    hotel_price, num_nights)
    Ao ajudar os usuários:
    1. Se perguntarem sobre voos, use search_flights
    2. Se perguntarem sobre hotéis, use search_hotels
    3. Se eles quiserem uma estimativa completa da viagem, use as duas ferramentas de
    pesquisa e depois calculate_trip_budget
    4. Apresente as opções sempre de forma clara, incluindo os preços
    5. Se uma ferramenta retornar um erro, peça desculpas e sugira destinos
    disponíveis (Paris ou Tóquio)
    Seja amigável e ajude os usuários a planejar a viagem perfeita.
    """,
    tools=[search_flights, search_hotels, calculate_trip_budget]
)