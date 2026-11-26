# Brief — رفيق سيدي بوسعيد / Rafik Sidi Bou Saïd

## Promesse
- **AR** — رفيق ثقافي بالذكاء الاصطناعي يجاوبك على تاريخ سيدي بوسعيد وبرنامجها، ويقولّك وقتاش المعلومة ما هيش مؤكّدة.
- **FR** — Un compagnon culturel IA pour Sidi Bou Saïd, qui distingue toujours ce qu'il sait de ce qu'il suppose.
- **EN** — An AI cultural companion for Sidi Bou Saïd that always separates what it knows from what it guesses.

## Personas
1. **Visiteur étranger, 2 heures sur place** — descend du TGM, ne lit pas l'arabe, veut comprendre ce qu'il regarde.
2. **Visiteur tunisien du week-end** — connaît le lieu, cherche le programme culturel du jour et le stationnement.

## Périmètre MVP (5 fonctions)
1. Conversation guidée en 3 langues avec bascule RTL réelle
2. Quatre questions suggérées au démarrage (démarrage à froid résolu)
3. Réponses patrimoine avec **statut de fiabilité affiché** et source
4. Onglet Événements : cartes du jour + carte schématique
5. Entrée vocale **présente mais désactivée**, annoncée comme telle

## Coupé volontairement
Compte utilisateur, paiement, notifications, réservation, géolocalisation réelle, back-office.
Un prototype démontre une idée, pas une infrastructure.

## Stack retenue
Générateur **Python (bibliothèque standard) → page HTML autonome**. Motif : la démo doit s'ouvrir d'un
double-clic, sans installation, sans clé d'API, y compris chez un partenaire non technique. Streamlit aurait
imposé un environnement à installer pour zéro bénéfice à ce stade.

## Données
| Donnée | Statut |
|---|---|
| Histoire du village, décret de 1915, inscription UNESCO | disponible et vérifiable |
| Horaires, tarifs, programme du colloque | **à obtenir de l'organisateur** — simulés et marqués |
| Positions cartographiques | simulées (carte schématique, non géoréférencée) |
