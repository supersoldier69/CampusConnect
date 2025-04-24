class ClickSpark {
    constructor(options = {}) {
        this.sparkColor = options.sparkColor || "#fff";
        this.sparkSize = options.sparkSize || 10;
        this.sparkRadius = options.sparkRadius || 15;
        this.sparkCount = options.sparkCount || 8;
        this.duration = options.duration || 400;
        this.easing = options.easing || "ease-out";
        this.extraScale = options.extraScale || 1.0;
        
        this.sparks = [];
        this.startTime = null;
        this.canvas = null;
        this.ctx = null;
        this.animationId = null;
    }

    init() {
        // Create canvas element
        this.canvas = document.createElement('canvas');
        this.canvas.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 9999;
        `;
        document.body.appendChild(this.canvas);
        this.ctx = this.canvas.getContext('2d');

        // Set canvas size
        this.resizeCanvas();

        // Add event listeners
        window.addEventListener('resize', this.resizeCanvas.bind(this));
        document.addEventListener('click', this.handleClick.bind(this));

        // Start animation loop
        this.animate();
    }

    resizeCanvas() {
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
    }

    ease(t) {
        switch (this.easing) {
            case "linear":
                return t;
            case "ease-in":
                return t * t;
            case "ease-in-out":
                return t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t;
            default:
                return t * (2 - t);
        }
    }

    handleClick(e) {
        const x = e.clientX;
        const y = e.clientY;
        const now = performance.now();

        const newSparks = Array.from({ length: this.sparkCount }, (_, i) => ({
            x,
            y,
            angle: (2 * Math.PI * i) / this.sparkCount,
            startTime: now,
        }));

        this.sparks.push(...newSparks);
    }

    animate() {
        const timestamp = performance.now();
        if (!this.startTime) {
            this.startTime = timestamp;
        }

        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

        this.sparks = this.sparks.filter(spark => {
            const elapsed = timestamp - spark.startTime;
            if (elapsed >= this.duration) {
                return false;
            }

            const progress = elapsed / this.duration;
            const eased = this.ease(progress);

            const distance = eased * this.sparkRadius * this.extraScale;
            const lineLength = this.sparkSize * (1 - eased);

            const x1 = spark.x + distance * Math.cos(spark.angle);
            const y1 = spark.y + distance * Math.sin(spark.angle);
            const x2 = spark.x + (distance + lineLength) * Math.cos(spark.angle);
            const y2 = spark.y + (distance + lineLength) * Math.sin(spark.angle);

            this.ctx.strokeStyle = this.sparkColor;
            this.ctx.lineWidth = 2;
            this.ctx.beginPath();
            this.ctx.moveTo(x1, y1);
            this.ctx.lineTo(x2, y2);
            this.ctx.stroke();

            return true;
        });

        this.animationId = requestAnimationFrame(this.animate.bind(this));
    }

    destroy() {
        if (this.animationId) {
            cancelAnimationFrame(this.animationId);
        }
        if (this.canvas && this.canvas.parentNode) {
            this.canvas.parentNode.removeChild(this.canvas);
        }
        window.removeEventListener('resize', this.resizeCanvas.bind(this));
        document.removeEventListener('click', this.handleClick.bind(this));
    }
}

// Initialize click spark effect
document.addEventListener('DOMContentLoaded', () => {
    const clickSpark = new ClickSpark({
        sparkColor: "#3498db", // Match your theme color
        sparkSize: 20,
        sparkRadius: 30,
        sparkCount: 12,
        duration: 400,
        easing: "ease-out",
        extraScale: 1.0
    });
    clickSpark.init();
}); 