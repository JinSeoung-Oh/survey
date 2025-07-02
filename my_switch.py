import streamlit as st
from streamlit.runtime.scriptrunner import get_script_run_ctx
from streamlit.runtime.pages_manager import PagesManager

def switch_page(target_page_name: str):
    """
    페이지 이름(target_page_name, .py 확장자 제외)으로 멀티페이지 간 이동을 수행합니다.
    """
    ctx = get_script_run_ctx()
    if ctx is None:
        raise RuntimeError("Couldn't get script context")
    # PagesManager 인스턴스에서 모든 페이지 정보 가져오기
    manager = PagesManager.get_current()
    pages = manager.get_pages()
    # 원하는 페이지 해시 찾기
    for page_hash, page_info in pages.items():
        name = page_info.get("page_name") or page_info.get("script_path","")
        # page_name 자체 또는 script_path의 파일명으로 매칭
        if name == target_page_name or name.endswith(f"{target_page_name}.py"):
            ctx.requested_page_script_hash = page_hash
            st.experimental_rerun()
            return
    raise ValueError(f"Could not find page: {target_page_name}")
