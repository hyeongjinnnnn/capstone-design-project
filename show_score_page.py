def show_score_page(st):
    # 가운데 정렬하기 위한 HTML/CSS
    centered_style = """
        <style>
            div.stButton > button {
                display: block;
                margin: 0 auto;
            }
        </style>
    """
    # Streamlit 앱에 적용
    st.markdown(centered_style, unsafe_allow_html=True)

    st.markdown("<h1 style='text-align: center; color: blue; font-size: 2em;'>Oral Proficiency Interview - computer (OPIc)</h1>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; font-size: 1.5em;'>점수</h1>", unsafe_allow_html=True)

    
    st.markdown("<h3 style='text-align: center; font-size: 1.5em;'>수고하셨습니다.</h3>", unsafe_allow_html=True)
    st.markdown("<br><br>", unsafe_allow_html=True)