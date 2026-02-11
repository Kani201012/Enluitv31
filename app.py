import streamlit as st
import zipfile
import io
import json
import datetime
import re

# --- 1. APP CONFIGURATION ---
st.set_page_config(
    page_title="Titan v30.7 | StopWebRent Master + Blog", 
    layout="wide", 
    page_icon="⚡",
    initial_sidebar_state="expanded"
)

# --- 2. GLOBAL UI SYSTEM (Preserving all your advanced CSS) ---
st.markdown("""
    <style>
    :root { --primary: #0f172a; --accent: #ef4444; }
    .stApp { background-color: #f8fafc; color: #1e293b; font-family: 'Inter', sans-serif; }
    [data-testid="stSidebar"] { background-color: #ffffff; border-right: 1px solid #e2e8f0; }
    [data-testid="stSidebar"] h1 { background: linear-gradient(90deg, #0f172a, #ef4444); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 900 !important; }
    .stButton>button { width: 100%; border-radius: 8px; height: 3.5rem; background: linear-gradient(135deg, #0f172a 0%, #334155 100%); color: white; font-weight: 800; border: none; box-shadow: 0 4px 15px rgba(15, 23, 42, 0.3); text-transform: uppercase; }
    iframe { border-radius: 12px; border: 1px solid #e2e8f0; box-shadow: 0 20px 40px -10px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR: CONTROL CENTER ---
with st.sidebar:
    st.title("Titan Architect")
    st.caption("v30.7 | Blog Engine Active")
    st.divider()
    
    with st.expander("🎨 Visual DNA", expanded=True):
        theme_mode = st.selectbox("Base Theme", ["Clean Corporate (Light)", "Midnight SaaS (Dark)", "Stark Minimalist"])
        c1, c2 = st.columns(2)
        p_color = c1.color_picker("Primary Brand", "#0F172A")
        s_color = c2.color_picker("Action (CTA)", "#EF4444")
        h_font = st.selectbox("Headings", ["Montserrat", "Space Grotesk", "Oswald"])
        b_font = st.selectbox("Body Text", ["Inter", "Open Sans", "Roboto"])
        border_rad = st.select_slider("Corner Roundness", ["0px", "4px", "12px", "24px"], value="12px")
        anim_type = st.selectbox("Animation Style", ["Fade Up", "Zoom In", "None"])

    with st.expander("🧩 Section Manager", expanded=False):
        show_hero = st.checkbox("Hero Carousel", value=True)
        show_stats = st.checkbox("Trust Stats", value=True)
        show_features = st.checkbox("Feature Grid (4 Pillars)", value=True)
        show_pricing = st.checkbox("Pricing Table", value=True)
        show_inventory = st.checkbox("Portfolio/Templates", value=True)
        show_blog = st.checkbox("Blog / Knowledge Base", value=True) # --- NEW ---
        show_gallery = st.checkbox("About Section", value=True)
        show_testimonials = st.checkbox("Testimonials", value=True)
        show_faq = st.checkbox("F.A.Q.", value=True)
        show_cta = st.checkbox("Final Call to Action", value=True)

    with st.expander("⚙️ SEO & Analytics"):
        seo_area = st.text_input("Service Area", "Global")
        ga_tag = st.text_input("Google Analytics ID")
        prod_url = st.text_input("Website URL", "https://www.stopwebrent.com")

# --- 4. MAIN WORKSPACE TABS ---
tabs = st.tabs(["1. Identity", "2. Content", "3. Pricing Logic", "4. Portfolio", "5. Blog Data", "6. Legal"])

with tabs[0]:
    c1, c2 = st.columns(2)
    biz_name = c1.text_input("Business Name", "StopWebRent.com")
    biz_tagline = c1.text_input("Tagline", "Stop Renting. Start Owning.")
    biz_phone = c1.text_input("WhatsApp Phone", "966572562151")
    biz_email = c1.text_input("Support Email", "hello@stopwebrent.com")
    biz_addr = c2.text_area("Address", "Titan HQ, Kolkata, India")
    map_iframe = c2.text_area("Map Embed Code")
    seo_d = c2.text_area("SEO Meta Description", "Stop paying monthly fees for Wix or Shopify. The Titan Engine builds ultra-fast (0.1s) websites. Pay once, own your code forever.")
    logo_url = c2.text_input("Logo URL (Optional)")

with tabs[1]:
    st.subheader("Hero & Pillars")
    hero_h = st.text_input("Hero Headline", "Stop Paying Rent for Your Website.")
    hero_sub = st.text_input("Hero Subtext", "0.1s Load Speed. $0 Monthly Fees. 100% Ownership.")
    hero_img_1 = st.text_input("Main Hero Image", "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=1600")
    feat_data = st.text_area("6 Pillars List (icon | title | desc)", "bolt | Performance | 0.1s Load Speed.\nwallet | Economic | $0 Monthly Rent.\ntable | Functional | Google Sheets CMS.\nshield | Authority | Unhackable Security.\nlayers | Reliability | Global Edge CDN.\nstar | Conversion | One-Tap WhatsApp.", height=150)
    about_h = st.text_input("About Headline", "Control Your Empire from a Spreadsheet")
    about_short = st.text_area("About Summary", "No WordPress dashboard. No plugins. Update your site via Google Sheets.")
    about_img = st.text_input("About Image", "https://images.unsplash.com/photo-1543286386-713df548e9cc?w=1600")

with tabs[2]:
    st.subheader("Pricing Table Data")
    titan_price, titan_mo = st.text_input("Titan Setup", "$199"), st.text_input("Titan Monthly", "$0")
    wix_name, wix_mo = st.text_input("Comp Name", "Wix (Core)"), st.text_input("Comp Monthly", "$29/mo")
    save_val = st.text_input("5-Year Savings", "$1,466")

with tabs[3]:
    st.subheader("Portfolio CSV")
    sheet_url = st.text_input("Portfolio CSV Link")
    custom_feat = st.text_input("Fallback Portfolio Image", "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=800")

# --- NEW: BLOG DATA TAB ---
with tabs[4]:
    st.header("📝 Blog Configuration")
    blog_csv_url = st.text_input("Blog Google Sheet CSV Link", placeholder="https://docs.google.com/spreadsheets/d/e/.../pub?output=csv")
    st.caption("Requires: Slug, Title, Date, Category, Summary, ImageURL, Content")

with tabs[5]:
    faq_data = st.text_area("FAQ (Q? ? A)", "Is it really $0? ? Yes, we use edge hosting.")
    testi_data = st.text_area("Testimonials (Name | Quote)", "Rajesh | Saved me $1000/year.")
    priv_txt = st.text_area("Privacy Text", "We treat data privacy as a fundamental architectural requirement.")
    term_txt = st.text_area("Terms Text", "Upon payment, full IP rights are transferred to the client.")

# --- 5. COMPILER ENGINE (Preserving all formatting logic) ---

def format_text(text):
    if not text: return ""
    processed = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    return processed.replace('\n', '<br>')

def get_theme_css():
    bg = "#ffffff" if "Light" in theme_mode else "#0f172a"
    txt = "#0f172a" if "Light" in theme_mode else "#f8fafc"
    card = "#ffffff" if "Light" in theme_mode else "#1e293b"
    return f"""
    :root {{ --p: {p_color}; --s: {s_color}; --bg: {bg}; --txt: {txt}; --card: {card}; --radius: {border_rad}; }}
    body {{ background: var(--bg); color: var(--txt); font-family: '{b_font}', sans-serif; margin: 0; line-height: 1.6; overflow-x:hidden; }}
    h1, h2, h3, h4 {{ font-family: '{h_font}', sans-serif; color: var(--p); line-height: 1.2; }}
    .container {{ max-width: 1200px; margin: 0 auto; padding: 0 20px; }}
    .btn {{ display: inline-block; padding: 1rem 2rem; border-radius: var(--radius); font-weight: 700; text-decoration: none; transition: 0.3s; text-align: center; cursor:pointer; border:none; }}
    .btn-primary {{ background: var(--p); color: white !important; }}
    .btn-accent {{ background: var(--s); color: white !important; }}
    nav {{ position: fixed; top: 0; width: 100%; z-index: 1000; background: rgba(255,255,255,0.95); backdrop-filter: blur(10px); border-bottom: 1px solid #eee; padding: 1rem 0; }}
    .nav-flex {{ display: flex; justify-content: space-between; align-items: center; }}
    .nav-links a {{ margin-left: 1.5rem; text-decoration: none; color: var(--txt); font-weight: 600; font-size: 0.9rem; }}
    .hero {{ padding: 10rem 0 5rem; text-align: center; background: linear-gradient(to bottom, var(--bg), var(--card)); }}
    .grid-3 {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem; }}
    .card {{ background: var(--card); padding: 2rem; border-radius: var(--radius); border: 1px solid rgba(0,0,0,0.05); transition: 0.3s; height: 100%; }}
    .card:hover {{ transform: translateY(-5px); box-shadow: 0 20px 40px rgba(0,0,0,0.05); }}
    .pricing-table {{ width: 100%; border-collapse: collapse; margin: 2rem 0; }}
    .pricing-table th, .pricing-table td {{ padding: 1.2rem; border: 1px solid #eee; text-align: left; }}
    .pricing-table th {{ background: var(--p); color: white; }}
    .contact-grid {{ display: grid; grid-template-columns: 1fr 2fr; gap: 3rem; }}
    @media (max-width: 768px) {{ .contact-grid, .detail-view {{ grid-template-columns: 1fr; }} .nav-links {{ display: none; }} }}
    .reveal {{ opacity: 0; transform: translateY(30px); transition: 0.8s; }}
    .reveal.active {{ opacity: 1; transform: translateY(0); }}
    """

def gen_nav():
    # Automatically adds Blog link if enabled
    blog_link = '<a href="blog.html">Blog</a>' if show_blog else ""
    logo = f'<img src="{logo_url}" height="40">' if logo_url else f'<span style="font-weight:900; font-size:1.5rem; color:var(--p)">{biz_name}</span>'
    return f"""<nav><div class="container nav-flex"><a href="index.html" style="text-decoration:none;">{logo}</a><div class="nav-links"><a href="index.html">Home</a><a href="about.html">About</a>{blog_link}<a href="contact.html">Contact</a><a href="https://wa.me/{biz_phone}" class="btn-accent btn" style="padding:0.5rem 1.2rem; border-radius:50px; margin-left:1rem;">WhatsApp</a></div></div></nav>"""

def gen_stats():
    if not show_stats: return ""
    return f"""<div style="background:var(--p); color:white; padding:4rem 0;"><div class="container grid-3" style="text-align:center;"><div><h2 style="color:white; font-size:3rem; margin:0;">{stat_1}</h2><p>{label_1}</p></div><div><h2 style="color:white; font-size:3rem; margin:0;">{stat_2}</h2><p>{label_2}</p></div><div><h2 style="color:white; font-size:3rem; margin:0;">{stat_3}</h2><p>{label_3}</p></div></div></div>"""

def gen_pricing_table():
    if not show_pricing: return ""
    return f"""<section id="pricing"><div class="container"><div class="section-head" style="text-align:center; margin-bottom:3rem;"><h2>The Cost of Ownership</h2><p>Stop paying rent to digital landlords.</p></div><div style="overflow-x:auto;"><table class="pricing-table"><thead><tr><th>Category</th><th style="background:var(--s);">Titan Engine</th><th>{wix_name}</th></tr></thead><tbody><tr><td>Setup Fee</td><td>{titan_price}</td><td>$0</td></tr><tr><td>Monthly Hosting</td><td>{titan_mo}</td><td>{wix_mo}</td></tr><tr><td><strong>5-Year Savings</strong></td><td style="color:var(--s); font-weight:bold;">Save {save_val}</td><td>$0</td></tr></tbody></table></div></div></section>"""

# --- BLOG HTML GENERATORS ---

def gen_blog_index_content():
    return f"""
    <section class="hero" style="min-height:40vh;">
        <div class="container"><h1>Knowledge Base</h1><p>Learn how to dominate local search without monthly fees.</p></div>
    </section>
    <section><div class="container"><div id="blog-grid" class="grid-3">Loading Articles...</div></div></section>
    <script>
    async function loadBlog() {{
        const res = await fetch('{blog_csv_url}');
        const txt = await res.text();
        const lines = txt.split(/\\r\\n|\\n/).slice(1);
        const box = document.getElementById('blog-grid');
        box.innerHTML = '';
        lines.forEach(line => {{
            if(!line.trim()) return;
            const c = line.split(/,(?=(?:(?:[^"]*"){2})*[^"]*$)/);
            box.innerHTML += `
                <div class="card">
                    <img src="${{c[5]}}" style="width:100%; height:200px; object-fit:cover; border-radius:8px; margin-bottom:1rem;">
                    <small style="color:var(--s); font-weight:bold;">${{c[3]}} | ${{c[2]}}</small>
                    <h3 style="margin:0.5rem 0;">${{c[1]}}</h3>
                    <p style="font-size:0.9rem; opacity:0.8; margin-bottom:1.5rem;">${{c[4]}}</p>
                    <a href="post.html?id=${{c[0]}}" class="btn btn-primary" style="padding:0.6rem 1rem; font-size:0.8rem;">Read Article</a>
                </div>`;
        }});
    }}
    loadBlog();
    </script>
    """

def gen_post_detail_content():
    return f"""
    <section style="padding-top:150px;"><div class="container" style="max-width:800px;">
        <div id="post-content">Loading...</div>
        <br><br>
        <a href="blog.html" style="text-decoration:none; color:var(--p); font-weight:bold;">&larr; Back to Knowledge Base</a>
    </div></section>
    <script>
    async function loadPost() {{
        const id = new URLSearchParams(window.location.search).get('id');
        const res = await fetch('{blog_csv_url}');
        const txt = await res.text();
        const lines = txt.split(/\\r\\n|\\n/).slice(1);
        lines.forEach(line => {{
            const c = line.split(/,(?=(?:(?:[^"]*"){2})*[^"]*$)/);
            if(c[0] === id) {{
                document.getElementById('post-content').innerHTML = `
                    <img src="${{c[5]}}" style="width:100%; border-radius:12px; margin-bottom:2rem;">
                    <h1 style="font-size:3rem; line-height:1.1;">${{c[1]}}</h1>
                    <p style="color:var(--s); font-weight:bold;">${{c[3]}} — ${{c[2]}}</p>
                    <hr style="opacity:0.1; margin:2rem 0;">
                    <div style="font-size:1.2rem; line-height:1.8;">${{c[6].replace(/\\n/g, '<br>')}}</div>
                `;
            }}
        }});
    }}
    loadPost();
    </script>
    """

# --- 6. PAGE BUILDER & EXPORT ---

def build_page(title, content):
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>{title} | {biz_name}</title><style>{get_theme_css()}</style></head><body>{gen_nav()}{content}{gen_footer()}<script>window.addEventListener('scroll',()=>{{document.querySelectorAll('.reveal').forEach(r=>{{if(r.getBoundingClientRect().top<window.innerHeight-100)r.classList.add('active')}})}});window.dispatchEvent(new Event('scroll'));</script></body></html>"""

st.divider()
c1, c2 = st.columns([3, 1])

with c1:
    st.subheader("Live Preview")
    home_preview = f'<section class="hero"><div class="container"><h1>{hero_h}</h1><p>{hero_sub}</p></div></section>' + gen_stats() + gen_pricing_table()
    st.components.v1.html(build_page("Home", home_preview), height=500, scrolling=True)

with c2:
    st.success("v30.7 Engine Ready.")
    if st.button("DOWNLOAD WEBSITE ZIP", type="primary"):
        z_b = io.BytesIO()
        with zipfile.ZipFile(z_b, "a", zipfile.ZIP_DEFLATED, False) as zf:
            # 1. Main Pages
            zf.writestr("index.html", build_page("Home", home_preview))
            zf.writestr("about.html", build_page("About", f'<section style="padding-top:150px;"><div class="container"><h1>{about_h}</h1><p>{about_short}</p><img src="{about_img}" style="width:100%; border-radius:12px;"></div></section>'))
            zf.writestr("contact.html", build_page("Contact", f'<section style="padding-top:150px;"><div class="container"><h1>Contact Us</h1><p>{biz_email}</p></div></section>'))
            zf.writestr("privacy.html", build_page("Privacy", f'<section style="padding-top:150px;"><div class="container">{priv_txt}</div></section>'))
            
            # 2. Blog Engine Pages (Mandatory for the feature to work)
            zf.writestr("blog.html", build_page("Blog", gen_blog_index_content()))
            zf.writestr("post.html", build_page("Article", gen_post_detail_content()))
            
            # 3. Robots & Sitemap
            zf.writestr("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {prod_url}/sitemap.xml")
            
        st.download_button("📥 Click to Save Zip", z_b.getvalue(), "stopwebrent_final.zip")
