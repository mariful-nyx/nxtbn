from django.db import models
from django.utils.translation import gettext_lazy as _

class MoneyFieldTypes(models.TextChoices):
    """Enumeration for specifying the type of monetary field, either as units or subunits."""
    UNIT = "unit", "Unit"
    SUBUNIT = "subunit", "Subunit"

class PublishableStatus(models.TextChoices):
    """Enumeration for specifying the status of a publishable object."""
    DRAFT = "DRAFT", _("Draft")
    PUBLISHED = "PUBLISHED", _("Published")
    ARCHIVED = "ARCHIVED", _("Archived")

class CurrencyTypes(models.TextChoices):
    USD = "USD", _("United States Dollar")
    EUR = "EUR", _("Euro")
    GBP = "GBP", _("British Pound Sterling")
    JPY = "JPY", _("Japanese Yen")
    AUD = "AUD", _("Australian Dollar")
    CAD = "CAD", _("Canadian Dollar")
    CHF = "CHF", _("Swiss Franc")
    CNY = "CNY", _("Chinese Yuan")
    SEK = "SEK", _("Swedish Krona")
    NZD = "NZD", _("New Zealand Dollar")
    INR = "INR", _("Indian Rupee")
    BRL = "BRL", _("Brazilian Real")
    RUB = "RUB", _("Russian Ruble")
    ZAR = "ZAR", _("South African Rand")
    AED = "AED", _("United Arab Emirates Dirham")
    AFN = "AFN", _("Afghan Afghani")
    ALL = "ALL", _("Albanian Lek")
    AMD = "AMD", _("Armenian Dram")
    ANG = "ANG", _("Netherlands Antillean Guilder")
    AOA = "AOA", _("Angolan Kwanza")
    ARS = "ARS", _("Argentine Peso")
    AWG = "AWG", _("Aruban Florin")
    AZN = "AZN", _("Azerbaijani Manat")
    BAM = "BAM", _("Bosnia and Herzegovina Convertible Mark")
    BBD = "BBD", _("Barbadian Dollar")
    BDT = "BDT", _("Bangladeshi Taka")
    BGN = "BGN", _("Bulgarian Lev")
    BHD = "BHD", _("Bahraini Dinar")
    BIF = "BIF", _("Burundian Franc")
    BMD = "BMD", _("Bermudian Dollar")
    BND = "BND", _("Brunei Dollar")
    BOB = "BOB", _("Bolivian Boliviano")
    BSD = "BSD", _("Bahamian Dollar")
    BTN = "BTN", _("Bhutanese Ngultrum")
    BWP = "BWP", _("Botswana Pula")
    BYN = "BYN", _("Belarusian Ruble")
    BZD = "BZD", _("Belize Dollar")
    CDF = "CDF", _("Congolese Franc")
    CLP = "CLP", _("Chilean Peso")
    COP = "COP", _("Colombian Peso")
    CRC = "CRC", _("Costa Rican Colón")
    CUP = "CUP", _("Cuban Peso")
    CVE = "CVE", _("Cape Verdean Escudo")
    CZK = "CZK", _("Czech Koruna")
    DJF = "DJF", _("Djiboutian Franc")
    DKK = "DKK", _("Danish Krone")
    DOP = "DOP", _("Dominican Peso")
    DZD = "DZD", _("Algerian Dinar")
    EGP = "EGP", _("Egyptian Pound")
    ERN = "ERN", _("Eritrean Nakfa")
    ETB = "ETB", _("Ethiopian Birr")
    FJD = "FJD", _("Fijian Dollar")
    FKP = "FKP", _("Falkland Islands Pound")
    FOK = "FOK", _("Faroese Króna")
    GEL = "GEL", _("Georgian Lari")
    GGP = "GGP", _("Guernsey Pound")
    GHS = "GHS", _("Ghanaian Cedi")
    GIP = "GIP", _("Gibraltar Pound")
    GMD = "GMD", _("Gambian Dalasi")
    GNF = "GNF", _("Guinean Franc")
    GTQ = "GTQ", _("Guatemalan Quetzal")
    GYD = "GYD", _("Guyanese Dollar")
    HKD = "HKD", _("Hong Kong Dollar")
    HNL = "HNL", _("Honduran Lempira")
    HRK = "HRK", _("Croatian Kuna")
    HTG = "HTG", _("Haitian Gourde")
    HUF = "HUF", _("Hungarian Forint")
    IDR = "IDR", _("Indonesian Rupiah")
    ILS = "ILS", _("Israeli New Shekel")
    IMP = "IMP", _("Isle of Man Pound")
    IQD = "IQD", _("Iraqi Dinar")
    IRR = "IRR", _("Iranian Rial")
    ISK = "ISK", _("Icelandic Króna")
    JMD = "JMD", _("Jamaican Dollar")
    JOD = "JOD", _("Jordanian Dinar")
    KES = "KES", _("Kenyan Shilling")
    KGS = "KGS", _("Kyrgyzstani Som")
    KHR = "KHR", _("Cambodian Riel")
    KID = "KID", _("Kiribati Dollar")
    KMF = "KMF", _("Comorian Franc")
    KRW = "KRW", _("South Korean Won")
    KWD = "KWD", _("Kuwaiti Dinar")
    KYD = "KYD", _("Cayman Islands Dollar")
    KZT = "KZT", _("Kazakhstani Tenge")
    LAK = "LAK", _("Lao Kip")
    LBP = "LBP", _("Lebanese Pound")
    LKR = "LKR", _("Sri Lankan Rupee")
    LRD = "LRD", _("Liberian Dollar")
    LSL = "LSL", _("Lesotho Loti")
    LYD = "LYD", _("Libyan Dinar")
    MAD = "MAD", _("Moroccan Dirham")
    MDL = "MDL", _("Moldovan Leu")
    MGA = "MGA", _("Malagasy Ariary")
    MKD = "MKD", _("Macedonian Denar")
    MMK = "MMK", _("Burmese Kyat")
    MNT = "MNT", _("Mongolian Tögrög")
    MOP = "MOP", _("Macanese Pataca")
    MRU = "MRU", _("Mauritanian Ouguiya")
    MUR = "MUR", _("Mauritian Rupee")
    MVR = "MVR", _("Maldivian Rufiyaa")
    MWK = "MWK", _("Malawian Kwacha")
    MXN = "MXN", _("Mexican Peso")
    MYR = "MYR", _("Malaysian Ringgit")
    MZN = "MZN", _("Mozambican Metical")
    NAD = "NAD", _("Namibian Dollar")
    NGN = "NGN", _("Nigerian Naira")
    NIO = "NIO", _("Nicaraguan Córdoba")
    NOK = "NOK", _("Norwegian Krone")
    NPR = "NPR", _("Nepalese Rupee")
    OMR = "OMR", _("Omani Rial")
    PAB = "PAB", _("Panamanian Balboa")
    PEN = "PEN", _("Peruvian Sol")
    PGK = "PGK", _("Papua New Guinean Kina")
    PHP = "PHP", _("Philippine Peso")
    PKR = "PKR", _("Pakistani Rupee")
    PLN = "PLN", _("Polish Złoty")
    PYG = "PYG", _("Paraguayan Guaraní")
    QAR = "QAR", _("Qatari Riyal")
    RON = "RON", _("Romanian Leu")
    RSD = "RSD", _("Serbian Dinar")
    RWF = "RWF", _("Rwandan Franc")
    SAR = "SAR", _("Saudi Riyal")
    SBD = "SBD", _("Solomon Islands Dollar")
    SCR = "SCR", _("Seychellois Rupee")
    SDG = "SDG", _("Sudanese Pound")
    SGD = "SGD", _("Singapore Dollar")
    SHP = "SHP", _("Saint Helena Pound")
    SLL = "SLL", _("Sierra Leonean Leone")
    SOS = "SOS", _("Somali Shilling")
    SRD = "SRD", _("Surinamese Dollar")
    SSP = "SSP", _("South Sudanese Pound")
    STN = "STN", _("São Tomé and Príncipe Dobra")
    SYP = "SYP", _("Syrian Pound")
    SZL = "SZL", _("Eswatini Lilangeni")
    THB = "THB", _("Thai Baht")
    TJS = "TJS", _("Tajikistani Somoni")
    TMT = "TMT", _("Turkmenistani Manat")
    TND = "TND", _("Tunisian Dinar")
    TOP = "TOP", _("Tongan Pa'anga")
    TRY = "TRY", _("Turkish Lira")
    TTD = "TTD", _("Trinidad and Tobago Dollar")
    TVD = "TVD", _("Tuvaluan Dollar")
    TWD = "TWD", _("New Taiwan Dollar")
    TZS = "TZS", _("Tanzanian Shilling")
    UAH = "UAH", _("Ukrainian Hryvnia")
    UGX = "UGX", _("Ugandan Shilling")
    UYU = "UYU", _("Uruguayan Peso")
    UZS = "UZS", _("Uzbekistani Som")
    VES = "VES", _("Venezuelan Bolívar Soberano")
    VND = "VND", _("Vietnamese Đồng")
    VUV = "VUV", _("Vanuatu Vatu")
    WST = "WST", _("Samoan Tālā")
    XAF = "XAF", _("Central African CFA Franc")
    XCD = "XCD", _("East Caribbean Dollar")
    XOF = "XOF", _("West African CFA Franc")
    XPF = "XPF", _("CFP Franc")
    YER = "YER", _("Yemeni Rial")
    ZMW = "ZMW", _("Zambian Kwacha")
    ZWL = "ZWL", _("Zimbabwean Dollar")



