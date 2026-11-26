# العمل الثاني — رفيق سيدي بوسعيد
**Travail 2 — Rafik Sidi Bou Saïd · Work 2 — Rafik Sidi Bou Saïd**

أربع صفحات تفاعلية مستقلّة حول قرية سيدي بوسعيد، **تُعلن ما لا تعرفه**.
Quatre pages interactives autonomes — qui affichent ce qu'elles ne savent pas.
Four standalone interactive pages — that display what they don't know.

حجز المقهى وشاشة المطبخ صارا في [العمل الثالث — احجز قبل ما توصل](../amal-3/).

**جرّبها:** https://samehgassouma-cloud.github.io/sidi-bou-said-hill/amal-2/

---

## القاعدة المركزية · Le principe · The governing rule

| | |
|---|---|
| ✓ **مؤكّد · Vérifié · Verified** | معلومة من مصدر موثّق، معروضة مع مصدرها |
| ⚠ **يتطلّب تحقّق · À vérifier · To verify** | معلومة غير مؤكّدة، بشارة ظاهرة — لا تُعرض أبداً كأنها ثابتة |

التوقيت والأسعار والبرامج **لم تُعمَّر بأرقام تبدو معقولة** — بقيت `[يتطلّب تأكيد]`. سعر مفبرك
يُعرض على حريف أغلى من خانة فارغة.

Horaires, tarifs et programmes **n'ont pas été remplis avec des valeurs plausibles** : ils restent
`[à confirmer]`. Un tarif inventé montré à un client coûte plus cher qu'un champ vide.

---

## الصفحات · Les pages · The pages

| الصفحة | ما تعمل | التوليد |
|---|---|---|
| `index.html` | صفحة استقبال العمل | — |
| `refek-sidi-bou-said-3d.html` | ديوراما بخمسة مشاهد (Three.js r128) | `prototype/build_3d.py` |
| `sidi-bou-said-carte.html` | مخطّط القرية: 8 معالم على جولة ≈ 1740 م | `prototype/build_village.py` |
| `carte-tunisie.html` | خريطة تونس: 23 ولاية و144 مدينة | `prototype/build_map.py` |
| `refek-sidi-bou-said.html` | محادثة الدليل الثقافي | `prototype/build_app.py` |

الصفحات مربوطة بينها: **تونس → القرية → الديوراما**. من مخطّط القرية، زرّ الحجز في المقهيين يفتح [العمل الثالث](../amal-3/cafe-reservation-3d.html).
الروابط القديمة `cafe-reservation-3d.html` و`cuisine-kds.html` تحوّل تلقائياً إلى العمل الثالث.

---

## التشغيل محلياً · Lancer en local · Run locally

```bash
python prototype/build_map.py        # خريطة تونس
python prototype/build_village.py    # مخطّط القرية
python prototype/build_3d.py         # الديوراما
python prototype/build_app.py        # المحادثة
```

بلا أي تبعية: المكتبة القياسية لبايثون فقط. **الملفات لازم تبقى في نفس المجلّد** حتى تخدم
الروابط بيناتها.

Aucune dépendance : bibliothèque standard Python uniquement.
**Les fichiers doivent rester dans le même dossier** pour que les liens fonctionnent.

---

## المقهى وشاشة المطبخ

انتقلوا إلى [العمل الثالث — احجز قبل ما توصل](../amal-3/).
البناء من هناك: `python prototype/build_cafe.py` و`python prototype/build_kds.py`.

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
- **الحدود الرسمية لمنطقة اليونسكو غير متوفّرة**: الدائرتان تعرضان المساحة الصحيحة
  (76,54 هك + 84,44 هك زون عازلة) بنصف قطر مكافئ، **وليستا الحدّ الحقيقي**
- عدد المراكب في الميناء: **محاكاة**، موش رفع ميداني
- خطط قاعات المقاهي ولافتاتها وحجز الطاولة: صارت في [العمل الثالث](../amal-3/)
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
[LinkedIn](https://linkedin.com/in/sameh-gassouma-ab58703b2)
