// Hand-authored prerequisite graphs attached to real book content nodes.
// Each descends from the law into its underlying concepts/math, justifies why
// each node needs the one beneath it, and STOPS at equation/variable literacy.
// Every prereq node carries one check question. Not deduped across laws.
//
// `anchor` locates the content node in the book graph (lesson code + type + a
// text fragment). Author more by following the same pattern.

const FLOOR = "equation/variable literacy";
const floorNode = { concept: FLOOR, layer: 4, is_floor: true,
  check_question: "في المعادلة 2x = 10، ماذا يمثّل الرمز x، وماذا تعني علامة = ؟" };

export const PREREQ_GRAPHS = [
  {
    name: "Kepler's third law",
    anchor: { lessonCode: "1-1", type: "equation", like: "الثالث لكبلر" },
    nodes: [
      { concept: "proportionality", layer: 1, check_question: "إذا تناسبت y طرديًا مع x وضاعفت x، فماذا يحدث لـ y؟" },
      { concept: "powers/exponents", layer: 1, check_question: "كم يساوي 2³، وماذا يعني الأس؟" },
      { concept: "ratio", layer: 1, check_question: "ماذا يعني أن النسبة r³/T² ثابتة لكل الكواكب؟" },
      { concept: "division", layer: 2, check_question: "اقسم 12 ÷ 4، وما الذي تخبرك به القسمة؟" },
      { concept: "constant", layer: 2, check_question: "ماذا يعني أن مقدارًا في معادلةٍ 'ثابت'؟" },
      { concept: "multiplication", layer: 2, check_question: "اكتب 3×4 على صورة جمعٍ متكرر." },
      { concept: "equals sign as balance", layer: 3, check_question: "إذا كان الطرف الأيسر = 10، فكم الطرف الأيمن، ولماذا؟" },
      { concept: "addition", layer: 3, check_question: "كم يساوي 7 + 5؟" },
      floorNode,
    ],
    edges: [
      { concept: "Kepler's third law", requires: "proportionality", why: "(r/…)³=(T/…)² علاقة تناسب" },
      { concept: "Kepler's third law", requires: "powers/exponents", why: "التكعيب والتربيع قوى" },
      { concept: "Kepler's third law", requires: "ratio", why: "r³/T² نسبة ثابتة" },
      { concept: "proportionality", requires: "division", why: "مقارنة كيف يتغير مقدار مع آخر قسمة" },
      { concept: "proportionality", requires: "constant", why: "'يتناسب' تعني أن النسبة ثابتة" },
      { concept: "powers/exponents", requires: "multiplication", why: "القوة ضربٌ متكرر" },
      { concept: "ratio", requires: "division", why: "النسبة قسمة كميتين" },
      { concept: "division", requires: "equals sign as balance", why: "القسمة على الطرفين تحافظ على التوازن" },
      { concept: "multiplication", requires: "addition", why: "الضرب جمعٌ متكرر" },
      { concept: "addition", requires: FLOOR, why: "الجمع يجمع قيمًا تمثّلها رموز" },
      { concept: "equals sign as balance", requires: FLOOR, why: "= تعني تساوي الطرفين" },
    ],
  },
  {
    name: "Newton's law of universal gravitation",
    anchor: { lessonCode: "1-1", type: "equation", like: "الجذب الكوني" },
    nodes: [
      { concept: "direct proportionality (F ∝ m₁m₂)", layer: 1, check_question: "إذا تضاعفت إحدى الكتلتين والباقي ثابت، فماذا يحدث لقوة الجذب؟" },
      { concept: "inverse-square law (F ∝ 1/r²)", layer: 1, check_question: "إذا تضاعفت المسافة r، إلى كم تتغيّر القوة؟" },
      { concept: "product of masses (m₁·m₂)", layer: 1, check_question: "ماذا يعني حاصل ضرب الكتلتين m₁·m₂؟" },
      { concept: "proportionality (constant ratio)", layer: 2, check_question: "ما معنى أن كميةً تتناسب طرديًا مع أخرى؟" },
      { concept: "division", layer: 2, check_question: "ماذا يمثّل المقدار 1/r²؟" },
      { concept: "powers/exponents", layer: 2, check_question: "كم يساوي r² إذا كان r=3؟" },
      { concept: "multiplication", layer: 2, check_question: "اكتب 4×3 على صورة جمعٍ متكرر." },
      { concept: "equals sign as balance", layer: 3, check_question: "في F = G·m₁m₂/r²، ماذا تعني علامة = ؟" },
      { concept: "addition", layer: 3, check_question: "كم يساوي 6 + 7؟" },
      floorNode,
    ],
    edges: [
      { concept: "Newton's law of universal gravitation", requires: "direct proportionality (F ∝ m₁m₂)", why: "القوة تكبر بكبر كل كتلة" },
      { concept: "Newton's law of universal gravitation", requires: "inverse-square law (F ∝ 1/r²)", why: "القوة تصغر مع مربع المسافة" },
      { concept: "Newton's law of universal gravitation", requires: "product of masses (m₁·m₂)", why: "الكتلتان تُضربان" },
      { concept: "direct proportionality (F ∝ m₁m₂)", requires: "proportionality (constant ratio)", why: "التناسب الطردي نسبة ثابتة" },
      { concept: "inverse-square law (F ∝ 1/r²)", requires: "division", why: "1/r² قسمة" },
      { concept: "inverse-square law (F ∝ 1/r²)", requires: "powers/exponents", why: "التربيع قوة" },
      { concept: "product of masses (m₁·m₂)", requires: "multiplication", why: "الحاصل ضرب" },
      { concept: "proportionality (constant ratio)", requires: "division", why: "النسبة قسمة" },
      { concept: "powers/exponents", requires: "multiplication", why: "القوة ضربٌ متكرر" },
      { concept: "division", requires: "equals sign as balance", why: "إعادة الترتيب تحافظ على التوازن" },
      { concept: "multiplication", requires: "addition", why: "الضرب جمعٌ متكرر" },
      { concept: "addition", requires: FLOOR, why: "الجمع يجمع قيمًا تمثّلها رموز" },
      { concept: "equals sign as balance", requires: FLOOR, why: "= تعني تساوي الطرفين" },
    ],
  },
  {
    name: "Angular velocity (ω = Δθ/Δt)",
    anchor: { lessonCode: "2-1", type: "key_term", like: "زاوي" },
    nodes: [
      { concept: "rate of change (per unit time)", layer: 1, check_question: "ماذا تعني أن مقدارًا يتغيّر بمعدّلٍ ثابت في الثانية؟" },
      { concept: "ratio of two changes (Δθ/Δt)", layer: 1, check_question: "ماذا تمثّل النسبة Δθ/Δt؟" },
      { concept: "angle measure (θ)", layer: 1, check_question: "ماذا يمثّل الرمز θ، وبأي وحدة يُقاس؟" },
      { concept: "division", layer: 2, check_question: "لماذا قسمة التغيّر على الزمن تعطي معدّلًا؟" },
      { concept: "subtraction (Δ = final − initial)", layer: 2, check_question: "إذا كانت الزاوية بدأت 30° وانتهت 80°، فكم Δθ؟" },
      { concept: "equals sign as balance", layer: 3, check_question: "في ω = Δθ/Δt، ماذا تعني علامة = ؟" },
      { concept: "addition", layer: 3, check_question: "كم يساوي 9 + 4؟" },
      floorNode,
    ],
    edges: [
      { concept: "Angular velocity (ω = Δθ/Δt)", requires: "rate of change (per unit time)", why: "ω مقدار تغيّر الزاوية في الثانية" },
      { concept: "Angular velocity (ω = Δθ/Δt)", requires: "ratio of two changes (Δθ/Δt)", why: "ω = Δθ/Δt نسبة" },
      { concept: "Angular velocity (ω = Δθ/Δt)", requires: "angle measure (θ)", why: "θ هي الزاوية المقطوعة" },
      { concept: "rate of change (per unit time)", requires: "division", why: "المعدّل قسمة على الزمن" },
      { concept: "ratio of two changes (Δθ/Δt)", requires: "division", why: "النسبة قسمة" },
      { concept: "ratio of two changes (Δθ/Δt)", requires: "subtraction (Δ = final − initial)", why: "Δ فرقٌ بين قيمتين" },
      { concept: "angle measure (θ)", requires: FLOOR, why: "θ رمزٌ يمثّل عددًا" },
      { concept: "division", requires: "equals sign as balance", why: "إعادة الترتيب تحافظ على التوازن" },
      { concept: "subtraction (Δ = final − initial)", requires: "addition", why: "الطرح عكس الجمع" },
      { concept: "addition", requires: FLOOR, why: "الجمع يجمع قيمًا تمثّلها رموز" },
      { concept: "equals sign as balance", requires: FLOOR, why: "= تعني تساوي الطرفين" },
    ],
  },
];
