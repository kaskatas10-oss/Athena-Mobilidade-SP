#!/usr/bin/env python3
"""Atualiza previsão meteorológica. Não simula status Metrô/CPTM."""
import json
import pathlib
import urllib.request
from datetime import datetime, timezone
url=("https://api.open-meteo.com/v1/forecast?"
     "latitude=-23.5505&longitude=-46.6333&"
     "current=temperature_2m,precipitation,weather_code&"
     "daily=temperature_2m_max,temperature_2m_min,precipitation_probability_max,"
     "precipitation_sum&timezone=America%2FSao_Paulo&forecast_days=1")
req=urllib.request.Request(url,headers={"User-Agent":"Athena-Mobilidade-SP/1.0"})
with urllib.request.urlopen(req,timeout=25) as response:
    payload=json.load(response)
current=payload.get("current",{})
daily=payload.get("daily",{})
assert current.get("time") and daily.get("time"), "Previsão incompleta"
doc={
    "updated_at":datetime.now(timezone.utc).isoformat(),
    "source":"Open-Meteo",
    "source_url":"https://open-meteo.com/",
    "reference":"São Paulo, SP",
    "current":{k:current.get(k) for k in ("time","temperature_2m","precipitation","weather_code")},
    "today":{k:(daily.get(k) or [None])[0] for k in ("time","temperature_2m_max","temperature_2m_min","precipitation_probability_max","precipitation_sum")},
    "transit":{"line3":"Não verificado","line11":"Não verificado"}
}
pathlib.Path("data").mkdir(exist_ok=True)
pathlib.Path("data/mobilidade.json").write_text(
    json.dumps(doc,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
