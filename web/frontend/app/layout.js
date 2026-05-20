import "./globals.css";

export const metadata = {
  title: "مكتبة الفيزياء ٢ — شاهد الفكرة، ثمّ حُلّ بنفسك",
  description: "مكتبة مفاهيم ومشاريع الفيزياء ٢ — نظام المسارات",
};

export default function RootLayout({ children }) {
  return (
    <html lang="ar" dir="rtl">
      <body>{children}</body>
    </html>
  );
}
