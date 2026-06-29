from data_utils import clean_data
from analytics import get_kpis, get_top_categories_by_sales, get_top_subcategories_by_sales, get_top_products_by_sales, get_sales_by_region, get_sales_by_segment, get_sales_by_country, get_monthly_sales_summary
from forecasting import evaluate_monthly_forecast, forecast_next_3_months
from business_recommendations import get_abc_analysis, get_top_priority_items, generate_sales_optimization_recommendations

def run_business_analytics(df):
    df = clean_data(df)
    results = {}
    results["df"] = df
    results["basic_stats"] = df[["Sales","Ship Delay"]].describe()
    results["kpis"] = get_kpis(df)
    results["top_categories"] = get_top_categories_by_sales(df)
    results["top_subcategories"] = get_top_subcategories_by_sales(df)
    results["top_products"] = get_top_products_by_sales(df)
    results["sales_by_region"] = get_sales_by_region(df)
    results["sales_by_segment"] = get_sales_by_segment(df)

    if "Country" in df.columns and df["Country"].nunique() > 1 and not df["Country"].eq("Unknown").all():
        results["sales_by_country"] = get_sales_by_country(df)
    else:
        results["sales_by_country"] = None

    results["monthly_summary"] = get_monthly_sales_summary(df)
    train, test, y_pred, mae, rmse, r2 = evaluate_monthly_forecast(results["monthly_summary"], test_periods=6)
    results["train"] = train
    results["test"] = test
    results["y_pred"] = y_pred
    results["mae"] = mae
    results["rmse"] = rmse
    results["r2"] = r2
    results["forecast_df"] = forecast_next_3_months(results["monthly_summary"])
    results["abc_products"] = get_abc_analysis(df, group_col="Product Name")
    results["abc_subcategories"] = get_abc_analysis(df, group_col="Sub-Category")
    results["priority_products"] = get_top_priority_items(results["abc_products"], top_n=10)
    results["priority_subcategories"] = get_top_priority_items(results["abc_subcategories"], top_n=10)
    results["recommendations_df"] = generate_sales_optimization_recommendations(
        results["kpis"],
        results["top_categories"],
        results["top_subcategories"],
        results["sales_by_region"],
        results["sales_by_segment"],
        results["monthly_summary"],
        results["forecast_df"],
        results["abc_products"],
        results["abc_subcategories"]
    )
    return results