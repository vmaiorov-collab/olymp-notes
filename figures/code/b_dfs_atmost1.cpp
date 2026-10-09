// «Не более одной истинной среди x_0..x_{k-1}» за O(k) дизъюнктов: вводим префиксные переменные p_i = «среди x_0..x_i есть истинная».
// Переменные x_i имеют номера xv + i, префиксные — pv + i (место под них нужно выделить в TwoSat заранее).
void atMostOne(TwoSat &T, int xv, int pv, int k) {
    for (int i = 0; i < k; i++) {
        T.addOr(TwoSat::lit(xv + i, false), TwoSat::lit(pv + i, true));                        // x_i → p_i
        if (i + 1 < k) {
            T.addOr(TwoSat::lit(pv + i, false), TwoSat::lit(pv + i + 1, true));                // p_i → p_{i+1}
            T.addOr(TwoSat::lit(pv + i, false), TwoSat::lit(xv + i + 1, false));               // p_i → ¬x_{i+1}
        }
    }
}
