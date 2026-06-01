// GraphQL schema + resolvers over the prerequisite graph store.
// This is the "graph DB API" the MCP server talks to. Diagnosis is a query,
// not an engine: the resolver just walks edges.

import { makeExecutableSchema } from "@graphql-tools/schema";

export const typeDefs = /* GraphQL */ `
  "A skill / concept node. An edge source->target means source is a prerequisite of target."
  type Skill {
    id: ID!
    name: String!
    "Direct prerequisites by default; pass recursive:true for the full upstream chain (nearest-first)."
    prerequisites(recursive: Boolean = false): [Skill!]!
    "Skills that directly depend on this one."
    dependents: [Skill!]!
  }

  "A directed prerequisite edge, carrying the empirical conditional probabilities that justified it."
  type Edge {
    source: Skill!
    target: Skill!
    "P(mastered source | mastered target) — high (>0.9) is why the edge exists."
    pSourceGivenTarget: Float
    "P(mastered target | mastered source) — low (<0.5) sets the arrow direction."
    pTargetGivenSource: Float
    "Number of students who attempted both skills."
    support: Int
  }

  "One link in a failed skill's prerequisite chain, with the student's status on it."
  type WeaknessLink {
    skill: Skill!
    "passed | failed | untested"
    status: String!
    "Distance (in prerequisite hops) from the failed skill."
    depth: Int!
  }

  type FailedSkillDiagnosis {
    skill: Skill!
    "Deepest not-mastered prerequisite — teach this first."
    rootCause: Skill
    "Full upstream prerequisite chain, nearest-first."
    chain: [WeaknessLink!]!
    "Subset of the chain the student has not mastered (blocks progress)."
    notMastered: [WeaknessLink!]!
    recommendation: String!
  }

  type Diagnosis {
    failed: [FailedSkillDiagnosis!]!
    summary: String!
  }

  type Query {
    skills: [Skill!]!
    skill(id: ID!): Skill
    edges: [Edge!]!
    "Skill ids with a prerequisite cycle (should be empty for a DAG)."
    cycles: [[ID!]!]!
    "Diagnose a student from quiz results: which prerequisites block each failed skill."
    diagnose(passed: [ID!]! = [], failed: [ID!]! = []): Diagnosis!
  }
`;

export function buildSchema(store) {
  const resolvers = {
    Query: {
      skills: () => store.allNodes(),
      skill: (_, { id }) => store.node(id),
      edges: () => store.allEdges(),
      cycles: () => store.findCycles(),
      diagnose: (_, { passed, failed }) => store.diagnose({ passed, failed }),
    },
    Skill: {
      prerequisites: (s, { recursive }) => store.prerequisitesOf(s.id, { recursive }),
      dependents: (s) => store.dependentsOf(s.id),
    },
    Edge: {
      source: (e) => store.node(e.source),
      target: (e) => store.node(e.target),
      pSourceGivenTarget: (e) => e.p_source_given_target ?? null,
      pTargetGivenSource: (e) => e.p_target_given_source ?? null,
      support: (e) => e.support ?? null,
    },
    WeaknessLink: {
      skill: (w) => store.node(w.id),
    },
  };
  return makeExecutableSchema({ typeDefs, resolvers });
}
