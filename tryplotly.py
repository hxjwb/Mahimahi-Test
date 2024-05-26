import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# 生成示例数据
df = px.data.tips()

# 创建Dash app
app = dash.Dash(__name__)

# 参数设置
app.layout = html.Div([
    dcc.Graph(id='scatter-plot'),
    dcc.Slider(
        id='slider-tip',
        min=df['total_bill'].min(),
        max=df['total_bill'].max(),
        value=df['total_bill'].mean(),
        marks={str(i): str(i) for i in range(int(df['total_bill'].min()), int(df['total_bill'].max()) + 1, 5)},
        step=1
    )
])


# 定义回调更新散点图
@app.callback(
    Output('scatter-plot', 'figure'),
    [Input('slider-tip', 'value')]
)
def update_scatter_plot(selected_tip):
    filtered_df = df[df['total_bill'] <= selected_tip]
    fig = px.scatter(filtered_df, x='total_bill', y='tip', title='Scatter Plot with Dynamic Filter')
    return fig


# 运行
if __name__ == '__main__':
    app.run_server(debug=True)