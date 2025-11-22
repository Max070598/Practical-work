# Practical 7 – TDD + Genshin Impact API Integration

**Модуль:** Python OOP + CLI + TDD  

---

## Опис проєкту

Фінальна ітерація проєкту, що поєднує:
- **CLI** для створення персонажів та предметів
- **API інтеграцію** з [Genshin Impact API](https://genshin.jmp.blue/)
- **Генерацію статів** за рідкістю
- **Markdown-рендеринг** через `TextFactory`
- **TDD** — 100% покриття тестами

---

## Використане API

- **URL**: `https://genshin.jmp.blue/`
- **Документація**: https://github.com/genshindev/api
- **Особливості**:
  - Немає базових статів → **генеруємо випадково** за рідкістю
  - Є опис, здібності, елемент

---

## Функціонал CLI (`python main.py --chars`)

| Команда | Опис |
|--------|------|
| `list chars` | Список персонажів з API |
| `create char --api <name>` | Створити з API |
| `print char <name>` | Markdown-вивід |
| `create char` | Ручне створення |
| `create item` | Ручне створення предмета |
| `add_to_char --char_id <char> --id <item>` | Екіпірувати |
| `ls --id <name>` | Деталі об’єкта |
| `save <name>` / `load <name>` | Збереження гри |

---

## Тести (TDD)

pytest -v
→ 13 passed

test_api.py — генерація статів
test_cli_api.py — list, create --api
test_render_character.py — Markdown
Усі старі тести — PASS

---

## Запуск

pip install -r requirements.txt
python main.py --chars

---

## Скриншоти

list chars
create char --api zhongli
add_to_char
pytest -v

---

## Генерація статів

```python
if rarity == 5:
    health = random.randint(120, 150)
    armor = random.randint(12, 18)
    attack = random.randint(20, 28)
