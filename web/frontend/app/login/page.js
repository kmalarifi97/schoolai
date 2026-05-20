"use client";
import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";

export default function Login() {
  const router = useRouter();
  const [u, setU] = useState("");
  const [p, setP] = useState("");
  const [err, setErr] = useState("");
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    if (localStorage.getItem("p2_token")) router.replace("/");
  }, [router]);

  async function submit(e) {
    e.preventDefault();
    setErr("");
    setBusy(true);
    try {
      const r = await fetch("/api/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username: u, password: p }),
      });
      const d = await r.json();
      if (!r.ok) throw new Error(d.detail || "تعذّر تسجيل الدخول");
      localStorage.setItem("p2_token", d.token);
      localStorage.setItem("p2_user", JSON.stringify(d.user));
      router.replace("/");
    } catch (e) {
      setErr(e.message);
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="login">
      <form className="login__box" onSubmit={submit}>
        <div className="kick">الفيزياء ٢ · نظام المسارات</div>
        <h1>
          شاهِد الفكرة.<br />
          ثمّ <span className="am">حُلَّ بنفسك.</span>
        </h1>
        <p>سجّل الدخول للوصول إلى المكتبة. الحسابات مُهيّأة مسبقًا من قِبل المعلّم.</p>
        <div className="fld">
          <label>اسم المستخدم</label>
          <input value={u} onChange={(e) => setU(e.target.value)} autoFocus dir="ltr" />
        </div>
        <div className="fld">
          <label>كلمة المرور</label>
          <input type="password" value={p} onChange={(e) => setP(e.target.value)} dir="ltr" />
        </div>
        <button className="btn" disabled={busy}>
          {busy ? "جارٍ التحقّق…" : "دخول"}
        </button>
        <div className="err">{err}</div>
        <div className="hint">حساب تجريبي: demo / demo</div>
      </form>
    </div>
  );
}
