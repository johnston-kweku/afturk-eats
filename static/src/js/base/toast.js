class ToastManager {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
    }

    show(text, tag = 'info') {
        const toast = document.createElement('div');
        toast.textContent = text;

        const toneClasses = {
            success: 'bg-cyprus-700 text-sand-100 border-cyprus-500/40',
            error: 'bg-red-600/90 text-sand-100 border-red-400/40',
            warning: 'bg-sand-500 text-cyprus-800 border-sand-400',
            info: 'bg-white/10 text-sand-100 border-sand-100/20 backdrop-blur-md',
        };

        toast.className = `w-full px-4 py-3 rounded-xl border shadow-lg font-sans text-sm
            translate-x-[120%] opacity-0 transition-all duration-500 ease-out
            ${toneClasses[tag] || toneClasses.info}`;

        this.container.appendChild(toast);

        requestAnimationFrame(() => {
            toast.classList.remove('translate-x-[120%]', 'opacity-0');
        });

        setTimeout(() => {
            toast.classList.add('translate-x-[120%]', 'opacity-0');
            toast.addEventListener('transitionend', () => toast.remove(), { once: true });
        }, 5000);
    }

    loadFromDjangoMessages() {
        const el = document.getElementById('django-messages');
        if (!el) return;

        let messages;
        try {
            messages = JSON.parse(el.textContent);
        } catch {
            return;
        }

        messages.forEach(msg => this.show(msg.text, msg.tags));
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const toastManager = new ToastManager('toast-container');
    toastManager.loadFromDjangoMessages();
});