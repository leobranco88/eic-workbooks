/* EIC · gravação das respostas (Firestore, com modo demonstração).
   Para ligar ao Firestore, cole a configuração do projeto em EIC_FIREBASE_CONFIG.
   Sem configuração, tudo fica no localStorage do navegador (serve só para testar). */
(function () {
  var CFG = window.EIC_FIREBASE_CONFIG || null;
  var COLLECTION = 'neural_praticas'; // neural_praticas/{aluna}/respostas/{auto}
  var LS = 'eic_vp2_';
  var fb = null;

  function lsGet(k, d) { try { return JSON.parse(localStorage.getItem(LS + k)) || d; } catch (e) { return d; } }
  function lsSet(k, v) { try { localStorage.setItem(LS + k, JSON.stringify(v)); } catch (e) {} }

  // O Firebase entra sob demanda: se o CDN cair, a página continua funcionando.
  function load() {
    if (fb) return fb;
    var base = 'https://www.gstatic.com/firebasejs/10.14.1/';
    fb = import(base + 'firebase-app.js').then(function (a) {
      return import(base + 'firebase-firestore.js').then(function (f) {
        var app = a.initializeApp(CFG);
        return { db: f.getFirestore(app), f: f };
      });
    });
    return fb;
  }

  function sendPending(aluna) {
    var q = lsGet('pending_' + aluna, []);
    if (!q.length || !CFG) return Promise.resolve();
    lsSet('pending_' + aluna, []);
    return Promise.all(q.map(function (r) { return write(aluna, r); }));
  }

  function write(aluna, rec) {
    return load().then(function (x) {
      return x.f.addDoc(x.f.collection(x.db, COLLECTION, aluna, 'respostas'), rec);
    }).catch(function () {
      var q = lsGet('pending_' + aluna, []);
      q.push(rec);
      lsSet('pending_' + aluna, q);
      throw new Error('offline');
    });
  }

  window.EICStore = {
    mode: CFG ? 'firestore' : 'local',
    save: function (aluna, rec) {
      rec.ts = Date.now();
      if (!CFG) {
        var all = lsGet('log_' + aluna, []);
        all.push(rec);
        lsSet('log_' + aluna, all);
        return Promise.resolve('local');
      }
      return sendPending(aluna).then(function () { return write(aluna, rec); }).then(function () { return 'ok'; });
    },
    watch: function (aluna, cb) {
      if (!CFG) {
        var run = function () { cb(lsGet('log_' + aluna, [])); };
        run();
        window.addEventListener('storage', run);
        return;
      }
      load().then(function (x) {
        var f = x.f;
        var q = f.query(f.collection(x.db, COLLECTION, aluna, 'respostas'), f.orderBy('ts'));
        f.onSnapshot(q, function (snap) {
          cb(snap.docs.map(function (d) { return d.data(); }));
        });
      }).catch(function (e) { console.warn('EIC: sem conexão com o Firestore', e); });
    }
  };
})();
