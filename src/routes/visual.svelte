<script lang="ts">
  import { onMount } from 'svelte';
  // import Plotly from 'plotly.js-dist';
  import { calculateFieldAndPotential } from './physics';
  let Plotly: any = null;

  export let l: number;
  export let λ: number;

  let div: HTMLDivElement;

  const graph = async (l: number, λ: number) => {
    const x = linspace(-2 * l, 2 * l, 50);
    const y = linspace(-2 * l, 2 * l, 50);
    const { X, Y } = meshgrid(x, y);
    const Ex_grid: number[][] = [];
    const Ey_grid: number[][] = [];
    const phi_grid: number[][] = [];

    for (let i = 0; i < X.length; i++) {
      Ex_grid.push([]);
      Ey_grid.push([]);
      phi_grid.push([]);
      for (let j = 0; j < X[i].length; j++) {
        const [Ex, Ey, phi] = calculateFieldAndPotential(l, λ, X[i][j], Y[i][j]);
        Ex_grid[i].push(Ex);
        Ey_grid[i].push(Ey);
        phi_grid[i].push(phi);

      }
      // console.log(phi_grid);
    }

    const data = [
      {
        z: phi_grid,
        x: x,
        y: y,
        type: 'contour',
        colorscale: 'RdBu',
        colorbar: {
          title: 'Потенциал (В)'
        }
      },
      {
        type: 'scatter',
        mode: 'lines',
        x: linspace(-l, l, 1000),
        y: Array(1000).fill(0),
        line: {
          color: 'black',
          width: 2
        },
        name: 'Заряженная нить'
      },
      {
        type: 'scatter',
        mode: 'markers',
        x: X.flat(),
        y: Y.flat(),
        marker: {
          size: 7,
          color: '000000cc  ',
          symbol: 'arrow-open',
          // angleref: 'previous',
          angle: flatten(Ex_grid).map(
            (Ex, idx) => (Math.atan2(flatten(Ey_grid)[idx], Ex) * 180 + 270) / Math.PI
          ),
          sizemode: 'scaled',
          sizeref: 2.5,
          sizemin: 0.5,
          sizemax: 10
        },
        name: 'Векторы поля'
      }
    ];

    const layout = {
      title: 'Визуализация предметной области',
      xaxis: { title: 'X', range: [-l * 1.5, l * 1.5] },
      yaxis: { title: 'Y', range: [-l * 0.75, l * 0.75]} ,
      showlegend: false
    };
    Plotly.newPlot(div, data, layout);
  };

  function linspace(start: number, end: number, num: number): number[] {
    const step = (end - start) / (num - 1);
    return Array.from({ length: num }, (v, k) => start + k * step);
  }

  function meshgrid(x: number[], y: number[]): { X: number[][]; Y: number[][] } {
    const X = [];
    const Y = [];
    for (let i = 0; i < y.length; i++) {
      Y.push(x.slice());
    }
    for (let j = 0; j < x.length; j++) {
      X.push(Array.from({ length: y.length }, () => y[j]));
    }
    return { X: Y, Y: X };
  }

  function flatten(arr: number[][]): number[] {
    return arr.reduce((flat, next) => flat.concat(next), []);
  }

  onMount(async () => {
    Plotly = await import('plotly.js-dist');
  });

  $: if (div && Plotly) graph(l, λ);
</script>

<div bind:this={div} class="graph"></div>

<style>
  .graph {
      position: absolute;
      top: 0;
      bottom: 0;
      left: 0;
      right: 0;
  }
</style>
