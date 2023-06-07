# ===============================页面跳转=========================
def switch_page(page_name: str):
    # https://github.com/arnaudmiribel/streamlit-extras/blob/main/src/streamlit_extras/switch_page_button/__init__.py
    from streamlit.runtime.scriptrunner import RerunData, RerunException
    from streamlit.source_util import get_pages

    def standardize_name(name: str) -> str:
        return name.lower().replace("_", " ")

    page_name = standardize_name(page_name)

    pages = get_pages("")

    for page_hash, config in pages.items():
        if standardize_name(config["page_name"]) == page_name:
            raise RerunException(
                RerunData(
                    page_script_hash=page_hash,
                    page_name=page_name,
                )
            )

    page_names = [standardize_name(config["page_name"]) for config in pages.values()]

    raise ValueError(f"Could not find page {page_name}. Must be one of {page_names}")


# ===============================页面跳转=========================

# ===============================页面跳转1=========================
from streamlit.components.v1 import html
import streamlit as st
import urllib.parse
def nav_page(page_name, timeout_secs=3):
    # https://github.com/streamlit/streamlit/issues/4832
    page_name = urllib.parse.quote(page_name.encode('utf8'))
    nav_script = """
        <script type="text/javascript">
            function attempt_nav_page(page_name, start_time, timeout_secs) {
                var links = window.parent.document.getElementsByTagName("a");
                for (var i = 0; i < links.length; i++) {
                    if (links[i].href.toLowerCase().endsWith("/" + page_name.toLowerCase())) {
                        links[i].click();
                        return;
                    }
                }
                var elasped = new Date() - start_time;
                if (elasped < timeout_secs * 1000) {
                    setTimeout(attempt_nav_page, 100, page_name, start_time, timeout_secs);
                } else {
                    alert("Unable to navigate to page '" + page_name + "' after " + timeout_secs + " second(s).");
                }
            }
            window.addEventListener("load", function() {
                attempt_nav_page("%s", new Date(), %d);
            });
        </script>
    """ % (page_name, timeout_secs)
    html(nav_script)

if __name__ == "__main__":
    want_to_contribute = st.button("重点指标地区覆盖度!")
    if want_to_contribute:
        switch_page("重点指标地区覆盖度")
    if st.button("重点指标数据查询"):
        nav_page("重点指标数据查询")
# ===============================页面跳转1=========================
