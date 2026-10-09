// Запросы (L, R, W): можно ли набрать вес W предметами с номерами из [L, R]?  dp[i][s] — максимальное g такое, что из предметов g..i можно набрать s (−1, если нельзя).
// Чем больше предметов берём (g меньше), тем больше сумм достижимо — монотонность по g.
const int SM = 1000;
struct SegKnap {
    int n; vector<array<int, SM + 1>> dp;
    SegKnap(const vector<int> &w) : n(w.size()), dp(w.size() + 1) {
        dp[0].fill(-1); dp[0][0] = 1 << 30;                    // пустой набор даёт сумму 0 при любом g
        for (int i = 1; i <= n; i++)
            for (int s = 0; s <= SM; s++) {
                if (s == 0) { dp[i][0] = 1 << 30; continue; }  // сумма 0 набирается пустым набором при любом g
                int best = dp[i - 1][s];                       // предмет i не берём
                if (s >= w[i - 1] && dp[i - 1][s - w[i - 1]] >= 0) best = max(best, min(dp[i - 1][s - w[i - 1]], i));    // берём i
                dp[i][s] = best;
            }
    }
    bool query(int L, int R, int W) { return dp[R][W] >= L; }  // номера предметов 1..n
};
