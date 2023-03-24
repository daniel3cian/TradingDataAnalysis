import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Comtrade HS Code 731815 Data Visualization 2017~2021",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="auto",
)

# 添加样式
st.markdown(
    f"""
    <style>
    .reportview-container {{
        background: linear-gradient(to right, #f12711, #f5af19);
        color: #fff;
    }}
    .sidebar .sidebar-content {{
        background: linear-gradient(to bottom, #f12711, #f5af19);
        color: #fff;
    }}
    h1 {{
        color: #f5af19;
    }}
    </style>
    """,
    unsafe_allow_html=True
)



# 读取csv文件
import os

file_path = os.path.join(os.path.expanduser("~"), "PycharmProjects", "FastenerGlobalTradingDataAnalysis", "comtrade.csv")
df = pd.read_csv(file_path)


# 重塑数据框
id_vars = ['Year', 'Partner', 'Commodity Code', 'Commodity']
value_vars = ['Netweight (kg)', 'Trade Value (US$)', 'Price per Ton(US$)']
df = df.melt(id_vars=id_vars, value_vars=value_vars, var_name='Metric', value_name='Value')

# 将年份转换为一列
df['Year'] = pd.to_datetime(df['Year'], format='%Y')

# 将Value列的数据类型转换为float
df['Value'] = df['Value'].astype(float)

# 将数据按照国家、Metric和Year排序
df = df.sort_values(['Partner', 'Metric', 'Year']).reset_index(drop=True)

# 获取所有的国家列表
countries = df['Partner'].unique().tolist()

# Streamlit应用程序
st.markdown(
    """
    <head>
        <style>
            .reportview-container {
                background: linear-gradient(#00B4DB, #0083B0);
            }
            .title {
                font-size: 48px;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                text-align: center;
                color: #008080;
                text-shadow: 2px 2px 5px #0083B0;
            }
        </style>
    </head>
    <h1 class="title">Comtrade HS Code 731815 Data Visualization 2017~2021</h1>
    """,
    unsafe_allow_html=True,
)




# 多选框来选择国家
selected_countries = st.multiselect("选择国家",
                                    countries,
                                    ['USA', "Viet Nam", "Germany", "Japan", "Russian Federation", "Malaysia", "Kazakhstan", "South Africa", "Pakistan", "Turkey", "Indonesia", "Philippines",
"Italy", "Iraq", "Egypt", "Iran", "Chile", "Peru", "United Kingdom", "India", "Poland", "Canada", "Thailand", "Mexico",
                                     "Argentina", "Azerbaijan", "Saudi Arabia", "Australia", "New Zealand", "United Arab Emirates"] )


# 根据选定的国家创建筛选后的数据框
filtered_df = df[df['Partner'].isin(selected_countries)]

# 绘制贸易价值图表
trade_value_df = filtered_df[filtered_df['Metric'] == 'Trade Value (US$)']
fig1 = px.line(trade_value_df, x="Year", y="Value", color="Partner", title="Trade Value")
st.plotly_chart(fig1, use_container_width=True)

# 绘制净重量图表
netweight_df = filtered_df[filtered_df['Metric'] == 'Netweight (kg)']
fig2 = px.line(netweight_df, x="Year", y="Value", color="Partner", title="Net Weight")
st.plotly_chart(fig2, use_container_width=True)

# 绘制每吨价格图表
price_df = filtered_df[filtered_df['Metric'] == 'Price per Ton(US$)']
fig3 = px.line(price_df, x="Year", y="Value", color="Partner", title="Price per Ton")
st.plotly_chart(fig3, use_container_width=True)

# 汇总每个国家的贸易价值
summary_df = df[df['Metric'] == 'Trade Value (US$)'].groupby('Partner').sum().sort_values('Value', ascending=False)

