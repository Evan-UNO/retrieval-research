"""Read Zotero metadata through the local API or an explicitly selected frozen backup."""
import argparse
import json
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import unquote, urlencode, urlparse
from urllib.request import ProxyHandler, build_opener


def read_api(query, item_key, limit, attachments):
    opener = build_opener(ProxyHandler({}))
    base = "http://127.0.0.1:23119/api/users/0/"

    def get(endpoint, text=False):
        with opener.open(base + endpoint, timeout=5) as response:
            value = response.read().decode("utf-8")
        return value if text else json.loads(value)

    if item_key:
        raw = [get("items/" + item_key)]
    else:
        params = {"limit": limit, "format": "json"}
        if query:
            params["q"] = query
        raw = get("items/top?" + urlencode(params))
    records = []
    for obj in raw:
        data = obj["data"]
        if data.get("itemType") in ("attachment", "note", "annotation"):
            continue
        record = {k: data.get(k) for k in (
            "key", "itemType", "title", "abstractNote", "date", "DOI", "url", "tags", "collections"
        )}
        record["library"] = obj.get("library")
        record["attachments"] = []
        if attachments or item_key:
            for child in get("items/" + data["key"] + "/children?format=json"):
                entry = child["data"]
                if entry.get("itemType") != "attachment":
                    continue
                attachment = {k: entry.get(k) for k in ("key", "title", "filename", "contentType", "linkMode")}
                if entry.get("linkMode") in ("imported_file", "imported_url", "linked_file"):
                    try:
                        value = get("items/" + entry["key"] + "/file/view/url", text=True).strip()
                        uri = urlparse(value)
                        if uri.scheme == "file" and uri.netloc in ("", "localhost"):
                            path = unquote(uri.path)
                            if sys.platform == "win32" and len(path) > 2 and path[2] == ":":
                                path = path[1:]
                            attachment["localPath"] = str(Path(path))
                            attachment["exists"] = Path(path).is_file()
                        else:
                            attachment["pathStatus"] = "not-a-local-file"
                    except Exception as exc:
                        attachment["pathStatus"] = str(exc)
                record["attachments"].append(attachment)
        records.append(record)
    return {"source": {"kind": "local-api", "scope": "personal-library", "readOnly": True}, "records": records}


def read_snapshot(snapshot, data_dir, query, item_key, limit, attachments):
    snapshot = Path(snapshot).resolve(strict=True)
    # immutable is safe only for an explicitly supplied frozen backup, not a live database.
    if not snapshot.name.endswith(".bak"):
        raise ValueError("--snapshot only accepts a frozen Zotero .bak file; do not pass the live database")
    for suffix in ("-wal", "-journal"):
        sidecar = Path(str(snapshot) + suffix)
        if sidecar.exists() and sidecar.stat().st_size:
            raise ValueError("Snapshot has a journal/WAL; use a consistent Zotero backup instead")
    stamp = snapshot.stat()
    c = sqlite3.connect(snapshot.as_uri() + "?mode=ro&immutable=1", uri=True)
    c.row_factory = sqlite3.Row
    try:
        if c.execute("PRAGMA quick_check").fetchone()[0] != "ok":
            raise ValueError("Snapshot failed SQLite integrity check")
        rows = c.execute("""SELECT i.itemID,i.key,i.libraryID,t.typeName
            FROM items i JOIN itemTypes t USING(itemTypeID)
            WHERE t.typeName NOT IN ('attachment','note','annotation')
            AND i.itemID NOT IN (SELECT itemID FROM deletedItems)
            ORDER BY i.dateAdded DESC,i.itemID DESC""").fetchall()
        records = []
        for row in rows:
            fields = dict(c.execute("""SELECT f.fieldName,v.value FROM itemData d
                JOIN fields f USING(fieldID) JOIN itemDataValues v USING(valueID)
                WHERE d.itemID=?""", (row["itemID"],)).fetchall())
            if item_key and row["key"] != item_key:
                continue
            if query and query.casefold() not in str(fields.get("title", "")).casefold():
                continue
            record = {"key": row["key"], "libraryID": row["libraryID"], "itemType": row["typeName"], **fields}
            record["tags"] = [r[0] for r in c.execute("""SELECT t.name FROM tags t
                JOIN itemTags it USING(tagID) WHERE it.itemID=?""", (row["itemID"],))]
            record["collections"] = [dict(r) for r in c.execute("""SELECT co.key,co.collectionName
                FROM collections co JOIN collectionItems ci USING(collectionID)
                WHERE ci.itemID=?""", (row["itemID"],))]
            record["attachments"] = []
            if attachments or item_key:
                children = c.execute("""SELECT i.key,a.path,a.contentType FROM itemAttachments a
                    JOIN items i USING(itemID) WHERE a.parentItemID=?
                    AND i.itemID NOT IN (SELECT itemID FROM deletedItems)""", (row["itemID"],))
                for child in children:
                    attachment = dict(child)
                    value = child["path"] or ""
                    path = None
                    if value.startswith("storage:"):
                        folder = (Path(data_dir) / "storage" / child["key"]).resolve()
                        candidate = (folder / value[len("storage:"):]).resolve()
                        if candidate.is_relative_to(folder):
                            path = candidate
                    elif value and not value.startswith("attachments:") and Path(value).is_absolute():
                        path = Path(value)
                    if path is not None:
                        attachment.update(localPath=str(path), exists=path.is_file())
                    else:
                        attachment["pathStatus"] = "unresolved; linked attachment base directory may be required"
                    record["attachments"].append(attachment)
            records.append(record)
            if len(records) == limit:
                break
    finally:
        c.close()
    after = snapshot.stat()
    if (stamp.st_mtime_ns, stamp.st_size) != (after.st_mtime_ns, after.st_size):
        raise ValueError("Backup changed while reading; retry after Zotero finishes its backup")
    return {"source": {"kind": "snapshot", "path": str(snapshot), "readOnly": True,
        "fileModifiedUTC": datetime.fromtimestamp(stamp.st_mtime, timezone.utc).isoformat(),
        "warning": "Frozen backup: file modification time is not a guarantee of library freshness."}, "records": records}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    selection = parser.add_mutually_exclusive_group()
    selection.add_argument("--query", help="Title search (API may also match creators/year)")
    selection.add_argument("--item-key", help="Exact eight-character Zotero item key")
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--attachments", action="store_true", help="Include attachment metadata and local file availability")
    parser.add_argument("--snapshot", type=Path, help="Explicit .bak fallback; never selected automatically")
    parser.add_argument("--data-dir", type=Path, default=Path.home() / "Zotero")
    args = parser.parse_args()
    if not 1 <= args.limit <= 100:
        parser.error("--limit must be between 1 and 100")
    if args.item_key and (len(args.item_key) != 8 or not args.item_key.isascii() or not args.item_key.isalnum()):
        parser.error("--item-key must be eight ASCII letters/digits")
    try:
        if args.snapshot:
            result = read_snapshot(args.snapshot, args.data_dir, args.query, args.item_key, args.limit, args.attachments)
        else:
            result = read_api(args.query, args.item_key, args.limit, args.attachments)
        result["returnedCount"] = len(result["records"])
        result["limit"] = args.limit
        result["possiblyTruncated"] = len(result["records"]) >= args.limit
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as exc:
        print(json.dumps({"error": str(exc), "nextStep": (
            "Open Zotero and enable its local read API, or explicitly supply a .bak snapshot. "
            "No settings were changed. You may also use an exported bibliography or local PDF directly."
        )}, ensure_ascii=False), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    raise SystemExit(main())
