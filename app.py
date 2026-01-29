import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os


# ==========================
# 🎯 إعدادات التطبيق الأساسية
# ==========================
def setup_application():
    """إعداد التطبيق الأساسي"""
    env_config = {
        "APP_INFO": {
            "APP_NAME": "Sira منصـة سـيرا القانونـية",
            "VERSION": "v4.0.0 - الإصدار الشامل",
            "DESCRIPTION": "منصة متكاملة تشمل جميع مواد قانون أصول المحاكمات المدنية الأردني لسنة 1988"
        },
        "FOOTER": {
            "TEXT": "© 2025 Sira سيرا — جميع الحقوق محفوظة"
        },
       
    }
    return env_config

config = setup_application()

# إعداد صفحة Streamlit
st.set_page_config(
    page_title=config["APP_INFO"]["APP_NAME"],
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================
# 🎨 التصميم الفاتح الاحترافي
# ==========================
def load_custom_css():
    """تحميل التصميم المخصص"""
    st.markdown("""
    <style>
    /* التصميم الفاتح الاحترافي */
    .stApp {
        background-color: #FFFFFF !important;
        color: #1F2937 !important;
    }
    
    /* تحسينات عامة للنص */
    .main * {
        color: #1F2937 !important;
    }
    
    /* تصميم الهيدر البسيط */
    .main-header {
        text-align: center;
        padding: 2rem 0;
        margin-bottom: 2rem;
        border-bottom: 1px solid #E5E7EB;
    }
    
    .platform-name {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1E40AF !important;
        margin-bottom: 0.5rem;
    }
    
    .platform-subtitle {
        font-size: 1.2rem;
        color: #6B7280 !important;
        font-weight: 400;
    }
    
    /* تصميم البطاقات البسيط */
    .section-card {
        background: #FFFFFF;
        padding: 1.5rem;
        border-radius: 8px;
        border: 1px solid #E5E7EB;
        margin: 1rem 0;
        transition: all 0.2s ease;
    }
    
    .section-card:hover {
        border-color: #1E40AF;
    }
    
    /* تصميم العناصر التفاعلية */
    .feature-item {
        background: #F9FAFB;
        padding: 1rem;
        border-radius: 6px;
        margin: 0.5rem 0;
        border-left: 4px solid #1E40AF;
        transition: all 0.2s ease;
    }
    
    .feature-item:hover {
        background: #F3F4F6;
    }
    
    /* تصميم التبويبات البسيط */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0px;
        background: #FFFFFF;
        border-bottom: 1px solid #E5E7EB;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: #FFFFFF !important;
        color: #6B7280 !important;
        border-radius: 0px !important;
        padding: 12px 24px !important;
        margin: 0px !important;
        border: none !important;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        color: #1E40AF !important;
        background: #F9FAFB !important;
    }
    
    .stTabs [aria-selected="true"] {
        color: #1E40AF !important;
        background: #FFFFFF !important;
        border-bottom: 2px solid #1E40AF !important;
    }
    
    /* تصميم الأزرار */
    .stButton button {
        background: #1E40AF !important;
        color: white !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 10px 20px !important;
        font-weight: 500 !important;
    }
    
    .stButton button:hover {
        background: #1E3A8A !important;
    }
    
    /* تصميم الشريط الجانبي */
    section[data-testid="stSidebar"] {
        background: #F9FAFB !important;
        border-right: 1px solid #E5E7EB !important;
    }
    
    /* تصميم خاص للمحامين */
    .legal-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .legal-card h3, .legal-card h4, .legal-card p {
        color: white !important;
    }
    
    .article-box {
        background: #F8FAFC;
        border-left: 4px solid #1E40AF;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 0 8px 8px 0;
    }
    
    .law-reference {
        background: #EFF6FF;
        border: 1px solid #BFDBFE;
        padding: 0.75rem;
        border-radius: 6px;
        margin: 0.5rem 0;
        font-size: 0.9rem;
    }
    
    </style>
    """, unsafe_allow_html=True)

load_custom_css()

# ==========================
# 🧮 دوال مساعدة أساسية
# ==========================
def initialize_session_state():
    """تهيئة حالة الجلسة"""
    default_states = {
        'selected_page': 'home',
        'calculation_history': [],
        'user_type': 'lawyer',
        'case_files': [],
        'financial_data': {},
        'current_case': None,
        'user_profile': {},
        'notifications': []
    }
    
    for key, value in default_states.items():
        if key not in st.session_state:
            st.session_state[key] = value

def show_breadcrumbs(section_name):
    """عرض مسار التنقل"""
    st.markdown(f"""
    <div style='
        background: #F9FAFB; 
        padding: 12px 16px; 
        border-radius: 6px; 
        margin-bottom: 20px; 
        border: 1px solid #E5E7EB;
        color: #6B7280;
        font-size: 0.9rem;
    '>
        <strong>المسار:</strong> الرئيسية ▶ {section_name}
    </div>
    """, unsafe_allow_html=True)

def show_law_reference(article_num, content):
    """عرض مرجع قانوني"""
    st.markdown(f"""
    <div class="law-reference">
        <strong>المادة {article_num}:</strong> {content}
    </div>
    """, unsafe_allow_html=True)

def display_article_section(title, articles):
    """عرض قسم من المواد القانونية"""
    st.markdown(f"#### {title}")
    for article in articles:
        with st.expander(f"📌 المادة {article['number']}", expanded=False):
            st.write(f"**النص:** {article['text']}")
            if 'explanation' in article:
                st.info(f"**💡 الشرح:** {article['explanation']}")
            if 'application' in article:
                st.success(f"**🎯 التطبيق العملي:** {article['application']}")

def calculate_deadline_date(start_date, days, include_holidays=True):
    """حساب تاريخ انتهاء الميعاد"""
    # هذا نموذج مبسط - في التطبيق الحقيقي يجب مراعاة العطل الرسمية
    return start_date + timedelta(days=days)

def save_to_session(key, value):
    """حفظ البيانات في حالة الجلسة"""
    st.session_state[key] = value

def get_from_session(key, default=None):
    """استرجاع البيانات من حالة الجلسة"""
    return st.session_state.get(key, default)

# ==========================
# 🧭 نظام التنقل
# ==========================
def setup_navigation():
    """إعداد خيارات التنقل"""
    return {
        "🏠 الرئيسية": "home",
        "📨 التبليغات والإجراءات (1-26)": "notifications_procedures",
        "🏛️ الاختصاص القضائي (27-47)": "judicial_jurisdiction", 
        "💰 التقييم المالي (48-55)": "financial_evaluation",
        "📝 رفع الدعوى واللوائح (56-60)": "filing_cases",
        "⚖️ إجراءات المحاكمة (61-87)": "trial_procedures",
        "🔍 التحقيق والمضاهاة (88-107)": "investigation_verification",
        "📋 الطلبات والدفوع (108-140)": "extended_requests_defenses",
        "🛡️ الإجراءات الوقائية (141-157)": "preventive_procedures",
        "🧾 الأحكام والطعون (158-225)": "judgments_appeals",
        "🔧 أدوات المحامي": "lawyer_tools"
    }

def show_sidebar_navigation():
    """إظهار القائمة الجانبية الموسعة"""
    st.sidebar.markdown("""
    <div style="text-align: center; padding: 1.5rem 0; border-bottom: 1px solid #E5E7EB; margin-bottom: 1rem;">
        <h3 style="margin: 0; color: #1E40AF;">⚖️ Sira</h3>
        <p style="margin: 0; color: #6B7280; font-size: 0.9rem;">الإصدار الشامل - قانون أصول المحاكمات</p>
    </div>
    """, unsafe_allow_html=True)
    
    page_options = setup_navigation()
    
    for page_name, page_id in page_options.items():
        if st.sidebar.button(
            page_name, 
            key=f"nav_{page_id}",
            use_container_width=True
        ):
            st.session_state.selected_page = page_id
            st.rerun()
    
    # إضافة معلومات المستخدم في الشريط الجانبي
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 👤 معلومات المستخدم")
    st.sidebar.info("محامي مرخص - عضو نقابة المحامين")
    
    # إشعارات سريعة
    if st.session_state.get('notifications'):
        st.sidebar.markdown("### 🔔 الإشعارات")
        for notification in st.session_state.notifications[:3]:
            st.sidebar.warning(notification)

# ==========================
# 🏠 الصفحة الرئيسية
# ==========================
def show_home_page():
    """عرض الصفحة الرئيسية"""
    st.markdown("""
    <div class="main-header">
        <div class="platform-name">Sira</div>
        <div class="platform-subtitle">الإصدار الشامل - قانون أصول المحاكمات المدنية الأردني لسنة 1988</div>
    </div>
    """, unsafe_allow_html=True)

    # بطاقة ترحيبية
    st.markdown("""
    <div class="legal-card">
        <h3>⚖️ الإصدار الشامل - جميع المواد القانونية (1-225)</h3>
        <p>تم تحديث المنصة لتشمل جميع مواد قانون أصول المحاكمات المدنية مع أدوات متخصصة للتقييم المالي، الإجراءات الوقائية، التحقيق والمضاهاة، الطعون، وغيرها من الأقسام الجديدة.</p>
    </div>
    """, unsafe_allow_html=True)

    # الإحصائيات
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📚 المواد القانونية", "225")
    with col2:
        st.metric("🆕 الأقسام المضافة", "8")
    with col3:
        st.metric("⚖️ أنواع الإجراءات", "30+")
    with col4:
        st.metric("🧮 أدوات متخصصة", "20+")

    # الأقسام الرئيسية
    st.markdown("### 📋 الأقسام الرئيسية الموسعة")
    
    sections = [
        {"icon": "📨", "title": "التبليغات والإجراءات (1-26)", "description": "إجراءات التبليغ والمواعيد والموطن القانوني", "link": "notifications_procedures"},
        {"icon": "🏛️", "title": "الاختصاص القضائي (27-47)", "description": "أنواع الاختصاص والنزاعات المكانية", "link": "judicial_jurisdiction"},
        {"icon": "💰", "title": "التقييم المالي للدعاوى (48-55)", "description": "تقدير قيمة الدعاوى المختلفة", "link": "financial_evaluation"},
        {"icon": "📝", "title": "رفع الدعوى واللوائح (56-60)", "description": "إجراءات رفع الدعوى وتقديم اللوائح", "link": "filing_cases"},
        {"icon": "⚖️", "title": "إجراءات المحاكمة (61-87)", "description": "جلسات المحاكمة والإثبات والخبرة", "link": "trial_procedures"},
        {"icon": "🔍", "title": "التحقيق والمضاهاة (88-107)", "description": "إجراءات التحقيق والتحقق من المستندات", "link": "investigation_verification"},
        {"icon": "📋", "title": "الطلبات والدفوع (108-140)", "description": "الدفوع المتخصصة والوقف والسقوط", "link": "extended_requests_defenses"},
        {"icon": "🛡️", "title": "الإجراءات الوقائية (141-157)", "description": "الحجز التحفظي والمنع من السفر", "link": "preventive_procedures"},
        {"icon": "🧾", "title": "الأحكام والطعون (158-225)", "description": "إصدار الأحكام وطرق الطعن فيها", "link": "judgments_appeals"},
        {"icon": "🔧", "title": "أدوات المحامي", "description": "نماذج قانونية، حاسبات، وأدوات عملية", "link": "lawyer_tools"}
    ]
    
    cols = st.columns(3)
    for idx, section in enumerate(sections):
        with cols[idx % 3]:
            if st.button(
                f"{section['icon']} {section['title']}",
                key=f"home_{section['link']}",
                use_container_width=True
            ):
                st.session_state.selected_page = section['link']
                st.rerun()
            st.caption(section['description'])

# ==========================
# 📨 قسم التبليغات والإجراءات (1-26)
# ==========================
def show_notifications_procedures_section():
    """قسم التبليغات والإجراءات"""
    show_breadcrumbs("📨 التبليغات والإجراءات (المواد 1-26)")
    
    st.markdown("""
    <div class="main-header">
        <h1>📨 التبليغات والإجراءات القضائية</h1>
        <p>تحليل مفصل لإجراءات التبليغ والمواعيد والموطن القانوني وفق المواد 1-26 من قانون أصول المحاكمات المدنية</p>
    </div>
    """, unsafe_allow_html=True)

    tabs = st.tabs(["📮 التبليغات (4-17)", "⏰ المواعيد (1-3,23)", "🏠 الموطن القانوني (18-22)", "⚖️ البطلان (24-26)", "🔍 أدوات التبليغ"])

    with tabs[0]:
        show_notifications_articles()
    with tabs[1]:
        show_deadlines_articles()
    with tabs[2]:
        show_legal_domicile_articles()
    with tabs[3]:
        show_invalidity_articles()
    with tabs[4]:
        show_notification_tools()

def show_notifications_articles():
    """عرض مواد التبليغات"""
    st.markdown("#### 📮 إجراءات التبليغ - المواد 4-17")
    
    articles = [
        {
            "number": "4",
            "text": "لا يجوز إجراء أي تبليغ أو تنفيذ قبل الساعة السابعة صباحاً، ولا بعد الساعة السابعة مساء ولا في أيام العطل الرسمية إلا في حالات الضرورة وبإذن كتابي من المحكمة.",
            "explanation": "تنظيم أوقات التبليغ لحماية الخصوصية وضمان جدية الإجراءات.",
            "application": "يتم رفض التبليغات التي تتم خارج الأوقات المحددة ما لم يكن هناك إذن خاص من المحكمة."
        },
        {
            "number": "5",
            "text": "يجب أن تشتمل ورقة التبليغ على البيانات التالية: التاريخ، اسم طالب التبليغ، اسم المحكمة، اسم المبلغ إليه، اسم المحضر، موضوع التبليغ، وتوقيع من سلم إليه.",
            "explanation": "ضمان شفافية التبليغ وإمكانية تتبع الإجراءات.",
            "application": "ورقة التبليغ غير المكتملة تعتبر باطلة ويجب إعادة التبليغ."
        },
        {
            "number": "6",
            "text": "كل تبليغ يكون بواسطة المحضرين ما لم ينص القانون على خلاف ذلك. ويجوز التبليغ بالوسائل الإلكترونية إذا كان المبلغ إليه مقيماً على عنوانه المسجل.",
            "explanation": "تعدد طرق التبليغ مع الحفاظ على الضمانات القانونية.",
            "application": "يمكن استخدام البريد الإلكتروني للتبليغ إذا كان العنوان الإلكتروني مسجلاً في الدعوى."
        },
        {
            "number": "7",
            "text": "يتم تبليغ الأوراق القضائية بتسليم نسخة منها إلى الشخص المطلوب تبليغه.",
            "explanation": "الأصل في التبليغ هو التسليم المباشر للشخص المعني.",
            "application": "في حالة تعذر التسليم المباشر، يتم اللجوء لطرق التبليغ البديلة."
        },
        {
            "number": "8",
            "text": "إذا لم يجد المحضر الشخص المطلوب تبليغه في منزله أو محل عمله، يسلم الورقة إلى وكيله أو مستخدمه.",
            "explanation": "توسيع نطاق التسليم ليشمل الأشخاص المرتبطين بالمعني.",
            "application": "يمكن تسليم الأوراق لأي شخص بالغ في نفس مسكن المعني."
        },
        {
            "number": "9", 
            "text": "إذا لم يجد المحضر من يسلم إليه الورقة، يتم الصاقها على الباب الخارجي للمنزل أو محل العمل.",
            "explanation": "التبليغ بالصاق كحل أخير عند تعذر جميع طرق التبليغ الأخرى.",
            "application": "يجب أن يكون الإلصاق بحضور شاهدين وإعادة نسخة للمحكمة."
        },
        {
            "number": "10",
            "text": "تسلم الأوراق القضائية للحكومة والمؤسسات العامة إلى الوكلاء العامين أو من ينوب عنهم.",
            "explanation": "تنظيم خاص لتبليغ الجهات الرسمية.",
            "application": "تبليغ الوزارات يتم عبر الوكلاء العامين المعينين."
        }
    ]
    
    display_article_section("📮 المواد 4-10: إجراءات التبليغ الأساسية", articles)
    
    # المواد 11-17
    st.markdown("#### 🔄 إجراءات التبليغ الخاصة - المواد 11-17")
    
    special_articles = [
        {
            "number": "11",
            "text": "يتم تبليغ الخصم أو الشاهد برسالة مسجلة أو على عنوان بريده الإلكتروني أو باستخدام إحدى الوسائل الإلكترونية.",
            "explanation": "توسيع خيارات التبليغ لتشمل الوسائل الحديثة.",
            "application": "التبليغ الإلكتروني يعتبر صحيحاً إذا تم إثبات وصوله."
        },
        {
            "number": "12",
            "text": "إذا تعذر إجراء التبليغ وفق الطرق المنصوص عليها، جاز للمحكمة أن تأمر بإجراء التبليغ بنشر إعلان في صحيفتين يوميتين.",
            "explanation": "التبليغ بالنشر كحل استثنائي عند تعذر جميع الطرق.",
            "application": "يستخدم التبليغ بالنشر عندما يكون عنوان الشخص مجهولاً."
        },
        {
            "number": "13",
            "text": "إذا كان المطلوب تبليغه مقيماً خارج المملكة، يجري التبليغ باستخدام الوسائل الإلكترونية أو البريد الدبلوماسي.",
            "explanation": "تنظيم التبليغ الدولي وفق المعايير القانونية.",
            "application": "يجب مراعاة اتفاقيات التبليغ الدولي عند التبليغ خارج المملكة."
        },
        {
            "number": "14",
            "text": "لا تسير في الدعوى حتى تبلغ الأوراق القضائية إلى المحكمة وفق الأصول.",
            "explanation": "التبليغ الصحيح شرط لسير الإجراءات.",
            "application": "أي إجراء يتم قبل التبليغ الصحيح يعتبر باطلاً."
        },
        {
            "number": "15",
            "text": "يعتبر التبليغ منتجاً لأثره من وقت توصل المطلوب تبليغه بورقة التبليغ.",
            "explanation": "تحديد وقت نفاذ التبليغ قانوناً.",
            "application": "تحسب المواعيد من تاريخ التبليغ الفعلي."
        },
        {
            "number": "16",
            "text": "يرتكز البطلان على عدم مراعاة مواعيد وإجراءات التبليغ المنصوص عليها.",
            "explanation": "جزاء مخالفة إجراءات التبليغ.",
            "application": "يمكن الطعن في الإجراءات لعدم صحة التبليغ."
        }
    ]
    
    for article in special_articles:
        with st.expander(f"📌 المادة {article['number']}", expanded=False):
            st.write(f"**النص:** {article['text']}")
            st.info(f"**💡 الشرح:** {article['explanation']}")
            st.success(f"**🎯 التطبيق العملي:** {article['application']}")

def show_deadlines_articles():
    st.markdown("#### ⏰ المواعيد والإجراءات - المواد 1-3, 23")
    
    deadline_articles = [
        {
            "number": "1",
            "text": "يسمى هذا القانون (قانون أصول المحاكمات المدنية لسنة 1988) ويبدأ العمل به بعد مائة وعشرين يوماً من تاريخ نشره في الجريدة الرسمية.",
            "explanation": "تحديد اسم القانون وتاريخ بدء العمل به.",
            "application": "يتم تطبيق القانون على الدعاوى المرفوعة بعد تاريخ نفاذه."
        },
        {
            "number": "2", 
            "text": "تسري أحكام هذا القانون على ما لم يكن فصل فيه من الدعاوى قبل تاريخ العمل به مع استثناءات محددة.",
            "explanation": "تنظيم سريان القانون زمنياً.",
            "application": "القواعد الإجرائية الجديدة تسري على الدعاوى الجارية."
        },
        {
            "number": "3",
            "text": "لا يقبل أي طلب أو دفع لا يكون لصاحبه فيه مصلحة قائمة يقرها القانون. وتكفي المصلحة المحتملة إذا كان الغرض من الطلب الاحتياط لدفع ضرر متوقع.",
            "explanation": "شرط المصلحة كأساس لقبول الدعاوى والطلبات.",
            "application": "رفض الدعاوى التي تفتقر إلى المصلحة القانونية."
        },
        {
            "number": "23",
            "text": "إذا كان الميعاد مقدراً بالأيام لا يحسب فيه يوم التبليغ. وتحسب المواعيد المعينة بالشهر أو السنة بالتقويم الميلادي. وإذا صادف آخر الميعاد عطلة رسمية يؤجل إلى أول يوم عمل بعدها.",
            "explanation": "قواعد حساب المواعيد القانونية.",
            "application": "يجب مراعاة هذه القواعد في جميع المواعيد القانونية."
        }
    ]
    
    for article in deadline_articles:
        with st.expander(f"⏰ المادة {article['number']}", expanded=False):
            st.write(f"**النص:** {article['text']}")
            st.info(f"**💡 الشرح:** {article['explanation']}")
            st.success(f"**🎯 التطبيق العملي:** {article['application']}")
    
    # حاسبة المواعيد
    st.markdown("##### 🧮 حاسبة المواعيد القانونية")
    
    with st.form("deadline_calculator"):
        col1, col2 = st.columns(2)
        
        with col1:
            start_date = st.date_input("تاريخ بدء الميعاد")
            deadline_type = st.selectbox("نوع الميعاد", [
                "استئناف الحكم (30 يوم)",
                "تمييز الحكم (30 يوم)", 
                "معارضة (15 يوم)",
                "لائحة جوابية (30 يوم)",
                "ميعاد آخر"
            ])
            
        with col2:
            custom_days = st.number_input("عدد الأيام (إذا اخترت ميعاد آخر)", min_value=1, value=30)
            include_holidays = st.checkbox("احتساب العطل الرسمية", value=True)
        
        if st.form_submit_button("🧮 احسب تاريخ الانتهاء", use_container_width=True):
            if "آخر" not in deadline_type:
                days = 30 if "استئناف" in deadline_type or "تمييز" in deadline_type or "جوابية" in deadline_type else 15
            else:
                days = custom_days
            
            end_date = calculate_deadline_date(start_date, days, include_holidays)
            remaining = (end_date - datetime.now().date()).days
            
            st.success(f"**تاريخ انتهاء الميعاد:** {end_date.strftime('%Y-%m-%d')}")
            st.info(f"**الأيام المتبقية:** {remaining} يوم")
            
            if remaining < 0:
                st.error("⚠️ انتهى الميعاد القانوني!")
            elif remaining <= 3:
                st.warning("🚨 الميعاد على وشك الانتهاء!")

def show_legal_domicile_articles():
    st.markdown("#### 🏠 الموطن القانوني - المواد 18-22")
    
    domicile_articles = [
        {
            "number": "18",
            "text": "الموطن هو المكان الذي يقيم فيه الشخص عادة. وموطن الشخص الاعتباري هو المكان الذي يوجد فيه مركز إدارته.",
            "explanation": "التعريف القانوني للموطن للأفراد والشركات.",
            "application": "يحدد الموطن الاختصاص المكاني للمحكمة."
        },
        {
            "number": "19",
            "text": "يجوز اتخاذ موطن مكاني للتقاضي على عمل قانوني معين ويكون هو الموطن بالنسبة لكل ما يتعلق بهذا العمل.",
            "explanation": "إمكانية اختيار موطن خاص لعمل قانوني محدد.",
            "application": "يجب أن يكون اختيار الموطن المكاني كتابياً."
        },
        {
            "number": "20", 
            "text": "إذا أوجب القانون على الشخص تعيين موطن مكاني له ولم يفعل، جاز تبليغه بالنشر.",
            "explanation": "جزاء عدم تعيين الموطن المكاني عندما يكون إلزامياً.",
            "application": "اللجوء للتبليغ بالنشر في حالة عدم تعيين الموطن."
        },
        {
            "number": "21",
            "text": "يساعد المحكمة في ضبط الإجراءات كاتب يحرر محضر الجلسات بشكل يدوي أو إلكتروني.",
            "explanation": "دور كاتب المحكمة في توثيق الإجراءات.",
            "application": "المحاضر الموقعة من القاضي والكاتب تكون حجة."
        },
        {
            "number": "22",
            "text": "لا يجوز لموظفي المحاكم أن يباشروا أعمالاً في الدعاوى الخاصة بهم أو بأقاربهم.",
            "explanation": "ضمان نزاهة الموظفين القضائيين.",
            "application": "يمنع الموظف من العمل في القضايا التي له فيها مصلحة."
        }
    ]
    
    for article in domicile_articles:
        with st.expander(f"🏠 المادة {article['number']}", expanded=False):
            st.write(f"**النص:** {article['text']}")
            st.info(f"**💡 الشرح:** {article['explanation']}")
            st.success(f"**🎯 التطبيق العملي:** {article['application']}")

def show_invalidity_articles():
    st.markdown("#### ⚖️ البطلان - المواد 24-26")
    
    invalidity_articles = [
        {
            "number": "24", 
            "text": "يكون الإجراء باطلاً إذا خالف القانون أو إذا شابه عيب وترتب عليه ضرر للخصم.",
            "explanation": "شروط بطلان الإجراءات القضائية.",
            "application": "لا يحكم بالبطلان لمجرد مخالفة الإجراءات ما لم يترتب ضرر."
        },
        {
            "number": "25",
            "text": "لا يجوز التمسك بالبطلان إلا من لحقه البطلان. ولا يجوز التمسك به من الخصم الذي تسبب فيه.",
            "explanation": "قواعد التمسك بالبطلان.",
            "application": "يمنع الخصم من التمسك بالبطلان الذي سببه بنفسه."
        },
        {
            "number": "26",
            "text": "يجب تحديد البطلان بالحكم ولو بعد التمسك به، ولا يعتد بالإجراء إلا من تاريخ تحديده.",
            "explanation": "إجراءات الفصل في طلبات البطلان.",
            "application": "يجب على المحكمة الفصل في طلبات البطلان بشكل صريح."
        }
    ]
    
    for article in invalidity_articles:
        with st.expander(f"⚖️ المادة {article['number']}", expanded=False):
            st.write(f"**النص:** {article['text']}")
            st.info(f"**💡 الشرح:** {article['explanation']}")
            st.success(f"**🎯 التطبيق العملي:** {article['application']}")

def show_notification_tools():
    st.markdown("#### 🔍 أدوات التبليغ والمواعيد")
    
    with st.form("notification_analysis"):
        st.subheader("تحليل إجراءات التبليغ")
        
        col1, col2 = st.columns(2)
        
        with col1:
            notification_type = st.selectbox("نوع التبليغ", [
                "تبليغ عادي بالمحضر",
                "تبليغ بالوسائل الإلكترونية", 
                "تبليغ بالصاق",
                "تبليغ بالنشر",
                "تبليغ دولي"
            ])
            person_type = st.selectbox("نوع الشخص المطلوب تبليغه", [
                "فرد",
                "شركة",
                "جهة حكومية",
                "شخص اعتباري"
            ])
            
        with col2:
            domicile_status = st.selectbox("حالة الموطن", [
                "موطن معروف",
                "موطن غير معروف", 
                "موطن خارج المملكة",
                "لا يوجد موطن"
            ])
            urgency_level = st.select_slider("درجة الاستعجال", options=["عادية", "متوسطة", "عاجلة"])
        
        if st.form_submit_button("🔍 تحليل إجراءات التبليغ", use_container_width=True):
            analysis = analyze_notification_procedures(notification_type, person_type, domicile_status, urgency_level)
            display_notification_analysis(analysis)

def analyze_notification_procedures(n_type, p_type, domicile, urgency):
    """تحليل إجراءات التبليغ المناسبة"""
    
    procedures = []
    legal_basis = []
    recommendations = []
    
    # تحليل نوع التبليغ
    if n_type == "تبليغ عادي بالمحضر":
        procedures.append("التسليم المباشر للشخص المعني")
        legal_basis.append("المادة 7")
    elif n_type == "تبليغ بالوسائل الإلكترونية":
        procedures.append("الإرسال عبر البريد الإلكتروني المسجل")
        legal_basis.append("المادة 6")
    elif n_type == "تبليغ بالصاق":
        procedures.append("الصاق الإعلان على الباب الخارجي")
        legal_basis.append("المادة 9")
    elif n_type == "تبليغ بالنشر":
        procedures.append("النشر في صحيفتين يوميتين")
        legal_basis.append("المادة 12")
    
    # تحليل نوع الشخص
    if p_type == "جهة حكومية":
        procedures.append("التسليم للوكيل العام أو من ينوب عنه")
        legal_basis.append("المادة 10")
    elif p_type == "شركة":
        procedures.append("التسليم للمدير أو المسؤول القانوني")
        legal_basis.append("المادة 10")
    
    # تحليل حالة الموطن
    if domicile == "موطن غير معروف":
        procedures.append("اللجوء للتبليغ بالنشر")
        recommendations.append("البحث عن آخر موطن معروف قبل التبليغ بالنشر")
    elif domicile == "موطن خارج المملكة":
        procedures.append("استخدام الوسائل الدبلوماسية أو الإلكترونية")
        legal_basis.append("المادة 13")
    
    # تحليل درجة الاستعجال
    if urgency == "عاجلة":
        recommendations.append("طلب إذن خاص للتبليغ خارج الأوقات الرسمية إذا لزم الأمر")
        legal_basis.append("المادة 4")
    
    return {
        'procedures': procedures,
        'legal_basis': legal_basis,
        'recommendations': recommendations,
        'estimated_time': get_estimated_notification_time(n_type, domicile, urgency)
    }

def display_notification_analysis(analysis):
    """عرض نتيجة تحليل التبليغ"""
    
    st.success("## 🔍 نتيجة تحليل إجراءات التبليغ")
    
    st.markdown("##### 📋 الإجراءات المطلوبة:")
    for procedure in analysis['procedures']:
        st.write(f"• {procedure}")
    
    st.markdown("##### ⚖️ الأساس القانوني:")
    for basis in analysis['legal_basis']:
        st.write(f"• {basis}")
    
    if analysis['recommendations']:
        st.markdown("##### 💡 التوصيات:")
        for recommendation in analysis['recommendations']:
            st.write(f"• {recommendation}")
    
    st.info(f"**⏰ الوقت المتوقع:** {analysis['estimated_time']}")

def get_estimated_notification_time(n_type, domicile, urgency):
    """تقدير الوقت اللازم للتبليغ"""
    
    base_time = 3  # أيام
    
    if n_type == "تبليغ بالنشر":
        base_time = 14
    elif n_type == "تبليغ دولي":
        base_time = 30
    
    if domicile == "موطن غير معروف":
        base_time += 7
    elif domicile == "موطن خارج المملكة":
        base_time += 21
    
    if urgency == "عاجلة":
        base_time = max(1, base_time // 2)
    
    return f"{base_time} يوم"

def calculate_deadline_date(start_date, days, include_holidays):
    """حساب تاريخ انتهاء الميعاد (نسخة مبسطة)"""
    from datetime import timedelta
    
    end_date = start_date + timedelta(days=days)
    
    # في التطبيق الحقيقي، يجب مراعاة العطل الرسمية
    # هذا نموذج مبسط لأغراض العرض
    return end_date

# ==========================
# 🏛️ قسم الاختصاص القضائي (27-47)
# ==========================
def show_judicial_jurisdiction_section():
    """قسم الاختصاص القضائي"""
    show_breadcrumbs("🏛️ الاختصاص القضائي (المواد 27-47)")
    
    st.markdown("""
    <div class="main-header">
        <h1>🏛️ الاختصاص القضائي في القانون الأردني</h1>
        <p>تحليل شامل لأنواع الاختصاص والنزاعات المكانية وفق المواد 27-47 من قانون أصول المحاكمات المدنية</p>
    </div>
    """, unsafe_allow_html=True)

    tabs = st.tabs(["🎯 الاختصاص العام (27-35)", "📍 الاختصاص المكاني (36-47)", "⚡ القضاء المستعجل (32-33)", "🔍 فحص الاختصاص"])

    with tabs[0]:
        show_general_jurisdiction_articles()
    with tabs[1]:
        show_territorial_jurisdiction_articles()
    with tabs[2]:
        show_urgent_matters_articles()
    with tabs[3]:
        show_jurisdiction_analysis_tools()

def show_general_jurisdiction_articles():
    st.markdown("#### 🎯 الاختصاص العام - المواد 27-35")
    
    general_articles = [
        {
            "number": "27",
            "text": "تعتبر المحاكم البدائية في المملكة مختصة في النظر والفصل في جميع الدعاوى المدنية، باستثناء الدعاوى التي قد يختص فيها حق القضاء إلى محاكم دينية أو محاكم خاصة.",
            "explanation": "الاختصاص العام للمحاكم البدائية يشمل جميع الدعاوى المدنية ما لم ينص قانون خاص على خلاف ذلك.",
            "application": "محكمة البداية تختص بنظر معظم الدعاوى المدنية في المملكة."
        },
        {
            "number": "28",
            "text": "تختص محاكم المملكة بنظر الدعاوى التي ترفع على الأجنبي الذي ليس له موطن أو محل إقامة في المملكة في حالات محددة.",
            "explanation": "تنظيم اختصاص المحاكم الأردنية في الدعاوى التي تتضمن عنصراً أجنبياً.",
            "application": "يمكن رفع الدعوى على الأجنبي في المملكة إذا كان له موطن مختار أو أموال فيها."
        },
        {
            "number": "29",
            "text": "إذا لم يختص المدعى عليه وكانت المحاكم البدائية غير مختصة بنظر الدعوى، تحكم المحكمة بعدم اختصاصها من تلقاء نفسها.",
            "explanation": "إلزام المحكمة بالفصل في مسألة الاختصاص حتى دون طلب من الخصوم.",
            "application": "المحكمة ترفض النظر في الدعوى إذا تبين لها عدم اختصاصها."
        },
        {
            "number": "30",
            "text": "تختص محكمة البداية بالنظر والفصل في الدعاوى التي لا تدخل في اختصاص محكمة أخرى بمقتضى أي قانون نافذ.",
            "explanation": "محكمة البداية هي محكمة القانون العام وتختص بما لا يختص به غيرها.",
            "application": "اللجوء لمحكمة البداية عندما لا تكون هناك محكمة مختصة بنوع الدعوى."
        },
        {
            "number": "31",
            "text": "قاضي الأمور المستعجلة هو رئيس محكمة البداية أو من يقوم مقامه أو من ينتدبه لذلك من قضاتها.",
            "explanation": "تنظيم اختصاص قاضي الأمور المستعجلة.",
            "application": "قاضي الأمور المستعجلة يختص بالمسائل العاجلة التي يخشى فوات وقتها."
        },
        {
            "number": "32",
            "text": "يحكم قاضي الأمور المستعجلة بأمر مؤقت في المسائل المستعجلة التي يخشى فوات وقتها.",
            "explanation": "الاختصاص الاستثنائي لقاضي الأمور المستعجلة.",
            "application": "يختص قاضي المستعجلات بالحجز التحفظي والمنع من السفر وغيرها."
        },
        {
            "number": "33",
            "text": "تنظر المحكمة أو قاضي الأمور المستعجلة في المسائل المستعجلة تحقيقاً دون حاجة لتبادل اللوائح.",
            "explanation": "تبسيط إجراءات القضاء المستعجل.",
            "application": "يمكن الفصل في الطلبات المستعجلة دون انتظار مدة اللوائح الجوابية."
        },
        {
            "number": "34",
            "text": "إذا نشأ نزاع يتعلق باختصاص محكمة ما، يحال هذا النزاع إلى المحكمة المنصوص عليها في القانون.",
            "explanation": "تنظيم حل النزاعات المتعلقة بالاختصاص بين المحاكم.",
            "application": "يحال نزاع الاختصاص إلى محكمة التمييز أو محكمة الاستئناف حسب الحالة."
        },
        {
            "number": "35",
            "text": "إذا حصل تنازع في الاختصاص بين محكمتين نظاميتين، فلأي من الخصوم أن يطلب تسليم التنازع المحصل إلى المحكمة التالية.",
            "explanation": "آلية حل التنازع في الاختصاص بين المحاكم.",
            "application": "يقدم طلب حل التنازع إلى محكمة الاستئناف أو التمييز حسب نوع المحكمتين."
        }
    ]
    
    display_article_section("🎯 المواد 27-35: الاختصاص العام والاستثنائي", general_articles)

def show_territorial_jurisdiction_articles():
    st.markdown("#### 📍 الاختصاص المكاني - المواد 36-47")
    
    territorial_articles = [
        {
            "number": "36",
            "text": "في جميع الدعاوى الشخصية أو العينية يكون الاختصاص للمحكمة التي يقع في دائرتها موطن المدعى عليه.",
            "explanation": "القاعدة العامة في الاختصاص المكاني هي موطن المدعى عليه.",
            "application": "ترفع الدعوى في المحكمة التي يقع في دائرتها موطن المدعى عليه."
        },
        {
            "number": "37",
            "text": "في الدعاوى العينية العقارية يكون الاختصاص للمحكمة التي يقع في دائرتها العقار.",
            "explanation": "استثناء من القاعدة العامة للدعاوى العينية العقارية.",
            "application": "دعاوى الملكية والارتفاق ترفع في مكان العقار."
        },
        {
            "number": "38",
            "text": "في الدعاوى المتعلقة بالشركات أو الجمعيات يكون الاختصاص للمحكمة التي يقع في دائرتها مركز إدارتها.",
            "explanation": "اختصاص خاص بالدعاوى المتعلقة بالأشخاص الاعتبارية.",
            "application": "ترفع الدعوى على الشركة في مكان مركز إدارتها الرئيسي."
        },
        {
            "number": "39",
            "text": "الدعاوى المتعلقة بالشركات أو التي يرفعها الشركاء قبل قسمة الشركة تكون من اختصاص المحكمة التي يقع في دائرتها مركز الشركة.",
            "explanation": "تنظيم اختصاص الدعاوى بين الشركاء.",
            "application": "دعاوى الشركاء ترفع في مكان المركز الرئيسي للشركة."
        },
        {
            "number": "40",
            "text": "في المواد التي فيها الالتزام بتنفيذ عقد يكون الاختصاص للمحكمة التي يقع في دائرتها موطن المدعى عليه أو مكان تنفيذ العقد.",
            "explanation": "تعدد خيارات الاختصاص في دعاوى التنفيذ العقدي.",
            "application": "يمكن رفع الدعوى في موطن المدعى عليه أو مكان التنفيذ."
        },
        {
            "number": "41", 
            "text": "في المنازعات المتعلقة بالعقود والإيجار يكون الاختصاص للمحكمة التي يقع في دائرتها موطن المدعى عليه، أو للمحكمة التي في دائرتها تم العقد.",
            "explanation": "اختصاص منفصل للمنازعات العقدية.",
            "application": "مرونة في اختيار المحكمة المختصة في المنازعات العقدية."
        },
        {
            "number": "42",
            "text": "في المنازعات المتعلقة بالتأمينات والأموال يكون الاختصاص للمحكمة التي يقع في دائرتها موطن المدعى عليه، أو للمحكمة التي في دائرتها تم العقد.",
            "explanation": "تنظيم اختصاص منازعات التأمين.",
            "application": "يمكن رفع الدعوى في موطن المؤمن له أو مكان إبرام العقد."
        },
        {
            "number": "43",
            "text": "في المنازعات المتعلقة بعقود التأمين يكون الاختصاص للمحكمة التي يقع في دائرتها موطن الشخص المؤمن عليه أو مكان المال المؤمن عليه.",
            "explanation": "اختصاص خاص بعقود التأمين.",
            "application": "مرونة في تحديد المحكمة المختصة في منازعات التأمين."
        },
        {
            "number": "44",
            "text": "في المواد التجارية يكون الاختصاص للمحكمة التي يقع في دائرتها موطن المدعى عليه أو للمحكمة التي في دائرتها تم العقد.",
            "explanation": "تنظيم اختصاص المنازعات التجارية.",
            "application": "يمكن رفع الدعوى التجارية في مكان إبرام العقد أو موطن المدعى عليه."
        },
        {
            "number": "45",
            "text": "في الدعاوى المتعلقة بإجراءات وقائية أو مستعجلة يكون الاختصاص للمحكمة التي يقع في دائرتها موطن المدعى عليه.",
            "explanation": "اختصاص الإجراءات الوقائية والمستعجلة.",
            "application": "ترفع الطلبات المستعجلة في موطن المدعى عليه."
        },
        {
            "number": "46",
            "text": "في المنازعات المتعلقة بمصروفات الدعوى يكون الاختصاص للمحكمة التي نظرت في الدعوى الأصلية.",
            "explanation": "اختصاص منازعات المصروفات.",
            "application": "تختص محكمة الموضوع الأصلية بنظر منازعات المصروفات."
        },
        {
            "number": "47",
            "text": "إذا لم يكن للمدعى عليه موطن ولا محل إقامة في المملكة، يكون الاختصاص للمحكمة التي يقع في دائرتها موطن المدعي.",
            "explanation": "حل استثنائي عند عدم وجود موطن للمدعى عليه.",
            "application": "اللجوء لموطن المدعي عندما لا يوجد موطن للمدعى عليه."
        }
    ]
    
    for article in territorial_articles:
        with st.expander(f"📍 المادة {article['number']}", expanded=False):
            st.write(f"**النص:** {article['text']}")
            st.info(f"**💡 الشرح:** {article['explanation']}")
            st.success(f"**🎯 التطبيق العملي:** {article['application']}")

def show_urgent_matters_articles():
    st.markdown("#### ⚡ القضاء المستعجل - المواد 32-33")
    
    urgent_articles = [
        {
            "number": "32",
            "text": "يحكم قاضي الأمور المستعجلة بأمر مؤقت في المسائل المستعجلة التي يخشى فوات وقتها، على أن هذا لا يمنع من اختصاص محكمة الموضوع للنظر في هذه المسائل.",
            "explanation": "الطبيعة الوقتية لأحكام القضاء المستعجل وعدم المساس باختصاص محكمة الموضوع.",
            "application": "أحكام القضاء المستعجل مؤقتة وقابلة للتعديل من محكمة الموضوع."
        },
        {
            "number": "33",
            "text": "تنظر المحكمة أو قاضي الأمور المستعجلة في المسائل المستعجلة تحقيقاً دون حاجة لتبادل اللوائح إلا إذا رأت المحكمة أو القاضي ذلك.",
            "explanation": "تبسيط إجراءات القضاء المستعجل وعدم التقيد بالإجراءات الشكلية.",
            "application": "يمكن الفصل في الطلبات المستعجلة بسرعة دون إجراءات معقدة."
        }
    ]
    
    for article in urgent_articles:
        with st.expander(f"⚡ المادة {article['number']}", expanded=False):
            st.write(f"**النص:** {article['text']}")
            st.info(f"**💡 الشرح:** {article['explanation']}")
            st.success(f"**🎯 التطبيق العملي:** {article['application']}")
    
    # أنواع المسائل المستعجلة
    st.markdown("##### 📋 أنواع المسائل التي يدخل فيها اختصاص القضاء المستعجل")
    
    urgent_matters = [
        "المسائل المستعجلة التي يخشى فوات وقتها",
        "طلبات تعيين وكيل أو قيم على مال", 
        "التحفظ التشغيلي أو الحراسة",
        "منع السفر في بعض الحالات",
        "الكشف المستعجل لحالة الأموال",
        "الحجز التحفظي",
        "أي مسألة أخرى يقرر القاضي أنها مستعجلة"
    ]
    
    for matter in urgent_matters:
        st.write(f"• {matter}")

def show_jurisdiction_analysis_tools():
    st.markdown("#### 🔍 أدوات تحليل الاختصاص القضائي")
    
    with st.form("jurisdiction_analyzer"):
        st.subheader("تحليل الاختصاص القضائي للدعوى")
        
        col1, col2 = st.columns(2)
        
        with col1:
            case_type = st.selectbox("نوع الدعوى", [
                "دعوى شخصية",
                "دعوى عينية عقارية", 
                "دعوى تجارية",
                "دعوى عمل",
                "دعوى أحوال شخصية",
                "دعوى مستعجلة"
            ])
            
            defendant_domicile = st.selectbox("موطن المدعى عليه", [
                "داخل المملكة - معروف",
                "داخل المملكة - غير معروف",
                "خارج المملكة",
                "متعدد الموطن"
            ])
            
        with col2:
            case_value = st.number_input("قيمة الدعوى (دينار)", min_value=0, value=5000)
            subject_matter = st.selectbox("موضوع الدعوى", [
                "عقدي",
                "تعدي",
                "تعويض",
                "تنفيذ عقد", 
                "تسليم منقول",
                "أخرى"
            ])
            
            property_location = st.text_input("موقع العقار (للدعاوى العقارية)")
        
        if st.form_submit_button("🔍 تحليل الاختصاص", use_container_width=True):
            analysis = analyze_jurisdiction_comprehensive(
                case_type, defendant_domicile, case_value, subject_matter, property_location
            )
            display_jurisdiction_analysis(analysis)

def analyze_jurisdiction_comprehensive(case_type, domicile, value, subject, property_location):
    """تحليل شامل للاختصاص القضائي"""
    
    jurisdiction_info = {
        'المحكمة_المختصة': '',
        'السبب': '',
        'التوصيات': [],
        'المواد_المعنية': [],
        'الاختصاص_المكاني': ''
    }
    
    # تحليل الاختصاص النوعي
    if case_type == "دعوى عينية عقارية":
        jurisdiction_info['المحكمة_المختصة'] = "محكمة البداية - مكان العقار"
        jurisdiction_info['السبب'] = "الدعاوى العينية العقارية ترفع في مكان وجود العقار"
        jurisdiction_info['المواد_المعنية'] = ["37"]
        jurisdiction_info['الاختصاص_المكاني'] = f"المحكمة التي يقع في دائرتها العقار في {property_location if property_location else 'مكان العقار'}"
    
    elif case_type == "دعوى مستعجلة":
        jurisdiction_info['المحكمة_المختصة'] = "قاضي الأمور المستعجلة"
        jurisdiction_info['السبب'] = "المسائل المستعجلة التي يخشى فوات وقتها"
        jurisdiction_info['المواد_المعنية'] = ["32", "33"]
        jurisdiction_info['الاختصاص_المكاني'] = "محكمة موطن المدعى عليه أو مكان التنفيذ"
    
    elif value <= 5000:
        jurisdiction_info['المحكمة_المختصة'] = "محكمة الصلح"
        jurisdiction_info['السبب'] = f"قيمة الدعوى ({value:,.0f} دينار) ضمن اختصاص محكمة الصلح"
        jurisdiction_info['المواد_المعنية'] = ["27"]
        jurisdiction_info['الاختصاص_المكاني'] = "محكمة موطن المدعى عليه"
    
    else:
        jurisdiction_info['المحكمة_المختصة'] = "محكمة البداية"
        jurisdiction_info['السبب'] = f"قيمة الدعوى ({value:,.0f} دينار) ضمن اختصاص محكمة البداية"
        jurisdiction_info['المواد_المعنية'] = ["27"]
        jurisdiction_info['الاختصاص_المكاني'] = "محكمة موطن المدعى عليه"
    
    # تحليل الاختصاص المكاني
    if domicile == "خارج المملكة":
        jurisdiction_info['التوصيات'].append("قد يكون الاختصاص للمحاكم الأردنية إذا وجدت علاقة وصلة للمملكة")
        jurisdiction_info['المواد_المعنية'].append("28")
        jurisdiction_info['الاختصاص_المكاني'] = "محكمة موطن المدعي (حسب المادة 47)"
    
    elif domicile == "غير معروف":
        jurisdiction_info['التوصيات'].append("يجب البحث عن آخر موطن معروف للمدعى عليه")
        jurisdiction_info['التوصيات'].append("يمكن اللجوء إلى التبليغ بالنشر إذا تعذر تحديد الموطن")
        jurisdiction_info['الاختصاص_المكاني'] = "محكمة موطن المدعي (حسب المادة 47)"
    
    elif domicile == "متعدد الموطن":
        jurisdiction_info['التوصيات'].append("يمكن رفع الدعوى في أي من المواطن المتعددة")
        jurisdiction_info['الاختصاص_المكاني'] = "أي محكمة يقع في دائرتها أحد مواطن المدعى عليه"
    
    # توصيات إضافية
    if "عقد" in subject:
        jurisdiction_info['التوصيات'].append("يمكن أيضاً رفع الدعوى في مكان تنفيذ العقد (المادة 40)")
        jurisdiction_info['المواد_المعنية'].append("40")
    
    return jurisdiction_info

def display_jurisdiction_analysis(analysis):
    """عرض نتيجة تحليل الاختصاص"""
    
    st.success(f"## 🏛️ المحكمة المختصة: **{analysis['المحكمة_المختصة']}**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"**📋 السبب:** {analysis['السبب']}")
        st.info(f"**📍 الاختصاص المكاني:** {analysis['الاختصاص_المكاني']}")
    
    with col2:
        st.warning("**⚖️ المواد القانونية المعنية:**")
        for article in analysis['المواد_المعنية']:
            st.write(f"• المادة {article}")
    
    if analysis['التوصيات']:
        st.markdown("##### 💡 التوصيات:")
        for recommendation in analysis['التوصيات']:
            st.write(f"• {recommendation}")
            
def show_filing_cases_section():
    show_breadcrumbs("📝 رفع الدعوى واللوائح (المواد 56-60)")
    
    st.markdown("""
    <div class="main-header">
        <h1>📝 رفع الدعوى واللوائح القضائية</h1>
        <p>تحليل شامل لإجراءات رفع الدعوى وتقديم اللوائح وفق المواد 56-60 من قانون أصول المحاكمات المدنية</p>
    </div>
    """, unsafe_allow_html=True)

# ==========================
# 💰 قسم التقييم المالي (48-55)
# ==========================
def show_financial_evaluation_section():
    """قسم التقييم المالي"""
    show_breadcrumbs("💰 التقييم المالي للدعاوى (المواد 48-55)")
    
    st.markdown("""
    <div class="main-header">
        <h1>💰 التقييم المالي للدعاوى</h1>
        <p>تقدير قيمة الدعاوى المختلفة وفق المواد 48-55 من قانون أصول المحاكمات المدنية</p>
    </div>
    """, unsafe_allow_html=True)

    tabs = st.tabs(["📊 التقييم العام (48-50)", "🏠 الدعاوى العقارية (51)", "📝 دعاوى العقود (52)", 
                   "💳 الدعاوى المالية (53-55)", "🧮 حاسبة التقييم", "🎯 أدوات التقدير"])

    with tabs[0]:
        show_general_valuation_articles()
    with tabs[1]:
        show_real_estate_valuation_articles()
    with tabs[2]:
        show_contract_valuation_articles()
    with tabs[3]:
        show_financial_claims_articles()
    with tabs[4]:
        show_valuation_calculator()
    with tabs[5]:
        show_valuation_tools()

def show_general_valuation_articles():
    st.markdown("#### 📊 التقييم العام - المواد 48-50")
    
    general_articles = [
        {
            "number": "48",
            "text": "تقرر قيمة الدعوى باعتبارها يوم إقامتها. وفي جميع الأحوال يكون لتقرير القاعدة حلين الخصوم.",
            "explanation": "تحديد وقت تقدير قيمة الدعوى وهو يوم رفعها، مع إعطاء الخصوم الحق في مناقشة التقدير.",
            "application": "يتم تقدير قيمة الدعوى في تاريخ رفعها وليس في تاريخ وقوع الحق المتنازع عليه."
        },
        {
            "number": "49", 
            "text": "إذا لم تذكر القيمة بالنقد وكان بالإمكان تقريرها بالنقد فقط من قبل رئيس المحكمة.",
            "explanation": "سلطة رئيس المحكمة في تقدير قيمة الدعوى عندما لا تكون القيمة محددة نقداً.",
            "application": "لرئيس المحكمة تقدير قيمة الدعوى غير المحددة بناء على الأدلة المقدمة."
        },
        {
            "number": "50",
            "text": "يحسب في تقدير قيمة الدعوى ما يكون مستحقاً يوم إقامتها من المستحقات والربح والمصروفات وغير ذلك من العلاقات المشتملة القيمة.",
            "explanation": "شمولية التقدير لجميع العناصر المالية المرتبطة بالدعوى.",
            "application": "يشمل التقدير الأصول والأرباح والمصروفات والفوائد المستحقة."
        }
    ]
    
    for article in general_articles:
        with st.expander(f"📊 المادة {article['number']}", expanded=False):
            st.write(f"**النص:** {article['text']}")
            st.info(f"**💡 الشرح:** {article['explanation']}")
            st.success(f"**🎯 التطبيق العملي:** {article['application']}")
    
    # مبادئ التقييم العامة
    st.markdown("##### 📋 مبادئ التقييم العام")
    
    valuation_principles = [
        "تقدير القيمة يوم إقامة الدعوى وليس تاريخ الحق",
        "احتساب جميع المستحقات والمصروفات والفوائد",
        "مراعاة قيمة البناء أو التعديل إذا طلبت إزالته",
        "تقرير القيمة بالنقد إذا أمكن ذلك",
        "حق الخصوم في مناقشة التقدير"
    ]
    
    for principle in valuation_principles:
        st.write(f"• {principle}")

def show_real_estate_valuation_articles():
    st.markdown("#### 🏠 الدعاوى العقارية - المادة 51")
    
    real_estate_articles = [
        {
            "number": "51",
            "text": "الدعاوى المتعلقة بقيمة العقارات تقدم قيمتها بقيمة العقار، وتقدم الدعاوى المتعلقة بالمنقول بقيمته.",
            "explanation": "التفرقة بين تقدير قيمة الدعاوى العقارية (بقيمة العقار) والمنقولات (بقيمة المنقول).",
            "application": "دعاوى الملكية العقارية تقدر بقيمة العقار كاملاً، ودعاوى المنقولات تقدر بقيمة الشيء المنقول."
        }
    ]
    
    for article in real_estate_articles:
        with st.expander(f"🏠 المادة {article['number']}", expanded=False):
            st.write(f"**النص:** {article['text']}")
            st.info(f"**💡 الشرح:** {article['explanation']}")
            st.success(f"**🎯 التطبيق العملي:** {article['application']}")
    
    # أنواع الدعاوى العقارية
    st.markdown("##### 🏠 أنواع الدعاوى العقارية وقيمتها")
    
    real_estate_cases = [
        {
            "النوع": "دعاوى الملكية العقارية",
            "التقييم": "قيمة العقار كاملاً في السوق",
            "الملاحظات": "تقييم السوق الحالي للعقار بما في ذلك الأراضي والمباني"
        },
        {
            "النوع": "دعاوى الانتفاع والإيجار", 
            "التقييم": "قيمة المنفعة أو الإيجار المستحق",
            "الملاحظات": "احتساب القيمة الإيجارية للمدة المتبقية"
        },
        {
            "النوع": "دعاوى الرهن العقاري",
            "التقييم": "قيمة الدين المضمون بالرهن",
            "الملاحظات": "لا تتجاوز قيمة العقار المرهون"
        },
        {
            "النوع": "دعاوى التعدي على العقار",
            "التقييم": "قيمة الضرر الناتج عن التعدي",
            "الملاحظات": "تشمل إزالة التعدي والتعويض عن الأضرار"
        },
        {
            "النوع": "دعاوى تقسيم العقار",
            "التقييم": "قيمة الحصة المطلوبة",
            "الملاحظات": "تقدير قيمة الحصة الشائعة المطلوب تقسيمها"
        }
    ]
    
    for case in real_estate_cases:
        with st.expander(f"🏠 {case['النوع']}", expanded=False):
            st.write(f"**التقييم:** {case['التقييم']}")
            st.write(f"**الملاحظات:** {case['الملاحظات']}")

def show_contract_valuation_articles():
    st.markdown("#### 📝 دعاوى العقود - المادة 52")
    
    contract_articles = [
        {
            "number": "52",
            "text": "إذا كانت الدعوى يطلب فسخ عقد أو إبطاله تقدر قيمتها بقيمة المتعاقد عليه، وبالنسبة لعقود البيع تقدر الدعوى بقيمة آخر الأثمانين.",
            "explanation": "تحديد قيمة دعاوى فسخ العقود بقيمة موضوع العقد، مع خاصية لعقود البيع بأخذ آخر ثمنين.",
            "application": "في عقود البيع، تؤخذ قيمة آخر ثمن تم الاتفاق عليه أو قيمة السوق أيهما أعلى."
        }
    ]
    
    for article in contract_articles:
        with st.expander(f"📝 المادة {article['number']}", expanded=False):
            st.write(f"**النص:** {article['text']}")
            st.info(f"**💡 الشرح:** {article['explanation']}")
            st.success(f"**🎯 التطبيق العملي:** {article['application']}")
    
    # أنواع دعاوى العقود
    st.markdown("##### 📝 تقدير قيمة دعاوى العقود")
    
    contract_cases = [
        {
            "الحالة": "فسخ عقد بيع",
            "التقييم": "قيمة آخر الأثمانين (ثمن العقد أو قيمة السوق)",
            "المثال": "عقد بيع عقار - تؤخذ قيمة السوق الحالية أو ثمن البيع أيهما أعلى"
        },
        {
            "الحالة": "فسخ عقد إيجار",
            "التقييم": "مجموع الإيجار المتبقي للمدة الباقية",
            "المثال": "عقد إيجار 3 سنوات تم تنفيذ سنة - تؤخذ قيمة إيجار السنتين المتبقيتين"
        },
        {
            "الحالة": "إبطال عقد",
            "التقييم": "قيمة الحق المطلوب إبطاله",
            "المثال": "إبطال عقد تبرع - تؤخذ قيمة المال المتبرع به"
        },
        {
            "الحالة": "عقد تم تنفيذ جزء منه",
            "التقييم": "باعتبار المدة الباقية أو الجزء غير المنفذ",
            "المثال": "عقد مقاولة تم تنفيذ 60% منه - تؤخذ قيمة الـ 40% المتبقية"
        },
        {
            "الحالة": "طلب تنفيذ عقد",
            "التقييم": "قيمة الالتزام المطلوب تنفيذه",
            "المثال": "طلب تنفيذ عقد تسليم بضاعة - تؤخذ قيمة البضاعة المتفق عليها"
        }
    ]
    
    for case in contract_cases:
        with st.expander(f"📝 {case['الحالة']}", expanded=False):
            st.write(f"**التقييم:** {case['التقييم']}")
            st.write(f"**المثال:** {case['المثال']}")

def show_financial_claims_articles():
    st.markdown("#### 💳 الدعاوى المالية - المواد 53-55")
    
    financial_articles = [
        {
            "number": "53",
            "text": "إذا كانت الدعوى بين دائن ومدين بشأن إجراء حق على مال تقدر قيمتها بقيمة الدين أو بقيمة المال محل إجراء الحق العيني أيهما أقل.",
            "explanation": "تقييم دعاوى الحقوق العينية بالحد الأدنى بين قيمة الدين وقيمة المال المضمون.",
            "application": "إذا كان الدين 100,000 دينار والعقار المرهون بقيمة 80,000 دينار، تقدر الدعوى بـ 80,000 دينار."
        },
        {
            "number": "54",
            "text": "إذا تضمنت الدعوى طلبات ناشئة عن سبب قانوني واحد كان التقدير باعتبار قيمتها جملة، وإذا كانت ناشئة عن أسباب قانونية مختلفة كان التقدير باعتبار قيمة كل منها على حدة.",
            "explanation": "طريقة تجميع أو تفريق تقدير قيمة الدعاوى المتعددة الطلبات.",
            "application": "الطلبات الناتجة عن حادث واحد تجمع قيمتها، والطلبات المستقلة تحسب كل على حدة."
        },
        {
            "number": "55", 
            "text": "إذا كانت الدعوى يطلب غير قابل للتقدير بحسب القواعد المقررة اعتبرت قيمتها ألف دينار على الأقل.",
            "explanation": "الحد الأدنى لقيمة الدعاوى غير القابلة للتقدير أو غير المحددة القيمة.",
            "application": "الدعاوى المعنوية أو التي لا يمكن تحديد قيمتها بدقة تقدر بألف دينار كحد أدنى."
        }
    ]
    
    for article in financial_articles:
        with st.expander(f"💳 المادة {article['number']}", expanded=False):
            st.write(f"**النص:** {article['text']}")
            st.info(f"**💡 الشرح:** {article['explanation']}")
            st.success(f"**🎯 التطبيق العملي:** {article['application']}")
    
    # حالات خاصة للتقدير
    st.markdown("##### 💰 حالات خاصة للتقدير المالي")
    
    special_cases = [
        "الدعاوى المتعلقة بالحقوق المعنوية: 1,000 دينار حد أدنى",
        "الدعاوى المتعددة من سبب واحد: تجمع قيمتها",
        "الدعاوى المتعددة من أسباب مختلفة: تحسب كل على حدة", 
        "دعاوى الحقوق العينية: تؤخذ الأقل بين قيمة الدين وقيمة المال",
        "الدعاوى غير المحددة القيمة: يترك تقديرها للمحكمة"
    ]
    
    for case in special_cases:
        st.write(f"• {case}")

def show_valuation_calculator():
    st.markdown("#### 🧮 حاسبة التقييم المالي الشاملة")
    
    with st.form("comprehensive_valuation_calculator"):
        st.subheader("تقدير قيمة الدعوى بشكل شامل")
        
        # معلومات أساسية
        col1, col2 = st.columns(2)
        
        with col1:
            case_type = st.selectbox("نوع الدعوى", [
                "دعوى عقارية - ملكية",
                "دعوى عقارية - إيجار", 
                "دعوى تعاقدية - فسخ عقد",
                "دعوى تعاقدية - إبطال عقد",
                "دعوى تعاقدية - تنفيذ عقد",
                "دعوى مالية - دين",
                "دعوى تعويض",
                "دعوى غير مقدرة القيمة",
                "دعوى حق عيني"
            ])
            
            filing_date = st.date_input("تاريخ رفع الدعوى")
            
        with col2:
            court_type = st.selectbox("نوع المحكمة", [
                "محكمة صلح",
                "محكمة بداية",
                "محكمة استئناف",
                "قاضي الأمور المستعجلة"
            ])
            
            valuation_date = st.date_input("تاريخ التقدير", value=datetime.now().date())
        
        # تفاصيل التقييم حسب نوع الدعوى
        st.markdown("##### 📋 تفاصيل التقييم")
        
        if "عقارية" in case_type:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                property_value = st.number_input("قيمة العقار في السوق (دينار)", min_value=0, value=100000)
                land_area = st.number_input("مساحة الأرض (م²)", min_value=0, value=500)
                
            with col2:
                building_area = st.number_input("مساحة البناء (م²)", min_value=0, value=300)
                property_type = st.selectbox("نوع العقار", ["سكني", "تجاري", "زراعي", "صناعي"])
                
            with col3:
                location_factor = st.slider("عامل الموقع", 0.5, 2.0, 1.0, 0.1)
                condition_factor = st.slider("عامل الحالة", 0.5, 1.5, 1.0, 0.1)
        
        elif "تعاقدية" in case_type:
            col1, col2 = st.columns(2)
            
            with col1:
                contract_value = st.number_input("قيمة العقد (دينار)", min_value=0, value=50000)
                contract_duration = st.number_input("مدة العقد (أشهر)", min_value=1, value=12)
                
            with col2:
                executed_portion = st.slider("النسبة المنفذة من العقد (%)", 0, 100, 50)
                remaining_months = st.number_input("الأشهر المتبقية", min_value=0, value=6)
        
        elif "مالية" in case_type or "تعويض" in case_type:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                principal_amount = st.number_input("المبلغ الأصلي (دينار)", min_value=0, value=25000)
                interest_rate = st.number_input("سعر الفائدة (%)", min_value=0.0, value=5.0)
                
            with col2:
                duration_years = st.number_input("مدة الدين (سنوات)", min_value=0, value=2)
                additional_costs = st.number_input("مصاريف إضافية (دينار)", min_value=0, value=1000)
                
            with col3:
                damage_type = st.selectbox("نوع الضرر", ["مادي", "أدبي", "مركب"])
                severity_factor = st.slider("شدة الضرر", 1, 10, 5)
        
        # مطالبات إضافية
        st.markdown("##### ➕ مطالبات إضافية")
        
        col1, col2 = st.columns(2)
        
        with col1:
            additional_claims = st.number_input("مطالبات إضافية (دينار)", min_value=0, value=0)
            legal_fees = st.number_input("أتعاب محاماة متوقعة (دينار)", min_value=0, value=2000)
            
        with col2:
            court_fees = st.number_input("رسوم المحكمة (دينار)", min_value=0, value=500)
            expert_fees = st.number_input("أتعاب الخبراء (دينار)", min_value=0, value=1000)
        
        if st.form_submit_button("🧮 حساب القيمة الشاملة", use_container_width=True):
            valuation_result = calculate_comprehensive_valuation(
                case_type, filing_date, valuation_date, court_type,
                property_value if "عقارية" in case_type else 0,
                contract_value if "تعاقدية" in case_type else 0,
                principal_amount if "مالية" in case_type else 0,
                additional_claims, legal_fees, court_fees, expert_fees,
                locals()  # تمرير جميع المتغيرات المحلية
            )
            display_comprehensive_valuation_result(valuation_result)

def calculate_comprehensive_valuation(case_type, filing_date, valuation_date, court_type,
                                    prop_value, contract_value, principal_amount,
                                    additional_claims, legal_fees, court_fees, expert_fees,
                                    local_vars):
    """حساب تقدير قيمة الدعوى بشكل شامل"""
    
    base_value = 0
    valuation_method = ""
    details = {}
    
    # حساب القيمة الأساسية حسب نوع الدعوى
    if "عقارية - ملكية" in case_type:
        base_value = prop_value
        valuation_method = "قيمة العقار في السوق (المادة 51)"
        details["قيمة العقار"] = prop_value
        if 'location_factor' in local_vars:
            base_value *= local_vars['location_factor']
            details["عامل الموقع"] = local_vars['location_factor']
        if 'condition_factor' in local_vars:
            base_value *= local_vars['condition_factor']
            details["عامل الحالة"] = local_vars['condition_factor']
            
    elif "عقارية - إيجار" in case_type:
        if 'contract_value' in local_vars and 'remaining_months' in local_vars:
            monthly_rent = local_vars['contract_value'] / local_vars['contract_duration']
            base_value = monthly_rent * local_vars['remaining_months']
            valuation_method = "قيمة الإيجار للمدة المتبقية (المادة 52)"
            details["الإيجار الشهري"] = monthly_rent
            details["الأشهر المتبقية"] = local_vars['remaining_months']
            
    elif "فسخ عقد" in case_type:
        base_value = contract_value
        valuation_method = "قيمة المتعاقد عليه (المادة 52)"
        details["قيمة العقد"] = contract_value
        
    elif "إبطال عقد" in case_type:
        base_value = max(prop_value, contract_value)
        valuation_method = "قيمة آخر الأثمانين (المادة 52)"
        details["أعلى قيمة"] = base_value
        
    elif "مالية - دين" in case_type:
        base_value = principal_amount
        if 'interest_rate' in local_vars and 'duration_years' in local_vars:
            interest = principal_amount * (local_vars['interest_rate'] / 100) * local_vars['duration_years']
            base_value += interest
            details["الفائدة"] = interest
        valuation_method = "قيمة الدين مع الفوائد (المادة 53)"
        
    elif "تعويض" in case_type:
        base_value = principal_amount
        if 'severity_factor' in local_vars:
            base_value *= (local_vars['severity_factor'] / 5)  # تعديل حسب شدة الضرر
            details["عامل شدة الضرر"] = local_vars['severity_factor']
        valuation_method = "تقدير التعويض حسب شدة الضرر"
        
    elif "غير مقدرة" in case_type:
        base_value = 1000  # الحد الأدنى حسب المادة 55
        valuation_method = "ألف دينار حد أدنى (المادة 55)"
        
    elif "حق عيني" in case_type:
        base_value = min(principal_amount, prop_value)  # الأقل بين الدين وقيمة المال
        valuation_method = "الأقل بين قيمة الدين وقيمة المال (المادة 53)"
        details["قيمة الدين"] = principal_amount
        details["قيمة المال"] = prop_value
    
    # إضافة المستحقات الإضافية
    total_additional = additional_claims + legal_fees + court_fees + expert_fees
    total_value = base_value + total_additional
    
    # تحديد الاختصاص القضائي
    if total_value <= 5000:
        competent_court = "محكمة الصلح"
    else:
        competent_court = "محكمة البداية"
    
    return {
        'case_type': case_type,
        'base_value': base_value,
        'additional_claims': additional_claims,
        'legal_fees': legal_fees,
        'court_fees': court_fees,
        'expert_fees': expert_fees,
        'total_additional': total_additional,
        'total_value': total_value,
        'valuation_method': valuation_method,
        'competent_court': competent_court,
        'valuation_details': details,
        'filing_date': filing_date,
        'valuation_date': valuation_date
    }

def display_comprehensive_valuation_result(result):
    """عرض نتيجة التقييم الشامل"""
    
    st.success(f"## 💰 نتيجة التقييم: {result['case_type']}")
    
    # عرض النتائج الرئيسية
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("القيمة الأساسية", f"{result['base_value']:,.0f} دينار")
    with col2:
        st.metric("المستحقات الإضافية", f"{result['total_additional']:,.0f} دينار")
    with col3:
        st.metric("القيمة الإجمالية", f"{result['total_value']:,.0f} دينار")
    with col4:
        st.metric("المحكمة المختصة", result['competent_court'])
    
    # التفاصيل
    st.markdown("##### 📊 تفاصيل التقييم")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"**📋 طريقة التقييم:** {result['valuation_method']}")
        st.info(f"**📅 تاريخ الرفع:** {result['filing_date'].strftime('%Y-%m-%d')}")
        st.info(f"**📅 تاريخ التقدير:** {result['valuation_date'].strftime('%Y-%m-%d')}")
        
    with col2:
        if result['valuation_details']:
            st.info("**🔍 تفاصيل الحساب:**")
            for key, value in result['valuation_details'].items():
                st.write(f"• {key}: {value:,.2f}" if isinstance(value, (int, float)) else f"• {key}: {value}")
    
    # تحليل التكاليف
    st.markdown("##### 💸 تحليل التكاليف")
    
    costs_data = {
        "البند": ["القيمة الأساسية", "المطالبات الإضافية", "أتعاب المحاماة", "رسوم المحكمة", "أتعاب الخبراء"],
        "المبلغ (دينار)": [
            result['base_value'],
            result['additional_claims'], 
            result['legal_fees'],
            result['court_fees'],
            result['expert_fees']
        ]
    }
    
    costs_df = pd.DataFrame(costs_data)
    st.dataframe(costs_df, use_container_width=True, hide_index=True)
    
    # توصيات
    st.markdown("##### 💡 التوصيات والإجراءات")
    
    recommendations = []
    
    if result['total_value'] <= 5000:
        recommendations.append("الدعوى ضمن اختصاص محكمة الصلح - إجراءات مبسطة")
    else:
        recommendations.append("الدعوى ضمن اختصاص محكمة البداية - إجراءات قياسية")
    
    if result['legal_fees'] > 5000:
        recommendations.append("أتعاب المحاماة مرتفعة - يوصى بالتفاوض على سعر مناسب")
    
    if result['expert_fees'] > 0:
        recommendations.append("تحتاج لتقارير خبراء - يوصى باختيار خبير معتمد")
    
    if result['total_value'] > 100000:
        recommendations.append("قيمة الدعوى كبيرة - يوصى بتقديم تامين مناسب إذا لزم الأمر")
    
    for rec in recommendations:
        st.write(f"• {rec}")

def show_valuation_tools():
    st.markdown("#### 🎯 أدوات التقدير المساعدة")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("##### 🏠 حاسبة العقارات")
        with st.form("real_estate_calculator"):
            property_type = st.selectbox("نوع العقار", ["شقة", "فيلا", "أرض", "محل تجاري"])
            area = st.number_input("المساحة (م²)", min_value=1, value=150)
            location = st.selectbox("الموقع", ["مركز المدينة", "ضاحية", "ريف", "منطقة صناعية"])
            age = st.number_input("العمر (سنوات)", min_value=0, value=5)
            condition = st.select_slider("الحالة", options=["قديم", "متوسط", "جيد", "ممتاز"])  # تم التصحيح هنا
            
            if st.form_submit_button("🏠 تقدير قيمة العقار", use_container_width=True):
                estimated_value = estimate_property_value(property_type, area, location, age, condition)
                st.success(f"**القيمة المقدرة:** {estimated_value:,.0f} دينار")
    
    with col2:
        st.markdown("##### 💼 حاسبة التعويضات")
        with st.form("compensation_calculator"):
            damage_type = st.selectbox("نوع الضرر", ["مادي", "أدبي", "فوات منفعة", "إصابة عمل"])
            base_amount = st.number_input("المبلغ الأساسي (دينار)", min_value=0, value=10000)
            duration = st.number_input("المدة (أشهر)", min_value=0, value=12)
            severity = st.select_slider("شدة الضرر", options=["بسيط", "متوسط", "شديد", "بالغ"])
            
            if st.form_submit_button("💼 تقدير التعويض", use_container_width=True):
                estimated_compensation = estimate_compensation(damage_type, base_amount, duration, severity)
                st.success(f"**التعويض المقدر:** {estimated_compensation:,.0f} دينار")
    
    # أدوات إضافية
    st.markdown("##### 📈 أدوات تحليل إضافية")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📋 نموذج تقدير القيمة", use_container_width=True):
            show_valuation_template()
    
    with col2:
        if st.button("💾 حفظ التقدير", use_container_width=True):
            st.success("تم حفظ التقدير بنجاح")
    
    with col3:
        if st.button("🖨️ تصدير التقرير", use_container_width=True):
            st.success("جاري تصدير التقرير...")

def estimate_property_value(prop_type, area, location, age, condition):
    """تقدير قيمة العقار"""
    base_prices = {
        "شقة": 800,
        "فيلا": 1200, 
        "أرض": 500,
        "محل تجاري": 1000
    }
    
    location_factors = {
        "مركز المدينة": 1.5,
        "ضاحية": 1.2,
        "ريف": 0.8,
        "منطقة صناعية": 0.9
    }
    
    condition_factors = {
        "قديم": 0.6,
        "متوسط": 0.8,
        "جيد": 1.0,
        "ممتاز": 1.2
    }
    
    age_factor = max(0.5, 1 - (age * 0.02))  # انخفاض 2% سنوياً
    
    base_price = base_prices.get(prop_type, 500)
    location_factor = location_factors.get(location, 1.0)
    condition_factor = condition_factors.get(condition, 1.0)
    
    estimated_value = base_price * area * location_factor * condition_factor * age_factor
    
    return estimated_value

def estimate_compensation(damage_type, base_amount, duration, severity):
    """تقدير التعويض"""
    severity_factors = {
        "بسيط": 0.5,
        "متوسط": 1.0,
        "شديد": 2.0,
        "بالغ": 3.0
    }
    
    type_factors = {
        "مادي": 1.0,
        "أدبي": 1.5,
        "فوات منفعة": 1.2,
        "إصابة عمل": 2.0
    }
    
    severity_factor = severity_factors.get(severity, 1.0)
    type_factor = type_factors.get(damage_type, 1.0)
    duration_factor = 1 + (duration / 12) * 0.1  # زيادة طفيفة مع زيادة المدة
    
    estimated_compensation = base_amount * severity_factor * type_factor * duration_factor
    
    return estimated_compensation

def show_valuation_template():
    """عرض نموذج تقدير القيمة"""
    template = """
    📊 نموذج تقدير قيمة الدعوى
    
    معلومات الدعوى:
    - نوع الدعوى: __________
    - رقم الدعوى: __________
    - المحكمة: __________
    - تاريخ الرفع: __________
    
    تفاصيل التقدير:
    - القيمة الأساسية: __________ دينار
    - المستحقات الإضافية: __________ دينار
    - أتعاب المحاماة: __________ دينار
    - رسوم المحكمة: __________ دينار
    - أتعاب الخبراء: __________ دينار
    - الإجمالي: __________ دينار
    
    طريقة التقدير:
    - الأساس القانوني: __________
    - طريقة الحساب: __________
    - الملاحظات: __________
    
    المحكمة المختصة: __________
    
    المقدم: __________
    التاريخ: __________
    """
    
    st.text_area("📋 النموذج الجاهز", value=template, height=400)

# ==========================
# 📝 قسم رفع الدعوى واللوائح (56-60)
# ==========================
def show_filing_cases_section():
    """قسم رفع الدعوى واللوائح"""
    show_breadcrumbs("📝 رفع الدعوى واللوائح (المواد 56-60)")
    
    st.markdown("""
    <div class="main-header">
        <h1>📝 رفع الدعوى واللوائح القضائية</h1>
        <p>تحليل شامل لإجراءات رفع الدعوى وتقديم اللوائح وفق المواد 56-60 من قانون أصول المحاكمات المدنية</p>
    </div>
    """, unsafe_allow_html=True)

    tabs = st.tabs(["📄 لائحة الدعوى (56-58)", "📝 اللوائح الجوابية (59)", "⚡ الدعاوى المستعجلة (60)", "🎯 أدوات رفع الدعوى"])

    with tabs[0]:
        show_plaintiff_articles()
    with tabs[1]:
        show_defense_articles()
    with tabs[2]:
        show_urgent_cases_articles()
    with tabs[3]:
        show_filing_tools()

def show_plaintiff_articles():
    st.markdown("#### 📄 لائحة الدعوى - المواد 56-58")
    
    plaintiff_articles = [
        {
            "number": "56",
            "text": "تقدم الدعوى بناء على طلب المدعي بعريضة توقع قلم المحكمة ما لم ينص القانون على غير ذلك. ويجب أن تشتمل العريضة على البيانات التالية: اسم المحكمة، أسماء الخصوم ومواصفاتهم، موضوع الدعوى، وقائع الدعوى وأسبابها وطلبات المدعي، وتوقيع المدعي أو وكيله، وتاريخ تقديم الدعوى.",
            "explanation": "الشروط الشكلية والموضوعية لعريضة الدعوى التي يجب توافرها لقبول الدعوى.",
            "application": "يجب أن تكون العريضة مكتملة البيانات وإلا رفضت شكلاً. يجب تضمين كافة المعلومات المطلوبة قانوناً."
        },
        {
            "number": "57",
            "text": "على المدعي أن يرفق بعريضة الدعوى قائمة بالبينات والمستندات المؤيدة لدعواه، وقائمة بأسماء الشهود ومحال إقامتهم. ويسقط حق المدعي في تقديم أي بينة أخرى إذا لم يقدمها مع عريضة الدعوى.",
            "explanation": "إلزامية إرفاق كافة البينات والمستندات مع عريضة الدعوى ابتداء.",
            "application": "يجب تقديم كافة الأدلة مع العريضة، ولا يقبل تقديم أدلة جديدة لاحقاً إلا في حالات استثنائية."
        },
        {
            "number": "58",
            "text": "تسلم عريضة الدعوى وملحقاتها من قبل قلم المحكمة في ملف خاص، وتسلم صورة من العريضة وملحقاتها إلى المدعى عليه للتبليغ.",
            "explanation": "إجراءات حفظ وتوثيق عريضة الدعوى وملحقاتها في سجلات المحكمة.",
            "application": "يقوم كاتب المحكمة بحفظ أصول الأوراق وتسليم صور للمدعى عليه للتبليغ."
        }
    ]
    
    for article in plaintiff_articles:
        with st.expander(f"📄 المادة {article['number']}", expanded=False):
            st.write(f"**النص:** {article['text']}")
            st.info(f"**💡 الشرح:** {article['explanation']}")
            st.success(f"**🎯 التطبيق العملي:** {article['application']}")
    
    # بيانات لائحة الدعوى الإلزامية
    st.markdown("##### 📋 البيانات الإلزامية في لائحة الدعوى")
    
    mandatory_data = [
        "اسم المحكمة المرفوعة أمامها الدعوى",
        "اسم المدعي الكامل وعنوانه ووسائل الاتصال",
        "اسم المدعى عليه الكامل وعنوانه ووسائل الاتصال", 
        "موضوع الدعوى بشكل واضح ومحدد",
        "وقائع الدعوى مرتبة ترتيباً زمنياً",
        "الأسباب القانونية للدعوى",
        "الطلبات المقدمة بشكل مفصل",
        "توقيع المدعي أو وكيله",
        "تاريخ تقديم الدعوى",
        "قائمة البينات والمستندات المؤيدة",
        "قائمة الشهود ومحال إقامتهم"
    ]
    
    for data in mandatory_data:
        st.write(f"• {data}")

def show_defense_articles():
    st.markdown("#### 📝 اللوائح الجوابية - المادة 59")
    
    defense_articles = [
        {
            "number": "59",
            "text": "على المدعى عليه أن يقدم إلى قلم المحكمة خلال ثلاثين يوماً من اليوم التالي لتاريخ تبليغه عريضة الدعوى جواباً كتابياً على هذه العريضة، ويرفق به قائمة بالبينات والمستندات المؤيدة لدفاعه وقائمة بأسماء الشهود. وإذا لم يقدم المدعى عليه جواباً كتابياً خلال المدة تعتبر المحكمة بأنه قد اطلع على عريضة الدعوى وبلغ بها.",
            "explanation": "الموعد القانوني لتقديم اللائحة الجوابية والآثار المترتبة على عدم تقديمها.",
            "application": "يمنح المدعى عليه 30 يوماً لتقديم رد مفصل على الدعوى مع أدلته، وإلا اعتبر مقراً بالوقائع."
        }
    ]
    
    for article in defense_articles:
        with st.expander(f"📝 المادة {article['number']}", expanded=False):
            st.write(f"**النص:** {article['text']}")
            st.info(f"**💡 الشرح:** {article['explanation']}")
            st.success(f"**🎯 التطبيق العملي:** {article['application']}")
    
    # محتويات اللائحة الجوابية
    st.markdown("##### 📋 مكونات اللائحة الجوابية")
    
    defense_components = [
        {
            "البند": "الرد على الوقائع",
            "الوصف": "الرد المنظم على كل واقعة من وقائع الدعوى بالقبول أو الرفض",
            "الأهمية": "تحديد النقاط المتفق والمختلف عليها"
        },
        {
            "البند": "الدفوع",
            "الوصف": "الدفوع الشكلية والموضوعية التي يعتمدها المدعى عليه",
            "الأهمية": "قد تؤدي إلى رفض الدعوى شكلاً أو موضوعاً"
        },
        {
            "البند": "الطلبات الفرعية", 
            "الوصف": "الطلبات المقابلة أو الطلبات العارضة",
            "الأهمية": "الحصول على أحكام لصالح المدعى عليه"
        },
        {
            "البند": "قائمة البينات",
            "الوصف": "المستندات والأدلة المؤيدة للدفاع",
            "الأهمية": "إثبات صحة دفوع المدعى عليه"
        },
        {
            "البند": "قائمة الشهود",
            "الوصف": "أسماء وعناوين الشهود المدلى بشهادتهم",
            "الأهمية": "إثبات الوقائع التي يعتمد عليها المدعى عليه"
        }
    ]
    
    for component in defense_components:
        with st.expander(f"📝 {component['البند']}", expanded=False):
            st.write(f"**الوصف:** {component['الوصف']}")
            st.write(f"**الأهمية:** {component['الأهمية']}")

def show_urgent_cases_articles():
    st.markdown("#### ⚡ الدعاوى المستعجلة - المادة 60")
    
    urgent_articles = [
        {
            "number": "60",
            "text": "في الدعاوى التي تحال إلى القضاء المستعجل يعين القاضي جلسة المحاكمة فور قيد الدعوى دون حاجة لتبادل اللوائح. وتعتبر الدعوى مستعجلة إذا اقتصر طلب المدعي فيها على استيفاء مبلغ مالي مستحق عليه من المدعى عليه بناء على عقد أو سند أو كفالة.",
            "explanation": "تبسيط إجراءات الدعاوى المستعجلة والإسراع في الفصل فيها.",
            "application": "يتم الفصل في الدعاوى المستعجلة بسرعة دون التقيد بالإجراءات العادية."
        }
    ]
    
    for article in urgent_articles:
        with st.expander(f"⚡ المادة {article['number']}", expanded=False):
            st.write(f"**النص:** {article['text']}")
            st.info(f"**💡 الشرح:** {article['explanation']}")
            st.success(f"**🎯 التطبيق العملي:** {article['application']}")
    
    # أنواع الدعاوى المستعجلة
    st.markdown("##### ⚡ أنواع الدعاوى المستعجلة")
    
    urgent_cases_types = [
        {
            "النوع": "دعاوى السندات التنفيذية",
            "الوصف": "الدعاوى المستندة إلى سندات ذات قوة تنفيذية",
            "المدة": "تُفصل خلال 15 يوماً"
        },
        {
            "النوع": "دعاوى الكمبيالات والشيكات",
            "الوصف": "المطالبة بمستحقات من الكمبيالات والشيكات",
            "المدة": "تُفصل خلال 15 يوماً"
        },
        {
            "النوع": "دعاوى الكفالات",
            "الوصف": "المطالبة بتنفيذ التزامات الكفالة",
            "المدة": "تُفصل خلال 15 يوماً"
        },
        {
            "النوع": "الدعاوى المستعجلة العادية",
            "الوصف": "أي دعوى يقرر القاضي أنها مستعجلة",
            "المدة": "تُفصل خلال 30 يوماً"
        }
    ]
    
    for case_type in urgent_cases_types:
        with st.expander(f"⚡ {case_type['النوع']}", expanded=False):
            st.write(f"**الوصف:** {case_type['الوصف']}")
            st.write(f"**المدة المتوقعة:** {case_type['المدة']}")

def show_filing_tools():
    st.markdown("#### 🎯 أدوات رفع الدعوى")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("##### 📄 منشئ لائحة الدعوى")
        with st.form("plaintiff_builder"):
            court_name = st.text_input("اسم المحكمة")
            plaintiff_name = st.text_input("اسم المدعي")
            defendant_name = st.text_input("اسم المدعى عليه")
            case_subject = st.text_area("موضوع الدعوى")
            case_facts = st.text_area("وقائع الدعوى")
            legal_basis = st.text_area("الأسباب القانونية")
            requests = st.text_area("الطلبات")
            
            if st.form_submit_button("📄 إنشاء لائحة الدعوى", use_container_width=True):
                lawsuit_draft = generate_lawsuit_draft(
                    court_name, plaintiff_name, defendant_name, 
                    case_subject, case_facts, legal_basis, requests
                )
                st.text_area("📄 مسودة لائحة الدعوى", value=lawsuit_draft, height=400)
    
    with col2:
        st.markdown("##### 📝 منشئ اللائحة الجوابية")
        with st.form("defense_builder"):
            response_type = st.selectbox("نوع الرد", [
                "الرد التفصيلي على الوقائع",
                "الدفوع الشكلية",
                "الدفوع الموضوعية", 
                "الطلبات المقابلة",
                "الرد الشامل"
            ])
            main_defenses = st.text_area("الدفوع الرئيسية")
            counter_requests = st.text_area("الطلبات المقابلة (إن وجدت)")
            evidence_list = st.text_area("قائمة الأدلة والدفوع")
            
            if st.form_submit_button("📝 إنشاء اللائحة الجوابية", use_container_width=True):
                defense_draft = generate_defense_draft(
                    response_type, main_defenses, counter_requests, evidence_list
                )
                st.text_area("📝 مسودة اللائحة الجوابية", value=defense_draft, height=400)
    
    # حاسبة مواعيد اللوائح
    st.markdown("##### ⏰ حاسبة مواعيد اللوائح")
    
    with st.form("deadline_calculator_filing"):
        col1, col2 = st.columns(2)
        
        with col1:
            notification_date = st.date_input("تاريخ تبليغ لائحة الدعوى")
            case_type = st.selectbox("نوع الدعوى", ["عادية", "مستعجلة", "تجارية", "عقارية"])
            
        with col2:
            defendant_type = st.selectbox("نوع المدعى عليه", [
                "فرد",
                "جهة حكومية", 
                "شركة خاصة",
                "مؤسسة عامة"
            ])
            has_attorney = st.checkbox("هل المدعى عليه ممثل بمحام؟")
        
        if st.form_submit_button("⏰ حساب المواعيد", use_container_width=True):
            deadlines = calculate_filing_deadlines(
                notification_date, case_type, defendant_type, has_attorney
            )
            display_filing_deadlines(deadlines)

def generate_lawsuit_draft(court, plaintiff, defendant, subject, facts, basis, requests):
    """إنشاء مسودة لائحة دعوى"""
    
    draft = f"""
    عريضة دعوى
    المحكمة: {court}
    
    المدعي: {plaintiff}
    المدعى عليه: {defendant}
    
    الموضوع: {subject}
    
    وقائع الدعوى:
    {facts}
    
    الأسباب القانونية:
    {basis}
    
    الطلبات:
    {requests}
    
    المرفقات:
    - قائمة البينات والمستندات
    - قائمة الشهود
    - صور من المستندات المؤيدة
    
    توقيع المدعي/الوكيل:
    ___________________
    التاريخ: __________
    """
    
    return draft

def generate_defense_draft(response_type, defenses, counter_requests, evidence):
    """إنشاء مسودة لائحة جوابية"""
    
    draft = f"""
    لائحة جوابية
    نوع الرد: {response_type}
    
    الدفوع الرئيسية:
    {defenses}
    
    الطلبات المقابلة:
    {counter_requests}
    
    الأدلة والدفوع:
    {evidence}
    
    المرفقات:
    - قائمة البينات المؤيدة للدفاع
    - قائمة الشهود
    - صور من المستندات الدفاعية
    
    توقيع المدعى عليه/الوكيل:
    ___________________
    التاريخ: __________
    """
    
    return draft

def calculate_filing_deadlines(notification_date, case_type, defendant_type, has_attorney):
    """حساب مواعيد تقديم اللوائح"""
    
    base_days = 30  # المدة الأساسية للائحة الجوابية
    
    # تعديل المدة حسب نوع الدعوى
    if case_type == "مستعجلة":
        base_days = 15
    elif case_type == "تجارية":
        base_days = 30
    elif case_type == "عقارية":
        base_days = 30
    
    # تعديل المدة حسب نوع المدعى عليه
    if defendant_type == "جهة حكومية":
        base_days = 60
    elif defendant_type == "مؤسسة عامة":
        base_days = 45
    
    # تعديل المدة حسب وجود محام
    if not has_attorney:
        base_days += 15  # إضافة وقت إضافي إذا لم يكن هناك محام
    
    deadline_date = notification_date + timedelta(days=base_days)
    remaining_days = (deadline_date - datetime.now().date()).days
    
    return {
        'notification_date': notification_date,
        'deadline_days': base_days,
        'deadline_date': deadline_date,
        'remaining_days': remaining_days,
        'case_type': case_type,
        'defendant_type': defendant_type
    }

def display_filing_deadlines(deadlines):
    """عرض مواعيد تقديم اللوائح"""
    
    st.success(f"## ⏰ المواعيد القانونية لتقديم اللوائح")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info(f"**تاريخ التبليغ:** {deadlines['notification_date'].strftime('%Y-%m-%d')}")
        st.info(f"**نوع الدعوى:** {deadlines['case_type']}")
        
    with col2:
        st.info(f"**المدة القانونية:** {deadlines['deadline_days']} يوم")
        st.info(f"**نوع المدعى عليه:** {deadlines['defendant_type']}")
        
    with col3:
        st.info(f"**آخر موعد للتقديم:** {deadlines['deadline_date'].strftime('%Y-%m-%d')}")
        st.info(f"**الأيام المتبقية:** {deadlines['remaining_days']} يوم")
    
    # تحذيرات
    if deadlines['remaining_days'] < 0:
        st.error("⚠️ انتهى الموعد القانوني لتقديم اللائحة الجوابية!")
    elif deadlines['remaining_days'] <= 7:
        st.warning("🚨 الموعد النهائي يقترب! يوصى بتقديم اللائحة فوراً.")
    elif deadlines['remaining_days'] <= 15:
        st.warning("⚠️ أقل من أسبوعين متبقيان، يوصى بالإسراع في إعداد اللائحة.")

# ==========================
# ⚖️ قسم إجراءات المحاكمة (61-87)
# ==========================
def show_trial_procedures_section():
    """قسم إجراءات المحاكمة"""
    show_breadcrumbs("⚖️ إجراءات المحاكمة (المواد 61-87)")
    
    st.markdown("""
    <div class="main-header">
        <h1>⚖️ إجراءات المحاكمة والإثبات</h1>
        <p>تحليل شامل لجلسات المحاكمة والإثبات والخبرة وفق المواد 61-87 من قانون أصول المحاكمات المدنية</p>
    </div>
    """, unsafe_allow_html=True)

    tabs = st.tabs(["📅 جلسات المحاكمة (61-75)", "👥 الإثبات بالبينة (76-82)", "🔍 الخبرة والكشف (83-87)", 
                   "⚡ الإجراءات المستعجلة", "🎯 أدوات المحاكمة", "📋 نماذج الإجراءات"])

    with tabs[0]:
        show_trial_sessions_articles()
    with tabs[1]:
        show_evidence_procedures_articles()
    with tabs[2]:
        show_expertise_procedures_articles()
    with tabs[3]:
        show_urgent_trial_procedures()
    with tabs[4]:
        show_trial_tools()
    with tabs[5]:
        show_trial_templates()

def show_trial_sessions_articles():
    st.markdown("#### 📅 جلسات المحاكمة - المواد 61-75")
    
    trial_articles = [
        {
            "number": "61",
            "text": "يعلن الحضور أمام محكمة الصلح والبداية والاستئناف، كما يجوز في حالة الضرورة للقاضي أن يمدد هذا الميعاد إلى سبعة أيام.",
            "explanation": "تنظيم مواعيد الحضور أمام المحاكم المختلفة مع إمكانية التمديد في حالات الضرورة.",
            "application": "يتم تحديد موعد الجلسة الأولى خلال مدة معينة ويمكن تمديدها إذا اقتضت الضرورة."
        },
        {
            "number": "62",
            "text": "يكون القرار الوجاهي في الدعوى المستعجلة بقرار من المحكمة أو قاضي الأمور المستعجلة.",
            "explanation": "اختصاص المحكمة أو قاضي المستعجلات في الفصل وجاهياً في الدعاوى المستعجلة.",
            "application": "يتم الفصل في الطلبات المستعجلة بسرعة وبحضور الأطراف."
        },
        {
            "number": "63",
            "text": "لا يجوز للمدعين (من غير المحامين) أن يحضروا أمام المحاكم للخصومة إلا بواسطة محامين مؤهلين بمقتضى سند توكيل.",
            "explanation": "إلزامية التوكيل بالمحامين في المرافعة أمام المحاكم.",
            "application": "يجب على الأفراد تعيين محامٍ للترافع عنهم إلا في حالات استثنائية."
        },
        {
            "number": "64",
            "text": "يحدد صدور التوكيل من أحد الخصوم يكون موطن وكيله أو عنوان بريده الإلكتروني مقراً لتبليغ الأوراق المتعلقة بالدعوى.",
            "explanation": "اعتبار موطن المحامى مقراً لتبليغ جميع الأوراق المتعلقة بالدعوى.",
            "application": "يتم تبليغ المحامي بجميع الأوراق والإجراءات نيابة عن موكله."
        },
        {
            "number": "65",
            "text": "التوكيل بالخصومة يكون التوكيل ساري المفعول للقيام بالإجراءات والطلبات المتعلقة برفع الدعوى وممارستها حتى يعتبر الحكم في موضوعها.",
            "explanation": "سريان مفعول التوكيل طوال مدة الدعوى حتى الفصل فيها.",
            "application": "يظل التوكيل ساري المفعول حتى انتهاء الدعوى بما في ذلك الطعون."
        },
        {
            "number": "66",
            "text": "يجوز لأي فريق ينوب عنه محام أن يعزل محاميه في أي دور من أدوار المحاكمة، ويجوز للمحامي أن يتنحل عن الدعوى بإذن من المحكمة.",
            "explanation": "حق الخصم في عزل محاميه وحق المحامي في التنحي عن الدعوى.",
            "application": "يمكن عزل المحامي أو تنحيه بشروط وإجراءات محددة."
        },
        {
            "number": "67",
            "text": "لا تجري المحاكمة إلا حضورياً أو بمثابة الحضوري. وإذا حضر أحد الأطراف في أول جلسة ثم تغيب بعد ذلك دون عذر مقبول، تعتبر المحاكمة حضورية بحقه.",
            "explanation": "أنواع المحاكمة (حضورية/غيابية) وآثار الحضور في الجلسة الأولى.",
            "application": "الحضور في الجلسة الأولى يحول المحاكمة إلى حضورية حتى مع التغيب اللاحق."
        },
        {
            "number": "68",
            "text": "يجوز للمدعي إلى المدعى عليه أن يبدي في الجلسة التي يحضر فيها خصمه طلبات جديدة، أو أن يزيد أو ينقص في الطلبات الأولى.",
            "explanation": "حق الأطراف في تعديل طلباتهم وتقديم طلبات جديدة أثناء المحاكمة.",
            "application": "يمكن تعديل الطلبات شريطة ألا يسبب ضرراً للخصم الآخر."
        },
        {
            "number": "69",
            "text": "إذا تبين للمحكمة عند غياب المدعى عليه أن تبليغه ناقص، يجب عليها تأجيل الدعوى إلى جلسة ثانية وتبليغه التبليغ الصحيح.",
            "explanation": "إلزامية إعادة التبليغ في حالة عدم صحة التبليغ الأول.",
            "application": "المحكمة ملزمة بتأجيل الدعوى وإعادة التبليغ إذا كان التبليغ ناقصاً."
        },
        {
            "number": "70",
            "text": "يجوز اتحاد أكثر من مدع في دعوى واحدة إذا كان الحق الذي يطالبون به متعلقاً بفعل واحد أو مجموعة واحدة من الأفعال.",
            "explanation": "جواز انضمام أكثر من مدع في دعوى واحدة عند اتحاد السبب.",
            "application": "يجوز انضمام المتضررين من فعل واحد في دعوى جماعية."
        },
        {
            "number": "71",
            "text": "يجوز للمحكمة في غير الجلسة الأولى عقد جلساتها في غياب الخصوم بعد التأكد من تبليغهم.",
            "explanation": "جواز عقد الجلسات في غياب الخصوم بعد التأكد من تبليغهم بشكل صحيح.",
            "application": "يمكن للمحكمة متابعة الإجراءات في غياب الخصوم بعد التبليغ الصحيح."
        },
        {
            "number": "72",
            "text": "تغريم المحكمة على من يتخلف من موظفيها أو من الخصوم عن لوازم المستندات أو القيام بأي إجراء من إجراءات المرافعة.",
            "explanation": "سلطة المحكمة في فرض الغرامات على المتخلفين عن الإجراءات.",
            "application": "يمكن فرض غرامة على من يتخلف عن تقديم المستندات المطلوبة."
        },
        {
            "number": "73",
            "text": "كبيرة الجلسة واجباتها ملحوظة برئيسها، وللرئيس أن يخرج من الجلسة كل من يخل بنظامها.",
            "explanation": "سلطة رئيس الجلسة في حفظ النظام وإخراج من يخل به.",
            "application": "لرئيس الجلسة الحق في إخراج أي شخص يخل بنظام الجلسة."
        },
        {
            "number": "74",
            "text": "يجب رئيس الجلسة بعبارة موجزة عن كل جريمة تقع أثناء انعقادها وما يرى اتخاذه من إجراءات التحقيق.",
            "explanation": "إلزامية تحرير محضر عن الجرائم التي تقع أثناء انعقاد الجلسة.",
            "application": "يتم تحرير محضر مفصل عن أي حادث يقع أثناء الجلسة."
        },
        {
            "number": "75",
            "text": "للمحكمة ولو من تلقاء نفسها أن تأمر بإلغاء البيانات الجارحة أو المخلة بالنظام العام من أي ورقة من أوراق المرافعات.",
            "explanation": "سلطة المحكمة في حذف العبارات المسيئة أو المخلة بالأدب من الأوراق.",
            "application": "يمكن للمحكمة حذف أي عبارات غير لائقة من مذكرات الأطراف."
        }
    ]
    
    # عرض المواد في مجموعات
    st.markdown("##### 📅 المواد 61-67: التنظيم العام للمحاكمة")
    for article in trial_articles[:7]:
        with st.expander(f"📌 المادة {article['number']}", expanded=False):
            st.write(f"**النص:** {article['text']}")
            st.info(f"**💡 الشرح:** {article['explanation']}")
            st.success(f"**🎯 التطبيق العملي:** {article['application']}")
    
    st.markdown("##### 🔄 المواد 68-75: إجراءات الجلسات والطلبات")
    for article in trial_articles[7:]:
        with st.expander(f"📌 المادة {article['number']}", expanded=False):
            st.write(f"**النص:** {article['text']}")
            st.info(f"**💡 الشرح:** {article['explanation']}")
            st.success(f"**🎯 التطبيق العملي:** {article['application']}")

def show_evidence_procedures_articles():
    st.markdown("#### 👥 الإثبات بالبينة - المواد 76-82")
    
    evidence_articles = [
        {
            "number": "76",
            "text": "تسمع المحكمة ما يبديه الخصوم أو وكلاؤهم شفاهة من طلبات أو دفوع في محضر الجلسة، ويكون المدعى عليه آخر من يتكلم.",
            "explanation": "ترتيب المرافعة الشفوية وإعطاء المدعى عليه الحق في الكلمة الأخيرة.",
            "application": "يتم سماع المرافعات الشفوية وتسجيلها في المحضر، ويتكلم المدعى عليه أخيراً."
        },
        {
            "number": "77",
            "text": "في ما عدا حالة الضرورة التي يجب إثبات المستندات فيها في المحضر، لا يجوز للمحكمة تأجيل الدعوى لمدة تزيد على ستة عشر يوماً.",
            "explanation": "تنظيم مدة التأجيلات في المحاكمة مع استثناء حالات الضرورة.",
            "application": "لا يمكن تأجيل الدعوى أكثر من 16 يوماً إلا في حالات استثنائية."
        },
        {
            "number": "78",
            "text": "للخصوم أن يطلبوا إلى المحكمة في أي حالة تكون عليها الدعوى إثبات ما اتفقوا عليه من صلح أو أي اتفاق آخر في محضر الجلسة.",
            "explanation": "إمكانية إثبات الاتفاقات والصلح بين الأطراف في محضر الجلسة.",
            "application": "يمكن للأطراف طلب تسجيل اتفاق الصلح في المحضر ليكون له قوة الحكم."
        },
        {
            "number": "79",
            "text": "في حال تحقيقات قانون أجنبي، يجوز للمحكمة أن تكلف الخصوم بتقديم النصوص التي يستندون إليها مترجمة ترجمة رسمية.",
            "explanation": "تنظيم إجراءات التحقيق بالقانون الأجنبي وضرورة الترجمة الرسمية.",
            "application": "يجب تقديم النصوص الأجنبية مترجمة ترجمة رسمية معتمدة."
        },
        {
            "number": "80",
            "text": "يجوز كتابة محضر المحاكمة باليد أو بواسطة الحاسوب أو الآلات الإلكترونية ويوقع عليه مع قضاة المحكمة.",
            "explanation": "طرق كتابة محضر الجلسات وأهمية توقيع القضاة عليه.",
            "application": "يمكن كتابة المحاضر يدوياً أو إلكترونياً مع التوقيع عليها."
        },
        {
            "number": "81",
            "text": "يحلف الشاهد قبل الإدلاء بشهادته اليمين القانونية. ويسجل المحكمة أقواله دون سماع الشهود الذين لم تسمع شهاداتهم.",
            "explanation": "إجراءات تحليف الشهود اليمين وتسجيل شهاداتهم.",
            "application": "يتم تحليف الشاهد اليمين قبل الشهادة وتسجيل أقواله بدقة."
        },
        {
            "number": "82",
            "text": "على الفريق الذي يطلب إصدار مذكرة حضور شاهد أن يدفع إلى المحكمة المبلغ الذي تراه المحكمة كافياً لتسديد مصاريف ذهاب الشاهد وإيابه.",
            "explanation": "التزام من يطلب استدعاء الشهود بدفع مصاريف حضورهم.",
            "application": "يدفع طالب استدعاء الشاهد مصاريف تنقلاته ومكافأته."
        }
    ]
    
    for article in evidence_articles:
        with st.expander(f"👥 المادة {article['number']}", expanded=False):
            st.write(f"**النص:** {article['text']}")
            st.info(f"**💡 الشرح:** {article['explanation']}")
            st.success(f"**🎯 التطبيق العملي:** {article['application']}")
    
    # طرق الإثبات
    st.markdown("##### 📋 طرق الإثبات في المحاكمة")
    
    evidence_methods = [
        {
            "الطريقة": "الإثبات بالكتابة",
            "الوصف": "العقود والمستندات الخطية الرسمية والعرفية",
            "القوة": "أقوى طرق الإثبات إذا كانت رسمية"
        },
        {
            "الطريقة": "شهادة الشهود", 
            "الوصف": "الإدلاء بالشهادة تحت اليمين القانونية",
            "القوة": "لإثبات الوقائع التي لا يشترط إثباتها كتابة"
        },
        {
            "الطريقة": "القرائن",
            "الوصف": "الاستدلال بوقائع ثابتة على وقائع غير ثابتة",
            "القوة": "تستخدم عندما لا يتوفر إثبات مباشر"
        },
        {
            "الطريقة": "الخبرة",
            "الوصف": "استعانة المحكمة بأهل الخبرة المتخصصين",
            "القوة": "في المسائل الفنية والعلمية المتخصصة"
        },
        {
            "الطريقة": "المعاينة",
            "الوصف": "انتقال المحكمة لمشاهدة مكان النزاع",
            "القوة": "للتحقق من الوقائع المادية مباشرة"
        }
    ]
    
    for method in evidence_methods:
        with st.expander(f"📋 {method['الطريقة']}", expanded=False):
            st.write(f"**الوصف:** {method['الوصف']}")
            st.write(f"**القوة الإثباتية:** {method['القوة']}")

def show_expertise_procedures_articles():
    st.markdown("#### 🔍 الخبرة والكشف - المواد 83-87")
    
    expertise_articles = [
        {
            "number": "83",
            "text": "للمحكمة في أي دور من أدوار المحاكمة أن تقرر إجراء كشف أو خبرة على أي مال منقول أو غير منقول، وعليها أن تبين في قرارها الأسباب الداعية لإجراء الكشف والخبرة.",
            "explanation": "سلطة المحكمة في تعيين الخبراء وتكليفهم بمهام محددة.",
            "application": "تصدر المحكمة قراراً مسبباً بتعيين الخبير وتحديد مهمته."
        },
        {
            "number": "84",
            "text": "إذا اتفق الخصوم على تسمية الخبير ووافقت المحكمة على تسميته، تتولى المحكمة انتخاب الخبير من بين الأسماء الواردة في جدول الخبراء.",
            "explanation": "إجراءات اختيار الخبير ومراعاة اتفاق الأطراف إن أمكن.",
            "application": "يمكن للأطراف اقتراح أسماء الخبراء مع احتفاظ المحكمة بحق الموافقة."
        },
        {
            "number": "85", 
            "text": "يجب على الخبير التقيد بما يلي: عدم تسلم أي وثائق من الخصوم إلا عبر المحكمة، إعلام المحكمة بأي صعوبات، عدم الإفصاح عن التقرير قبل تقديمه.",
            "explanation": "الواجبات والالتزامات الملقاة على عاتق الخبير.",
            "application": "يجب على الخبير الالتزام بالحياد وإعلام المحكمة بأي معوقات."
        },
        {
            "number": "86",
            "text": "إذا لم يقدم الخبير تقريره في الوقت المحدد، وجب عليه أن يقدم عذراً للمحكمة مع بيان الأعمال التي قام بها.",
            "explanation": "التزام الخبير بتقديم التقرير في المدة المحددة.",
            "application": "يجب على الخبير تقديم تقرير في الوقت المحدد أو تبرير التأخير."
        },
        {
            "number": "87",
            "text": "ينظر التزوير أو انتحال الأسماء على الوثائق والمستندات غير الرسمية. وإذا ثبت التزوير تحكم المحكمة على المزور بغرامة.",
            "explanation": "معاقبة التزوير وانتحال الشخصية في المستندات.",
            "application": "يعاقب المزور بغرامة مالية وقد تصل العقوبة إلى الحبس."
        }
    ]
    
    for article in expertise_articles:
        with st.expander(f"🔍 المادة {article['number']}", expanded=False):
            st.write(f"**النص:** {article['text']}")
            st.info(f"**💡 الشرح:** {article['explanation']}")
            st.success(f"**🎯 التطبيق العملي:** {article['application']}")
    
    # أنواع الخبرات
    st.markdown("##### 🔬 أنواع الخبرات القضائية")
    
    expertise_types = [
        {
            "النوع": "خبرة هندسية",
            "المجالات": "البناء، المقاولات، التخطيط العمراني",
            "المدة": "2-4 أشهر"
        },
        {
            "النوع": "خبرة محاسبية",
            "المجالات": "الحسابات، التقييم المالي، التدقيق",
            "المدة": "1-3 أشهر"
        },
        {
            "النوع": "خبرة طبية",
            "المجالات": "الإصابات، العجز، الأضرار الصحية",
            "المدة": "2-6 أشهر"
        },
        {
            "النوع": "خبرة فنية",
            "المجالات": "الآلات، التقنيات، الصناعات",
            "المدة": "1-3 أشهر"
        },
        {
            "النوع": "خبرة عقارية",
            "المجالات": "التقييم، التحديد، التقسيم",
            "المدة": "1-2 أشهر"
        }
    ]
    
    for exp_type in expertise_types:
        with st.expander(f"🔬 {exp_type['النوع']}", expanded=False):
            st.write(f"**المجالات:** {exp_type['المجالات']}")
            st.write(f"**المدة المتوسطة:** {exp_type['المدة']}")

def show_urgent_trial_procedures():
    st.markdown("#### ⚡ الإجراءات المستعجلة في المحاكمة")
    
    st.markdown("""
    <div class="article-box">
    <h4>🎯 الإجراءات المستعجلة وفق القانون</h4>
    <p>تنص المواد على مجموعة من الإجراءات المستعجلة التي يمكن للمحكمة اتخاذها لضمان سير العدالة وحماية حقوق الأطراف.</p>
    </div>
    """, unsafe_allow_html=True)
    
    urgent_procedures = [
        {
            "الإجراء": "التبليغ الفوري",
            "الوصف": "إجراء التبليغ في غير الأوقات الرسمية في حالات الضرورة",
            "الشروط": "موافقة كتابية من المحكمة، وجود ضرورة قصوى"
        },
        {
            "الإجراء": "تأجيل الجلسات العاجل",
            "الوصف": "تأجيل الجلسة لأسباب طارئة ومقبولة",
            "الشروط": "أسباب قاهرة، تقديم طلب مسبب"
        },
        {
            "الإجراء": "الخبرة المستعجلة", 
            "الوصف": "إجراء الخبرة بشكل عاجل لحماية الأدلة",
            "الشروط": "خوف من ضياع أو تلف الأدلة"
        },
        {
            "الإجراء": "سماع الشهود المستعجل",
            "الوصف": "سماع شهادة الشهود بشكل عاجل",
            "الشروط": "خوف من عدم تمكن الشاهد من الحضور لاحقاً"
        },
        {
            "الإجراء": "الإثبات المستعجل",
            "الوصف": "إثبات الوقائع بشكل عاجل قبل ضياعها",
            "الشروط": "وجود خطر محدق على الأدلة"
        }
    ]
    
    for procedure in urgent_procedures:
        with st.expander(f"⚡ {procedure['الإجراء']}", expanded=False):
            st.write(f"**الوصف:** {procedure['الوصف']}")
            st.write(f"**الشروط:** {procedure['الشروط']}")

def show_trial_tools():
    st.markdown("#### 🎯 أدوات المحاكمة المتقدمة")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("##### 📅 منظم الجلسات")
        with st.form("session_organizer"):
            case_number = st.text_input("رقم الدعوى")
            next_session = st.date_input("موعد الجلسة القادمة")
            session_type = st.selectbox("نوع الجلسة", [
                "جلسة مرافعة",
                "جلسة سماع شهود", 
                "جلسة مناقشة تقرير خبير",
                "جلسة النطق بالحكم"
            ])
            required_documents = st.text_area("المستندات المطلوبة")
            
            if st.form_submit_button("💾 حفظ بيانات الجلسة", use_container_width=True):
                st.success("✅ تم حفظ بيانات الجلسة بنجاح!")
    
    with col2:
        st.markdown("##### 👥 منظم الشهود")
        with st.form("witness_organizer"):
            witness_name = st.text_input("اسم الشاهد")
            witness_type = st.selectbox("نوع الشهادة", ["شهادة حضر", "شهادة كتابية", "شهادة خبير"])
            testimony_subject = st.text_area("موضوع الشهادة")
            session_date = st.date_input("موعد الشهادة")
            
            if st.form_submit_button("📋 إضافة الشاهد", use_container_width=True):
                st.success("✅ تم إضافة الشاهد إلى القائمة!")
    
    # حاسبة تكاليف المحاكمة
    st.markdown("##### 💰 حاسبة تكاليف المحاكمة")
    
    with st.form("trial_costs_calculator"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            sessions_count = st.number_input("عدد الجلسات المتوقعة", min_value=1, value=5)
            witnesses_count = st.number_input("عدد الشهود", min_value=0, value=3)
            expertise_needed = st.checkbox("هل تحتاج خبرة؟")
            
        with col2:
            lawyer_fees = st.number_input("أتعاب المحامي الشهرية (دينار)", min_value=0, value=1000)
            duration_months = st.number_input("المدة المتوقعة (أشهر)", min_value=1, value=6)
            translation_needed = st.checkbox("هل تحتاج ترجمة؟")
            
        with col3:
            court_fees = st.number_input("رسوم المحكمة (دينار)", min_value=0, value=500)
            other_costs = st.number_input("مصاريف أخرى (دينار)", min_value=0, value=1000)
        
        if st.form_submit_button("🧮 حساب التكاليف", use_container_width=True):
            total_costs = calculate_trial_costs(
                sessions_count, witnesses_count, expertise_needed,
                lawyer_fees, duration_months, translation_needed,
                court_fees, other_costs
            )
            display_trial_costs(total_costs)

def calculate_trial_costs(sessions, witnesses, expertise, lawyer_fees, duration, translation, court_fees, other_costs):
    """حساب تكاليف المحاكمة"""
    
    costs = {
        'أتعاب المحامي': lawyer_fees * duration,
        'رسوم المحكمة': court_fees,
        'مصاريف الجلسات': sessions * 50,  # افتراضي 50 دينار للجلسة
        'مصاريف الشهود': witnesses * 100,  # افتراضي 100 دينار للشاهد
        'مصاريف أخرى': other_costs
    }
    
    if expertise:
        costs['أتعاب الخبراء'] = 2000  # افتراضي 2000 دينار للخبرة
    
    if translation:
        costs['الترجمة'] = 500  # افتراضي 500 دينار للترجمة
    
    total = sum(costs.values())
    
    return {
        'costs_breakdown': costs,
        'total_cost': total,
        'estimated_duration': duration
    }

def display_trial_costs(costs_result):
    """عرض نتائج حساب تكاليف المحاكمة"""
    
    st.success(f"## 💰 التكاليف الإجمالية: {costs_result['total_cost']:,.0f} دينار")
    
    st.markdown("##### 📊 تفصيل التكاليف:")
    costs_df = pd.DataFrame({
        "البند": list(costs_result['costs_breakdown'].keys()),
        "المبلغ (دينار)": list(costs_result['costs_breakdown'].values())
    })
    
    st.dataframe(costs_df, use_container_width=True, hide_index=True)
    
    # مخطط التكاليف
    fig, ax = plt.subplots()
    ax.pie(costs_result['costs_breakdown'].values(), labels=costs_result['costs_breakdown'].keys(), autopct='%1.1f%%')
    ax.set_title('توزيع تكاليف المحاكمة')
    st.pyplot(fig)
    
    st.info(f"**⏰ المدة المتوقعة:** {costs_result['estimated_duration']} أشهر")

def show_trial_templates():
    st.markdown("#### 📋 نماذج إجراءات المحاكمة")
    
    templates = [
        {
            "name": "📄 نموذج محضر جلسة",
            "description": "نموذج شامل لمحضر الجلسات القضائية",
            "content": """
            محضر الجلسة
            المحكمة: __________
            الدعوى رقم: __________
            التاريخ: __________
            القضاة الحاضرون: __________
            
            الحضور:
            - المدعي/وكيله: __________
            - المدعى عليه/وكيله: __________
            
            الإجراءات:
            1. __________
            2. __________
            3. __________
            
            القرارات:
            - __________
            - __________
            
            موعد الجلسة القادمة: __________
            
            توقيع القاضي: __________
            توقيع الكاتب: __________
            """
        },
        {
            "name": "👥 نموذج استدعاء شاهد",
            "description": "نموذج لاستدعاء الشهود للحضور للإدلاء بشهادتهم",
            "content": """
            استدعاء شاهد
            المحكمة: __________
            الدعوى رقم: __________
            الموضوع: __________
            
            السيد/__________
            العنوان: __________
            
            تطلب منكم المحكمة الحضور في:
            التاريخ: __________
            الوقت: __________
            المكان: __________
            
            للإدلاء بشهادتكم في الدعوى المذكورة أعلاه.
            
            رئيس المحكمة: __________
            التاريخ: __________
            """
        },
        {
            "name": "🔍 نموذج طلب خبرة",
            "description": "نموذج لطلب تعيين خبير في الدعوى",
            "content": """
            طلب تعيين خبير
            المحكمة: __________
            الدعوى رقم: __________
            المدعي: __________
            المدعى عليه: __________
            
            الموضوع: طلب تعيين خبير
            
            المطلوب:
            - تعيين خبير في مجال __________
            - المهمة: __________
            - المدة: __________
            
            الأسباب:
            - __________
            - __________
            
            توقيع الطالب: __________
            التاريخ: __________
            """
        },
        {
            "name": "⚡ نموذج طلب مستعجل",
            "description": "نموذج للطلبات المستعجلة في الدعوى",
            "content": """
            طلب مستعجل
            المحكمة: __________
            الدعوى رقم: __________
            
            الموضوع: طلب __________ مستعجل
            
            الوقائع:
            - __________
            - __________
            
            أسباب الاستعجال:
            - __________
            - __________
            
            الطلب:
            - __________
            - __________
            
            توقيع الطالب: __________
            التاريخ: __________
            """
        }
    ]
    
    for template in templates:
        with st.expander(f"{template['name']} - {template['description']}", expanded=False):
            st.text_area("النموذج", value=template['content'], height=300, key=f"template_{template['name']}")
            
            col1, col2 = st.columns(2)
            with col1:
                st.download_button("📥 تحميل النموذج", template['content'], 
                                 file_name=f"{template['name']}.txt", key=f"download_{template['name']}")
            with col2:
                if st.button("🎯 استخدام النموذج", key=f"use_{template['name']}"):
                    st.success("تم نسخ النموذج إلى الحافظة")

# ==========================
# 🔍 قسم التحقيق والمضاهاة (88-107)
# ==========================
def show_investigation_verification_section():
    """قسم التحقيق والمضاهاة"""
    show_breadcrumbs("🔍 التحقيق والمضاهاة (المواد 88-107)")
    
    st.markdown("""
    <div class="main-header">
        <h1>🔍 التحقيق والمضاهاة</h1>
        <p>إجراءات التحقيق والتحقق من المستندات والتوقيعات وفق المواد 88-107 من قانون أصول المحاكمات المدنية</p>
    </div>
    """, unsafe_allow_html=True)

    tabs = st.tabs(["🖋️ التحقيق بالمضاهاة (88-99)", "📄 المستندات والإبراز (100-107)", "🔬 أدوات التحقيق"])

    with tabs[0]:
        show_handwriting_investigation_articles()
    with tabs[1]:
        show_documents_production_articles()
    with tabs[2]:
        show_investigation_tools()

def show_handwriting_investigation_articles():
    st.markdown("#### 🖋️ التحقيق بالمضاهاة - المواد 88-99")
    
    investigation_articles = [
        {
            "number": "88",
            "text": "إذا ادعى أحد الطرفين تزوير توقيع أو خط أو ختم في مستند معين، جاز للمحكمة بناء على طلب ذوي الشأن أن تقرر إجراء تحقيق بالمضاهاة والاستكتاب.",
            "explanation": "الأسس القانونية لطلب إجراء تحقيق في التزوير بالمضاهاة.",
            "application": "يقدم طلب التحقيق بالمضاهاة عندما يدعي أحد الأطراف تزوير توقيع أو خط في مستند."
        },
        {
            "number": "89",
            "text": "تنظم المحكمة محضراً تبين فيه حالة الوثيقة وأوصافها يوقعها قضاة الجلسة مع الكاتب، كما توقع الوثيقة نفسها من رئيس الجلسة.",
            "explanation": "إجراءات توثيق حالة الوثيقة المشكوك في صحتها.",
            "application": "يتم تحرير محضر مفصل يصف حالة الوثيقة ويوقع عليه القضاة والكاتب."
        },
        {
            "number": "90",
            "text": "تنتدب المحكمة أحد قضاتها للإشراف على إجراءات التحقيق والمضاهاة وسماع الشهود إذا اقتضت الحالة.",
            "explanation": "تعيين قاضي منتدب للإشراف على إجراءات التحقيق.",
            "application": "ينتدب قاضي لمتابعة إجراءات التحقيق والمضاهاة بشكل مباشر."
        },
        {
            "number": "91",
            "text": "يحدد الخبراء الزمان والمكان الذين عينتهما المحكمة للتحقيق، وبعد أن يحلفوا اليمين يؤدون عملهم بدقة وأمانة.",
            "explanation": "التزام الخبراء باليمين والتقيد بالزمان والمكان المحددين.",
            "application": "يحلف الخبراء اليمين القانونية قبل البدء بأعمال التحقيق."
        },
        {
            "number": "92",
            "text": "على الخصم أن يمين النماذج التي يعتبرها صالحة للتحقيق والمضاهاة ويسلمها إلى الخبراء في الزمان والمكان المحددين.",
            "explanation": "إلزامية تقديم نماذج المقارنة للتحقيق بالمضاهاة.",
            "application": "يقدم الطرف طالب التحقيق النماذج التي يعتبرها صالحة للمقارنة."
        },
        {
            "number": "93",
            "text": "إذا تعذر الحصول على النماذج في مكان اجتماع الخبراء، يتنقل القاضي مع الخبراء والطرفين إلى مكان وجودها.",
            "explanation": "إجراءات الانتقال لمكان وجود النماذج عند تعذر إحضارها.",
            "application": "ينتقل القاضي والخبراء لمكان النماذج إذا تعذر إحضارها."
        },
        {
            "number": "94",
            "text": "إذا تعذر الحصول على نماذج كافية للتحقيق، يستكتب المدعى عليه التوقيع عبارات بعينها ثم يقابلون ما كان بخط السند والتوقيع.",
            "explanation": "إجراءات الاستكتاب عند عدم توفر نماذج كافية للمقارنة.",
            "application": "يكتب المدعى عليه نماذج كتابية أمام الخبراء للمقارنة."
        },
        {
            "number": "95",
            "text": "للخبراء أن يستمعوا إلى أقوال من ذكر لهم لهم معرفة بالمدعى عليه وهو يكتب الوثيقة أو السند المدعى أو شاهدوه وهو يضع إمضاء عليه.",
            "explanation": "سماع أقوال الشهود في إجراءات التحقيق بالمضاهاة.",
            "application": "يسمع الخبراء شهادة من لديه معرفة بخط أو توقيع المدعى عليه."
        },
        {
            "number": "96",
            "text": "بعد الانتهاء من التحقيق والمضاهاة والاستكتاب وسماع الأقوال، يجب على الخبراء أن ينظموا تقريراً يبينون فيه إجراءات التحقيق ويقررون ما إذا كان الخط أو الإمضاء للمدعى عليه أم لا.",
            "explanation": "إلزامية تقديم تقرير مفصل بنتائج التحقيق.",
            "application": "يقدم الخبراء تقريراً مفصلاً بنتائج التحقيق وأسبابها."
        },
        {
            "number": "97",
            "text": "بعد تقديم التقرير إلى المحكمة، يبلغ كل من الطرفين نسخة عنه، وللمحكمة أن تحمي الخبير للمناقشة.",
            "explanation": "إجراءات مناقشة تقرير الخبراء والطعن فيه.",
            "application": "تبلغ الأطراف بنسخ من التقرير ويمكن مناقشة الخبير حوله."
        },
        {
            "number": "98",
            "text": "على مدعي التزوير أن يدفع سلفة ما تقرره المحكمة لمصاريف التحقيق والمضاهاة.",
            "explanation": "التزام مدعي التزوير بدفع مصاريف التحقيق مقدماً.",
            "application": "يدفع طالب التحقيق مصاريف التحقيق مقدماً كتأمين."
        },
        {
            "number": "99",
            "text": "إذا ادعى أن السند المدعى عليه مزور وطلب إلى المحكمة التحقيق في ذلك، وكانت هناك دلائل تؤيد الادعاء، جاز للمحكمة أن تأمر بكفالة مؤقتة.",
            "explanation": "إمكانية طلب كفالة مؤقتة في دعاوى التزوير.",
            "application": "يمكن للمحكمة طلب كفالة مؤقتة إذا وجدت دلائل على صحة الادعاء بالتزوير."
        }
    ]
    
    # عرض المواد في مجموعات
    st.markdown("##### 🖋️ المواد 88-94: إجراءات بدء التحقيق")
    for article in investigation_articles[:7]:
        with st.expander(f"🖋️ المادة {article['number']}", expanded=False):
            st.write(f"**النص:** {article['text']}")
            st.info(f"**💡 الشرح:** {article['explanation']}")
            st.success(f"**🎯 التطبيق العملي:** {article['application']}")
    
    st.markdown("##### 📊 المواد 95-99: إجراءات الخبراء والنتائج")
    for article in investigation_articles[7:]:
        with st.expander(f"🖋️ المادة {article['number']}", expanded=False):
            st.write(f"**النص:** {article['text']}")
            st.info(f"**💡 الشرح:** {article['explanation']}")
            st.success(f"**🎯 التطبيق العملي:** {article['application']}")

def show_documents_production_articles():
    st.markdown("#### 📄 المستندات والإبراز - المواد 100-107")
    
    documents_articles = [
        {
            "number": "100",
            "text": "يجوز للمحكمة أن تأمر أي فريق أن يبرز في حياته أو تحت تحريمه من مستندات ترى أنها ضرورية للفصل في الدعوى.",
            "explanation": "سلطة المحكمة في إلزام الأطراف بإبراز المستندات.",
            "application": "يمكن للمحكمة إلزام أي طرف بتقديم مستندات بحوزته تكون ضرورية للفصل في الدعوى."
        },
        {
            "number": "101",
            "text": "يجوز لأي فريق في الدعوى أن يطلب إلى المحكمة أن تلزم الفريق الآخر بتكلفيه إبراز أي مستندات أشار إليها في اللائحة ولم يبرزها.",
            "explanation": "حق الأطراف في طلب إلزام الخصم بإبراز المستندات.",
            "application": "يمكن طلب إلزام الخصم بتقديم مستندات ذكرها في لوائحه ولم يقدمها."
        },
        {
            "number": "102",
            "text": "على الفريق الذي يوجه إليه الطلب أن يعطي الفريق الذي طلبه مهلة من تاريخ تبلغه الطلب كتابياً لا تتجاوز تسعة أيام لإبراز المستندات.",
            "explanation": "المدة القانونية للاستجابة لطلب إبراز المستندات.",
            "application": "يمنح الطرف المهلة 9 أيام للاستجابة لطلب إبراز المستندات."
        },
        {
            "number": "103",
            "text": "إذا امتنع الفريق عن الإبراز بمقتضى المادة 101، جاز للمحكمة بأنه على طلب الفريق الطالب أن تحكم قراراً بوجوب الإبراز.",
            "explanation": "جزاء الامتناع عن إبراز المستندات المطلوبة.",
            "application": "تصدر المحكمة قراراً ملزماً بالإبراز في حالة الامتناع."
        },
        {
            "number": "104",
            "text": "إذا طلب أحد الفريقين الاطلاع على مستندات محفوظة عند الفريق الآخر ولم يشر إليها في اللائحة، يجب عنه أن يبين المستندات التي يجوز له الاطلاع عليها.",
            "explanation": "تنظيم طلبات الاطلاع على المستندات غير المذكورة في اللوائح.",
            "application": "يمكن طلب الاطلاع على مستندات لم تذكر في اللوائح مع بيان أسباب ذلك."
        },
        {
            "number": "105",
            "text": "إذا قدم أحد الخصوم طلباً للاطلاع على دفاتر مصرف أو تاجر، جاز للمحكمة أن تأمر بتقديم نسخة من أي قيد من القيود المثبتة فيها.",
            "explanation": "إجراءات الاطلاع على الدفاتر التجارية والمصرفية.",
            "application": "يمكن للمحكمة إلزام المصارف والتجار بتقديم نسخ من دفاترهم."
        },
        {
            "number": "106",
            "text": "إذا قدم طلب لإصدار قرار بالاطلاع على مستندات محفوظة لدى النيابة العامة، فيجوز للمحكمة تقدير ما إذا كان الإبراز متبعاً من صحة الدعوى.",
            "explanation": "تنظيم الاطلاع على المستندات المحفوظة لدى النيابة العامة.",
            "application": "يخضع إبراز المستندات المحفوظة لدى النيابة لتقدير المحكمة."
        },
        {
            "number": "107",
            "text": "إذا تخلف أي فريق عن الامتثال للأمر بإبراز مستند أو إجراء الاطلاع عليه، فإنه يعرض دعواه للرفض إذا كان مدعياً، ويعرض دفاعه للرفض إذا كان مدعى عليه.",
            "explanation": "الجزاءات المترتبة على عدم الامتثال لأمر الإبراز.",
            "application": "رفض الدعوى أو الدفاع في حالة عدم الامتثال لأمر الإبراز."
        }
    ]
    
    for article in documents_articles:
        with st.expander(f"📄 المادة {article['number']}", expanded=False):
            st.write(f"**النص:** {article['text']}")
            st.info(f"**💡 الشرح:** {article['explanation']}")
            st.success(f"**🎯 التطبيق العملي:** {article['application']}")

def show_investigation_tools():
    st.markdown("#### 🔬 أدوات التحقيق والمضاهاة")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("##### 🖋️ محلل التزوير")
        with st.form("forgery_analyzer"):
            document_type = st.selectbox("نوع المستند", [
                "عقد",
                "شيك",
                "كمبيالة", 
                "إقرار",
                "توقيع",
                "مستند رسمي"
            ])
            suspicion_basis = st.text_area("أسباب الشك في التزوير")
            available_samples = st.checkbox("هل تتوفر نماذج للمقارنة؟")
            witness_available = st.checkbox("هل يوجد شهود على التوقيع؟")
            
            if st.form_submit_button("🔍 تحليل إمكانية التحقيق", use_container_width=True):
                analysis = analyze_forgery_case(
                    document_type, suspicion_basis, available_samples, witness_available
                )
                display_forgery_analysis(analysis)
    
    with col2:
        st.markdown("##### 📄 منشئ طلب التحقيق")
        with st.form("investigation_request_builder"):
            disputed_element = st.selectbox("العنصر المتنازع عليه", [
                "التوقيع",
                "خط اليد", 
                "الختم",
                "التاريخ",
                "المحتوى"
            ])
            evidence_details = st.text_area("تفاصيل الأدلة على التزوير")
            comparison_samples = st.text_area("النماذج المتاحة للمقارنة")
            
            if st.form_submit_button("📄 إنشاء طلب التحقيق", use_container_width=True):
                request_draft = generate_investigation_request(
                    disputed_element, evidence_details, comparison_samples
                )
                st.text_area("📄 مسودة طلب التحقيق", value=request_draft, height=300)
    
    # حاسبة تكاليف التحقيق
    st.markdown("##### 💰 حاسبة تكاليف التحقيق")
    
    with st.form("investigation_costs_calculator"):
        col1, col2 = st.columns(2)
        
        with col1:
            experts_count = st.number_input("عدد الخبراء", min_value=1, max_value=3, value=2)
            investigation_type = st.selectbox("نوع التحقيق", [
                "تحقيق بسيط",
                "تحقيق متوسط",
                "تحقيق معقد",
                "تحقيق فني متقدم"
            ])
            
        with col2:
            sessions_estimated = st.number_input("الجلسات المتوقعة", min_value=1, value=3)
            travel_required = st.checkbox("هل يتطلب الانتقال؟")
            technical_tools = st.checkbox("هل يحتاج لأدوات فنية متخصصة؟")
        
        if st.form_submit_button("💰 حساب التكاليف", use_container_width=True):
            costs = calculate_investigation_costs(
                experts_count, investigation_type, sessions_estimated, travel_required, technical_tools
            )
            display_investigation_costs(costs)

def analyze_forgery_case(doc_type, suspicion, samples, witnesses):
    """تحليل حالة التزوير وإمكانية إجراء التحقيق"""
    
    analysis = {
        'feasibility': '',
        'required_evidence': [],
        'estimated_duration': '',
        'success_probability': '',
        'recommendations': []
    }
    
    # تحليل الجدوى
    if samples and witnesses:
        analysis['feasibility'] = "عالية"
        analysis['success_probability'] = "70-90%"
    elif samples or witnesses:
        analysis['feasibility'] = "متوسطة" 
        analysis['success_probability'] = "50-70%"
    else:
        analysis['feasibility'] = "منخفضة"
        analysis['success_probability'] = "30-50%"
    
    # الأدلة المطلوبة
    if not samples:
        analysis['required_evidence'].append("نماذج كتابية للمقارنة")
    if not witnesses:
        analysis['required_evidence'].append("شهود على التوقيع أو الخط")
    
    # المدة المتوقعة
    if doc_type in ["عقد", "مستند رسمي"]:
        analysis['estimated_duration'] = "2-4 أشهر"
    else:
        analysis['estimated_duration'] = "1-3 أشهر"
    
    # التوصيات
    analysis['recommendations'].append("تقديم طلب تحقيق فوري")
    if not samples:
        analysis['recommendations'].append("جمع نماذج كتابية للمقارنة")
    if not witnesses:
        analysis['recommendations'].append("البحث عن شهود على التوقيع")
    
    return analysis

def display_forgery_analysis(analysis):
    """عرض نتيجة تحليل التزوير"""
    
    st.success(f"## 🔍 نتيجة التحليل: جدوى {analysis['feasibility']}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"**📊 احتمالية النجاح:** {analysis['success_probability']}")
        st.info(f"**⏰ المدة المتوقعة:** {analysis['estimated_duration']}")
        
    with col2:
        if analysis['required_evidence']:
            st.warning("**📋 الأدلة المطلوبة:**")
            for evidence in analysis['required_evidence']:
                st.write(f"• {evidence}")
    
    if analysis['recommendations']:
        st.markdown("##### 💡 التوصيات:")
        for recommendation in analysis['recommendations']:
            st.write(f"• {recommendation}")

def generate_investigation_request(element, evidence, samples):
    """إنشاء مسودة طلب تحقيق"""
    
    request = f"""
    طلب إجراء تحقيق بالمضاهاة
    العنصر المتنازع عليه: {element}
    
    الأدلة على التزوير:
    {evidence}
    
    النماذج المتاحة للمقارنة:
    {samples}
    
    الطلبات:
    1. تعيين خبير في الخطوط والتوقيعات
    2. إجراء تحقيق بالمضاهاة والاستكتاب
    3. سماع الشهود إن وجدوا
    4. تقديم تقرير مفصل بنتائج التحقيق
    
    الأسباب:
    - الشك في صحة {element} المدعى تزويره
    - توفر أدلة على التزوير
    - أهمية المستند في الفصل في الدعوى
    
    المرفقات:
    - صورة من المستند المتنازع عليه
    - صور من النماذج المتاحة للمقارنة
    - قائمة الشهود إن وجدوا
    
    توقيع الطالب:
    ___________________
    التاريخ: __________
    """
    
    return request

def calculate_investigation_costs(experts, inv_type, sessions, travel, technical):
    """حساب تكاليف التحقيق"""
    
    base_costs = {
        'أتعاب الخبراء': experts * 1000,
        'رسوم المحكمة': 500,
        'مصاريف الجلسات': sessions * 200
    }
    
    # تعديل حسب نوع التحقيق
    type_multipliers = {
        "تحقيق بسيط": 1.0,
        "تحقيق متوسط": 1.5, 
        "تحقيق معقد": 2.0,
        "تحقيق فني متقدم": 3.0
    }
    
    multiplier = type_multipliers.get(inv_type, 1.0)
    
    # تعديل التكاليف
    for key in base_costs:
        base_costs[key] *= multiplier
    
    # إضافة تكاليف إضافية
    if travel:
        base_costs['مصاريف الانتقال'] = 300
    if technical:
        base_costs['أدوات فنية متخصصة'] = 500
    
    total = sum(base_costs.values())
    
    return {
        'costs_breakdown': base_costs,
        'total_cost': total,
        'experts_count': experts,
        'investigation_type': inv_type
    }

def display_investigation_costs(costs):
    """عرض تكاليف التحقيق"""
    
    st.success(f"## 💰 التكاليف الإجمالية: {costs['total_cost']:,.0f} دينار")
    
    st.markdown("##### 📊 تفصيل التكاليف:")
    costs_df = pd.DataFrame({
        "البند": list(costs['costs_breakdown'].keys()),
        "المبلغ (دينار)": list(costs['costs_breakdown'].values())
    })
    
    st.dataframe(costs_df, use_container_width=True, hide_index=True)
    
    st.info(f"**👥 عدد الخبراء:** {costs['experts_count']}")
    st.info(f"**🔬 نوع التحقيق:** {costs['investigation_type']}")

# ==========================
# 📋 قسم الطلبات والدفوع (108-140)
# ==========================
def show_extended_requests_defenses_section():
    """قسم الطلبات والدفوع"""
    show_breadcrumbs("📋 الطلبات والدفوع (المواد 108-140)")
    
    st.markdown("""
    <div class="main-header">
        <h1>📋 الطلبات والدفوع الموسعة</h1>
        <p>الدفوع المتخصصة، الوقف والسقوط، رد القضاة، والدفوع المالية وفق المواد 108-140 من قانون أصول المحاكمات المدنية</p>
    </div>
    """, unsafe_allow_html=True)

    tabs = st.tabs(["🚫 الدفوع الشكلية (108-111)", "⏸️ الوقف والسقوط (122-126)", "⚖️ رد القضاة (132-140)", "💰 الدفوع المالية (127-131)", "🎯 أدوات الدفوع"])

    with tabs[0]:
        show_formal_defenses_articles()
    with tabs[1]:
        show_suspension_dismissal_articles()
    with tabs[2]:
        show_judges_recusal_articles()
    with tabs[3]:
        show_financial_defenses_articles()
    with tabs[4]:
        show_defenses_tools()

def show_formal_defenses_articles():
    st.markdown("#### 🚫 الدفوع الشكلية - المواد 108-111")
    
    formal_defenses_articles = [
        {
            "number": "108",
            "text": "للمدعى عليه قبل التعرض لموضوع الدعوى أن يطلب من المحكمة إصدار الحكم بأي من الدفوع التالية شريطة أن يذكر جميع ما يرغب بالتذرع بها منها في طلب واحد: عدم الاختصاص النوعي، وجود شرط تحكيم، سقوط الخصومة، خلل في إجراءات رفع الدعوى.",
            "explanation": "الدفوع الشكلية التي يجب إثارتها قبل الدخول في موضوع الدعوى.",
            "application": "يجب تقديم الدفوع الشكلية في بداية الدعوى قبل مناقشة الموضوع."
        },
        {
            "number": "109",
            "text": "على المحكمة أن تفصل في الطلبات المتعلقة بعدم الاختصاص النوعي ووجود شرط التحكيم، ولها أن تفصل في طلب سقوط الخصومة أو أن تؤجل الفصل فيه إلى الموضوع.",
            "explanation": "إجراءات الفصل في الدفوع الشكلية.",
            "application": "تفصل المحكمة في بعض الدفوع فوراً وفي أخرى تؤجلها للموضوع."
        },
        {
            "number": "110",
            "text": "الدفوع بعدم الاختصاص النوعي أو بوجود شرط التحكيم يجب إثارتها قبل إبداء أي دفع أو طلب آخر في الدعوى وإلا سقط الحق فيها.",
            "explanation": "مواعيد إثارة الدفوع الشكلية وآثار عدم إثارتها في الوقت المناسب.",
            "application": "يسقط الحق في هذه الدفوع إذا لم تثار في أول جلسة."
        },
        {
            "number": "111",
            "text": "الدفوع بعدم اختصاص المحكمة أو المرتبطة بسبب نوع الدعوى أو قيمتها أو بعدم جواز نظرها لسبق الفصل فيها يجوز التذرع بها في أي حالة تكون عليها الدعوى.",
            "explanation": "الدفوع التي يجوز إثارتها في أي مرحلة من مراحل الدعوى.",
            "application": "بعض الدفوع لا تسقط ويمكن إثارتها في أي وقت."
        }
    ]
    
    for article in formal_defenses_articles:
        with st.expander(f"🚫 المادة {article['number']}", expanded=False):
            st.write(f"**النص:** {article['text']}")
            st.info(f"**💡 الشرح:** {article['explanation']}")
            st.success(f"**🎯 التطبيق العملي:** {article['application']}")
    
    # أنواع الدفوع الشكلية
    st.markdown("##### 🚫 أنواع الدفوع الشكلية")
    
    formal_defenses_types = [
        {
            "النوع": "عدم الاختصاص النوعي",
            "الوصف": "الدعوى مرفوعة على محكمة غير مختصة بنوعها",
            "التوقيت": "قبل الدخول في الموضوع"
        },
        {
            "النوع": "شرط التحكيم",
            "الوصف": "وجود اتفاق بين الطرفين على اللجوء للتحكيم",
            "التوقيت": "قبل الدخول في الموضوع"
        },
        {
            "النوع": "سقوط الخصومة", 
            "الوصف": "انقضاء الخصومة لسبب من الأسباب",
            "التوقيت": "في أي مرحلة"
        },
        {
            "النوع": "خلل في الإجراءات",
            "الوصف": "وجود عيب في إجراءات رفع الدعوى أو التبليغ",
            "التوقيت": "أول جلسة"
        }
    ]
    
    for defense in formal_defenses_types:
        with st.expander(f"🚫 {defense['النوع']}", expanded=False):
            st.write(f"**الوصف:** {defense['الوصف']}")
            st.write(f"**التوقيت:** {defense['التوقيت']}")

def show_suspension_dismissal_articles():
    st.markdown("#### ⏸️ الوقف والسقوط - المواد 122-126")
    
    suspension_articles = [
        {
            "number": "122",
            "text": "تأمر المحكمة بوقف الدعوى إذا رأت تعليق الحكم في موضوعها على الفصل في مسألة أخرى يتوقف عليها الحكم، ويعتبر زوال سبب الوقف يكون لدى أي من الخصوم طلب السير في الدعوى.",
            "explanation": "أسباب وقف الدعوى وآثارها.",
            "application": "توقف الدعوى لحين الفصل في مسألة أخرى مرتبطة بها."
        },
        {
            "number": "123",
            "text": "يجوز وقف الدعوى بناء على اتفاق الخصوم على عدم السير فيها مدة لا تزيد على سنة، وإذا لم يطلب أي من الخصوم السير في الدعوى خلال سنة تسقط الدعوى.",
            "explanation": "وقف الدعوى باتفاق الأطراف وآثار السقوط.",
            "application": "يمكن وقف الدعوى سنة باتفاق الأطراف ثم تسقط إذا لم يستأنف السير."
        },
        {
            "number": "124", 
            "text": "يجوز للمحكمة أن تقرر سقوط الدعوى في الحالات التالية: إذا كانت العريضة لا تتضمن سبب الدعوى، إذا كانت الحقوق المدعى بها مقدرة بأقل من قيمتها.",
            "explanation": "أسباب سقوط الدعوى.",
            "application": "تسقط الدعوى لأسباب شكلية أو لعدم جديتها."
        },
        {
            "number": "125",
            "text": "سقوط الدعوى وفقاً لأحكام هذا القانون لا يسقط الحق ولا الدعوى ولا يجوز رفع الدعوى مرة أخرى.",
            "explanation": "آثار سقوط الدعوى.",
            "application": "السقوط يمنع إعادة رفع الدعوى لنفس السبب."
        },
        {
            "number": "126",
            "text": "لا يجوز للمدعي الاستفادة من غيبة المدعى عليه في أي دور من أدوار المحاكمة إلا بموافقته إذا كان حاضراً.",
            "explanation": "قواعد الاستفادة من غياب الخصم.",
            "application": "لا يمكن الاستفادة من غياب الخصم إلا في ظروف محددة."
        }
    ]
    
    for article in suspension_articles:
        with st.expander(f"⏸️ المادة {article['number']}", expanded=False):
            st.write(f"**النص:** {article['text']}")
            st.info(f"**💡 الشرح:** {article['explanation']}")
            st.success(f"**🎯 التطبيق العملي:** {article['application']}")

def show_judges_recusal_articles():
    st.markdown("#### ⚖️ رد القضاة - المواد 132-140")
    
    recusal_articles = [
        {
            "number": "132",
            "text": "يكون القاضي غير صالح لنظر الدعوى معيناً من سماعها في الحالات التالية: إذا كان زوجاً لأحد الخصوم، أو كان قريباً أو مصاهراً إلى الدرجة الرابعة، إذا كان له أو لزوجته خصومة قائمة مع أحد الخصوم.",
            "explanation": "أسباب رد القضاة المتعلقة بالقرابة والخصومة.",
            "application": "يمتنع على القاضي نظر الدعوى إذا كان له صلة بأحد الأطراف."
        },
        {
            "number": "133",
            "text": "يقع باطلاً عمل القاضي أو القضاة في الحالات المنصوص عليها في المادة السابقة ولو تم باتفاق الخصوم.",
            "explanation": "بطلان عمل القاضي في حالات الرد.",
            "application": "أعمال القاضي المردود تعتبر باطلة حتى لو وافق الأطراف."
        },
        {
            "number": "134",
            "text": "يجوز رد القاضي للأسباب التالية: إذا كان له أو لزوجته دعوى مماثلة، إذا كان أحد الخصوم يعمل لديه.",
            "explanation": "أسباب أخرى لرد القضاة.",
            "application": "يتسع نطاق أسباب الرد ليشعار العلاقات الوظيفية."
        },
        {
            "number": "135",
            "text": "إذا كان القاضي غير صالح لنظر الدعوى أو قام به سبب لرده أن يخبر رئيس المحكمة لإبداله في المهمة.",
            "explanation": "إجراءات إبدال القاضي المردود.",
            "application": "على القاضي إخطار رئيس المحكمة بأسباب الرد."
        },
        {
            "number": "136",
            "text": "يطلب رد القاضي بالمرافعة بعريضة إلى رئيس محكمة البداية إذا كان المطلوب رده قاضي صلح أو أحد قضاة محكمة البداية.",
            "explanation": "إجراءات طلب رد القاضي.",
            "application": "يقدم طلب الرد بعريضة لرئيس المحكمة المختص."
        },
        {
            "number": "137",
            "text": "يجب أن يشتمل استدعاء طلب الرد على أسبابه ومستندات إثباته وأن يودع به وسائل الإثبات من أصول مؤيدة له.",
            "explanation": "متطلبات طلب الرد.",
            "application": "يجب أن يكون طلب الرد مسبباً ومدعماً بالأدلة."
        },
        {
            "number": "138",
            "text": "ينظم الرئيس المطلوب رده مدة للرد على استدعاء طلب الرد وبعد ورود الجواب فيه تقرر المحكمة بدون حضور الخصوم والقاضي المطلوب رده ما تراه بهذا الشأن.",
            "explanation": "إجراءات الفصل في طلب الرد.",
            "application": "تفصل المحكمة في طلب الرد دون حضور الأطراف."
        },
        {
            "number": "139",
            "text": "إذا ظهر للمحكمة المرفوع إليها طلب الرد أن الأسباب التي بينها طالبها تحقق قانوناً للرد تقرر إبدال القاضي عن النظر في الدعوى.",
            "explanation": "قبول طلب الرد.",
            "application": "إذا توافرت أسباب الرد تقرر المحكمة إبدال القاضي."
        },
        {
            "number": "140",
            "text": "إذا قررت المحكمة رفض طلب الرد، يجوز للطالب أن يستأنف هذا القرار مع الحكم الذي يصدر في نهاية الدعوى.",
            "explanation": "الطعن في قرار رفض طلب الرد.",
            "application": "يمكن الطعن في قرار رفض الرد مع الحكم النهائي."
        }
    ]
    
    # عرض المواد في مجموعات
    st.markdown("##### ⚖️ المواد 132-134: أسباب الرد")
    for article in recusal_articles[:3]:
        with st.expander(f"⚖️ المادة {article['number']}", expanded=False):
            st.write(f"**النص:** {article['text']}")
            st.info(f"**💡 الشرح:** {article['explanation']}")
            st.success(f"**🎯 التطبيق العملي:** {article['application']}")
    
    st.markdown("##### 📝 المواد 135-140: إجراءات الرد")
    for article in recusal_articles[3:]:
        with st.expander(f"⚖️ المادة {article['number']}", expanded=False):
            st.write(f"**النص:** {article['text']}")
            st.info(f"**💡 الشرح:** {article['explanation']}")
            st.success(f"**🎯 التطبيق العملي:** {article['application']}")

def show_financial_defenses_articles():
    st.markdown("#### 💰 الدفوع المالية - المواد 127-131")
    
    financial_articles = [
        {
            "number": "127",
            "text": "إذا كانت دعوى استيفاء دين أو تعويضات يجوز للمدعى عليه بعد إشعار المدعي أن يدفع إلى المحكمة في أي وقت مبلغاً من المال تسديداً للدين أو تسديداً بسبب واحد أو أكثر من أسباب الدعوى.",
            "explanation": "إيداع المال في المحكمة كدفع مالي.",
            "application": "يمكن للمدعى عليه إيداع المال المستحق في المحكمة."
        },
        {
            "number": "128",
            "text": "يجب أن يبين في الإشعار سبب أو أسباب الدعوى التي تم الدفع عنها والمبلغ المستحق لأداة قبرات المحكمة.",
            "explanation": "متطلبات إشعار الدفع المالي.",
            "application": "يجب أن يكون الإشعار مفصلاً بالأسباب والمبالغ."
        },
        {
            "number": "129",
            "text": "يجب للمدعي خلال سبعة أيام من تاريخ تسليم الإشعار بإيداع المبلغ عن طريق المحكمة أن يقوم بتسلم المبلغ كاملاً أو قسماً منه.",
            "explanation": "موعد تسلم المبلغ المودع.",
            "application": "للمدعي 7 أيام لتسلم المبلغ المودع."
        },
        {
            "number": "130",
            "text": "إذا لم يتسلم المبلغ المودع في المحكمة بكامله فلا يجوز دفعه إلا تسديداً للدين أو لسبب من أسباب الدعوى المعنية.",
            "explanation": "تخصيص المبالغ المودعة.",
            "application": "تخصص المبالغ للدين أو السبب المحدد."
        },
        {
            "number": "131",
            "text": "إذا كانت الدعوى متعلقة بشخص ناقص الأهلية يمكن تسويتها أو مصالحة أو قبول مبلغ يودع في المحكمة بموافقة المحكمة.",
            "explanation": "معاملات ناقصي الأهلية.",
            "application": "تخضع تصرفات ناقصي الأهلية لموافقة المحكمة."
        }
    ]
    
    for article in financial_articles:
        with st.expander(f"💰 المادة {article['number']}", expanded=False):
            st.write(f"**النص:** {article['text']}")
            st.info(f"**💡 الشرح:** {article['explanation']}")
            st.success(f"**🎯 التطبيق العملي:** {article['application']}")

def show_defenses_tools():
    st.markdown("#### 🎯 أدوات الدفوع والطلبات")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("##### 🚫 منشئ الدفوع الشكلية")
        with st.form("formal_defenses_builder"):
            defense_type = st.selectbox("نوع الدفع الشكلي", [
                "عدم الاختصاص النوعي",
                "وجود شرط تحكيم",
                "سقوط الخصومة",
                "خلل في إجراءات رفع الدعوى"
            ])
            defense_basis = st.text_area("الأساس القانوني للدفع")
            supporting_evidence = st.text_area("الأدلة المؤيدة")
            
            if st.form_submit_button("🚫 إنشاء الدفع الشكلي", use_container_width=True):
                defense_draft = generate_formal_defense(
                    defense_type, defense_basis, supporting_evidence
                )
                st.text_area("🚫 مسودة الدفع الشكلي", value=defense_draft, height=300)
    
    with col2:
        st.markdown("##### ⏸️ محلل الوقف والسقوط")
        with st.form("suspension_analyzer"):
            case_duration = st.number_input("مدة الدعوى (أشهر)", min_value=1, value=6)
            last_action = st.date_input("تاريخ آخر إجراء")
            parties_agreement = st.checkbox("هل هناك اتفاق على الوقف؟")
            suspension_reason = st.text_area("سبب الوقف المقترح")
            
            if st.form_submit_button("⏸️ تحليل إمكانية الوقف", use_container_width=True):
                analysis = analyze_suspension_possibility(
                    case_duration, last_action, parties_agreement, suspension_reason
                )
                display_suspension_analysis(analysis)
    
    # حاسبة مواعيد الدفوع
    st.markdown("##### ⏰ حاسبة مواعيد الدفوع")
    
    with st.form("defenses_deadline_calculator"):
        col1, col2 = st.columns(2)
        
        with col1:
            session_date = st.date_input("تاريخ الجلسة الأولى")
            defense_category = st.selectbox("نوع الدفع", [
                "دفوع شكلية - قبل الموضوع",
                "دفوع موضوعية - مع الموضوع", 
                "دفوع سقوط - في أي وقت",
                "طلب وقف - عند توفر السبب"
            ])
            
        with col2:
            case_stage = st.selectbox("مرحلة الدعوى", [
                "قبل تبادل اللوائح",
                "بعد تبادل اللوائح",
                "أثناء سماع البينات",
                "قبل المرافعة النهائية"
            ])
            has_attorney = st.checkbox("هل الخصم ممثل بمحام؟")
        
        if st.form_submit_button("⏰ حساب المواعيد", use_container_width=True):
            deadlines = calculate_defenses_deadlines(
                session_date, defense_category, case_stage, has_attorney
            )
            display_defenses_deadlines(deadlines)

def generate_formal_defense(defense_type, basis, evidence):
    """إنشاء مسودة دفع شكلي"""
    
    defense = f"""
    دفع شكلي
    نوع الدفع: {defense_type}
    
    الأساس القانوني:
    {basis}
    
    الأدلة المؤيدة:
    {evidence}
    
    الطلبات:
    1. الحكم بعدم اختصاص المحكمة بنظر الدعوى
    2. رد الدعوى شكلاً
    3. تحميل المدعي المصاريف
    
    المرفقات:
    - المستندات المؤيدة للدفع
    - النصوص القانونية المعتمدة
    
    توقيع المدعى عليه/الوكيل:
    ___________________
    التاريخ: __________
    """
    
    return defense

def analyze_suspension_possibility(duration, last_action, agreement, reason):
    """تحليل إمكانية وقف الدعوى"""
    
    analysis = {
        'possibility': '',
        'required_conditions': [],
        'expected_duration': '',
        'recommendations': []
    }
    
    # تحليل الإمكانية
    if agreement and reason:
        analysis['possibility'] = "عالية"
        analysis['expected_duration'] = "سنة قابلة للتجديد"
    elif reason and duration > 12:
        analysis['possibility'] = "متوسطة"
        analysis['expected_duration'] = "6 أشهر"
    else:
        analysis['possibility'] = "منخفضة"
        analysis['expected_duration'] = "غير محدد"
    
    # الشروط المطلوبة
    if not agreement:
        analysis['required_conditions'].append("اتفاق الطرفين على الوقف")
    if not reason:
        analysis['required_conditions'].append("سبب مقنع للوقف")
    
    # التوصيات
    if agreement:
        analysis['recommendations'].append("تقديم طلب وقف باتفاق الطرفين")
    else:
        analysis['recommendations'].append("محاولة الوصول لاتفاق مع الطرف الآخر")
    
    analysis['recommendations'].append("إعداد مذكرة مسببة لطلب الوقف")
    
    return analysis

def display_suspension_analysis(analysis):
    """عرض نتيجة تحليل الوقف"""
    
    st.success(f"## ⏸️ نتيجة التحليل: إمكانية {analysis['possibility']}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"**⏰ المدة المتوقعة:** {analysis['expected_duration']}")
        
    with col2:
        if analysis['required_conditions']:
            st.warning("**📋 الشروط المطلوبة:**")
            for condition in analysis['required_conditions']:
                st.write(f"• {condition}")
    
    if analysis['recommendations']:
        st.markdown("##### 💡 التوصيات:")
        for recommendation in analysis['recommendations']:
            st.write(f"• {recommendation}")

def calculate_defenses_deadlines(session_date, defense_type, case_stage, has_attorney):
    """حساب مواعيد تقديم الدفوع"""
    
    base_days = 0
    
    # تحديد الموعد حسب نوع الدفع
    if defense_type == "دفوع شكلية - قبل الموضوع":
        base_days = 0  # تقدم في أول جلسة
    elif defense_type == "دفوع موضوعية - مع الموضوع":
        base_days = 30
    elif defense_type == "دفوع سقوط - في أي وقت":
        base_days = -1  # لا يوجد موعد محدد
    elif defense_type == "طلب وقف - عند توفر السبب":
        base_days = 15
    
    # تعديل حسب مرحلة الدعوى
    if case_stage == "قبل تبادل اللوائح":
        base_days = max(0, base_days)
    elif case_stage == "بعد تبادل اللوائح":
        base_days += 15
    
    # تعديل حسب وجود محام
    if not has_attorney:
        base_days += 15
    
    if base_days >= 0:
        deadline_date = session_date + timedelta(days=base_days)
        remaining_days = (deadline_date - datetime.now().date()).days
    else:
        deadline_date = None
        remaining_days = -1
    
    return {
        'session_date': session_date,
        'defense_type': defense_type,
        'deadline_days': base_days,
        'deadline_date': deadline_date,
        'remaining_days': remaining_days,
        'case_stage': case_stage
    }

def display_defenses_deadlines(deadlines):
    """عرض مواعيد الدفوع"""
    
    st.success(f"## ⏰ المواعيد القانونية لتقديم الدفوع")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"**تاريخ الجلسة:** {deadlines['session_date'].strftime('%Y-%m-%d')}")
        st.info(f"**نوع الدفع:** {deadlines['defense_type']}")
        
    with col2:
        st.info(f"**مرحلة الدعوى:** {deadlines['case_stage']}")
        
        if deadlines['deadline_days'] >= 0:
            st.info(f"**المدة القانونية:** {deadlines['deadline_days']} يوم")
            st.info(f"**آخر موعد:** {deadlines['deadline_date'].strftime('%Y-%m-%d')}")
            st.info(f"**الأيام المتبقية:** {deadlines['remaining_days']} يوم")
        else:
            st.info("**الموعد:** يمكن تقديمه في أي وقت")
    
    # تحذيرات
    if deadlines['remaining_days'] == 0:
        st.error("⚠️ اليوم هو آخر موعد لتقديم الدفع!")
    elif deadlines['remaining_days'] > 0 and deadlines['remaining_days'] <= 7:
        st.warning("🚨 الموعد النهائي يقترب! يوصى بتقديم الدفع فوراً.")
        

# ==========================
# 🛡️ قسم الإجراءات الوقائية (141-157)
# ==========================
def show_preventive_procedures_section():
    """قسم الإجراءات الوقائية"""
    show_breadcrumbs("🛡️ الإجراءات الوقائية (المواد 141-157)")
    
    st.markdown("""
    <div class="main-header">
        <h1>🛡️ الإجراءات الوقائية</h1>
        <p>الحجز التحفظي، المنع من السفر، وتعيين القيم وفق المواد 141-157 من قانون أصول المحاكمات المدنية</p>
    </div>
    """, unsafe_allow_html=True)

    tabs = st.tabs(["💰 الحجز التحفظي (141-152)", "🚫 المنع من السفر (157)", "👨‍💼 تعيين القيم (153-156)", "🛡️ أدوات وقائية"])

    with tabs[0]:
        show_attachment_articles()
    with tabs[1]:
        show_travel_ban_articles()
    with tabs[2]:
        show_trustee_articles()
    with tabs[3]:
        show_preventive_tools()

def show_attachment_articles():
    st.markdown("#### 💰 الحجز التحفظي - المواد 141-152")
    
    attachment_articles = [
        {
            "number": "141",
            "text": "لرفع طلب توقيع الحجز التحفظي سواء قبل إقامة الدعوى أو عند تقديمها أو خلالها، يرفع إلى قاضي الأمور المستعجلة أو المحكمة بناء على ما يقدم من مستندات وبينات أو بناء على حكم أو قرار تحكيم، وذلك على أموال المدين المنقولة وغير المنقولة.",
            "explanation": "الإطار العام لطلبات الحجز التحفظي وتوقيت تقديمها.",
            "application": "يمكن طلب الحجز قبل رفع الدعوى أو أثناء سريانها."
        },
        {
            "number": "142",
            "text": "تستثنى الأموال التالية من الحجز: المسكن والفرش الضروري، أدوات العمل، المركبات الناقلة إذا كان المدين ناقلاً، المحاصيل الزراعية قبل نضجها.",
            "explanation": "الأموال غير القابلة للحجز التحفظي.",
            "application": "يحمي القانون بعض الأموال الضرورية للمدين من الحجز."
        },
        {
            "number": "143",
            "text": "يحضر محضر الحجز الذي تنتدبه المحكمة شاهدين ويباشر إجراءات الحجز بحضورهم، ويمكنه أن يتضمن في المحضر الأموال التي وقع عليها الحجز ونوعها وقيمتها.",
            "explanation": "إجراءات تنفيذ الحجز التحفظي.",
            "application": "يتم الحجز بحضور شاهدين وتحرير محضر مفصل."
        },
        {
            "number": "144",
            "text": "يجوز للمحكمة أو قاضي الأمور المستعجلة أن تأمر بوضع الأموال المحجوزة تحت يد شخص أمين للحفاظ عليها.",
            "explanation": "تعيين أمين على الأموال المحجوزة.",
            "application": "يمكن تعيين أمين للحفاظ على الأموال لحين الفصل في الدعوى."
        },
        {
            "number": "145",
            "text": "إذا كان المال في يد شخص ثالث، يقوم هذا الشخص بإخطار الحجز وبيان الأموال الموجودة لديه للمدين.",
            "explanation": "الحجز على الأموال الموجودة لدى الغير.",
            "application": "يلتزم الحائز بالإفصاح عن الأموال الموجودة لديه."
        },
        {
            "number": "146",
            "text": "إذا ادعى الشخص الثالث أنه ليس لديه أموال للمدين، أو إذا لم يقدم البيان المنصوص عليه، جاز للمدين رفع دعوى عليه.",
            "explanation": "جزاء عدم تقديم البيان من الشخص الثالث.",
            "application": "يمكن رفع دعوى على من يمتنع عن الإفصاح عن الأموال."
        },
        {
            "number": "147",
            "text": "إذا سلم الشخص الثالث إلى المدين أو إلى أي شخص آخر شيئاً من الأموال التي تم إخطار الحجز عليها يضمن ما سلمه.",
            "explanation": "ضمانات التسليم بعد إخطار الحجز.",
            "application": "يضمن الحائز التسليمات بعد علمه بالحجز."
        },
        {
            "number": "148",
            "text": "ينظم الطالب صورة مصدقة عن البيان الذي يقدمه الشخص الثالث سواء كان هذا البيان يعترف بوجود أموال لديه للمدين أو لا.",
            "explanation": "توثيق إفصاح الشخص الثالث.",
            "application": "يحتفظ طالب الحجز بصورة من إفصاح الحائز."
        },
        {
            "number": "149",
            "text": "إذا نفي الشخص الثالث وجود أموال لديه ورفض الحجز، يجب عليه أن يقدم إلى المحكمة ما يثبت صحة هذا الإنكار.",
            "explanation": "إثباتات إنكار وجود الأموال.",
            "application": "على المنكر تقديم ما يثبت عدم وجود أموال."
        },
        {
            "number": "150",
            "text": "إذا ثبت الدين وعينت المحكمة الحكم بالدعوى الأصلية تثبيت الحجز.",
            "explanation": "تثبيت الحجز بعد الحكم في الدعوى.",
            "application": "يثبت الحجز إذا حكم للمدعي في الدعوى الأصلية."
        },
        {
            "number": "151",
            "text": "يتم الحجز على الأموال غير المنقولة بوضع إشارة الحجز على سجلاتها في دوائر التسجيل، وعلى ذلك يجب تبليغ دائرة تسجيل الأراضي.",
            "explanation": "إجراءات الحجز على العقارات.",
            "application": "يتم الحجز على العقار في سجلات التسجيل."
        },
        {
            "number": "152",
            "text": "إذا صدر قرار بإيقاع الحجز التحفظي قبل إقامة الدعوى، يجب على الطالب أن يقيم دعوى إثبات حقه خلال خمسة عشر يوماً من تاريخ صدور القرار.",
            "explanation": "موعد رفع الدعوى بعد الحجز التحفظي.",
            "application": "يجب رفع الدعوى خلال 15 يوماً من الحجز التحفظي."
        }
    ]
    
    # عرض المواد في مجموعات
    st.markdown("##### 💰 المواد 141-144: إجراءات الحجز")
    for article in attachment_articles[:4]:
        with st.expander(f"💰 المادة {article['number']}", expanded=False):
            st.write(f"**النص:** {article['text']}")
            st.info(f"**💡 الشرح:** {article['explanation']}")
            st.success(f"**🎯 التطبيق العملي:** {article['application']}")
    
    st.markdown("##### 📋 المواد 145-152: إجراءات متقدمة")
    for article in attachment_articles[4:]:
        with st.expander(f"💰 المادة {article['number']}", expanded=False):
            st.write(f"**النص:** {article['text']}")
            st.info(f"**💡 الشرح:** {article['explanation']}")
            st.success(f"**🎯 التطبيق العملي:** {article['application']}")

def show_travel_ban_articles():
    st.markdown("#### 🚫 المنع من السفر - المادة 157")
    
    travel_ban_articles = [
        {
            "number": "157",
            "text": "إذا اقتنعت المحكمة أو قاضي الأمور المستعجلة بناء على ما قدم من بينات بأن المدعى عليه قد يعمل على تهريب أمواله أو هربها إلى خارج البلد، أو أنه على وشك أن يفعل ذلك وذلك خوفاً من تعطيل حق الخصم، جاز للمحكمة أن تأمر بمنعه من السفر بعد أن تبين له السبب الذي يحول دون تقديمه كفالة.",
            "explanation": "أسباب وإجراءات المنع من السفر.",
            "application": "يتم المنع من السفر عند خشية تهريب الأموال أو الهرب."
        }
    ]
    
    for article in travel_ban_articles:
        with st.expander(f"🚫 المادة {article['number']}", expanded=False):
            st.write(f"**النص:** {article['text']}")
            st.info(f"**💡 الشرح:** {article['explanation']}")
            st.success(f"**🎯 التطبيق العملي:** {article['application']}")
    
    # شروط المنع من السفر
    st.markdown("##### 🚫 شروط المنع من السفر")
    
    travel_ban_conditions = [
        "وجود أدلة على نية تهريب الأموال",
        "خوف من هرب المدعى عليه خارج البلاد",
        "تعطيل حقوق الدائن",
        "عدم تقديم كفالة مناسبة",
        "تقديم طلب من الدائن"
    ]
    
    for condition in travel_ban_conditions:
        st.write(f"• {condition}")

def show_trustee_articles():
    st.markdown("#### 👨‍💼 تعيين القيم - المواد 153-156")
    
    trustee_articles = [
        {
            "number": "153",
            "text": "في كل قضية يرفع طلب تعيين قيم على مال أو تقرر فيها الحجز على مال وطلب تعيين قيم عليه، يجوز للمحكمة أن تقرر: تعيين قيم على ذلك المال، تسليم المال إلى القيم، تكليف القيم بممارسة جميع أو بعض الصلاحيات.",
            "explanation": "أساسيات تعيين القيم على الأموال.",
            "application": "يمكن تعيين قيم لإدارة الأموال المحجوزة أو المتنازع عليها."
        },
        {
            "number": "154",
            "text": "تحدد المحكمة أو قاضي الأمور المستعجلة المبلغ الواجب دفعه للقيم مكافأة على خدماته وكيفية دفعه والشخص المكلف بدفعه.",
            "explanation": "مكافأة القيم وتحديدها.",
            "application": "تحدد المحكمة مكافأة القيم بناء على طبيعة العمل."
        },
        {
            "number": "155",
            "text": "يتعين على القيم أن يقدم الكفالة التي تراها المحكمة مناسبة لضمان: تقديم الحساب، دفع المبالغ المستحقة، المسؤولية عن الضرر الذي يلحق بالأموال.",
            "explanation": "كفالة القيم وضماناتها.",
            "application": "يقدم القيم كفالة تضمن أداءه لمهامه."
        },
        {
            "number": "156",
            "text": "يجوز للمحكمة أن تأمر بحجز على أموال القيم وعقاره على أن يسمح من قيمته ما تراه استحقاقه عليه.",
            "explanation": "مسؤولية القيم وحجز أمواله.",
            "application": "يمكن حجز أموال القيم في حالة التقصير."
        }
    ]
    
    for article in trustee_articles:
        with st.expander(f"👨‍💼 المادة {article['number']}", expanded=False):
            st.write(f"**النص:** {article['text']}")
            st.info(f"**💡 الشرح:** {article['explanation']}")
            st.success(f"**🎯 التطبيق العملي:** {article['application']}")

def show_preventive_tools():
    st.markdown("#### 🛡️ أدوات الإجراءات الوقائية")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("##### 💰 محلل الحجز التحفظي")
        with st.form("attachment_analyzer"):
            debt_amount = st.number_input("مبلغ الدين (دينار)", min_value=0, value=50000)
            defendant_assets = st.selectbox("أموال المدين", [
                "عقارات",
                "مركبات",
                "أموال نقدية",
                "استثمارات",
                "أموال مختلطة"
            ])
            risk_level = st.select_slider("مستوى خطر تهريب الأموال", options=["منخفض", "متوسط", "مرتفع", "عالٍ جداً"])
            
            if st.form_submit_button("💰 تحليل إمكانية الحجز", use_container_width=True):
                analysis = analyze_attachment_possibility(
                    debt_amount, defendant_assets, risk_level
                )
                display_attachment_analysis(analysis)
    
    with col2:
        st.markdown("##### 🚫 منشئ طلب المنع من السفر")
        with st.form("travel_ban_builder"):
            ban_reason = st.selectbox("سبب المنع", [
                "خشية تهريب الأموال",
                "خوف من الهرب",
                "تعطيل حقوق الدائن",
                "عدم وجود كفالة"
            ])
            evidence_details = st.text_area("تفاصيل الأدلة على الخطر")
            proposed_guarantee = st.number_input("الكفالة المقترحة (دينار)", min_value=0, value=0)
            
            if st.form_submit_button("🚫 إنشاء طلب المنع", use_container_width=True):
                request_draft = generate_travel_ban_request(
                    ban_reason, evidence_details, proposed_guarantee
                )
                st.text_area("🚫 مسودة طلب المنع", value=request_draft, height=300)
    
    # حاسبة الكفالات
    st.markdown("##### 💳 حاسبة الكفالات والضمانات")
    
    with st.form("guarantee_calculator"):
        col1, col2 = st.columns(2)
        
        with col1:
            case_type = st.selectbox("نوع القضية", [
                "دعوى تعاقدية",
                "دعوى تعويض",
                "دعوى تجارية", 
                "دعوى عائلية"
            ])
            claim_amount = st.number_input("مبلغ المطالبة (دينار)", min_value=0, value=100000)
            
        with col2:
            defendant_status = st.selectbox("وضع المدعى عليه", [
                "فرد",
                "تاجر",
                "شركة",
                "مؤسسة"
            ])
            risk_factors = st.multiselect("عوامل الخطر", [
                "سفر سابق متكرر",
                "أموال خارجية",
                "تهريب سابق",
                "عدم تعاون"
            ])
        
        if st.form_submit_button("💳 حساب الكفالة", use_container_width=True):
            guarantee_analysis = calculate_guarantee_amount(
                case_type, claim_amount, defendant_status, risk_factors
            )
            display_guarantee_analysis(guarantee_analysis)

def analyze_attachment_possibility(debt_amount, assets_type, risk_level):
    """تحليل إمكانية الحجز التحفظي"""
    
    analysis = {
        'possibility': '',
        'recommended_assets': [],
        'estimated_duration': '',
        'success_probability': '',
        'requirements': []
    }
    
    # تحليل الإمكانية
    if debt_amount <= 50000 and risk_level in ["مرتفع", "عالٍ جداً"]:
        analysis['possibility'] = "عالية جداً"
        analysis['success_probability'] = "80-95%"
    elif debt_amount <= 100000 and risk_level in ["متوسط", "مرتفع"]:
        analysis['possibility'] = "عالية"
        analysis['success_probability'] = "70-85%"
    else:
        analysis['possibility'] = "متوسطة"
        analysis['success_probability'] = "50-70%"
    
    # الأصول الموصى بها للحجز
    if assets_type == "عقارات":
        analysis['recommended_assets'] = ["العقارات المسجلة", "الشقق", "الأراضي"]
    elif assets_type == "مركبات":
        analysis['recommended_assets'] = ["السيارات", "الشاحنات", "المعدات"]
    elif assets_type == "أموال نقدية":
        analysis['recommended_assets'] = ["الحسابات المصرفية", "الاستثمارات"]
    
    # المتطلبات
    analysis['requirements'] = [
        "إثبات وجود الدين",
        "إثبات خطر تهريب الأموال",
        "تقديم كفالة مناسبة",
        "رفع دعوى خلال 15 يوماً"
    ]
    
    analysis['estimated_duration'] = "2-6 أشهر"
    
    return analysis

def display_attachment_analysis(analysis):
    """عرض نتيجة تحليل الحجز"""
    
    st.success(f"## 💰 نتيجة التحليل: إمكانية {analysis['possibility']}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"**📊 احتمالية النجاح:** {analysis['success_probability']}")
        st.info(f"**⏰ المدة المتوقعة:** {analysis['estimated_duration']}")
        
    with col2:
        if analysis['recommended_assets']:
            st.warning("**📋 الأصول الموصى بالحجز عليها:**")
            for asset in analysis['recommended_assets']:
                st.write(f"• {asset}")
    
    if analysis['requirements']:
        st.markdown("##### 📋 المتطلبات:")
        for requirement in analysis['requirements']:
            st.write(f"• {requirement}")

def generate_travel_ban_request(reason, evidence, guarantee):
    """إنشاء مسودة طلب منع من السفر"""
    
    request = f"""
    طلب منع من السفر
    السبب: {reason}
    
    الأدلة على الخطر:
    {evidence}
    
    الكفالة المقترحة: {guarantee:,} دينار
    
    الطلبات:
    1. منع المدعى عليه من السفر خارج المملكة
    2. إلزامه بتقديم كفالة مناسبة
    3. إخطار جهات الحدود والجوازات
    
    الأسباب:
    - خشية تهريب الأموال أو الهرب
    - تعطيل حقوق الدائن
    - عدم كفاية الضمانات الحالية
    
    المرفقات:
    - أدلة على نية التهريب أو الهرب
    - مستندات الدعوى الأصلية
    - تقرير عن وضع المدعى عليه المالي
    
    توقيع الطالب:
    ___________________
    التاريخ: __________
    """
    
    return request

def calculate_guarantee_amount(case_type, claim_amount, defendant_status, risk_factors):
    """حساب مبلغ الكفالة المناسب"""
    
    base_guarantee = claim_amount * 0.3  # 30% من المطالبة كحد أدنى
    
    # تعديل حسب نوع القضية
    type_multipliers = {
        "دعوى تعاقدية": 1.0,
        "دعوى تعويض": 1.2,
        "دعوى تجارية": 1.5,
        "دعوى عائلية": 0.8
    }
    
    multiplier = type_multipliers.get(case_type, 1.0)
    base_guarantee *= multiplier
    
    # تعديل حسب وضع المدعى عليه
    status_multipliers = {
        "فرد": 1.0,
        "تاجر": 1.3,
        "شركة": 1.5,
        "مؤسسة": 1.2
    }
    
    status_multiplier = status_multipliers.get(defendant_status, 1.0)
    base_guarantee *= status_multiplier
    
    # تعديل حسب عوامل الخطر
    risk_multiplier = 1.0
    for risk in risk_factors:
        if risk == "سفر سابق متكرر":
            risk_multiplier *= 1.2
        elif risk == "أموال خارجية":
            risk_multiplier *= 1.3
        elif risk == "تهريب سابق":
            risk_multiplier *= 1.5
        elif risk == "عدم تعاون":
            risk_multiplier *= 1.1
    
    final_guarantee = base_guarantee * risk_multiplier
    
    return {
        'base_guarantee': base_guarantee,
        'final_guarantee': final_guarantee,
        'risk_factors': risk_factors,
        'risk_multiplier': risk_multiplier,
        'case_type': case_type,
        'defendant_status': defendant_status
    }

def display_guarantee_analysis(analysis):
    """عرض نتيجة حساب الكفالة"""
    
    st.success(f"## 💳 الكفالة الموصى بها: {analysis['final_guarantee']:,.0f} دينار")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"**💰 الكفالة الأساسية:** {analysis['base_guarantee']:,.0f} دينار")
        st.info(f"**📊 مضاعف المخاطر:** {analysis['risk_multiplier']:.1f}x")
        
    with col2:
        st.info(f"**⚖️ نوع القضية:** {analysis['case_type']}")
        st.info(f"**👤 وضع المدعى عليه:** {analysis['defendant_status']}")
    
    if analysis['risk_factors']:
        st.markdown("##### 🚫 عوامل الخطر المؤثرة:")
        for risk in analysis['risk_factors']:
            st.write(f"• {risk}")
# ==========================
# 🧾 قسم الأحكام والطعون (158-225)
# ==========================
def show_judgments_appeals_section():
    """قسم الأحكام والطعون"""
    show_breadcrumbs("🧾 الأحكام والطعون (المواد 158-225)")
    
    st.markdown("""
    <div class="main-header">
        <h1>🧾 الأحكام القضائية وطرق الطعن</h1>
        <p>تحليل شامل لإصدار الأحكام وطرق الطعن فيها وفق المواد 158-225 من قانون أصول المحاكمات المدنية</p>
    </div>
    """, unsafe_allow_html=True)

    tabs = st.tabs(["⚖️ إصدار الأحكام (158-169)", "📈 الاستئناف (170-190)", "🔍 التمييز (191-204)", "🔄 الطعون الأخرى (205-225)", "🎯 أدوات الطعون"])

    with tabs[0]:
        show_judgments_issuance_articles()
    with tabs[1]:
        show_appeal_articles()
    with tabs[2]:
        show_cassation_articles()
    with tabs[3]:
        show_other_appeals_articles()
    with tabs[4]:
        show_appeals_tools()

def show_judgments_issuance_articles():
    st.markdown("#### ⚖️ إصدار الأحكام - المواد 158-169")
    
    judgments_articles = [
        {
            "number": "158",
            "text": "في غير الأحكام التي تحتمل السرية، تعني المحكمة كتابة الحكم بعد الانتهاء من سماع البينات والمرافعات، وتدلقي بالحكم علانية في نفس الجلسة أو في جلسة أخرى تعينها خلال ثلاثين يوماً.",
            "explanation": "الإجراءات الأساسية لكتابة وإصدار الأحكام.",
            "application": "يجب إصدار الحكم خلال 30 يوماً من انتهاء المرافعات."
        },
        {
            "number": "159",
            "text": "تكون المداولة في الحكم سرية بين القضاة المحكمين ولا يجوز أن يشارك فيها غير القضاة الذين سمعوا المرافعة.",
            "explanation": "سرية المداولة بين القضاة.",
            "application": "تتم المداولة سراً بين القضاة الذين شاركوا في المحاكمة."
        },
        {
            "number": "160",
            "text": "يجب أن يبين في الحكم المحكمة التي أصدرته وتاريخ صدوره وأسماء القضاة الذين اشتركوا في إصداره وأسماء الخصوم ووكيلهم، وعرض موجز لوقائع الدعوى وطلبات الخصوم وأسباب الحكم ومنطوقه.",
            "explanation": "المكونات الأساسية للحكم القضائي.",
            "application": "يجب أن يشتمل الحكم على جميع البيانات الإلزامية."
        },
        {
            "number": "161",
            "text": "تدعم المحكمة عند إصدارها الحكم النهائي في الدعوى برسوم ومصاريف الدعوى والإجراءات التي خصمت للخصم المحكوم له في الدعوى.",
            "explanation": "الرسوم والمصاريف في الأحكام.",
            "application": "تضمن المحكمة الرسوم والمصاريف في منطوق الحكم."
        },
        {
            "number": "162",
            "text": "يحكم بمصاريف تحقيق الخط والحكم والإعانة وبحسبة الدعوى على منتجها أو مدعي تزويره إذا ثبت في نتيجة التحقيق عدم حدة الخط أو إثبات التزوير.",
            "explanation": "مصاريف التحقيق في التزوير.",
            "application": "تحمل مصاريف التحقيق على من يثبت كذبه في ادعاء التزوير."
        },
        {
            "number": "163",
            "text": "إذا ظهر أن المدعي غير محق في قسم من دعواه يخفض المحكوم به بالإضافة إلى الرسوم والمصاريف بنسبة المبلغ المحكوم.",
            "explanation": "تخفيض المحكوم به عند عدم إحاقة المدعي كلياً.",
            "application": "يخفض المبلغ المحكوم به عند قبول جزء من الدعوى فقط."
        },
        {
            "number": "164",
            "text": "إذا تعدد المحكوم عليهم ووكيلهم متضامنين في أصل الدعوى يلزم كل منهم بالرسوم والمصاريف بنسبة ما يحكم به عليه.",
            "explanation": "توزيع الرسوم والمصاريف في حالة التضامن.",
            "application": "توزع الرسوم على الملتزمين حسب نصيب كل منهم."
        },
        {
            "number": "165",
            "text": "إذا أدخل شخص ثالث في الدعوى بناء على طلب الخصوم وحكم عليه في الدعوى بإلزام ما بالرسوم والمصاريف.",
            "explanation": "رسوم ومصاريف الشخص الثالث.",
            "application": "يلزم الشخص الثالث بالرسوم إذا حكم عليه."
        },
        {
            "number": "166",
            "text": "بالإضافة إلى الرسوم والمصاريف على اختلاف أنواعها تحكم المحكمة بإتعاب المحاماة على الخصم المحكوم عليه في الدعوى.",
            "explanation": "أتعاب المحاماة في الأحكام.",
            "application": "يمكن الحكم بأتعاب المحاماة للطرف المحكوم له."
        },
        {
            "number": "167",
            "text": "إذا كان المدين قد تعهد بدفع مبلغ من المال في وقت معين والتزم بفوائد عند التأخير، يحكم عليه بالفائدة دون أن يختل الطلب ثبوت ضرر من عدم الدفع.",
            "explanation": "الفائدة في الأحكام القضائية.",
            "application": "تحكم الفائدة على المبالغ المالية المتأخرة."
        },
        {
            "number": "168",
            "text": "تأمر المحكمة تصحيح ما يقع في الحكم من أخطاء مادية بكتابة أو أرقام أو حسابية وذلك بقرار تصدره من تلقاء نفسها أو بناء على طلب أي من الخصوم.",
            "explanation": "تصحيح الأخطاء المادية في الأحكام.",
            "application": "يمكن تصحيح الأخطاء المادية في الحكم."
        },
        {
            "number": "169",
            "text": "الطعن في الحكم للمحكوم عليه، وللمحكوم له أن يطعن في الحكم إذا اعتقد على أسباب خلاف الوقائع التي بني عليها الدعوى أو على تقدير هذه الوقائع.",
            "explanation": "حقوق الطعن في الأحكام.",
            "application": "لكل من الخصوم الحق في الطعن بالحكم."
        }
    ]
    
    # عرض المواد في مجموعات
    st.markdown("##### ⚖️ المواد 158-162: إجراءات الإصدار")
    for article in judgments_articles[:5]:
        with st.expander(f"⚖️ المادة {article['number']}", expanded=False):
            st.write(f"**النص:** {article['text']}")
            st.info(f"**💡 الشرح:** {article['explanation']}")
            st.success(f"**🎯 التطبيق العملي:** {article['application']}")
    
    st.markdown("##### 💰 المواد 163-169: الرسوم والطعون")
    for article in judgments_articles[5:]:
        with st.expander(f"⚖️ المادة {article['number']}", expanded=False):
            st.write(f"**النص:** {article['text']}")
            st.info(f"**💡 الشرح:** {article['explanation']}")
            st.success(f"**🎯 التطبيق العملي:** {article['application']}")

def show_appeal_articles():
    st.markdown("#### 📈 الاستئناف - المواد 170-190")
    
    appeal_articles = [
        {
            "number": "170",
            "text": "يجوز الطعن في الأحكام التي تحسم سير الدعوى ولا تقضي بها الخصومة أو التي تقضي بصميم الخصومة باستثناء القرارات الصادرة في المسائل المستعجلة ووقف الدعوى وإجراءات التحقيق.",
            "explanation": "نطاق الأحكام القابلة للاستئناف.",
            "application": "يستأنف معظم الأحكام التي تفصل في موضوع الدعوى."
        },
        {
            "number": "171",
            "text": "على الرغم مما يرد في أي قانون آخر تربط مواعيد الطعون في الأحكام الوجاهية والأحكام الصادرة وجاهياً اعتباراً من اليوم الثاني لتاريخ صدورها.",
            "explanation": "مواعيد الطعن في الأحكام.",
            "application": "تحسب مواعيد الطعن من اليوم التالي لصدور الحكم."
        },
        {
            "number": "172",
            "text": "ترتكز على عدم مراعاة مواعيد الطعن في الأحكام رد الطعن شكلاً، وتفصل المحكمة في ذلك من تلقاء نفسها.",
            "explanation": "رد الطعن شكلاً لانقضاء الميعاد.",
            "application": "ترد الطلبات المقدمة بعد انقضاء الميعاد."
        },
        {
            "number": "173",
            "text": "إذا كان الطالب في الطعن قد قدم استدعاء بخصوص تأجيل دفع رسوم الطعن، فالمدة التي تنقضي من يوم تقديمه الاستدعاء لا تحسب من المدة المعينة لتقديم الطعن.",
            "explanation": "احتساب مدة تأجيل رسوم الطعن.",
            "application": "لا تحتسب مدة نظر طلب تأجيل الرسوم من مدة الطعن."
        },
        {
            "number": "174",
            "text": "إذا توفي أحد أطراف الدعوى أو إذا تقرر عزل وكيله، يكمل مواعيد الطعن بناء للحكم إلى من يقوم مقامه قانوناً.",
            "explanation": "استمرار مواعيد الطعن في حالة الوفاة أو العزل.",
            "application": "تستمر المواعيد لورثة المتوفي أو الموكل الجديد."
        },
        {
            "number": "175",
            "text": "يقتصر الطعن على من رفعه ولا يحكم به على من رفع عليه، إلا إذا كان الحكم صادراً في موضوع غير قابل للتجزئة.",
            "explanation": "مدى تأثير الطعن على الأطراف.",
            "application": "الطعن شخصي ولا يشمل من لم يطعن إلا في الأحكام غير القابلة للتجزئة."
        },
        {
            "number": "176",
            "text": "تستأنف الأحكام الصادرة عن محاكم البداية إلى محكمة الاستئناف، ويجوز استئناف القرارات الصادرة في الأمور المستعجلة.",
            "explanation": "محاكم الاستئناف المختصة.",
            "application": "تستأنف أحكام البداية لمحكمة الاستئناف."
        },
        {
            "number": "177",
            "text": "إذا اتفق الطرفان على أن محكمة البداية تنظر في الدعوى دون أن يكون لهما الحق في استئناف حكم تلك المحكمة، فلا يبقى لهما الحق في استئناف الحكم.",
            "explanation": "الاتفاق على عدم الاستئناف.",
            "application": "يمكن للأطراف الاتفاق على عدم الطعن بالاستئناف."
        },
        {
            "number": "178",
            "text": "تكون مدة الطعن بالاستئناف ثلاثين يوماً في الأحكام القاضية بالخصومة، كما تكون مدة الطعن عشرة أيام في القرارات القابلة للطعن.",
            "explanation": "مدة الطعن بالاستئناف.",
            "application": "مدة استئناف الأحكام 30 يوماً والقرارات 10 أيام."
        },
        {
            "number": "179",
            "text": "تقدم عريضة الاستئناف ومستنداتها إلى قلم المحكمة التي أصدرت الحكم المستأنف، وتوضح مع أوراق الدعوى بعد إجراء التبليغات إلى المحكمة المستأنف إليها.",
            "explanation": "إجراءات تقديم عريضة الاستئناف.",
            "application": "تقدم عريضة الاستئناف لمحكمة الدرجة الأولى."
        },
        {
            "number": "180",
            "text": "يجب أن تشتمل عريضة الاستئناف على اسم المستأنف ووكيله وعنوان التبليغ، واسم المستأنف ضده ووكيله، واسم المحكمة التي أصدرت الحكم المستأنف، وأسباب الاستئناف.",
            "explanation": "متطلبات عريضة الاستئناف.",
            "application": "يجب أن تكون عريضة الاستئناف مكتملة البيانات."
        },
        {
            "number": "181",
            "text": "تدخل محكمة الاستئناف تحقيقاً في الطعون المقدمة إليها في الأحكام الصادرة عن محاكم البداية إذا كانت قيمة الدعوى لا تزيد على خمسة آلاف دينار.",
            "explanation": "نظر الاستئناف تحقيقاً أو مراجعة.",
            "application": "تنظر محكمة الاستئناف الدعوى تحقيقاً في القضايا محدودة القيمة."
        },
        {
            "number": "182",
            "text": "تدخل محكمة الاستئناف مراجعة في الطعون المقدمة إليها في الأحكام الصادرة عن محاكم البداية وذلك في الدعاوى التي تزيد قيمتها على خمسة آلاف دينار.",
            "explanation": "المراجعة في القضايا مرتفعة القيمة.",
            "application": "تنظر محكمة الاستئناف الدعوى مراجعة في القضايا مرتفعة القيمة."
        },
        {
            "number": "183",
            "text": "لدى استيفاء الشروط والإجراءات النظامية في هذا القانون تعين المحكمة يوماً لسماع الاستئناف وتخطر به الأطراف.",
            "explanation": "تعيين جلسة الاستئناف.",
            "application": "تعين محكمة الاستئناف جلسة لنظر الطعن."
        },
        {
            "number": "184",
            "text": "لا يسمح للمستأنف أن يبدي في المراجعة أسباباً لم يذكرها في العريضة ما لم تأذن له المحكمة، ولكن المحكمة لا تتقيد عند الفصل في الاستئناف بالأسباب المذكورة في عريضته.",
            "explanation": "تقييد أسباب الاستئناف.",
            "application": "يقتصر المستأنف على الأسباب المذكورة في العريضة إلا بإذن المحكمة."
        },
        {
            "number": "185",
            "text": "لا يجوز للمستأنف أن يقدم بينات إضافية كان في وسعه تقديمها في المحكمة المستأنف منها، إلا في حالات محددة.",
            "explanation": "تقييد البينات في الاستئناف.",
            "application": "يمنع تقديم بينات جديدة في الاستئناف إلا في حالات استثنائية."
        },
        {
            "number": "186",
            "text": "لا تسمح المحكمة بتقديم بينات إضافية إلا إذا رأت ذلك ضرورياً.",
            "explanation": "سلطة المحكمة في قبول البينات الإضافية.",
            "application": "للمحكمة سلطة تقديرية في قبول البينات الجديدة."
        },
        {
            "number": "187",
            "text": "لمحكمة الاستئناف عند إصدار حكمها أن تستند لسبب أو أسباب غير التي استندت إليها المحكمة البداية في قرارها.",
            "explanation": "سلطة محكمة الاستئناف في تغيير أسباب الحكم.",
            "application": "يمكن لمحكمة الاستئناف تغيير أسباب الحكم مع إبقاء النتيجة."
        },
        {
            "number": "188",
            "text": "لمحكمة الاستئناف أن تنقض الحكم المستأنف إذا ظهر لها أنه مخالف للقانون أو أن في الإجراءات والمستندات التي قامت بها المحكمة المستأنف منها ما يوجب النقض.",
            "explanation": "أسباب نقض الحكم في الاستئناف.",
            "application": "تنقض محكمة الاستئناف الحكم لوجود مخالفات قانونية."
        },
        {
            "number": "189",
            "text": "تتحكم المحكمة في الرسوم والمصاريف والإتعاب المحاماة المقررة على الدعوى من حين نظرها في محكمة الدرجة الأولى إلى حين الحكم بها استئنافاً.",
            "explanation": "الرسوم والمصاريف في الاستئناف.",
            "application": "تفصل محكمة الاستئناف في جميع الرسوم والمصاريف."
        },
        {
            "number": "190",
            "text": "تسري على المستأنف القواعد المقروة أمام محكمة الدرجة الأولى سواء فيما يتعلق بالإجراءات أو بالأحكام ما لم ينص القانون على غير ذلك.",
            "explanation": "تطبيق القواعد الإجرائية في الاستئناف.",
            "application": "تطبق في الاستئناف نفس القواعد الإجرائية لمحكمة الدرجة الأولى."
        }
    ]
    
    # عرض المواد في مجموعات
    st.markdown("##### 📈 المواد 170-178: نطاق ومواعيد الاستئناف")
    for article in appeal_articles[:9]:
        with st.expander(f"📈 المادة {article['number']}", expanded=False):
            st.write(f"**النص:** {article['text']}")
            st.info(f"**💡 الشرح:** {article['explanation']}")
            st.success(f"**🎯 التطبيق العملي:** {article['application']}")
    
    st.markdown("##### 📝 المواد 179-190: إجراءات الاستئناف")
    for article in appeal_articles[9:]:
        with st.expander(f"📈 المادة {article['number']}", expanded=False):
            st.write(f"**النص:** {article['text']}")
            st.info(f"**💡 الشرح:** {article['explanation']}")
            st.success(f"**🎯 التطبيق العملي:** {article['application']}")

def show_cassation_articles():
    st.markdown("#### 🔍 التمييز - المواد 191-204")
    
    cassation_articles = [
        {
            "number": "191",
            "text": "على الرغم مما ورد في أي قانون آخر يقبل الطعن أمام محكمة التمييز في الأحكام الصادرة في المحاكمات التي تزيد قيمتها على عشرة آلاف دينار، وذلك خلال ثلاثين يوماً من تاريخ صدورها.",
            "explanation": "نطاق ومواعيد الطعن بالتمييز.",
            "application": "يختص التمييز بالقضايا التي تزيد قيمتها على 10,000 دينار."
        },
        {
            "number": "192",
            "text": "لا تقبل الأحكام المستأنفة التي قد تقبل الطعن بالتمييز إلا التي من رئيس محكمة التمييز أو من يفوضه.",
            "explanation": "شرط قبول الطعن بالتمييز.",
            "application": "يشترط موافقة رئيس محكمة التمييز لقبول الطعن."
        },
        {
            "number": "193",
            "text": "على طالب الطعن بالتمييز أن يقدم الطلب خلال عشرة أيام من اليوم التالي لتاريخ صدور الحكم إذا كان وجاهياً أو من تاريخ تبليغه.",
            "explanation": "مدة تقديم طلب التمييز.",
            "application": "مدة طلب التمييز 10 أيام من التبليغ."
        },
        {
            "number": "194",
            "text": "على طالب الطعن بالتمييز أن يبين في طلبه بالتفصيل النقطة القانونية المستحدثة أو التي على جانب من التعقيد القانوني.",
            "explanation": "متطلبات طلب التمييز.",
            "application": "يجب أن يبين طلب التمييز النقاط القانونية المعقدة."
        },
        {
            "number": "195",
            "text": "إذا صح القرار بالطعن وجب على مقدم الطلب أن يقدم عريضة الطعن خلال عشرة أيام من تاريخ تبليغه قرار الطعن.",
            "explanation": "إكمال إجراءات التمييز.",
            "application": "يقدم عريضة التمييز خلال 10 أيام من قبول الطلب."
        },
        {
            "number": "196",
            "text": "تقدم عريضة التمييز إلى محكمة المستأنف منها لترفعها مع أوراق الدعوى إلى محكمة التمييز بعد إجراء التبليغات.",
            "explanation": "إجراءات تقديم عريضة التمييز.",
            "application": "تقدم العريضة لمحكمة الاستئناف التي ترفعها للتمييز."
        },
        {
            "number": "197",
            "text": "تنظر محكمة التمييز في محضر الدعوى واللوائح التي قدمها الأطراف ووسائل أوراق الدعوى تحقيقاً إلا إذا قررت المراجعة.",
            "explanation": "طريقة نظر التمييز.",
            "application": "تنظر محكمة التمييز في الأوراق دون المرافعة عادة."
        },
        {
            "number": "198",
            "text": "لا يقبل الطعن في الأحكام بالتمييز إلا في الحالات التالية: إذا كان الحكم مبنياً على مخالفة القانون، إذا قام بطلان في الحكم أو في الإجراءات.",
            "explanation": "أسباب الطعن بالتمييز.",
            "application": "يقتصر التمييز على المخالفات القانونية والإجراءية."
        },
        {
            "number": "199",
            "text": "إذا كان الحكم المميز قد شابته مخالفة قواعد الاختصاص تقتصر المحكمة على الفصل في مسألة الاختصاص.",
            "explanation": "معالجة مخالفات الاختصاص في التمييز.",
            "application": "تفصل محكمة التمييز في مخالفات الاختصاص فقط."
        },
        {
            "number": "200",
            "text": "إذا نقض الحكم بسبب خطأ في أصول المحاكمة يعتبر النقض شاملاً للإجراءات التي وقعت بعد السبب الذي أوجب النقض.",
            "explanation": "مدى النقض في التمييز.",
            "application": "يشمل النقض جميع الإجراءات اللاحقة للخطأ."
        },
        {
            "number": "201",
            "text": "إذا نقض الحكم المميز وأعيد إلى المحكمة التي أصدرت وجب عليها أن تخطر الأطراف في الدعوى للمرافعة في يوم تعينه.",
            "explanation": "إجراءات إعادة الدعوى بعد النقض.",
            "application": "تعاد الدعوى للمحكمة الأصلية بعد النقض."
        },
        {
            "number": "202",
            "text": "تصدر محكمة التمييز قراراتها بأغلبية آراء قضاتها ويجب أن تحتوي هذه القرارات على اسمي الطرفين وأسباب الطعن والقرار الذي أصدرته.",
            "explanation": "إصدار قرارات التمييز.",
            "application": "تصدر قرارات التمييز بأغلبية الآراء وتكون مسببة."
        },
        {
            "number": "203",
            "text": "لا يجوز الطعن في قرارات محكمة التمييز بأي طريق من طرق الطعن.",
            "explanation": "حجية قرارات التمييز.",
            "application": "قرارات التمييز نهائية ولا تقبل الطعن."
        },
        {
            "number": "204",
            "text": "على الرغم مما يرد يجوز لمحكمة التمييز إعادة النظر في قرارها النهائي في أي قضية إذا تبين لها أنها قد بنت الطعن استناداً لسبب شكلي.",
            "explanation": "إعادة النظر في قرارات التمييز.",
            "application": "يمكن إعادة النظر في قرار التمييز لسبب استثنائي."
        }
    ]
    
    for article in cassation_articles:
        with st.expander(f"🔍 المادة {article['number']}", expanded=False):
            st.write(f"**النص:** {article['text']}")
            st.info(f"**💡 الشرح:** {article['explanation']}")
            st.success(f"**🎯 التطبيق العملي:** {article['application']}")

def show_other_appeals_articles():
    st.markdown("#### 🔄 الطعون الأخرى - المواد 205-225")
    
    other_appeals_articles = [
        {
            "number": "205",
            "text": "إذا رأت إحدى هيئات محكمة التمييز أن تخالف مبدأ مقرر في حكم سابق تحيل الدعوى إلى الهيئة العامة.",
            "explanation": "إحالة الدعوى للهيئة العامة.",
            "application": "تحال الدعوى للهيئة العامة عند التعارض مع مبادئ سابقة."
        },
        {
            "number": "206",
            "text": "لا يعتبر شخص لم يكن خصماً ولا ممثلاً ولا مدخلاً في دعوى حكم فيها بحكم يعتبر حجة عليه أن يعترض على هذا الحكم اعتراض الغير.",
            "explanation": "اعتراض الغير على الأحكام.",
            "application": "يجوز للغير الاعتراض على حكم لم يكن طرفاً فيه."
        },
        {
            "number": "207",
            "text": "اعتراض الغير على نوعين أصلي وطارئ، يقوم الاعتراض الأصلي إلى المحكمة التي أصدرت الحكم المطعون فيه بعريضة دعوى.",
            "explanation": "أنواع اعتراض الغير.",
            "application": "ينقسم اعتراض الغير إلى أصلي وطارئ."
        },
        {
            "number": "208",
            "text": "يبقى الحق في الاعتراض على الحكم ما لم يسقط بالتقادم.",
            "explanation": "تقادم اعتراض الغير.",
            "application": "يسقط اعتراض الغير بالتقادم."
        },
        {
            "number": "209",
            "text": "للمحكمة أن كان الاعتراض جازياً أن تفصل بالدعوى الأصلية وترجئ الفصل في الاعتراض.",
            "explanation": "فصل الاعتراض عن الدعوى الأصلية.",
            "application": "يمكن فصل النظر في الاعتراض عن الدعوى الأصلية."
        },
        {
            "number": "210",
            "text": "لا يترتب على تقديم اعتراض الغير وقف تنفيذ الحكم المعترض عليه ما لم تقرر المحكمة كذلك.",
            "explanation": "أثر الاعتراض على التنفيذ.",
            "application": "لا يوقف الاعتراض التنفيذ إلا بقرار من المحكمة."
        },
        {
            "number": "211",
            "text": "إذا كان الغير محقاً في اعتراضه تعمل المحكمة الحكم في حدود ما يمس حقوق هذا الغير.",
            "explanation": "حكم الاعتراض المقبول.",
            "application": "إذا قبل الاعتراض يقتصر الحكم على حقوق المعترض."
        },
        {
            "number": "212",
            "text": "إذا أدخل الغير في اعتراضه يلزم بالرسوم والمصاريف والإتعاب المحاماة.",
            "explanation": "التكاليف في اعتراض الغير.",
            "application": "يلزم المعترض بالرسوم والمصاريف."
        },
        {
            "number": "213",
            "text": "يجوز للخصوم أن يطلبوا إعادة المحاكمة في الأحكام التي حازت قوة القضية المقضي بها في الحالات التالية: إذا حكم بناء على وثائق مزورة، إذا كان الحكم مبنياً على شهادة كاذبة.",
            "explanation": "أسباب إعادة المحاكمة.",
            "application": "تجوز إعادة المحاكمة لوجود تزوير أو شهادة زور."
        },
        {
            "number": "214",
            "text": "يبدأ ميعاد طلب إعادة المحاكمة من اليوم الذي يلي ظهور التزوير أو الذي حكم فيه على الشاهد بالشهادة الكاذبة.",
            "explanation": "ميعاد طلب إعادة المحاكمة.",
            "application": "يحسب ميعاد إعادة المحاكمة من تاريخ اكتشاف السبب."
        },
        {
            "number": "215",
            "text": "يقدم طلب إعادة المحاكمة إلى المحكمة التي أصدرت الحكم ويجري في ذلك تبادل اللوائح بين الطرفين.",
            "explanation": "إجراءات طلب إعادة المحاكمة.",
            "application": "يقدم الطلب للمحكمة المصدرة للحكم."
        },
        {
            "number": "216",
            "text": "يقدم طلب إعادة المحاكمة بالعريضة إلى المحكمة التي أصدرت الحكم بالوثائق المثبتة للحقوق.",
            "explanation": "متطلبات طلب إعادة المحاكمة.",
            "application": "يقدم الطلب بعريضة مع الوثائق المؤيدة."
        },
        {
            "number": "217",
            "text": "لا يترتب على طلب إعادة المحاكمة وقف تنفيذ الحكم ما لم تقرر المحكمة كذلك.",
            "explanation": "أثر طلب إعادة المحاكمة على التنفيذ.",
            "application": "لا يوقف طلب الإعادة التنفيذ إلا بقرار."
        },
        {
            "number": "218",
            "text": "لا تعيد المحكمة النظر إلا في الطلبات التي تناولها الاعتراض.",
            "explanation": "مدى إعادة المحاكمة.",
            "application": "تقتصر إعادة المحاكمة على النقاط المعترض عليها."
        },
        {
            "number": "219",
            "text": "تفصل المحكمة أبداً في جواز قبول طلب إعادة المحاكمة شكلاً ثم تنظر في الموضوع.",
            "explanation": "الفصل في القبول الشكلي أولاً.",
            "application": "تفصل المحكمة في القبول الشكلي قبل الموضوع."
        },
        {
            "number": "220",
            "text": "إذا حكم برد الطلب يحكم على مقدمه بمصاريف مقداره عشرة دنانير والرسوم والمصاريف.",
            "explanation": "تكاليف رد طلب إعادة المحاكمة.",
            "application": "يلزم مقدم الطلب بالتكاليف إذا رفض طلبه."
        },
        {
            "number": "221",
            "text": "الحكم في موضوع الطلب يحل محل الحكم السابق.",
            "explanation": "أثر حكم إعادة المحاكمة.",
            "application": "يستبدل الحكم الجديد الحكم السابق."
        },
        {
            "number": "222",
            "text": "لا يجوز طلب إعادة المحاكمة بشأن الحكم الذي يصدر بيع طلب إعادة المحاكمة.",
            "explanation": "منع الطعن المتكرر.",
            "application": "يمنع طلب إعادة المحاكمة في حكم الإعادة نفسه."
        },
        {
            "number": "223",
            "text": "إذا فقدت أي من أوراق الدعوى أو المستندات المقدمة فيها، فتعتبر النسخة المحفوظة في قاعدة البيانات بمثابة الأصل.",
            "explanation": "اعتماد النسخ الإلكترونية.",
            "application": "تعتمد النسخ الإلكترونية عند فقدان الأصول."
        },
        {
            "number": "224",
            "text": "تبقى محاكم البداية ومحاكم الاستئناف تنظر في جميع الدعاوى والقضايا المقامة لديها قبل تاريخ العمل بأحكام هذا القانون.",
            "explanation": "سريان القانون على الدعاوى الجارية.",
            "application": "يطبق القانون على الدعاوى المرفوعة بعد نفاذه."
        },
        {
            "number": "225",
            "text": "رئيس الوزراء والوزراء مكلفون بتنفيذ أحكام هذا القانون.",
            "explanation": "جهة تنفيذ القانون.",
            "application": "يتولى رئيس الوزراء والوزراء تنفيذ القانون."
        }
    ]
    
    # عرض المواد في مجموعات
    st.markdown("##### 🔄 المواد 205-212: اعتراض الغير")
    for article in other_appeals_articles[:8]:
        with st.expander(f"🔄 المادة {article['number']}", expanded=False):
            st.write(f"**النص:** {article['text']}")
            st.info(f"**💡 الشرح:** {article['explanation']}")
            st.success(f"**🎯 التطبيق العملي:** {article['application']}")
    
    st.markdown("##### 🔁 المواد 213-225: إعادة المحاكمة وأحكام ختامية")
    for article in other_appeals_articles[8:]:
        with st.expander(f"🔄 المادة {article['number']}", expanded=False):
            st.write(f"**النص:** {article['text']}")
            st.info(f"**💡 الشرح:** {article['explanation']}")
            st.success(f"**🎯 التطبيق العملي:** {article['application']}")

def show_appeals_tools():
    st.markdown("#### 🎯 أدوات الطعون والإستئنافات")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("##### 📈 محلل إمكانية الاستئناف")
        with st.form("appeal_analyzer"):
            judgment_type = st.selectbox("نوع الحكم", [
                "حكم ابتدائي",
                "حكم مستعجل", 
                "قرار إجرائي",
                "حكم نهائي"
            ])
            judgment_value = st.number_input("قيمة الحكم (دينار)", min_value=0, value=15000)
            appeal_reasons = st.text_area("أسباب الطعن المحتملة")
            error_type = st.selectbox("نوع الخطأ", [
                "خطأ في تطبيق القانون",
                "خطأ في تقدير الوقائع",
                "خلل في الإجراءات",
                "عدم الاختصاص"
            ])
            
            if st.form_submit_button("📈 تحليل إمكانية الاستئناف", use_container_width=True):
                analysis = analyze_appeal_possibility(
                    judgment_type, judgment_value, appeal_reasons, error_type
                )
                display_appeal_analysis(analysis)
    
    with col2:
        st.markdown("##### 🔍 منشئ عريضة التمييز")
        with st.form("cassation_builder"):
            legal_issue = st.text_area("النقطة القانونية المعقدة")
            law_violation = st.text_area("المخالفة القانونية")
            previous_judgments = st.text_area("الأحكام السابقة المتعارضة")
            requested_relief = st.text_area("الطلبات")
            
            if st.form_submit_button("🔍 إنشاء عريضة التمييز", use_container_width=True):
                draft = generate_cassation_request(
                    legal_issue, law_violation, previous_judgments, requested_relief
                )
                st.text_area("🔍 مسودة عريضة التمييز", value=draft, height=400)
    
    # حاسبة مواعيد الطعون
    st.markdown("##### ⏰ حاسبة مواعيد الطعون")
    
    with st.form("appeal_deadline_calculator"):
        col1, col2 = st.columns(2)
        
        with col1:
            judgment_date = st.date_input("تاريخ صدور الحكم")
            judgment_delivery = st.date_input("تاريخ تبليغ الحكم")
            appeal_type = st.selectbox("نوع الطعن", [
                "استئناف",
                "تمييز",
                "اعتراض الغير",
                "إعادة محاكمة"
            ])
            
        with col2:
            court_type = st.selectbox("المحكمة المصدرة", [
                "محكمة صلح",
                "محكمة بداية",
                "محكمة استئناف",
                "محكمة تمييز"
            ])
            has_attorney = st.checkbox("هل الخصم ممثل بمحام؟")
        
        if st.form_submit_button("⏰ حساب المواعيد", use_container_width=True):
            deadlines = calculate_appeal_deadlines(
                judgment_date, judgment_delivery, appeal_type, court_type, has_attorney
            )
            display_appeal_deadlines(deadlines)
    
    # حاسبة تكاليف الطعون
    st.markdown("##### 💰 حاسبة تكاليف الطعون")
    
    with st.form("appeal_costs_calculator"):
        col1, col2 = st.columns(2)
        
        with col1:
            appeal_court = st.selectbox("محكمة الطعن", [
                "محكمة استئناف",
                "محكمة تمييز"
            ])
            case_complexity = st.select_slider("تعقيد القضية", options=["بسيطة", "متوسطة", "معقدة", "عالية التعقيد"])
            
        with col2:
            documents_count = st.number_input("عدد المستندات", min_value=1, value=20)
            sessions_estimated = st.number_input("الجلسات المتوقعة", min_value=1, value=3)
        
        if st.form_submit_button("💰 حساب التكاليف", use_container_width=True):
            costs = calculate_appeal_costs(
                appeal_court, case_complexity, documents_count, sessions_estimated
            )
            display_appeal_costs(costs)

def analyze_appeal_possibility(judgment_type, value, reasons, error_type):
    """تحليل إمكانية الطعن في الحكم"""
    
    analysis = {
        'possibility': '',
        'recommended_appeal': '',
        'success_probability': '',
        'estimated_duration': '',
        'requirements': [],
        'recommendations': []
    }
    
    # تحليل الإمكانية
    if judgment_type == "حكم نهائي" and value > 10000:
        analysis['possibility'] = "عالية"
        analysis['recommended_appeal'] = "تمييز"
        analysis['success_probability'] = "40-60%"
        analysis['estimated_duration'] = "6-12 شهر"
    elif judgment_type == "حكم ابتدائي":
        analysis['possibility'] = "عالية"
        analysis['recommended_appeal'] = "استئناف"
        analysis['success_probability'] = "50-70%"
        analysis['estimated_duration'] = "3-6 أشهر"
    elif judgment_type == "قرار إجرائي":
        analysis['possibility'] = "متوسطة"
        analysis['recommended_appeal'] = "استئناف"
        analysis['success_probability'] = "30-50%"
        analysis['estimated_duration'] = "2-4 أشهر"
    else:
        analysis['possibility'] = "منخفضة"
        analysis['recommended_appeal'] = "غير موصى به"
        analysis['success_probability'] = "10-30%"
        analysis['estimated_duration'] = "غير محدد"
    
    # المتطلبات
    analysis['requirements'] = [
        "عريضة طعن مسببة",
        "صورة من الحكم المطعون فيه",
        "دفع الرسوم القانونية",
        "تقديم الطلب خلال الميعاد"
    ]
    
    # التوصيات
    if "خطأ في تطبيق القانون" in error_type:
        analysis['recommendations'].append("التركيز على النقاط القانونية في الطعن")
    if "خلل في الإجراءات" in error_type:
        analysis['recommendations'].append("إثبات الخلل الإجرائي بشكل مفصل")
    
    analysis['recommendations'].append("استشارة محامٍ متخصص في الطعون")
    
    return analysis

def display_appeal_analysis(analysis):
    """عرض نتيجة تحليل الطعن"""
    
    st.success(f"## 📈 نتيجة التحليل: إمكانية {analysis['possibility']}")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info(f"**📊 الطعن الموصى به:** {analysis['recommended_appeal']}")
        st.info(f"**⏰ المدة المتوقعة:** {analysis['estimated_duration']}")
        
    with col2:
        st.info(f"**🎯 احتمالية النجاح:** {analysis['success_probability']}")
        
    with col3:
        if analysis['requirements']:
            st.warning("**📋 المتطلبات:**")
            for requirement in analysis['requirements']:
                st.write(f"• {requirement}")
    
    if analysis['recommendations']:
        st.markdown("##### 💡 التوصيات:")
        for recommendation in analysis['recommendations']:
            st.write(f"• {recommendation}")

def generate_cassation_request(legal_issue, violation, previous_judgments, relief):
    """إنشاء مسودة عريضة تمييز"""
    
    request = f"""
    عريضة تمييز
    النقطة القانونية المعقدة:
    {legal_issue}
    
    المخالفة القانونية:
    {violation}
    
    الأحكام السابقة المتعارضة:
    {previous_judgments}
    
    الطلبات:
    {relief}
    
    الأسباب:
    1. مخالفة القانون في تطبيق النصوص
    2. خطأ في تفسير القواعد القانونية  
    3. تعارض مع المبادئ القانونية المستقرة
    4. خرق قواعد الاختصاص أو الإجراءات
    
    المرفقات:
    - صورة من الحكم المطعون فيه
    - صور من الأحكام السابقة المتعارضة
    - المذكرات القانونية المؤيدة
    - النصوص القانونية المعتمدة
    
    توقيع المميز/الوكيل:
    ___________________
    التاريخ: __________
    """
    
    return request

def calculate_appeal_deadlines(judgment_date, delivery_date, appeal_type, court_type, has_attorney):
    """حساب مواعيد الطعون"""
    
    base_days = 0
    
    # تحديد الموعد حسب نوع الطعن
    if appeal_type == "استئناف":
        base_days = 30
    elif appeal_type == "تمييز":
        base_days = 30
    elif appeal_type == "اعتراض الغير":
        base_days = 90  # 3 أشهر
    elif appeal_type == "إعادة محاكمة":
        base_days = 30
    
    # استخدام تاريخ التبليغ إذا كان متاحاً
    if delivery_date:
        start_date = delivery_date
    else:
        start_date = judgment_date
    
    deadline_date = start_date + timedelta(days=base_days)
    remaining_days = (deadline_date - datetime.now().date()).days
    
    return {
        'start_date': start_date,
        'deadline_days': base_days,
        'deadline_date': deadline_date,
        'remaining_days': remaining_days,
        'appeal_type': appeal_type,
        'court_type': court_type
    }

def display_appeal_deadlines(deadlines):
    """عرض مواعيد الطعون"""
    
    st.success(f"## ⏰ المواعيد القانونية للطعن")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info(f"**تاريخ البدء:** {deadlines['start_date'].strftime('%Y-%m-%d')}")
        st.info(f"**نوع الطعن:** {deadlines['appeal_type']}")
        
    with col2:
        st.info(f"**المدة القانونية:** {deadlines['deadline_days']} يوم")
        st.info(f"**المحكمة:** {deadlines['court_type']}")
        
    with col3:
        st.info(f"**آخر موعد:** {deadlines['deadline_date'].strftime('%Y-%m-%d')}")
        st.info(f"**الأيام المتبقية:** {deadlines['remaining_days']} يوم")
    
    # تحذيرات
    if deadlines['remaining_days'] < 0:
        st.error("⚠️ انتهى الموعد القانوني للطعن!")
    elif deadlines['remaining_days'] <= 7:
        st.warning("🚨 الموعد النهائي يقترب! يوصى بتقديم الطعن فوراً.")
    elif deadlines['remaining_days'] <= 15:
        st.warning("⚠️ أقل من أسبوعين متبقيان، يوصى بالإسراع في إعداد الطعن.")

def calculate_appeal_costs(appeal_court, complexity, documents, sessions):
    """حساب تكاليف الطعون"""
    
    base_costs = {
        'رسوم الطعن': 0,
        'أتعاب المحاماة': 0,
        'مصاريف الجلسات': 0,
        'مصاريف المستندات': 0,
        'مصاريف أخرى': 500
    }
    
    # تحديد الرسوم حسب محكمة الطعن
    if appeal_court == "محكمة استئناف":
        base_costs['رسوم الطعن'] = 250
        base_costs['أتعاب المحاماة'] = 1500
    elif appeal_court == "محكمة تمييز":
        base_costs['رسوم الطعن'] = 500
        base_costs['أتعاب المحاماة'] = 3000
    
    # تعديل حسب التعقيد
    complexity_multipliers = {
        "بسيطة": 1.0,
        "متوسطة": 1.5,
        "معقدة": 2.0,
        "عالية التعقيد": 3.0
    }
    
    multiplier = complexity_multipliers.get(complexity, 1.0)
    
    # تطبيق المضاعف
    for key in ['أتعاب المحاماة', 'مصاريف الجلسات', 'مصاريف المستندات']:
        base_costs[key] *= multiplier
    
    # إضافة التكاليف الإضافية
    base_costs['مصاريف الجلسات'] = sessions * 200
    base_costs['مصاريف المستندات'] = documents * 10
    
    total = sum(base_costs.values())
    
    return {
        'costs_breakdown': base_costs,
        'total_cost': total,
        'appeal_court': appeal_court,
        'complexity': complexity
    }

def display_appeal_costs(costs):
    """عرض تكاليف الطعون"""
    
    st.success(f"## 💰 التكاليف الإجمالية: {costs['total_cost']:,.0f} دينار")
    
    st.markdown("##### 📊 تفصيل التكاليف:")
    costs_df = pd.DataFrame({
        "البند": list(costs['costs_breakdown'].keys()),
        "المبلغ (دينار)": list(costs['costs_breakdown'].values())
    })
    
    st.dataframe(costs_df, use_container_width=True, hide_index=True)
    
    st.info(f"**⚖️ محكمة الطعن:** {costs['appeal_court']}")
    st.info(f"**🎯 مستوى التعقيد:** {costs['complexity']}")# # ==========================
# 🔧 قسم أدوات المحامي - الكود الكامل
# ==========================

def show_lawyer_tools_section():
    """قسم أدوات المحامي - الإصدار الكامل"""
    show_breadcrumbs("🔧 أدوات المحامي")
    
    st.markdown("""
    <div class="main-header">
        <h1>🔧 أدوات المحامي المتخصص</h1>
        <p>مجموعة متكاملة من الأدوات العملية والنماذج الجاهزة للمحامين المتخصصين في قانون أصول المحاكمات المدنية</p>
    </div>
    """, unsafe_allow_html=True)

    tabs = st.tabs(["📋 مكتبة النماذج", "🧮 الحاسبات القانونية", "📅 منظم القضايا", "⚡ أدوات سريعة"])

    with tabs[0]:
        show_templates_library()
    with tabs[1]:
        show_legal_calculators()
    with tabs[2]:
        show_cases_organizer()
    with tabs[3]:
        show_quick_tools()

def show_templates_library():
    """مكتبة النماذج القانونية الكاملة"""
    st.markdown("#### 📋 مكتبة النماذج القانونية")
    
    categories = st.selectbox("اختر الفئة", [
        "لوائح الدعاوى",
        "الدفوع والطلبات",
        "الإجراءات الوقائية", 
        "الطعون والاستئنافات",
        "مذكرات ومرافعات",
        "اتفاقيات وتسويات"
    ])
    
    if categories == "لوائح الدعاوى":
        show_lawsuit_templates()
    elif categories == "الدفوع والطلبات":
        show_defense_templates()
    elif categories == "الإجراءات الوقائية":
        show_preventive_templates()
    elif categories == "الطعون والاستئنافات":
        show_appeal_templates()
    elif categories == "مذكرات ومرافعات":
        show_memo_templates()
    elif categories == "اتفاقيات وتسويات":
        show_settlement_templates()

def show_lawsuit_templates():
    """نماذج لوائح الدعاوى"""
    st.markdown("##### 📄 نماذج لوائح الدعاوى")
    
    templates = [
        {
            "name": "لائحة دعوى تعاقدية",
            "description": "نموذج شامل لدعوى التعاقد والإلتزامات العقدية",
            "content": """
            عريضة دعوى تعاقدية
            المحكمة: __________
            
            المدعي: __________
            المدعى عليه: __________
            
            الموضوع: دعوى تنفيذ عقد/فسخ عقد/تعويض
            
            الوقائع:
            1. تم إبرام العقد بين الطرفين بتاريخ __________
            2. نص العقد على __________
            3. المدعى عليه أخل بالتزاماته __________
            4. المدعي قام ب __________
            
            الأسباب القانونية:
            - المادة __________ من القانون المدني
            - المادة __________ من قانون أصول المحاكمات
            - __________
            
            الطلبات:
            1. الحكم __________
            2. __________
            3. تحميل المدعى عليه المصاريف
            
            المرفقات:
            - صورة العقد
            - المستندات المؤيدة
            - __________
            
            توقيع المدعي/الوكيل:
            ___________________
            التاريخ: __________
            """
        },
        {
            "name": "لائحة دعوى تعويض",
            "description": "نموذج لدعوى المطالبة بالتعويض عن الأضرار",
            "content": """
            عريضة دعوى تعويض
            المحكمة: __________
            
            المدعي: __________  
            المدعى عليه: __________
            
            الموضوع: دعوى تعويض عن __________
            
            الوقائع:
            1. في تاريخ __________ وقع __________
            2. نتج عن ذلك الأضرار التالية __________
            3. قيم الأضرار __________
            4. __________
            
            الأسباب القانونية:
            - المسؤولية التقصيرية
            - __________
            
            الطلبات:
            1. الحكم بالتعويض __________
            2. __________
            """
        },
        {
            "name": "لائحة دعوى عمالية",
            "description": "نموذج لدعاوى العمل والمنازعات العمالية",
            "content": """
            عريضة دعوى عمالية
            المحكمة: محكمة العمل/__________
            
            المدعي (العامل): __________
            المدعى عليه (صاحب العمل): __________
            
            الموضوع: دعوى __________ (إنهاء تعسفي/مستحقات مالية/أخرى)
            
            الوقائع:
            1. تاريخ التعيين: __________
            2. الراتب الأخير: __________ دينار
            3. تاريخ إنهاء الخدمة: __________
            4. سبب النزاع: __________
            
            الأسباب القانونية:
            - قانون العمل الأردني
            - __________
            
            الطلبات:
            1. __________
            2. __________
            """
        }
    ]
    
    for template in templates:
        with st.expander(f"📄 {template['name']} - {template['description']}", expanded=False):
            st.text_area("النموذج", value=template['content'], height=300, key=f"template_{template['name']}")
            col1, col2 = st.columns(2)
            with col1:
                st.download_button("📥 تحميل", template['content'], file_name=f"{template['name']}.txt")
            with col2:
                if st.button("🎯 استخدام", key=f"use_{template['name']}"):
                    st.success("تم نسخ النموذج")

def show_defense_templates():
    """نماذج الدفوع والطلبات"""
    st.markdown("##### 🛡️ نماذج الدفوع والطلبات")
    
    defenses = [
        {
            "name": "دفع بعدم الاختصاص",
            "description": "نموذج دفع بعدم اختصاص المحكمة",
            "content": """
            دفع بعدم الاختصاص
            الدعوى: __________
            
            أسباب الدفع:
            1. المحكمة غير مختصة نوعياً __________
            2. __________
            3. __________
            
            الطلبات:
            1. الحكم بعدم اختصاص المحكمة
            2. رد الدعوى
            3. __________
            """
        },
        {
            "name": "طلب وقف الدعوى", 
            "description": "نموذج طلب وقف سير الدعوى",
            "content": """
            طلب وقف الدعوى
            الدعوى: __________
            
            أسباب الوقف:
            1. __________
            2. __________
            
            المدة المطلوبة: __________
            
            الطلبات:
            1. وقف الدعوى لمدة __________
            2. __________
            """
        },
        {
            "name": "دفع بالتقادم",
            "description": "نموذج دفع بالتقادم المسقط",
            "content": """
            دفع بالتقادم المسقط
            الدعوى: __________
            
            الأسباب:
            1. مضي المدة القانونية للتقادم __________
            2. __________
            3. __________
            
            الطلبات:
            1. الحكم بسقوط الحق بالتقادم
            2. رد الدعوى
            3. تحميل المدعي المصاريف
            """
        }
    ]
    
    for defense in defenses:
        with st.expander(f"🛡️ {defense['name']}", expanded=False):
            st.text_area("النموذج", value=defense['content'], height=200, key=f"defense_{defense['name']}")
            st.download_button("📥 تحميل", defense['content'], file_name=f"{defense['name']}.txt")

def show_preventive_templates():
    """نماذج الإجراءات الوقائية"""
    st.markdown("#### 🛡️ نماذج الإجراءات الوقائية")
    
    templates = [
        {
            "name": "طلب حجز تحفظي",
            "description": "نموذج طلب توقيع حجز تحفظي على أموال المدين",
            "content": """
            طلب حجز تحفظي
            المحكمة: قاضي الأمور المستعجلة/__________
            
            الطالب: __________
            المحجوز عليه: __________
            
            الموضوع: طلب توقيع حجز تحفظي على أموال المدين
            
            الأسباب:
            1. وجود دين مستحق للطالب على المدين بمبلغ __________ دينار
            2. خشية تهريب المدين لأمواله أو التصرف فيها
            3. __________
            
            المستندات المؤيدة:
            - __________
            - __________
            
            الطلبات:
            1. توقيع حجز تحفظي على أموال المدين
            2. __________
            3. تحميل المدين المصاريف
            
            توقيع الطالب/الوكيل:
            ___________________
            """
        },
        {
            "name": "طلب منع من السفر",
            "description": "نموذج طلب منع المدين من السفر خوفاً من تهريب الأموال",
            "content": """
            طلب منع من السفر
            المحكمة: __________
            
            الطالب: __________
            الممنوع من السفر: __________
            
            الأسباب:
            1. وجود دين مستحق بمبلغ __________
            2. خشية هرب المدين أو تهريب أمواله
            3. __________
            
            الطلبات:
            1. منع المدين من السفر خارج المملكة
            2. إلزامه بتقديم كفالة مناسبة
            3. __________
            """
        }
    ]
    
    for template in templates:
        with st.expander(f"🛡️ {template['name']} - {template['description']}", expanded=False):
            st.text_area("النموذج", value=template['content'], height=300, key=f"preventive_{template['name']}")
            st.download_button("📥 تحميل", template['content'], file_name=f"{template['name']}.txt")

def show_appeal_templates():
    """نماذج الطعون والاستئنافات"""
    st.markdown("#### 📈 نماذج الطعون والاستئنافات")
    
    templates = [
        {
            "name": "عريضة استئناف",
            "description": "نموذج عريضة استئناف ضد حكم محكمة البداية",
            "content": """
            عريضة استئناف
            المحكمة: محكمة الاستئناف/__________
            
            المستأنف: __________
            المستأنف ضده: __________
            
            الحكم المستأنف: الصادر عن محكمة __________ بتاريخ __________
            
            أسباب الاستئناف:
            1. الخطأ في تطبيق القانون __________
            2. __________
            3. __________
            
            الطلبات:
            1. نقض الحكم المستأنف
            2. الفصل في الموضوع/إعادة الدعوى
            3. تحميل الخصم المصاريف
            
            توقيع المستأنف/الوكيل:
            ___________________
            """
        },
        {
            "name": "عريضة تمييز",
            "description": "نموذج عريضة تمييز ضد حكم محكمة الاستئناف",
            "content": """
            عريضة تمييز
            المحكمة: محكمة التمييز/__________
            
            المميز: __________
            المميز ضده: __________
            
            الحكم المميز: الصادر عن محكمة __________ بتاريخ __________
            
            النقاط القانونية:
            1. مخالفة القانون في __________
            2. __________
            3. __________
            
            الطلبات:
            1. قبول التمييز شكلاً
            2. نقض الحكم المميز
            3. __________
            """
        }
    ]
    
    for template in templates:
        with st.expander(f"📈 {template['name']} - {template['description']}", expanded=False):
            st.text_area("النموذج", value=template['content'], height=300, key=f"appeal_{template['name']}")
            st.download_button("📥 تحميل", template['content'], file_name=f"{template['name']}.txt")

def show_memo_templates():
    """نماذج المذكرات والمرافعات"""
    st.markdown("#### 📝 نماذج المذكرات والمرافعات")
    
    templates = [
        {
            "name": "مذكرة مرافعة",
            "description": "نموذج مذكرة مرافعة شاملة",
            "content": """
            مذكرة مرافعة
            القضية: __________
            المحكمة: __________
            
            السيد/__________ المحترم
            
            الموضوع: مرافعة في __________
            
            المقدمة:
            __________
            
            الوقائع:
            1. __________
            2. __________
            
            المناقشة القانونية:
            - __________
            - __________
            
            الخلاصة:
            - __________
            - __________
            
            وتفضلوا بقبول فائق الاحترام...
            
            المحامي: __________
            """
        },
        {
            "name": "مذكرة قانونية",
            "description": "نموذج مذكرة قانونية متخصصة",
            "content": """
            مذكرة قانونية
            الموضوع: __________
            
            التحليل القانوني:
            
            ١. الإطار القانوني:
            - __________
            - __________
            
            ٢. التطبيق على الواقعة:
            - __________
            - __________
            
            ٣. النتائج والتوصيات:
            - __________
            - __________
            
            الخاتمة:
            __________
            """
        }
    ]
    
    for template in templates:
        with st.expander(f"📝 {template['name']} - {template['description']}", expanded=False):
            st.text_area("النموذج", value=template['content'], height=300, key=f"memo_{template['name']}")
            st.download_button("📥 تحميل", template['content'], file_name=f"{template['name']}.txt")

def show_settlement_templates():
    """نماذج الاتفاقيات والتسويات"""
    st.markdown("#### 🤝 نماذج الاتفاقيات والتسويات")
    
    templates = [
        {
            "name": "اتفاق صلح",
            "description": "نموذج اتفاق صلح وإنهاء المنازعات",
            "content": """
            اتفاق صلح
            الطرف الأول: __________
            الطرف الثاني: __________
            
            تم الاتفاق بين الطرفين على ما يلي:
            
            ١. موضوع الصلح: __________
            
            ٢. بنود الاتفاق:
            - __________
            - __________
            - __________
            
            ٣. التزامات الطرفين:
            - __________
            - __________
            
            ٤. إنهاء الدعوى:
            يتنازل الطرفان عن جميع الدعاوى والطلبات المتعلقة بموضوع هذا الصلح
            
            وتوقيع الطرفين:
            الطرف الأول: __________    الطرف الثاني: __________
            """
        },
        {
            "name": "اتفاق تسوية مالية",
            "description": "نموذج اتفاق تسوية المطالبات المالية",
            "content": """
            اتفاق تسوية مالية
            بين: __________ (الدائن)
            و: __________ (المدين)
            
            تم الاتفاق على:
            
            ١. المبلغ الأصلي: __________ دينار
            ٢. المبلغ المتفق عليه: __________ دينار
            ٣. طريقة السداد: __________
            ٤. مواعيد السداد: __________
            
            ٥. آثار الاتفاق:
            - إنهاء جميع المطالبات المالية
            - __________
            
            وتوقيع الطرفين:
            الدائن: __________    المدين: __________
            """
        }
    ]
    
    for template in templates:
        with st.expander(f"🤝 {template['name']} - {template['description']}", expanded=False):
            st.text_area("النموذج", value=template['content'], height=300, key=f"settlement_{template['name']}")
            st.download_button("📥 تحميل", template['content'], file_name=f"{template['name']}.txt")

def show_legal_calculators():
    """الحاسبات القانونية المتكاملة"""
    st.markdown("#### 🧮 الحاسبات القانونية")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("##### ⏰ حاسبة المواعيد الشاملة")
        with st.form("comprehensive_deadline_calculator"):
            event_type = st.selectbox("نوع الإجراء", [
                "تبليغ",
                "لائحة جوابية", 
                "استئناف",
                "تمييز",
                "تنفيذ حكم"
            ])
            start_date = st.date_input("تاريخ البدء")
            complexity = st.select_slider("التعقيد", options=["بسيط", "متوسط", "معقد"])
            
            if st.form_submit_button("⏰ حساب المواعيد", use_container_width=True):
                deadlines = calculate_comprehensive_deadlines(event_type, start_date, complexity)
                display_comprehensive_deadlines(deadlines)
    
    with col2:
        st.markdown("##### 💰 حاسبة التكاليف المتوقعة")
        with st.form("comprehensive_costs_calculator"):
            case_value = st.number_input("قيمة الدعوى (دينار)", min_value=0, value=50000)
            case_type = st.selectbox("نوع القضية", [
                "تعاقدية",
                "تعويض",
                "عقارية",
                "تجارية"
            ])
            expected_duration = st.number_input("المدة المتوقعة (أشهر)", min_value=1, value=6)
            
            if st.form_submit_button("💰 حساب التكاليف", use_container_width=True):
                costs = calculate_comprehensive_costs(case_value, case_type, expected_duration)
                display_comprehensive_costs(costs)
    
    # حاسبة الفوائد والنفقات
    st.markdown("##### 📈 حاسبة الفوائد والنفقات")
    
    with st.form("interest_calculator"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            principal = st.number_input("المبلغ الأصلي (دينار)", min_value=0, value=100000)
            interest_rate = st.number_input("سعر الفائدة (%)", min_value=0.0, value=8.0)
            
        with col2:
            start_date = st.date_input("تاريخ الاستحقاق")
            calculation_date = st.date_input("تاريخ الحساب")
            
        with col3:
            interest_type = st.selectbox("نوع الفائدة", ["بسيطة", "مركبة"])
            include_costs = st.checkbox("احتساب المصاريف القضائية")
        
        if st.form_submit_button("📈 حساب الفوائد", use_container_width=True):
            interest_data = calculate_legal_interest(
                principal, interest_rate, start_date, calculation_date, interest_type, include_costs
            )
            display_interest_calculation(interest_data)

def calculate_comprehensive_deadlines(event_type, start_date, complexity):
    """حساب المواعيد الشاملة"""
    
    base_days = {
        "تبليغ": 7,
        "لائحة جوابية": 30,
        "استئناف": 30,
        "تمييز": 30,
        "تنفيذ حكم": 90
    }
    
    complexity_multipliers = {
        "بسيط": 1.0,
        "متوسط": 1.2,
        "معقد": 1.5
    }
    
    base_days = base_days.get(event_type, 30)
    multiplier = complexity_multipliers.get(complexity, 1.0)
    adjusted_days = int(base_days * multiplier)
    
    deadline_date = start_date + timedelta(days=adjusted_days)
    remaining_days = (deadline_date - datetime.now().date()).days
    
    return {
        'event_type': event_type,
        'base_days': base_days,
        'adjusted_days': adjusted_days,
        'deadline_date': deadline_date,
        'remaining_days': remaining_days,
        'complexity': complexity
    }

def display_comprehensive_deadlines(deadlines):
    """عرض المواعيد الشاملة"""
    
    st.success(f"## ⏰ المواعيد المحسوبة")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info(f"**الإجراء:** {deadlines['event_type']}")
        st.info(f"**المدة الأساسية:** {deadlines['base_days']} يوم")
        
    with col2:
        st.info(f"**المدة المعدلة:** {deadlines['adjusted_days']} يوم")
        st.info(f"**مستوى التعقيد:** {deadlines['complexity']}")
        
    with col3:
        st.info(f"**الموعد النهائي:** {deadlines['deadline_date'].strftime('%Y-%m-%d')}")
        st.info(f"**الأيام المتبقية:** {deadlines['remaining_days']} يوم")

def calculate_comprehensive_costs(case_value, case_type, duration):
    """حساب التكاليف الشاملة"""
    
    base_costs = {
        "تعاقدية": 2000,
        "تعويض": 2500,
        "عقارية": 3000,
        "تجارية": 3500
    }
    
    base_cost = base_costs.get(case_type, 2000)
    
    # إضافة نسبة من قيمة الدعوى
    value_percentage = case_value * 0.05  # 5% من قيمة الدعوى
    duration_cost = duration * 500  # 500 دينار شهرياً
    
    total_cost = base_cost + value_percentage + duration_cost
    
    return {
        'base_cost': base_cost,
        'value_percentage': value_percentage,
        'duration_cost': duration_cost,
        'total_cost': total_cost,
        'case_value': case_value,
        'case_type': case_type,
        'duration': duration
    }

def display_comprehensive_costs(costs):
    """عرض التكاليف الشاملة"""
    
    st.success(f"## 💰 التكاليف المتوقعة: {costs['total_cost']:,.0f} دينار")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"**التكلفة الأساسية:** {costs['base_cost']:,.0f} دينار")
        st.info(f"**نسبة من قيمة الدعوى:** {costs['value_percentage']:,.0f} دينار")
        
    with col2:
        st.info(f"**تكلفة المدة:** {costs['duration_cost']:,.0f} دينار")
        st.info(f"**نوع القضية:** {costs['case_type']}")

def calculate_legal_interest(principal, rate, start_date, calculation_date, interest_type, include_costs):
    """حساب الفوائد القانونية"""
    
    days_diff = (calculation_date - start_date).days
    years = days_diff / 365.25
    
    if interest_type == "بسيطة":
        interest = principal * (rate / 100) * years
    else:  # مركبة
        interest = principal * ((1 + rate / 100) ** years - 1)
    
    total_amount = principal + interest
    
    if include_costs:
        additional_costs = total_amount * 0.1  # افتراضي 10% مصاريف قضائية
        total_amount += additional_costs
    
    return {
        'principal': principal,
        'interest': interest,
        'total_amount': total_amount,
        'days': days_diff,
        'years': years,
        'include_costs': include_costs
    }

def display_interest_calculation(interest_data):
    """عرض حساب الفوائد"""
    
    st.success(f"## 📈 المبلغ الإجمالي: {interest_data['total_amount']:,.2f} دينار")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info(f"**المبلغ الأصلي:** {interest_data['principal']:,.2f} دينار")
        st.info(f"**الفائدة:** {interest_data['interest']:,.2f} دينار")
        
    with col2:
        st.info(f"**عدد الأيام:** {interest_data['days']} يوم")
        st.info(f"**عدد السنوات:** {interest_data['years']:.2f} سنة")
        
    with col3:
        if interest_data['include_costs']:
            st.info("**شامل المصاريف القضائية**")

def show_cases_organizer():
    """منظم القضايا والمهام المتكامل"""
    st.markdown("#### 📅 منظم القضايا والمهام")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("##### 📋 إضافة قضية جديدة")
        with st.form("new_case_form"):
            case_number = st.text_input("رقم القضية *")
            court_name = st.text_input("اسم المحكمة *")
            case_type = st.selectbox("نوع القضية", [
                "تعاقدية", "تعويض", "عقارية", "تجارية", "أحوال شخصية"
            ])
            next_session = st.date_input("موعد الجلسة القادمة")
            priority = st.select_slider("الأولوية", options=["منخفضة", "متوسطة", "عالية", "عاجلة"])
            
            if st.form_submit_button("💾 حفظ القضية", use_container_width=True):
                if case_number and court_name:
                    save_case_to_organizer({
                        'case_number': case_number,
                        'court_name': court_name,
                        'case_type': case_type,
                        'next_session': next_session,
                        'priority': priority
                    })
                    st.success("✅ تم حفظ القضية بنجاح!")
                else:
                    st.error("❌ يرجى ملء الحقول الإلزامية (*)")
    
    with col2:
        st.markdown("##### 🔔 المهام القادمة")
        
        # قائمة المهام الافتراضية
        tasks = [
            {"القضية": "١٢٣/٢٠٢٤", "المهمة": "تقديم لائحة جوابية", "الموعد": "٢٠٢٤-٠٣-١٥", "الأولوية": "عالية"},
            {"القضية": "٤٥٦/٢٠٢٤", "المهمة": "حضور جلسة", "الموعد": "٢٠٢٤-٠٣-٢٠", "الأولوية": "عاجلة"},
            {"القضية": "٧٨٩/٢٠٢٤", "المهمة": "تقديم طعن", "الموعد": "٢٠٢٤-٠٣-٢٥", "الأولوية": "متوسطة"}
        ]
        
        for task in tasks:
            with st.expander(f"📌 {task['القضية']} - {task['المهمة']}", expanded=False):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**الموعد:** {task['الموعد']}")
                with col2:
                    st.write(f"**الأولوية:** {task['الأولوية']}")
                
                if task['الأولوية'] in ["عاجلة", "عالية"]:
                    st.warning("⏰ مهمة عاجلة!")
                
                if st.button("✅ إكمال", key=f"complete_{task['القضية']}"):
                    st.success("تم إكمال المهمة")

def save_case_to_organizer(case_data):
    """حفظ القضية في المنظم"""
    if 'cases' not in st.session_state:
        st.session_state.cases = []
    
    st.session_state.cases.append(case_data)

def show_quick_tools():
    """الأدوات السريعة المتكاملة"""
    st.markdown("#### ⚡ أدوات سريعة")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📋 منشئ المرافعات", use_container_width=True, key="pleading_builder_btn"):
            show_pleading_builder()
        
        if st.button("🧮 حاسبة الرسوم", use_container_width=True, key="fees_calculator_btn"):
            show_fees_calculator()
            
        if st.button("📅 منظم الجلسات", use_container_width=True, key="session_planner_btn"):
            show_session_planner()
    
    with col2:
        if st.button("⚖️ مساعد الدفوع", use_container_width=True, key="defenses_assistant_btn"):
            show_defenses_assistant()
            
        if st.button("🔍 مدقق المستندات", use_container_width=True, key="documents_checker_btn"):
            show_documents_checker()
    
    with col3:
        if st.button("💰 مقدر التعويضات", use_container_width=True, key="compensation_estimator_btn"):
            show_compensation_estimator()
            
        if st.button("⏰ منبه المواعيد", use_container_width=True, key="deadline_alerts_btn"):
            show_deadline_alerts()
            
        if st.button("📈 محلل السوابق", use_container_width=True, key="precedents_analyzer_btn"):
            show_precedents_analyzer()

def show_pleading_builder():
    """منشئ المرافعات"""
    st.markdown("##### 📋 منشئ المرافعات")
    
    with st.form("pleading_builder_form"):
        case_details = st.text_area("تفاصيل القضية")
        legal_points = st.text_area("النقاط القانونية")
        requested_relief = st.text_area("الطلبات")
        supporting_docs = st.text_area("المستندات المؤيدة")
        
        if st.form_submit_button("📄 إنشاء مسودة المرافعة", use_container_width=True):
            pleading_draft = generate_pleading_draft(case_details, legal_points, requested_relief, supporting_docs)
            st.text_area("📄 مسودة المرافعة", value=pleading_draft, height=400)

def show_fees_calculator():
    """حاسبة الرسوم الشاملة"""
    st.markdown("##### 💰 حاسبة الرسوم الشاملة")
    
    with st.form("comprehensive_fees_calculator"):
        col1, col2 = st.columns(2)
        
        with col1:
            case_stage = st.selectbox("مرحلة القضية", [
                "قبل الرفع",
                "مرحلة الرفع",
                "أثناء المحاكمة", 
                "الاستئناف",
                "التمييز"
            ])
            hearings_count = st.number_input("عدد الجلسات المتوقعة", min_value=0, value=5)
            
        with col2:
            documents_count = st.number_input("عدد المستندات", min_value=0, value=15)
            complexity_level = st.select_slider("مستوى التعقيد", options=["بسيط", "متوسط", "معقد", "عالٍ"])
        
        if st.form_submit_button("💰 حساب الرسوم", use_container_width=True):
            fees = calculate_comprehensive_fees(case_stage, hearings_count, documents_count, complexity_level)
            display_comprehensive_fees(fees)

def generate_pleading_draft(details, points, relief, docs):
    """إنشاء مسودة مرافعة"""
    
    draft = f"""
    مذكرة مرافعة
    تفاصيل القضية:
    {details}
    
    النقاط القانونية:
    {points}
    
    الطلبات:
    {relief}
    
    المستندات المؤيدة:
    {docs}
    
    الخلاصة:
    - __________
    - __________
    - __________
    
    توقيع المحامي:
    ___________________
    التاريخ: __________
    """
    
    return draft

def calculate_comprehensive_fees(stage, hearings, documents, complexity):
    """حساب الرسوم الشاملة"""
    
    base_fees = {
        "قبل الرفع": 500,
        "مرحلة الرفع": 1000,
        "أثناء المحاكمة": 2000,
        "الاستئناف": 3000,
        "التمييز": 4000
    }
    
    complexity_multipliers = {
        "بسيط": 1.0,
        "متوسط": 1.5,
        "معقد": 2.0,
        "عالٍ": 3.0
    }
    
    base_fee = base_fees.get(stage, 1000)
    multiplier = complexity_multipliers.get(complexity, 1.0)
    
    additional_costs = (hearings * 200) + (documents * 50)
    total_fees = (base_fee * multiplier) + additional_costs
    
    return {
        'base_fee': base_fee,
        'complexity_multiplier': multiplier,
        'additional_costs': additional_costs,
        'total_fees': total_fees,
        'stage': stage,
        'complexity': complexity
    }

def display_comprehensive_fees(fees):
    """عرض الرسوم الشاملة"""
    
    st.success(f"## 💰 الرسوم الإجمالية: {fees['total_fees']:,.0f} دينار")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"**الرسوم الأساسية:** {fees['base_fee']:,.0f} دينار")
        st.info(f"**مضاعف التعقيد:** {fees['complexity_multiplier']:.1f}x")
        
    with col2:
        st.info(f"**التكاليف الإضافية:** {fees['additional_costs']:,.0f} دينار")
        st.info(f"**مرحلة القضية:** {fees['stage']}")

def show_session_planner():
    """منظم الجلسات المتقدم"""
    st.markdown("#### 📅 منظم الجلسات المتقدم")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("##### 🗓️ إضافة جلسة جديدة")
        with st.form("session_planner_form"):
            case_number = st.text_input("رقم القضية *")
            court_name = st.text_input("المحكمة *")
            session_date = st.date_input("تاريخ الجلسة *")
            session_time = st.time_input("وقت الجلسة *")
            session_type = st.selectbox("نوع الجلسة", [
                "جلسة مرافعة", "جلسة إثبات", "جلسة شهود", 
                "جلسة خبير", "جلسة النطق بالحكم"
            ])
            judge_name = st.text_input("اسم القاضي")
            
            if st.form_submit_button("💾 حفظ الجلسة", use_container_width=True):
                if case_number and court_name:
                    save_session_to_planner({
                        'case_number': case_number,
                        'court_name': court_name,
                        'session_date': session_date,
                        'session_time': session_time,
                        'session_type': session_type,
                        'judge_name': judge_name
                    })
                    st.success("✅ تم حفظ الجلسة بنجاح!")
                else:
                    st.error("❌ يرجى ملء الحقول الإلزامية (*)")
    
    with col2:
        st.markdown("##### 📋 الجلسات القادمة")
        
        upcoming_sessions = [
            {
                "case_number": "١٢٣/٢٠٢٤",
                "court": "محكمة بداية عمان",
                "date": "٢٠٢٤-٠٣-١٥",
                "time": "٠٩:٠٠",
                "type": "جلسة مرافعة",
                "judge": "القاضي أحمد",
                "days_left": 3
            },
            {
                "case_number": "٤٥٦/٢٠٢٤", 
                "court": "محكمة استئناف عمان",
                "date": "٢٠٢٤-٠٣-٢٠",
                "time": "١٠:٣٠",
                "type": "جلسة شهود",
                "judge": "القاضي محمد",
                "days_left": 8
            }
        ]
        
        for session in upcoming_sessions:
            with st.expander(f"📌 {session['case_number']} - {session['type']}", expanded=False):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**المحكمة:** {session['court']}")
                    st.write(f"**التاريخ:** {session['date']}")
                    st.write(f"**الوقت:** {session['time']}")
                with col2:
                    st.write(f"**القاضي:** {session['judge']}")
                    st.write(f"**الأيام المتبقية:** {session['days_left']}")
                    
                    if session['days_left'] <= 3:
                        st.warning("⏰ جلسة قريبة!")
                
                if st.button("📝 إضافة تذكير", key=f"reminder_{session['case_number']}"):
                    st.success("تم إضافة تذكير للجلسة")

def save_session_to_planner(session_data):
    """حفظ بيانات الجلسة"""
    if 'sessions' not in st.session_state:
        st.session_state.sessions = []
    
    st.session_state.sessions.append(session_data)

def show_defenses_assistant():
    """مساعد الدفوع الذكي"""
    st.markdown("#### ⚖️ مساعد الدفوع الذكي")
    
    with st.form("defenses_assistant_form"):
        case_type = st.selectbox("نوع القضية", [
            "تعاقدية", "تعويض", "عقارية", "تجارية", "أحوال شخصية", "عمل"
        ])
        
        case_stage = st.selectbox("مرحلة القضية", [
            "قبل الرفع", "بعد الرفع", "أثناء المحاكمة", "قرار الاستئناف", "قرار التمييز"
        ])
        
        facts_summary = st.text_area("ملخص وقائع القضية")
        plaintiff_claims = st.text_area("مطالبات المدعي")
        
        if st.form_submit_button("🛡️ اقتراح الدفوع المناسبة", use_container_width=True):
            defenses = suggest_legal_defenses(case_type, case_stage, facts_summary, plaintiff_claims)
            display_suggested_defenses(defenses)

def suggest_legal_defenses(case_type, stage, facts, claims):
    """اقتراح الدفوع القانونية المناسبة"""
    
    defenses_database = {
        "تعاقدية": [
            "انعدام الرضا",
            "عدم توفر شروط العقد",
            "استحالة التنفيذ",
            "التقادم المسقط",
            "الدفع بعدم التنفيذ"
        ],
        "تعويض": [
            "انتفاء الخطأ",
            "انتفاء العلاقة السببية", 
            "الضرر غير متحقق",
            "التقادم",
            "الدفع بالسبب الأجنبي"
        ],
        "عقارية": [
            "عدم الاختصاص المكاني",
            "انتفاء صفة المدعي",
            "التقادم الاكتسابي",
            "عدم صحة السند",
            "الدفع بعدم وجود حق"
        ]
    }
    
    # تحليل النص لاكتشاف الكلمات المفتاحية
    keywords = {
        "تقادم": ["التقادم المسقط", "التقادم الاكتسابي"],
        "اختصاص": ["عدم الاختصاص المكاني", "عدم الاختصاص النوعي"],
        "عقد": ["انعدام الرضا", "عدم توفر شروط العقد"],
        "خطأ": ["انتفاء الخطأ", "الدفع بالسبب الأجنبي"]
    }
    
    suggested_defenses = defenses_database.get(case_type, [])
    
    # إضافة دفوع بناء على الكلمات المفتاحية
    for keyword, related_defenses in keywords.items():
        if keyword in facts or keyword in claims:
            suggested_defenses.extend(related_defenses)
    
    # إزالة التكرارات
    suggested_defenses = list(set(suggested_defenses))
    
    return {
        'case_type': case_type,
        'stage': stage,
        'suggested_defenses': suggested_defenses[:8],  # الحد لـ 8 دفوع كحد أقصى
        'confidence_level': "عالية" if len(suggested_defenses) >= 3 else "متوسطة"
    }

def display_suggested_defenses(defenses):
    """عرض الدفوع المقترحة"""
    
    st.success(f"## 🛡️ الدفوع المقترحة للقضية ({defenses['case_type']})")
    
    st.info(f"**📊 مستوى الثقة:** {defenses['confidence_level']}")
    st.info(f"**⏰ المرحلة المناسبة:** {defenses['stage']}")
    
    st.markdown("##### 💡 الدفوع المقترحة:")
    
    for i, defense in enumerate(defenses['suggested_defenses'], 1):
        with st.expander(f"🛡️ الدفع {i}: {defense}", expanded=False):
            st.write(f"**التطبيق:** {get_defense_application(defense)}")
            st.write(f"**الشروط:** {get_defense_conditions(defense)}")
            
            if st.button("📝 إنشاء صياغة الدفع", key=f"draft_{defense}"):
                defense_draft = generate_defense_draft(defense)
                st.text_area("📄 مسودة الدفع", value=defense_draft, height=200)

def get_defense_application(defense):
    """الحصول على تطبيق الدفع"""
    applications = {
        "التقادم المسقط": "ينطبق عندما ينقضي الحق بمضي المدة القانونية دون المطالبة به",
        "انعدام الرضا": "ينطبق عندما يكون الرضا معيباً بالغلط أو التدليس أو الإكراه",
        "عدم الاختصاص المكاني": "ينطبق عندما ترفع الدعوى على محكمة غير مختصة مكانياً"
    }
    return applications.get(defense, "تطبيق عام وفق أحكام القانون")

def get_defense_conditions(defense):
    """الحصول على شروط الدفع"""
    conditions = {
        "التقادم المسقط": "مضي المدة القانونية المقررة للتقادم",
        "انعدام الرضا": "إثبات وجود عيب في الرضا (غلط، تدليس، إكراه)",
        "عدم الاختصاص المكاني": "إثبات أن المحكمة غير مختصة وفق قواعد الاختصاص المكاني"
    }
    return conditions.get(defense, "شروط عامة وفق أحكام القانون")

def generate_defense_draft(defense):
    """إنشاء مسودة الدفع"""
    return f"""
    دفع بـ: {defense}
    
    الأساس القانوني:
    - المادة المناسبة من القانون المدني/التجاري
    - المادة المناسبة من قانون أصول المحاكمات
    
    الأسباب:
    1. __________
    2. __________
    3. __________
    
    الطلبات:
    1. قبول الدفع شكلاً
    2. الحكم بعدم اختصاص المحكمة/رفض الدعوى
    3. تحميل المدعي المصاريف
    
    توقيع المحامي:
    ___________________
    """

def show_documents_checker():
    """مدقق المستندات المتقدم"""
    st.markdown("#### 🔍 مدقق المستندات المتقدم")
    
    tab1, tab2 = st.tabs(["📄 تدقيق المستندات", "✅ فحص الاكتمال"])
    
    with tab1:
        st.markdown("##### 📄 تدقيق المستندات القانونية")
        
        uploaded_file = st.file_uploader("رفع المستند للتدقيق", type=['pdf', 'docx', 'txt'])
        
        if uploaded_file is not None:
            document_analysis = analyze_document_content(uploaded_file)
            display_document_analysis(document_analysis)
    
    with tab2:
        st.markdown("##### ✅ فحص اكتمال المرفقات")
        
        document_types = st.multiselect("أنواع المستندات المطلوبة", [
            "عقد الاتفاق", "مستندات الملكية", "سندات الدين",
            "مستندات الإثبات", "تقارير الخبراء", "مستندات الهوية",
            "السجل التجاري", "الرخص والمؤهلات"
        ])
        
        if st.button("🔍 فحص الاكتمال", use_container_width=True):
            completeness_check = check_documents_completeness(document_types)
            display_completeness_report(completeness_check)

def analyze_document_content(file):
    """تحليل محتوى المستند"""
    # محاكاة تحليل المستند
    return {
        'file_name': file.name,
        'file_size': f"{len(file.getvalue()) / 1024:.1f} KB",
        'issues_found': [
            "توقيع غير واضح",
            "تاريخ مستند قديم",
            "بعض البنود تحتاج توضيح"
        ],
        'suggestions': [
            "توثيق التوقيع من جهة مختصة",
            "تحديث تاريخ المستند",
            "مراجعة البنود الغامضة"
        ],
        'risk_level': "منخفض",
        'compliance_score': 85
    }

def display_document_analysis(analysis):
    """عرض تحليل المستند"""
    
    st.success(f"## 🔍 نتائج تدقيق المستند: {analysis['file_name']}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"**حجم الملف:** {analysis['file_size']}")
        st.info(f"**مستوى المخاطر:** {analysis['risk_level']}")
        
    with col2:
        st.info(f"**درجة المطابقة:** {analysis['compliance_score']}%")
    
    if analysis['issues_found']:
        st.markdown("##### ⚠️ المشاكل المكتشفة:")
        for issue in analysis['issues_found']:
            st.write(f"• {issue}")
    
    if analysis['suggestions']:
        st.markdown("##### 💡 التوصيات:")
        for suggestion in analysis['suggestions']:
            st.write(f"• {suggestion}")

def check_documents_completeness(document_types):
    """فحص اكتمال المستندات"""
    return {
        'required_documents': document_types,
        'missing_documents': ["سندات الدين", "تقارير الخبراء"] if len(document_types) > 3 else [],
        'completeness_percentage': 75 if len(document_types) > 3 else 90,
        'recommendations': [
            "توفير المستندات المفقورة لإكمال الملف",
            "التحقق من صحة جميع التواقيع",
            "تحديث التواريخ إن لزم الأمر"
        ]
    }

def display_completeness_report(check):
    """عرض تقرير الاكتمال"""
    
    st.success(f"## ✅ تقرير الاكتمال: {check['completeness_percentage']}%")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"**المستندات المطلوبة:** {len(check['required_documents'])}")
        st.info(f"**نسبة الاكتمال:** {check['completeness_percentage']}%")
        
    with col2:
        if check['missing_documents']:
            st.error(f"**المستندات الناقصة:** {len(check['missing_documents'])}")
        else:
            st.success("**جميع المستندات مكتملة**")
    
    if check['missing_documents']:
        st.markdown("##### 📋 المستندات الناقصة:")
        for doc in check['missing_documents']:
            st.write(f"• {doc}")
    
    if check['recommendations']:
        st.markdown("##### 💡 التوصيات:")
        for rec in check['recommendations']:
            st.write(f"• {rec}")

def show_compensation_estimator():
    """مقدر التعويضات المتقدم"""
    st.markdown("#### 💰 مقدر التعويضات المتقدم")
    
    with st.form("compensation_estimator_form"):
        st.markdown("##### 📋 معلومات الأساس")
        
        col1, col2 = st.columns(2)
        
        with col1:
            damage_type = st.selectbox("نوع الضرر", [
                "مادي مباشر", "مادي غير مباشر", "أدبي", "مركب"
            ])
            incident_date = st.date_input("تاريخ الحادث")
            base_amount = st.number_input("المبلغ الأساسي (دينار)", min_value=0, value=10000)
            
        with col2:
            severity = st.select_slider("شدة الضرر", options=["بسيط", "متوسط", "شديد", "بالغ"])
            duration = st.number_input("مدة التأثير (أشهر)", min_value=1, value=12)
            has_medical_report = st.checkbox("هل يوجد تقرير طبي؟")
        
        st.markdown("##### 📊 تفاصيل إضافية")
        
        col1, col2 = st.columns(2)
        
        with col1:
            lost_income = st.number_input("الدخل المفقود (دينار)", min_value=0, value=5000)
            medical_costs = st.number_input("التكاليف الطبية (دينار)", min_value=0, value=3000)
            
        with col2:
            other_costs = st.number_input("مصاريف أخرى (دينار)", min_value=0, value=1000)
            future_impact = st.slider("التأثير المستقبلي %", 0, 100, 20)
        
        if st.form_submit_button("💰 تقدير التعويض", use_container_width=True):
            compensation_estimate = calculate_compensation(
                damage_type, base_amount, severity, duration, 
                has_medical_report, lost_income, medical_costs, 
                other_costs, future_impact
            )
            display_compensation_estimate(compensation_estimate)

def calculate_compensation(damage_type, base_amount, severity, duration, 
                          has_medical_report, lost_income, medical_costs, 
                          other_costs, future_impact):
    """حساب تقدير التعويض"""
    
    # عوامل التعديل
    severity_factors = {
        "بسيط": 0.5,
        "متوسط": 1.0,
        "شديد": 2.0,
        "بالغ": 3.0
    }
    
    type_factors = {
        "مادي مباشر": 1.0,
        "مادي غير مباشر": 0.8,
        "أدبي": 1.5,
        "مركب": 2.0
    }
    
    severity_factor = severity_factors.get(severity, 1.0)
    type_factor = type_factors.get(damage_type, 1.0)
    
    # حساب التعويض الأساسي
    base_compensation = base_amount * severity_factor * type_factor
    
    # إضافة التكاليف
    total_costs = lost_income + medical_costs + other_costs
    
    # إضافة التأثير المستقبلي
    future_compensation = base_compensation * (future_impact / 100)
    
    # تعديل حسب التقارير الطبية
    if has_medical_report:
        medical_bonus = medical_costs * 0.2
    else:
        medical_bonus = 0
    
    total_compensation = base_compensation + total_costs + future_compensation + medical_bonus
    
    return {
        'base_compensation': base_compensation,
        'total_costs': total_costs,
        'future_compensation': future_compensation,
        'medical_bonus': medical_bonus,
        'total_compensation': total_compensation,
        'damage_type': damage_type,
        'severity': severity,
        'confidence_level': "عالية" if has_medical_report else "متوسطة"
    }

def display_compensation_estimate(estimate):
    """عرض تقدير التعويض"""
    
    st.success(f"## 💰 التقدير النهائي: {estimate['total_compensation']:,.0f} دينار")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("التعويض الأساسي", f"{estimate['base_compensation']:,.0f} دينار")
        st.metric("التكاليف المباشرة", f"{estimate['total_costs']:,.0f} دينار")
        
    with col2:
        st.metric("التعويض المستقبلي", f"{estimate['future_compensation']:,.0f} دينار")
        st.metric("مستوى الثقة", estimate['confidence_level'])
        
    with col3:
        st.metric("نوع الضرر", estimate['damage_type'])
        st.metric("شدة الضرر", estimate['severity'])
    
    # توصيات
    st.markdown("##### 💡 توصيات لزيادة التعويض:")
    recommendations = [
        "تقديم تقارير طبية مفصلة",
        "إثبات العلاقة السببية بوضوح",
        "توثيق جميع التكاليف",
        "الاستعانة بخبراء متخصصين"
    ]
    
    for rec in recommendations:
        st.write(f"• {rec}")

def show_deadline_alerts():
    """منبه المواعيد الذكي"""
    st.markdown("#### ⏰ منبه المواعيد الذكي")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("##### 🎯 إضافة منبه جديد")
        with st.form("deadline_alert_form"):
            alert_title = st.text_input("عنوان المنبه *")
            deadline_date = st.date_input("تاريخ الانتهاء *")
            deadline_time = st.time_input("وقت الانتهاء")
            priority = st.select_slider("الأولوية", options=["منخفضة", "متوسطة", "عالية", "حرجة"])
            alert_type = st.selectbox("نوع المنبه", [
                "موعد قضائي", "موعد تقديم", "موعد استئناف", 
                "موعد تبليغ", "موعد جلسة", "آخر"
            ])
            description = st.text_area("وصف المنبه")
            
            if st.form_submit_button("🔔 إضافة المنبه", use_container_width=True):
                if alert_title and deadline_date:
                    add_deadline_alert({
                        'title': alert_title,
                        'date': deadline_date,
                        'time': deadline_time,
                        'priority': priority,
                        'type': alert_type,
                        'description': description
                    })
                    st.success("✅ تم إضافة المنبه بنجاح!")
                else:
                    st.error("❌ يرجى ملء الحقول الإلزامية (*)")
    
    with col2:
        st.markdown("##### 📋 المنبهات النشطة")
        
        # محاكاة بيانات المنبهات
        active_alerts = [
            {
                "title": "تقديم لائحة جوابية - قضية ١٢٣",
                "date": "٢٠٢٤-٠٣-١٠",
                "priority": "حرجة",
                "days_left": 2,
                "type": "موعد تقديم"
            },
            {
                "title": "جلسة استماع - قضية ٤٥٦", 
                "date": "٢٠٢٤-٠٣-١٥",
                "priority": "عالية",
                "days_left": 7,
                "type": "موعد جلسة"
            },
            {
                "title": "استئناف حكم - قضية ٧٨٩",
                "date": "٢٠٢٤-٠٣-٢٥",
                "priority": "عالية", 
                "days_left": 17,
                "type": "موعد استئناف"
            }
        ]
        
        for alert in active_alerts:
            alert_color = "🔴" if alert['priority'] == "حرجة" else "🟡" if alert['priority'] == "عالية" else "🟢"
            
            with st.expander(f"{alert_color} {alert['title']}", expanded=alert['priority'] in ["حرجة", "عالية"]):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**النوع:** {alert['type']}")
                    st.write(f"**التاريخ:** {alert['date']}")
                with col2:
                    st.write(f"**الأولوية:** {alert['priority']}")
                    st.write(f"**الأيام المتبقية:** {alert['days_left']}")
                
                if alert['days_left'] <= 3:
                    st.error("⏰ موعد قريب! يرجى الإسراع في الإجراء")
                elif alert['days_left'] <= 7:
                    st.warning("⚠️ موعد يقترب! يوصى بالمتابعة")

def add_deadline_alert(alert_data):
    """إضافة منبه جديد"""
    if 'deadline_alerts' not in st.session_state:
        st.session_state.deadline_alerts = []
    
    st.session_state.deadline_alerts.append(alert_data)

def show_precedents_analyzer():
    """محلل السوابق القضائية"""
    st.markdown("#### 📈 محلل السوابق القضائية")
    
    tab1, tab2 = st.tabs(["🔍 بحث السوابق", "📊 تحليل الاتجاهات"])
    
    with tab1:
        st.markdown("##### 🔍 البحث في السوابق القضائية")
        
        with st.form("precedents_search_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                search_keywords = st.text_input("الكلمات المفتاحية للبحث")
                legal_issue = st.selectbox("المسألة القانونية", [
                    "التقادم", "الاختصاص", "الإثبات", "التعويض",
                    "فسخ العقد", "الدفوع", "التبليغ", "الطعون"
                ])
                
            with col2:
                court_level = st.selectbox("مستوى المحكمة", [
                    "جميع المحاكم", "محكمة التمييز", "محاكم الاستئناف", "محاكم البداية"
                ])
                time_period = st.selectbox("الفترة الزمنية", [
                    "جميع الفترات", "آخر سنة", "آخر ٣ سنوات", "آخر ٥ سنوات"
                ])
            
            if st.form_submit_button("🔍 بحث في السوابق", use_container_width=True):
                search_results = search_legal_precedents(
                    search_keywords, legal_issue, court_level, time_period
                )
                display_precedents_search_results(search_results)
    
    with tab2:
        st.markdown("##### 📊 تحليل اتجاهات الأحكام")
        analyze_legal_trends()

def search_legal_precedents(keywords, issue, court, period):
    """البحث في السوابق القضائية"""
    # محاكاة نتائج البحث
    precedents = [
        {
            "case_number": "تمييز مدني ١٢٣/٢٠٢٣",
            "court": "محكمة التمييز",
            "date": "٢٠٢٣-٠٦-١٥",
            "issue": "التقادم المسقط",
            "summary": "حكم بتطبيق التقادم المسقط في الدعوى العقارية",
            "key_points": [
                "مضي المدة القانونية للتقادم",
                "انعدام أي سبب لقطع التقادم",
                "تطبيق المادة ٤٢٨ من القانون المدني"
            ]
        },
        {
            "case_number": "استئناف عمان ٤٥٦/٢٠٢٢", 
            "court": "محكمة الاستئناف",
            "date": "٢٠٢٢-١١-٢٠",
            "issue": "الإثبات بالبينة",
            "summary": "قبول الإثبات بالبينة في عدم وجود مستند كتابي",
            "key_points": [
                "جواز الإثبات بالبينة في المعاملات التجارية",
                "توافر شروط قبول البينة",
                "تطبيق المادة ٧٦ من قانون البينات"
            ]
        }
    ]
    
    return {
        'keywords': keywords,
        'issue': issue,
        'court': court,
        'period': period,
        'results': precedents,
        'total_found': len(precedents)
    }

def display_precedents_search_results(results):
    """عرض نتائج البحث في السوابق"""
    
    st.success(f"## 🔍 نتائج البحث: {results['total_found']} سابقة قضائية")
    
    for precedent in results['results']:
        with st.expander(f"📌 {precedent['case_number']} - {precedent['issue']}", expanded=False):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**المحكمة:** {precedent['court']}")
                st.write(f"**التاريخ:** {precedent['date']}")
            with col2:
                st.write(f"**المسألة:** {precedent['issue']}")
            
            st.write(f"**الملخص:** {precedent['summary']}")
            
            st.markdown("**النقاط الرئيسية:**")
            for point in precedent['key_points']:
                st.write(f"• {point}")
            
            if st.button("📝 استخدام السابقة", key=f"use_{precedent['case_number']}"):
                st.success("تم نسخ معلومات السابقة للاستخدام")

def analyze_legal_trends():
    """تحليل الاتجاهات في الأحكام"""
    
    st.markdown("##### 📈 اتجاهات الأحكام في المسائل القانونية")
    
    # بيانات افتراضية للاتجاهات
    trends_data = {
        "المسألة القانونية": ["التقادم", "الإثبات", "التعويض", "الاختصاص"],
        "عدد الأحكام (٢٠٢٢)": [45, 78, 120, 35],
        "عدد الأحكام (٢٠٢٣)": [52, 85, 135, 42],
        "التغيير %": ["+١٥٪", "+٩٪", "+١٢٪", "+٢٠٪"]
    }
    
    trends_df = pd.DataFrame(trends_data)
    st.dataframe(trends_df, use_container_width=True, hide_index=True)
    
    st.info("""
    **ملاحظات التحليل:**
    - زيادة ملحوظة في قضايا التعويض
    - ارتفاع طفيف في قضايا الإثبات
    - زيادة كبيرة في منازعات الاختصاص
    """)

# ==========================
# 🔧 نظام التشغيل الرئيسي
# ==========================
def main():
    """الدالة الرئيسية للتطبيق"""
    try:
        # تهيئة حالة الجلسة
        initialize_session_state()
        
        # عرض القائمة الجانبية
        show_sidebar_navigation()
        
        # نظام التوجيه للصفحات الموسعة
        page_handlers = {
            "home": show_home_page,
            "notifications_procedures": show_notifications_procedures_section,
            "judicial_jurisdiction": show_judicial_jurisdiction_section,
            "financial_evaluation": show_financial_evaluation_section,
            "filing_cases": show_filing_cases_section,
            "trial_procedures": show_trial_procedures_section,
            "investigation_verification": show_investigation_verification_section,
            "extended_requests_defenses": show_extended_requests_defenses_section,
            "preventive_procedures": show_preventive_procedures_section,
            "judgments_appeals": show_judgments_appeals_section,
            "lawyer_tools": show_lawyer_tools_section
        }
        
        # الحصول على المعالج المناسب للصفحة
        current_page = st.session_state.selected_page
        page_handler = page_handlers.get(current_page, show_home_page)
        
        # تنفيذ الصفحة المطلوبة
        page_handler()
        
        # تذييل الصفحة
        st.markdown("---")
        st.markdown(f"""
        <div style="text-align: center; color: #6B7280; font-size: 0.9rem;">
            <p>⚖️ {config["APP_INFO"]["APP_NAME"]} | {config["APP_INFO"]["VERSION"]} | © 2025 جميع الحقوق محفوظة</p>
          
        """, unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"""
        ## ⚠️ حدث خطأ غير متوقع
        
        نعتذر عن هذا الخطأ. يرجى:
        1. تحديث الصفحة
        2. التأكد من اتصال الإنترنت  
        3. التواصل مع الدعم إذا استمرت المشكلة
        
        تفاصيل الخطأ: {str(e)}
        """)
        
        if st.button("🔄 تحديث الصفحة"):
            st.rerun()

if __name__ == "__main__":
    main()