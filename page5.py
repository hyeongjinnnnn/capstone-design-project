import random

def page5(st):
    st.markdown("<h1 style='text-align: center; color: blue; font-size: 2em;'>Oral Proficiency Interview - computer (OPIc)</h1>", unsafe_allow_html=True)
        # 이미지 추가
    image_url = "https://raw.githubusercontent.com/ttkdenddl11/Algorithm/main/begin_warning.png"  # GitHub Raw URL 사용
    st.markdown(f'<div style="text-align: center;"><img src="{image_url}" style="width:95%;"></div>', unsafe_allow_html=True)

    # 가운데 정렬하기 위한 HTML/CSS
    centered_style = """
        <style>
            div.stButton > button {
                display: block;
                margin: 0 auto;
            }
        </style>
    """

    st.markdown(centered_style, unsafe_allow_html=True)

    if st.button("Begin", type="primary", ):
        # 질문 선별
        cursor = st.session_state.connection.cursor()
        st.session_state.question_list.append("Can you introduce yourself in as much detail as possible?")

        query = "SELECT question_text FROM question WHERE property = %s AND link = %s"

        option_value = st.session_state.selected_options['종사 분야']
        for i in range(3):
            cursor.execute(query, (option_value, i))
            st.session_state.question_list.append(cursor.fetchone()[0])

        option_value = st.session_state.selected_options['거주 방식']
        for i in range(3):
            cursor.execute(query, (option_value, i))
            st.session_state.question_list.append(cursor.fetchone()[0])

        option_value = random.choice(st.session_state.selected_options['여가 및 취미'])
        for i in range(3):
            cursor.execute(query, (option_value, i))
            st.session_state.question_list.append(cursor.fetchone()[0])

        option_value = random.choice(['롤플레이1', '롤플레이2', '롤플레이3', '롤플레이4'])
        for i in range(3):
            cursor.execute(query, (option_value, i))
            st.session_state.question_list.append(cursor.fetchone()[0])

        option_value = random.choice(['돌발질문:코로나', '돌발질문:코인', '돌발질문:출산율'])
        for i in range(2):
            cursor.execute(query, (option_value, i))
            st.session_state.question_list.append(cursor.fetchone()[0])

        st.session_state.question_page_number = 1
        return 'question_page'