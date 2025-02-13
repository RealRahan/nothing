from flask import Flask, render_template, request
import requests
import json
import datetime

app = Flask(__name__)

def fetch_tiktok_data(username):
    url = f"https://www.tiktok.com/@{username}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        start_tag = '<script id="__UNIVERSAL_DATA_FOR_REHYDRATION__" type="application/json">'
        end_tag = '</script>'
        start_index = response.text.find(start_tag) + len(start_tag)
        end_index = response.text.find(end_tag, start_index)
        json_data = response.text[start_index:end_index]

        data = json.loads(json_data)
        return data
    except (requests.exceptions.RequestException, json.JSONDecodeError, TypeError) as e:
        print(f"Error fetching/parsing: {e}")
        return None

country_arabic_names_with_emojis = {
    "AF": "أفغانستان 🇦🇫",
    "AL": "ألبانيا 🇦🇱",
    "DZ": "الجزائر 🇩🇿",
    "AS": "ساموا الأمريكية 🇦🇸",
    "AD": "أندورا 🇦🇩",
    "AO": "أنغولا 🇦🇴",
    "AI": "أنغيلا 🇦🇮",
    "AQ": "أنتاركتيكا 🇦🇶",
    "AG": "أنتيغوا وبربودا 🇦🇬",
    "AR": "الأرجنتين 🇦🇷",
    "AM": "أرمينيا 🇦🇲",
    "AU": "أستراليا 🇦🇺",
    "AT": "النمسا 🇦🇹",
    "AZ": "أذربيجان 🇦🇿",
    "BS": "جزر البهاما 🇧🇸",
    "BH": "البحرين 🇧🇭",
    "BD": "بنغلاديش 🇧🇩",
    "BB": "بربادوس 🇧🇧",
    "BY": "بيلاروسيا 🇧🇾",
    "BE": "بلجيكا 🇧🇪",
    "BZ": "بليز 🇧🇿",
    "BJ": "بنين 🇧🇯",
    "BM": "برمودا 🇧🇲",
    "BT": "بوتان 🇧🇹",
    "BO": "بوليفيا 🇧🇴",
    "BA": "البوسنة والهرسك 🇧🇦",
    "BW": "بوتسوانا 🇧🇼",
    "BR": "البرازيل 🇧🇷",
    "VG": "جزر العذراء البريطانية 🇻🇬",
    "IO": "إقليم المحيط الهندي البريطاني 🇮🇴",
    "BN": "بروناي 🇧🇳",
    "BG": "بلغاريا 🇧🇬",
    "BF": "بوركينا فاسو 🇧🇫",
    "BI": "بوروندي 🇧🇮",
    "CV": "كابو فيردي 🇨🇻",
    "KH": "كمبوديا 🇰🇭",
    "CM": "الكاميرون 🇨🇲",
    "CA": "كندا 🇨🇦",
    "KY": "جزر كايمان 🇰🇾",
    "CF": "جمهورية أفريقيا الوسطى 🇨🇫",
    "TD": "تشاد 🇹🇩",
    "CL": "تشيلي 🇨🇱",
    "CN": "الصين 🇨🇳",
    "CX": "جزيرة عيد الميلاد 🇨🇽",
    "CC": "جزر كوكوس (كيلينغ) 🇨🇨",
    "CO": "كولومبيا 🇨🇴",
    "KM": "جزر القمر 🇰🇲",
    "CG": "الكونغو 🇨🇬",
    "CD": "جمهورية الكونغو الديمقراطية 🇨🇩",
    "CK": "جزر كوك 🇨🇰",
    "CR": "كوستاريكا 🇨🇷",
    "CI": "ساحل العاج 🇨🇮",
    "HR": "كرواتيا 🇭🇷",
    "CU": "كوبا 🇨🇺",
    "CW": "كوراساو 🇨🇼",
    "CY": "قبرص 🇨🇾",
    "CZ": "التشيك 🇨🇿",
    "DK": "الدنمارك 🇩🇰",
    "DJ": "جيبوتي 🇩🇯",
    "DM": "دومينيكا 🇩🇲",
    "DO": "جمهورية الدومينيكان 🇩🇴",
    "EC": "الإكوادور 🇪🇨",
    "EG": "مصر 🇪🇬",
    "SV": "السلفادور 🇸🇻",
    "GQ": "غينيا الاستوائية 🇬🇶",
    "ER": "إريتريا 🇪🇷",
    "EE": "إستونيا 🇪🇪",
    "SZ": "إسواتيني 🇸🇿",
    "ET": "إثيوبيا 🇪🇹",
    "FK": "جزر فوكلاند 🇫🇰",
    "FO": "جزر فارو 🇫🇴",
    "FJ": "فيجي 🇫🇯",
    "FI": "فنلندا 🇫🇮",
    "FR": "فرنسا 🇫🇷",
    "GF": "غيانا الفرنسية 🇬🇫",
    "PF": "بولينيزيا الفرنسية 🇵🇫",
    "GA": "الغابون 🇬🇦",
    "GM": "غامبيا 🇬🇲",
    "GE": "جورجيا 🇬🇪",
    "DE": "ألمانيا 🇩🇪",
    "GH": "غانا 🇬🇭",
    "GI": "جبل طارق 🇬🇮",
    "GR": "اليونان 🇬🇷",
    "GL": "جرينلاند 🇬🇱",
    "GD": "غرينادا 🇬🇩",
    "GP": "جوادلوب 🇬🇵",
    "GU": "غوام 🇬🇺",
    "GT": "غواتيمالا 🇬🇹",
    "GG": "غيرنسي 🇬🇬",
    "GN": "غينيا 🇬🇳",
    "GW": "غينيا بيساو 🇬🇼",
    "GY": "غيانا 🇬🇾",
    "HT": "هايتي 🇭🇹",
    "HN": "هندوراس 🇭🇳",
    "HK": "هونغ كونغ 🇭🇰",
    "HU": "هنغاريا 🇭🇺",
    "IS": "آيسلندا 🇮🇸",
    "IN": "الهند 🇮🇳",
    "ID": "إندونيسيا 🇮🇩",
    "IR": "إيران 🇮🇷",
    "IQ": "العراق 🇮🇶",
    "IE": "أيرلندا 🇮🇪",
    "IM": "جزيرة مان 🇮🇲",
    "IL": "إسرائيل 🇮🇱",
    "IT": "إيطاليا 🇮🇹",
    "JM": "جامايكا 🇯🇲",
    "JP": "اليابان 🇯🇵",
    "JE": "جيرسي 🇯🇪",
    "JO": "الأردن 🇯🇴",
    "KZ": "كازاخستان 🇰🇿",
    "KE": "كينيا 🇰🇪",
    "KI": "كيريباتي 🇰🇮",
    "KP": "كوريا الشمالية 🇰🇵",
    "KR": "كوريا الجنوبية 🇰🇷",
    "KW": "الكويت 🇰🇼",
    "KG": "قيرغيزستان 🇰🇬",
    "LA": "لاوس 🇱🇦",
    "LV": "لاتفيا 🇱🇻",
    "LB": "لبنان 🇱🇧",
    "LS": "ليسوتو 🇱🇸",
    "LR": "ليبيريا 🇱🇷",
    "LY": "ليبيا 🇱🇾",
    "LI": "ليختنشتاين 🇱🇮",
    "LT": "ليتوانيا 🇱🇹",
    "LU": "لوكسمبورغ 🇱🇺",
    "MO": "ماكاو 🇲🇴",
    "MG": "مدغشقر 🇲🇬",
    "MW": "مالاوي 🇲🇼",
    "MY": "ماليزيا 🇲🇾",
    "MV": "جزر المالديف 🇲🇻",
    "ML": "مالطا 🇲🇱",
    "MH": "جزر مارشال 🇲🇭",
    "MQ": "مارتينيك 🇲🇶",
    "MR": "موريتانيا 🇲🇷",
    "MU": "موريشيوس 🇲🇺",
    "MX": "المكسيك 🇲🇽",
    "FM": "ولايات ميكرونيزيا المتحدة 🇫🇲",
    "MD": "مولدوفا 🇲🇩",
    "MC": "موناكو 🇲🇨",
    "MN": "منغوليا 🇲🇳",
    "ME": "الجبل الأسود 🇲🇪",
    "MS": "مونتسيرات 🇲🇸",
    "MA": "المغرب 🇲🇦",
    "MZ": "موزمبيق 🇲🇿",
    "MM": "ميانمار 🇲🇲",
    "NA": "ناميبيا 🇳🇦",
    "NR": "ناورو 🇳🇷",
    "NP": "نيبال 🇳🇵",
    "NL": "هولندا 🇳🇱",
    "NC": "كاليدونيا الجديدة 🇳🇨",
    "NZ": "نيوزيلندا 🇳🇿",
    "NI": "نيكاراغوا 🇳🇮",
    "NE": "النيجر 🇳🇪",
    "NG": "نيجيريا 🇳🇬",
    "NU": "نيوي 🇳🇺",
    "NF": "جزيرة نورفولك 🇳🇫",
    "MP": "جزر ماريانا الشمالية 🇲🇵",
    "NO": "النرويج 🇳🇴",
    "OM": "عمان 🇴🇲",
    "PK": "باكستان 🇵🇰",
    "PW": "بالاو 🇵🇼",
    "PS": "فلسطين 🇵🇸",
    "PA": "بنما 🇵🇦",
    "PG": "بابوا غينيا الجديدة 🇵🇬",
    "PY": "باراغواي 🇵🇾",
    "PE": "بيرو 🇵🇪",
    "PH": "الفلبين 🇵🇭",
    "PN": "جزر بيتكيرن 🇵🇳",
    "PL": "بولندا 🇵🇱",
    "PT": "البرتغال 🇵🇹",
    "PR": "بورتوريكو 🇵🇷",
    "QA": "قطر 🇶🇦",
    "RE": "Réunion 🇷🇪",
    "RO": "رومانيا 🇷🇴",
    "RU": "روسيا 🇷🇺",
    "RW": "رواندا 🇷🇼",
    "BL": "سانت بارتيليمي 🇧🇱",
    "SH": "سانت هيلينا 🇸🇭",
    "KN": "سانت كيتس ونيفيس 🇰🇳",
    "LC": "سانت لوسيا 🇱🇨",
    "MF": "سانت مارتن 🇲🇫",
    "PM": "سانت بيير وميكلون 🇵🇲",
    "VC": "سانت فنسنت وجزر غرينادين 🇻🇨",
    "WS": "ساموا 🇼🇸",
    "SM": "سان مارينو 🇸🇲",
    "ST": "ساو تومي وبرينسيبي 🇸🇹",
    "SA": "المملكة العربية السعودية 🇸🇦",
    "SN": "السنغال 🇸🇳",
    "RS": "صربيا 🇷🇸",
    "SC": "سيشيل 🇸🇨",
    "SL": "سيراليون 🇸🇱",
    "SG": "سنغافورة 🇸🇬",
    "SX": "سينت مارتن 🇸🇽",
    "SK": "سلوفاكيا 🇸🇰",
    "SI": "سلوفينيا 🇸🇮",
    "SB": "جزر سليمان 🇸🇧",
    "SO": "الصومال 🇸🇴",
    "ZA": "جنوب أفريقيا 🇿🇦",
    "SS": "جنوب السودان 🇸🇸",
    "ES": "إسبانيا 🇪🇸",
    "LK": "سريلانكا 🇱🇰",
    "SD": "السودان 🇸🇩",
    "SR": "سورينام 🇸🇷",
    "SE": "السويد 🇸🇪",
    "CH": "سويسرا 🇨🇭",
    "SY": "سوريا 🇸🇾",
    "TW": "تايوان 🇹🇼",
    "TJ": "طاجيكستان 🇹🇯",
    "TZ": "تنزانيا 🇹🇿",
    "TH": "تايلاند 🇹🇭",
    "TL": "تيمور الشرقية 🇹🇱",
    "TG": "توغو 🇹🇬",
    "TK": "توكيلاو 🇹🇰",
    "TO": "تونغا 🇹🇴",
    "TT": "ترينيداد وتوباغو 🇹🇹",
    "TN": "تونس 🇹🇳",
    "TR": "تركيا 🇹🇷",
    "TM": "تركمانستان 🇹🇲",
    "TC": "جزر تركس وكايكوس 🇹🇨",
    "TV": "توفالو 🇹🇻",
    "UG": "أوغندا 🇺🇬",
    "UA": "أوكرانيا 🇺🇦",
    "AE": "الإمارات العربية المتحدة 🇦🇪",
    "GB": "المملكة المتحدة 🇬🇧",
    "US": "الولايات المتحدة 🇺🇸",
    "UY": "أوروغواي 🇺🇾",
    "UZ": "أوزبكستان 🇺🇿",
    "VU": "فانواتو 🇻🇺",
    "VA": "مدينة الفاتيكان 🇻🇦",
    "VE": "فنزويلا 🇻🇪",
    "VN": "فيتنام 🇻🇳",
    "VI": "جزر العذراء الأمريكية 🇻🇮",
    "WF": "واليس وفوتونا 🇼🇫",
    "EH": "الصحراء الغربية 🇪🇭",
    "YE": "اليمن 🇾🇪",
    "ZM": "زامبيا 🇿🇲",
    "ZW": "زيمبابوي 🇿🇼"
}

