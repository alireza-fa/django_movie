FILM = 1
SERIES = 2

TYPE_CHOICES = (
    (FILM, 'film'),
    (SERIES, 'series'),
)

ORIGIN_QUALITY = 1
CURTAIN_QUALITY = 2

QUALITY_CHOICES = (
    (ORIGIN_QUALITY, 'کیفیت اصلی'),
    (CURTAIN_QUALITY, 'کیفیت پرده')
)


# Country
AFGHANISTAN = 'afghanistan'
ARGENTINA = 'argentina'
AUSTRIA = 'austria'
AZERBAIJAN = 'azerbaijan'
BELGIUM = 'belgium'
BRAZIL = 'brazil'
BULGARIA = 'bulgaria'
CAMEROON = 'cameroon'
CANADA = 'canada'
CHILE = 'chile'
CHINA = 'china'
COLOMBIA = 'colombia'
DENMARK = 'denmark'
EGYPT = 'egypt'
FINLAND = 'finland'
FRANCE = 'france'
GERMANY = 'germany'
HUNGARY = 'hungary'
INDONESIA = 'indonesia'
IRAN = 'iran'
IRAQ = 'iraq'
ITALY = 'italy'
JAPAN = 'japan'
MEXICO = 'mexico'
MOROCCO = 'morocco'
NEPAL = 'nepal'
NETHERLANDS = 'netherlands'
POLAND = 'poland'
PORTUGAL = 'portugal'
ROMANIA = 'romania'
RUSSIA = 'russia'
SWEDEN = 'sweden'
THAILAND = 'thailand'
TURKEY = 'turkey'
UNITED_KINGDOM = 'uk'
UNITED_STATES_OF_AMERICAN = 'usa'
VIETNAM = 'vietnam'

COUNTRY_CHOICES = (
    (AFGHANISTAN, 'افغانستان'),
    (ARGENTINA, 'آرژانتین'),
    (AUSTRIA, 'استرالیا'),
    (AZERBAIJAN, 'آذربایجان'),
    (BELGIUM, 'بلژیک'),
    (CAMEROON, 'کامرون'),
    (CANADA, 'کانادا'),
    (CHILE, 'شیلی'),
    (CHINA, 'چین'),
    (COLOMBIA, 'کلمبیا'),
    (DENMARK, 'دانمارک'),
    (EGYPT, 'مصر'),
    (FINLAND, 'فنلاند'),
    (FRANCE, 'فرانسه'),
    (GERMANY, 'آلمان'),
    (HUNGARY, 'مجارستان'),
    (INDONESIA, 'اندونیزیا'),
    (IRAN, 'ایران'),
    (IRAQ, 'عراق'),
    (ITALY, 'ایتالیا'),
    (JAPAN, 'ژاپن'),
    (MEXICO, 'مکزیک'),
    (MOROCCO, 'مراکش'),
    (NEPAL, 'نپال'),
    (NETHERLANDS, 'ایرلند'),
    (POLAND, 'پولند'),
    (RUSSIA, 'روسیه'),
    (SWEDEN, 'سوئد'),
    (THAILAND, 'تایلند'),
    (TURKEY, 'ترکیه'),
    (UNITED_KINGDOM, 'انگلستان'),
    (UNITED_STATES_OF_AMERICAN, 'آمریکا'),
    (VIETNAM, 'ویتنام'),
)


# Genre
ACTION = 'action'
ANIMATION = 'animation'
COMEDY = 'comedy'
CRIME = 'crime'
DRAMA = 'drama'
EXPERIMENTAL = 'experimental'
FANTASY = 'fantasy'
HISTORICAL = 'historical'
HORROR = 'horror'
ROMANCE = 'romance'
SCIENCE = 'science'
THRILLER = 'thriller'
WESTERN = 'western'
OTHER = 'other'

GENRE_CHOICES = (
    (ACTION, 'اکشن'),
    (ANIMATION, 'انیمیشن'),
    (COMEDY, 'کمدی'),
    (CRIME, 'کرایم'),
    (DRAMA, 'درام'),
    (EXPERIMENTAL, 'اکسپرمنشال'),
    (FANTASY, 'فانتزی'),
    (HISTORICAL, 'تاریخی'),
    (HORROR, 'وحشت'),
    (ROMANCE, 'رمانتیک'),
    (SCIENCE, 'علمی'),
    (THRILLER, 'تریلر'),
    (WESTERN, 'غربی'),
    (OTHER, 'دیگر'),
)
