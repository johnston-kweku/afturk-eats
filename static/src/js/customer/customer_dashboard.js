document.addEventListener('DOMContentLoaded', () => {
    const MAX_QUANTITY = 20;

    const popup = document.getElementById('cart-popup');
    const nameEl = document.getElementById('popup-item-name');
    const vendorEl = document.getElementById('popup-vendor-name');
    const variantEl = document.getElementById('popup-variant');
    const qtyEl = document.getElementById('qty-value');
    const totalEl = document.getElementById('popup-total');
    const addBtn = document.getElementById('popup-add');
    const csrfToken = popup.querySelector('[name=csrfmiddlewaretoken]').value;

    let current = null;
    let quantity = 1;

    function render() {
        qtyEl.textContent = quantity;
        totalEl.textContent = `GHS ${(current.price * quantity).toFixed(2)}`;
    }

    function openPopup(pill) {
        current = {
            url: pill.dataset.addUrl,
            price: parseFloat(pill.dataset.price),
        };
        quantity = 1;
        nameEl.textContent = pill.dataset.itemName;
        vendorEl.textContent = pill.dataset.vendorName;
        variantEl.textContent = `${pill.dataset.label} · GHS ${pill.dataset.price}`;
        render();
        popup.classList.remove('hidden');
        popup.classList.add('flex');
    }

    function closePopup() {
        popup.classList.add('hidden');
        popup.classList.remove('flex');
        current = null;
    }

    document.querySelectorAll('.variant-pill').forEach(pill => {
        pill.addEventListener('click', () => openPopup(pill));
    });

    document.getElementById('qty-minus').addEventListener('click', () => {
        if (quantity > 1) { quantity--; render(); }
    });
    document.getElementById('qty-plus').addEventListener('click', () => {
        if (quantity < MAX_QUANTITY) { quantity++; render(); }
    });

    document.getElementById('popup-close').addEventListener('click', closePopup);
    popup.addEventListener('click', (e) => {
        if (e.target === popup) closePopup();
    });

    addBtn.addEventListener('click', async () => {
        if (!current) return;
        addBtn.disabled = true;

        try {
            const response = await fetch(current.url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken,
                },
                body: JSON.stringify({ quantity }),
            });
            const data = await response.json();

            if (data.success) {
                window.toastManager.show(data.message, 'success');
                closePopup();
            } else {
                window.toastManager.show(data.message || 'Something went wrong.', 'error');
            }
        } catch (err) {
            window.toastManager.show('Could not add to cart. Please try again.', 'error');
        } finally {
            addBtn.disabled = false;
        }
    });
});