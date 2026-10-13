#include <bits/stdc++.h>
using namespace std;
typedef long long ll;
const ll INF = LLONG_MAX / 4;

// Дейкстра на set: храним пары (расстояние, вершина), при улучшении удаляем старую пару
vector<ll> dijkstra_set(int n, const vector<vector<pair<int,int>>>& g, int s) {
    vector<ll> d(n, INF);
    set<pair<ll,int>> q;
    d[s] = 0; q.insert({0, s});
    while (!q.empty()) {
        int v = q.begin()->second;
        q.erase(q.begin());                      // вершина помечена: d[v] окончательно
        for (auto [u, w] : g[v])
            if (d[u] > d[v] + w) {
                q.erase({d[u], u});              // erase несуществующей пары безопасен
                d[u] = d[v] + w;
                q.insert({d[u], u});
            }
    }
    return d;
}

// Дейкстра на priority_queue: дубликаты пропускаем проверкой d != d[v]
vector<ll> dijkstra_pq(int n, const vector<vector<pair<int,int>>>& g, int s) {
    vector<ll> d(n, INF);
    priority_queue<pair<ll,int>, vector<pair<ll,int>>, greater<>> q;   // минимум наверху
    d[s] = 0; q.push({0, s});
    while (!q.empty()) {
        auto [dv, v] = q.top(); q.pop();
        if (dv != d[v]) continue;                // устаревшая копия
        for (auto [u, w] : g[v])
            if (d[u] > d[v] + w) { d[u] = d[v] + w; q.push({d[u], u}); }
    }
    return d;
}

// Дейкстра за O(n^2 + m): минимум ищем проходом по массиву
vector<ll> dijkstra_n2(int n, const vector<vector<pair<int,int>>>& g, int s) {
    vector<ll> d(n, INF);
    vector<char> used(n, 0);
    d[s] = 0;
    for (int it = 0; it < n; it++) {
        int v = -1;
        for (int i = 0; i < n; i++) if (!used[i] && (v == -1 || d[i] < d[v])) v = i;
        if (d[v] == INF) break;
        used[v] = 1;
        for (auto [u, w] : g[v]) d[u] = min(d[u], d[v] + w);
    }
    return d;
}

// 0-1 BFS на деке
vector<int> bfs01(int n, const vector<vector<pair<int,int>>>& g, int s) {
    vector<int> d(n, INT_MAX);
    deque<int> q; d[s] = 0; q.push_back(s);
    while (!q.empty()) {
        int v = q.front(); q.pop_front();
        for (auto [u, w] : g[v])
            if (d[u] > d[v] + w) {
                d[u] = d[v] + w;
                if (w == 0) q.push_front(u); else q.push_back(u);
            }
    }
    return d;
}

// BFS по весам 0..K на K+1 циклических очередях
vector<int> dial(int n, const vector<vector<pair<int,int>>>& g, int s, int K) {
    vector<int> d(n, INT_MAX);
    vector<queue<pair<int,int>>> q(K + 1);       // в очереди (расстояние, вершина)
    d[s] = 0; q[0].push({0, s});
    int pending = 1;                              // сколько записей лежит в очередях
    for (int cur = 0; pending > 0; cur = (cur + 1) % (K + 1)) {
        while (!q[cur].empty()) {
            auto [dv, v] = q[cur].front(); q[cur].pop(); pending--;
            if (dv != d[v]) continue;
            for (auto [u, w] : g[v])
                if (d[u] > d[v] + w) {
                    d[u] = d[v] + w;
                    q[d[u] % (K + 1)].push({d[u], u}); pending++;
                }
        }
    }
    return d;
}

// Флойд: d[a][b] = min(d[a][b], d[a][k] + d[k][b]); k — внешний цикл
vector<vector<ll>> floyd(int n, const vector<vector<ll>>& w) {
    auto d = w;
    for (int k = 0; k < n; k++)
        for (int a = 0; a < n; a++)
            for (int b = 0; b < n; b++)
                if (d[a][k] < INF && d[k][b] < INF) d[a][b] = min(d[a][b], d[a][k] + d[k][b]);
    return d;
}

int main() {
    mt19937 rng(17);
    for (int it = 0; it < 3000; it++) {
        int n = rng() % 8 + 1, m = rng() % 20, K = rng() % 4 + 1;
        vector<vector<pair<int,int>>> g(n), g01(n), gK(n);
        vector<vector<ll>> w(n, vector<ll>(n, INF));
        for (int i = 0; i < n; i++) w[i][i] = 0;
        for (int i = 0; i < m; i++) {
            int a = rng() % n, b = rng() % n, c = rng() % 10;
            g[a].push_back({b, c}); w[a][b] = min<ll>(w[a][b], c);
            g01[a].push_back({b, (int)(rng() % 2)});
            gK[a].push_back({b, (int)(rng() % (K + 1))});
        }
        auto fl = floyd(n, w);
        auto d1 = dijkstra_set(n, g, 0), d2 = dijkstra_pq(n, g, 0), d3 = dijkstra_n2(n, g, 0);
        for (int v = 0; v < n; v++)
            if (d1[v] != fl[0][v] || d2[v] != fl[0][v] || d3[v] != fl[0][v]) { puts("FAIL dijkstra"); return 1; }
        // 0-1 и Dial сверяем с Дейкстрой на тех же графах
        auto b01 = bfs01(n, g01, 0);
        auto dd = dial(n, gK, 0, K);
        auto r01 = dijkstra_pq(n, [&]{ vector<vector<pair<int,int>>> h = g01; return h; }(), 0);
        auto rK = dijkstra_pq(n, gK, 0);
        for (int v = 0; v < n; v++) {
            ll e1 = r01[v] == INF ? INT_MAX : r01[v], e2 = rK[v] == INF ? INT_MAX : rK[v];
            if (b01[v] != e1 || dd[v] != e2) { puts("FAIL bfs"); return 1; }
        }
    }
    puts("ok");
}
