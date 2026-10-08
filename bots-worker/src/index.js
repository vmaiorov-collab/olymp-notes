// Cloudflare Worker: бот статистики + счётчик визитов без cookie.
//   POST /tg   — вебхук Telegram (заголовок X-Telegram-Bot-Api-Secret-Token = WEBHOOK_SECRET)
//   GET  /hit  — маячок со страниц конспектов: ?p=/путь/страницы.html
// Секреты (wrangler secret put): STATS_BOT_TOKEN, WEBHOOK_SECRET, SALT.
// Хранилище: D1 (hits — просмотры по дням и страницам, visitors — хэши уникальных за день).

const PARALLELS = {
  "parallel-c": "Параллель C",
  "parallel-b": "Параллель B",
  "parallel-bs": "Параллель BS",
  "parallel-x": "Параллель X",
};
const SPARK = "▁▂▃▄▅▆▇█";
const WEEKDAYS = ["вс", "пн", "вт", "ср", "чт", "пт", "сб"];
const PERIODS = [1, 7, 30, 90];
const DAY = 86400000;

const esc = (s) => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
const dayStr = (d) => d.toISOString().slice(0, 10);

async function tg(token, method, body) {
  const res = await fetch(`https://api.telegram.org/bot${token}/${method}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  const data = await res.json();
  if (!data.ok) throw new Error(data.description || "telegram error");
  return data.result;
}

// ---------- счётчик ----------

async function sha(text) {
  const buf = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(text));
  return [...new Uint8Array(buf)].slice(0, 12).map((b) => b.toString(16).padStart(2, "0")).join("");
}

function cors(extra = {}) {
  return { "Access-Control-Allow-Origin": "*", "Cache-Control": "no-store", ...extra };
}

async function handleHit(request, env) {
  const url = new URL(request.url);
  let path = (url.searchParams.get("p") || "/").slice(0, 200);
  path = path.replace(/^\/olymp-notes/, "").replace(/\/index\.html$/, "/") || "/";
  if (!/^[\w\-./%]+$/.test(path)) path = "/";
  const day = dayStr(new Date());
  const ip = request.headers.get("CF-Connecting-IP") || "";
  const ua = request.headers.get("User-Agent") || "";
  const h = await sha(`${env.SALT}|${day}|${ip}|${ua}`); // ежедневно меняется — повторно не отследить
  await env.DB.batch([
    env.DB.prepare("INSERT INTO hits(day,path,n) VALUES(?,?,1) ON CONFLICT(day,path) DO UPDATE SET n=n+1").bind(day, path),
    env.DB.prepare("INSERT OR IGNORE INTO visitors(day,h) VALUES(?,?)").bind(day, h),
  ]);
  return new Response(null, { status: 204, headers: cors() });
}

// ---------- оформление ----------

function fmtDay(iso) {
  const d = new Date(iso + "T00:00:00Z");
  return `${iso.slice(8, 10)}.${iso.slice(5, 7)} (${WEEKDAYS[d.getUTCDay()]})`;
}
function spark(values, maxLen = 30) {
  if (!values.length) return "";
  let v = values;
  if (v.length > maxLen) {
    const k = Math.ceil(v.length / maxLen);
    v = [];
    for (let i = 0; i < values.length; i += k) v.push(values.slice(i, i + k).reduce((a, b) => a + b, 0));
  }
  const max = Math.max(...v);
  if (!max) return SPARK[0].repeat(v.length);
  return v.map((x) => SPARK[Math.min(7, Math.round((x / max) * 7))]).join("");
}
const bar = (value, max, w = 10) => {
  const n = max ? Math.max(value > 0 ? 1 : 0, Math.round((value / max) * w)) : 0;
  return "█".repeat(n) + "░".repeat(w - n);
};
function delta(cur, prev) {
  if (!prev) return cur ? "новое" : "—";
  const p = Math.round(((cur - prev) / prev) * 100);
  return `${p > 0 ? "▲ +" : p < 0 ? "▼ −" : "• "}${Math.abs(p)}%`;
}
const periodLabel = (d) => (d === 1 ? "сегодня" : `${d} дн.`);

function range(days) {
  const today = new Date();
  today.setUTCHours(0, 0, 0, 0);
  const start = new Date(today.getTime() - (days - 1) * DAY);
  const prevStart = new Date(start.getTime() - days * DAY);
  return { start: dayStr(start), end: dayStr(today), prevStart: dayStr(prevStart), prevEnd: dayStr(new Date(start.getTime() - DAY)), startDate: start, today };
}

// ---------- GoatCounter (если задан секрет GC_API_TOKEN) ----------
// Сайт общий со старым conspectus, поэтому берём только страницы нового сайта (/olymp-notes/…).
const GC_PREFIX = "/olymp-notes";

async function gcHits(env, from, to) {
  const url = new URL(`https://${env.GC_SITE}.goatcounter.com/api/v0/stats/hits`);
  url.searchParams.set("start", `${from}T00:00:00Z`);
  url.searchParams.set("end", `${to}T23:59:59Z`);
  url.searchParams.set("limit", "100");
  const res = await fetch(url, { headers: { Authorization: `Bearer ${env.GC_API_TOKEN}` } });
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || JSON.stringify(data));
  return (data.hits || []).filter((h) => (h.path || "").startsWith(GC_PREFIX + "/") || h.path === GC_PREFIX);
}

