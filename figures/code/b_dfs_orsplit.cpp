// Число разбиений массива на отрезки так, чтобы побитовые OR отрезков не убывали: OR_1 <= OR_2 <= ... (по модулю MOD). a_i < 2^B.
// dp[j] — маленький список (значение OR последнего отрезка, число способов) для префикса длины j. «Динамика вперёд» из j.
const long long MOD = 998244353;
const int B = 20;
long long countOrSplits(const vector<int> &a0) {
    int n = a0.size();
    vector<int> a(n + 2, 0);
    for (int i = 0; i < n; i++) a[i + 1] = a0[i];
    vector<vector<int>> nxt(B, vector<int>(n + 3, n + 1));    // nxt[k][s] — первая позиция >= s, где установлен бит k
    for (int k = 0; k < B; k++)
        for (int s = n; s >= 1; s--) nxt[k][s] = (a[s] >> k & 1) ? s : nxt[k][s + 1];
    struct Ev { int x; long long d; int c; };
    vector<vector<Ev>> events(n + 3);                         // события «добавить/убрать вклад для значения x» в позиции i
    map<int, pair<long long,int>> cur;                        // x -> (сумма вкладов, число активных вкладов)
    vector<pair<int,long long>> dp = {{0, 1}};                // dp[0]: пустой префикс, «OR» = 0 (подходит под любой следующий)
    for (int j = 0; j <= n; j++) {
        if (j >= 1) {
            for (auto &e : events[j]) {                       // применяем события в позиции j
                auto &p = cur[e.x];
                p.first = ((p.first + e.d) % MOD + MOD) % MOD; p.second += e.c;
                if (p.second == 0) cur.erase(e.x);
            }
            dp.clear();
            for (auto &[x, p] : cur) dp.push_back({x, p.first});     // dp[j]: OR последнего отрезка = x
        }
        if (j == n) break;
        int s = j + 1;
        vector<int> pos;                                      // позиции, где в OR(s..i) появляется новый бит
        for (int k = 0; k < B; k++) if (nxt[k][s] <= n) pos.push_back(nxt[k][s]);
        sort(pos.begin(), pos.end()); pos.erase(unique(pos.begin(), pos.end()), pos.end());
        int curOr = 0, start = s;
        auto emit = [&](int l, int r, int orv) {              // для i в [l, r] отрезок (j, i] имеет OR = orv
            long long S = 0;
            for (auto &[v, c] : dp) if (v <= orv) S = (S + c) % MOD;     // суммируем dp[j][v] по v <= orv
            events[l].push_back({orv, S, 1}); events[r + 1].push_back({orv, (MOD - S) % MOD, -1});
        };
        for (int p : pos) {
            if (p > start) emit(start, p - 1, curOr);
            curOr |= a[p]; start = p;
        }
        emit(start, n, curOr);
    }
    long long ans = 0;
    for (auto &[v, c] : dp) ans = (ans + c) % MOD;
    return ans;
}
