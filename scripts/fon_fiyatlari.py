"""BES (emeklilik) fon fiyatlarını TEFAS'tan çekip prices/emk.json dosyasına yazar.

GitHub Actions tarafından her gün çalıştırılır (bkz. .github/workflows/fon-fiyatlari.yml).
Takip edilecek fon kodları prices/fonlar.txt dosyasındadır (her satıra bir kod).
Program (index.html) bu JSON'u aynı adresten okur; kişisel veri içermez.
"""
import datetime as dt
import json
import pathlib
import sys

from tefas import Crawler

ROOT = pathlib.Path(__file__).resolve().parent.parent
LIST = ROOT / "prices" / "fonlar.txt"
OUT = ROOT / "prices" / "emk.json"


def to_float(v):
    try:
        return float(str(v).replace(",", "."))
    except (TypeError, ValueError):
        return 0.0


def main():
    codes = sorted({l.strip().upper() for l in LIST.read_text(encoding="utf-8").splitlines()
                    if l.strip() and not l.strip().startswith("#")})
    old = json.loads(OUT.read_text(encoding="utf-8")) if OUT.exists() else {}
    funds = dict(old.get("funds", {}))
    today = dt.date.today()
    start = (today - dt.timedelta(days=75)).isoformat()   # belge tarihindeki fiyat için ~2,5 ay geçmiş
    crawler = Crawler()
    errors = []
    for code in codes:
        try:
            df = crawler.fetch(start=start, end=today.isoformat(), name=code, kind="EMK",
                               columns=["code", "date", "price", "title"])
            if df is None or df.empty:
                errors.append(f"{code}: veri yok")
                continue
            df = df.sort_values("date")
            row = df.iloc[-1]
            price = to_float(row["price"])
            hist = {str(d)[:10]: to_float(p) for d, p in zip(df["date"], df["price"]) if to_float(p) > 0}
            if price > 0:
                funds[code] = {"price": price, "date": str(row["date"])[:10],
                               "title": str(row.get("title", "") or ""), "hist": hist}
            else:
                errors.append(f"{code}: fiyat 0")
        except Exception as e:  # tek bir fon hatası diğerlerini durdurmasın
            errors.append(f"{code}: {e}")
    changed = funds != old.get("funds") or errors != old.get("errors")
    out = {
        "updated": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds") if changed else old.get("updated"),
        "funds": funds,
        "errors": errors,
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"{len(funds)} fon, {len(errors)} hata")
    for e in errors:
        print("  -", e)
    if codes and not any(c in funds for c in codes):
        sys.exit("Hiçbir fonun fiyatı alınamadı")


if __name__ == "__main__":
    main()
