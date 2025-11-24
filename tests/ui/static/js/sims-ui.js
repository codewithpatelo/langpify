// Langpify Sims UI - JavaScript Controller

import { Avatar3DManager } from './avatar-3d.js';

class LangpifySimsUI {
    constructor() {
        this.ws = null;
        this.audioPlayer = document.getElementById('audioPlayer');
        this.startTime = null;
        this.currentIteration = 0;
        this.carlaAvatar = null;
        this.robertoAvatar = null;
        
        this.init();
    }
    
    init() {
        // Event listeners
        document.getElementById('startBtn').addEventListener('click', () => this.startDebate());
        document.getElementById('pauseBtn').addEventListener('click', () => this.pauseDebate());
        
        // Inicializar avatares 3D
        this.initAvatars();
        
        console.log('🎮 Langpify Sims UI inicializado');
    }
    
    initAvatars() {
        console.log('🧍 Inicializando avatares 3D...');
        
        try {
            // Avatar femenino para Carla
            this.carlaAvatar = new Avatar3DManager('carlaCanvas', 'female');
            
            // Avatar masculino para Roberto
            this.robertoAvatar = new Avatar3DManager('robertoCanvas', 'male');
            
            console.log('✅ Avatares 3D inicializados');
        } catch (error) {
            console.error('❌ Error inicializando avatares:', error);
        }
    }
    
    startDebate() {
        if (this.ws && this.ws.readyState === WebSocket.OPEN) {
            console.warn('Debate ya en progreso');
            return;
        }
        
        const startBtn = document.getElementById('startBtn');
        const pauseBtn = document.getElementById('pauseBtn');
        
        startBtn.disabled = true;
        pauseBtn.disabled = false;
        
        this.startTime = Date.now();
        this.currentIteration = 0;
        
        // Conectar WebSocket
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        this.ws = new WebSocket(`${protocol}//${window.location.host}/ws`);
        
        this.ws.onopen = () => {
            console.log('✅ WebSocket conectado');
            this.addTimelineEvent('Conexión establecida');
            this.updateStatus('Iniciando debate...');
            
            // Enviar comando de inicio
            this.ws.send(JSON.stringify({
                action: 'start_debate'
            }));
        };
        
        this.ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            this.handleMessage(data);
        };
        
        this.ws.onerror = (error) => {
            console.error('❌ WebSocket error:', error);
            this.addTimelineEvent('Error de conexión');
        };
        
