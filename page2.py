def page2(st):
    st.markdown("<h6 font-size: 1.0em;'>질문을 읽고 정확히 답변해 주시기 바랍니다. 설문에 대한 응답을 기초로 개인별 문항이 출제됩니다.</h6>", unsafe_allow_html=True)
    st.markdown("<h3 font-size: 1.0em;'>Part 1 of 3</h3>", unsafe_allow_html=True)

    # Create Radio Buttons
    # 선택 옵션
    options = ["사업자/직장인", "학생", "취업준비생"]
    
    # 라디오 박스 생성
    selected_option = st.radio("현재 귀하는 어느 분야에 종사하고 계십니까?", options, key="_1")

    # 선택된 옵션을 딕셔너리에 저장
    st.session_state.selected_options['종사 분야'] = selected_option

    # 가운데 정렬하기 위한 HTML/CSS
    centered_style = """
        <style>
            div.stButton > button {
                display: block;
                margin: 0;
            }
        </style>
    """

    # Streamlit 앱에 적용
    st.markdown(centered_style, unsafe_allow_html=True)
    
    if st.button("Next >", type="primary", ):
        return 'page3'