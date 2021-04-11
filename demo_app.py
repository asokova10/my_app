import streamlit as st
import altair as alt
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
with st.echo(code_location='below'):
    def main():
        df = get_data()
        p = st.sidebar.selectbox("Выберите страничку", ["Начало", "Зависимость индекса счастья\nот различных переменных",
                                                           "Зависимость переменных", "Распеределение переменных"])

        if p == "Начало":
            st.markdown("### Онлайн-визуализатор статистики по индексу счастья")
            st.markdown("Выберите страницу слева.")
            st.markdown("Исходный датасет:")
            st.write(df)
        elif p == "Зависимость переменных":
            st.markdown("### Зависимость переменных")
            st.markdown("Здесь вы можете увидеть, как выбранные вами переменные зависят друг от друга.")
            st.markdown("Вы можете настроить фильтр и смотреть зависимость только для интересующих вас стран.")
            st.markdown("Если фильтр не выбран, статистика показывается по всем странам из датасета.")
            countries = st.multiselect("Фильтр по странам",
                                   list(df["Country (region)"]))
            if countries:
                df1 = df.loc[df['Country (region)'].isin(countries)]
            else:
                df1 = df

            x_ax = st.selectbox("Выберите переменную по оси x", df1.columns)
            y_ax = st.selectbox("Выберите переменную по оси y", df1.columns)

            visualize_data(df1, x_ax, y_ax)
        elif p == "Зависимость индекса счастья\nот различных переменных":
            st.markdown("### Зависимость индекса счастья от различных переменных")
            st.markdown("Здесь вы можете посмотреть зависимость индекса счастья и выбранных вами переменных.")
            st.markdown("Если вид графика - 'matplotlib', то здесь вы можете выбрать шкалу: стандартную или логарифмическую.")
            headers = df.dtypes.index
            graph_type = st.radio("Выберите вид графика:", ['altair', 'matplotlib'])
            if graph_type == "matplotlib":
                scale_type = st.radio("Ввыберите вид шкалы: ", ['стандартная', 'логарифмическая'])
                if scale_type == "стандартная":
                    options = st.multiselect("Выберите переменные",
                                      list(headers))
                    visualize_data2(df, options)
                elif scale_type == "логарифмическая":
                    n = list(headers)[2:8]
                    n[len(n) - 1] = list(headers)[10]
                    options = st.multiselect("Выберите переменные", n)
                    visualize_data2(df, options, "логарифмическая")
            else:
                options = st.multiselect("Выберите переменные",
                                         list(headers))
                visualize_data4(df, options, scale_type="стандартная")
        elif p == "Распеределение переменных":
            st.markdown("### Распеределение переменных")
            st.markdown("Здесь вы можете увидеть распределение выбранных вами переменных.")
            headers = df.dtypes.index
            options = st.multiselect("Выберите переменные",
                                     list(headers))
            visualize_data3(df, options)





    @st.cache
    def get_data():
        df = pd.read_csv("world-happiness-report-2019.csv")
        df = df.dropna()
        return df

    def visualize_data(df, x_ax, y_ax):
        graph = alt.Chart(df).mark_circle(size=40).encode(x=x_ax, y=y_ax, color='Country (region)',
            tooltip=['Country (region)', 'Ladder']).interactive()
        st.write(graph)
    def visualize_data2(df, options, scale_type = "стандартная"):
        fig, ax = plt.subplots()
        for i in options:
            if scale_type == "логарифмическая":
                ax.loglog(df["Ladder"], df[i], label=str(i))
            else:
                ax.plot(df["Ladder"], df[i], label=str(i))
        ax.set_xlabel('Ladder')
        ax.legend()
        st.pyplot(fig)
    def visualize_data3(df, options):
        fig, ax = plt.subplots()
        for i in options:
            sns.kdeplot(df[i])
        ax.legend()
        st.pyplot(fig)
    def visualize_data4(df, options, scale_type = "стандартная"):
        ### FROM: https://altair-viz.github.io/gallery/multiline_tooltip.html
        np.random.seed(42)
        source = pd.DataFrame(df[options], index=df["Ladder"])
        source = source.reset_index().melt('Ladder', var_name='param', value_name='y')

        # Create a selection that chooses the nearest point & selects based on x-value
        nearest = alt.selection(type='single', nearest=True, on='mouseover',
                                fields=['Ladder'], empty='none')
        # The basic line
        line = alt.Chart(source).mark_line(interpolate='basis').encode(
            x='Ladder:Q',
            y='y:Q',
            color='param:N'
        )

        # Transparent selectors across the chart. This is what tells us
        # the x-value of the cursor
        selectors = alt.Chart(source).mark_point().encode(
            x='Ladder:Q',
            opacity=alt.value(0),
        ).add_selection(
            nearest
        )

        # Draw points on the line, and highlight based on selection
        points = line.mark_point().encode(
            opacity=alt.condition(nearest, alt.value(1), alt.value(0))
        )

        # Draw text labels near the points, and highlight based on selection
        text = line.mark_text(align='left', dx=5, dy=-5).encode(
            text=alt.condition(nearest, 'y:Q', alt.value(' '))
        )

        # Draw a rule at the location of the selection
        rules = alt.Chart(source).mark_rule(color='gray').encode(
            x='Ladder:Q',
        ).transform_filter(
            nearest
        )

        # Put the five layers into a chart and bind the data
        st.write(alt.layer(
            line, selectors, points, rules, text
        ).properties(
            width=600, height=300
        ))
        ###END





    if __name__ == "__main__":
        main()
