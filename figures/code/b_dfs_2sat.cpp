// 2-SAT. Переменная i: вершина 2i — «x_i истинна», 2i+1 — «x_i ложна»; отрицание = XOR с 1.
struct TwoSat {
    int n;
    SCC scc;
    TwoSat(int n) : n(n), scc(2 * n) {}
    // литерал: номер вершины (2*i или 2*i+1).  Дизъюнкт (a ∨ b) = (¬a → b) ∧ (¬b → a)
    void addOr(int a, int b) { scc.addEdge(a ^ 1, b); scc.addEdge(b ^ 1, a); }
    static int lit(int var, bool value) { return 2 * var + (value ? 0 : 1); }
    bool solve(vector<bool> &ans) {
        scc.run();
        ans.assign(n, false);
        for (int i = 0; i < n; i++) {
            if (scc.comp[2 * i] == scc.comp[2 * i + 1]) return false;     // x и ¬x в одной компоненте — решения нет
            // comp идёт от стоков к истокам; true получает та вершина, которая встречается в топсорте ПОЗЖЕ, то есть имеет меньший comp
            ans[i] = scc.comp[2 * i] < scc.comp[2 * i + 1];
        }
        return true;
    }
};
