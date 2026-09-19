/* Camada de dados do reforço · EIC
   Projeto eic-worksheets, coleção "reforco". Nada aqui toca outras coleções. */
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-app.js";
import {
  getFirestore, collection, doc, setDoc, getDoc, getDocs, deleteDoc,
  query, where, orderBy, serverTimestamp
} from "https://www.gstatic.com/firebasejs/10.12.2/firebase-firestore.js";

const firebaseConfig = {
  apiKey: "AIzaSyDWXC2LYj4Ksa8ijTvei24EIUmWJ4uILGc",
  authDomain: "eic-worksheets.firebaseapp.com",
  projectId: "eic-worksheets",
  storageBucket: "eic-worksheets.firebasestorage.app",
  messagingSenderId: "671300791274",
  appId: "1:671300791274:web:6cdb2d7348c7f3a14ca093"
};

const app = initializeApp(firebaseConfig);
const db = getFirestore(app);
const COL = "reforco";

/* id curto e legível, para caber no link que vai para a família */
export function novoId() {
  const abc = "abcdefghjkmnpqrstuvwxyz23456789";
  let s = "";
  for (let i = 0; i < 6; i++) s += abc[Math.floor(Math.random() * abc.length)];
  return s;
}

export async function salvarPlano(id, dados) {
  const ref = doc(db, COL, id);
  const antes = await getDoc(ref);
  await setDoc(ref, {
    ...dados,
    criadoEm: antes.exists() ? antes.data().criadoEm : serverTimestamp(),
    atualizadoEm: serverTimestamp()
  }, { merge: true });
  return id;
}

export async function lerPlano(id) {
  const snap = await getDoc(doc(db, COL, id));
  return snap.exists() ? { id: snap.id, ...snap.data() } : null;
}

export async function listarTurma(nivel, checkpoint, turma) {
  let q = query(collection(db, COL),
                where("nivel", "==", nivel),
                where("checkpoint", "==", Number(checkpoint)));
  const snap = await getDocs(q);
  const fora = String(turma || "").trim().toLowerCase();
  return snap.docs
    .map(d => ({ id: d.id, ...d.data() }))
    .filter(p => !fora || String(p.turma || "").trim().toLowerCase() === fora)
    .sort((a, b) => String(a.aluno || "").localeCompare(String(b.aluno || ""), "pt"));
}

export async function listarTurmas(nivel, checkpoint) {
  const snap = await getDocs(query(collection(db, COL),
    where("nivel", "==", nivel), where("checkpoint", "==", Number(checkpoint))));
  const nomes = new Set();
  snap.docs.forEach(d => { const t = (d.data().turma || "").trim(); if (t) nomes.add(t); });
  return [...nomes].sort((a, b) => a.localeCompare(b, "pt"));
}

export async function apagarPlano(id) {
  await deleteDoc(doc(db, COL, id));
}
