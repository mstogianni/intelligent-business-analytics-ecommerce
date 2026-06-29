import matplotlib.pyplot as plt

def plot_monthly_sales(monthly_summary):
    plt.figure(figsize=(10,5))
    plt.plot(monthly_summary.index, monthly_summary["Sales"], marker="o")
    plt.title("Monthly Sales Trend")
    plt.xlabel("Month")
    plt.ylabel("Sales")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def plot_top_categories_by_sales(top_categories):
    top_categories = top_categories.sort_values(by="Sales", ascending=True)
    plt.figure(figsize=(8,5))
    plt.barh(top_categories.index, top_categories["Sales"])
    plt.title("Top Categories by Sales")
    plt.xlabel("Sales")
    plt.ylabel("Category")
    plt.tight_layout()
    plt.show()

def plot_top_subcategories_by_sales(top_subcategories):
    top_subcategories = top_subcategories.sort_values(by="Sales", ascending=True)
    plt.figure(figsize=(10,6))
    plt.barh(top_subcategories.index, top_subcategories["Sales"])
    plt.title("Top Sub-Categories by Sales")
    plt.xlabel("Sales")
    plt.ylabel("Sub-Category")
    plt.tight_layout()
    plt.show()

def plot_top_products_by_sales(top_products):
    top_products = top_products.sort_values(by="Sales", ascending=True)
    plt.figure(figsize=(10,6))
    plt.barh(top_products.index, top_products["Sales"])
    plt.title("Top Products by Sales")
    plt.xlabel("Sales")
    plt.ylabel("Product")
    plt.tight_layout()
    plt.show()

def plot_sales_by_region(sales_by_region):
    plt.figure(figsize=(8,5))
    plt.bar(sales_by_region.index, sales_by_region["Sales"])
    plt.title("Sales by Region")
    plt.xlabel("Region")
    plt.ylabel("Sales")
    plt.tight_layout()
    plt.show()

def plot_sales_by_segment(sales_by_segment):
    plt.figure(figsize=(8,5))
    plt.bar(sales_by_segment.index, sales_by_segment["Sales"])
    plt.title("Sales by Segment")
    plt.xlabel("Segment")
    plt.ylabel("Sales")
    plt.tight_layout()
    plt.show()

def plot_actual_vs_predicted(test, y_pred):
    plt.figure(figsize=(10,5))
    plt.plot(test.index, test.values, marker="o", label="Actual Sales")
    plt.plot(test.index, y_pred.values, marker="o", label="Predicted Sales")
    plt.title("Actual vs Predicted Monthly Sales")
    plt.xlabel("Month")
    plt.ylabel("Sales")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.show()

def plot_next_3_months_forecast(monthly_summary, forecast_df):
    recent_history = monthly_summary.tail(12)
    plt.figure(figsize=(10,5))
    plt.plot(recent_history.index, recent_history["Sales"], marker="o", label="Historical Sales")
    plt.plot(forecast_df.index, forecast_df["PredictedSales"], marker="o", label="Next 3 Months Forecast")
    plt.title("Next 3 Months Sales Forecast")
    plt.xlabel("Month")
    plt.ylabel("Sales")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.show()
    
def plot_abc_subcategories(abc_subcategories):
    plot_df = abc_subcategories.head(10).sort_values(by="Sales", ascending=True)
    plt.figure(figsize=(10,6))
    plt.barh(plot_df.index, plot_df["Sales"])
    plt.title("Top ABC Sub-Categories by Sales")
    plt.xlabel("Sales")
    plt.ylabel("Sub-Category")
    plt.tight_layout()
    plt.show()