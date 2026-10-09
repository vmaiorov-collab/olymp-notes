// Сколько способов раздать ровно K конфет детям, если i-й готов съесть не более a_i (можно ничего не дать)?  Ответ по модулю MOD.
// dp[i][k] = Σ_{t=0..min(a_i,k)} dp[i−1][k−t]  — сумма в скользящем окне; пересчёт за O(1) вместо O(a_i).
const long long MOD = 998244353;
long long candyWays(const vector<int> &a, int K) {
    vector<long long> prev(K + 1, 0), cur(K + 1, 0);
    prev[0] = 1;
    for (int ai : a) {
        cur[0] = prev[0];
        for (int k = 1; k <= K; k++) {
            cur[k] = (cur[k - 1] + prev[k]) % MOD;              // окно [k−ai, k] получено из окна [k−1−ai, k−1] сдвигом на 1
            if (k - ai - 1 >= 0) cur[k] = (cur[k] - prev[k - ai - 1] + MOD) % MOD;     // выпавший слева элемент вычитаем
        }
        swap(prev, cur);
    }
    return prev[K];
}
