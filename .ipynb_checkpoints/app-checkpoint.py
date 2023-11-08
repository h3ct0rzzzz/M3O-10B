import streamlit as st
import pandas as pd
import plotly.express as px
import time
from itertools import count
from tabulate import tabulate  # Импортируйте библиотеку tabulate
from PIL import Image


# Функция для сортировки вставками
def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
        yield arr

        
# Основная функция приложения
def main():
    st.title('Лабораторная №1. Проектирование ПО при структурном подходе. Реализация сортировки вставками.')
    st.markdown(' Выполнили студенты группы `М3О-310Б-21` - Караваев К., Дудоров Д., Алиякбяров М.')

    
    # Markdown-секция с теорией по сортировке вставками
    st.markdown("## Сортировка вставками (Insertion Sort).")
    st.markdown("Сортировка вставками (Insertion sort) — алгоритм сортировки, в котором элементы входной последовательности просматриваются по одному, и каждый новый поступивший элемент размещается в подходящее место среди ранее упорядоченных элементов.")
    st.markdown("Вход: последовательность из $n$ чисел〈$a_1, a_2, \dots, a_n $〉. ")
    st.markdown("Выход: перестановка (изменение порядка) 〈$a_1', a_2', \dots, a_n'$〉 входной последовательности таким образом, что для ее членов выполняется соотношение $$ a_1' \leqslant a_2' \leqslant \cdots, a_n' $$")
    st.markdown("В начальный момент отсортированная последовательность пуста. На каждом шаге алгоритма выбирается один из элементов входных данных и помещается на нужную позицию в уже отсортированной последовательности до тех пор, пока набор входных данных не будет исчерпан. В любой момент времени в отсортированной последовательности элементы удовлетворяют требованиям к выходным данным алгоритма.")
    st.markdown("Данный алгоритм можно ускорить при помощи использования бинарного поиска для нахождения места текущему элементу в отсортированной части. Проблема с долгим сдвигом массива вправо решается при помощи смены указателей.")
    st.markdown("Псевдокод сортировки методом вставок представлен ниже под названием **INSERTION_SORT**. На его вход подается массив $A[1..n]$, содержащий последовательность из $n$ сортируемых чисел (количество элементов массива $A$ обозначено в этом коде как $length[A]$.) Входные числа **сортируются без использования дополнительной памяти:** их перестановка производится в пределах массива, и объем используемой при этом дополнительной памяти не превышает некоторую постоянную величину. По окончании работы алгоритма **INSERTION_SORT** входной массив содержит отсортированную последовательность:")
    st.markdown("$INSERTION\_SORT(A)$")
    st.markdown("$for \, j  \leftarrow 2 \, to \, length[A]$")
    st.markdown("$\quad do \, key \leftarrow \, A[j]$")
    st.markdown("$ \quad$▷ Вставка элемента $A[j]$ в отсортированную последовательность $A[1..j − 1]$")
    st.markdown("$ \quad i \leftarrow j - 1 $")
    st.markdown("$ \quad while \, i > 0 \, and \, A[i] > \, key$")
    st.markdown("$ \quad \quad do \, A[i+1] \leftarrow A[i]$")
    st.markdown("$ \quad \quad \quad i \leftarrow  i - 1$")
    st.markdown("$ \quad  A[i+1] \leftarrow \, key$")
    st.markdown("")

    image = Image.open('Screenshot_1.png')
    st.image(image, caption='Изображение сортировки выбором.')

    st.markdown("Анализ алгоритма.")
    st.markdown("* Худшее время: $\mathcal{O}(n^{2})$ сравнений, обменов")
    st.markdown("* Лучшее время: $\mathcal{O}(n)$ сравнений, обменов")
    st.markdown("* Среднее время: $\mathcal{O}(n^{2})$ сравнений, обменов")
    st.markdown("* Затраты памяти: $\mathcal{O}(n)$ всего, $\mathcal{O}(1)$ вспомогательный")
    
    
    st.title("Запуск алгоритма.")
    
    # Выбор входного файла или готовых файлов
    option = st.radio("Выберите источник данных", ("Ввести данные вручную", "Использовать готовый файл", "Загрузить файл из директории"))
    data = None
    if option == "Ввести данные вручную":
        data = st.text_area("Введите данные (разделитель - запятая)", "5,2,9,1,5,6,3,8,7,4")
        data = [int(x.strip()) for x in data.split(',')]
    elif option == "Использовать готовый файл":
        selected_file = st.selectbox("Выберите готовый файл", ("test_1.txt", "test_2.txt", "test_3.txt", "test_4.txt", "test_5.txt"))
        with open(selected_file, 'r') as file:
            data = file.read().strip().split(',')
            data = [int(x) for x in data]
    else:
        uploaded_file = st.file_uploader("Загрузите файл", type=["txt"])
        if uploaded_file is not None:
            data = uploaded_file.read().decode("utf-8").strip().split(',')
            data = [int(x) for x in data]
    
    
    # Отображение данных в виде таблицы в маркдаун
    data_table = tabulate([data], headers=[''], tablefmt='pipe')
    st.markdown(f"Исходные данные:\n\n{data_table}")
    st.markdown("")

    speed = st.slider('Скорость визуализации одного такта сортировки на графике (сек.)', 0.0, 1.0, 0.2)

    st.title("")
    
    if st.button('Отсортировать массив'):
         # # График для визуализации сортировки
        fig = px.bar(y=data, labels={'y': 'Значение'}, title='Сортировка вставками')
        fig.update_layout(yaxis=dict(dtick=1.0))  # Добавляем интервал на оси y равный 1.0
        chart = st.plotly_chart(fig)

        # Массив для хранения всех итераций
        all_iterations = []

        # Переменная для цвета измененных элементов
        color_changed = 'red'

        prev_sorted_data = data.copy()  # Создаем копию исходных данных

        for step, sorted_data in enumerate(insertion_sort(data)):
            # Обновляем график с текущим состоянием массива
            fig.data[0].y = sorted_data
            chart.plotly_chart(fig)

            # Определяем измененные элементы и помечаем их
            changed_indices = [i for i in range(len(sorted_data)) if sorted_data[i] != prev_sorted_data[i]]
            colored_data = sorted_data.copy()

            # Добавляем текущую итерацию в массив всех итераций
            all_iterations.append(colored_data)

            # Обновляем предыдущее состояние
            prev_sorted_data = sorted_data

            # Добавляем временную задержку для визуализации
            time.sleep(speed)

        # Вывод всех итераций в виде таблицы Markdown
        st.write('Все итерации сортировки:')
        #data_table = tabulate([data], headers=[''], tablefmt='pipe')
        st.markdown(f'**Итерация 0:**\n\n{data_table}')
        for i, iteration in enumerate(all_iterations):
            iteration_table = tabulate([iteration], headers=[''], tablefmt='pipe')
            st.markdown(f'**Итерация {i + 1}:**\n\n{iteration_table}')

        st.write('\n')
        st.markdown('## `Сортировка завершена!`')  
        st.balloons()
        
    st.button("Очистить кэш", type="primary")
    
if __name__ == '__main__':
    main()