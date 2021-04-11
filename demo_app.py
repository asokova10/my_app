import streamlit as st
import altair as alt
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
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
            st.markdown("Вы можете выбрать шкалу: стандартную или логарифмическую.")
            headers = df.dtypes.index
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
        graph = alt.Chart(df).mark_circle(size=60).encode(
            x=x_ax,
            y=y_ax,
            color='Country (region)',
            tooltip=['Country (region)', 'Ladder']
        ).interactive()
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

    if __name__ == "__main__":
        main()
