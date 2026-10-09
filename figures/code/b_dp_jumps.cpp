// Прыжки вправо: первый прыжок длины d, каждый следующий длиннее/такой же/короче на 1 (длина ≥ 1). Монеты лежат в клетках; максимум собранного (старт в 0).
// Сумма длин ≥ 1+2+...+k, поэтому длина отличается от d не более чем на ~√(2·M) (M — число клеток): храним только «окно» длин вокруг d.
int maxCoins(int M, int d, const vector<int> &coin) {          // coin[x] — монет в клетке x (0..M)
    const int OFF = 250;                                        // для M ≤ 30000: |длина − d| ≤ 245
    vector<vector<int>> dp(M + 1, vector<int>(2 * OFF + 1, -1));
    int ans = 0;
    if (d <= M) dp[d][OFF] = coin[d];
    for (int x = d; x <= M; x++)
        for (int o = 0; o <= 2 * OFF; o++) {
            if (dp[x][o] < 0) continue;
            ans = max(ans, dp[x][o]);
            int len = d + o - OFF;
            for (int nl = len - 1; nl <= len + 1; nl++) {
                if (nl < 1) continue;
                int no = nl - d + OFF;
                if (no < 0 || no > 2 * OFF || x + nl > M) continue;
                dp[x + nl][no] = max(dp[x + nl][no], dp[x][o] + coin[x + nl]);
            }
        }
    return ans;
}
