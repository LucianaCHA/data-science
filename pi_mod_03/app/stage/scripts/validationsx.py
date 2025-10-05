import pandas as pd
import json
from datetime import datetime
from sqlalchemy import create_engine
import yaml


def run_validation(engine):
    df = pd.read_sql("SELECT * FROM airbnb_raw", engine)
    report = {
        "timestamp": datetime.utcnow().isoformat(),
        "row_count": len(df),
        "nulls": df.isnull().sum().to_dict(),
        "dtypes": df.dtypes.astype(str).to_dict(),
    }

    if "id" in df.columns:
        report["duplicate_ids"] = int(df.duplicated(subset=["id"]).sum())

    return report


def main():
    with open("/app/config.yaml") as f:
        config = yaml.safe_load(f)

    engine = create_engine(config["postgres"]["url"])
    report = run_validation(engine)

    report_path = "/app/report.json"
    with open(report_path, "w") as f:
        json.dump(report, f, indent=4)

    print(" Reporte ¡:", report_path)


if __name__ == "__main__":
    main()
