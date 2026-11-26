# فحص المحتوى التونسي — Contrôle culturel

Passage au filtre de chaque élément du brief d'origine. Trois statuts : ✅ مؤكّد · ⚠️ يتطلب تحقق · 🚫 مرفوض.

| Champ | Valeur proposée | Statut | Note |
|---|---|---|---|
| app.name | « REFEK » puis « REFEEK » dans le même texte | 🚫 | Deux graphies pour un seul produit. Retenu : **رفيق سيدي بوسعيد / Rafik Sidi Bou Saïd**, translittération stable dans les trois langues |
| Toponyme | Sidi Bou Saïd | ✅ | Village du gouvernorat de Tunis, sur le promontoire au-dessus de Carthage. Accent circonflexe en français |
| Portes bleues et blanches | « symbolisent… » | ✅ | Décret du **28 août 1915**, obtenu grâce au baron Rodolphe d'Erlanger : protection du village, imposition du bleu et du blanc, interdiction des constructions anarchiques. Formulation corrigée : il s'agit d'une **norme réglementaire**, pas d'un symbolisme spontané |
| Statut patrimonial | absent du brief | ✅ | **Fait majeur manquant** : le village est inscrit sur la Liste du patrimoine mondial de l'UNESCO depuis le **25 juillet 2026** (48e session, Busan), critère culturel (iii), 76,54 ha inscrits + 84,44 ha de zone tampon ; 10e bien tunisien. Ajouté en bandeau permanent |
| Origine du village | absente | ✅ | Sanctuaire du maître soufi Abou Saïd El Beji (XIIe–XIIIe s.), demeures de la bourgeoisie tunisoise au XVIIIe s. |
| « exhibition in the Medina near the main souk » | Sidi Bou Saïd | 🚫 | Sidi Bou Saïd n'a ni médina ni souk principal : c'est un village de ruelles avec des boutiques d'artisanat. La médina à souks est celle de **Tunis**, à ~20 km. Remplacé par « centre du village » |
| « digital art workshop at La Marsa » présenté comme fait | dans 30 min | ⚠️ | La Marsa est une **commune voisine**, pas un quartier de Sidi Bou Saïd : le dire, sinon le visiteur croit marcher 5 minutes. Événement conservé comme démonstration, horaire et lieu marqués |
| Programme du colloque des arts | horaires précis | ⚠️ | Aucun programme public consulté. Champs laissés en `[à confirmer]` plutôt que remplis de valeurs crédibles |
| Tarifs | non renseignés | ⚠️ | `price_tnd: null`. Rappel : le dinar se divise en 1000 millimes — « 3,500 » se lit trois dinars cinq cents |
| « Tunis 2027 » | orientation visuelle | 🚫 | Référence non identifiée à une initiative vérifiable. Retirée : une app ne s'adosse pas à un label dont on ne peut pas citer la source |
| Accessibilité des ruelles | absente | ⚠️ | En **janvier 2026**, des pluies exceptionnelles ont provoqué des glissements et endommagé des façades ; l'état actuel des accès n'est pas confirmé. Mention ajoutée, sans affirmer quel accès est fermé |
| Registre de langue | interface arabe | ✅ | Interface en فصحى ; darija réservée aux réponses conversationnelles courtes (« شنوّة البرنامج متاع اليوم؟ ») — cohérent avec un public local |
| Micro / entrée vocale | icône fonctionnelle | ⚠️ | Présente mais inactive : le prototype le dit explicitement au lieu de laisser croire à une fonction livrée |

## Éléments refusés
- La médina et le souk principal *à Sidi Bou Saïd* (confusion avec Tunis)
- La double graphie REFEK / REFEEK
- L'ancrage « Tunis 2027 »

## À confirmer avant toute mise en production
1. Programme réel du colloque des arts (organisateur)
2. Horaires et tarifs d'Ennejma Ezzahra / CMAM (établissement)
3. État des accès et des ruelles après les intempéries de janvier 2026 (municipalité)
4. Relecture de la darija par un locuteur du Grand Tunis


## Ajout — carte de la Tunisie

| Élément | Statut | Note |
|---|---|---|
| Limites des 24 gouvernorats | ⚠️ | Le jeu Natural Earth 10m n'en contient que **23** : l'Ariana est absente. Signalé dans le pied de carte plutôt que dessiné au jugé |
| Noms arabes des gouvernorats | ✅ | Formes standard (تونس، أريانة، بن عروس، منوبة، نابل…) |
| Noms arabes des 144 localités | 🚫 | Non produits : translittérer 144 toponymes sans source les aurait faussés. Les noms restent dans la graphie GeoNames |
| Populations | ⚠️ | Estimations GeoNames, pas les chiffres de l'INS. Badge affiché sur chaque fiche ville |
| Rattachement ville → gouvernorat | ⚠️ | **Calculé** par test point-dans-polygone, pas recopié d'une source. 138/144 aboutissent ; 6 villes côtières échouent parce que la simplification des contours les rejette à la mer — listées, pas réaffectées à la main |
| Sidi Bou Saïd | ✅ | 10,3417 E / 36,8687 N (GeoNames), gouvernorat de Tunis — cohérent avec le calcul |


