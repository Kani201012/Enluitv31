import streamlit as st
import zipfile
import io
import json
import datetime
import re

# --- 1. APP CONFIGURATION ---
st.set_page_config(
    page_title="Titan v31.5 | Social Edition", 
    layout="wide", 
    page_icon="⚡",
    initial_sidebar_state="expanded"
)

# --- 2. ADVANCED UI SYSTEM (CSS FOR BUILDER) ---
st.markdown("""
    <style>
    /* UI Reset & Variables */
    :root { --primary: #0f172a; --accent: #ef4444; }
    .stApp { background-color: #f8fafc; color: #1e293b; font-family: 'Inter', sans-serif; }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] { background-color: #ffffff; border-right: 1px solid #e2e8f0; }
    [data-testid="stSidebar"] h1 { 
        background: linear-gradient(90deg, #0f172a, #ef4444);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900 !important;
        font-size: 1.8rem !important;
    }
    
    /* Modern Inputs */
    .stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] {
        background-color: #ffffff !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 8px !important;
        color: #0f172a !important;
        transition: all 0.2s ease;
    }
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.1) !important;
    }
    
    /* Action Buttons */
    .stButton>button {
        width: 100%; border-radius: 8px; height: 3.5rem;
        background: linear-gradient(135deg, #0f172a 0%, #334155 100%);
        color: white; font-weight: 800; border: none;
        box-shadow: 0 4px 15px rgba(15, 23, 42, 0.3);
        text-transform: uppercase; letter-spacing: 1px;
        transition: transform 0.2s;
    }
    .stButton>button:hover { transform: translateY(-2px); }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR: THE CONTROL CENTER ---
with st.sidebar:
    st.title("Titan Architect")
    st.caption("v31.5 | Social Sharing Added")
    st.divider()
    
    # 3.1 VISUAL DNA
    with st.expander("🎨 Visual DNA", expanded=True):
        theme_mode = st.selectbox("Base Theme", [
            "Clean Corporate (Light)", 
            "Midnight SaaS (Dark)", 
            "Glassmorphism (Blur)",
            "Cyberpunk Neon",
            "Luxury Gold",
            "Forest Eco",
            "Ocean Breeze",
            "Stark Minimalist"
        ])
        c1, c2 = st.columns(2)
        p_color = c1.color_picker("Primary Brand", "#0F172A") 
        s_color = c2.color_picker("Action (CTA)", "#EF4444")  
        
        st.markdown("**Typography**")
        h_font = st.selectbox("Headings", ["Montserrat", "Space Grotesk", "Playfair Display", "Oswald", "Clash Display"])
        b_font = st.selectbox("Body Text", ["Inter", "Open Sans", "Roboto", "Satoshi", "Lora"])
        
        st.markdown("**UI Physics**")
        border_rad = st.select_slider("Corner Roundness", ["0px", "4px", "12px", "24px", "40px"], value="12px")
        anim_type = st.selectbox("Animation Style", ["Fade Up", "Zoom In", "Slide Right", "None"])

    # 3.2 MODULE MANAGER
    with st.expander("🧩 Section Manager", expanded=False):
        st.caption("Toggle sections to include:")
        show_hero = st.checkbox("Hero Carousel", value=True)
        show_stats = st.checkbox("Trust Stats/Logos", value=True)
        show_features = st.checkbox("Feature Grid (4 Pillars)", value=True)
        show_pricing = st.checkbox("Pricing Comparison Table", value=True)
        show_inventory = st.checkbox("Portfolio/Inventory (CSV)", value=True)
        show_blog = st.checkbox("Blog / News Engine", value=True)
        show_gallery = st.checkbox("About Section", value=True)
        show_testimonials = st.checkbox("Testimonials", value=True)
        show_faq = st.checkbox("F.A.Q.", value=True)
        show_cta = st.checkbox("Final Call to Action", value=True)

    # 3.3 TECHNICAL
    with st.expander("⚙️ SEO & Analytics", expanded=False):
        st.markdown("**Targeting**")
        seo_area = st.text_input("Service Area (City/Region)", "Global / Online")
        seo_kw = st.text_area("SEO Keywords", "web design, no monthly fees, one time payment website, stop web rent")
        
        st.markdown("**Verification**")
        gsc_tag = st.text_input("Google Verification ID")
        ga_tag = st.text_input("Google Analytics ID (G-XXXX)")
        og_image = st.text_input("Social Share Image URL")

# --- 4. MAIN WORKSPACE ---
st.title("🏗️ StopWebRent Site Builder")

tabs = st.tabs(["1. Identity", "2. Content Blocks", "3. Pricing Logic", "4. Inventory/Portfolio", "5. Blog Engine", "6. Legal & Footer"])

with tabs[0]:
    c1, c2 = st.columns(2)
    with c1:
        biz_name = st.text_input("Business Name", "StopWebRent.com")
        biz_tagline = st.text_input("Tagline", "Stop Renting. Start Owning.")
        biz_phone = st.text_input("Phone", "966572562151")
        biz_email = st.text_input("Email (For Forms)", "hello@kaydiemscriptlab.com")
    with c2:
        prod_url = st.text_input("Website URL", "https://www.stopwebrent.com")
        biz_addr = st.text_area("Address", "Kaydiem Script Lab\nKanishka’s House, Garia Station Rd\nKolkata, West Bengal 700084, India", height=100)
        map_iframe = st.text_area("Google Map Embed Code", placeholder='<iframe src="..."></iframe>', height=100)
        seo_d = st.text_area("Meta Description (SEO)", "Stop paying monthly fees for Wix or Shopify. The Titan Engine builds ultra-fast (0.1s) websites with $0 hosting costs. Pay once, own your code forever.", height=100)
        logo_url = st.text_input("Logo URL (PNG/SVG)")
        
    st.subheader("Social Links (Footer Icons)")
    sc1, sc2, sc3 = st.columns(3)
    fb_link = sc1.text_input("Facebook URL")
    ig_link = sc2.text_input("Instagram URL")
    x_link = sc3.text_input("X (Twitter) URL")
    
    sc4, sc5, sc6 = st.columns(3)
    li_link = sc4.text_input("LinkedIn URL")
    yt_link = sc5.text_input("YouTube URL")
    wa_num = sc6.text_input("WhatsApp Number (No +)", "966572562151")

with tabs[1]:
    st.subheader("Hero Carousel")
    st.info("💡 Add up to 3 images for the sliding hero banner.")
    hero_h = st.text_input("Hero Headline", "Stop Paying Rent for Your Website.")
    hero_sub = st.text_input("Hero Subtext", "The Titan Engine is the world’s first 0.1s website architecture that runs on $0 monthly fees. Pay once. Own it forever.")
    
    hc1, hc2, hc3 = st.columns(3)
    hero_img_1 = hc1.text_input("Slide 1 Image", "https://images.unsplash.com/photo-1460925895917-afdab827c52f?q=80&w=1600")
    hero_img_2 = hc2.text_input("Slide 2 Image", "https://images.unsplash.com/photo-1551288049-bebda4e38f71?q=80&w=1600")
    hero_img_3 = hc3.text_input("Slide 3 Image", "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?q=80&w=1600")
    
    st.divider()
    
    st.subheader("Trust Stats Data")
    col_s1, col_s2, col_s3 = st.columns(3)
    stat_1 = col_s1.text_input("Stat 1", "0.1s")
    label_1 = col_s1.text_input("Label 1", "Load Speed")
    
    stat_2 = col_s2.text_input("Stat 2", "$0")
    label_2 = col_s2.text_input("Label 2", "Monthly Fees")
    
    stat_3 = col_s3.text_input("Stat 3", "100%")
    label_3 = col_s3.text_input("Label 3", "Ownership")

    st.divider()
    
    st.subheader("The 4 Pillars (Feature Grid)")
    st.info("Keywords: bolt (speed), wallet (cost), table (sheets), shield (security), star, heart")
    f_title = st.text_input("Features Title", "The Titan Value Pillars")
    feat_data = st.text_area("Features List", 
                             "bolt | The Performance Pillar | **0.1s High-Velocity Loading**. While traditional sites take 3–5s, Titan loads instantly. This satisfies Google’s Core Web Vitals perfectly for higher ranking.\nwallet | The Economic Pillar | **$0 Monthly Fees**. We eliminated hosting subscriptions. You pay once and own the raw source code forever. No 'rent', no 'maintenance fees'.\ntable | The Functional Pillar | **Google Sheets CMS**. Update prices and photos directly from a simple spreadsheet. If you can use Excel, you can manage your website instantly.\nshield | The Authority Pillar | **Unhackable Security**. By removing the database (Zero-DB Architecture), we have removed the hacker's primary entry point. Your site is impenetrable.\nlayers | The Reliability Pillar | **Global Edge Deployment**. Your site doesn't live on one slow server. It is distributed across 100+ servers worldwide (CDN), creating 99.9% uptime and instant access from any city.\nstar | The Conversion Pillar | **One-Tap WhatsApp**. We embed 'Direct-to-Chat' technology. Customers don't need to save your number; they simply tap one button to start a sales conversation immediately.",
                             height=150)
    
    st.subheader("About Content")
    
    about_h = st.text_input("About Title", "Control Your Empire from a Spreadsheet")
    about_img = st.text_input("About Side Image", "https://images.unsplash.com/photo-1543286386-713df548e9cc?q=80&w=1600")
    
    c_a1, c_a2 = st.columns(2)
    about_short = c_a1.text_area("Home Page Summary (Short)", "No WordPress dashboard. No plugins to update. Just open your private Google Sheet, change a text, and watch your site update globally in seconds.", height=200)
    about_long = c_a2.text_area("Full About Page Content (Long)", "**The Digital Landlord Trap**\nMost business owners don't realize they are trapped in a rental cycle. Platforms like Wix, Squarespace, and Shopify act as Digital Landlords. They charge you rent every single month to keep your business online. If you stop paying, they delete your website. Over 5 years, a cheap $29/mo website actually drains over $1,700 from your pocket.\n\n**The Titan Philosophy: Ownership**\nAt StopWebRent.com, we believe you should own your digital home, not rent it. We reject bloatware, heavy databases, and recurring subscription models. Our mission is to democratize Enterprise Grade technology for small business owners.\n\n**How We Achieve $0 Monthly Fees**\nWe utilize Static Site Architecture. Unlike traditional sites that require a heavy server running 24/7 (costing money), Titan sites are pre-built and live on the Global Edge (CDN).", height=200)

with tabs[2]:
    st.subheader("💰 Pricing Comparison Table")
    st.info("This configures the table that compares you vs. Wix/Shopify.")
    
    col_p1, col_p2, col_p3 = st.columns(3)
    titan_price = col_p1.text_input("Titan Setup Price", "$199")
    titan_mo = col_p1.text_input("Titan Monthly", "$0")
    
    wix_name = col_p2.text_input("Competitor Name", "Wix (Core Plan)")
    wix_mo = col_p2.text_input("Competitor Monthly", "$29/mo")
    
    save_val = col_p3.text_input("5-Year Savings Calculation", "$1,466")
    
    st.caption("The table calculates: Titan (One time) vs Competitor (Monthly x 60 months).")

with tabs[3]:
    st.subheader("Portfolio & Templates")
    st.info("⚡ Power your portfolio with a Google Sheet")
    sheet_url = st.text_input("Google Sheet CSV Link", placeholder="https://docs.google.com/spreadsheets/d/e/.../pub?output=csv")
    custom_feat = st.text_input("Default Product Image URL (Fallback)", "https://images.unsplash.com/photo-1460925895917-afdab827c52f?q=80&w=800")
    st.caption("Required Columns: Name, Price, Description, ImageURL")

# --- NEW TAB: BLOG ENGINE ---
with tabs[4]:
    st.subheader("📰 Titan Blog Engine")
    st.info("Connect a Google Sheet to power your blog. Zero database required.")
    
    blog_sheet_url = st.text_input("Blog CSV Link", placeholder="https://docs.google.com/spreadsheets/d/e/.../pub?output=csv", help="Publish your sheet as CSV")
    
    st.markdown("""
    **Required CSV Columns:**
    1. `Slug` (e.g., my-first-post)
    2. `Title` (e.g., Why we are the best)
    3. `Date` (e.g., Oct 20, 2026)
    4. `Category` (e.g., Tech)
    5. `Summary` (Short intro for the grid)
    6. `ImageURL` (Main featured image)
    7. `Content` (Full text. Supports **Bold** and * Bullets)
    """)
    
    blog_hero_title = st.text_input("Blog Page Title", "Latest Insights")
    blog_hero_sub = st.text_input("Blog Page Subtext", "Thoughts on technology, business, and freedom.")

with tabs[5]:
    st.subheader("Trust & Legal")
    st.info("💡 Use `**Title**` for bold headers.")
    testi_data = st.text_area("Testimonials (Name | Quote)", "Rajesh Gupta, HVAC Business Owner | I was paying Wix $35/month for 3 years. Titan built me a faster site for a one-time fee. I stopped the bleeding and finally own my asset.\nSarah Jenkins, Cafe Owner | Updating my menu used to be a nightmare on WordPress. Now, I just open a Google Sheet on my phone, change the price, and it updates the website instantly.\nDavid Miller, Financial Consultant | Speed is everything for SEO. My old site took 4 seconds to load. My new Titan site loads in 0.1 seconds. My Google ranking jumped to Page 1 within a month.", height=100)
    
    faq_data = st.text_area("FAQ Data (Q? ? A)", "Do I really pay $0 for hosting? ? Yes. We utilize 'Static Site Architecture' which allows your site to be hosted on Enterprise CDNs (like Netlify/Vercel) within their generous free tiers for small businesses.\nWhat about my Domain Name? ? You pay that directly to the registrar (like GoDaddy or Namecheap). It usually costs ~$15/year. We do not mark this up.\nCan I add a blog later? ? Yes. The Titan Engine is scalable. We can add a blog, gallery, or more pages for a one-time expansion fee.\nIs it secure? ? It is safer than WordPress. Because there is no database to hack, your site is virtually impenetrable to common SQL injection attacks.", height=100)
    
    l1, l2 = st.columns(2)
    priv_txt = l1.text_area("Privacy Policy Text", "**1. Introduction & Digital Sovereignty**\nAt StopWebRent.com (operated by Kaydiem Script Lab), we treat data privacy not just as a compliance requirement, but as a fundamental architectural feature. We collect the absolute minimum amount of data required to engineer, deploy, and maintain your digital asset. This Privacy Policy outlines how we handle your information under the jurisdiction of West Bengal, India, while respecting global standards.\n\n**2. Information We Collect**\nTo provide our Titan Engine services, we collect Identity Data, Contact Data, and Technical Data (your Google Sheet ID).\n\n**3. The Static Site Privacy Advantage**\nUnlike traditional WordPress sites that store user data in complex databases (vulnerable to hacking), the websites we build for you are Static. They do not inherently store your customers data on our servers. This Zero-DB Architecture inherently reduces your liability and privacy risk.", height=200)
    term_txt = l2.text_area("Terms of Service Text", "**1. Service Agreement**\nBy engaging StopWebRent.com (Kaydiem Script Lab) for web development services, you agree to these Terms. We provide Static Website Architecture designed for speed and cost-efficiency.\n\n**2. Payment & Fees**\nYou agree to pay the one-time architectural setup fee (e.g., $199) as advertised. StopWebRent.com does not charge monthly maintenance or hosting fees. The Client is responsible for their own Domain Name renewal fees.\n\n**3. Intellectual Property (The Ownership Clause)**\nUpon settlement of the final invoice, full intellectual property rights and source code ownership are transferred to the Client. You are granted a perpetual, worldwide, non-exclusive license to the code.", height=200)

# --- 5. COMPILER ENGINE ---

def format_text(text):
    """Advanced Text Formatter v30.4"""
    if not text: return ""
    processed_text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    lines = processed_text.split('\n')
    html_out = ""
    in_list = False
    
    for line in lines:
        clean_line = line.strip()
        if not clean_line: continue
        if clean_line.startswith("* "):
            if not in_list:
                html_out += '<ul style="margin-bottom:1rem; padding-left:1.5rem;">'
                in_list = True
            content = clean_line[2:] 
            html_out += f'<li style="margin-bottom:0.5rem; opacity:0.9; color:inherit;">{content}</li>'
        elif clean_line.startswith("<strong>") and clean_line.endswith("</strong>"):
            if in_list: 
                html_out += "</ul>"
                in_list = False
            header_text = clean_line.replace("<strong>", "").replace("</strong>", "")
            html_out += f"<h3 style='margin-top:1.5rem; margin-bottom:0.5rem; color:var(--p); font-size:1.25rem;'>{header_text}</h3>"
        else:
            if in_list: 
                html_out += "</ul>"
                in_list = False
            html_out += f"<p style='margin-bottom:1rem; opacity:0.9; color:inherit;'>{clean_line}</p>"
    if in_list: html_out += "</ul>"
    return html_out

def gen_schema():
    schema = {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "name": biz_name,
        "image": logo_url or hero_img_1,
        "telephone": biz_phone,
        "email": biz_email,
        "areaServed": seo_area,
        "address": {
            "@type": "PostalAddress",
            "streetAddress": biz_addr
        },
        "url": prod_url,
        "description": seo_d
    }
    return f'<script type="application/ld+json">{json.dumps(schema)}</script>'

def get_theme_css():
    # Base Defaults
    bg_color = "#ffffff"
    text_color = "#0f172a"
    card_bg = "#ffffff"
    glass_nav = "rgba(255, 255, 255, 0.95)"
    
    # Theme Logic
    if "Midnight" in theme_mode:
        bg_color, text_color, card_bg, glass_nav = "#0f172a", "#f8fafc", "#1e293b", "rgba(15, 23, 42, 0.9)"
    elif "Cyberpunk" in theme_mode:
        bg_color, text_color, card_bg, glass_nav = "#050505", "#00ff9d", "#111", "rgba(0,0,0,0.8)"
    elif "Luxury" in theme_mode:
        bg_color, text_color, card_bg, glass_nav = "#1c1c1c", "#D4AF37", "#2a2a2a", "rgba(28,28,28,0.95)"
    elif "Forest" in theme_mode:
        bg_color, text_color, card_bg, glass_nav = "#f1f8e9", "#1b5e20", "#ffffff", "rgba(241,248,233,0.9)"
    elif "Ocean" in theme_mode:
        bg_color, text_color, card_bg, glass_nav = "#e0f7fa", "#006064", "#ffffff", "rgba(224,247,250,0.9)"
    elif "Stark" in theme_mode:
        bg_color, text_color, card_bg, glass_nav = "#ffffff", "#000000", "#ffffff", "rgba(255,255,255,1)"

    anim_css = ""
    if anim_type == "Fade Up":
        anim_css = ".reveal { opacity: 0; transform: translateY(30px); transition: all 0.8s ease-out; } .reveal.active { opacity: 1; transform: translateY(0); }"
    elif anim_type == "Zoom In":
        anim_css = ".reveal { opacity: 0; transform: scale(0.95); transition: all 0.8s cubic-bezier(0.175, 0.885, 0.32, 1.275); } .reveal.active { opacity: 1; transform: scale(1); }"
    
    # Hero Carousel CSS
    hero_css = """
    .hero { position: relative; min-height: 90vh; overflow: hidden; display: flex; align-items: center; justify-content: center; text-align: center; color: white; padding-top: 80px; background-color: var(--p); }
    .carousel-slide { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background-size: cover; background-position: center; opacity: 0; transition: opacity 1.5s ease-in-out; z-index: 0; }
    .carousel-slide.active { opacity: 1; }
    .hero-overlay { background: rgba(0,0,0,0.5); position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 1; }
    .hero-content { z-index: 2; position: relative; animation: slideUp 1s ease-out; }
    @keyframes slideUp { from { opacity:0; transform: translateY(30px); } to { opacity:1; transform: translateY(0); } }
    """

    return f"""
    :root {{
        --p: {p_color}; --s: {s_color}; --bg: {bg_color}; --txt: {text_color}; --card: {card_bg};
        --radius: {border_rad}; --nav: {glass_nav};
        --h-font: '{h_font}', sans-serif; --b-font: '{b_font}', sans-serif;
    }}
    * {{ box-sizing: border-box; }}
    html {{ scroll-behavior: smooth; }}
    body {{ background-color: var(--bg); color: var(--txt); font-family: var(--b-font); margin: 0; line-height: 1.6; overflow-x: hidden; }}
    
    p, h1, h2, h3, h4, h5, h6, span, li, div {{ color: inherit; }}
    .legal-text {{ color: var(--txt) !important; }}
    
    h1, h2, h3, h4 {{ font-family: var(--h-font); color: var(--p); line-height: 1.1; margin-bottom: 1rem; }}
    strong {{ color: var(--p); font-weight: 800; }}
    
    input, textarea, select {{ width: 100%; padding: 0.8rem; margin-bottom: 1rem; border: 1px solid #ccc; border-radius: 6px; font-family: inherit; }}
    label {{ color: var(--txt); font-weight: bold; margin-bottom: 0.5rem; display: block; }}

    .container {{ max-width: 1280px; margin: 0 auto; padding: 0 20px; }}
    .btn {{ display: inline-block; padding: 1rem 2.5rem; border-radius: var(--radius); font-weight: 700; text-decoration: none; transition: 0.3s; text-transform: uppercase; letter-spacing: 0.5px; cursor: pointer; border: none; text-align: center; }}
    .btn-primary {{ background: var(--p); color: white !important; }}
    .btn-accent {{ background: var(--s); color: white !important; box-shadow: 0 10px 25px -5px var(--s); }}
    .btn:hover {{ transform: translateY(-3px); filter: brightness(1.15); }}
    
    /* Nav */
    nav {{ position: fixed; top: 0; width: 100%; z-index: 1000; background: var(--nav); backdrop-filter: blur(12px); border-bottom: 1px solid rgba(100,100,100,0.1); padding: 1rem 0; }}
    .nav-flex {{ display: flex; justify-content: space-between; align-items: center; }}
    .nav-links {{ display: flex; align-items: center; }}
    .nav-links a {{ margin-left: 2rem; text-decoration: none; font-weight: 600; color: var(--txt); font-size: 0.9rem; opacity: 0.8; transition:0.2s; }}
    .nav-links a:hover {{ opacity: 1; color: var(--s); }}
    .mobile-menu {{ display: none; font-size: 1.5rem; cursor: pointer; }}
    
    {hero_css}
    .hero h1 {{ color: white; font-size: clamp(2.5rem, 8vw, 5rem); margin-bottom: 1.5rem; }}
    .hero p {{ color: rgba(255,255,255,0.9); font-size: clamp(1.1rem, 2vw, 1.5rem); max-width: 700px; margin: 0 auto 2.5rem auto; }}
    
    section {{ padding: 5rem 0; }}
    .section-head {{ text-align: center; margin-bottom: 4rem; }}
    .section-head h2 {{ font-size: 2.5rem; }}
    
    /* GRIDS */
    .grid-3 {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem; }}
    .about-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 4rem; align-items: center; }}
    
    /* CONTACT PAGE GRID (MOBILE FIXED) */
    .contact-grid {{ display: grid; grid-template-columns: 1fr 2fr; gap: 3rem; }}
    
    .card {{ background: var(--card); padding: 2rem; border-radius: var(--radius); border: 1px solid rgba(100,100,100,0.1); transition: 0.3s; height: 100%; display: flex; flex-direction: column; }}
    .card:hover {{ transform: translateY(-5px); box-shadow: 0 20px 40px -10px rgba(0,0,0,0.1); border-color: var(--s); }}
    
    .prod-img {{ width: 100%; height: 250px; object-fit: cover; border-radius: calc(var(--radius) - 4px); margin-bottom: 1.5rem; background: #f1f5f9; }}
    
    /* PRICING TABLE */
    .pricing-wrapper {{ overflow-x: auto; margin: 2rem 0; }}
    .pricing-table {{ width: 100%; border-collapse: collapse; min-width: 600px; }}
    .pricing-table th {{ background: var(--p); color: white; padding: 1.5rem; text-align: left; font-size: 1.1rem; }}
    .pricing-table td {{ padding: 1.5rem; border-bottom: 1px solid rgba(100,100,100,0.1); background: var(--card); color: var(--txt); }}
    .pricing-table tr:last-child td {{ font-weight: bold; font-size: 1.2rem; background: rgba(var(--s), 0.1); border-bottom: none; }}

    /* FAQ */
    details {{ background: var(--card); border: 1px solid rgba(100,100,100,0.1); border-radius: 8px; margin-bottom: 1rem; padding: 1rem; cursor: pointer; color: var(--txt); }}
    details summary {{ font-weight: bold; font-size: 1.1rem; color: var(--txt); }}
    details p {{ margin-top: 1rem; margin-bottom: 0; opacity: 0.9; color: var(--txt); }}

    /* Footer & Social */
    footer {{ background: var(--p); color: white; padding: 4rem 0; margin-top: auto; }}
    .footer-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 3rem; }}
    .footer a, footer a {{ color: rgba(255,255,255,0.8) !important; text-decoration: none; display: block; margin-bottom: 0.5rem; transition: 0.3s; }}
    .footer a:hover, footer a:hover {{ color: #ffffff !important; text-decoration: underline; }}
    .social-icon {{ width: 24px; height: 24px; fill: rgba(255,255,255,0.7); transition: 0.3s; }}
    .social-icon:hover {{ fill: #ffffff; transform: scale(1.1); }}

    /* Detail View */
    .detail-view {{ display: grid; grid-template-columns: 1fr 1fr; gap: 4rem; align-items: start; }}
    
    /* BLOG STYLES */
    .blog-badge {{ background: var(--s); color: white; padding: 0.3rem 0.8rem; border-radius: 50px; font-size: 0.75rem; text-transform: uppercase; font-weight: bold; width: fit-content; margin-bottom: 1rem; display:inline-block; }}
    .article-content ul {{ padding-left: 1.5rem; margin-bottom: 1.5rem; }}
    .article-content li {{ margin-bottom: 0.5rem; }}
    .article-content p {{ margin-bottom: 1.5rem; font-size: 1.1rem; opacity: 0.9; line-height: 1.8; }}
    
    /* SOCIAL SHARE BAR STYLES (NEW) */
    .share-row {{ display: flex; gap: 0.8rem; margin-top: 2rem; align-items: center; flex-wrap: wrap; }}
    .share-label {{ font-weight: bold; margin-right: 0.5rem; font-size: 0.9rem; opacity: 0.8; }}
    .share-btn {{ width: 40px; height: 40px; display: flex; align-items: center; justify-content: center; border-radius: 50%; color: white; transition: 0.3s; border: none; cursor: pointer; text-decoration: none; }}
    .share-btn:hover {{ transform: translateY(-3px); filter: brightness(1.1); }}
    .share-btn svg {{ width: 18px; height: 18px; fill: white; }}
    .bg-fb {{ background: #1877F2; }}
    .bg-x {{ background: #000000; }}
    .bg-li {{ background: #0A66C2; }}
    .bg-link {{ background: #64748b; }}
    
    {anim_css}
    
    /* MOBILE OPTIMIZATIONS */
    @media (max-width: 768px) {{
        .nav-links {{ 
            position: fixed; top: 70px; left: -100%; width: 100%; height: calc(100vh - 70px); 
            background: var(--bg); flex-direction: column; padding: 2rem; transition: 0.3s; 
            align-items: flex-start; justify-content: flex-start;
            border-top: 1px solid rgba(0,0,0,0.1);
        }}
        .nav-links.active {{ left: 0; }}
        .nav-links a {{ margin-left: 0; margin-bottom: 1.5rem; font-size: 1.1rem; }}
        .mobile-menu {{ display: block; }}
        
        .hero {{ min-height: 70vh; }}
        .about-grid {{ grid-template-columns: 1fr !important; gap: 2rem; text-align: left; }}
        .about-grid img {{ order: 2; margin-top: 1rem; }}
        .about-grid div {{ order: 1; }}
        
        /* FIX: FORCE CONTACT GRID TO 1 COLUMN ON MOBILE */
        .contact-grid {{ grid-template-columns: 1fr; gap: 2rem; }}
        .detail-view {{ grid-template-columns: 1fr; gap: 2rem; }}
    }}
    """

def gen_nav():
    logo_display = f'<img src="{logo_url}" height="40" alt="{biz_name} Logo">' if logo_url else f'<span style="font-weight:900; font-size:1.5rem; color:var(--p)">{biz_name}</span>'
    blog_link = '<a href="blog.html" onclick="document.querySelector(\'.nav-links\').classList.remove(\'active\')">Blog</a>' if show_blog else ''
    
    return f"""
    <nav><div class="container nav-flex">
        <a href="index.html" style="text-decoration:none">{logo_display}</a>
        <div class="mobile-menu" onclick="document.querySelector('.nav-links').classList.toggle('active')">☰</div>
        <div class="nav-links">
            <a href="index.html" onclick="document.querySelector('.nav-links').classList.remove('active')">Home</a>
            {'<a href="index.html#features" onclick="document.querySelector(\'.nav-links\').classList.remove(\'active\')">Features</a>' if show_features else ''}
            {'<a href="index.html#pricing" onclick="document.querySelector(\'.nav-links\').classList.remove(\'active\')">Savings</a>' if show_pricing else ''}
            {'<a href="index.html#inventory" onclick="document.querySelector(\'.nav-links\').classList.remove(\'active\')">Portfolio</a>' if show_inventory else ''}
            {blog_link}
            <a href="about.html" onclick="document.querySelector('.nav-links').classList.remove('active')">About</a>
            <a href="contact.html" onclick="document.querySelector('.nav-links').classList.remove('active')">Contact</a>
            <a href="tel:{biz_phone}" class="btn-accent" style="padding:0.6rem 1.5rem; margin-left:1.5rem; margin-bottom:0; border-radius:50px; color:white !important;">Call Now</a>
        </div>
    </div></nav>
    """

def gen_hero():
    return f"""
    <section class="hero">
        <div class="hero-overlay"></div>
        <div class="carousel-slide active" style="background-image: url('{hero_img_1}')"></div>
        <div class="carousel-slide" style="background-image: url('{hero_img_2}')"></div>
        <div class="carousel-slide" style="background-image: url('{hero_img_3}')"></div>
        
        <div class="container hero-content">
            <h1>{hero_h}</h1>
            <p>{hero_sub}</p>
            <div style="display:flex; gap:1rem; justify-content:center; flex-wrap:wrap;">
                <a href="#inventory" class="btn btn-accent">Explore Now</a>
                <a href="contact.html" class="btn" style="background:rgba(255,255,255,0.2); backdrop-filter:blur(10px); color:white;">Contact Us</a>
            </div>
        </div>
    </section>
    <script>
        let slides = document.querySelectorAll('.carousel-slide');
        let currentSlide = 0;
        setInterval(() => {{
            slides[currentSlide].classList.remove('active');
            currentSlide = (currentSlide + 1) % slides.length;
            slides[currentSlide].classList.add('active');
        }}, 4000);
    </script>
    """

def get_simple_icon(name):
    name = name.lower().strip()
    if "code" in name: return '<svg viewBox="0 0 24 24" width="32" height="32" fill="currentColor"><path d="M9.4 16.6L4.8 12l4.6-4.6L8 6l-6 6 6 6 1.4-1.4zm5.2 0l4.6-4.6-4.6-4.6L16 6l6 6-6 6-1.4-1.4z"/></svg>'
    if "database" in name: return '<svg viewBox="0 0 24 24" width="32" height="32" fill="currentColor"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z"/></svg>'
    if "layers" in name: return '<svg viewBox="0 0 24 24" width="32" height="32" fill="currentColor"><path d="M11.99 18.54l-7.37-5.73L3 14.07l9 7 9-7-1.63-1.27-7.38 5.74zM12 16l7.36-5.73L21 9l-9-7-9 7 1.63 1.27L12 16z"/></svg>'
    if "truck" in name or "logistics" in name: return '<svg viewBox="0 0 24 24" width="32" height="32" fill="currentColor"><path d="M20 8h-3V4H3c-1.1 0-2 .9-2 2v11h2c0 1.66 1.34 3 3 3s3-1.34 3-3h6c0 1.66 1.34 3 3 3s3-1.34 3-3h2v-5l-3-4zM6 18.5c-.83 0-1.5-.67-1.5-1.5s.67-1.5 1.5-1.5 1.5.67 1.5 1.5-.67 1.5-1.5 1.5zm13.5-9l1.96 2.5H17V9.5h2.5zm-1.5 9c-.83 0-1.5-.67-1.5-1.5s.67-1.5 1.5-1.5 1.5.67 1.5 1.5-.67 1.5-1.5 1.5z"/></svg>'
    if "shield" in name or "secure" in name: return '<svg viewBox="0 0 24 24" width="32" height="32" fill="currentColor"><path d="M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4zm0 10.99h7c-.53 4.12-3.28 7.79-7 8.94V12H5V6.3l7-3.11v8.8z"/></svg>'
    if "hammer" in name or "build" in name: return '<svg viewBox="0 0 24 24" width="32" height="32" fill="currentColor"><path d="M22.11 11.26l-1.41-1.41c-.55-.56-1.43-.6-2.03-.1L15 6.6V3c0-.55-.45-1-1-1H9c-.55 0-1 .45-1 1v7h2v-2h2v4l-6.88 5.73c-.78.65-1.95.65-2.73 0-.78-.65-.78-1.71 0-2.36L8.53 10.2l-1.27-1.27c-.78-.78-.78-2.05 0-2.83.78-.78 2.05-.78 2.83 0l1.27 1.27 5.14-4.28c.15-.12.33-.19.51-.19.18 0 .37.07.51.19l1.41 1.41c.29.29.29.77 0 1.06L14 10.53l6.59 5.49c1.56-1.56 1.56-4.09 1.52-4.76z"/></svg>'
    if "water" in name or "plumb" in name or "drop" in name: return '<svg viewBox="0 0 24 24" width="32" height="32" fill="currentColor"><path d="M12 22c4.97 0 9-4.03 9-9 0-4.97-9-13-9-13S3 8.03 3 13c0 4.97 4.03 9 9 9zm0-11c1.66 0 3 1.34 3 3s-1.34 3-3 3-3-1.34-3-3 1.34-3 3-3z"/></svg>'
    if "home" in name or "roof" in name: return '<svg viewBox="0 0 24 24" width="32" height="32" fill="currentColor"><path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z"/></svg>'
    if "bolt" in name or "electric" in name: return '<svg viewBox="0 0 24 24" width="32" height="32" fill="currentColor"><path d="M11 21h-1l1-7H7.5c-.58 0-.57-.32-.38-.66.19-.34.05-.08.07-.12C8.48 10.94 10.42 7.54 13 3h1l-1 7h3.5c.49 0 .56.33.47.51l-.07.15C12.96 17.55 11 21 11 21z"/></svg>'
    if "star" in name: return '<svg viewBox="0 0 24 24" width="32" height="32" fill="currentColor"><path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/></svg>'
    if "heart" in name: return '<svg viewBox="0 0 24 24" width="32" height="32" fill="currentColor"><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/></svg>'
    if "wallet" in name: return '<svg viewBox="0 0 24 24" width="32" height="32" fill="currentColor"><path d="M21 18v1c0 1.1-.9 2-2 2H5c-1.11 0-2-.9-2-2V5c0-1.1.89-2 2-2h14c1.1 0 2 .9 2 2v1h-9c-1.11 0-2 .9-2 2v8c0 1.1.89 2 2 2h9zm-9-2h10V8H12v8zm4-2.5c-.83 0-1.5-.67-1.5-1.5s.67-1.5 1.5-1.5 1.5.67 1.5 1.5-.67 1.5-1.5 1.5z"/></svg>'
    if "table" in name: return '<svg viewBox="0 0 24 24" width="32" height="32" fill="currentColor"><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zM5 19V5h14v14H5zm2-2h10v-2H7v2zm0-4h10v-2H7v2zm0-4h10V7H7v2z"/></svg>'
    return '<svg viewBox="0 0 24 24" width="32" height="32" fill="currentColor"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/></svg>'

def gen_features():
    cards = ""
    lines = [x for x in feat_data.split('\n') if x.strip()]
    for line in lines:
        if "|" in line:
            parts = line.split('|')
            if len(parts) >= 3:
                icon_code = get_simple_icon(parts[0])
                title = parts[1].strip()
                desc = parts[2].strip()
                cards += f"""<div class="card reveal"><div style="color:var(--s); margin-bottom:1rem;">{icon_code}</div><h3 style="color:var(--p); font-size:1.2rem; text-transform:uppercase; letter-spacing:1px;">{title}</h3><div style="opacity:0.9; color:var(--txt); font-size:0.95rem;">{format_text(desc)}</div></div>"""
            elif len(parts) == 2:
                title = parts[0].strip()
                desc = parts[1].strip()
                cards += f"""<div class="card reveal"><h3 style="color:var(--s); font-size:1.2rem; text-transform:uppercase; letter-spacing:1px;">{title}</h3><div style="opacity:0.9; color:var(--txt); font-size:0.95rem;">{format_text(desc)}</div></div>"""
    return f"""<section id="features"><div class="container"><div class="section-head reveal"><h2>{f_title}</h2></div><div class="grid-3">{cards}</div></div></section>"""

def gen_stats():
    return f"""
    <div style="background:var(--p); color:white; padding:3rem 0; text-align:center;">
        <div class="container grid-3">
            <div class="reveal">
                <h3 style="color:#ffffff; margin:0; font-size:3rem;">{stat_1}</h3>
                <p style="color:rgba(255,255,255,0.8); margin:0;">{label_1}</p>
            </div>
            <div class="reveal">
                <h3 style="color:#ffffff; margin:0; font-size:3rem;">{stat_2}</h3>
                <p style="color:rgba(255,255,255,0.8); margin:0;">{label_2}</p>
            </div>
            <div class="reveal">
                <h3 style="color:#ffffff; margin:0; font-size:3rem;">{stat_3}</h3>
                <p style="color:rgba(255,255,255,0.8); margin:0;">{label_3}</p>
            </div>
        </div>
    </div>
    """

def gen_pricing_table():
    if not show_pricing: return ""
    return f"""
    <section id="pricing"><div class="container">
        <div class="section-head reveal"><h2>The Cost of Ownership</h2><p>See how the "Monthly Trap" adds up over 5 years.</p></div>
        <div class="pricing-wrapper reveal">
            <table class="pricing-table">
                <thead>
                    <tr><th style="width:40%">Expense Category</th><th style="background:var(--s); font-size:1.2rem;">Titan Engine (Us)</th><th>{wix_name}</th><th>Standard Agency</th></tr>
                </thead>
                <tbody>
                    <tr><td>Initial Setup Fee</td><td><strong>{titan_price}</strong> (One-time)</td><td>$0 (DIY)</td><td>$2,000+</td></tr>
                    <tr><td>Annual Hosting Costs</td><td><strong>{titan_mo}</strong></td><td>{wix_mo} ($348/yr)</td><td>$600/yr</td></tr>
                    <tr><td>SSL & Security</td><td>$0 (Included)</td><td>$0 (Included)</td><td>$100/yr</td></tr>
                    <tr><td><strong>Your 5-Year Savings</strong></td><td style="color:var(--s); font-size:1.3rem;">You Save {save_val}</td><td>$0</td><td>$0</td></tr>
                </tbody>
            </table>
        </div>
        <p style="text-align:center; font-size:0.8rem; opacity:0.6; margin-top:1rem;">*Comparison pricing based on standard public rates. Titan Engine is not affiliated with competitor trademarks.</p>
    </div></section>
    """

def gen_csv_parser():
    return """
    <script>
    function parseCSVLine(str) {
        const res = [];
        let cur = '';
        let inQuote = false;
        for (let i = 0; i < str.length; i++) {
            const c = str[i];
            if (c === '"') {
                if (inQuote && str[i+1] === '"') { cur += '"'; i++; }
                else { inQuote = !inQuote; }
            } else if (c === ',' && !inQuote) {
                res.push(cur.trim()); cur = '';
            } else { cur += c; }
        }
        res.push(cur.trim());
        return res;
    }
    // Markdown Parser
    function parseMarkdown(text) {
        if (!text) return '';
        let html = text
            .replace(/\\r\\n/g, '\\n')
            .replace(/\\n/g, '<br>')
            .replace(/\\*\\*(.*?)\\*\\*/g, '<strong>$1</strong>')
            .replace(/\\*(.*?)\\*/g, '<em>$1</em>');
        
        if (html.includes('* ')) {
            const lines = html.split('<br>');
            let inList = false;
            let finalHtml = '';
            lines.forEach(line => {
                if (line.trim().startsWith('* ')) {
                    if (!inList) { finalHtml += '<ul>'; inList = true; }
                    finalHtml += '<li>' + line.trim().substring(2) + '</li>';
                } else {
                    if (inList) { finalHtml += '</ul>'; inList = false; }
                    finalHtml += line + '<br>';
                }
            });
            if (inList) finalHtml += '</ul>';
            return finalHtml;
        }
        return html;
    }
    </script>
    """

def gen_inventory_js(is_demo=False):
    demo_flag = "const isDemo = true;" if is_demo else "const isDemo = false;"
    
    return f"""
    {gen_csv_parser()}
    <script>
    {demo_flag}
    
    async function loadInv() {{
        try {{
            const res = await fetch('{sheet_url}');
            const txt = await res.text();
            const lines = txt.split(/\\r\\n|\\n/);
            const box = document.getElementById('inv-grid');
            if(!box) return;
            box.innerHTML = '';
            for(let i=1; i<lines.length; i++) {{
                if(!lines[i].trim()) continue;
                const clean = parseCSVLine(lines[i]);
                let img = clean[3] && clean[3].length > 5 ? clean[3] : '{custom_feat}'; 
                if(clean[6] && clean[6].length > 5) img = clean[6];
                if(clean.length > 1) {{
                    const prodName = encodeURIComponent(clean[0]);
                    box.innerHTML += `
                    <div class="card reveal" style="color: var(--txt);">
                        <img src="${{img}}" class="prod-img" loading="lazy" alt="${{clean[0]}}" onerror="this.onerror=null;this.src='{custom_feat}';">
                        <div style="flex-grow:1; display:flex; flex-direction:column; justify-content:space-between;">
                            <div>
                                <h3 style="color:var(--p);">${{clean[0]}}</h3>
                                <p style="font-weight:bold; color:var(--s); font-size:1.1rem;">${{clean[1]}}</p>
                                <p style="font-size:0.9rem; opacity:0.9; margin-bottom:1rem; color:var(--txt);">${{clean[2] ? clean[2].substring(0,60)+'...' : ''}}</p>
                            </div>
                            <div style="display:grid; grid-template-columns:1fr 1fr; gap:0.5rem;">
                                <a href="product.html?item=${{prodName}}" class="btn" style="background:#e2e8f0; color:#0f172a !important; padding:0.8rem; font-size:0.8rem;">View Details</a>
                                <a href="https://wa.me/{wa_num}?text=I am interested in ${{prodName}}" target="_blank" class="btn-primary btn" style="padding:0.8rem; font-size:0.8rem;">WhatsApp</a>
                            </div>
                        </div>
                    </div>`;
                }}
            }}
        }} catch(e) {{ console.log(e); }}
    }}
    if(document.getElementById('inv-grid')) window.addEventListener('load', loadInv);
    </script>
    """

def gen_inventory():
    if not show_inventory: return ""
    return f"""
    <section id="inventory" style="background:rgba(0,0,0,0.02)"><div class="container">
        <div class="section-head reveal"><h2>Portfolio / Templates</h2><p>Choose a foundation. We customize it for you.</p></div>
        <div id="inv-grid" class="grid-3"><div style="grid-column:1/-1; text-align:center; padding:4rem; color:var(--s);">Loading Database...</div></div>
    </div></section>
    {gen_inventory_js(is_demo=False)}
    """

def gen_about_section():
    formatted_about = format_text(about_short)
    return f"""
    <section id="about"><div class="container">
        <div class="about-grid">
            <div class="reveal">
                <h2 style="font-size:2.5rem; margin-bottom:1.5rem;">{about_h}</h2>
                <div style="font-size:1.1rem; opacity:0.9; margin-bottom:2rem; color:var(--txt);">{formatted_about}</div>
                <a href="about.html" class="btn btn-primary" style="padding: 0.8rem 2rem; font-size:0.9rem;">Read Our Full Story</a>
            </div>
            <img src="{about_img}" class="reveal" loading="lazy" alt="About {biz_name}" style="width:100%; border-radius:var(--radius); box-shadow:0 20px 50px -20px rgba(0,0,0,0.2); aspect-ratio:4/3; object-fit:cover;">
        </div>
    </div></section>
    """

def gen_faq_section():
    items = ""
    for line in faq_data.split('\n'):
        if "?" in line and not line.strip() == "":
            parts = line.split('?', 1)
            if len(parts) == 2:
                q = parts[0].strip() + "?"
                a = parts[1].replace("?", "").strip()
                items += f"<details class='reveal'><summary>{q}</summary><p>{a}</p></details>"
    return f"""<section id="faq" style="background:rgba(0,0,0,0.02)"><div class="container" style="max-width:800px;"><div class="section-head reveal"><h2>Frequently Asked Questions</h2></div>{items}</div></section>"""

def gen_footer():
    icons = ""
    if fb_link: icons += f'<a href="{fb_link}" target="_blank" aria-label="Facebook"><svg class="social-icon" viewBox="0 0 24 24"><path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"></path></svg></a>'
    if ig_link: icons += f'<a href="{ig_link}" target="_blank" aria-label="Instagram"><svg class="social-icon" viewBox="0 0 24 24"><path d="M16.98 0a6.9 6.9 0 0 1 5.08 1.98A6.94 6.94 0 0 1 24 7.02v9.96c0 2.08-.68 3.87-1.98 5.13A7.14 7.14 0 0 1 16.94 24H7.06a7.06 7.06 0 0 1-5.03-1.89A6.96 6.96 0 0 1 0 16.94V7.02C0 2.8 2.8 0 7.02 0h9.96zM7.17 2.1c-1.4 0-2.6.48-3.46 1.33c-.85.85-1.33 2.06-1.33 3.46v10.3c0 1.3.47 2.5 1.33 3.36c.86.85 2.06 1.33 3.46 1.33h9.66c1.4 0 2.6-.48 3.46-1.33c.85-.85 1.33-2.06 1.33-3.46V6.89c0-1.4-.47-2.6-1.33-3.46c-.86-.85-2.06-1.33-3.46-1.33H7.17zm11.97 3.33c.77 0 1.4.63 1.4 1.4c0 .77-.63 1.4-1.4 1.4c-.77 0-1.4-.63-1.4-1.4c0-.77.63-1.4 1.4-1.4zM12 5.76c3.39 0 6.14 2.75 6.14 6.14c0 3.39-2.75 6.14-6.14 6.14c-3.39 0-6.14-2.75-6.14-6.14c0-3.39 2.75-6.14 6.14-6.14zm0 2.1c-2.2 0-3.99 1.79-3.99 4.04c0 2.25 1.79 4.04 3.99 4.04c2.2 0 3.99-1.79 3.99-4.04c0-2.25-1.79-4.04-3.99-4.04c0-2.25-1.79-4.04-3.99-4.04c0-2.25-1.79-4.04-3.99-4.04c0-2.25-1.79-4.04-3.99-4.04c0-2.25-1.79-4.04-3.99-4.04z"/></svg></a>'
    if x_link: icons += f'<a href="{x_link}" target="_blank" aria-label="X (Twitter)"><svg class="social-icon" viewBox="0 0 24 24"><path d="M18.901 1.153h3.68l-8.04 9.19L24 22.846h-7.406l-5.8-7.584l-6.638 7.584H.474l8.6-9.83L0 1.154h7.594l5.243 6.932ZM17.61 20.644h2.039L6.486 3.24H4.298Z"></path></svg></a>'
    if li_link: icons += f'<a href="{li_link}" target="_blank" aria-label="LinkedIn"><svg class="social-icon" viewBox="0 0 24 24"><path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2a2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6zM2 9h4v12H2zM4 2a2 2 0 1 1-2 2a2 2 0 0 1 2-2z"></path></svg></a>'
    if yt_link: icons += f'<a href="{yt_link}" target="_blank" aria-label="YouTube"><svg class="social-icon" viewBox="0 0 24 24"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg></a>'

    return f"""
    <footer><div class="container">
        <div class="footer-grid">
            <div>
                <h3 style="color:white; margin-bottom:1.5rem;">{biz_name}</h3>
                <p style="opacity:0.8; font-size:0.9rem;">{biz_addr}</p>
                <p style="opacity:0.8; font-size:0.9rem; margin-top:1rem;">{biz_email}</p>
                <p style="opacity:0.6; font-size:0.8rem; margin-top:1rem;">Serving: {seo_area}</p>
                <div style="margin-top:1.5rem; display:flex; gap:1.2rem; align-items:center;">
                    {icons}
                </div>
            </div>
            <div>
                <h4 style="color:white; font-size:0.9rem; text-transform:uppercase; letter-spacing:1px; margin-bottom:1.5rem;">Explore</h4>
                <a href="index.html">Home</a>
                <a href="blog.html">Blog</a>
                <a href="about.html">About Us</a>
                <a href="contact.html">Contact</a>
            </div>
            <div>
                <h4 style="color:white; font-size:0.9rem; text-transform:uppercase; letter-spacing:1px; margin-bottom:1.5rem;">Legal</h4>
                <a href="privacy.html">Privacy Policy</a>
                <a href="terms.html">Terms of Service</a>
            </div>
        </div>
        <div style="border-top:1px solid rgba(255,255,255,0.1); margin-top:3rem; padding-top:2rem; text-align:center; opacity:0.4; font-size:0.8rem;">
            &copy; <a href="https://www.kaydiemscriptlab.com/" target="_blank" style="display:inline; color:white;">Kaydiem Script Lab</a>. Powered by Titan Engine.
        </div>
    </div></footer>
    """

def gen_wa_widget():
    if not wa_num: return ""
    return f"""<a href="https://wa.me/{wa_num}" class="wa-float" target="_blank" aria-label="Chat on WhatsApp" style="position:fixed; bottom:30px; right:30px; background:#25d366; color:white; width:60px; height:60px; border-radius:50%; display:flex; align-items:center; justify-content:center; box-shadow:0 10px 30px rgba(37,211,102,0.4); z-index:9999;"><svg style="width:32px;height:32px" viewBox="0 0 24 24"><path fill="currentColor" d="M12.04 2c-5.46 0-9.91 4.45-9.91 9.91c0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38c1.45.79 3.08 1.21 4.74 1.21c5.46 0 9.91-4.45 9.91-9.91c0-2.65-1.03-5.14-2.9-7.01A9.816 9.816 0 0 0 12.04 2m.01 1.67c2.2 0 4.26.86 5.82 2.42a8.225 8.225 0 0 1 2.41 5.83c0 4.54-3.7 8.23-8.24 8.23c-1.48 0-2.93-.39-4.19-1.15l-.3-.17l-3.12.82l.83-3.04l-.2-.32a8.188 8.188 0 0 1-1.26-4.38c.01-4.54 3.7-8.24 8.25-8.24m-3.53 3.16c-.13 0-.35.05-.54.26c-.19.2-.72.7-.72 1.72s.73 2.01.83 2.14c.1.13 1.44 2.19 3.48 3.07c.49.21.87.33 1.16.43c.49.16.94.13 1.29.08c.4-.06 1.21-.5 1.38-.98c.17-.48.17-.89.12-.98c-.05-.09-.18-.13-.37-.23c-.19-.1-.1.13-.1.13s-1.13-.56-1.32-.66c-.19-.1-.32-.15-.45.05c-.13.2-.51.65-.62.78c-.11.13-.23.15-.42.05c-.19-.1-.8-.3-1.53-.94c-.57-.5-1.02-1.12-1.21-1.45c-.11-.19-.01-.29.09-.38c.09-.08.19-.23.29-.34c.1-.11.13-.19.19-.32c.06-.13.03-.24-.01-.34c-.05-.1-.45-1.08-.62-1.48c-.16-.4-.36-.34-.51-.35c-.11-.01-.25-.01-.4-.01Z"/></svg></a>"""

def gen_scripts():
    return """
    <script>
    window.addEventListener('scroll', () => {
        var reveals = document.querySelectorAll('.reveal');
        for (var i = 0; i < reveals.length; i++) {
            var windowHeight = window.innerHeight;
            var elementTop = reveals[i].getBoundingClientRect().top;
            var elementVisible = 150;
            if (elementTop < windowHeight - elementVisible) { reveals[i].classList.add('active'); }
        }
    });
    window.dispatchEvent(new Event('scroll'));
    </script>
    """

def build_page(title, content, extra_js=""):
    css = get_theme_css()
    meta_tags = f'<meta name="description" content="{seo_d}">'
    if gsc_tag: meta_tags += f'\n<meta name="google-site-verification" content="{gsc_tag}">'
    if og_image: meta_tags += f'\n<meta property="og:image" content="{og_image}">'
    
    analytics = ""
    if ga_tag:
        analytics = f"""<script async src="https://www.googletagmanager.com/gtag/js?id={ga_tag}"></script>
        <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','{ga_tag}');</script>"""

    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title} | {biz_name}</title>
        {meta_tags}
        {gen_schema()}
        <link href="https://fonts.googleapis.com/css2?family={h_font.replace(' ', '+')}:wght@400;700;900&family={b_font.replace(' ', '+')}:wght@300;400;600&display=swap" rel="stylesheet">
        <style>{css}</style>
        {analytics}
    </head>
    <body>
        {gen_nav()}
        {content}
        {gen_footer()}
        {gen_wa_widget()}
        {gen_scripts()}
        {extra_js}
    </body>
    </html>
    """

# --- 404 & PRODUCTS ---
def gen_404_content():
    return f"""<section class="hero" style="min-height:70vh;"><div class="container"><h1 style="font-size:6rem; margin:0;">404</h1><p>Page Not Found</p><br><a href="index.html" class="btn btn-accent">Return Home</a></div></section>"""

# --- MODIFIED: gen_product_page_content with Social Shares ---
def gen_product_page_content(is_demo=False):
    demo_flag = "const isDemo = true;" if is_demo else "const isDemo = false;"
    return f"""
    <section style="padding-top:150px;"><div class="container"><div id="product-detail" class="detail-view">
        <div style="background:#eee; height:400px; border-radius:12px;"></div><div>Loading...</div>
    </div></div></section>
    {gen_csv_parser()}
    <script>
    {demo_flag}
    function shareWA(url, title) {{ window.open('https://wa.me/?text=' + encodeURIComponent(title + ' ' + url), '_blank'); }}
    async function loadProduct() {{
        const params = new URLSearchParams(window.location.search);
        let targetName = params.get('item');
        if(isDemo && !targetName) targetName = "Demo Item";
        try {{
            const res = await fetch('{sheet_url}');
            const txt = await res.text();
            const lines = txt.split(/\\r\\n|\\n/);
            for(let i=1; i<lines.length; i++) {{
                const clean = parseCSVLine(lines[i]);
                if(isDemo) targetName = clean[0];
                if(clean[0] === targetName) {{
                    let img = clean[3] || '{custom_feat}';
                    const shareUrl = encodeURIComponent(window.location.href);
                    const shareTitle = encodeURIComponent(clean[0]);
                    
                    document.getElementById('product-detail').innerHTML = `
                        <img src="${{img}}" style="width:100%; border-radius:12px;">
                        <div>
                            <h1 style="font-size:3rem; line-height:1.1;">${{clean[0]}}</h1>
                            <p style="font-size:1.5rem; color:var(--s); font-weight:bold; margin-bottom:1.5rem;">${{clean[1]}}</p>
                            <p>${{clean[2]}}</p>
                            <button onclick="shareWA(window.location.href, '${{clean[0]}}')" class="btn btn-primary" style="width:100%; margin-top:2rem;">Share on WhatsApp</button>
                            
                            <!-- SOCIAL SHARE ROW -->
                            <div class="share-row">
                                <span class="share-label">Share This:</span>
                                <a href="https://www.facebook.com/sharer/sharer.php?u=${{shareUrl}}" target="_blank" class="share-btn bg-fb"><svg viewBox="0 0 24 24"><path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"></path></svg></a>
                                <a href="https://twitter.com/intent/tweet?url=${{shareUrl}}&text=${{shareTitle}}" target="_blank" class="share-btn bg-x"><svg viewBox="0 0 24 24"><path d="M18.901 1.153h3.68l-8.04 9.19L24 22.846h-7.406l-5.8-7.584l-6.638 7.584H.474l8.6-9.83L0 1.154h7.594l5.243 6.932ZM17.61 20.644h2.039L6.486 3.24H4.298Z"></path></svg></a>
                                <a href="https://www.linkedin.com/sharing/share-offsite/?url=${{shareUrl}}" target="_blank" class="share-btn bg-li"><svg viewBox="0 0 24 24"><path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2a2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6zM2 9h4v12H2zM4 2a2 2 0 1 1-2 2a2 2 0 0 1 2-2z"></path></svg></a>
                                <button onclick="navigator.clipboard.writeText(window.location.href);alert('Link Copied!')" class="share-btn bg-link" title="Copy Link"><svg viewBox="0 0 24 24"><path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"></path></svg></button>
                            </div>
                        </div>
                    `;
                    break;
                }}
            }}
        }} catch(e) {{}}
    }}
    loadProduct();
    </script>
    """

# --- BLOG GENERATION LOGIC ---
def gen_blog_index_html():
    return f"""
    <section class="hero" style="min-height:40vh; background-image: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('{hero_img_1}'); background-size: cover; background-position: center;">
        <div class="container"><h1>{blog_hero_title}</h1><p>{blog_hero_sub}</p></div>
    </section>
    <section>
        <div class="container">
            <div id="blog-grid" class="grid-3">
                <div style="text-align:center; grid-column:1/-1;">Loading Articles...</div>
            </div>
        </div>
    </section>
    {gen_csv_parser()}
    <script>
    async function loadBlog() {{
        try {{
            const res = await fetch('{blog_sheet_url}');
            const txt = await res.text();
            const lines = txt.split(/\\r\\n|\\n/);
            const box = document.getElementById('blog-grid');
            if(!box) return;
            box.innerHTML = '';
            for(let i=1; i<lines.length; i++) {{
                if(!lines[i].trim()) continue;
                const r = parseCSVLine(lines[i]);
                if(r.length > 4) {{
                    box.innerHTML += `
                    <div class="card reveal">
                        <img src="${{r[5] || '{hero_img_1}'}}" class="prod-img" alt="${{r[1]}}">
                        <div>
                            <span class="blog-badge">${{r[3]}}</span>
                            <span style="float:right; font-size:0.8rem; opacity:0.7;">${{r[2]}}</span>
                            <h3 style="margin-top:0.5rem; color:var(--p);"><a href="post.html?id=${{r[0]}}" style="text-decoration:none; color:inherit;">${{r[1]}}</a></h3>
                            <p style="font-size:0.95rem; opacity:0.8;">${{r[4]}}</p>
                            <a href="post.html?id=${{r[0]}}" style="color:var(--s); font-weight:bold; text-decoration:none;">Read Article &rarr;</a>
                        </div>
                    </div>`;
                }}
            }}
        }} catch(e) {{ console.log(e); }}
    }}
    window.addEventListener('load', loadBlog);
    </script>
    """

# --- MODIFIED: gen_blog_post_html with Social Shares ---
def gen_blog_post_html():
    return f"""
    <div id="post-container" style="padding-top:100px; min-height:60vh;">
        <div class="container" style="text-align:center; padding:5rem 0;">
            <h1>Loading Article...</h1>
        </div>
    </div>
    
    {gen_csv_parser()}
    <script>
    async function loadPost() {{
        const params = new URLSearchParams(window.location.search);
        const slug = params.get('id');
        if(!slug) {{ window.location.href = 'blog.html'; return; }}
        
        try {{
            const res = await fetch('{blog_sheet_url}');
            const txt = await res.text();
            const lines = txt.split(/\\r\\n|\\n/);
            const container = document.getElementById('post-container');
            
            let found = false;
            for(let i=1; i<lines.length; i++) {{
                const r = parseCSVLine(lines[i]);
                if(r[0] === slug) {{
                    found = true;
                    document.title = r[1] + " | {biz_name}";
                    const contentHtml = parseMarkdown(r[6]);
                    
                    const shareUrl = encodeURIComponent(window.location.href);
                    const shareTitle = encodeURIComponent(r[1]);
                    
                    container.innerHTML = `
                        <div style="background:var(--p); padding:6rem 0 4rem 0; color:white; text-align:center;">
                            <div class="container">
                                <span class="blog-badge" style="background:rgba(255,255,255,0.2); margin-bottom:1rem; display:inline-block;">${{r[3]}}</span>
                                <h1 style="font-size:clamp(2rem, 5vw, 3.5rem); margin-bottom:1rem; color:white;">${{r[1]}}</h1>
                                <p style="opacity:0.8;">Published on ${{r[2]}}</p>
                            </div>
                        </div>
                        <div class="container" style="max-width:800px; padding:4rem 1rem;">
                            <img src="${{r[5]}}" style="width:100%; border-radius:12px; margin-bottom:3rem; box-shadow:0 10px 30px rgba(0,0,0,0.1);">
                            <div class="article-content" style="line-height:1.8; color:var(--txt);">
                                ${{contentHtml}}
                            </div>
                            
                            <!-- SOCIAL SHARE ROW -->
                            <div class="share-row" style="margin-top:3rem; border-top:1px solid #eee; padding-top:2rem;">
                                <span class="share-label">Share Article:</span>
                                <a href="https://www.facebook.com/sharer/sharer.php?u=${{shareUrl}}" target="_blank" class="share-btn bg-fb"><svg viewBox="0 0 24 24"><path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"></path></svg></a>
                                <a href="https://twitter.com/intent/tweet?url=${{shareUrl}}&text=${{shareTitle}}" target="_blank" class="share-btn bg-x"><svg viewBox="0 0 24 24"><path d="M18.901 1.153h3.68l-8.04 9.19L24 22.846h-7.406l-5.8-7.584l-6.638 7.584H.474l8.6-9.83L0 1.154h7.594l5.243 6.932ZM17.61 20.644h2.039L6.486 3.24H4.298Z"></path></svg></a>
                                <a href="https://www.linkedin.com/sharing/share-offsite/?url=${{shareUrl}}" target="_blank" class="share-btn bg-li"><svg viewBox="0 0 24 24"><path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2a2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6zM2 9h4v12H2zM4 2a2 2 0 1 1-2 2a2 2 0 0 1 2-2z"></path></svg></a>
                                <button onclick="navigator.clipboard.writeText(window.location.href);alert('Link Copied!')" class="share-btn bg-link" title="Copy Link"><svg viewBox="0 0 24 24"><path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"></path></svg></button>
                            </div>

                            <hr style="margin:2rem 0; border:0; border-top:1px solid #eee;">
                            <a href="blog.html" class="btn btn-primary">&larr; Back to Blog</a>
                        </div>
                    `;
                    break;
                }}
            }}
            if(!found) container.innerHTML = '<div class="container" style="text-align:center; padding:5rem;"><h2>Article Not Found</h2><a href="blog.html" class="btn btn-primary">Back</a></div>';
            
        }} catch(e) {{ console.log(e); }}
    }}
    window.addEventListener('load', loadPost);
    </script>
    """

# --- 6. PAGE CONTENT GENERATION ---
home_content = ""
if show_hero: home_content += gen_hero()
if show_stats: home_content += gen_stats()
if show_features: home_content += gen_features()
if show_pricing: home_content += gen_pricing_table()
if show_inventory: home_content += gen_inventory()
if show_gallery: home_content += gen_about_section()
if show_testimonials: 
    t_cards = "".join([f'<div class="card reveal" style="text-align:center;"><i>"{x.split("|")[1]}"</i><br><br><b>- {x.split("|")[0]}</b></div>' for x in testi_data.split('\n') if "|" in x])
    home_content += f'<section style="background:#f8fafc"><div class="container"><div class="section-head reveal"><h2>Client Stories</h2></div><div class="grid-3">{t_cards}</div></div></section>'
if show_faq: home_content += gen_faq_section()
if show_cta: home_content += f'<section style="background:var(--s); color:white; text-align:center;"><div class="container reveal"><h2>Start Owning Your Future</h2><p style="margin-bottom:2rem;">Stop paying rent. Start building equity.</p><a href="contact.html" class="btn" style="background:white; color:var(--s);">Get Started</a></div></section>'

# --- 7. RENDER & DEPLOY ---
st.divider()
st.subheader("🚀 Launchpad")

preview_mode = st.radio("Preview Page:", ["Home", "About", "Contact", "Blog Index", "Blog Post (Demo)", "Privacy", "Terms", "Product Detail (Demo)"], horizontal=True)

# HELPER: Function to generate a header for inner pages with the image
def gen_inner_header(title):
    return f"""
    <section class="hero" style="min-height: 40vh; background-image: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('{hero_img_1}'); background-size: cover; background-position: center;">
        <div class="container">
            <h1 style="font-size: 3.5rem; margin-bottom: 0;">{title}</h1>
        </div>
    </section>
    """

# 1. GENERATE ABOUT PAGE CONTENT
about_body = format_text(about_long)
about_content = f"""{gen_inner_header("About Us")}<section><div class="container"><div class="about-grid"><div class="legal-text">{about_body}</div><img src="{about_img}" style="width:100%; border-radius:12px; box-shadow:0 10px 30px rgba(0,0,0,0.1);"></div></div></section>"""

# 2. GENERATE CONTACT PAGE CONTENT (FIXED MOBILE LAYOUT)
contact_content = f"""
{gen_inner_header("Contact Us")}
<section>
    <div class="container">
        <!-- FIXED: Class instead of inline style -->
        <div class="contact-grid">
            <div>
                <div style="background:var(--card); padding:2rem; border-radius:12px; border:1px solid #eee;">
                    <h3 style="color:var(--p);">Get In Touch</h3>
                    <p style="margin-top:1rem;"><strong>📍 Address:</strong><br>{biz_addr.replace(chr(10),'<br>')}</p>
                    <p style="margin-top:1rem;"><strong>📞 Phone:</strong><br><a href="tel:{biz_phone}" style="color:var(--s);">{biz_phone}</a></p>
                    <p style="margin-top:1rem;"><strong>📧 Email:</strong><br><a href="mailto:{biz_email}">{biz_email}</a></p>
                    <br>
                    <a href="https://wa.me/{wa_num}" target="_blank" class="btn btn-accent" style="width:100%; text-align:center;">Chat on WhatsApp</a>
                </div>
            </div>
            
            <div class="card">
                <h3 style="margin-bottom:1.5rem;">Send a Message</h3>
                <form action="https://formsubmit.co/{biz_email}" method="POST">
                    <div style="display:grid; grid-template-columns:1fr 1fr; gap:1rem;">
                        <div><label>Name</label><input type="text" name="name" required placeholder="Your Name"></div>
                        <div><label>Email</label><input type="email" name="email" required placeholder="Your Email"></div>
                    </div>
                    <label>Message</label><textarea name="message" rows="5" required placeholder="How can we help you?"></textarea>
                    <button type="submit" class="btn btn-primary" style="width:100%;">Send Message</button>
                    <input type="hidden" name="_captcha" value="false">
                    <input type="hidden" name="_next" value="{prod_url}/contact.html">
                </form>
            </div>
        </div>
        <br><br>
        <div style="border-radius:12px; overflow:hidden; box-shadow:0 10px 30px rgba(0,0,0,0.1);">{map_iframe}</div>
    </div>
</section>
"""

# 3. GENERATE LEGAL PAGES
privacy_content = f'{gen_inner_header("Privacy Policy")}<section><div class="container legal-text">{format_text(priv_txt)}</div></section>'
terms_content = f'{gen_inner_header("Terms of Service")}<section><div class="container legal-text">{format_text(term_txt)}</div></section>'

# --- PREVIEW & DOWNLOAD ---
c1, c2 = st.columns([3, 1])
with c1:
    if preview_mode == "Home": st.components.v1.html(build_page("Home", home_content), height=600, scrolling=True)
    elif preview_mode == "About": st.components.v1.html(build_page("About", about_content), height=600, scrolling=True)
    elif preview_mode == "Contact": st.components.v1.html(build_page("Contact", contact_content), height=600, scrolling=True)
    elif preview_mode == "Privacy": st.components.v1.html(build_page("Privacy", privacy_content), height=600, scrolling=True)
    elif preview_mode == "Terms": st.components.v1.html(build_page("Terms", terms_content), height=600, scrolling=True)
    elif preview_mode == "Blog Index": st.components.v1.html(build_page("Blog", gen_blog_index_html()), height=600, scrolling=True)
    elif preview_mode == "Blog Post (Demo)": st.components.v1.html(build_page("Article", gen_blog_post_html()), height=600, scrolling=True)
    elif preview_mode == "Product Detail (Demo)":
        st.info("ℹ️ Demo Mode Active: Showing the first available product from your CSV.")
        st.components.v1.html(build_page("Product Name", gen_product_page_content(is_demo=True)), height=600, scrolling=True)

with c2:
    st.success("System Ready.")
    if st.button("DOWNLOAD WEBSITE ZIP", type="primary"):
        z_b = io.BytesIO()
        with zipfile.ZipFile(z_b, "a", zipfile.ZIP_DEFLATED, False) as zf:
            zf.writestr("index.html", build_page("Home", home_content))
            zf.writestr("about.html", build_page("About", about_content))
            zf.writestr("contact.html", build_page("Contact", contact_content))
            zf.writestr("privacy.html", build_page("Privacy Policy", privacy_content))
            zf.writestr("terms.html", build_page("Terms of Service", terms_content))
            zf.writestr("product.html", build_page("Product Details", gen_product_page_content(is_demo=False)))
            
            if show_blog:
                zf.writestr("blog.html", build_page("Blog", gen_blog_index_html()))
                zf.writestr("post.html", build_page("Article", gen_blog_post_html()))

            zf.writestr("404.html", build_page("404 Not Found", gen_404_content()))
            zf.writestr("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {prod_url}/sitemap.xml")
            
            import datetime
            date_str = datetime.date.today().isoformat()
            
            sitemap_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
   <url><loc>{prod_url}/</loc><lastmod>{date_str}</lastmod></url>
   <url><loc>{prod_url}/index.html</loc><lastmod>{date_str}</lastmod></url>
   <url><loc>{prod_url}/about.html</loc><lastmod>{date_str}</lastmod></url>
   <url><loc>{prod_url}/contact.html</loc><lastmod>{date_str}</lastmod></url>
   <url><loc>{prod_url}/privacy.html</loc><lastmod>{date_str}</lastmod></url>
   <url><loc>{prod_url}/terms.html</loc><lastmod>{date_str}</lastmod></url>
   <url><loc>{prod_url}/blog.html</loc><lastmod>{date_str}</lastmod></url>
</urlset>"""
            zf.writestr("sitemap.xml", sitemap_xml)
            
        st.download_button("📥 Click to Save", z_b.getvalue(), f"{biz_name.lower().replace(' ','_')}_site.zip", "application/zip")
