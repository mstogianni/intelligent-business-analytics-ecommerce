def get_kpis(df):
    total_sales = df["Sales"].sum()
    total_orders = df["Order ID"].nunique()
    kpis = {
        "total_sales": total_sales,
        "total_orders": total_orders,
        "total_customers": df["Customer ID"].nunique(),
        "average_order_value": total_sales / total_orders,
        "average_ship_delay_days": df["Ship Delay"].mean()
    }
    return kpis

def get_top_categories_by_sales(df, top_n=10):
    top_categories = (
        df.groupby("Category")
        .agg({"Sales":"sum","Order ID":"nunique"})
        .sort_values(by="Sales", ascending=False)
        .head(top_n)
    )
    return top_categories

def get_top_subcategories_by_sales(df, top_n=10):
    top_subcategories = (
        df.groupby("Sub-Category")
        .agg({"Sales":"sum","Order ID":"nunique"})
        .sort_values(by="Sales", ascending=False)
        .head(top_n)
    )
    return top_subcategories

def get_top_products_by_sales(df, top_n=10):
    top_products = (
        df.groupby("Product Name")
        .agg({"Sales":"sum","Order ID":"nunique"})
        .sort_values(by="Sales", ascending=False)
        .head(top_n)
    )
    return top_products

def get_sales_by_region(df):
    sales_by_region = (
        df.groupby("Region")
        .agg({"Sales":"sum","Order ID":"nunique"})
        .sort_values(by="Sales", ascending=False)
    )
    return sales_by_region

def get_sales_by_segment(df):
    sales_by_segment = (
        df.groupby("Segment")
        .agg({"Sales":"sum","Order ID":"nunique"})
        .sort_values(by="Sales", ascending=False)
    )
    return sales_by_segment

def get_sales_by_country(df):
    sales_by_country = (
        df.groupby("Country")
        .agg({"Sales":"sum","Order ID":"nunique"})
        .sort_values(by="Sales", ascending=False)
    )
    return sales_by_country

def get_monthly_sales_summary(df):
    monthly_summary = (
        df.groupby("YearMonth")
        .agg({"Sales":"sum","Order ID":"nunique"})
        .sort_index()
    )
    monthly_summary = monthly_summary.asfreq("MS")
    return monthly_summary