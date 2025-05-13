document.addEventListener('DOMContentLoaded', () => {
    const searchForm = document.querySelector('.search-form');
    const searchInput = searchForm ? searchForm.querySelector('input[name="q"]') : null;
    const resultsContainer = document.querySelector('.medicine-grid');

    if (searchForm && searchInput && resultsContainer) {
        searchForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const query = searchInput.value.trim();
            if (query) {
                fetch(`/search/?q=${encodeURIComponent(query)}`, {
                    headers: { 'X-Requested-With': 'XMLHttpRequest' }
                })
                    .then(response => response.json())
                    .then(data => {
                        resultsContainer.innerHTML = '';
                        data.results.forEach(medicine => {
                            const card = document.createElement('div');
                            card.className = 'medicine-card';
                            card.innerHTML = `
                                <img src="${medicine.image}" alt="${medicine.name}">
                                <h3>${medicine.name}</h3>
                                <p>$${medicine.price}</p>
                                <button onclick="addToCart(${medicine.id})">Add to Cart</button>
                            `;
                            resultsContainer.appendChild(card);
                        });
                    });
            }
        });
    }

    window.addToCart = (medicineId) => {
        fetch(`/cart/add/${medicineId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    alert('Added to cart!');
                }
            });
    };

    const removeButtons = document.querySelectorAll('.cart-table button');
    removeButtons.forEach(button => {
        button.addEventListener('click', (e) => {
            const cartId = e.target.dataset.cartId;
            fetch(`/cart/remove/${cartId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        e.target.closest('tr').remove();
                        updateCartTotal();
                    }
                });
        });
    });

    function updateCartTotal() {
        const rows = document.querySelectorAll('.cart-table tr');
        let total = 0;
        rows.forEach(row => {
            const price = parseFloat(row.querySelector('td:nth-child(3)').textContent.replace('$', ''));
            const quantity = parseInt(row.querySelector('td:nth-child(4)').textContent);
            total += price * quantity;
        });
        const totalElement = document.querySelector('.total');
        if (totalElement) {
            totalElement.textContent = `Total: $${total.toFixed(2)}`;
        }
    }

    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
        return null;
    }
});