        this.ws.onclose = () => {
            console.log('🔌 WebSocket desconectado');
            startBtn.disabled = false;
            pauseBtn.disabled = true;
        };
    }
    
    pauseDebate() {
        if (this.ws) {
            this.ws.close();
        }
    }
    
    handleMessage(data) {
        console.log('📨 Mensaje recibido:', data.type);
        
        switch (data.type) {
            case 'debate_start':
                this.onDebateStart(data);
                break;
            case 'iteration_start':
                this.onIterationStart(data);
                break;
            case 'agent_speech':
                this.onAgentSpeech(data);
                break;
            case 'debate_end':
                this.onDebateEnd();
                break;
            case 'error':
                this.onError(data);
                break;
        }
    }
    
    onDebateStart(data) {
        this.addTimelineEvent('Debate iniciado');
        this.updateStatus('Debate en progreso');
        
        // Actualizar necesidades iniciales
        if (data.agents.carla) {
            this.updateNeed('carla', 'life-purpose', data.agents.carla.needs.life_purpose);
        }
        if (data.agents.roberto) {
            this.updateNeed('roberto', 'life-purpose', data.agents.roberto.needs.life_purpose);
        }
    }
    
    onIterationStart(data) {
        this.currentIteration = data.iteration;
        document.getElementById('currentIteration').textContent = data.iteration;
        this.addTimelineEvent(`Iteración ${data.iteration} iniciada`);
        this.updateStatus(`Iteración ${data.iteration} de 4`);
    }
    
    async onAgentSpeech(data) {
        const agentName = data.agent;
        console.log(`💬 ${agentName} está hablando`);
        
        // Activar indicador de habla
        this.setAgentStatus(agentName, 'speaking');
        
        // Mostrar speech bubble
        this.showSpeechBubble(agentName, data.text, data.emotion);
        
        // Actualizar necesidades
        this.updateNeed(agentName, 'life-purpose', data.needs.life_purpose);
        
        // Mostrar cambio de necesidad
        const purposeChange = ((data.needs.life_purpose - data.old_need_value) * 100).toFixed(1);
        const changeIndicator = purposeChange > 0 ? '↑' : '↓';
        this.addTimelineEvent(
            `${agentName.toUpperCase()}: Propósito ${changeIndicator} ${Math.abs(purposeChange)}%`
        );
        
        // Reproducir audio si está disponible
        if (data.audio) {
            await this.playAudio(data.audio);
        } else {
            // Simular tiempo de habla
            await this.delay(3000);
        }
        
        // Desactivar indicador de habla
        this.setAgentStatus(agentName, 'idle');
        
        // Ocultar speech bubble después de un momento
        setTimeout(() => {
            this.hideSpeechBubble(agentName);
        }, 2000);
    }
    
    onDebateEnd() {
        this.addTimelineEvent('¡Debate finalizado!');
        this.updateStatus('Debate completado');
        
        document.getElementById('startBtn').disabled = false;
        document.getElementById('pauseBtn').disabled = true;
        
        console.log('✅ Debate completado');
    }
    
    onError(data) {
        console.error('❌ Error:', data.message);
        this.addTimelineEvent(`Error: ${data.message}`);
        alert(`Error: ${data.message}`);
    }
    
    // UI Update Methods
    
    updateStatus(message) {
        document.getElementById('statusTitle').textContent = message;
    }
    
    setAgentStatus(agent, status) {
        const statusId = agent === 'carla' ? 'carlaStatus' : 'robertoStatus';
        const indicator = document.getElementById(statusId);
        
        indicator.className = `status-indicator ${status}`;
        indicator.textContent = status.toUpperCase();
        
        // Controlar avatar 3D
        const avatar = agent === 'carla' ? this.carlaAvatar : this.robertoAvatar;
        if (avatar) {
            if (status === 'speaking') {
                avatar.startSpeaking();
            } else {
                avatar.stopSpeaking();
            }
        }
    }
    
    showSpeechBubble(agent, text, emotion) {
        const bubbleId = agent === 'carla' ? 'carlaSpeech' : 'robertoSpeech';
        const bubble = document.getElementById(bubbleId);
        
        bubble.querySelector('.speech-text').textContent = text;
        bubble.querySelector('.emotion-tag').textContent = `😊 ${emotion}`;
        bubble.classList.add('active');
    }
    
    hideSpeechBubble(agent) {
        const bubbleId = agent === 'carla' ? 'carlaSpeech' : 'robertoSpeech';
        const bubble = document.getElementById(bubbleId);
        bubble.classList.remove('active');
    }
    
    updateNeed(agent, needName, value) {
        const barId = `${agent}-${needName}`;
        const bar = document.getElementById(barId);
        const valueSpan = bar.nextElementSibling;
        
        const percentage = Math.round(value * 100);
        bar.style.width = `${percentage}%`;
        valueSpan.textContent = `${percentage}%`;
        
        // Cambiar color según nivel
        if (percentage < 20) {
            bar.style.background = 'linear-gradient(90deg, #FF4444 0%, #FF8844 100%)';
        } else if (percentage < 40) {
            bar.style.background = 'linear-gradient(90deg, #FF8844 0%, #FFDD44 100%)';
        } else if (percentage < 60) {
            bar.style.background = 'linear-gradient(90deg, #FFDD44 0%, #88DD44 100%)';
        } else {
            bar.style.background = 'linear-gradient(90deg, #88DD44 0%, #44DD88 100%)';
        }
        
        // Efecto de actualización
        bar.style.transition = 'width 1s ease, background 0.5s ease';
    }
    
    addTimelineEvent(text) {
        const timeline = document.getElementById('timelineEvents');
        const event = document.createElement('div');
        event.className = 'timeline-event';
        
        const elapsed = this.startTime ? Math.floor((Date.now() - this.startTime) / 1000) : 0;
        const minutes = Math.floor(elapsed / 60);
        const seconds = elapsed % 60;
        const timeStr = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
        
        event.innerHTML = `
            <span class="event-time">${timeStr}</span>
            <span class="event-text">${text}</span>
        `;
        
        timeline.appendChild(event);
        timeline.scrollTop = timeline.scrollHeight;
    }
    
    async playAudio(base64Audio) {
        return new Promise((resolve) => {
            try {
                const audioBlob = this.base64ToBlob(base64Audio, 'audio/mp3');
                const audioUrl = URL.createObjectURL(audioBlob);
                
                this.audioPlayer.src = audioUrl;
                this.audioPlayer.onended = () => {
                    URL.revokeObjectURL(audioUrl);
                    resolve();
                };
                this.audioPlayer.play();
            } catch (error) {
                console.error('Error reproduciendo audio:', error);
                resolve();
            }
        });
    }
    
    base64ToBlob(base64, mimeType) {
        const byteCharacters = atob(base64);
        const byteNumbers = new Array(byteCharacters.length);
        
        for (let i = 0; i < byteCharacters.length; i++) {
            byteNumbers[i] = byteCharacters.charCodeAt(i);
        }
        
        const byteArray = new Uint8Array(byteNumbers);
        return new Blob([byteArray], { type: mimeType });
    }
    
    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    window.simsUI = new LangpifySimsUI();
});
