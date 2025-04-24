class CursorTrail {
    constructor() {
        this.particles = [];
        this.maxParticles = 20;
        this.colors = [
            '#00f7ff', // Neon Blue
            '#ff00ff', // Neon Pink
            '#00ff00', // Neon Green
            '#ff00ff', // Neon Purple
        ];
        this.init();
    }

    init() {
        document.addEventListener('mousemove', (e) => this.createParticle(e));
        this.animate();
    }

    createParticle(e) {
        const particle = {
            x: e.clientX,
            y: e.clientY,
            size: Math.random() * 3 + 2,
            color: this.colors[Math.floor(Math.random() * this.colors.length)],
            speedX: (Math.random() - 0.5) * 2,
            speedY: (Math.random() - 0.5) * 2,
            life: 1,
            decay: Math.random() * 0.02 + 0.01
        };

        this.particles.push(particle);

        if (this.particles.length > this.maxParticles) {
            this.particles.shift();
        }
    }

    animate() {
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        canvas.style.position = 'fixed';
        canvas.style.top = '0';
        canvas.style.left = '0';
        canvas.style.width = '100%';
        canvas.style.height = '100%';
        canvas.style.pointerEvents = 'none';
        canvas.style.zIndex = '9999';
        document.body.appendChild(canvas);

        const resizeCanvas = () => {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        };
        resizeCanvas();
        window.addEventListener('resize', resizeCanvas);

        const animate = () => {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            
            this.particles.forEach((particle, index) => {
                particle.x += particle.speedX;
                particle.y += particle.speedY;
                particle.life -= particle.decay;

                if (particle.life <= 0) {
                    this.particles.splice(index, 1);
                    return;
                }

                ctx.beginPath();
                ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2);
                ctx.fillStyle = particle.color;
                ctx.globalAlpha = particle.life;
                ctx.fill();
                ctx.closePath();

                // Add glow effect
                ctx.shadowBlur = 15;
                ctx.shadowColor = particle.color;
            });

            requestAnimationFrame(animate);
        };

        animate();
    }
}

// Initialize the cursor trail
new CursorTrail(); 