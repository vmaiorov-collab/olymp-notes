// Сколько способов разрезать массив на отрезки с положительной суммой (по модулю MOD)?
// dp[i] = Σ dp[j] по j < i с P[j] < P[i];  Фенвик по сжатым префиксным суммам P.
const long long MOD = 998244353;
long long countSplits(const vector<long long> &a) {
    int n = a.size();
    vector<long long> P(n + 1, 0);
    for (int i = 0; i < n; i++) P[i + 1] = P[i] + a[i];
    vector<long long> vals(P);                               // сжатие координат: порядок сохраняется
    sort(vals.begin(), vals.end()); vals.erase(unique(vals.begin(), vals.end()), vals.end());
    int m = vals.size();
    vector<long long> bit(m + 1, 0);
    auto add = [&](int i, long long x) { for (i++; i <= m; i += i & -i) bit[i] = (bit[i] + x) % MOD; };
    auto pref = [&](int i) { long long r = 0; for (; i > 0; i -= i & -i) r = (r + bit[i]) % MOD; return r; };   // сумма по индексам < i
    auto id = [&](long long p) { return int(lower_bound(vals.begin(), vals.end(), p) - vals.begin()); };
    add(id(P[0]), 1);                                        // dp[0] = 1: пустой префикс
    long long dp = 1;
    for (int i = 1; i <= n; i++) {
        dp = pref(id(P[i]));                                 // все j с P[j] < P[i]
        add(id(P[i]), dp);
    }
    return dp;                                               // dp[n]
}
