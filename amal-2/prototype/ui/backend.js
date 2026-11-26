/* Transport des commandes — deux modes, une seule interface.

   local : BroadcastChannel, instantané, limité aux fenêtres d'un même navigateur.
   cloud : appels REST directs (PostgREST / Supabase) + sondage. Pas de bibliothèque
           externe, donc aucune dépendance CDN : la page reste autonome.

   Le passage de l'un à l'autre se fait en saisissant l'URL et la clé ; sans elles,
   on reste en local. Rien n'est stocké : la configuration vit le temps de la session. */
window.makeBackend = function (cfg) {
  const state = {
    mode: "local",
    url: (cfg && cfg.url) || "",
    key: (cfg && cfg.anon_key) || "",
    table: (cfg && cfg.table) || "orders",
    poll: ((cfg && cfg.poll_seconds) || 5) * 1000,
    lastSync: null,
    timer: null
  };

  let channel = null;
  try { channel = new BroadcastChannel((cfg && cfg.channel) || "kds-sbs"); } catch (err) { channel = null; }

  function endpoint(qs) {
    return state.url.replace(/\/+$/, "") + "/rest/v1/" + state.table + (qs ? "?" + qs : "");
  }

  function headers(extra) {
    const h = {
      "apikey": state.key,
      "Authorization": "Bearer " + state.key,
      "Content-Type": "application/json"
    };
    if (extra) Object.keys(extra).forEach(function (k) { h[k] = extra[k]; });
    return h;
  }

  /* ---------- conversion ticket <-> ligne ---------- */
  function toRow(tk) {
    return {
      venue_id: tk.v, venue_name: tk.vname, table_id: tk.table,
      items: tk.items, prep_min: tk.prep,
      start_at: new Date(tk.start).toISOString(),
      ready_at: new Date(tk.ready).toISOString(),
      arrival_at: new Date(tk.arrival).toISOString(),
      state: tk.state || "todo"
    };
  }

  function fromRow(r) {
    return {
      id: r.id, v: r.venue_id, vname: r.venue_name, table: r.table_id,
      items: r.items, prep: r.prep_min,
      start: Date.parse(r.start_at), ready: Date.parse(r.ready_at),
      arrival: Date.parse(r.arrival_at),
      state: r.state, ts: Date.parse(r.created_at || r.start_at)
    };
  }

  /* ---------- API ---------- */
  return {
    get mode() { return state.mode; },
    get lastSync() { return state.lastSync; },

    /** Essaie la configuration donnée ; ne bascule en cloud que si l'appel répond. */
    connect: function (url, key) {
      state.url = (url || "").trim();
      state.key = (key || "").trim();
      if (!state.url || !state.key) {
        state.mode = "local";
        return Promise.reject(new Error("URL / key"));
      }
      return fetch(endpoint("select=id&limit=1"), { headers: headers() })
        .then(function (r) {
          if (!r.ok) return r.text().then(function (txt) {
            throw new Error(r.status + " " + (txt || r.statusText).slice(0, 140));
          });
          state.mode = "cloud";
          state.lastSync = Date.now();
          return true;
        })
        .catch(function (e) { state.mode = "local"; throw e; });
    },

    /** Dépose une commande. En local, elle part sur le canal ; en cloud, elle est écrite. */
    send: function (ticket) {
      if (channel) channel.postMessage({ type: "order", ticket: ticket });
      if (state.mode !== "cloud") return Promise.resolve({ mode: "local" });
      return fetch(endpoint(), {
        method: "POST",
        headers: headers({ "Prefer": "return=representation" }),
        body: JSON.stringify(toRow(ticket))
      }).then(function (r) {
        if (!r.ok) return r.text().then(function (txt) {
          throw new Error(r.status + " " + (txt || r.statusText).slice(0, 140));
        });
        state.lastSync = Date.now();
        return r.json().then(function (rows) {
          return { mode: "cloud", row: rows && rows[0] ? fromRow(rows[0]) : null };
        });
      });
    },

    /** Fait avancer l'état d'un ticket déjà écrit côté serveur. */
    setState: function (id, newState) {
      if (state.mode !== "cloud" || !id) return Promise.resolve(false);
      return fetch(endpoint("id=eq." + encodeURIComponent(id)), {
        method: "PATCH",
        headers: headers(),
        body: JSON.stringify({ state: newState })
      }).then(function (r) { state.lastSync = Date.now(); return r.ok; });
    },

    /** Commandes du service en cours, les plus urgentes d'abord. */
    fetchRecent: function () {
      if (state.mode !== "cloud") return Promise.resolve([]);
      return fetch(endpoint("select=*&state=neq.cancelled&order=start_at.asc&limit=80"),
                   { headers: headers() })
        .then(function (r) {
          if (!r.ok) throw new Error(r.status + " " + r.statusText);
          return r.json();
        })
        .then(function (rows) {
          state.lastSync = Date.now();
          return rows.map(fromRow);
        });
    },

    /** Écoute : canal local en direct, et sondage régulier quand le cloud est actif. */
    subscribe: function (onTicket, onList) {
      if (channel) {
        channel.onmessage = function (e) {
          if (e.data && e.data.type === "order") onTicket(e.data.ticket);
        };
      }
      const self = this;
      if (state.timer) clearInterval(state.timer);
      state.timer = setInterval(function () {
        if (state.mode !== "cloud") return;
        self.fetchRecent().then(onList).catch(function () { /* réseau instable : on réessaie */ });
      }, state.poll);
    },

    stop: function () { if (state.timer) clearInterval(state.timer); }
  };
};