const normPath = (p) => (p.slice(GC_PREFIX.length).replace(/\/index\.html$/, "/") || "/");

async function perDay(env, from, to) {
  if (env.GC_API_TOKEN) {
    const m = new Map();
    for (const h of await gcHits(env, from, to)) for (const d of h.stats || []) {
      if (d.day < from || d.day > to) continue;
      m.set(d.day, { v: (m.get(d.day)?.v || 0) + d.daily, u: 0 });
    }
    return m;
  }
  const hits = await env.DB.prepare("SELECT day, SUM(n) AS v FROM hits WHERE day BETWEEN ? AND ? GROUP BY day").bind(from, to).all();
  const uniq = await env.DB.prepare("SELECT day, COUNT(*) AS u FROM visitors WHERE day BETWEEN ? AND ? GROUP BY day").bind(from, to).all();
  const m = new Map();
  for (const r of hits.results) m.set(r.day, { v: r.v, u: 0 });
  for (const r of uniq.results) m.set(r.day, { v: m.get(r.day)?.v || 0, u: r.u });
  return m;
}

async function reportStats(env, days) {
  const r = range(days);
  const cur = await perDay(env, r.start, r.end);
  const prev = await perDay(env, r.prevStart, r.prevEnd);
  const rows = [];
  for (let t = r.startDate.getTime(); t <= r.today.getTime(); t += DAY) {
    const day = dayStr(new Date(t));
    rows.push({ day, v: cur.get(day)?.v || 0, u: cur.get(day)?.u || 0 });
  }
  const sum = (a, k) => a.reduce((x, y) => x + y[k], 0);
  const views = sum(rows, "v");
  const uniq = sum(rows, "u"); // сумма «уникальных по дням»
  const pv = [...prev.values()].reduce((x, y) => x + y.v, 0);
  const best = rows.reduce((a, b) => (b.v > a.v ? b : a), rows[0]);
  const lines = [`📊 <b>Статистика olymp-notes</b> · ${periodLabel(days)}`, ""];
  lines.push(`👁 Просмотров: <b>${views}</b>  <i>${delta(views, pv)} к прошлому периоду (${pv})</i>`);
  if (!env.GC_API_TOKEN) lines.push(`👥 Посетителей (по дням): <b>${uniq}</b>`);
  if (days > 1) {
    lines.push(`📈 В среднем: <b>${(views / rows.length).toFixed(1)}</b> просмотров в день`);
    if (best.v > 0) lines.push(`🔥 Рекорд: <b>${best.v}</b> — ${fmtDay(best.day)}`);
    lines.push("", `<code>${spark(rows.map((x) => x.v))}</code>`, `<i>${rows[0].day.slice(8)}.${rows[0].day.slice(5, 7)} → сегодня</i>`);
  }
  if (!views) lines.push("", "Данных пока нет — счётчик заработает, когда страницы начнут открывать.");
  return lines.join("\n");
}

async function topRows(env, days) {
  const r = range(days);
  if (env.GC_API_TOKEN) {
    return (await gcHits(env, r.start, r.end)).map((h) => ({ path: normPath(h.path), v: h.count })).sort((a, b) => b.v - a.v);
  }
  const q = await env.DB.prepare("SELECT path, SUM(n) AS v FROM hits WHERE day BETWEEN ? AND ? GROUP BY path ORDER BY v DESC LIMIT 200").bind(r.start, r.end).all();
  return q.results;
}

async function reportTop(env, days, n = 8) {
  const head = `🏆 <b>Топ страниц</b> · ${periodLabel(days)}`;
  const rows = (await topRows(env, days)).slice(0, n);
  if (!rows.length) return `${head}\n\nПока нет данных.`;
  const medals = ["🥇", "🥈", "🥉"];
  const lines = [head, ""];
  rows.forEach((h, i) => {
    lines.push(`${medals[i] || `<b>${i + 1}.</b>`} <code>${esc(h.path)}</code>`);
    lines.push(`     <code>${bar(h.v, rows[0].v)}</code> <b>${h.v}</b>`);
  });
  return lines.join("\n");
}

async function reportParallels(env, days) {
  const head = `🧩 <b>Просмотры по параллелям</b> · ${periodLabel(days)}`;
  const totals = {};
  for (const h of await topRows(env, days)) {
    const seg = h.path.split("/").filter(Boolean)[0];
    const k = PARALLELS[seg] || "Главная / прочее";
    totals[k] = (totals[k] || 0) + h.v;
  }
  const entries = Object.entries(totals).sort((a, b) => b[1] - a[1]);
  if (!entries.length) return `${head}\n\nПока нет данных.`;
  const all = entries.reduce((a, [, v]) => a + v, 0);
  const lines = [head, ""];
  for (const [name, v] of entries) {
    lines.push(esc(name), `<code>${bar(v, entries[0][1])}</code> <b>${v}</b> · ${Math.round((v / all) * 100)}%`);
  }
  return lines.join("\n");
}

