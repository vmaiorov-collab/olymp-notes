//---- sieve_simple
const int A = 100000;
int lp[A + 1];                                   // lp[i] — наименьший простой делитель i (0, пока не найден)
void sieve_simple() {
    for (int i = 2; i <= A; i++)
        if (lp[i] == 0) {                        // i простое
            lp[i] = i;
            for (long long j = 1LL * i * i; j <= A; j += i)   // i*i считаем в long long: в int будет переполнение
                if (lp[j] == 0) lp[j] = i;
        }
}
//---- sieve_linear
const int A = 100000;
int lp[A + 1];
vector<int> primes;                              // найденные простые по возрастанию
void sieve_linear() {
    for (int i = 2; i <= A; i++) {
        if (lp[i] == 0) { lp[i] = i; primes.push_back(i); }
        for (int x : primes) {
            if (x > lp[i] || 1LL * i * x > A) break;   // нужно x ≤ lp(i), иначе c = i·x получится повторно
            lp[i * x] = x;                       // x — наименьший простой делитель числа i·x
        }
    }
}
//---- mult_sieve
const int A = 100000;
int lp[A + 1];
int e[A + 1];          // e[i]  — показатель наименьшего простого в i
int pw[A + 1];         // pw[i] — наибольшая степень наименьшего простого, делящая i  (p^e)
int sp[A + 1];         // sp[i] — 1 + p + … + p^e для этого простого (хватает и для A ≤ 1e5)
long long d[A + 1], sigma[A + 1], phi[A + 1];
void mult_sieve() {
    vector<int> primes;
    d[1] = sigma[1] = phi[1] = 1; pw[1] = 1;
    for (int i = 2; i <= A; i++) {
        if (lp[i] == 0) {                        // i простое: значения для p^1
            lp[i] = i; primes.push_back(i);
            e[i] = 1; pw[i] = i; sp[i] = i + 1;
            d[i] = 2; sigma[i] = i + 1; phi[i] = i - 1;
        }
        for (int x : primes) {
            if (x > lp[i] || 1LL * i * x > A) break;
            int c = i * x; lp[c] = x;
            if (x < lp[i]) {                     // x не делит i  ⇒  gcd(i, x) = 1: умножаем значения
                e[c] = 1; pw[c] = x; sp[c] = x + 1;
                d[c] = d[i] * 2; sigma[c] = sigma[i] * sp[c]; phi[c] = phi[i] * (x - 1);
            } else {                             // x = lp(i): показатель наименьшего простого вырос на 1
                e[c] = e[i] + 1; pw[c] = pw[i] * x; sp[c] = sp[i] * x + 1;
                int rest = c / pw[c];            // часть без наименьшего простого: она взаимно проста с p^e
                d[c] = d[rest] * (e[c] + 1);
                sigma[c] = sigma[rest] * sp[c];
                phi[c] = phi[i] * x;             // φ(p^k) = p·φ(p^(k−1)) при k ≥ 2
            }
        }
    }
}
//---- egcd
typedef long long ll;
// возвращает g = gcd(a, b) и числа x, y, для которых a·x + b·y = g
ll egcd(ll a, ll b, ll& x, ll& y) {
    if (b == 0) { x = 1; y = 0; return a; }
    ll x1, y1;
    ll g = egcd(b, a % b, x1, y1);               // b·x1 + (a mod b)·y1 = g
    x = y1;                                      // a mod b = a − ⌊a/b⌋·b  ⇒  подставляем и группируем по a и b
    y = x1 - (a / b) * y1;
    return g;
}
// обратный к a по модулю m (gcd(a, m) = 1), результат в [0, m)
ll inv(ll a, ll m) {
    ll x, y;
    egcd(a, m, x, y);                            // a·x + m·y = 1  ⇒  a·x ≡ 1 (mod m)
    return (x % m + m) % m;
}
//---- crt
// попарно взаимно простые модули m[i]; возвращает x mod M, M = ∏ m[i], с x ≡ a[i] (mod m[i])
ll crt(const vector<ll>& a, const vector<ll>& m) {
    ll M = 1;
    for (ll v : m) M *= v;
    ll x = 0;
    for (size_t i = 0; i < a.size(); i++) {
        ll Mi = M / m[i];                        // делится на все модули, кроме m[i]
        ll K = Mi * inv(Mi % m[i], m[i]) % M;    // K ≡ 1 (mod m[i]),  K ≡ 0 (mod остальным)
        x = (x + a[i] % M * K) % M;
    }
    return x;
}
//---- incl_excl
// сколько чисел из [1, N] взаимно просты с n: включения-исключения по простым делителям n
long long coprime_count(long long N, long long n) {
    vector<long long> ps;
    for (long long p = 2; p * p <= n; p++)
        if (n % p == 0) { ps.push_back(p); while (n % p == 0) n /= p; }
    if (n > 1) ps.push_back(n);
    long long res = 0;
    for (int mask = 0; mask < (1 << ps.size()); mask++) {   // подмножество простых; 2^k слагаемых, k ≤ 9 для n ≤ 1e9
        long long prod = 1; int bits = 0;
        for (size_t i = 0; i < ps.size(); i++)
            if (mask >> i & 1) { prod *= ps[i]; bits++; }
        res += (bits % 2 ? -1 : 1) * (N / prod);  // нечётные подмножества вычитаем
    }
    return res;
}
//---- binom
// C[n][k] по треугольнику Паскаля, C[n][k] = C[n−1][k−1] + C[n−1][k]
const int NMAX = 31;
long long C[2 * NMAX + 1][2 * NMAX + 1];
void build_binom() {
    for (int n = 0; n <= 2 * NMAX; n++) {
        C[n][0] = 1;
        for (int k = 1; k <= n; k++) C[n][k] = C[n - 1][k - 1] + (k <= n - 1 ? C[n - 1][k] : 0);
    }
}
long long catalan(int n) { return C[2 * n][n] - (n ? C[2 * n][n - 1] : 0); }   // = C(2n, n)/(n+1)
// непересекающиеся пары путей в таблице n×m (старты и финиши — как на рисунке), n, m ≥ 2
long long disjoint_pairs(int n, int m) {
    return C[n + m - 4][n - 2] * C[n + m - 4][n - 2] - C[n + m - 4][n - 1] * (n >= 3 ? C[n + m - 4][n - 3] : 0);
}
