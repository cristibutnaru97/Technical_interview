import pandas as pd
import argparse
import json


def load_data(csv_path: str) -> pd.DataFrame:
    """
    Load the CSV file and handle missing or invalid data interactively.
    
    - Nu șterge rândurile cu date lipsă.
    - Afișează rândurile incomplete.
    - Permite completarea manuală sau ștergerea lor.
    """
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        raise SystemExit(f"Error: File not found at path '{csv_path}'.")

    for col in ["year", "revenue", "profit"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    
    incomplete_rows = df[df[["company", "year", "revenue", "profit"]].isnull().any(axis=1)]
    if not incomplete_rows.empty:
        print("\n⚠️ Next rows have missing data:\n")
        print(incomplete_rows)
        
        choice = input("\nDo you want to manually fill in these lines?? (y/n) ")
        if choice.lower() == 'y':
            for idx in incomplete_rows.index:
                for col in ["company", "year", "revenue", "profit"]:
                    if pd.isna(df.at[idx, col]):
                        value = input(f"Enter the value for {col} at row {idx}: ")
                        if col in ["year", "revenue", "profit"]:
                            try:
                                value = float(value)
                                if col == "year":
                                    value = int(value)
                            except ValueError:
                                print("Invalid data, stay NaN")
                                value = pd.NA
                        df.at[idx, col] = value
        else:
            df = df.drop(incomplete_rows.index)
            print("Incomplete rows will remain in the DataFrame and can be removed later if you want..")
    
    return df


def compute_summary(df: pd.DataFrame, min_revenue: float = 0) -> list[dict]:
    """
    Compute summary per company:
      - Average yearly profit
      - YoY revenue growth (latest vs previous)
      - Profit margin for latest year
    Filter companies by min_revenue if provided.
    """
    summaries = []

    for company, group in df.groupby("company"):
        group = group.sort_values("year")

        # Skip companies that don't meet the min revenue requirement
        if group["revenue"].max() < min_revenue:
            continue

        avg_profit = group["profit"].mean()

        if len(group) >= 2:
            latest = group.iloc[-1]
            prev = group.iloc[-2]
            yoy_growth = ((latest["revenue"] - prev["revenue"]) / prev["revenue"]) * 100
        else:
            yoy_growth = None

        latest = group.iloc[-1]
        profit_margin = (latest["profit"] / latest["revenue"]) * 100

        summaries.append({
            "company": company,
            "avg_profit": round(avg_profit, 2),
            "yoy_growth_%": round(yoy_growth, 2) if yoy_growth is not None else "N/A",
            "profit_margin_%": round(profit_margin, 2)
        })

    return summaries


def main():
    parser = argparse.ArgumentParser(description="Generate financial summary from CSV.")
    parser.add_argument("csv_path", help="Path to the input CSV file.")
    parser.add_argument(
        "--min-revenue",
        type=float,
        default=0,
        help="Filter companies by minimum revenue (default: 0)."
    )
    parser.add_argument(
        "--output-json",
        action="store_true",
        help="Output results as JSON instead of text table."
    )
    args = parser.parse_args()

    df = load_data(args.csv_path)
    print (df)
    results = compute_summary(df, min_revenue=args.min_revenue)

    if args.output_json:
        print(json.dumps(results, indent=2))
    else:
        print(f"{'Company':<20} {'Avg Profit':>12} {'YoY Growth %':>12} {'Margin %':>10}")
        print("-" * 60)
        for r in results:
            print(
                f"{r['company']:<20} "
                f"{r['avg_profit']:>12,.2f} "
                f"{r['yoy_growth_%']:>12} "
                f"{r['profit_margin_%']:>10,.2f}"
            )


if __name__ == "__main__":
    main()
