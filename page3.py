def page3(st):
    st.markdown("<h6 font-size: 1.0em;'>질문을 읽고 정확히 답변해 주시기 바랍니다. 설문에 대한 응답을 기초로 개인별 문항이 출제됩니다.</h6>", unsafe_allow_html=True)
    st.markdown("<h3 font-size: 1.0em;'>Part 2 of 3</h3>", unsafe_allow_html=True)

    # Create Radio Buttons
    # 선택 옵션
    options = ["개인주택이나 아파트에 홀로 거주", "친구나 룸메이트와 함께 주택이나 아파트에 거주", "가족과 함께 주택이나 아파트에 거주",]
    
    # 라디오 박스 생성
    selected_option = st.radio("현재 귀하는 어디에 살고 계십니까?", options, key="_1")

    # 선택된 옵션을 딕셔너리에 저장
    st.session_state.selected_options['거주 방식'] = selected_option
    
    # 가운데 정렬하기 위한 HTML/CSS
    centered_style = """
        <style>
            div.stButton > button {
                display: block;
                
            }
        </style>
    """

    # Streamlit 앱에 적용
    st.markdown(centered_style, unsafe_allow_html=True)
    col1_btn, col2_btn = st.columns(2)
    if col1_btn.button("< Back", type="primary", ):
        #if custom_button("다음 페이지", key='page1_next'):
        return 'page2'
        
    elif col2_btn.button("Next >", type="primary", ):
        #if custom_button("다음 페이지", key='page1_next'):
        return 'page4'