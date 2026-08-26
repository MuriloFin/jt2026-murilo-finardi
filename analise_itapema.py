"""Hackathon Seazone 2026 - análise de investimento em Itapema/SC.

Reproduz as principais tabelas usadas na recomendação executiva.

Uso:
    python analise_itapema.py --data-dir /caminho/para/os/csvs

Se --data-dir não for informado, procura os cinco CSVs primeiro em ./data e depois na raiz.
"""
from pathlib import Path
import argparse
import ast
import unicodedata
import numpy as np
import pandas as pd
from scipy.stats import mannwhitneyu
import statsmodels.formula.api as smf

FILES = [
    "Details_Itapema.csv",
    "Hosts_ids_Itapema.csv",
    "Mesh_Ids_Data_Itapema.csv",
    "Price_AV_Itapema.csv",
    "VivaReal_Itapema.csv",
]


def resolve_data_dir(arg: str | None) -> Path:
    candidates = [Path(arg)] if arg else [Path("data"), Path(".")]
    for candidate in candidates:
        if all((candidate / f).exists() for f in FILES):
            return candidate
    raise FileNotFoundError(
        "Não encontrei os 5 CSVs. Use --data-dir CAMINHO ou coloque-os em ./data."
    )


def parse_list(value):
    if pd.isna(value):
        return []
    try:
        result = ast.literal_eval(value)
        return result if isinstance(result, list) else []
    except Exception:
        return []


def normalize_text(value):
    return (
        unicodedata.normalize("NFKD", str(value))
        .encode("ascii", "ignore")
        .decode()
        .lower()
    )


def load_data(data_dir: Path):
    details = pd.read_csv(data_dir / "Details_Itapema.csv")
    hosts = pd.read_csv(data_dir / "Hosts_ids_Itapema.csv")
    mesh = pd.read_csv(data_dir / "Mesh_Ids_Data_Itapema.csv")
    price = pd.read_csv(data_dir / "Price_AV_Itapema.csv")
    viva = pd.read_csv(data_dir / "VivaReal_Itapema.csv")
    return details, hosts, mesh, price, viva


def build_panel(details, hosts, mesh, price):
    price = price.copy()
    price["date"] = pd.to_datetime(price["date"])
    price["aquisition_date"] = pd.to_datetime(price["aquisition_date"])
    price["acq_day"] = price["aquisition_date"].dt.normalize()

    host_unique = (
        hosts.sort_values("host_snapshot_date")
        .drop_duplicates("owner_id", keep="last")
    )

    master = (
        details.merge(
            mesh[["airbnb_listing_id", "suburb"]],
            on="airbnb_listing_id",
            how="left",
        )
        .merge(
            host_unique[[
                "owner_id", "is_superhost", "years_host", "number_of_reviews_host"
            ]],
            on="owner_id",
            how="left",
        )
    )

    d7 = pd.Timestamp("2025-01-07")
    d20 = pd.Timestamp("2025-01-20")
    start = pd.Timestamp("2025-01-20")
    end = pd.Timestamp("2025-04-06")
    n_days = (end - start).days + 1

    ids7 = set(price.loc[price["acq_day"].eq(d7), "airbnb_listing_id"])
    ids20 = set(price.loc[price["acq_day"].eq(d20), "airbnb_listing_id"])
    ids_both = ids7 & ids20

    p7 = price[
        price["acq_day"].eq(d7)
        & price["airbnb_listing_id"].isin(ids_both)
        & price["date"].between(start, end)
    ]
    p20 = price[
        price["acq_day"].eq(d20)
        & price["airbnb_listing_id"].isin(ids_both)
        & price["date"].between(start, end)
    ]

    p7 = p7.groupby(["airbnb_listing_id", "date"], as_index=False)["price"].median()
    p20 = p20.groupby(["airbnb_listing_id", "date"], as_index=False)["price"].median()

    rows = []
    for listing_id in sorted(ids_both):
        a = p7[p7["airbnb_listing_id"].eq(listing_id)]
        b = p20[p20["airbnb_listing_id"].eq(listing_id)]

        available_7 = set(a["date"])
        available_20 = set(b["date"])
        disappeared = available_7 - available_20
        prices_7 = dict(zip(a["date"], a["price"]))

        median_rate = pd.concat([a["price"], b["price"]], ignore_index=True).median()
        unavailable_nights = n_days - len(available_20)

        rows.append({
            "airbnb_listing_id": listing_id,
            "median_rate": median_rate,
            "occupancy_proxy": unavailable_nights / n_days,
            "revenue_proxy_77": unavailable_nights * median_rate,
            "pickup_revenue_13d": sum(float(prices_7[d]) for d in disappeared),
            "pickup_nights_13d": len(disappeared),
        })

    metrics = pd.DataFrame(rows).merge(master, on="airbnb_listing_id", how="left")
    return metrics


def clean_sales(viva):
    sales = (
        viva.sort_values("aquisition_date")
        .drop_duplicates("listing_id", keep="last")
        .copy()
    )
    sales = sales[
        sales["listing_type"].eq("apartamento")
        & sales["usable_area"].between(20, 500)
        & sales["sale_price"].between(100_000, 20_000_000)
    ].copy()
    sales["price_per_sqm"] = sales["sale_price"] / sales["usable_area"]
    return sales


