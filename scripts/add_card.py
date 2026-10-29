#!/usr/bin/env python3
"""Добавляет открытку на сайт: скачивает PNG по ссылке экспорта Figma,
делает миниатюру и дописывает запись в data.json.

Пример:
  python3 scripts/add_card.py --id tr-2026-10-29 --date 2026-10-29 \
    --holiday "Republic Day" --country "🇹🇷 Turkey" --lang RU \
    --file "7G Turkey Republic Day RU.png" \
    --url "https://www.figma.com/api/mcp/asset/....png"

Повторный запуск с тем же --id и --lang заменяет картинку (не дублирует).
Требуется: pip install pillow
"""
import argparse, json, os, sys, urllib.request
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--id', required=True, help='код страны + дата, напр. tr-2026-10-29')
    ap.add_argument('--date', required=True, help='YYYY-MM-DD')
    ap.add_argument('--holiday', required=True, help='название праздника по-английски')
    ap.add_argument('--country', required=True, help='флаг + страна по-английски, напр. "🇹🇷 Turkey"')
    ap.add_argument('--lang', required=True, choices=['RU', 'EN'])
    ap.add_argument('--file', required=True, help='имя файла для скачивания, напр. "7G Turkey Republic Day RU.png"')
    ap.add_argument('--url', required=True, help='ссылка export.url из Figma download_assets (png, scale 2)')
    a = ap.parse_args()

    base = f"{a.id}-{a.lang.lower()}"
    png = os.path.join(ROOT, 'cards', base + '.png')
    jpg = os.path.join(ROOT, 'thumbs', base + '.jpg')
    os.makedirs(os.path.dirname(png), exist_ok=True)
    os.makedirs(os.path.dirname(jpg), exist_ok=True)

    with urllib.request.urlopen(a.url, timeout=120) as r, open(png, 'wb') as f:
        f.write(r.read())
    im = Image.open(png)
    w, h = im.size
    t = im.convert('RGB')
    t.thumbnail((480, 480), Image.LANCZOS)
    t.save(jpg, quality=82, optimize=True, progressive=True)
    size = os.path.getsize(png)

    dpath = os.path.join(ROOT, 'data.json')
    data = json.load(open(dpath, encoding='utf-8')) if os.path.exists(dpath) else []
    entry = next((e for e in data if e['id'] == a.id), None)
    if entry is None:
        entry = {'id': a.id, 'date': a.date, 'holiday': a.holiday, 'country': a.country, 'images': []}
        data.append(entry)
    else:
        entry.update(date=a.date, holiday=a.holiday, country=a.country)
    img = {'lang': a.lang, 'src': f'cards/{base}.png', 'thumb': f'thumbs/{base}.jpg',
           'file': a.file, 'w': w, 'h': h, 'bytes': size}
    entry['images'] = [i for i in entry['images'] if i['lang'] != a.lang] + [img]
    entry['images'].sort(key=lambda i: 0 if i['lang'] == 'RU' else 1)
    data.sort(key=lambda e: (e['date'], e['id']))
    with open(dpath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    print(f"OK {a.id} {a.lang}: {w}x{h}, {size} bytes")


if __name__ == '__main__':
    sys.exit(main())
