import json
import os
import requests


class CampusAPI:
    BASE_URL = "https://api.campus.kpi.ua"
    CACHE_DIR = "data"

    @classmethod
    def _get(this, path: str, **params):
        resp = requests.get(f"{this.BASE_URL}/{path}", params=params, timeout=10)
        resp.raise_for_status()
        return resp.json()

    @classmethod
    def _cache_path(this, name: str) -> str:
        os.makedirs(this.CACHE_DIR, exist_ok=True)
        return os.path.join(this.CACHE_DIR, f"{name}.json")

    @classmethod
    def _load_cache(this, name: str):
        path = this._cache_path(name)
        if not os.path.exists(path):
            return None
        
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    @classmethod
    def _save_cache(this, name: str, data):
        path = this._cache_path(name)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    @classmethod
    def groups_list(this):
        cache = this._load_cache("groups")
        if cache:
            return cache
        data = this._get("schedule/groups")
        this._save_cache("groups", data)
        return data

    @classmethod
    def find_group_id(this, group_name: str):
        groups = this.groups_list()
        for group in groups:
            if group["name"].lower() == group_name.lower():
                return group["id"]
        return None

    @classmethod
    def group_schedule(this, group_id: str):
        cache_name = f"schedule_{group_id}"
        data = this._load_cache(cache_name)
        if data:
            return data
        data = this._get("schedule/lessons", groupId=group_id)
        this._save_cache(cache_name, data)
        return data
