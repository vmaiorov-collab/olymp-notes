// Самый длинный «горб» (строго возрастает, затем строго убывает) среди подотрезков массива. Сравниваем соседей: U — рост, D — спад, E — равенство.
// Нужна самая длинная подстрока вида U*D* без E. Узел дерева хранит 7 величин.
struct Node {
    int len = 0;
    int pre = 0, suf = 0;          // самый длинный префикс / суффикс вида U*D*
    int preD = 0, sufU = 0;        // самый длинный префикс из одних D / суффикс из одних U
    int best = 0;                  // лучшая подстрока внутри
    bool allU = true, allD = true; // весь отрезок из U / весь из D (пустой отрезок — оба true)
};
Node merge(const Node &a, const Node &b) {
    Node r;
    r.len = a.len + b.len;
    r.allU = a.allU && b.allU; r.allD = a.allD && b.allD;
    // префикс U*D*: если левая часть — одни U, префикс может продолжиться любым префиксом U*D* справа; если левая U*D*, но не одни U — только префиксом из D
    if (a.allU) r.pre = a.len + b.pre;
    else if (a.pre == a.len) r.pre = a.len + b.preD;
    else r.pre = a.pre;
    if (b.allD) r.suf = b.len + a.suf;
    else if (b.suf == b.len) r.suf = b.len + a.sufU;
    else r.suf = b.suf;
    r.preD = a.allD ? a.len + b.preD : a.preD;
    r.sufU = b.allU ? b.len + a.sufU : b.sufU;
    // через границу: (суффикс левой из одних U) + (любой префикс U*D* правой)  либо  (любой суффикс U*D* левой) + (префикс из одних D)
    r.best = max({a.best, b.best, a.sufU + b.pre, a.suf + b.preD});
    return r;
}
Node leaf(int type) {              // type: 0 = U, 1 = D, 2 = E
    Node r; r.len = 1;
    r.allU = type == 0; r.allD = type == 1;
    r.pre = r.suf = r.best = (type != 2);
    r.preD = (type == 1); r.sufU = (type == 0);
    return r;
}
int typeOf(long long x, long long y) { return x < y ? 0 : (x > y ? 1 : 2); }
// Ответ для всего массива из n >= 1 чисел: best + 1 (число элементов горба), для n = 1 — 1.
