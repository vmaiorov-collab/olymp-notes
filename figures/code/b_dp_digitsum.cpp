// Сколько чисел от 0 до R (R — строка цифр) имеют сумму цифр ровно S?  Для отрезка [L, R]: f(R) − f(L − 1).
// dp[i][s][t]: собрали i цифр, сумма s, t = 1, если префикс уже строго меньше префикса R.
typedef long long ll;
ll countDigitSum(const string &R, int S) {
    int n = R.size();
    vector<vector<array<ll,2>>> dp(n + 1, vector<array<ll,2>>(S + 1, {0, 0}));
    dp[0][0][0] = 1;
    for (int i = 0; i < n; i++)
        for (int s = 0; s <= S; s++)
            for (int t = 0; t < 2; t++) {
                ll cur = dp[i][s][t];
                if (!cur) continue;
                int lim = t ? 9 : R[i] - '0';                  // если ещё равны R, следующая цифра ≤ цифры R; иначе любая
                for (int d = 0; d <= lim && s + d <= S; d++)
                    dp[i + 1][s + d][t || d < lim] += cur;
            }
    return dp[n][S][0] + dp[n][S][1];
}
