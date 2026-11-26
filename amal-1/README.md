# العمل الأول — هضبة سيدي بوسعيد
**Travail 1 — Colline de Sidi Bou Saïd · Work 1 — Sidi Bou Said hill**

صفحة واحدة مستقلّة بتبويبين: **دليل للسكان** حول علامات خطر الانزلاق، و**أداة جيوتقنية أولية**
للمهندسين بطريقة Bishop المبسّطة وعرض ثلاثي الأبعاد.

Une page autonome, deux volets : un guide pour les habitants et un outil géotechnique
préliminaire (Bishop simplifiée, vue 3D).
One standalone page, two parts: a residents' guide and a preliminary geotechnical tool.

**جرّبها:** https://samehgassouma-cloud.github.io/sidi-bou-said-hill/amal-1/

---

## القاعدة المركزية · Le principe · The governing rule

| | |
|---|---|
| ✓ **موثّق · Vérifié · Verified** | الطريقة مُتحقَّق منها على أمثلة مرجعية — [`docs/validation.md`](docs/validation.md) |
| ⚠ **تقديري · Indicatif · Indicative** | المعطيات الافتراضية **أمثلة**، وليست معطيات الهضبة |

نتائج الأسبار الرسمية غير منشورة، فخانات التربة **لم تُعمَّر بأرقام تبدو معقولة**: القيم الموجودة
أمثلة معلنة كأمثلة. معامل أمان مفبرك لمبنى يسكنه الناس أخطر من خانة فارغة. النتائج تقديرية، لا
تُعدّ تقييمًا رسميًا لأي مبنى، ولا تُغني عن الدراسة الجيوتقنية الميدانية الجارية.

Les résultats de sondages officiels ne sont pas publiés : les valeurs de sol sont des exemples
annoncés comme tels. Un coefficient de sécurité inventé pour un immeuble habité coûte plus cher
qu'un champ vide.

---

## الصفحات · Les pages · The pages

| الصفحة | ما تعمل | التوليد |
|---|---|---|
| `index.html` | صفحة استقبال العمل | — |
| `sidi-bou-said-landslide.html` | التوعية + أداة Bishop + العرض ثلاثي الأبعاد | `prototype/build_landslide.py` |

### التبويب الأول — التوعية والسلامة

ستّ علامات خطر (شقوق تتّسع، أبواب تعلق، ميلان، تسرّب ماء، هبوط الأرض، تساقط حجارة)، وماذا يُفعل
عند ظهورها، ورقم **الحماية المدنية 198**، وأسباب الانزلاق، والمسار الرسمي لسنة 2026 مع مصادره.

### التبويب الثاني — الأداة الجيوتقنية

تُدخَل الطبقات (القاع، γ، c′، φ′)، ومنسوب الماء، وحمولة المباني وموضعها، والمعامل الزلزالي kh.
تُحسب دائرة الانزلاق الحرجة وتُعرض في مجسّم ثلاثي الأبعاد مع:

- معامل الأمان الساكن والزلزالي
- مراكز الدوائر المجرّبة ملوّنة حسب معامل الأمان
- فحص أي شريحة من الثلاثين مع أسهم القوى (W · kh·W · المقاومة)
- أعمدة ثلاثية الأبعاد لتأثير منسوب الماء
- محاكاة عاصفة: يرتفع الماء، يُعاد الحساب عند كل منسوب، ثم انزلاق دوراني حول مركز الدائرة إذا نزل المعامل تحت 1
- جدول الشرائح الكامل

```
F  = Σ [ (c′·b + (W − u·b)·tanφ′) / mα ] ÷ Σ [ W·sinα + kh·W·(yc − yg)/R ]
mα = cosα + sinα·tanφ′ / F
```

---

## التشغيل محلياً · Lancer en local · Run locally

```bash
python prototype/build_landslide.py      # يبني sidi-bou-said-landslide.html
```

بلا أي تبعية: المكتبة القياسية لبايثون فقط.
Sans aucune dépendance : bibliothèque standard de Python seulement.

Three.js r128 يُحمَّل من CDN عند فتح الأداة. إذا تعذّر التحميل أو لم يدعم الجهاز WebGL، تعود
الأداة تلقائياً إلى الرسم ثنائي الأبعاد **بالحسابات نفسها** — لا شاشة سوداء.

---

## المصدر · La source · The source

```
prototype/
├── build_landslide.py          المولّد: قالب HTML + حقن المصدر والمعطيات
├── data/defaults.json          القيم الافتراضية: الطبقات، الحقول وحدودها، عدد الشرائح، القيم المرجعية
├── i18n/ar.json fr.json en.json  76 مفتاحاً × 3 لغات (البنية مُتحقَّق منها عند البناء)
└── ui/
    ├── bishop.js               محرّك Bishop: makeModel · bishop · search
    ├── scene3d.js              العرض ثلاثي الأبعاد والعاصفة والتسميات والفحص
    └── app.js                  الواجهة: اللغات، التبويبات، القراءة، العرض، الرسم ثنائي الأبعاد
```

**لا تُعدَّل `sidi-bou-said-landslide.html` مباشرة** — تُولَّد من جديد عند كل بناء. لتغيير قيم
التربة الافتراضية أو حدود الحقول، عدّل `data/defaults.json`. لتغيير نصّ، عدّل ملف اللغة. البناء
يرفض الإكمال إذا اختلفت مفاتيح اللغات الثلاث أو نقص حقل.

---

## الحدود · Limites · Limitations

- مقطع ثنائي الأبعاد مثالي: لا فوالق، ولا انزلاقات غير دائرية، ولا تعرية بحرية
- ضغط الماء هيدروستاتيكي تحت خط الماء (بلا تدفّق)
- التأثير الزلزالي شبه ساكن
- الوزن الحجمي المُدخل يُطبَّق فوق الماء وتحته

تفصيل أوسع في [`docs/validation.md`](docs/validation.md).

---

## الرسوم · Les figures · The figures

في [`design/`](design/) — أربعة ملفات SVG أصلية ثلاثية اللغات، بلا أي شعار لطرف ثالث:
علامات الخطر · طريقة Bishop · سلّم معامل الأمان · القوى على المنحدر.

---

## المصادر · Sources

La Presse de Tunisie · Webmanagercenter · Kapitalis · Ultra Tunisia · Jawhara FM — 2024-2026
وزارة التجهيز والإسكان — بلاغات لجنة قيادة مشروع حماية هضبة سيدي بوسعيد

---

**سماح قسومة — مدرّبة دولية · مستشارة جبائية**
**Sameh Gassouma — Formatrice internationale · Conseillère fiscale**
**Sameh Gassouma — International Trainer · Tax Advisor**

TadreebPro.ai · samehgassouma@tadreebpro.ai
