# التحقّق من الحساب · Vérification du calcul · Calculation check

محرّك `prototype/ui/bishop.js` — طريقة Bishop المبسّطة، دوائر انزلاق، 30 شريحة، بحث آلي على
شبكة مراكز ثم تنقيح محلّي.

Moteur `prototype/ui/bishop.js` — Bishop simplifiée, cercles de glissement, 30 tranches,
recherche sur grille de centres puis raffinement local.

---

## الحالات المرجعية · Cas de référence · Reference cases

| الحالة · Cas | المعطيات · Données | المحسوب | المرجع |
|---|---|---|---|
| ACADS 1(a) | H = 10 م، ميل 2:1 (26.565°)، c′ = 3 kPa، φ′ = 19.6°، γ = 20 kN/m³، جاف | **0.985** | ≈ 0.99 |
| تربة رملية · sol pulvérulent | c′ = 0، φ′ = 35°، β = 30°، جاف | **1.213** | 1.213 = tan φ′ ⁄ tan β |
| البحث الآلي · recherche automatique | معطيات العمل الافتراضية | مطابق | بحث شامل بالقوة على xc, yc, R |

الحالة الثانية حلّها النظري مغلق: في المنحدر اللانهائي بتربة بلا تماسك، معامل الأمان يساوي
`tan φ′ / tan β` ولا يتعلّق بالارتفاع ولا بالوزن الحجمي.

Le deuxième cas a une solution analytique fermée : dans une pente infinie en sol pulvérulent,
le coefficient vaut `tan φ′ / tan β`, indépendamment de la hauteur et du poids volumique.

---

## القيم الافتراضية للعمل · Valeurs par défaut · Default values

من `prototype/data/defaults.json` — **أمثلة، وليست معطيات هضبة سيدي بوسعيد.**

| | |
|---|---|
| H = 30 م · β = 30° | zw = 15 م · q = 50 kPa على عرض 12 م، 3 م من الحافة |
| الطبقة 1 | القاع 20 م · γ = 19 · c′ = 12 kPa · φ′ = 28° |
| الطبقة 2 | القاع 5 م · γ = 20 · c′ = 20 kPa · φ′ = 24° |
| القاعدة الصلبة | القاع −10 م · γ = 22 · c′ = 50 kPa · φ′ = 34° |

| الناتج | القيمة |
|---|---|
| معامل الأمان الساكن · statique | 1.291 |
| معامل الأمان الزلزالي (kh = 0.10) · sismique | 1.052 |
| الدائرة الحرجة · cercle critique | المركز (14.8 ، 58.9) م · نصف القطر 53.9 م |

القيم المرجعية الشائعة في الممارسة: **1.5** للحالة الساكنة طويلة المدى و**1.1** للحالة الزلزالية.
فالمثال الافتراضي أعلاه **لا يستوفي** الهامش الساكن. تحقّق من المعيار المعتمد (مثل Eurocode 7).

---

## إعادة التحقّق · Refaire la vérification · Re-run the check

```bash
node -e "
var CFG={slices:30,targets:{static:1.5},search:{gridSide:18,seeds:4,refineRounds:4,radiiCoarse:24,radiiFine:40}};
$(cat prototype/ui/bishop.js)
const mk=(H,b,c,phi,g)=>makeModel({H,beta:b,layers:[{bot:-H,g,c,phi}],zw:-99,kh:0,q:0,qd:0,qB:0});
console.log('ACADS 1(a):', search(mk(10,26.565,3,19.6,20),0).best.F.toFixed(3));
console.log('c=0 phi=35 b=30:', search(mk(20,30,0,35,20),0).best.F.toFixed(3));
"
```

---

## ما لا يغطّيه التحقّق · Hors périmètre · Out of scope

- الفوالق والكسور، وهي كثيرة في صخور الهضبة الطينية والرملية
- أسطح الانزلاق غير الدائرية (الطرية، المركّبة)
- التعرية البحرية التي تنحت قاعدة الجرف
- التدفّق والضغط العابر (consolidation, écoulement transitoire)
- الثبات ثلاثي الأبعاد الحقيقي: الحساب على مقطع لكل متر طول

لهذا تبقى النتيجة **تقديرية وغير معتمدة**، ولا تُغني عن الدراسة الجيوتقنية الميدانية الجارية.
