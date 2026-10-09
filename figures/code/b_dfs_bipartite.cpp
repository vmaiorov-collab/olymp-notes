// Нечётный цикл: красим граф в два цвета DFS-ом, стек вершин хранится в path. Возвращает вершины цикла нечётной длины или пустой список.
bool findOdd(const vector<vector<int>> &g, int v, int p, vector<int> &color, vector<int> &path, vector<int> &cycle) {
    color[v] = (p < 0) ? 1 : 3 - color[p];                    // цвета 1 и 2: у потомка цвет противоположный родителю
    path.push_back(v);
    for (int to : g[v]) {
        if (to == p) continue;
        if (color[to] == 0) { if (findOdd(g, to, v, color, path, cycle)) return true; }
        else if (color[to] == color[v]) {                     // сосед того же цвета; он уже на стеке path — снимаем вершины до него
            int i = (int)path.size() - 1;
            while (path[i] != to) i--;
            cycle.assign(path.begin() + i, path.end());
            return true;
        }
    }
    path.pop_back();
    return false;
}
vector<int> oddCycle(const vector<vector<int>> &g) {
    int n = g.size();
    vector<int> color(n, 0), path, cycle;
    for (int v = 0; v < n; v++) if (!color[v] && findOdd(g, v, -1, color, path, cycle)) return cycle;
    return {};
}
