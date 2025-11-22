# infra/api/genshin_api.py
import requests
import random
from typing import List, Dict, Any

BASE_URL = "https://genshin.jmp.blue"


class GenshinAPI:
    def __init__(self):
        self.session = requests.Session()

    def _get(self, endpoint: str) -> Any:
        """Send GET request and return JSON or raise error."""
        try:
            response = self.session.get(f"{BASE_URL}{endpoint}")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise RuntimeError(f"API request failed: {e}")

    # === CHARACTERS ===
    def get_characters_list(self) -> List[str]:
        """Return list of character names."""
        return self._get("/characters")

    def get_character(self, name: str) -> Dict:
        """Return character data with generated stats based on rarity."""
        data = self._get(f"/characters/{name.lower()}")
        rarity = data.get("rarity", 1)

        # Stat ranges by rarity
        ranges = {
            1: (50, 80, 5, 10, 3, 6),
            2: (60, 90, 7, 12, 4, 8),
            3: (70, 100, 8, 15, 5, 10),
            4: (90, 120, 12, 20, 8, 15),
            5: (110, 150, 15, 25, 10, 18)
        }
        h_min, h_max, a_min, a_max, d_min, d_max = ranges.get(rarity, ranges[3])
        data["generated_stats"] = {
            "health": random.randint(h_min, h_max),
            "armor": random.randint(d_min, d_max),
            "attack": random.randint(a_min, a_max)
        }
        return data

    # === WEAPONS ===
    def get_weapons_list(self) -> List[str]:
        """Return list of weapon names."""
        return self._get("/weapons")

    def get_weapon(self, name: str) -> Dict:
        """Return weapon data with bonus stats."""
        data = self._get(f"/weapons/{name.lower()}")
        rarity = data.get("rarity", 1)
        base_atk = data.get("baseAttack", 30)
        data["bonuses"] = {
            "health_bonus": 0,
            "armor_bonus": random.randint(0, rarity * 3),
            "attack_bonus": base_atk // 5 + random.randint(0, rarity * 5)
        }
        return data