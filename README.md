# رفيق سيدي بوسعيد · Rafik Sidi Bou Saïd

**ستّ صفحات تفاعلية لقرية سيدي بوسعيد — تُعلن ما لا تعرفه.**
**Six pages interactives sur le village de Sidi Bou Saïd — qui affichent ce qu'elles ne savent pas.**
**Six interactive pages on the village of Sidi Bou Saïd — that display what they don't know.**

---

## القاعدة المركزية · Le principe · The governing rule

كل معلومة تحمل حالتها. Chaque information porte son statut. Every fact carries its status.

| | |
|---|---|
| ✓ **مؤكّد · Vérifié · Verified** | معلومة من مصدر موثّق، معروضة مع مصدرها |
| ⚠ **يتطلّب تحقّق · À vérifier · To verify** | معلومة غير مؤكّدة، معروضة بشارة ظاهرة — لا تُعرض أبداً كأنها ثابتة |

التوقيت والأسعار والبرامج **لم تُعمَّر بأرقام تبدو معقولة** — بقيت `[يتطلّب تأكيد]`. سعر مفبرك يُعرض على حريف
أغلى من خانة فارغة.

Horaires, tarifs et programmes **n'ont pas été remplis avec des valeurs plausibles** : ils restent
`[à confirmer]`. Un tarif inventé montré à un client coûte plus cher qu'un champ vide.

---

## الصفحات · Les pages · The pages

| الصفحة | ما تعمل | التوليد |
|---|---|---|
| `carte-tunisie.html` | خريطة تونس: 23 ولاية و144 مدينة بإحداثيات موثّقة | `prototype/build_map.py` |
| `sidi-bou-said-carte.html` | مخطّط القرية: 8 معالم تظهر واحداً واحداً على جولة ≈ 1740 م | `prototype/build_village.py` |
| `refek-sidi-bou-said-3d.html` | ديوراما بخمسة مشاهد (Three.js r128) | `prototype/build_3d.py` |
| `refek-sidi-bou-said.html` | محادثة الدليل الثقافي، ثلاثية اللغة | `prototype/build_app.py` |
| `cafe-reservation-3d.html` | حجز طاولة في قاعة ثلاثية الأبعاد + حساب التوقيت بالمقلوب | `prototype/build_cafe.py` |
| `cuisine-kds.html` | شاشة المطبخ: التذاكر مرتّبة بوقت انطلاق التحضير | `prototype/build_kds.py` |

الصفحات مربوطة بينها: **تونس → القرية → الديوراما → المقهى → المطبخ**.
Les pages sont liées entre elles. The pages link to one another.

---

## التشغيل · Lancer · Run

```bash
python prototype/build_map.py        # خريطة تونس
python prototype/build_village.py    # مخطّط القرية
python prototype/build_3d.py         # الديوراما
python prototype/build_app.py        # المحادثة
python prototype/build_cafe.py       # حجز المقهى
python prototype/build_kds.py        # شاشة المطبخ
```

بلا أي تبعية: المكتبة القياسية لبايثون فقط. الصفحات مستقلّة — تتحلّ بنقرة مزدوجة.
**الستّ ملفات لازم تكون في نفس المجلّد** باش الروابط بيناتهم تخدم.

Aucune dépendance : bibliothèque standard Python uniquement. Les pages sont autonomes.
**Les six fichiers doivent rester dans le même dossier** pour que les liens fonctionnent.

### نشرها على الإنترنت · Publier en ligne

في إعدادات المستودع → **Pages** → فرع `main` ومجلّد `/ (root)`. تولّي الصفحات متاحة على:

```
https://samehgassouma-cloud.github.io/sidi-bou-said-hill/carte-tunisie.html
```

وهكذا كل الروابط بين الصفحات تخدم بلا تحميل.

---

## المقهى: الحساب بالمقلوب · Le minutage à rebours

```
الجاهزية       = وقت وصولك − الفارق المختار (0 / 5 / 15 دقيقة)
بداية التحضير  = الجاهزية − مدّة تحضير الطلب
```

