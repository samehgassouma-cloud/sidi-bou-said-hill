# Journal de l'équipe — رفيق سيدي بوسعيد

**🧭 وكيل التحليل.** Le brief demandait un rendu d'écran unique. J'en ai fait un périmètre en 5 fonctions et
j'ai coupé compte, paiement, notifications et réservation. Stack : générateur Python → HTML autonome, pour que
la démo s'ouvre sans installation. → `docs/brief.md`

**🎨 وكيل التصميم.** Trois écrans, un fichier SVG chacun : conversation AR (RTL), conversation EN (LTR),
événements. Les deux motifs géométriques sont dessinés dans les SVG, aucune icône importée. J'ai prévu deux
maquettes de conversation parce que le passage à l'arabe change l'ordre de lecture, pas seulement la police.
→ `design/*.svg`, `design/tokens.md`

**🏛️ وكيل الثقافة.** Trois refus. Le « souk principal » n'existe pas à Sidi Bou Saïd — c'est la médina de Tunis.
La double graphie REFEK/REFEEK devait être tranchée. « Tunis 2027 » n'est rattaché à aucune source vérifiable.
Et un ajout : l'inscription UNESCO du 25 juillet 2026 manquait alors qu'elle est le fait central du lieu
aujourd'hui. Horaires et tarifs passent tous en ⚠️. → `docs/culture-check.md`

**💻 وكيل البرمجة.** Aucun texte visible dans le code : 24 clés × 3 langues. Le statut `verified` des données
remonte jusqu'au badge affiché dans la bulle. RTL traité par `dir` sur `<html>`, propriétés logiques CSS et
inversion explicite de la barre de navigation. → `prototype/`

**✅ وكيل الجودة.** Contrôle passé : parité i18n, aucune chaîne en dur, 5 SVG séparés sans référence externe,
tous les enregistrements portent leur statut. Reste à tester sur un vrai écran mobile et à faire relire la
darija par un locuteur du Grand Tunis. → `docs/rapport.md`

## Itération 2 — نسخة Pop-up 3D

