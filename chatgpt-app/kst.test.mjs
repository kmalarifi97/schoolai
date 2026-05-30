import { createDiagnostics } from "./kst.js";
const dx = createDiagnostics({ spineDir: "./data/spine" });
let ok = true;
console.log("n_states:", dx._struct.states.length, dx._struct.states.length === 1079 ? "OK" : (ok=false,"MISMATCH"));
const items = [...dx._items.entries()];
const mom = items.filter(([,n]) => n === "Q2305665").slice(0,6).map(([id]) => id);
const grav = items.filter(([,n]) => n === "Q134465").slice(0,4).map(([id]) => id);
const responses = [...grav.map(id=>({item_id:id,correct:true})), ...mom.map(id=>({item_id:id,correct:false}))];
const d = dx.diagnose(responses);
console.log("status:", d.status, "| gap:", d.gap_node, "| slug:", d.slug, "| lesson:", d.lesson, "| pages:", d.book_pages);
console.log("teach_kind:", d.teach_kind, "| note:", (d.note||"").slice(0,80));
const par = d.gap_node==="Q2305665" && d.slug==="momentumcons" && d.lesson==="3-2" && d.book_pages==="74-95";
console.log("PARITY (momentum-weak -> momentumcons/3-2/74-95):", par ? "PASS" : "FAIL");
// full-mastery -> no gap (answer everything correct)
const allRight = items.filter(([,n])=>n).slice(0,40).map(([id])=>({item_id:id,correct:true}));
const d2 = dx.diagnose(allRight);
console.log("all-correct status:", d2.status, "gap:", d2.gap_node);
console.log("suggestNext(empty):", JSON.stringify(dx.suggestNext([]).next_item));
process.exit(par && ok ? 0 : 1);