## Ajout — plan interactif de Sidi Bou Saïd

| Élément | Statut | Note |
|---|---|---|
| Existence et position des 8 repères | ✅ | Vérifiés un par un (recherche de lieux Google Places) : station TGM, Dar El Annabi, Café des Nattes, mosquée du village, phare, Ennejma Ezzahra, Café Sidi Chabaane, port de plaisance |
| Positions sur le plan | ⚠️ | **Positions relatives réelles** (écart maximal 855 m × 603 m, parcours ≈ 1 740 m), posées sur un **fond dessiné**. Le plan n'est pas géoréférencé et ne doit pas servir à naviguer |
| Horaires, tarifs, ouverture au public | ⚠️ | Aucun affiché comme certain. Chaque fiche porte sa réserve (ex. « ouverture du phare au public non confirmée ») |
| « Mausolée de Sidi Bou Saïd » | 🚫 | Deux résultats de recherche renvoyaient vers **Sidi Boughaba au Maroc** et la **zaouïa de Sidi Sahab à Kairouan** — écartés. Seule la mosquée du village a été retenue |
| Café Sidi Chabaane / des Délices | ✅ | Lieu confirmé ; réserve ajoutée sur les prix, signalés comme élevés par les visiteurs |
| Tracé des ruelles | ⚠️ | Dessiné, pas relevé. Signalé sous le plan : « positions relatives réelles, fond non géoréférencé » |


## Ajout — périmètre UNESCO

