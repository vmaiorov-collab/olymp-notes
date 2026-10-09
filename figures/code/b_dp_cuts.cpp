// Бревно длиной xs.back(), отсечки xs[0]=0 < xs[1] < ... < xs[m]. Разрез бревна длины ℓ стоит ℓ. dp[l][r] — минимальная стоимость разрезать кусок между отсечками l и r полностью.
typedef long long ll;
ll cutLog(const vector<ll> &xs) {
    int m = xs.size();                                         // отсечек m (включая концы)
    vector<vector<ll>> dp(m, vector<ll>(m, 0));
    for (int len = 2; len < m; len++)                          // по возрастанию длины отрезка отсечек
        for (int l = 0; l + len < m; l++) {
            int r = l + len; dp[l][r] = LLONG_MAX;
            for (int k = l + 1; k < r; k++)                    // первый разрез проводим по отсечке k
                dp[l][r] = min(dp[l][r], xs[r] - xs[l] + dp[l][k] + dp[k][r]);
        }
    return dp[0][m - 1];
}
