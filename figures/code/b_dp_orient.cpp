// Каждый день — ребро между проектами (s_i, t_i). Нужно ориентировать рёбра так, чтобы в каждой вершине входящих было столько же, сколько исходящих.
// Ребро направлено a→b: Алексей делает проект a, Иван — проект b (swap не нужен); b→a — нужен swap.
// Возможно ⇔ все степени чётны (проект встречается чётное число раз). Ориентация = направление обхода замкнутых маршрутов, найденных «пока есть свободное ребро».
vector<int> orientDays(int n, const vector<pair<int,int>> &e, bool &ok) {      // результат: swap[i] = 1, если в день i нужно поменяться
    vector<vector<pair<int,int>>> adj(n);
    vector<int> deg(n, 0);
    for (int i = 0; i < (int)e.size(); i++) {
        adj[e[i].first].push_back({e[i].second, i}); adj[e[i].second].push_back({e[i].first, i});
        deg[e[i].first]++; deg[e[i].second]++;
    }
    ok = true;
    for (int d : deg) if (d % 2) ok = false;
    vector<int> swp(e.size(), 0), ptr(n, 0);
    vector<char> used(e.size(), 0);
    if (!ok) return swp;
    for (int s = 0; s < n; s++) {
        for (;;) {                                           // выпускаем замкнутые маршруты из s, пока у s есть свободные рёбра
            while (ptr[s] < (int)adj[s].size() && used[adj[s][ptr[s]].second]) ptr[s]++;
            if (ptr[s] == (int)adj[s].size()) break;
            int v = s;
            for (;;) {
                while (ptr[v] < (int)adj[v].size() && used[adj[v][ptr[v]].second]) ptr[v]++;
                if (ptr[v] == (int)adj[v].size()) break;      // идти некуда: из-за чётных степеней мы вернулись в s
                auto [to, id] = adj[v][ptr[v]];
                used[id] = 1;
                swp[id] = (e[id].first != v);                 // шли v→to; если v — «второй» конец, значит порядок надо перевернуть
                if (e[id].first == e[id].second) swp[id] = 0;
                v = to;
            }
        }
    }
    return swp;
}
