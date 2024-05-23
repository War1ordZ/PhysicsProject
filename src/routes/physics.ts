// physics.ts

export const k = 8.99e9;  // N m^2/C^2

export function calculateFieldAndPotential(l: number, lambda: number, xP: number, yP: number, zP: number = 0): [number, number, number] {
    const x = linspace(-l, l, 100);
    
    const dEx = x.map(xi => k * lambda * (xi - xP) / ((xi - xP)**2 + yP**2 + zP**2)**(3/2));
    const dEy = x.map(xi => k * lambda * yP / ((xi - xP)**2 + yP**2 + zP**2)**(3/2));
    // const dEz = x.map(xi => k * lambda * zP / ((xi - xP)**2 + yP**2 + zP**2)**(3/2));
    
    const Ex = trapz(dEx, x);
    const Ey = trapz(dEy, x);
    // const Ez = trapz(dEz, x);
    
    // const E = Math.sqrt(Ex**2 + Ey**2 + Ez**2);
    
    const dphi = x.map(xi => k * lambda / Math.sqrt((xi - xP)**2 + yP**2 + zP**2));
    const phi = trapz(dphi, x);
    
    return [Ex, Ey, phi];
}

function linspace(start: number, end: number, num: number): number[] {
    const step = (end - start) / (num - 1);
    return Array.from({ length: num }, (v, k) => start + k * step);
}

function trapz(y: number[], x: number[]): number {
    const n = y.length;
    let sum = 0;
    for (let i = 0; i < n - 1; i++) {
        sum += 0.5 * (y[i] + y[i + 1]) * (x[i + 1] - x[i]);
    }
    return sum;
}
