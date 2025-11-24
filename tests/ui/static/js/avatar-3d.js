// Avatar 3D Manager usando Ready Player Me
// Ready Player Me proporciona avatares 3D gratuitos

import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';

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
        // URLs de avatares Ready Player Me gratuitos
        // Estos son avatares públicos de ejemplo
        const avatarUrls = {
            female: 'https://models.readyplayer.me/65e92a7c7ffd4c47d67cf4b2.glb',
            male: 'https://models.readyplayer.me/65e92a1c7ffd4c47d67cf4a1.glb'
        };
        
        const loader = new GLTFLoader();
        const avatarUrl = avatarUrls[this.gender] || avatarUrls.female;
        
        loader.load(
            avatarUrl,
            (gltf) => {
                this.avatar = gltf.scene;
                this.avatar.position.set(0, 0, 0);
                this.avatar.scale.set(1, 1, 1);
                
                // Setup shadows
                this.avatar.traverse((node) => {
                    if (node.isMesh) {
                        node.castShadow = true;
                        node.receiveShadow = true;
                    }
                });
                
                this.scene.add(this.avatar);
                
                // Setup animations if available
                if (gltf.animations && gltf.animations.length) {
                    this.mixer = new THREE.AnimationMixer(this.avatar);
                    
                    // Play idle animation
                    const idleAnimation = gltf.animations.find(anim => 
                        anim.name.toLowerCase().includes('idle')
                    ) || gltf.animations[0];
                    
                    if (idleAnimation) {
                        const action = this.mixer.clipAction(idleAnimation);
                        action.play();
                    }
                }
                
                console.log(`✅ Avatar ${this.gender} cargado exitosamente`);
            },
            (progress) => {
                const percent = (progress.loaded / progress.total) * 100;
                console.log(`Cargando avatar: ${percent.toFixed(0)}%`);
            },
            (error) => {
                console.error('Error cargando avatar:', error);
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
        
        // Update animations
        if (this.mixer) {
            this.mixer.update(delta);
        }
        
        // Subtle rotation when speaking
        if (this.isAnimating && this.avatar) {
            this.avatar.rotation.y += 0.005;
        }
        
        this.renderer.render(this.scene, this.camera);
    }
    
    startSpeaking() {
        this.isAnimating = true;
        
        // Cambiar a animación de hablar si existe
        if (this.mixer && this.avatar) {
            // Aquí podrías cargar una animación de hablar
            console.log('🗣️ Avatar hablando');
        }
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
