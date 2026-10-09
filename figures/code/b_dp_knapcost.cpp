// Рюкзак: максимум стоимости при суммарном весе ≤ B. Если вес большой, а сумма стоимостей мала, меняем параметр и значение местами:
// dp[c] — минимальный вес, которым можно набрать стоимость ровно c;  ответ — максимальное c с dp[c] ≤ B.
typedef long long ll;
ll knapsackByCost(const vector<int> &w, const vector<int> &cost, ll B) {
    int total = accumulate(cost.begin(), cost.end(), 0);
    const ll INF = LLONG_MAX / 4;
    vector<ll> dp(total + 1, INF);
    dp[0] = 0;
    for (size_t i = 0; i < w.size(); i++)
        for (int c = total; c >= cost[i]; c--)                  // c по убыванию — предмет берётся не более одного раза
            dp[c] = min(dp[c], dp[c - cost[i]] + w[i]);
    ll best = 0;
    for (int c = 0; c <= total; c++) if (dp[c] <= B) best = c;
    return best;
}