// ---------- бот ----------

const VIEWS = [["stats", "📊 Сводка"], ["top", "🏆 Топ"], ["par", "🧩 Параллели"]];

function keyboard(view, days, env) {
  const views = VIEWS.map(([v, label]) => ({ text: v === view ? `● ${label}` : label, callback_data: `${v}:${days}` }));
  const periods = PERIODS.map((d) => {
    const name = d === 1 ? "Сегодня" : `${d} дн.`;
    return { text: d === days ? `● ${name}` : name, callback_data: `${view}:${d}` };
  });
  return { inline_keyboard: [views, periods, [{ text: "🔄 Обновить", callback_data: `${view}:${days}` }, { text: "🌐 Открыть сайт", url: env.SITE_URL }]] };
}

// постоянная клавиатура под полем ввода: команды набирать не нужно
const REPLY_KB = {
  keyboard: [[{ text: "📊 Сводка" }, { text: "☀️ Сегодня" }], [{ text: "🏆 Топ" }, { text: "🧩 Параллели" }]],
  resize_keyboard: true,
  is_persistent: true,
  input_field_placeholder: "Выберите раздел…",
};
const BUTTON_CMD = { "📊 Сводка": "/stats", "☀️ Сегодня": "/today", "🏆 Топ": "/top", "🧩 Параллели": "/parallels" };

const render = (env, view, days) => (view === "top" ? reportTop(env, days) : view === "par" ? reportParallels(env, days) : reportStats(env, days));
const clampDays = (a, def = 7) => { const n = parseInt(a, 10); return Number.isFinite(n) && n >= 1 ? Math.min(n, 365) : def; };

const HELP =
  "👋 <b>Бот статистики olymp-notes</b>\n\n" +
  "Кнопки внизу — быстрый доступ, а под каждым отчётом можно менять раздел и период.\n\n" +
  "Команды: /stats [дни] · /today · /top [дни] · /parallels [дни]";

async function handleUpdate(update, env) {
  const token = env.STATS_BOT_TOKEN;
  const cq = update.callback_query;
  if (cq) {
    const m = cq.message;
    if (!m) return;
    const [view, d] = (cq.data || "").split(":");
    const days = clampDays(d);
    let text;
    try { text = await render(env, view, days); } catch (e) { text = `⚠️ Не удалось получить статистику: ${esc(e.message)}`; }
    try {
      await tg(token, "editMessageText", { chat_id: m.chat.id, message_id: m.message_id, text, parse_mode: "HTML", disable_web_page_preview: true, reply_markup: keyboard(view, days, env) });
      await tg(token, "answerCallbackQuery", { callback_query_id: cq.id });
    } catch (e) {
      await tg(token, "answerCallbackQuery", { callback_query_id: cq.id, text: String(e.message).includes("not modified") ? "Уже актуально ✅" : "Ошибка обновления" }).catch(() => {});
    }
    return;
  }
  const msg = update.message;
  if (!msg || !msg.text) return;
  const raw = BUTTON_CMD[msg.text.trim()] || msg.text;
  if (!raw.startsWith("/")) return;
  const parts = raw.trim().split(/\s+/);
  const cmd = parts[0].split("@")[0].toLowerCase();
  let text, view = "stats", days = 7;
  try {
    if (cmd === "/start" || cmd === "/help") {
      await tg(token, "sendMessage", { chat_id: String(msg.chat.id), text: HELP, parse_mode: "HTML", reply_markup: REPLY_KB });
      text = await reportStats(env, 7);
    }
    else if (cmd === "/stats") { days = clampDays(parts[1]); text = await reportStats(env, days); }
    else if (cmd === "/today") { days = 1; text = await reportStats(env, 1); }
    else if (cmd === "/top") { view = "top"; days = clampDays(parts[1]); text = await reportTop(env, days); }
    else if (cmd === "/parallels") { view = "par"; days = clampDays(parts[1]); text = await reportParallels(env, days); }
  } catch (e) { text = `⚠️ Не удалось получить статистику: ${esc(e.message)}`; }
  if (text) await tg(token, "sendMessage", { chat_id: String(msg.chat.id), text, parse_mode: "HTML", disable_web_page_preview: true, reply_markup: keyboard(view, days, env) });
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === "/hit") {
      if (request.method === "OPTIONS") return new Response(null, { status: 204, headers: cors({ "Access-Control-Allow-Methods": "GET,POST" }) });
      try { return await handleHit(request, env); } catch (e) { console.error(e); return new Response(null, { status: 204, headers: cors() }); }
    }
    if (url.pathname === "/tg" && request.method === "POST") {
      if (request.headers.get("X-Telegram-Bot-Api-Secret-Token") !== env.WEBHOOK_SECRET) return new Response("forbidden", { status: 403 });
      try { await handleUpdate(await request.json(), env); } catch (e) { console.error(e); }
      return new Response("ok"); // всегда 200, иначе Telegram будет ретраить
    }
    return new Response("ok");
  },
};