def segment_table(metrics, sales):
    airbnb = (
        metrics[
            metrics["listing_type"].eq("apartamento")
            & metrics["suburb"].isin(["Meia Praia", "Centro", "Morretes"])
            & metrics["number_of_bedrooms"].isin([1, 2, 3])
        ]
        .groupby(["suburb", "number_of_bedrooms"])
        .agg(
            n_airbnb=("airbnb_listing_id", "count"),
            revenue_proxy_77=("revenue_proxy_77", "median"),
            occupancy_proxy=("occupancy_proxy", "median"),
            daily_rate=("median_rate", "median"),
            guests=("number_of_guests", "median"),
        )
        .reset_index()
    )

    market = (
        sales[
            sales["suburb"].isin(["Meia Praia", "Centro", "Morretes"])
            & sales["bedrooms"].isin([1, 2, 3])
        ]
        .groupby(["suburb", "bedrooms"])
        .agg(
            n_sales=("listing_id", "count"),
            purchase_price=("sale_price", "median"),
            area=("usable_area", "median"),
        )
        .reset_index()
    )

    result = airbnb.merge(
        market,
        left_on=["suburb", "number_of_bedrooms"],
        right_on=["suburb", "bedrooms"],
        how="left",
    )
    result["yield_77"] = result["revenue_proxy_77"] / result["purchase_price"]
    result["annualized_run_rate"] = result["yield_77"] * 365 / 77
    result["gross_payback_years"] = 1 / result["annualized_run_rate"]
    return result


def location_table(metrics):
    return (
        metrics.groupby("suburb")
        .agg(
            n=("airbnb_listing_id", "count"),
            revenue_proxy_77=("revenue_proxy_77", "median"),
            occupancy_proxy=("occupancy_proxy", "median"),
            daily_rate=("median_rate", "median"),
        )
        .reset_index()
        .query("n >= 30")
        .sort_values("revenue_proxy_77", ascending=False)
    )


def bootstrap_location(metrics, seed=42, iterations=10_000):
    meia = metrics.loc[metrics["suburb"].eq("Meia Praia"), "revenue_proxy_77"].dropna().values
    centro = metrics.loc[metrics["suburb"].eq("Centro"), "revenue_proxy_77"].dropna().values
    rng = np.random.default_rng(seed)
    diffs = []
    for _ in range(iterations):
        diffs.append(
            np.median(rng.choice(meia, len(meia), replace=True))
            - np.median(rng.choice(centro, len(centro), replace=True))
        )
    return np.percentile(diffs, [2.5, 50, 97.5]), mannwhitneyu(meia, centro)


def driver_models(metrics):
    metrics = metrics.copy()
    metrics["amenity_list"] = metrics["amenities"].apply(parse_list)
    metrics["amenity_text"] = metrics["amenity_list"].apply(
        lambda values: " | ".join(normalize_text(v) for v in values)
    )
    metrics["amenity_count"] = metrics["amenity_list"].str.len()
    metrics["sea_view"] = metrics["amenity_text"].str.contains(
        "vista para o mar|vista do mar|vista pro mar", regex=True
    )
    metrics["beach_access"] = metrics["amenity_text"].str.contains("acesso a praia")
    metrics["pool"] = metrics["amenity_text"].str.contains("piscina")
    metrics["balcony"] = metrics["amenity_text"].str.contains("varanda")

    model_data = metrics[
        metrics["median_rate"].gt(0)
        & metrics["number_of_bedrooms"].between(0, 6)
        & metrics["number_of_guests"].between(1, 16)
        & metrics["number_of_bathrooms"].between(0, 8)
    ].copy()

    controls = (
        "number_of_bedrooms + number_of_guests + number_of_bathrooms + "
        "amenity_count + sea_view + beach_access + pool + balcony + "
        "C(suburb) + C(listing_type)"
    )
    adr = smf.ols("np.log(median_rate) ~ " + controls, model_data).fit(cov_type="HC3")
    occ = smf.ols("occupancy_proxy ~ " + controls, model_data).fit(cov_type="HC3")
    return adr, occ


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", default=None)
    args = parser.parse_args()

    data_dir = resolve_data_dir(args.data_dir)
    out = Path("output/tables")
    out.mkdir(parents=True, exist_ok=True)

    details, hosts, mesh, price, viva = load_data(data_dir)
    metrics = build_panel(details, hosts, mesh, price)
    sales = clean_sales(viva)

    segments = segment_table(metrics, sales)
    locations = location_table(metrics)
    ci, mw = bootstrap_location(metrics)
    adr, occ = driver_models(metrics)

    segments.to_csv(out / "segmentos.csv", index=False)
    locations.to_csv(out / "localizacoes.csv", index=False)

    print(f"Painel comparável: {len(metrics)} imóveis")
    print("\nSegmentos:")
    print(segments.to_string(index=False))
    print("\nLocalizações (n >= 30):")
    print(locations.to_string(index=False))
    print(f"\nBootstrap Meia Praia - Centro (IC95%): {ci}")
    print(f"Mann-Whitney p-value: {mw.pvalue:.6g}")
    print(f"R² ADR: {adr.rsquared:.3f} | R² ocupação: {occ.rsquared:.3f}")


if __name__ == "__main__":
    main()
