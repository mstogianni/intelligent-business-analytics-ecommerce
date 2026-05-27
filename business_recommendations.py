import pandas as pd

def get_abc_analysis(df, group_col="Sub-Category"):
    abc = (
        df.groupby(group_col)
        .agg({"Sales":"sum","Order ID":"nunique"})
        .sort_values(by="Sales", ascending=False)
        .copy()
    )
    abc["SalesShare"] = abc["Sales"] / abc["Sales"].sum()
    abc["CumulativeShare"] = abc["SalesShare"].cumsum()
    abc["ABC_Class"] = abc["CumulativeShare"].apply(lambda x: "A" if x <= 0.80 else ("B" if x <= 0.95 else "C"))
    return abc

def get_top_priority_items(abc_analysis, top_n=10):
    priority_items = abc_analysis[abc_analysis["ABC_Class"] == "A"].head(top_n).copy()
    return priority_items

def generate_sales_optimization_recommendations(kpis, top_categories, top_subcategories, sales_by_region, sales_by_segment, monthly_summary, forecast_df, abc_products, abc_subcategories):
    recommendations = []
    total_sales = kpis["total_sales"]
    avg_ship_delay = kpis["average_ship_delay_days"]
    top_category = top_categories.index[0]
    top_category_sales = top_categories.iloc[0]["Sales"]
    top_category_share = top_category_sales / total_sales
    top_subcategory = top_subcategories.index[0]
    top_subcategory_sales = top_subcategories.iloc[0]["Sales"]
    top_region = sales_by_region.index[0]
    low_region = sales_by_region.index[-1]
    top_segment = sales_by_segment.index[0]
    low_segment = sales_by_segment.index[-1]
    recent_3m_avg = monthly_summary["Sales"].tail(3).mean()
    forecast_3m_avg = forecast_df["PredictedSales"].mean()
    seasonality = monthly_summary.copy()
    seasonality["MonthNum"] = seasonality.index.month
    month_avg = seasonality.groupby("MonthNum")["Sales"].mean().sort_values(ascending=False)
    best_month = month_avg.index[0]
    worst_month = month_avg.index[-1]
    top_a_products = abc_products[abc_products["ABC_Class"] == "A"].head(5).index.tolist()
    top_a_subcategories = abc_subcategories[abc_subcategories["ABC_Class"] == "A"].head(5).index.tolist()

    recommendations.append({
        "Area":"Category Strategy",
        "Priority":"High",
        "Insight":f"The category {top_category} contributes {top_category_share:.1%} of total sales.",
        "Recommendation":f"Maintain high commercial priority for the {top_category} category by strengthening visibility, availability, and promotional activity."
    })
    recommendations.append({
        "Area":"Sub-Category Strategy",
        "Priority":"High",
        "Insight":f"The sub-category {top_subcategory} has the highest sales ({top_subcategory_sales:,.2f}).",
        "Recommendation":f"Increase stock priority and commercial visibility for the {top_subcategory} sub-category."
    })
    recommendations.append({
        "Area":"Regional Strategy",
        "Priority":"Medium",
        "Insight":f"The {top_region} region is the strongest, while the {low_region} region has the lowest sales.",
        "Recommendation":f"Maintain strong market focus in {top_region} and apply targeted growth actions in {low_region}."
    })
    recommendations.append({
        "Area":"Customer Segment Strategy",
        "Priority":"Medium",
        "Insight":f"The {top_segment} segment is the most profitable in sales contribution, while {low_segment} contributes less.",
        "Recommendation":f"Focus tailored commercial offers on {top_segment} and test activation strategies for {low_segment}."
    })
    recommendations.append({
        "Area":"Inventory Prioritization",
        "Priority":"High",
        "Insight":f"A-class products are the most critical for sales performance. Indicative examples: {', '.join(top_a_products)}.",
        "Recommendation":"Prioritize availability, stock monitoring, and faster replenishment for A-class products."
    })
    recommendations.append({
        "Area":"Portfolio Focus",
        "Priority":"Medium",
        "Insight":f"The A-class sub-categories are: {', '.join(top_a_subcategories)}.",
        "Recommendation":"Direct the largest share of commercial effort and stock planning toward A-class sub-categories."
    })
    recommendations.append({
        "Area":"Seasonality Planning",
        "Priority":"High",
        "Insight":f"The strongest seasonal month is {best_month}, while the weakest is {worst_month}.",
        "Recommendation":"Increase stock preparation and campaign intensity before strong months, and avoid excessive stock commitments during weaker periods."
    })

    if forecast_3m_avg > recent_3m_avg:
        recommendations.append({
            "Area":"Forecast Action",
            "Priority":"High",
            "Insight":f"The average forecast for the next 3 months ({forecast_3m_avg:,.2f}) is higher than the recent 3-month average ({recent_3m_avg:,.2f}).",
            "Recommendation":"Prepare for higher demand by increasing availability of priority products and strengthening inventory planning in advance."
        })
    else:
        recommendations.append({
            "Area":"Forecast Action",
            "Priority":"Medium",
            "Insight":f"The average forecast for the next 3 months ({forecast_3m_avg:,.2f}) is lower than or close to the recent 3-month average ({recent_3m_avg:,.2f}).",
            "Recommendation":"Maintain more conservative stock planning and reinforce promotional actions to sustain demand."
        })

    if avg_ship_delay >= 4:
        recommendations.append({
            "Area":"Operational Efficiency",
            "Priority":"Medium",
            "Insight":f"The average shipping delay is {avg_ship_delay:.2f} days.",
            "Recommendation":"Review logistics processes and shipment speed in order to improve customer experience and operational efficiency."
        })
    else:
        recommendations.append({
            "Area":"Operational Efficiency",
            "Priority":"Low",
            "Insight":f"The average shipping delay is {avg_ship_delay:.2f} days and remains at an acceptable level.",
            "Recommendation":"Maintain the current operational performance and continue monitoring for any future deterioration."
        })

    return pd.DataFrame(recommendations)

def print_recommendations(recommendations_df):
    print("\nSales Optimization Recommendations:")
    print(recommendations_df.to_string(index=False))