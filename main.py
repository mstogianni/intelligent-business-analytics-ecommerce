from data_utils import load_data
from pipeline import run_business_analytics
from business_recommendations import print_recommendations
from visualizations import plot_monthly_sales, plot_top_categories_by_sales, plot_top_subcategories_by_sales, plot_top_products_by_sales, plot_sales_by_region, plot_sales_by_segment, plot_actual_vs_predicted, plot_next_3_months_forecast, plot_abc_subcategories

if __name__ == "__main__":
    df = load_data("train.csv")
    results = run_business_analytics(df)

    print("\nDataset Info:")
    print(results["df"].info())

    print("\nBasic Statistics:")
    print(results["basic_stats"])

    print("\nBusiness KPIs:")
    for key, value in results["kpis"].items():
        print(f"{key}: {value}")

    print("\nTop Categories by Sales:")
    print(results["top_categories"])

    print("\nTop Sub-Categories by Sales:")
    print(results["top_subcategories"])

    print("\nTop Products by Sales:")
    print(results["top_products"])

    print("\nSales by Region:")
    print(results["sales_by_region"])

    print("\nSales by Segment:")
    print(results["sales_by_segment"])

    print("\nMonthly Sales Summary:")
    print(results["monthly_summary"])

    print("\nMonthly Forecast Metrics:")
    print(f"MAE: {results['mae']}")
    print(f"RMSE: {results['rmse']}")
    print(f"R2: {results['r2']}")

    print("\nNext 3 Months Forecast:")
    print(results["forecast_df"])

    print("\nABC Analysis - Products:")
    print(results["abc_products"].head(10))

    print("\nABC Analysis - Sub-Categories:")
    print(results["abc_subcategories"].head(10))

    print("\nTop Priority Products:")
    print(results["priority_products"])

    print("\nTop Priority Sub-Categories:")
    print(results["priority_subcategories"])

    print_recommendations(results["recommendations_df"])

    plot_monthly_sales(results["monthly_summary"])
    plot_top_categories_by_sales(results["top_categories"])
    plot_top_subcategories_by_sales(results["top_subcategories"])
    plot_top_products_by_sales(results["top_products"])
    plot_sales_by_region(results["sales_by_region"])
    plot_sales_by_segment(results["sales_by_segment"])
    plot_actual_vs_predicted(results["test"], results["y_pred"])
    plot_next_3_months_forecast(results["monthly_summary"], results["forecast_df"])
    plot_abc_subcategories(results["abc_subcategories"])
    
