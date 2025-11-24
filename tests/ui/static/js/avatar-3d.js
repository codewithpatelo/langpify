// Avatar 3D Manager usando three-vrm (Pixiv oficial)
// Modelos VRM oficiales del repositorio vrm-specification

import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { VRMLoaderPlugin, VRMUtils } from '@pixiv/three-vrm';

class Avatar3DManager {
    constructor(canvasId, gender = 'female') {
        this.canvas = document.getElementById(canvasId);
        this.gender = gender;
        this.scene = null;
        this.camera = null;
        this.renderer = null;
        this.avatar = null;
        this.mixer = null;
        this.clock = new THREE.Clock();
        this.isAnimating = false;
        
        this.init();
    }
    
    init() {
        // Setup Scene
        this.scene = new THREE.Scene();
        this.scene.background = null; // Transparente
        
        // Setup Camera
        this.camera = new THREE.PerspectiveCamera(
            45,
            this.canvas.clientWidth / this.canvas.clientHeight,
            0.1,
            1000
        );
        this.camera.position.set(0, 1.5, 2);
        this.camera.lookAt(0, 1.2, 0);
        
        // Setup Renderer
        this.renderer = new THREE.WebGLRenderer({
            canvas: this.canvas,
            alpha: true,
            antialias: true
        });
        this.renderer.setSize(this.canvas.clientWidth, this.canvas.clientHeight);
        this.renderer.setPixelRatio(window.devicePixelRatio);
        this.renderer.shadowMap.enabled = true;
        
        // Lighting
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.8);
        this.scene.add(ambientLight);
        
        const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
        directionalLight.position.set(2, 3, 2);
        directionalLight.castShadow = true;
        this.scene.add(directionalLight);
        
        const fillLight = new THREE.DirectionalLight(0x00d4aa, 0.3);
        fillLight.position.set(-2, 1, -2);
        this.scene.add(fillLight);
        
        // Load Avatar
        this.loadAvatar();
        
        // Start animation loop
        this.animate();
        
        // Handle resize
        window.addEventListener('resize', () => this.onResize());
    }
    
    loadAvatar() {
        // URLs de avatares VRM oficiales del repositorio vrm-c/vrm-specification
        // Estos modelos SIEMPRE funcionan y son de dominio público
        const avatarUrls = {
            female: 'https://raw.githubusercontent.com/vrm-c/vrm-specification/master/samples/VRM1_Constraint_Twist_Sample/vrm/VRM1_Constraint_Twist_Sample.vrm',
            male: 'https://raw.githubusercontent.com/vrm-c/vrm-specification/master/samples/Seed-san/vrm/Seed-san.vrm'
        };
        
        const loader = new GLTFLoader();
        loader.crossOrigin = 'anonymous';
        
        // Install VRM plugin
        loader.register((parser) => {
            return new VRMLoaderPlugin(parser);
        });
        
        const avatarUrl = avatarUrls[this.gender] || avatarUrls.female;
        
        loader.load(
            avatarUrl,
            (gltf) => {
                const vrm = gltf.userData.vrm;
                
                // Optimizations (oficial de three-vrm)
                VRMUtils.removeUnnecessaryVertices(gltf.scene);
                VRMUtils.combineSkeletons(gltf.scene);
                
                // Disable frustum culling
                vrm.scene.traverse((obj) => {
                    obj.frustumCulled = false;
                });
                
                this.avatar = vrm;
                this.scene.add(vrm.scene);
                
                console.log(`✅ Avatar VRM ${this.gender} cargado exitosamente`);
                console.log(vrm);
            },
            (progress) => {
                const percent = (progress.loaded / progress.total) * 100;
                console.log(`Cargando avatar VRM: ${percent.toFixed(0)}%`);
            },
            (error) => {
                console.error('❌ Error cargando avatar VRM:', error);
                // Crear avatar placeholder si falla
                this.createPlaceholderAvatar();
            }
        );
    }
    
    createPlaceholderAvatar() {
        // Crear un avatar simple si falla la carga
        const geometry = new THREE.CapsuleGeometry(0.3, 1, 8, 16);
        const material = new THREE.MeshStandardMaterial({ 
            color: this.gender === 'female' ? 0xff6b9d : 0x00d4aa,
            metalness: 0.3,
            roughness: 0.7
        });
        
        this.avatar = new THREE.Mesh(geometry, material);
        this.avatar.position.y = 0.5;
        this.avatar.castShadow = true;
        this.scene.add(this.avatar);
        
        // Head
        const headGeometry = new THREE.SphereGeometry(0.25, 16, 16);
        const head = new THREE.Mesh(headGeometry, material);
        head.position.y = 1.3;
        this.avatar.add(head);
        
        console.log('⚠️  Avatar placeholder creado');
    }
    
    animate() {
        requestAnimationFrame(() => this.animate());
        
        const delta = this.clock.getDelta();
        
        // Update VRM (si existe)
        if (this.avatar && this.avatar.update) {
            this.avatar.update(delta);
        }
        
        // NO rotation cuando habla - mantener fijo por ahora
        // (Las animaciones VRM de expresiones faciales se pueden agregar después)
        
        this.renderer.render(this.scene, this.camera);
    }
    
    startSpeaking() {
        this.isAnimating = true;
        
        // TODO: Agregar expresiones VRM si el modelo las soporta
        // VRM soporta expresiones faciales (BlendShapes) pero requiere configuración
        console.log('🗣️ Avatar hablando');
    }
    
    stopSpeaking() {
        this.isAnimating = false;
        
        // Volver a idle
        if (this.mixer && this.avatar) {
            // Volver a animación idle
            console.log('😌 Avatar idle');
        }
    }
    
    onResize() {
        const width = this.canvas.clientWidth;
        const height = this.canvas.clientHeight;
        
        this.camera.aspect = width / height;
        this.camera.updateProjectionMatrix();
        this.renderer.setSize(width, height);
    }
    
    dispose() {
        // Cleanup
        if (this.avatar) {
            this.scene.remove(this.avatar);
        }
        if (this.renderer) {
            this.renderer.dispose();
        }
    }
}

// Exportar para uso como módulo
export { Avatar3DManager };
