// Сколько x ∈ [0, R], делящихся на каждую свою ненулевую цифру?  Состояние: (позиция, флаг «меньше R», НОК цифр (48 делителей 2520), остаток по модулю 2520).
typedef long long ll;
ll countDivisibleByDigits(const string &R) {
    vector<int> divs; for (int d = 1; d <= 2520; d++) if (2520 % d == 0) divs.push_back(d);
    int D = divs.size();
    vector<int> id(2521, -1); for (int i = 0; i < D; i++) id[divs[i]] = i;
    int n = R.size();
    auto lcm = [](int a, int b) { return a / gcd(a, b) * b; };
    // dp[флаг][индекс НОК][остаток]
    vector<vector<vector<ll>>> cur(2, vector<vector<ll>>(D, vector<ll>(2520, 0))), nxt = cur;
    cur[0][id[1]][0] = 1;
    for (int i = 0; i < n; i++) {
        for (auto &a : nxt) for (auto &b : a) fill(b.begin(), b.end(), 0);
        for (int t = 0; t < 2; t++) for (int li = 0; li < D; li++) for (int r = 0; r < 2520; r++) {
            ll c = cur[t][li][r]; if (!c) continue;
            int lim = t ? 9 : R[i] - '0';
            for (int d = 0; d <= lim; d++) {
                int nl = d ? id[lcm(divs[li], d)] : li;
                nxt[t || d < lim][nl][(r * 10 + d) % 2520] += c;
            }
        }
        swap(cur, nxt);
    }
    ll ans = 0;
    for (int t = 0; t < 2; t++) for (int li = 0; li < D; li++) for (int r = 0; r < 2520; r++)
        if (cur[t][li][r] && r % divs[li] == 0) ans += cur[t][li][r];   // остаток по 2520 делится на НОК ⇒ число делится на НОК
    return ans;
}