def get_country_info(country_code):
    country_name_with_emoji = country_arabic_names_with_emojis.get(country_code)
    if country_name_with_emoji:
        return {"name": country_name_with_emoji}
    else:
        return {"name": "غير معروف"}


def process_tiktok_data(data):
    try:
        user_info = data["__DEFAULT_SCOPE__"]["webapp.user-detail"]["userInfo"]
        output_text = ""

        pfp_url = user_info['user']['avatarLarger']
        pfp_filename = f"{user_info['user']['uniqueId']}_profile_pic.jpg"

        output_text += f'<div style="text-align: center;"><img src="{pfp_url}" alt="Profile Picture" style="max-width: 200px; max-height: 200px;"></div><br>'

        create_time_seconds = user_info['user']['createTime']
        create_datetime = datetime.datetime.fromtimestamp(int(create_time_seconds))
        formatted_create_date = create_datetime.strftime("%Y/%m/%d %H:%M")
        output_text += (
            f"اسم المستخدم: {user_info['user']['uniqueId']}<br><br>"
            f"الاسم المستعار: {user_info['user']['nickname']}<br><br>"
            f"المعرف: {user_info['user']['id']}<br><br>"
            f"تاريخ الإنشاء: {formatted_create_date}<br>"
            f"المتابعون: {user_info['stats']['followerCount']}<br><br>"
            f"يتابع: {user_info['stats']['followingCount']}<br><br>"
            f"الإعجابات: {user_info['stats']['heartCount']}<br><br>"
            f"مقاطع الفيديو: {user_info['stats']['videoCount']}<br><br>"
            f"السيرة الذاتية: {user_info['user']['signature']}<br><br>"
        )

        country_code = user_info.get('user', {}).get('region')
        country_info = get_country_info(country_code)
        output_text += f"البلد: {country_info.get('name', 'غير معروف')}<br>"

        output_text += f'<a href="{pfp_url}" download="{pfp_filename}">تنزيل صورة الملف الشخصي</a><br>'

        return output_text

    except (KeyError, TypeError) as e:
        return f"خطأ في معالجة البيانات: {e}.  من المحتمل أن يكون اسم المستخدم أو تنسيق البيانات غير صالح.  الخطأ: {e}"


@app.route("/", methods=["GET", "POST"])
def index():
    output_text = ""
    username = None
    if request.method == "POST":
        username = request.form.get("username")
        if username:
            user_data = fetch_tiktok_data(username)
            if user_data:
                output_text = process_tiktok_data(user_data)
            else:
                output_text = "لا يمكن استرداد البيانات. تحقق من اسم المستخدم أو الشبكة."
        else:
            output_text = "الرجاء إدخال اسم مستخدم."

    current_year = datetime.datetime.now().year
    return render_template("index.html", output_text=output_text, current_year=current_year, username=username)

if __name__ == "__main__":
    app.run(debug=False)