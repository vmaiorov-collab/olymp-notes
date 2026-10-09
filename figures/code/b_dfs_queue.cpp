// Очередь: человек приходит в момент t и занимает кабинет на d. Обслуживают в порядке прихода. Запрос T: когда освободится кабинет после всех, кто пришёл раньше T.
// Каждый человек — функция s -> max(s + d, t + d) = max(s + A, B); композиция таких функций — снова такая же функция: дерево отрезков над функциями.
const long long NEG = LLONG_MIN / 4;
struct F { long long A, B; };                                 // s -> max(s + A, B)
F compose(F f, F g) { return {f.A + g.A, max(f.B + g.A, g.B)}; }    // сначала f, потом g
const F IDENT = {0, NEG};
struct QueueTree {
    int n; vector<F> t; vector<long long> times;              // times — отсортированные возможные моменты прихода
    QueueTree(vector<long long> ts) : times(ts) {
        sort(times.begin(), times.end());
        n = 1; while (n < (int)times.size()) n <<= 1;
        t.assign(2 * n, IDENT);
    }
    void set(long long arrive, long long dur, bool present) {
        int i = lower_bound(times.begin(), times.end(), arrive) - times.begin() + n;
        t[i] = present ? F{dur, arrive + dur} : IDENT;
        for (i >>= 1; i; i >>= 1) t[i] = compose(t[2 * i], t[2 * i + 1]);
    }
    long long waitFrom(long long T) {                          // сколько ждать, если прийти в момент T
        int r = lower_bound(times.begin(), times.end(), T) - times.begin();   // берём тех, кто пришёл строго раньше T
        F acc = IDENT;
        // композиция левого префикса [0, r): обход снизу вверх, левые куски накапливаем слева направо
        vector<int> leftNodes, rightNodes;
        for (int l = n, rr = n + r; l < rr; l >>= 1, rr >>= 1) {
            if (l & 1) leftNodes.push_back(l++);
            if (rr & 1) rightNodes.push_back(--rr);
        }
        for (int v : leftNodes) acc = compose(acc, t[v]);
        for (int k = (int)rightNodes.size() - 1; k >= 0; k--) acc = compose(acc, t[rightNodes[k]]);
        long long freeAt = max(0LL + acc.A, acc.B);            // начальное свободное время 0
        return max(0LL, freeAt - T);
    }
};
