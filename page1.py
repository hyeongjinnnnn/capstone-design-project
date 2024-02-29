def page1(st):
    st.markdown("<h1 style='text-align: center; color: blue; font-size: 2em;'>Oral Proficiency Interview - computer (OPIc)</h1>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; font-size: 1.5em;'>지금부터 English 말하기 평가를 시작하겠습니다.</h1>", unsafe_allow_html=True)

    # 이미지 추가
    image_url = "https://raw.githubusercontent.com/ttkdenddl11/Algorithm/main/index_woman.png"  # GitHub Raw URL 사용

    st.markdown(f'<div style="text-align: center;"><img src="{image_url}" style="width:33%;"></div>', unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; font-size: 1.5em;'>본 인터뷰 평가는 졸업작품 평가용 입니다.</h1>", unsafe_allow_html=True)
    st.markdown("<br><br>", unsafe_allow_html=True)

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

    if st.button("Next >", type="primary", ):
        return 'page2'