كي الوقت يكون ضيّق، التطبيق **يقولها** بدل ما يوعد بشيء ما يصيرش.
Quand le délai est trop court, l'application le dit au lieu de promettre.

الطلب يخرج بثلاث طرق: **واتساب** (الرقم يدخّلو صاحب المحلّ — ما فمّاش رقم مكتوب في الكود)،
**شاشة المطبخ** عبر BroadcastChannel، و**كود الطلب** للصق اليدوي.

### الوضع السحابي · Mode cloud

1. مشروع Supabase، ثم تنفيذ `prototype/db/schema.sql` في محرّر SQL.
2. لصق عنوان المشروع والمفتاح العمومي في الصفحتين، ثم «اتصل».
3. الطلبات تبدا تمشي بين الأجهزة. بلا إعداد، الكل يبقى محلّي.

⚠ المفتاح العمومي يبان لأي زائر في كود الصفحة. المخطّط يحدّ القراءة والتحديث في آخر 6 ساعات،
والنشر الحقيقي يلزمو تسجيل دخول لشاشة المطبخ.

---

## المصادر · Sources

| | |
|---|---|
| حدود الولايات | Natural Earth 10m admin-1 — ملك عام |
| المدن والإحداثيات | GeoNames (via all-the-cities) — CC BY 4.0 |
| إدراج اليونسكو | قائمة التراث العالمي رقم 1769 — الدورة 48، بوسان، 25 جويلية 2026 |
| مواقع المعالم الثمانية | تحقّق موقعاً بموقع |
| الأزرق والأبيض | أمر 28 أوت 1915 — بمسعى البارون رودولف ديرلنجي |

---

## الحدود المعلنة · Limites déclarées · Declared limits

هذي ليست عيوباً مخفية — معلنة في الواجهة وفي `docs/culture-check.md`:

- ولاية **أريانة غير موجودة** في مصدر الحدود المستعمل (23 ولاية موش 24)
- **6 مدن ساحلية** تقع خارج الحدود بعد تبسيط المضلّعات
- أرقام السكان **تقديرات GeoNames**، موش أرقام المعهد الوطني للإحصاء
- **الحدود الرسمية لمنطقة اليونسكو غير متوفّرة**: الدائرتان تعرضان المساحة الصحيحة (76,54 هك + 84,44 هك
  زون عازلة) بنصف قطر مكافئ، **وليستا الحدّ الحقيقي**
- خطط قاعات المقاهي وأماكن المقابس وعدد المراكب في الميناء: **محاكاة**، موش رفع ميداني
- لافتات المقاهي **فارغة**: الهوية البصرية ملك أصحابها
- أسماء 144 مدينة **لم تُترجم للعربية**: بلا مصدر كان الخطأ محتوماً

---

## البناء · docs/

| | |
|---|---|
| `docs/brief.md` | المجال والقرارات |
| `docs/culture-check.md` | فحص المحتوى التونسي — كل ✓ و⚠ و🚫 بسببه |
| `docs/rapport.md` | التقرير الكامل، ثلاثي اللغة |
| `docs/crew-log.md` | أثر الوكلاء الخمسة عبر 12 تكرارة |
| `design/` | 4 ماكيتات SVG أصلية + `tokens.md` |

مبني بـ **tadreeb-prototype-crew** — فريق خمسة وكلاء: تحليل · تصميم · ثقافة · برمجة · جودة.
وكيل الثقافة له حقّ الفيتو.

---

<div dir="rtl">

**سماح قسومة** — مدرّبة دولية · مستشارة جبائية

</div>

**Sameh Gassouma** — Formatrice internationale · Conseillère fiscale
**Sameh Gassouma** — International Trainer · Tax Advisor

TadreebPro.ai · samehgassouma@tadreebpro.ai
WhatsApp : <span dir="ltr">+216 28 516 751</span> · <span dir="ltr">+216 22 022 624</span>
[LinkedIn](https://linkedin.com/in/sameh-gassouma-ab58703b2)
