import * as THREE from 'three';
import { GLTFLoader } from 'GLTFLoader';
import { OrbitControls } from 'OrbitControls';

let scene, camera, renderer, controls;

try {
    init();
} catch (error) {
    console.error('Error in init:', error);
}

try {
    animate();
} catch (error) {
    console.error('Error in animate:', error);
}

function init() {
    // Создаем сцену
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0x808080); // Черный фон

    // Добавляем сетку для ориентации
    const gridHelper = new THREE.GridHelper(100, 100);
    gridHelper.position.y = -0.5; // Сетка под моделью
    scene.add(gridHelper);

    // Создаем камеру
    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.set(0, 10, 20); // Отодвигаем камеру для лучшего обзора

    // Создаем рендерер
    renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.shadowMap.enabled = true; // Включаем тени
    document.getElementById('container').appendChild(renderer.domElement);

    // Добавляем окружение (Ambient Light) для базового освещения
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);  // Усиливаем рассеянное освещение
    scene.add(ambientLight);

    // Добавляем направленный свет (Directional Light) для создания теней и более четкого освещения
    const directionalLight = new THREE.DirectionalLight(0xffffff, 1); // Яркий направленный свет
    directionalLight.position.set(10, 20, 10);
    directionalLight.castShadow = true;
    directionalLight.shadow.mapSize.width = 4096; // Увеличиваем качество теней
    directionalLight.shadow.mapSize.height = 4096;
    scene.add(directionalLight);

    // Добавляем еще один источник света для дополнительного освещения модели
    const pointLight = new THREE.PointLight(0xffffff, 0.8); // Дополнительное освещение
    pointLight.position.set(-10, 10, -10);
    scene.add(pointLight);

    // Загружаем 3D модель
    const loader = new GLTFLoader();
    loader.load('static/model/city.glb', function (gltf) {
        const model = gltf.scene;

        // Настройка модели (позиционирование, масштабирование, вращение)
        model.position.set(0, 0, 0);
        model.scale.set(0.1, 0.1, 0.1); // Уменьшаем масштаб модели
        model.rotation.set(0, 0, 0);

        // Включаем тени для всех объектов модели
        model.traverse(function (child) {
            if (child.isMesh) {
                child.castShadow = true;
                child.receiveShadow = true;
            }
        });

        scene.add(model);

        // Корректируем позицию камеры, чтобы она смотрела на центр модели
        const boundingBox = new THREE.Box3().setFromObject(model);
        const center = boundingBox.getCenter(new THREE.Vector3());
        camera.lookAt(center);
    }, undefined, function (error) {
        console.error('Error loading model:', error);
    });

    // Добавляем управление (OrbitControls)
    controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true; // Плавное управление
    controls.dampingFactor = 0.25;
    controls.screenSpacePanning = false;
    controls.maxPolarAngle = Math.PI / 2; // Ограничение вращения по вертикали

    // Обрабатываем изменение размера окна
    window.addEventListener('resize', onWindowResize, false);
}

function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
}

function animate() {
    requestAnimationFrame(animate);
    controls.update(); // Плавное управление
    renderer.render(scene, camera);
}
