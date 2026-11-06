#!/usr/bin/env python3
"""Собирает список отметок (mentions) для сообщения в Teams.

Айдана отмечается всегда. Дополнительно — ответственный за регион каждой открытки
из сообщения (столбец «Регион» таблицы). Неизвестный или пустой регион — только Айдана.

Пример:
  python3 scripts/mentions.py "СНГ" "MENA"

Печатает JSON для параметра mentions в teams_reply_channel_message.
"""
import json, sys

ALWAYS = {"id": "f4ef0425-ded7-4fae-85b3-696687131bf1", "displayName": "Aidana Kabdykaparova"}  # a.kabdykaparova@7g.team

ZAMIRA = {"id": "d42d7baf-eb37-46cf-b83d-810ef88814b4", "displayName": "Zamira Akhmetzhanova"}  # z.akhmetzhanova@7g.team
ARVIN = {"id": "7ebf3585-8265-4801-8774-0b325ca1cbcf", "displayName": "Arvin Singh"}  # arvin@7g.team
MARAT = {"id": "e9d2bf76-e3b9-43c7-90eb-1f00d4353c43", "displayName": "Marat Zhunussov"}  # m.zhunusov@7g.team
AZIZ = {"id": "406bbebd-344e-40e4-969c-e6f1019445c6", "displayName": "Aziz Kazimov"}  # a.kazimov@7g.team

# Значение столбца «Регион» (без учёта регистра и пробелов по краям) → ответственный.
BY_REGION = {
    "снг": ZAMIRA,
    "снг и ца": ZAMIRA,
    "apac": ARVIN,
    "mena": MARAT,
    "африка": AZIZ,
}


def mentions(regions):
    out = [ALWAYS]
    for r in regions:
        person = BY_REGION.get((r or "").strip().casefold())
        if person and person not in out:
            out.append(person)
    return out


if __name__ == '__main__':
    print(json.dumps(mentions(sys.argv[1:]), ensure_ascii=False))
