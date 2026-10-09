// Ограниченный рюкзак: предметы веса a в количестве c заменяем на O(log c) предметов a·1, a·2, a·4, ..., и остаток.
// Любое количество 0..c собирается из них, больше c — нет.
vector<int> splitBinary(int a, int c) {
    vector<int> res;
    for (int p = 1; c > 0; p <<= 1) { int t = min(p, c); res.push_back(a * t); c -= t; }
    return res;
}
