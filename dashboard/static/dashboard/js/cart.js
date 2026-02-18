function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

document.addEventListener('DOMContentLoaded', function() {
            const products = document.querySelectorAll(".product")

            products.forEach(product => {
                product.addEventListener('submit', function(e) {
                    e.preventDefault();
                    const form = product.querySelector(".add-to-cart-form")
                    const formData = new FormData(form);

                    const button = form.querySelector('.add-to-cart-btn');

                    button.disabled = true;

                    fetch("/products/add",
                        {
                            method: 'POST',
                            body: formData,
                            headers: {
                                'X-Requested-With': 'XMLHttpRequest',
                            }
                        }
                    ).then(response => response.json()).then(data => {
                            if (data.limited) {
                                button.innerHTML = 'NO MORE IN STOCK';

                                setTimeout(() => {
                                    button.innerHTML = '<i class="fa fa-shopping-cart"></i> add to cart';
                                    button.disabled = false;
                                }, 2500);
                            }
                        if (data.success) {
                            button.innerHTML = '<i class="fa fa-shopping-cart"></i> added!';

                            const cartCountText = document.querySelector('.cart-count-text');
                            if (cartCountText) {
                                cartCountText.textContent = `${data.cart_count} Item(s) selected`;
                            }

                            const cartTotal = document.querySelector('.cart-total');
                            if (cartTotal && data.cart_total) {
                                cartTotal.textContent = data.cart_total;
                            }
                            const cartCount = document.querySelector('.cart-count');
                            if (cartCount) {
                                cartCount.textContent = data.cart_count
                            }

                            const cartDisabled = document.getElementById("view-cart-btn");
                            if (cartDisabled) {
                                cartDisabled.classList.toggle("disabled", data.cart_count === 0)
                                cartDisabled.setAttribute("aria-disabled", data.cart_count === 0);
                            }

                            const checkoutDisabled = document.getElementById("checkout-btn");
                            if (checkoutDisabled) {
                                checkoutDisabled.classList.toggle("disabled", data.cart_count === 0)
                                checkoutDisabled.setAttribute("aria-disabled", data.cart_count === 0);
                            }

                            const cartContainer = document.getElementById('cart-items-container');
                            if (cartContainer && data.cart_html) {
                                cartContainer.innerHTML = data.cart_html;
                            }

                            setTimeout(() => {
                                button.innerHTML = '<i class="fa fa-shopping-cart"></i> add to cart';
                                button.disabled = false;
                            }, 2000);
                        }
                        })
                        .catch(error => {
                            console.error('Error: ', error);
                            button.disabled = false;
                        });
                });
            });

            document.addEventListener('submit', function(e)
            {
                if (e.target.classList.contains('remove-from-cart-form'))
                {
                    e.preventDefault();
                    const form = e.target;
                    const formData = new FormData(form);
                    const button = form.querySelector('.remove-from-cart-btn');

                    if (button) {
                        button.disabled = true;
                    }

                    fetch(form.action, {
                        method: 'POST',
                        body: formData,
                        headers: {
                                'X-Requested-With': 'XMLHttpRequest',
                                'X-CSRFToken': getCookie('csrftoken')
                        }
                    }).then(response => response.json()).then(data => {
                        if (data.success) {

                            const cartCountText = document.querySelector('.cart-count-text');
                            if (cartCountText) {
                                cartCountText.textContent = `${data.cart_count} Item(s) selected`;
                            }
                            const cartCount = document.querySelector('.cart-count');
                            if (cartCount) {
                                cartCount.textContent = data.cart_count
                            }

                            const cartTotal = document.querySelector('.cart-total');
                            if (cartTotal && data.cart_total) {
                                cartTotal.textContent = data.cart_total;
                            }

                            const cartDisabled = document.getElementById("view-cart-btn");
                            if (cartDisabled) {
                                cartDisabled.classList.toggle("disabled", data.cart_count === 0)
                                cartDisabled.setAttribute("aria-disabled", data.cart_count === 0);
                            }

                            const checkoutDisabled = document.getElementById("checkout-btn");
                            if (checkoutDisabled) {
                                checkoutDisabled.classList.toggle("disabled", data.cart_count === 0)
                                checkoutDisabled.setAttribute("aria-disabled", data.cart_count === 0);
                            }

                            const cartContainer = document.getElementById('cart-items-container');
                            if (cartContainer && data.cart_html) {
                                cartContainer.innerHTML = data.cart_html;
                            }

                        }
                    }).catch(error => {
                        console.error('Error', error);
                        if (button) {
                            button.disabled = false;
                        }
                    });
                }
            });
        });

document.addEventListener("DOMContentLoaded", () => {
    const csrfToken = getCookie('csrftoken');

    document.querySelectorAll(".input-number").forEach(wrapper => {
        const input = wrapper.querySelector(".qty-input");
        const warning = wrapper.parentElement.querySelector(".stock-warning");
        const productId = wrapper.dataset.productId;
        const maxStock = parseInt(wrapper.dataset.max, 10);

        const sendUpdate = (quantity) => {
            fetch("/cart/update/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrfToken
                },
                body: JSON.stringify({
                    product_id: productId,
                    quantity: quantity
                })
            })
            .then(res => res.json())
            .then(data => {
                warning.style.display = "none";
                if (data.limited) {
                    input.value = data.quantity;
                    warning.style.display = "block";

                    setTimeout(() => {
                        warning.style.display = "none";
                    }, 2500);
                }
                if (data.success) {

                            const cartCountText = document.querySelector('.cart-count-text');
                            if (cartCountText) {
                                cartCountText.textContent = `${data.cart_count} Item(s) selected`;
                            }
                            const cartCount = document.querySelector('.cart-count');
                            if (cartCount) {
                                cartCount.textContent = data.cart_count
                            }

                            const cartTotal = document.querySelector('.cart-total');
                            if (cartTotal && data.cart_total) {
                                cartTotal.textContent = data.cart_total;
                            }

                            const cartDisabled = document.getElementById("view-cart-btn");
                            if (cartDisabled) {
                                cartDisabled.classList.toggle("disabled", data.cart_count === 0)
                                cartDisabled.setAttribute("aria-disabled", data.cart_count === 0);
                            }

                            const checkoutDisabled = document.getElementById("checkout-btn");
                            if (checkoutDisabled) {
                                checkoutDisabled.classList.toggle("disabled", data.cart_count === 0)
                                checkoutDisabled.setAttribute("aria-disabled", data.cart_count === 0);
                            }

                            const cartContainer = document.getElementById('cart-items-container');
                            if (cartContainer && data.cart_html) {
                                cartContainer.innerHTML = data.cart_html;
                            }

                        }
                    }).catch(error => {
                        console.error('Error', error);
                        if (button) {
                            button.disabled = false;
                        }
                    });
        };

        wrapper.querySelector(".qty-up").addEventListener("click", () => {
            let value = parseInt(input.value, 10);
            input.value = value;
            sendUpdate(value);
        });

        wrapper.querySelector(".qty-down").addEventListener("click", () => {
            let value = parseInt(input.value, 10);
            input.value = value
            sendUpdate(value);
        });

        input.addEventListener("change", () => {
            let value = parseInt(input.value, 10);
            if (value > maxStock) value = maxStock;
            if (value < 0) value = 0;
            input.value = value;
            sendUpdate(value);
        });
    });
});
