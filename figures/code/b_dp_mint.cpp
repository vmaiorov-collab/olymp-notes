// Число по модулю: все операции сами берут остаток, сложение и вычитание — без деления (условное вычитание).
const int MOD = 1000000007;
struct Mint {
    int x;                                                      // всегда 0 <= x < MOD
    Mint(long long v = 0) { x = (int)(v % MOD); if (x < 0) x += MOD; }
    Mint operator+(Mint o) const { int r = x + o.x; if (r >= MOD) r -= MOD; Mint m; m.x = r; return m; }   // сумма < 2·MOD помещается в int
    Mint operator-(Mint o) const { int r = x - o.x; if (r < 0) r += MOD; Mint m; m.x = r; return m; }
    Mint operator*(Mint o) const { Mint m; m.x = (int)((long long)x * o.x % MOD); return m; }       // умножать нужно в long long
    Mint &operator+=(Mint o) { return *this = *this + o; }
};
// Мемоизация: функция возвращает значение состояния; уже вычисленное берём из таблицы.
// Пример — число путей из (0,0) в (n,m) по клеткам вправо/вниз.
long long memo[50][50];
long long paths(int i, int j) {
    if (i == 0 || j == 0) return 1;
    long long &r = memo[i][j];                                  // ссылка на ячейку: запись значения при выходе
    if (r) return r;                                            // уже считали
    return r = paths(i - 1, j) + paths(i, j - 1);
}