**🎨 وكيل التصميم.** Quatre scènes, un décor SVG dessiné par scène (village, porte cloutée, coupole, cartes
d'événements). Le livre s'ouvre par une couverture, les cartes se relèvent depuis `rotateX(72deg)`.

**💻 وكيل البرمجة.** Architecture « 3D optionnel » : moteur CSS d'abord, Three.js r128 chargé dynamiquement
avec `degrade()` en cas d'échec — le bouton se désactive et la page annonce le repli. Caméra sphérique
maison, aucune OrbitControls, aucune CapsuleGeometry, écouteurs `passive`, `prefers-reduced-motion` géré.
Le contenu vient des mêmes `i18n/` et `data/` que la version chat : une seule source de vérité.

**🏛️ وكيل الثقافة.** Rien de neuf à refuser : les quatre scènes réutilisent des fiches déjà statuées.
La scène « programme » reste entièrement ⚠, y compris en 3D.


## Itération 3 — diorama cinématique

**🎨 وكيل التصميم.** Cinq plans, un par scène, avec une lumière propre à chacun : dorée sur le panorama,
plus chaude en gros plan sur la porte, rasante sur la zaouïa. Les matières (chaux, porte cloutée, zellige,
mer) sont peintes au canvas pour rester originales et sans dépendance.

**💻 وكيل البرمجة.** Première version : 1 105 objets à dessiner — trop pour un téléphone. Repassé le village
et la végétation en `InstancedMesh` : 112 appels de rendu, ~46 000 triangles, même densité visuelle
(60 maisons, 26 cyprès, 34 buissons). Le repli CSS reste intact : sans WebGL, la page garde ses cinq scènes.

**🏛️ وكيل الثقافة.** Contrôle du diorama : coupole et minaret séparés (le mausolée n'est pas une mosquée
à minaret unique collé), portes cloutées à motif d'étoile, bougainvilliers et cyprès conformes au paysage.
La scène « programme » garde son ⚠ : bannières et lanternes sont un décor, pas un événement attesté.


## Itération 4 — patio enrichi, fiche masquable, médias

**🎨 وكيل التصميم.** Le patio d'Ennejma Ezzahra est repris de zéro : quatre galeries de cinq colonnes
(base, fût, chapiteau doré), quatre arcades par côté, soubassement de zellige, poutraison de bois,
garde-corps du niveau haut, lanternes suspendues, quatre orangers et une fontaine octogonale à six jets
avec ondes concentriques. La fiche de texte se ferme pour libérer la vue.

**💻 وكيل البرمجة.** Trois surfaces d'affichage reçoivent les médias de l'utilisateur (écran de la place,
deux cadres de la galerie). Image animée → redessinée dans un canvas à chaque frame ; vidéo → `VideoTexture`
avec reprise au premier geste si l'autoplay est refusé. Un bug attrapé au test : la fonction de cadre
s'appelait `frame()`, comme la boucle de rendu — la déclaration tardive écrasait l'autre et la boucle
démarrait avant l'initialisation des variables. Renommée `mediaFrame()`.

**✅ وكيل الجودة.** 140 objets, ~48 500 triangles. Les trois chemins médias testés hors navigateur :
WebP animé, image fixe, vidéo avec autoplay refusé.


## Itération 5 — carte de la Tunisie

**🧭 وكيل التحليل.** Pas d'image de carte en entrée : il fallait des données réelles, pas une vision.
Sources retenues : Natural Earth 10m (limites) et GeoNames (localités), toutes deux librement réutilisables.

**💻 وكيل البرمجة.** Rendu SVG maison plutôt qu'une bibliothèque de tuiles : zéro dépendance réseau, et la
carte s'ouvre hors ligne comme les deux autres pages. Bug corrigé au passage : la simplification
Douglas-Peucker réduisait chaque contour fermé à deux points, parce que le segment de référence d'un anneau
est dégénéré (extrémités confondues) — la distance se mesure alors au point de départ. Contours passés de
2 à 1 453 points.

**🏛️ وكيل الثقافة.** Trois manques déclarés en pied de carte au lieu d'être comblés : gouvernorat de
l'Ariana absent de la source, six villes côtières hors contours simplifiés, populations non officielles.
Refus de translittérer 144 toponymes en arabe sans source.


## Itération 6 — plan de village

**🏛️ وكيل الثقافة.** Cette fois les positions sont vérifiées lieu par lieu avant d'être dessinées. Deux
résultats de recherche pointaient hors sujet — un mausolée au Maroc, une zaouïa à Kairouan — écartés plutôt
que placés « à peu près ». Le fond de plan reste déclaré schématique : dessiner des ruelles au jugé et les
présenter comme une carte serait exactement l'erreur que ce projet évite depuis le début.

**🎨 وكيل التصميم.** Le vol d'entrée réutilise le contour Natural Earth déjà présent dans le projet : on
part de la carte nationale et on plonge, sans rupture. Les repères reprennent la mécanique des plats du
menu 3D : médaillon circulaire, cerclage doré, relevé depuis `rotateX(58deg)`.

**💻 وكيل البرمجة.** Huit illustrations SVG originales (train, maison, café, coupole, phare, palais,
terrasses, barque), révélation progressive liée à l'étape, tracé du parcours qui se dore au fur et à mesure,
mode parcours automatique et navigation au clavier. Les trois cartes sont reliées : pays → village → diorama.


## Itération 7 — périmètre UNESCO

**🏛️ وكيل الثقافة.** Le tracé officiel du périmètre n'est pas publié dans ce qui a été consulté. Deux options :
inventer un contour plausible, ou représenter la **surface exacte** par un cercle équivalent et le dire. Retenu :
la seconde, avec la mention en clair sur la fiche. Ajouté aussi la précision que le classement porte sur le cœur
historique et non sur toute la commune, et que le malouf, l'Issaouia, le jasmin et la kharja du Mouled ne sont pas
classés individuellement — deux raccourcis fréquents.

**💻 وكيل البرمجة.** Les rayons équivalents (494 m et 716 m) sont recalculés depuis les hectares, pas saisis à la
main, et convertis en pourcentages du plan séparément en X et en Y puisque le fond est étiré. La fiche UNESCO est
partagée par les trois pages via `data/unesco.json` : une seule source pour la carte, le plan et le chat.


## Itération 8 — réservation de table

**🧭 وكيل التحليل.** La demande contient quatre promesses : choisir sa table, choisir sa place électrique,
commander à l'avance, et arriver quand c'est prêt. Retenu tel quel, sauf le paiement et l'envoi réel de la
commande — sans accord des établissements, ça ferait croire à une réservation qui n'existe pas.

**🎨 وكيل التصميم.** Terrasse en gradins, comme la vraie topographie du lieu : trois niveaux vers la mer plus
une salle intérieure. La prise électrique n'est pas une ligne de texte mais un halo turquoise pulsant sous la
table — l'information se lit sans lire.

**💻 وكيل البرمجة.** Sélection au Raycaster sur un disque invisible par table (d'où des maillages
individuels plutôt qu'instanciés). Le minutage se calcule à rebours depuis l'arrivée ; testé hors navigateur
sur quatre cas, dont un délai volontairement trop court pour vérifier que l'alerte se déclenche. Repli sans
WebGL : le plan de salle devient une grille de boutons, la réservation reste possible.

**🏛️ وكيل الثقافة.** Carte tunisienne courante (قهوة عربي، كابوسان، تاي بالصنوبر، بمبالوني), aucun prix
affiché, et mention permanente que salle, disponibilités et affluence sont simulées.


## Itération 9 — transmission

**💻 وكيل البرمجة.** Trois voies, par ordre de robustesse décroissante : WhatsApp (fonctionne partout, mais
demande un numéro), BroadcastChannel (instantané, limité aux fenêtres d'un même navigateur), code encodé en
base64 (dernier recours, marche par copier-coller y compris entre appareils). Le ticket encodé a été testé en
aller-retour, arabe compris. L'écran cuisine ne touche à aucun stockage local : tout est en mémoire, ce qui
évite d'introduire une persistance qui ne survivrait pas au premier vrai déploiement.

**🏛️ وكيل الثقافة.** Un point ferme : le champ du numéro WhatsApp reste **vide**, et l'envoi est bloqué
sous 8 chiffres. Un +216 inventé aurait dirigé de vraies commandes vers un inconnu — c'est la version
téléphonique du faux tarif refusé depuis le début du projet.

**✅ وكيل الجودة.** Testé hors navigateur : aller-retour du code (arabe préservé), refus du numéro vide,
tri de l'écran cuisine avec un ticket en retard qui remonte en tête, absence de localStorage.


## Itération 10 — backend

**💻 وكيل البرمجة.** Adaptateur unique (`ui/backend.js`) avec deux transports derrière la même interface :
BroadcastChannel et REST PostgREST. Choix d'appeler l'API en `fetch` brut plutôt que via la bibliothèque
Supabase : aucune dépendance CDN, donc les pages restent autonomes comme le reste du projet. Le sondage à
5 s remplace le Realtime pour la même raison. Testé contre un serveur simulé, puis en chaîne complète —
café écrit, cuisine relit, état renvoyé, fusion sans doublon.

**🏛️ وكيل الثقافة.** Deux refus dans la même ligne : pas d'URL, pas de clé dans les fichiers livrés. Et une
mise en garde affichée, pas enterrée dans la doc : une clé anon dans une page HTML est publique. Le schéma
limite déjà la casse (6 heures glissantes), mais le dire vaut mieux que le laisser découvrir.

**✅ وكيل الجودة.** Aucune instance réelle n'a pu être contactée depuis cet environnement — c'est écrit dans
le contrôle culturel plutôt que présenté comme un test réussi.


## Itération 11 — chaque café dans sa salle

**🏛️ وكيل الثقافة.** Avant de modéliser, relevé de ce que les sources décrivent réellement : hautes marches,
porte jaune et noire, nattes et doukkanas, colonnes torsadées rouge et vert à liseré blanc, plafond à
solives, ancienne entrée de la mosquée pour les Nattes ; terrasses en gradins, marina, ouverture fin des
années 1960 et prix élevés pour Sidi Chabaane. Ce qui n'est pas documenté — nombre de tables, prises — reste
marqué comme estimé, sous les yeux de l'utilisateur et non en note de bas de page.

**🎨 وكيل التصميم.** Deux matières nouvelles peintes au canvas : la natte tressée et la colonne à bandes
spiralées. Dans la salle, tables basses et assises sur doukkanas ; sur la falaise, tabourets bleus et
parasols. La caméra ne démarre pas au même endroit : face à la salle aux Nattes, face à la mer à Sidi
Chabaane.

**💻 وكيل البرمجة.** Bug corrigé : la scène était construite une seule fois, donc changer de café ne changeait
que la liste des tables. Le canvas est désormais remplacé et la scène reconstruite. Vérifié avec le vrai
Three.js : 207 objets / ~16 000 triangles aux Nattes, 175 / ~17 200 à Sidi Chabaane.


## Itération 12 — l'entrée et le port

**🎨 وكيل التصميم.** La scène raconte maintenant l'arrivée : on entre par le haut, on descend, la vue
s'ouvre. C'est la séquence réelle du lieu, et elle donne son sens aux quatre niveaux de terrasses qui
n'étaient jusque-là que des plateaux.

**💻 وكيل البرمجة.** Seize bateaux composés de pièces simples (coque, liston bleu, roof, mât, bôme, voile
ferlée), animés par un déphasage propre à chacun. Test dédié avec horloge simulée : amplitude verticale
0,31 m de houle, dérive horizontale nulle — ils bougent sans quitter leur place, ce qui est exactement le
comportement attendu d'un bateau amarré. Scène passée de 175 à 321 objets, ~18 900 triangles.

**🏛️ وكيل الثقافة.** L'enseigne reste vierge : peindre le nom et le graphisme d'un établissement, c'est
reprendre son identité visuelle. Et le port est déclaré comme composition, pas comme relevé — même règle que
pour le plan de salle.
