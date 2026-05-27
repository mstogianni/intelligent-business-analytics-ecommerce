import pandas as pd
import streamlit as st
from pipeline import run_business_analytics

st.set_page_config(page_title="Business Analytics System", layout="wide")

def build_template_df():
    return pd.DataFrame(columns=[
        "Order ID",
        "Order Date",
        "Ship Date",
        "Customer ID",
        "Segment",
        "Country",
        "Region",
        "Category",
        "Sub-Category",
        "Product Name",
        "Sales"
    ])

def to_csv_download(df):
    return df.to_csv(index=False).encode("utf-8")

def prepare_uploaded_dataframe(user_df, mapping):
    df = user_df.copy()
    rename_dict = {}
    for standard_col, user_col in mapping.items():
        if user_col is not None and user_col != "":
            rename_dict[user_col] = standard_col
    df = df.rename(columns=rename_dict)

    if "Order Date" not in df.columns:
        raise ValueError("Order Date / Transaction Date mapping is required.")
    if "Sales" not in df.columns:
        raise ValueError("Sales / Revenue mapping is required.")

    if "Order ID" not in df.columns:
        df["Order ID"] = [f"ORD_{i+1}" for i in range(len(df))]
    if "Ship Date" not in df.columns:
        df["Ship Date"] = df["Order Date"]
    if "Customer ID" not in df.columns:
        df["Customer ID"] = "Unknown"
    if "Segment" not in df.columns:
        df["Segment"] = "Unknown"
    if "Country" not in df.columns:
        df["Country"] = "Unknown"
    if "Region" not in df.columns:
        df["Region"] = "Unknown"
    if "Category" not in df.columns:
        df["Category"] = "Unknown"
    if "Sub-Category" not in df.columns:
        df["Sub-Category"] = "Unknown"
    if "Product Name" not in df.columns:
        df["Product Name"] = "Unknown"

    final_cols = ["Order ID","Order Date","Ship Date","Customer ID","Segment","Country","Region","Category","Sub-Category","Product Name","Sales"]
    df = df[final_cols].copy()
    return df

st.title("Business Analytics and Forecasting System")
st.write("Upload your business CSV file, map the required columns, and run analytics, forecasting, and sales optimization insights.")

