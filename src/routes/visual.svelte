<script lang="ts">
  import { onMount } from 'svelte';
  import * as THREE from 'three';
  import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';

  export let L = 2; // длина нити в метрах
  export let λ = 3; // линейная плотность заряда в Кл/м
  export let E = 0;
  export let V = 0;

  const minDistance = 1e-6; // минимальное расстояние для вычислений, чтобы избежать деления на ноль
  const k_e = 8.99e9; // постоянная Кулона в Н·м²/Кл²

  let container: HTMLDivElement;
  let scene: THREE.Scene,
      camera: THREE.PerspectiveCamera,
      renderer: THREE.WebGLRenderer,
      controls: OrbitControls;

  onMount(() => {
    init();
    animate();
    updateVisualization();
  });

  function init() {
    // Создание сцены
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0xffffff);

    // Камера
    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.set(0, 0, 10);

    // Рендерер
    renderer = new THREE.WebGLRenderer();
    renderer.setSize(window.innerWidth, window.innerHeight);
    container.appendChild(renderer.domElement);

    // Контроллеры
    controls = new OrbitControls(camera, renderer.domElement);

    // Свет
    const ambientLight = new THREE.AmbientLight(0x404040);
    scene.add(ambientLight);

    const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
    directionalLight.position.set(5, 5, 5).normalize();
    scene.add(directionalLight);
  }

  $: updater(L, λ);

  const updater = (L: number, λ: number) => {
    if (scene) updateVisualization();
  };

  function updateVisualization() {
    // Очистка предыдущих объектов
    while (scene.children.length > 0) {
      scene.remove(scene.children[0]);
    }

    // Создание нити
    const lineMaterial = new THREE.LineBasicMaterial({ color: 0x0000ff });
    const lineGeometry = new THREE.BufferGeometry().setFromPoints([
      new THREE.Vector3(-L / 2, 0, 0),
      new THREE.Vector3(L / 2, 0, 0)
    ]);
    const line = new THREE.Line(lineGeometry, lineMaterial);
    scene.add(line);

    // Создание заряда
    const chargeMaterial = new THREE.MeshBasicMaterial({ color: 0xff0000 });
    const chargeGeometry = new THREE.SphereGeometry(0.05, 32, 32);

    for (let i = -L / 2; i <= L / 2; i += 0.1) {
      const charge = new THREE.Mesh(chargeGeometry, chargeMaterial);
      charge.position.set(i, 0, 0);
      scene.add(charge);
    }

    // Визуализация силовых линий и эквипотенциальных линий
    visualizeFieldAndPotential(L, λ);
  }

  function createTextSprite(message: string) {
    const canvas = document.createElement('canvas');
    const context = canvas.getContext('2d');
    if (!context) throw new Error('no context');

    context.font = 'Bold 20px Arial';
    context.fillStyle = 'rgba(0, 0, 0, 1.0)';
    context.fillText(message, 0, 20);

    const texture = new THREE.CanvasTexture(canvas);
    const spriteMaterial = new THREE.SpriteMaterial({ map: texture });
    const sprite = new THREE.Sprite(spriteMaterial);
    sprite.scale.set(2, 1, 1);
    return sprite;
  }

  function animate() {
    requestAnimationFrame(animate);
    controls.update();
    renderer.render(scene, camera);
  }

  function computeFieldIntensity(L: number, lambda: number, x: number, y: number): { Ex: number, Ey: number } {
    const halfL = L / 2;
    const dx = 0.1; // шаг по длине нити
    let Ex = 0;
    let Ey = 0;

    for (let i = -halfL; i <= halfL; i += dx) {
      const r = Math.sqrt((x - i) * (x - i) + y * y);
      if (r < minDistance) continue; // избегаем деления на ноль
      const Exi = k_e * lambda * (x - i) / (r * r * r);
      const Eyi = k_e * lambda * y / (r * r * r);
      Ex += Exi;
      Ey += Eyi;
    }

    return { Ex, Ey };
  }

  function computePotential(L: number, lambda: number, x: number, y: number): number {
    const halfL = L / 2;
    const dx = 0.1; // шаг по длине нити
    let V = 0;

    for (let i = -halfL; i <= halfL; i += dx) {
      const r = Math.sqrt((x - i) * (x - i) + y * y);
      if (r < minDistance) continue; // избегаем деления на ноль
      V += k_e * lambda * dx / r;
    }

    return V;
  }

  function visualizeFieldAndPotential(L: number, lambda: number) {
    const gridSize = 10;
    const step = 1;

    for (let x = -gridSize; x <= gridSize; x += step) {
      for (let y = -gridSize; y <= gridSize; y += step) {
        const { Ex, Ey } = computeFieldIntensity(L, λ, x, y);
        const V = computePotential(L, λ, x, y);

        // Визуализация векторов напряженности
        const arrowLength = Math.sqrt(Ex * Ex + Ey * Ey) * 0.1; // уменьшаем длину стрелок для лучшей визуализации
        const arrowDir = new THREE.Vector3(Ex, Ey, 0).normalize();
        const arrowStart = new THREE.Vector3(x, y, 0);
        const arrow = new THREE.ArrowHelper(arrowDir, arrowStart, arrowLength, 0x000000);
        scene.add(arrow);

        // Визуализация эквипотенциальных линий
        if (Math.abs(V) < 100) {
          const potentialMaterial = new THREE.LineBasicMaterial({ color: 0x00ff00 });
          const potentialGeometry = new THREE.BufferGeometry().setFromPoints([
            new THREE.Vector3(x - step / 2, y - step / 2, 0),
            new THREE.Vector3(x + step / 2, y + step / 2, 0)
          ]);
          const potentialLine = new THREE.Line(potentialGeometry, potentialMaterial);
          scene.add(potentialLine);
        }
      }
    }
  }
</script>

<main>
  <h1>Вычисление напряжённости и потенциала поля</h1>
  <div class="input-group">
    <label for="length">Длина нити (L), м:</label>
    <input
      id="length"
      type="number"
      bind:value={L}
      min="0.1"
      step="0.1"
      on:input={updateVisualization}
    />
  </div>
  <div class="input-group">
    <label for="density">Линейная плотность заряда (λ), Кл/м:</label>
    <input
      id="density"
      type="number"
      bind:value={λ}
      min="0.1"
      step="0.1"
      on:input={updateVisualization}
    />
  </div>
  <div>
    <h2>Результаты</h2>
    <p>Напряженность поля (E): {E} Н/Кл</p>
    <p>Потенциал поля (V): {V} В</p>
  </div>
  <div bind:this={container}></div>
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
