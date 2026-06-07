import re
from modules.llm_enhancer import ask_llm
from modules.prompts import recommendation_prompt

# business advice based on topic and sentiment
delivery_positive = [
    "Keep up the fast delivery, customers are happy with it.",
    "Use quick delivery as a selling point in your marketing.",
    "Offer priority shipping rewards for loyal customers.",
]

delivery_negative = [
    "Improve the delivery process to reduce delays.",
    "Work with more than one courier to avoid dependency issues.",
    "Send customers tracking updates so they are not left waiting.",
]

delivery_mixed = [
    "Delivery is sometimes good and sometimes bad, make it more consistent.",
    "Find out where delays are happening and fix those specific areas.",
]

delivery_neutral = [
    "Review your delivery timelines and compare with industry standards.",
]

support_positive = [
    "Your support team is doing well, keep training them the same way.",
    "Share positive support stories as customer testimonials.",
    "Add a feedback form after support tickets are closed.",
]

support_negative = [
    "Reduce response time, customers are waiting too long for replies.",
    "Add more support staff during busy hours.",
    "Create an FAQ page so customers can solve simple issues themselves.",
]

support_mixed = [
    "Support quality is not consistent, set clear response time rules.",
    "Retrain agents who are getting the most complaints.",
]

support_neutral = [
    "Start collecting customer satisfaction scores for your support team.",
]

product_positive = [
    "Customers love the product, highlight the best features in ads.",
    "Use good reviews as proof in your marketing campaigns.",
    "Think about launching a premium version of this product.",
]

product_negative = [
    "Find the root cause of defects and fix them in the next update.",
    "Do more quality checks before shipping products.",
    "Offer a warranty or easy replacement to rebuild customer trust.",
]

product_mixed = [
    "Some features are liked and some are not, check feedback for each one separately.",
    "Test changes on a small group before rolling out to everyone.",
]

product_neutral = [
    "Set up a system to regularly collect feedback about the product.",
]

pricing_positive = [
    "Customers think the price is fair, keep it consistent.",
    "Try a small price increase on top products to improve profit.",
]

pricing_negative = [
    "Your prices may be too high compared to competitors, review them.",
    "Offer a cheaper plan or bundle for budget customers.",
    "Make sure customers understand what they are paying for.",
]

pricing_mixed = [
    "Some customers are okay with the price and some are not, consider flexible pricing.",
]

pricing_neutral = [
    "Do a pricing comparison with your competitors and adjust if needed.",
]

app_positive = [
    "App is working well, keep updating it regularly.",
    "Mention how easy the app is to use in your onboarding.",
]

app_negative = [
    "Fix the bugs and crashes that customers are reporting.",
    "Make the app load faster, aim for under 2 seconds.",
    "Add a tutorial or guide for new users who are confused.",
]

app_mixed = [
    "Main features work but there are some bugs, focus on fixing edge cases.",
]

app_neutral = [
    "Run a short survey inside the app to understand what users want improved.",
]

general_positive = [
    "Continue the strategies contributing to strong business performance.",
    "Identify successful practices and expand them across the organization.",
    "Use current strengths as a foundation for future growth."
]

general_negative = [
    "Identify the main causes of underperformance and address them systematically.",
    "Develop an improvement plan with measurable goals and timelines.",
    "Monitor key business metrics regularly and take corrective actions early."
]

general_mixed = [
    "Build on successful areas while addressing weaker performance segments.",
    "Analyze performance trends to identify improvement opportunities.",
    "Focus on creating more consistent results across the organization."
]

general_neutral = [
    "Review performance data regularly to identify opportunities for improvement.",
    "Establish clear metrics and monitor progress over time."
]

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def find_topic(text, keywords):
    all_words = set(clean_text(text).split())

    if keywords:
        for k in keywords:
            all_words.add(str(k).lower())

    delivery_words = ["delivery", "shipping", "courier", "package", "delay", "delayed", "late", "tracking", "dispatch", "logistics", "arrived"]
    support_words  = ["support", "response", "reply", "help", "agent", "ticket", "helpdesk", "staff", "resolved", "resolution", "chat"]
    product_words  = ["product", "quality", "battery", "camera", "screen", "build", "hardware", "software", "defect", "feature", "performance", "design", "version"]
    pricing_words  = ["price", "pricing", "expensive", "cheap", "overpriced", "affordable", "value", "money", "discount", "deal", "refund", "cost"]
    app_words      = ["app", "application", "website", "platform", "login", "bug", "bugs", "crash", "crashes", "slow", "load", "error", "lag", "install", "update", "ui", "ux"]
   
    scores = {
        "delivery": sum(1 for w in delivery_words if w in all_words),
        "support":  sum(1 for w in support_words  if w in all_words),
        "product":  sum(1 for w in product_words  if w in all_words),
        "pricing":  sum(1 for w in pricing_words  if w in all_words),
        "app":      sum(1 for w in app_words       if w in all_words)
    }
    
        
    best = max(scores, key=scores.get)

    if scores[best] == 0:
        
        return "general"

    return best


def get_recommendations(text, sentiment="neutral", keywords=None):

    if not text or not str(text).strip():
        return []

    if keywords is None:
        keywords = []

    keywords = [k for k in keywords if k != "No keywords found"]

    topic = find_topic(text, keywords)
    sentiment = (sentiment or "neutral").lower()

    # pick the right advice list based on topic and sentiment
    if topic == "delivery":
        if sentiment == "positive":
            advice = delivery_positive
        elif sentiment == "negative":
            advice = delivery_negative
        elif sentiment == "mixed":
            advice = delivery_mixed
        else:
            advice = delivery_neutral

    elif topic == "support":
        if sentiment == "positive":
            advice = support_positive
        elif sentiment == "negative":
            advice = support_negative
        elif sentiment == "mixed":
            advice = support_mixed
        else:
            advice = support_neutral

    elif topic == "product":
        if sentiment == "positive":
            advice = product_positive
        elif sentiment == "negative":
            advice = product_negative
        elif sentiment == "mixed":
            advice = product_mixed
        else:
            advice = product_neutral

    elif topic == "pricing":
        if sentiment == "positive":
            advice = pricing_positive
        elif sentiment == "negative":
            advice = pricing_negative
        elif sentiment == "mixed":
            advice = pricing_mixed
        else:
            advice = pricing_neutral

    elif topic == "app":
        if sentiment == "positive":
            advice = app_positive
        elif sentiment == "negative":
            advice = app_negative
        elif sentiment == "mixed":
            advice = app_mixed
        else:
            advice = app_neutral

    else:
        if sentiment == "positive":
            advice = general_positive
        elif sentiment == "negative":
            advice = general_negative
        elif sentiment == "mixed":
            advice = general_mixed
        else:
            advice = general_neutral

    return advice[:3]

def smart_recommendations(
        text,
        sentiment="neutral",
        keywords=None
):

    if text is None or not str(text).strip():
        return []
    
    # Rule-based fallback
    basic_recommendations = get_recommendations(
        text=text,
        sentiment=sentiment,
        keywords=keywords
    )

    basic_text = "\n".join(
        f"- {r}"
        for r in basic_recommendations
    )

    prompt = recommendation_prompt(text,sentiment,
                                   keywords,basic_text)
    try:

        llm_result = ask_llm(prompt)

        if llm_result:

            recommendations = [
                line.strip("-• ").strip()
                for line in llm_result.split("\n")
                if line.strip()
            ]

            if recommendations:
                return recommendations[:3]
        
    except Exception:
        pass

    return basic_recommendations
