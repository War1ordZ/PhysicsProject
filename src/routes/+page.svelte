<script lang="ts">
  import Visual from './visual.svelte';
  import { calculateFieldAndPotential } from './physics';

  let l = 1; // длина нити в метрах
  let λ = 1; // линейная плотность заряда в Кл/м
  let x = 0;
  let y = 1;

  let [Ex, Ey, phi] = [0, 0, 0];

  let controls_toggled = true;
  // let E = 0;
  // let V = 0;

  function formatValue(value: number, unit: string) {
    if (Math.abs(value) >= 1e9) {
      return `${(value / 1e9).toFixed(2)} Г${unit}`;
    } else if (Math.abs(value) >= 1e6) {
      return `${(value / 1e6).toFixed(2)} М${unit}`;
    } else if (Math.abs(value) >= 1e3) {
      return `${(value / 1e3).toFixed(2)} к${unit}`;
    } else if (Math.abs(value) < 1e-3) {
      return `${(value * 1e6).toFixed(2)} мк${unit}`;
    } else if (Math.abs(value) < 1) {
      return `${(value * 1e3).toFixed(2)} м${unit}`;
    } else if (Math.abs(value) < 1e-6) {
      return `${(value * 1e9).toFixed(2)} н${unit}`;
    }
    return `${value.toFixed(2)} ${unit}`;
  }

  setInterval(() => {
    const [new_Ex, new_Ey, new_phi] = calculateFieldAndPotential(l, λ, x, y);
    Ex = new_Ex ?? 0;
    Ey = new_Ey ?? 0;
    phi = new_phi ?? 0;

    console.log(Ex, Ey);
  }, 100);
</script>

<main>
  <div class="controls-container">
    <div class={`controls ${controls_toggled ? 'active' : 'hidden'}`}>
      <h1>Вычисление напряжённости и потенциала поля</h1>
      <h3>Параметры симуляции</h3>
      <div class="input-group">
        <label for="length">Длина нити (L), <strong>м</strong>:</label>
        <input id="length" type="number" bind:value={l} min="0.1" step="0.1" />
      </div>
      <div class="input-group">
        <label for="density">Линейная плотность заряда (λ), <strong>Кл/м</strong>:</label>
        <input id="density" type="number" bind:value={λ} min="0.1" step="0.1" />
      </div>
      <h3>Расчёт напряжённости и потенциала в точке</h3>
      <div class="input-group">
        <label for="x-coordinate">Координата X, <strong>м</strong>:</label>
        <input id="x-coordinate" type="number" bind:value={x} step="0.1" />
      </div>
      <div class="input-group">
        <label for="x-coordinate">Координата Y, <strong>м</strong>:</label>
        <input id="x-coordinate" type="number" bind:value={y} step="0.1" />
      </div>
      <div class="input-group">
        <label for="potential">Потенциал поля:</label>
        <input id="x-coordinate" type="text" value={formatValue(phi, 'В')} disabled />
      </div>
      <div class="input-group">
        <label for="potential">Модуль вектора напряжённости:</label>
        <input id="x-coordinate" type="text" value={formatValue(Math.sqrt(Ex * Ex + Ey * Ey), 'Н/Кл')} disabled />
      </div>
      <h3>Формулы для расчёта</h3>
      <img src={`https://latex.codecogs.com/svg.image?\\varphi=\\int_{${-l}}^{${l}}\\frac{\\lambda dx}{4\\pi\\epsilon_0\\sqrt{(x-(${x}))^2+(${y})^2}}=${phi}\\text{ V}`} alt="varphi">
      <br>
      <img src={`https://latex.codecogs.com/svg.image?\\overline{E}_x=\\int_{${-l}}^{${l}}\\frac{k\\lambda((${x})-x)}{(((${x})-x^2)-(${y})^2)^{\\frac{3}{2}}}dx=${-Ex}\\text{ N/C}`} alt="varphi">
      <br>
      <img src={`https://latex.codecogs.com/svg.image?\\overline{E}_y=\\int_{${-l}}^{${l}}\\frac{k\\lambda(${y})}{(((${x})-x^2)-(${y})^2)^{\\frac{3}{2}}}dx=${Ey}\\text{ N/C}`} alt="varphi">

      <img class="cross" src="cross.svg" alt="cross" on:click={() => controls_toggled = false} />

    </div>
  </div>
  <img class="settings" src="settings.svg" alt="setting" on:click={() => controls_toggled = true} />
  <Visual {l} {λ} />
</main>

<style>
    main {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        text-align: center;
        overflow-x: hidden;
    }

    h1 {
        margin-bottom: 30px;
    }

    h3 {
        margin-bottom: 20px;
    }

    .vector-display {
        top: -110px;
        left: 350px;
        position: relative;
    }

    .circle {
        position: absolute;
        width: 60px;
        height: 60px;
    }

    .arrow {
        top: 10px;
        left: 10px;
        position: absolute;
        width: 40px;
        height: 40px;
    }

    .controls-container {
        z-index: 1000;
        position: absolute;
        top: 0;
        bottom: 0;
        left: 0;
        right: 0;
        display: flex;
        justify-content: center;
        align-items: center;
        pointer-events: none;
    }

    .controls {
        box-sizing: border-box;
        pointer-events: all;
        position: relative;
        height: 100%;
        width: 700px;
        z-index: 1000;
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        justify-content: flex-start;
        background: #ffffff;
        padding: 40px;
        border-right: 2px solid #e4e4e4;
        border-left: 2px solid #e4e4e4;
    }

    .controls.active {
        opacity: 1;
    }

    .controls.hidden {
        opacity: 0;
        visibility: hidden;
    }

    .settings {
        height: 40px;
        width: 40px;
        position: absolute;
        top: 40px;
        right: 50px;
        cursor: pointer;
        z-index: 500;
        opacity: 0.7;
        transition: all 0.3s;
    }

    .settings:hover {
        opacity: 0.8;
        transform: scale(1.1) rotate(90deg);
    }

    .cross {
        height: 20px;
        width: 20px;
        position: absolute;
        top: 20px;
        right: 20px;
        cursor: pointer;
        opacity: 0.6;
    }

    .cross:hover {
        opacity: 1;
    }

    .input-group {
        margin-bottom: 1em;
    }

    canvas {
        display: block;
        width: 100%;
        height: 100vh;
    }
</style>