class LanguageChoices(models.TextChoices):
    ENGLISH_US = "en-US", "English (United States)"
    ENGLISH_UK = "en-GB", "English (United Kingdom)"
    ENGLISH_CA = "en-CA", "English (Canada)"
    ENGLISH_AU = "en-AU", "English (Australia)"
    ENGLISH_IN = "en-IN", "English (India)"
    ENGLISH_AE = "en-AE", "English (United Arab Emirates)"
    ENGLISH_SG = "en-SG", "English (Singapore)"
    ENGLISH_NZ = "en-NZ", "English (New Zealand)"
    ENGLISH_IE = "en-IE", "English (Ireland)"
    ENGLISH_ZA = "en-ZA", "English (South Africa)"
    ENGLISH_PH = "en-PH", "English (Philippines)"
    ENGLISH_FJ = "en-FJ", "English (Fiji)"
    ENGLISH_IL = "en-IL", "English ( Israel)"
    HEBREW = "he-IL" , "Hebrew ( Israel)"
    BANGLA_BD = "bn-BD", "Bangla (Bangladesh)"
    BANGLA_IN = "bn-IN", "Bangla (India)"
    FRENCH_FR = "fr-FR", "French (France)"
    FRENCH_CA = "fr-CA", "French (Canada)"
    FRENCH_BE = "fr-BE", "French (Belgium)"
    FRENCH_CH = "fr-CH", "French (Switzerland)"
    SPANISH_ES = "es-ES", "Spanish (Spain)"
    SPANISH_MX = "es-MX", "Spanish (Mexico)"
    SPANISH_AR = "es-AR", "Spanish (Argentina)"
    SPANISH_CO = "es-CO", "Spanish (Colombia)"
    SPANISH_US = "es-US", "Spanish (United States)"
    ARABIC_AE = "ar-AE", "Arabic (United Arab Emirates)"
    ARABIC_SA = "ar-SA", "Arabic (Saudi Arabia)"
    ARABIC_EG = "ar-EG", "Arabic (Egypt)"
    ARABIC_MA = "ar-MA", "Arabic (Morocco)"
    CHINESE_CN = "zh-CN", "Chinese (Simplified, China)"
    CHINESE_HK = "zh-HK", "Chinese (Traditional, Hong Kong)"
    CHINESE_TW = "zh-TW", "Chinese (Traditional, Taiwan)"
    HINDI_IN = "hi-IN", "Hindi (India)"
    GERMAN_DE = "de-DE", "German (Germany)"
    GERMAN_AT = "de-AT", "German (Austria)"
    GERMAN_CH = "de-CH", "German (Switzerland)"
    PORTUGUESE_PT = "pt-PT", "Portuguese (Portugal)"
    PORTUGUESE_BR = "pt-BR", "Portuguese (Brazil)"
    RUSSIAN_RU = "ru-RU", "Russian (Russia)"
    RUSSIAN_BY = "ru-BY", "Russian (Belarus)"
    RUSSIAN_KZ = "ru-KZ", "Russian (Kazakhstan)"
    JAPANESE_JP = "ja-JP", "Japanese (Japan)"
    KOREAN_KR = "ko-KR", "Korean (South Korea)"
    ITALIAN_IT = "it-IT", "Italian (Italy)"
    ITALIAN_CH = "it-CH", "Italian (Switzerland)"
    DUTCH_NL = "nl-NL", "Dutch (Netherlands)"
    DUTCH_BE = "nl-BE", "Dutch (Belgium)"
    GREEK_GR = "el-GR", "Greek (Greece)"
    TURKISH_TR = "tr-TR", "Turkish (Turkey)"
    SWEDISH_SE = "sv-SE", "Swedish (Sweden)"
    NORWEGIAN_NO = "no-NO", "Norwegian (Norway)"
    DANISH_DK = "da-DK", "Danish (Denmark)"
    FINNISH_FI = "fi-FI", "Finnish (Finland)"
    POLISH_PL = "pl-PL", "Polish (Poland)"
    VIETNAMESE_VN = "vi-VN", "Vietnamese (Vietnam)"
    THAI_TH = "th-TH", "Thai (Thailand)"
    INDONESIAN_ID = "id-ID", "Indonesian (Indonesia)"
    MALAY_MY = "ms-MY", "Malay (Malaysia)"
    UKRAINIAN_UA = "uk-UA", "Ukrainian (Ukraine)"
    CZECH_CZ = "cs-CZ", "Czech (Czech Republic)"
    SLOVAK_SK = "sk-SK", "Slovak (Slovakia)"
    HUNGARIAN_HU = "hu-HU", "Hungarian (Hungary)"
    ROMANIAN_RO = "ro-RO", "Romanian (Romania)"
    BULGARIAN_BG = "bg-BG", "Bulgarian (Bulgaria)"
    CROATIAN_HR = "hr-HR", "Croatian (Croatia)"
    SERBIAN_RS = "sr-RS", "Serbian (Serbia)"
    SLOVENIAN_SI = "sl-SI", "Slovenian (Slovenia)"
    LITHUANIAN_LT = "lt-LT", "Lithuanian (Lithuania)"
    LATVIAN_LV = "lv-LV", "Latvian (Latvia)"
    ESTONIAN_EE = "et-EE", "Estonian (Estonia)"
    MALTESE_MT = "mt-MT", "Maltese (Malta)"
    ICELANDIC_IS = "is-IS", "Icelandic (Iceland)"
    ALBANIAN_AL = "sq-AL", "Albanian (Albania)"
    MACEDONIAN_MK = "mk-MK", "Macedonian (North Macedonia)"
    BASQUE_ES = "eu-ES", "Basque (Spain)"
    GALICIAN_ES = "gl-ES", "Galician (Spain)"
    WELSH_GB = "cy-GB", "Welsh (United Kingdom)"
    BRETON_FR = "br-FR", "Breton (France)"
    CATALAN_ES = "ca-ES", "Catalan (Spain)"
    OCCITAN_FR = "oc-FR", "Occitan (France)"
    CORSICAN_FR = "co-FR", "Corsican (France)"
    ALEMANNIC_DE = "gsw-DE", "Alemannic (Germany)"
    LUXEMBOURGISH_LU = "lb-LU", "Luxembourgish (Luxembourg)"
    AFRIKAANS_ZA = "af-ZA", "Afrikaans (South Africa)"
    SWAHILI_KE = "sw-KE", "Swahili (Kenya)"
    KINYARWANDA_RW = "rw-RW", "Kinyarwanda (Rwanda)"
    KIRUNDI_BI = "rn-BI", "Kirundi (Burundi)"
    LINGALA_CD = "ln-CD", "Lingala (Congo - Kinshasa)"
    KONGO_CD = "kg-CD", "Kongo (Congo - Kinshasa)"
    TSHILUBA_CD = "lu-CD", "Tshiluba (Congo - Kinshasa)"
    CHICHEWA_MW = "ny-MW", "Chichewa (Malawi)"
    CHEWA_ZM = "ny-ZM", "Chewa (Zambia)"
    SESOTHO_LS = "st-LS", "Sesotho (Lesotho)"
    SETSWANA_BW = "tn-BW", "Setswana (Botswana)"
    SOGA_UG = "xog-UG", "Soga (Uganda)"
    VENDA_ZA = "ve-ZA", "Venda (South Africa)"
    ZULU_ZA = "zu-ZA", "Zulu (South Africa)"
    TIGRINYA_ET = "ti-ET", "Tigrinya (Ethiopia)"
    PASHTO_AF = "ps-AF", "Pashto (Afghanistan)"
    DARI_AF = "fa-AF", "Dari (Afghanistan)"
    UZBEK_UZ = "uz-UZ", "Uzbek (Uzbekistan)"
    KAZAKH_KZ = "kk-KZ", "Kazakh (Kazakhstan)"
    TAJIK_TJ = "tg-TJ", "Tajik (Tajikistan)"
    TURKMEN_TM = "tk-TM", "Turkmen (Turkmenistan)"
    KYRGYZ_KG = "ky-KG", "Kyrgyz (Kyrgyzstan)"
    ARMENIAN_AM = "hy-AM", "Armenian (Armenia)"
    GEORGIAN_GE = "ka-GE", "Georgian (Georgia)"
    AZERBAIJANI_AZ = "az-AZ", "Azerbaijani (Azerbaijan)"
    MONGOLIAN_MN = "mn-MN", "Mongolian (Mongolia)"
    SINHALA_LK = "si-LK", "Sinhala (Sri Lanka)"
    TAMIL_IN = "ta-IN", "Tamil (India)"
    TAMIL_LK = "ta-LK", "Tamil (Sri Lanka)"
    TELUGU_IN = "te-IN", "Telugu (India)"
    KANNADA_IN = "kn-IN", "Kannada (India)"
    MALAYALAM_IN = "ml-IN", "Malayalam (India)"
    MARATHI_IN = "mr-IN", "Marathi (India)"
    GUJARATI_IN = "gu-IN", "Gujarati (India)"
    PUNJABI_IN = "pa-IN", "Punjabi (India)"
    PUNJABI_PK = "pa-PK", "Punjabi (Pakistan)"
    URDU_PK = "ur-PK", "Urdu (Pakistan)"
    URDU_IN = "ur-IN", "Urdu (India)"
    NEPALI_NP = "ne-NP", "Nepali (Nepal)"
    TIBETAN_CN = "bo-CN", "Tibetan (China)"
    BURMESE_MM = "my-MM", "Burmese (Myanmar)"
    KHMER_KH = "km-KH", "Khmer (Cambodia)"
    LAO_LA = "lo-LA", "Lao (Laos)"
    MALAY_SG = "ms-SG", "Malay (Singapore)"
    MALAY_ID = "ms-ID", "Malay (Indonesia)"
    MALAY_BN = "ms-BN", "Malay (Brunei)"
    FILIPINO_PH = "fil-PH", "Filipino (Philippines)"
    MAORI_NZ = "mi-NZ", "Maori (New Zealand)"
    SAMOAN_WS = "sm-WS", "Samoan (Samoa)"
    TONGAN_TO = "to-TO", "Tongan (Tonga)"
    FIJIAN_FJ = "fj-FJ", "Fijian (Fiji)"
    HAWAIIAN_US = "haw-US", "Hawaiian (United States)"
    TAHITIAN_PF = "ty-PF", "Tahitian (French Polynesia)"
    MALAGASY_MG = "mg-MG", "Malagasy (Madagascar)"
    SESOTHO_ZA = "st-ZA", "Sesotho (South Africa)"
    TSWANA_ZA = "tn-ZA", "Tswana (South Africa)"
    XHOSA_ZA = "xh-ZA", "Xhosa (South Africa)"
    SWAHILI_TZ = "sw-TZ", "Swahili (Tanzania)"
    SWAHILI_UG = "sw-UG", "Swahili (Uganda)"
    SWAHILI_CD = "sw-CD", "Swahili (Congo - Kinshasa)"
    SOMALI_SO = "so-SO", "Somali (Somalia)"
    SOMALI_ET = "so-ET", "Somali (Ethiopia)"
    SOMALI_KE = "so-KE", "Somali (Kenya)"
    SOMALI_DJ = "so-DJ", "Somali (Djibouti)"
    AMHARIC_ET = "am-ET", "Amharic (Ethiopia)"
    TIGRINYA_ER = "ti-ER", "Tigrinya (Eritrea)"
    OROMO_ET = "om-ET", "Oromo (Ethiopia)"
    OROMO_KE = "om-KE", "Oromo (Kenya)"
    HAUSA_NG = "ha-NG", "Hausa (Nigeria)"
    HAUSA_NE = "ha-NE", "Hausa (Niger)"
    HAUSA_GH = "ha-GH", "Hausa (Ghana)"
    YORUBA_NG = "yo-NG", "Yoruba (Nigeria)"
    YORUBA_BJ = "yo-BJ", "Yoruba (Benin)"
    IGBO_NG = "ig-NG", "Igbo (Nigeria)"
    FULAH_SN = "ff-SN", "Fulah (Senegal)"
    FULAH_GM = "ff-GM", "Fulah (Gambia)"
    FULAH_MR = "ff-MR", "Fulah (Mauritania)"
    FULAH_GN = "ff-GN", "Fulah (Guinea)"
    WOLOF_SN = "wo-SN", "Wolof (Senegal)"
    WOLOF_GM = "wo-GM", "Wolof (Gambia)"
    WOLOF_MR = "wo-MR", "Wolof (Mauritania)"
    BERBER_MA = "ber-MA", "Berber (Morocco)"
    BERBER_DZ = "ber-DZ", "Berber (Algeria)"
    BERBER_LY = "ber-LY", "Berber (Libya)"
    BERBER_TN = "ber-TN", "Berber (Tunisia)"
    BERBER_ML = "ber-ML", "Berber (Mali)"
    BERBER_NG = "ber-NG", "Berber (Niger)"