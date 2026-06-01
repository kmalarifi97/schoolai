// Smoke test: exercise the schema + store directly (no HTTP), so we can verify
// traversal and diagnosis logic in isolation. Run: npm run smoke
import { graphql } from "graphql";
import { join } from "node:path";
import { fileURLToPath } from "node:url";
import { createGraphStore } from "./graphStore.mjs";
import { buildSchema } from "./schema.mjs";

const ROOT = join(fileURLToPath(new URL(".", import.meta.url)), "..");
const store = createGraphStore(join(ROOT, "graph", "seed.graph.json"));
const schema = buildSchema(store);
const run = (query, variables) => graphql({ schema, source: query, variableValues: variables });

let failures = 0;
const check = (label, cond, detail) => {
  console.log(`${cond ? "PASS" : "FAIL"}  ${label}${detail ? "  — " + detail : ""}`);
  if (!cond) failures++;
};

console.log("=== cycles (expect none) ===");
const cyc = await run(`{ cycles }`);
check("graph is a DAG", cyc.data.cycles.length === 0, JSON.stringify(cyc.data.cycles));

console.log("\n=== recursive prerequisites of work_energy ===");
const pre = await run(`{ skill(id:"work_energy"){ name prerequisites(recursive:true){ id } } }`);
const ids = pre.data.skill.prerequisites.map((p) => p.id);
console.log(ids.join(" -> "));
check("work_energy depends on kinematics (transitively)", ids.includes("kinematics"));
check("work_energy depends on functions (deep root)", ids.includes("functions"));

console.log("\n=== diagnose: student failed work_energy & forces, passed kinematics ===");
const diag = await run(
  `query($p:[ID!]!,$f:[ID!]!){ diagnose(passed:$p, failed:$f){
     summary
     failed { skill{name} rootCause{id name} recommendation
              notMastered { skill{id} status depth } } } }`,
  { p: ["kinematics", "derivatives", "vectors"], f: ["work_energy", "forces"] }
);
console.log(JSON.stringify(diag.data.diagnose, null, 2));
const we = diag.data.diagnose.failed.find((f) => f.skill.name.startsWith("Work"));
// forces is failed and is the nearest unmet prerequisite of work_energy -> root cause
check("work_energy root cause is forces", we?.rootCause?.id === "forces", we?.rootCause?.id);
check("passed prerequisites are NOT flagged", !we.notMastered.some((n) => n.skill.id === "kinematics"));

console.log(`\n${failures === 0 ? "ALL PASS" : failures + " FAILURE(S)"}`);
process.exit(failures === 0 ? 0 : 1);
