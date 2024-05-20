const k_e = 8.99e9; // постоянная Кулона в Н·м²/Кл²



export function computeFieldIntens(L: number, lambda: number) {
  const r = L / 2; // расстояние до середины нити
    const term1 = L / (2 * Math.sqrt(r * r + (L / 2) * (L / 2)));
    const E = (2 * k_e * lambda / r) * term1;
    return E;
}

export function computePoten(L: number, lambda: number) {
  const r = L / 2; // расстояние до середины нити
    const term1 = (L / 2) + Math.sqrt(r * r + (L / 2) * (L / 2));
    const Phi = 2 * k_e * lambda * Math.log(term1 / r);
    return Phi;
}