| Élément | Statut | Note |
|---|---|---|
| Date, session, critère | ✅ | 25 juillet 2026, 48e session (Busan), critère culturel **(iii)** — témoignage exceptionnel sur une tradition culturelle. Bien n° 1769 |
| Superficies | ✅ | Cœur inscrit **76,54 ha**, zone tampon **84,44 ha** |
| Tracé du périmètre | ⚠️ | **Non disponible.** Les deux cercles affichés ont la *surface exacte* (rayon équivalent : 494 m pour le cœur, 716 m cœur + tampon) mais **ne sont pas la limite officielle** — dit explicitement sur la fiche |
| Étendue | ✅ | Le périmètre couvre le **seul cœur historique**, plus petit que le territoire communal. Précision reprise dans les trois pages : une inscription ne protège pas toute la commune |
| Motif de sélection | ✅ | Village formé autour du tombeau du saint soufi ; légitimité des dynasties adossée à sa baraka dès le XVIe s. ; villégiatures des beys husseinites et des grandes familles de Tunis aux XVIIIe–XXe s. |
| Dossier | ✅ | Déposé en février 2024, ministère des Affaires culturelles + INP, sous le titre « Le village de Sidi Bou Saïd : hub d'inspiration culturelle et spirituelle en Méditerranée » |
| Éléments immatériels | ⚠️ | **Malouf, Issaouia, jasmin, kharja de la nuit du Mouled ne sont pas classés individuellement** par cette décision. Précisé dans la réponse du chat, pour couper court à un raccourci fréquent |
| Rang | ✅ | 10e bien tunisien : 9 culturels + 1 naturel (parc national de l'Ichkeul) |


## Ajout — réservation de table en terrasse 3D

| Élément | Statut | Note |
|---|---|---|
| Établissements | ✅ | Café des Nattes et Café Sidi Chabaane existent et sont déjà vérifiés dans le parcours |
| Plan de salle, nombre de tables, prises électriques | 🚫→⚠️ | **Entièrement simulé.** 17 tables, 8 avec prise : c'est un modèle de démonstration, pas le relevé des salles réelles. Écrit sous chaque écran |
| Disponibilité et affluence | ⚠️ | Aucune donnée d'occupation réelle. La maquette ne prétend pas savoir si une table est libre |
| Prix | 🚫 | Aucun tarif affiché. Le menu porte les temps de préparation, pas des prix inventés en TND. Message explicite : les tarifs viennent de l'établissement |
| Transmission de la réservation | ⚠️ | **Rien n'est envoyé.** La page le dit à chaque étape : sans accord de l'établissement, une confirmation ferait croire à une table réservée qui ne l'est pas |
| Temps de préparation | ⚠️ | Valeurs plausibles par boisson (3 à 6 min) + marge du lieu. À caler avec le gérant avant tout usage réel |
| Cartes et boissons | ✅ | Café arabe, capucin, thé aux pignons, bambalouni — carte tunisienne courante, pas de plat inventé |


## Ajout — WhatsApp et écran cuisine

| Élément | Statut | Note |
|---|---|---|
| Numéro WhatsApp des cafés | 🚫→⚠️ | **Aucun numéro n'est écrit dans l'application.** Le champ est vide et se saisit par l'établissement ; l'envoi est bloqué tant que moins de 8 chiffres sont entrés. Inventer un +216 aurait envoyé de vraies commandes chez un inconnu |
| Envoi de la commande | ⚠️ | Le lien `wa.me` **ouvre** WhatsApp avec le message pré-rempli ; c'est la personne qui appuie sur envoyer. Rien ne part automatiquement |
| Circulation vers la cuisine | ⚠️ | `BroadcastChannel` entre fenêtres du même navigateur, plus un code à coller en secours. **Pas de serveur, pas de base** : deux appareils distincts ne communiquent pas |
| Persistance des tickets | ⚠️ | Uniquement en mémoire : fermer l'écran cuisine efface les commandes. Assumé pour une maquette, à remplacer par un vrai back-end en production |
| Temps de préparation affichés en cuisine | ⚠️ | Repris du minutage client (3 à 6 min par boisson + marge). À caler avec le gérant |


## Ajout — backend Supabase

| Élément | Statut | Note |
|---|---|---|
| URL et clé anon | 🚫→⚠️ | **Aucune n'est écrite dans les fichiers.** Champs vides, saisis par l'exploitant, gardés en mémoire le temps de la session. Sans eux, les pages restent en mode local |
| Schéma SQL | ✅ | `prototype/db/schema.sql`, exécutable tel quel : table, index sur `start_at`, RLS, trois policies, publication realtime |
| Sécurité | ⚠️ | **Dit en clair dans l'interface** : la clé anon est publique dès qu'elle est dans une page HTML ; le schéma limite lecture et mise à jour aux 6 dernières heures, mais un déploiement réel doit authentifier l'écran cuisine |
| Instance testée | ⚠️ | Aucune instance Supabase n'a été contactée depuis cet environnement (réseau restreint). L'adaptateur a été testé contre un serveur simulé : URL, en-têtes, corps, relecture, changement d'état, retour en mode local sur clé invalide |
| Realtime | ⚠️ | La publication est dans le schéma, mais les pages fonctionnent par sondage (5 s) pour ne dépendre d'aucune bibliothèque externe |


## Ajout — les deux salles rendues séparément

| Élément | Statut | Note |
|---|---|---|
| Café des Nattes — escalier raide, terrasse en haut | ✅ | Documenté de façon concordante : on gravit de hautes marches avant d'atteindre la terrasse, qui donne sur la rue principale et la placette |
| — porte jaune et noire | ✅ | Décrite par plusieurs sources ; reproduite en façade |
| — nattes et doukkanas | ✅ | Banquettes maçonnées garnies de nattes : c'est ce qui donne son nom au café. Matière tressée dessinée au canvas |
| — colonnade torsadée rouge et verte, plafond à solives | ✅ | Décrite explicitement ; texture de colonne peinte en bandes spiralées à liseré blanc |
| — ancienne entrée de la mosquée, soirées de malouf | ✅ | Repris dans la fiche du lieu |
| Café Sidi Chabaane — terrasses en gradins sur la falaise | ✅ | Vue sur la marina et le golfe ; ouvert vers la fin des années 1960 |
| — prix élevés | ⚠️ | Signalés par les visiteurs. Affiché comme mise en garde, sans chiffre |
| Nombre et disposition des tables | ⚠️ | **Estimation dans les deux cas.** 17 tables aux Nattes, 18 à Sidi Chabaane : plausible, pas relevé. Écrit sous l'écran de choix |
| Emplacement des prises électriques | ⚠️ | Entièrement simulé. Aucune source ne documente les prises d'un café |


## Ajout — entrée, golfe et marina du Café des Délices

| Élément | Statut | Note |
|---|---|---|
| Entrée par le haut, descente vers les terrasses | ✅ | Cohérent avec les descriptions : le café s'ouvre en hauteur et ses terrasses descendent la falaise |
| Portail bleu, murs blancs, bougainvilliers | ✅ | Palette et végétation du village, déjà validées |
| Enseigne | ⚠️ | Panneau **vierge** : ni logo ni nom peint. Reproduire une enseigne réelle serait reprendre une identité visuelle qui ne nous appartient pas |
| Vue sur la marina et le golfe | ✅ | C'est l'argument même du lieu, documenté partout |
| Bateaux amarrés (16), pontons, digue, feu de port | ⚠️ | **Composition plausible, pas un relevé du port.** Le nombre de bateaux, leur type et leur place ne correspondent à aucune photo précise |
| Relief au loin | ⚠️ | Silhouettes de cap et de montagne évoquant l'autre rive du golfe. Volontairement floues et sans nom affiché : la vue exacte depuis chaque terrasse n'a pas été vérifiée |
