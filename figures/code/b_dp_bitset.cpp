// Рюкзак «можно ли набрать вес ровно s» для всех s ≤ SMAX, bitset: новый слой = старый | (старый << w).
const int SMAX = 10000;
vector<bool> reachableSums(const vector<int> &w) {
    bitset<SMAX + 1> dp;
    dp[0] = 1;
    for (int x : w) dp |= dp << x;                              // 64 состояния за одну операцию процессора
    vector<bool> res(SMAX + 1);
    for (int s = 0; s <= SMAX; s++) res[s] = dp[s];
    return res;
}
