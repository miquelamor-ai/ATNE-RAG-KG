"""
Migració Supabase: claus condicions curtes → llargues
Canvia conditions=['disl','l2','ac'] → ['dislexia','nouvingut','altes_capacitats']
i subvariables.l2 → subvariables.nouvingut (i similars) a atne_custom_profiles.

Executar UNA sola vegada post-deploy del commit que unifica les claus.
"""
import os, json, requests
from dotenv import load_dotenv

load_dotenv()
URL = os.getenv("SUPABASE_URL")
KEY = os.getenv("SUPABASE_SERVICE_KEY") or os.getenv("SUPABASE_ANON_KEY")
HDR = {"apikey": KEY, "Authorization": f"Bearer {KEY}", "Content-Type": "application/json"}

SHORT_TO_LONG = {"disl": "dislexia", "l2": "nouvingut", "ac": "altes_capacitats"}

def migrate_profile(pd):
    changed = False
    # conditions
    old_conds = pd.get("conditions") or []
    new_conds = [SHORT_TO_LONG.get(k, k) for k in old_conds]
    if new_conds != old_conds:
        pd["conditions"] = new_conds
        changed = True
    # subvariables keys
    sv = pd.get("subvariables")
    if isinstance(sv, dict):
        new_sv = {SHORT_TO_LONG.get(k, k): v for k, v in sv.items()}
        if new_sv != sv:
            pd["subvariables"] = new_sv
            changed = True
    return pd, changed

def main():
    r = requests.get(f"{URL}/rest/v1/atne_custom_profiles?select=id,profile_data", headers=HDR)
    rows = r.json()
    print(f"Total perfils: {len(rows)}")
    n_updated = 0
    for row in rows:
        rid = row["id"]
        pd = row.get("profile_data") or {}
        new_pd, changed = migrate_profile(pd)
        if changed:
            resp = requests.patch(
                f"{URL}/rest/v1/atne_custom_profiles?id=eq.{rid}",
                headers={**HDR, "Prefer": "return=minimal"},
                json={"profile_data": new_pd},
            )
            if resp.status_code in (200, 204):
                print(f"  OK {rid}: {pd.get('conditions')} -> {new_pd.get('conditions')}")
                n_updated += 1
            else:
                print(f"  ERR {rid}: error {resp.status_code} {resp.text}")
    print(f"\nActualitzats: {n_updated}/{len(rows)}")

if __name__ == "__main__":
    main()
