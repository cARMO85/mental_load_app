# utils/ui.py
import html
import streamlit as st
import streamlit.components.v1 as components
from typing import List, Optional

def _has_popover() -> bool:
    return hasattr(st, "popover")

def _esc(s: str) -> str:
    # Escape HTML so user text doesn’t break your markup
    return html.escape(s or "")

def step_header(title: str, subtitle: str = "", progress: int | None = None):
    st.markdown(f"### {title}")
    if subtitle:
        st.caption(subtitle)
    if isinstance(progress, int):
        st.progress(max(0, min(progress, 100)))

def learn_popover():
    ctx = st.popover("🔎 Learn / Help") if _has_popover() else st.expander("🔎 Learn / Help")
    with ctx:
        st.markdown("**What is mental load?**")
        st.write("The unseen planning, thinking and keeping-track work behind household life.")
        st.markdown("**What do sliders mean?**")
        st.write("- **Responsibility (0–100):** who mainly owns it (0 = Partner A, 100 = Partner B).")
        st.write("- **Burden (1–5):** how mentally taxing it feels.")
        st.write("- **Fairness (1–5):** how fair it feels right now.")
        st.markdown("**Tips for doing this together**")
        st.write("Talk as you go, keep it light, take a break if needed.")

def safety_note():
    st.info(
        "If anything here feels sensitive, pause and come back later. "
        "This tool is for a constructive chat, not for blame or therapy."
    )

def section_notes(key: str, placeholder: str = "Anything you noticed while answering…"):
    return st.text_area("📝 Notes for this section (optional)", key=key, height=100, placeholder=placeholder)

def tiny_hint(text: str):
    st.caption(text)

def explainer_block(title: str, bullets: List[str]):
    st.markdown(f"**{_esc(title)}**", unsafe_allow_html=True)
    for b in bullets:
        st.write(f"- {b}")


def scroll_to_top():
    """Scroll the app viewport to the top using an embedded script.

    This uses a few approaches in the script to improve reliability across
    different Streamlit embedding/layout variations.
    """
    components.html(
        """
        <script>
            try {
                const mainContent = window.parent.document.querySelector('section.main');
                if (mainContent) {
                    mainContent.scrollTop = 0;
                }
            } catch(e) {}
            try { window.parent.document.body.scrollTop = 0; } catch(e) {}
            try { window.parent.document.documentElement.scrollTop = 0; } catch(e) {}
            try { window.parent.scrollTo(0,0); } catch(e) {}
            try { window.parent.scrollTo({top:0, behavior:'instant'}); } catch(e) {}
        </script>
        """,
        height=0,
    )

def definition_box(
    title: str,
    definition: str,
    what_counts: Optional[List[str]] = None,
    note: Optional[str] = None,
    example: Optional[str] = None,
):
    """Compact definition card used at the top of each task."""
    html_parts = [
        '<div class="card">',
        f'<div class="section-title">{_esc(title)}</div>',
        f'<p>{_esc(definition)}</p>',
    ]
    if what_counts:
        html_parts.append("<ul>")
        for item in what_counts:
            html_parts.append(f"<li>{_esc(item)}</li>")
        html_parts.append("</ul>")

    if example:
        html_parts.append(
            f'<div class="alert-info" style="margin-top:8px;"><strong>Example</strong><br>{_esc(example)}</div>'
        )

    if note:
        html_parts.append(
            f'<p style="color:#475569;margin-top:8px;"><small>{_esc(note)}</small></p>'
        )

    html_parts.append("</div>")
    st.markdown("".join(html_parts), unsafe_allow_html=True)
