import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image

# ✅ Set Page Config FIRST
st.set_page_config(page_title="Delivery Time Prediction App", page_icon=":truck:", layout="wide")

# ✅ Custom CSS for Styling
st.markdown(
    """
    <style>
    /* Set text color to black */
    .stApp, .stMarkdown, h1, h2, h3, h4, h5, h6, p, label {
        color: #000000 !important;
    }

    /* Change cursor to pointer (hand) for selectbox fields (Dropdown Menus) */
    div[data-baseweb="select"] div[role="option"],
    div[data-baseweb="select"] > div {
        cursor: pointer !important;
    }

    /* Set the background color of the main app to white */
    .stApp {
        background-color: white;
    }

    /* Set the sidebar background to light grey */
    section[data-testid="stSidebar"] {
        background-color: #f0f0f0;
    }

    /* Style for the Predict Button */
    div.stButton > button {
        background-color: #007BFF !important; /* Blue background */
        color: white !important; /* White text */
        font-size: 18px !important;
        padding: 12px 20px !important;
        border-radius: 10px !important;
        border: none !important;
        width: 100% !important; /* Make button full-width */
    }

    /* Button Hover Effect */
    div.stButton > button:hover {
        background-color: #0056b3 !important; /* Darker blue on hover */
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ✅ Display Title & Captions with Black Text
st.title("Delivery Time Prediction App")
st.caption(
    "This app predicts the delivery time for orders based on various factors such as product details, customer location, shipping method, and more."
)
st.caption("By analyzing historical data, it helps businesses optimize their supply chain efficiency.")

# ✅ Sidebar with Light Grey Background
with st.sidebar:
    img = Image.open("./assets/supply_chain_optimisation.jpg")  
    st.image(img)
    st.header("Input Parameters")

    # ✅ Primary Inputs
    st.markdown("### Primary Parameters")
    product_category = st.selectbox("Product Category", ["Electronics", "Clothing", "Home & Kitchen", "Books", "Other"])
    customer_location = st.selectbox("Customer Location", ["Urban", "Suburban", "Rural"])
    shipping_method = st.selectbox("Shipping Method", ["Standard", "Express", "Same-Day"])
    shipping_priority = st.selectbox("Shipping Priority", ["Normal", "High", "Urgent"])
    weather = st.selectbox("Weather Conditions", ["Sunny", "Rainy", "Snowy", "Stormy"])

    # ✅ Additional Inputs
    st.markdown("### Additional Parameters")
    package_weight = st.number_input("Package Weight (kg)", min_value=0.1, max_value=100.0, step=0.1, value=5.0)
    package_size = st.selectbox("Package Size", ["Small", "Medium", "Large"])
    distance = st.number_input("Distance to Destination (km)", min_value=1, max_value=5000, step=1, value=100)
    warehouse_proximity = st.radio("Warehouse Proximity", ["Yes", "No"])
    delivery_type = st.selectbox("Delivery Type", ["Residential", "Business"])

    # ✅ Predict Button with Proper Visibility
    submit = st.button("Predict Delivery Time")

# ✅ Prediction Function
def predict_delivery_time():
    base_time = {"Standard": 3, "Express": 2, "Same-Day": 1}[shipping_method]
    if customer_location == "Rural":
        base_time += 2
    elif customer_location == "Suburban":
        base_time += 1
    if weather in ["Rainy", "Snowy", "Stormy"]:
        base_time += 1
    if package_weight > 10:
        base_time += 1
    if package_size == "Large":
        base_time += 1
    elif package_size == "Medium":
        base_time += 0.5
    if distance > 1000:
        base_time += 2
    elif distance > 500:
        base_time += 1
    if warehouse_proximity == "Yes":
        base_time -= 1
    if delivery_type == "Business":
        base_time -= 1
    if shipping_priority == "Urgent":
        base_time = min(base_time, 2)
    return max(1, base_time)

# ✅ Display Output Only After Clicking Button
if submit:
    st.header("Output: Predicted Delivery Time")
    with st.spinner("Predicting delivery time..."):
        delivery_time = predict_delivery_time()
        st.success(f"Estimated Delivery Time: **{delivery_time:.2f} days**")

    # Display Input Data
    st.markdown("### Input Data")
    input_data = {
        "Product Category": product_category,
        "Customer Location": customer_location,
        "Shipping Method": shipping_method,
        "Shipping Priority": shipping_priority,
        "Weather Conditions": weather,
        "Package Weight (kg)": package_weight,
        "Package Size": package_size,
        "Distance (km)": distance,
        "Warehouse Proximity": warehouse_proximity,
        "Delivery Type": delivery_type,
    }
    st.table(pd.DataFrame(list(input_data.items()), columns=["Parameter", "Value"]))

    # ✅ Breakdown of Adjustments (Bar Chart using Seaborn)
    st.markdown("### Delivery Time Breakdown")
    breakdown = {
        "Base Time": {"Standard": 3, "Express": 2, "Same-Day": 1}[shipping_method],
        "Location Adjustment": 2 if customer_location == "Rural" else 1 if customer_location == "Suburban" else 0,
        "Weather Adjustment": 1 if weather in ["Rainy", "Snowy", "Stormy"] else 0,
        "Weight Adjustment": 1 if package_weight > 10 else 0,
        "Size Adjustment": 1 if package_size == "Large" else 0.5 if package_size == "Medium" else 0,
        "Distance Adjustment": 2 if distance > 1000 else 1 if distance > 500 else 0,
        "Warehouse Adjustment": -1 if warehouse_proximity == "Yes" else 0,
        "Delivery Type Adjustment": -1 if delivery_type == "Business" else 0,
    }
    breakdown_df = pd.DataFrame(list(breakdown.items()), columns=["Factor", "Adjustment (Days)"])

    # Bar Chart using Seaborn
    st.markdown("#### Adjustments to Base Delivery Time")
    plt.figure(figsize=(10, 6))
    sns.barplot(x="Factor", y="Adjustment (Days)", data=breakdown_df, palette="viridis")
    plt.xticks(rotation=45)
    plt.title("Adjustments to Base Delivery Time")
    st.pyplot(plt)

# ✅ Sample Dataset Section
st.header("Sample Dataset")
data = {
    "Product Category": ["Electronics", "Clothing", "Home & Kitchen"],
    "Customer Location": ["Urban", "Suburban", "Rural"],
    "Shipping Method": ["Standard", "Express", "Same-Day"],
    "Shipping Priority": ["Normal", "High", "Urgent"],
    "Weather Conditions": ["Sunny", "Rainy", "Snowy"],
    "Package Weight (kg)": [5.0, 12.0, 8.0],
    "Package Size": ["Small", "Large", "Medium"],
    "Distance (km)": [100, 1200, 500],
    "Warehouse Proximity": ["Yes", "No", "Yes"],
    "Delivery Type": ["Residential", "Business", "Residential"],
}
st.write(pd.DataFrame(data))