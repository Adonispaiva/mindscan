import os, sys, json, shutil, hashlib, time
from datetime import datetime, timedelta

ROOT = r"D:\projetos-inovexa\mindscan"
BACKUP = os.path.join(ROOT, "backup")
ARCHIVE = os.path.join(BACKUP, "_archive")
LOGS = os.path.join(ROOT, "logs")
CONFIG = os.path.join(ROOT, "config", "backup_policy.json")
REPORT = os.path.join(LOGS, f"backup_manager_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")

CHUNK = 8 * 1024 * 1024  # 8MB

def sizeof(path):
    total = 0
    for r, _, fs in os.walk(path):
        for f in fs:
            try: total += os.path.getsize(os.path.join(r, f))
            except: pass
    return total

def load_policy():
    os.makedirs(os.path.dirname(CONFIG), exist_ok=True)
    defaults = {
        "keep_last": 2,
        "retention_days": 15,
        "max_backup_dir_gb": 5,
        "purge_archive_after_days": 7,
        "force_purge_when_single_file_over_gb": 20,
        "dry_run": False,
        "progressive_hash": True
    }
    if not os.path.exists(CONFIG):
        with open(CONFIG, "w", encoding="utf-8") as f: json.dump(defaults, f, indent=2, ensure_ascii=False)
        return defaults
    with open(CONFIG, "r", encoding="utf-8") as f: policy = json.load(f)
    for k, v in defaults.items():
        policy.setdefault(k, v)
    return policy

def progress_bar(readb, total, name):
    percent = 100 * readb / total if total else 100
    bar_len = 50
    filled = int(bar_len * percent / 100)
    bar = "█" * filled + "-" * (bar_len - filled)
    sys.stdout.write(f"\r🔍 {name}: |{bar}| {percent:5.1f}%")
    sys.stdout.flush()

def sha256_file(path, progressive=True):
    h = hashlib.sha256()
    sz = os.path.getsize(path)
    readb = 0
    with open(path, "rb") as f:
        while True:
            chunk = f.read(CHUNK)
            if not chunk: break
            h.update(chunk)
            if progressive:
                readb += len(chunk)
                progress_bar(readb, sz, os.path.basename(path))
    if progressive: sys.stdout.write("\n")
    return h.hexdigest()

def purge(path, dry, progress):
    info = {"file": path, "deleted": False, "error": None, "hash": None}
    try:
        info["hash"] = sha256_file(path, progress)
        if not dry:
            os.remove(path)
            info["deleted"] = True
    except Exception as e:
        info["error"] = str(e)
    return info

def main():
    policy = load_policy()
    os.makedirs(LOGS, exist_ok=True)
    os.makedirs(ARCHIVE, exist_ok=True)

    report = {
        "started_at": datetime.now().isoformat(),
        "policy": policy,
        "kept": [], "archived": [], "purged": [], "errors": []
    }

    backups = [os.path.join(BACKUP, f) for f in os.listdir(BACKUP) if os.path.isfile(os.path.join(BACKUP, f))]
    backups.sort(key=os.path.getmtime, reverse=True)
    keep = backups[:policy["keep_last"]]
    archive = backups[policy["keep_last"]:]

    for f in keep:
        report["kept"].append(f)
    for f in archive:
        try:
            shutil.move(f, os.path.join(ARCHIVE, os.path.basename(f)))
            report["archived"].append(f)
        except Exception as e:
            report["errors"].append({"file": f, "error": str(e)})

    # purga por política
    now = datetime.now()
    for f in os.listdir(ARCHIVE):
        fp = os.path.join(ARCHIVE, f)
        if not os.path.isfile(fp): continue
        age = (now - datetime.fromtimestamp(os.path.getmtime(fp))).days
        size_gb = os.path.getsize(fp)/(1024**3)
        if age >= policy["purge_archive_after_days"] or size_gb >= policy["force_purge_when_single_file_over_gb"]:
            res = purge(fp, policy["dry_run"], policy["progressive_hash"])
            report["purged"].append(res)

    report["finished_at"] = datetime.now().isoformat()
    with open(REPORT, "w", encoding="utf-8") as f: json.dump(report, f, indent=2, ensure_ascii=False)

    print(f"📄 Relatório salvo: {REPORT}")
    print(f"✅ Mantidos: {len(report['kept'])} | Arquivados: {len(report['archived'])} | Purgados: {len(report['purged'])}")
    if policy["dry_run"]: print("⚙️ DRY-RUN: Nenhuma exclusão efetiva.")

if __name__ == "__main__":
    main()
subprocess.run(["python", "scripts/post_purge_validator.py"], check=False)

