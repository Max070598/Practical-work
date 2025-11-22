from unittest.mock import patch
from infra.api.genshin_api import GenshinAPI

def test_get_character_generates_stats():
    api = GenshinAPI()
    with patch.object(api, "_get") as mock_get:
        mock_get.return_value = {
            "name": "Zhongli", "rarity": 5, "description": "Geo Archon",
            "element": "Geo", "skills": []
        }
        data = api.get_character("zhongli")
        stats = data["generated_stats"]
        assert 110 <= stats["health"] <= 150
        assert 10 <= stats["armor"] <= 18
        assert 15 <= stats["attack"] <= 25