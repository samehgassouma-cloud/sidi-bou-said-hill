-- شاشة المطبخ — schéma minimal pour faire circuler les commandes entre appareils.
-- À exécuter dans l'éditeur SQL de Supabase (ou tout PostgreSQL avec PostgREST).

create table if not exists public.orders (
  id          bigint generated always as identity primary key,
  venue_id    text        not null,
  venue_name  text        not null,
  table_id    text        not null,
  items       jsonb       not null,              -- [{id, q, n:{ar,fr,en}}]
  prep_min    int         not null default 0,
  start_at    timestamptz not null,              -- heure de lancement en cuisine
  ready_at    timestamptz not null,              -- commande prête
  arrival_at  timestamptz not null,              -- arrivée annoncée du client
  state       text        not null default 'todo'
              check (state in ('todo','doing','ready','served','cancelled')),
  created_at  timestamptz not null default now()
);

-- L'écran cuisine trie par heure de lancement : c'est cet index qui compte.
create index if not exists orders_start_idx on public.orders (start_at);
create index if not exists orders_created_idx on public.orders (created_at desc);

alter table public.orders enable row level security;

-- Le client anonyme peut déposer une commande…
drop policy if exists orders_insert_anon on public.orders;
create policy orders_insert_anon on public.orders
  for insert to anon with check (true);

-- …et ne lire que le service en cours (6 heures), jamais l'historique complet.
drop policy if exists orders_select_recent on public.orders;
create policy orders_select_recent on public.orders
  for select to anon using (created_at > now() - interval '6 hours');

-- L'écran cuisine fait avancer l'état des commandes récentes.
drop policy if exists orders_update_recent on public.orders;
create policy orders_update_recent on public.orders
  for update to anon
  using (created_at > now() - interval '6 hours')
  with check (created_at > now() - interval '6 hours');

-- Realtime (facultatif : l'application interroge aussi par sondage).
alter publication supabase_realtime add table public.orders;

-- ⚠ Limite assumée : avec la seule clé anon, n'importe qui connaissant l'URL peut lire
-- les commandes des 6 dernières heures et modifier leur état. Pour un déploiement réel,
-- authentifier l'écran cuisine (rôle "staff") et restreindre update/select à ce rôle.