template_df = build_template_df()
st.download_button(
    label="Download CSV Template",
    data=to_csv_download(template_df),
    file_name="business_template.csv",
    mime="text/csv"
)

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    user_df = pd.read_csv(uploaded_file, encoding="latin1")
    st.subheader("Uploaded Data Preview")
    st.dataframe(user_df.head(), use_container_width=True)

    st.subheader("Column Mapping")
    columns = list(user_df.columns)
    optional_columns = [""] + columns

    col1, col2 = st.columns(2)

    with col1:
        order_date_col = st.selectbox("Order Date / Transaction Date", columns)
        sales_choices = [c for c in columns if c != order_date_col] if len(columns) > 1 else columns
        sales_col = st.selectbox("Sales / Revenue", sales_choices)
        order_id_col = st.selectbox("Order ID / Transaction ID (optional)", optional_columns)
        ship_date_col = st.selectbox("Ship Date / Delivery Date (optional)", optional_columns)
        customer_id_col = st.selectbox("Customer ID (optional)", optional_columns)

    with col2:
        segment_col = st.selectbox("Customer Segment (optional)", optional_columns)
        country_col = st.selectbox("Country (optional)", optional_columns)
        region_col = st.selectbox("Sales Region / Market Region (optional)", optional_columns)
        category_col = st.selectbox("Product Category (optional)", optional_columns)
        subcategory_col = st.selectbox("Product Sub-Category (optional)", optional_columns)
        product_name_col = st.selectbox("Product / Item Name (optional)", optional_columns)

    mapping = {
        "Order Date": order_date_col,
        "Sales": sales_col,
        "Order ID": order_id_col if order_id_col != "" else None,
        "Ship Date": ship_date_col if ship_date_col != "" else None,
        "Customer ID": customer_id_col if customer_id_col != "" else None,
        "Segment": segment_col if segment_col != "" else None,
        "Country": country_col if country_col != "" else None,
        "Region": region_col if region_col != "" else None,
        "Category": category_col if category_col != "" else None,
        "Sub-Category": subcategory_col if subcategory_col != "" else None,
        "Product Name": product_name_col if product_name_col != "" else None
    }

    if st.button("Run Analysis"):
        try:
            prepared_df = prepare_uploaded_dataframe(user_df, mapping)
            results = run_business_analytics(prepared_df)

            st.success("Analysis completed successfully.")

            st.subheader("Prepared Data Preview")
            st.dataframe(prepared_df.head(), use_container_width=True)

            st.subheader("Business KPIs")
            kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
            kpi1.metric("Total Sales", f"{results['kpis']['total_sales']:,.2f}")
            kpi2.metric("Total Orders", f"{results['kpis']['total_orders']:,}")
            kpi3.metric("Total Customers", f"{results['kpis']['total_customers']:,}")
            kpi4.metric("Average Order Value", f"{results['kpis']['average_order_value']:,.2f}")
            kpi5.metric("Avg Ship Delay", f"{results['kpis']['average_ship_delay_days']:.2f}")

            st.subheader("Monthly Forecast Metrics")
            m1, m2, m3 = st.columns(3)
            m1.metric("MAE", f"{results['mae']:,.2f}")
            m2.metric("RMSE", f"{results['rmse']:,.2f}")
            m3.metric("R²", f"{results['r2']:.4f}")

            st.subheader("Monthly Sales Trend")
            st.line_chart(results["monthly_summary"][["Sales"]], use_container_width=True)

            st.subheader("Actual vs Predicted Monthly Sales")
            comparison_df = pd.DataFrame({
                "Actual Sales": results["test"].values,
                "Predicted Sales": results["y_pred"].values
            }, index=results["test"].index)
            st.line_chart(comparison_df, use_container_width=True)

            st.subheader("Next 3 Months Forecast")
            st.dataframe(results["forecast_df"], use_container_width=True)

            forecast_chart = pd.concat([
                results["monthly_summary"][["Sales"]].tail(12).rename(columns={"Sales":"Historical Sales"}),
                results["forecast_df"].rename(columns={"PredictedSales":"Next 3 Months Forecast"})
            ], axis=0)
            st.line_chart(forecast_chart, use_container_width=True)

            st.subheader("Top Categories by Sales")
            st.bar_chart(results["top_categories"][["Sales"]], use_container_width=True)
            st.dataframe(results["top_categories"], use_container_width=True)

            st.subheader("Top Sub-Categories by Sales")
            st.bar_chart(results["top_subcategories"][["Sales"]], use_container_width=True)
            st.dataframe(results["top_subcategories"], use_container_width=True)

            st.subheader("Top Products by Sales")
            st.bar_chart(results["top_products"][["Sales"]], use_container_width=True)
            st.dataframe(results["top_products"], use_container_width=True)

            st.subheader("Sales by Region")
            st.bar_chart(results["sales_by_region"][["Sales"]], use_container_width=True)
            st.dataframe(results["sales_by_region"], use_container_width=True)

            st.subheader("Sales by Segment")
            st.bar_chart(results["sales_by_segment"][["Sales"]], use_container_width=True)
            st.dataframe(results["sales_by_segment"], use_container_width=True)

            if results["sales_by_country"] is not None:
                st.subheader("Sales by Country")
                st.bar_chart(results["sales_by_country"][["Sales"]], use_container_width=True)
                st.dataframe(results["sales_by_country"], use_container_width=True)

            st.subheader("ABC Analysis - Products")
            st.bar_chart(results["abc_products"].head(10)[["Sales"]], use_container_width=True)
            st.dataframe(results["abc_products"].head(10), use_container_width=True)

            st.subheader("ABC Analysis - Sub-Categories")
            st.bar_chart(results["abc_subcategories"].head(10)[["Sales"]], use_container_width=True)
            st.dataframe(results["abc_subcategories"].head(10), use_container_width=True)

            st.subheader("Top Priority Products")
            st.dataframe(results["priority_products"], use_container_width=True)

            st.subheader("Top Priority Sub-Categories")
            st.dataframe(results["priority_subcategories"], use_container_width=True)

            st.subheader("Sales Optimization Recommendations")

            for i, row in results["recommendations_df"].iterrows():
                with st.expander(f"{row['Area']} | Priority: {row['Priority']}", expanded=False):
                    st.markdown(f"**Insight:** {row['Insight']}")
                    st.markdown(f"**Recommendation:** {row['Recommendation']}")

        except Exception as e:
            st.error(f"Error: {e}")