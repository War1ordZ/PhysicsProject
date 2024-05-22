<script lang="ts">
  import Visual from './visual.svelte';

  let l = 1; // длина нити в метрах
  let λ = 1; // линейная плотность заряда в Кл/м
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
</script>

<main>
  <h1>Вычисление напряжённости и потенциала поля</h1>
  <div class="input-group">
    <label for="length">Длина нити (L), м:</label>
    <input id="length" type="number" bind:value={l} min="0.1" step="0.1" />
  </div>
  <div class="input-group">
    <label for="density">Линейная плотность заряда (λ), Кл/м:</label>
    <input id="density" type="number" bind:value={λ} min="0.1" step="0.1" />
  </div>
  <div>
    <h2>Результаты</h2>
    <!-- <p>Напряженность поля (E): {formatValue(E, 'Н/Кл')}</p>
    <p>Потенциал поля (V): {formatValue(V, 'В')}</p> -->
  </div>
  <Visual {l} {λ} />
</main>

<style>
  main {
    text-align: center;
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
