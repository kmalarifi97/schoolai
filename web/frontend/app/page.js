"use client";
import { useState, useEffect, useMemo, useCallback } from "react";
import { useRouter } from "next/navigation";

const AR = ["", "١", "٢", "٣", "٤", "٥", "٦", "٧", "٨", "٩"];
const ar = (n) => String(n).split("").map((d) => AR[+d] || d).join("");

export default function Reader() {
  const router = useRouter();
  const [token, setToken] = useState(null);
  const [user, setUser] = useState(null);
  const [cat, setCat] = useState(null);
  const [err, setErr] = useState("");
  const [sel, setSel] = useState(null); // {ch, lessonId}
  const [lb, setLb] = useState(null);

  useEffect(() => {
    const t = localStorage.getItem("p2_token");
    if (!t) return router.replace("/login");
    setToken(t);
    try { setUser(JSON.parse(localStorage.getItem("p2_user") || "null")); } catch {}
    fetch("/api/library", { headers: { Authorization: "Bearer " + t } })
      .then((r) => { if (r.status === 401) throw new Error("401"); return r.json(); })
      .then((d) => {
        setCat(d);
        const c0 = d.chapters[0];
        if (c0) setSel({ ch: c0.id, lessonId: c0.lessons[0]?.id });
      })
      .catch((e) => {
        if (String(e.message).includes("401")) { localStorage.removeItem("p2_token"); router.replace("/login"); }
        else setErr("تعذّر تحميل المكتبة");
      });
  }, [router]);

  const logout = useCallback(() => {
    localStorage.removeItem("p2_token"); localStorage.removeItem("p2_user");
    router.replace("/login");
  }, [router]);

  const open = (kind, slug, title) =>
    setLb({ src: `/api/video/${kind}/${slug}?t=${encodeURIComponent(token)}`, title });

  useEffect(() => {
    const k = (e) => e.key === "Escape" && setLb(null);
    addEventListener("keydown", k);
    return () => removeEventListener("keydown", k);
  }, []);

  const { chapter, lesson, projects } = useMemo(() => {
    if (!cat || !sel) return {};
    const chapter = cat.chapters.find((c) => c.id === sel.ch);
    const lesson = chapter?.lessons.find((l) => l.id === sel.lessonId);
    const projects = cat.projects.filter((p) => p.chapter === sel.ch);
    return { chapter, lesson, projects };
  }, [cat, sel]);

  if (err) return <div className="center">{err}</div>;
  if (!cat || !sel) return <div className="center">جارٍ فتح الكتاب…</div>;

  const pdfSrc = cat.book.has_pdf && lesson
    ? `/api/book?t=${encodeURIComponent(token)}#page=${lesson.start_page}&view=FitH`
    : null;

  return (
    <div className="shell">
      <div className="top">
        <div className="brand">الفيزياء ٢ — <span className="am">اقرأ، ثمّ شاهِد الشرارة.</span></div>
        <div className="right">
          <span className="who">{user?.name}</span>
          <button className="out" onClick={logout}>خروج</button>
        </div>
      </div>

      <div className="body">
        {/* TABLE OF CONTENTS — the book is the spine */}
        <nav className="toc">
          <div className="panhd">
            <span className="panhd__i">▦</span>
            <div>
              <strong>فهرس الكتاب</strong>
              <span>اختر درسًا — ينتقل الكتاب إلى صفحاته</span>
            </div>
          </div>
          <h2>{ar(cat.book.pages)} صفحة · ٦ فصول</h2>
          {cat.chapters.map((c) => (
            <div className="ch" key={c.id}>
              <div className="ch__t">
                <span className="ch__n">{ar(c.id)}</span>
                <div>
                  <h3>{c.title_ar}</h3>
                  <span className="ch__en">{c.title_en}</span>
                </div>
              </div>
              {c.lessons.map((l) => (
                <button
                  key={l.id}
                  className={"les" + (sel.lessonId === l.id ? " on" : "")}
                  onClick={() => setSel({ ch: c.id, lessonId: l.id })}
                >
                  {l.title_ar}
                  <small>{l.id} · ص {ar(l.start_page)}–{ar(l.end_page)} · {l.concepts.length} شرارة</small>
                </button>
              ))}
            </div>
          ))}
        </nav>

        {/* THE PAGE */}
        <main className="read">
          {pdfSrc ? (
            <iframe key={sel.lessonId} src={pdfSrc} title="الكتاب" />
          ) : (
            <div className="nopdf">الكتاب غير متوفّر في هذا التشغيل.</div>
          )}
          {lesson && (
            <div className="pg">{chapter.title_ar} · {lesson.title_ar} · ص {ar(lesson.start_page)}–{ar(lesson.end_page)}</div>
          )}
        </main>

        {/* DOCK: spark videos for this lesson + the chapter's project */}
        <aside className="dock">
          <div className="panhd">
            <span className="panhd__i">▶</span>
            <div>
              <strong>بعد أن تقرأ</strong>
              <span>شرارات هذا الدرس ومشروع الفصل</span>
            </div>
          </div>
          <p className="lbl">شرارات الدرس · {lesson?.title_ar}</p>
          <p className="sub">مقطعٌ قصيرٌ يبني الحدس، ثمّ تعود إلى الصفحة وتحلّ بنفسك.</p>
          {lesson?.concepts.length ? lesson.concepts.map((cc) => (
            <div className="vc" key={cc.slug}>
              <div className="vc__r">
                {cc.video
                  ? <button className="play" onClick={() => open("concept", cc.slug, cc.ar)}>▶</button>
                  : <span className="ext">مؤرشَف</span>}
                <div>
                  <span className="en">{cc.en}</span>
                  <h4>{cc.ar}</h4>
                </div>
              </div>
              {cc.handoff && <p className="ho">{cc.handoff}</p>}
            </div>
          )) : <p className="empty">لا توجد شرارات لهذا الدرس.</p>}

          {projects.length > 0 && (
            <>
              <p className="lbl two">مشروع الفصل — على مِحاكاة PhET</p>
              {projects.map((p) => (
                <div className="pj" key={p.slug} style={{ marginBottom: 14 }}>
                  <div className="psim">{p.sim}</div>
                  <h4>{p.ar}</h4>
                  <p className="per">{p.persona}</p>
                  <div className="act">
                    {p.video && <button className="play" onClick={() => open("project", p.slug, p.ar)}>▶ القصّة</button>}
                    <a className="phet" href={p.phet} target="_blank" rel="noopener">افتح PhET ↗</a>
                  </div>
                </div>
              ))}
            </>
          )}
        </aside>
      </div>

      <div className={"lb" + (lb ? " on" : "")} onClick={(e) => e.target.classList.contains("lb") && setLb(null)}>
        <button className="lb__x" onClick={() => setLb(null)} aria-label="إغلاق">✕</button>
        {lb && (
          <div className="lb__in">
            <div className="lb__t">{lb.title}</div>
            <video src={lb.src} controls autoPlay preload="metadata" />
          </div>
        )}
      </div>
    </div>
  );
}
