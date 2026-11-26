# Tokens visuels — رفيق سيدي بوسعيد

| Token | Valeur | Usage |
|---|---|---|
| color.blue.deep | #123A5C | en-tête, barre de navigation, texte principal des bulles guide |
| color.blue | #2E7BB5 | dégradé d'en-tête, accents « vérifié » |
| color.gold | #C9A227 | liseré, bouton d'envoi, contour des bulles guide, badges ⚠ |
| color.gold.soft | #F6EEDA | bandeau UNESCO, fond des bulles guide |
| color.surface | #FAF7F0 | fond des écrans |
| color.user | #E9EBEE | bulles utilisateur |
| color.muted | #5A6570 | textes secondaires |
| radius.card | 18px | cartes, bulles, champ de saisie |
| space.gutter | 16–20px | marge horizontale des écrans |
| font.ar | "Noto Naskh Arabic", "Amiri", serif | tout texte arabe |
| font.latin | system-ui, "Segoe UI", sans-serif | français et anglais |
| pattern.star8 | étoile à huit branches, or 30 % | fond du fil de conversation (AR) |
| pattern.lattice | entrelacs losange + cercle, bleu 22 % | fond du fil de conversation (EN/FR) |

**Note RTL.** Les bulles guide inversent leur coin tronqué (`border-start-start-radius`), l'ordre de la barre
de navigation est retourné, et le bouton d'envoi passe à gauche. Les chiffres et les tarifs restent en
chiffres latins, non inversés.

**Motifs.** Les deux motifs sont dessinés dans les SVG (`<pattern>`), sans image importée ni jeu d'icônes tiers.
