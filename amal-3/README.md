# العمل الثالث — احجز قبل ما توصل
**Travail 3 — Réservez avant d'arriver · Work 3 — Book before you arrive**

حجز طاولة في قاعة مقهى مجسّمة ثلاثية الأبعاد في سيدي بوسعيد، مع حساب التوقيت بالمقلوب وشاشة مطبخ.
Une réservation de table en terrasse 3D, un minutage à rebours, et un écran cuisine.

**جرّبها:** https://samehgassouma-cloud.github.io/sidi-bou-said-hill/amal-3/

المقهيان في النموذج: **مقهى العليّة** (Café des Nattes) و**مقهى سيدي شعبان** (Café Sidi Chabaane).
المواقع حقيقية؛ خطة القاعة والتوفّر والأسعار محاكاة.

---

## الصفحات · Les pages

| الصفحة | ما تعمل | التوليد |
|---|---|---|
| `index.html` | صفحة استقبال العمل | — |
| `cafe-reservation-3d.html` | حجز طاولة في قاعة مجسّمة + حساب التوقيت بالمقلوب | `prototype/build_cafe.py` |
| `cuisine-kds.html` | شاشة المطبخ: التذاكر مرتّبة بوقت انطلاق التحضير | `prototype/build_kds.py` |

الصفحتان مربوطتان: **الحجز → المطبخ**. ومن مخطّط القرية في [العمل الثاني](../amal-2/) يفتح زرّ «احجز في هذا المقهى» صفحة الحجز هنا.

---

## التشغيل محلياً · Lancer en local

```bash
python prototype/build_cafe.py       # حجز المقهى
python prototype/build_kds.py        # شاشة المطبخ
```

بلا أي تبعية: المكتبة القياسية لبايثون فقط. الملفّان لازم يبقوا في نفس المجلّد حتى تخدم الروابط بيناتهم.

---

## الحساب بالمقلوب · Le minutage à rebours

```
الجاهزية       = وقت وصولك − الفارق المختار (0 / 5 / 15 دقيقة)
بداية التحضير  = الجاهزية − مدّة تحضير الطلب
```

كي الوقت يكون ضيّق، التطبيق **يقولها** بدل ما يوعد بشيء ما يصيرش.

الطلب يخرج بثلاث طرق: **واتساب** (الرقم يدخّلو صاحب المحلّ — ما فمّاش رقم مكتوب في كود الحجز)،
**شاشة المطبخ** عبر BroadcastChannel، و**كود الطلب** للصق اليدوي.

### الوضع السحابي · Mode cloud

1. مشروع Supabase، ثم تنفيذ `prototype/db/schema.sql` في محرّر SQL.
2. لصق عنوان المشروع والمفتاح العمومي في الصفحتين، ثم «اتصل».
3. الطلبات تبدا تمشي بين الأجهزة. بلا إعداد، الكل يبقى محلّي.

⚠ المفتاح العمومي يبان لأي زائر في كود الصفحة. المخطّط يحد القراءة والتحديث في آخر 6 ساعات،
والنشر الحقيقي يلزمو تسجيل دخول لشاشة المطبخ.

---

## الحدود المعلنة · Limites déclarées

- خطط قاعات المقاهي وأماكن المقابس والتوفّر: **محاكاة**، موش رفع ميداني
- لافتات المقاهي **فارغة**: الهوية البصرية ملك أصحابها
- **الحجز لا يُرسل إلى أي جهة**: بلا اتفاق مع المقهى، التأكيد يخلّي الحريف يظنّ عندو طاولة محجوزة

التفصيل في [`../amal-2/docs/culture-check.md`](../amal-2/docs/culture-check.md).

---

<div dir="rtl">

**سماح قسومة** — مدرّبة دولية · مستشارة جبائية

</div>

**Sameh Gassouma** — Formatrice internationale · Conseillère fiscale
**Sameh Gassouma** — International Trainer · Tax Advisor

TadreebPro.ai · samehgassouma@tadreebpro.ai
[LinkedIn](https://linkedin.com/in/sameh-gassouma-ab58703b2)
