# هضبة سيدي بوسعيد — التوعية والتحليل الجيوتقني الأولي

**Colline de Sidi Bou Saïd — sensibilisation et analyse géotechnique préliminaire**
**Sidi Bou Said hill — awareness and preliminary geotechnical analysis**

منصة ويب في ملف واحد، ثلاثية اللغات (العربية / الفرنسية / الإنجليزية) مع دعم كامل للكتابة من اليمين إلى اليسار.

Application web autonome, trilingue (arabe / français / anglais), sans dépendance de build.
Self-contained web page, trilingual (Arabic / French / English), no build step.

---

## ⚠️ تنبيه · Avertissement · Disclaimer

**ع** — أداة تعليمية ومساعدة أولية. النتائج تقديرية ولا تُعدّ تقييمًا رسميًا لأي مبنى أو موقع، ولا تُغني عن الدراسة الجيوتقنية الميدانية. القيم الافتراضية أمثلة، ويجب استبدالها بنتائج الأسبار والتجارب المخبرية.

**FR** — Outil pédagogique et d'aide préliminaire. Les résultats sont indicatifs, ne constituent pas une évaluation officielle d'un bâtiment ou d'un site et ne remplacent pas une étude géotechnique de terrain. Les valeurs par défaut sont des exemples : remplacez-les par vos résultats de sondages et d'essais.

**EN** — Educational and preliminary aid only. Results are indicative, are not an official assessment of any building or site, and do not replace a field geotechnical investigation. Default values are examples: replace them with your own borehole and laboratory results.

---

## المحتوى · Contenu · Contents

| الملف | الوصف |
|---|---|
| `index.html` | المنصة كاملة (ملف واحد مستقل) · La plateforme complète · The full platform |
| `assets/warning-signs-infographic.svg` | علامات خطر الانزلاق · Signes de glissement · Warning signs |
| `assets/bishop-method-diagram.svg` | طريقة Bishop المبسّطة · Méthode de Bishop simplifiée · Simplified Bishop method |
| `assets/fos-scale-infographic.svg` | سلّم معامل الأمان · Échelle du coefficient de sécurité · Factor of safety scale |
| `assets/slope-forces-diagram.svg` | القوى المؤثرة في المنحدر · Forces sur la pente · Forces on the slope |

---

## 1. التوعية والسلامة · Sensibilisation · Awareness

- رقم الحماية المدنية **198** · Protection civile · Civil Protection
- ست علامات خطر وما يجب فعله عند ظهورها
- أسباب الانزلاق كما شرحها الجيولوجيون
- المسار الرسمي لسنة 2026 مع مصادره الصحفية

## 2. الأداة الهندسية ثلاثية الأبعاد · Outil d'ingénierie 3D · 3D engineering tool

**الطريقة · Méthode · Method**

Simplified Bishop method, circular slip surfaces, 30 slices, automatic grid search of trial centres with local refinement.

```
F = Σ [ (c′·b + (W − u·b)·tanφ′) / mα ] ÷ Σ [ W·sinα + kh·W·(yc − yg)/R ]
mα = cosα + sinα·tanφ′ / F
```

**المعطيات · Entrées · Inputs** — ارتفاع الجرف H، الميل β، ثلاث طبقات (القاع، γ، c′، φ′)، منسوب الماء، حمولة المباني q وموضعها، المعامل الزلزالي kh.

**المخرجات · Sorties · Outputs**

- معامل الأمان الساكن والزلزالي
- مجسّم ثلاثي الأبعاد (Three.js) للطبقات، خط الماء، المباني، ودائرة الانزلاق الحرجة
- مراكز الدوائر المجرّبة ملوّنة حسب معامل الأمان
- فحص أي شريحة من الثلاثين مع أسهم القوى (W، kh·W، المقاومة)
- أعمدة ثلاثية الأبعاد لتأثير منسوب الماء
- محاكاة عاصفة: ارتفاع الماء، إعادة الحساب عند كل منسوب، ثم انزلاق دوراني حول مركز الدائرة إذا نزل المعامل تحت 1
- جدول الشرائح الكامل

**التحقق · Vérification · Validation**

| الحالة | النتيجة المحسوبة | القيمة المرجعية |
|---|---|---|
| ACADS 1(a) — c′=3 kPa, φ′=19.6°, γ=20 kN/m³ | 0.985 | ≈ 0.99 |
| تربة رملية — c′=0, φ′=35°, β=30° | 1.213 | 1.21 (tanφ′/tanβ) |
| البحث الآلي مقابل بحث شامل بالقوة | مطابق | — |

---

## الحدود · Limites · Limitations

- مقطع ثنائي الأبعاد مثالي: لا يمثّل الفوالق ولا الانزلاقات غير الدائرية ولا التعرية البحرية
- ضغط الماء هيدروستاتيكي تحت خط الماء (بدون تدفّق)
- التأثير الزلزالي شبه ساكن
- الوزن الحجمي المُدخل يُطبَّق فوق الماء وتحته

---

## التشغيل · Utilisation · Usage

افتح `index.html` في أي متصفّح حديث. لا يحتاج إلى خادم ولا إلى تثبيت.

Three.js r128 يُحمَّل من CDN عند فتح الأداة الهندسية. إذا تعذّر التحميل أو لم يدعم الجهاز WebGL، تعود الأداة تلقائيًا إلى الرسم ثنائي الأبعاد مع الحسابات نفسها.

---

## المصادر · Sources

- La Presse de Tunisie, Webmanagercenter, Kapitalis, Ultra Tunisia, Jawhara FM — 2024-2026
- وزارة التجهيز والإسكان — بلاغات لجنة قيادة مشروع حماية هضبة سيدي بوسعيد

---

---

**الأستاذة سماح قسومة — مدرّبة دولية ومستشارة جبائية**
**Sameh Gassouma — Formatrice internationale & Conseillère fiscale**
**Sameh Gassouma — International Trainer & Tax Advisor**

TadreebPro.ai · samehgassouma@tadreebpro.ai
