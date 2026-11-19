
from flask import Flask

app = Flask(__name__)

@app.route("/")
def accueil():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>NatureShop | Natural Beauty</title>

        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }

            body {
                font-family: Arial, sans-serif;
                background-color: #faf9f5;
                color: #344536;
            }

            header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 25px 8%;
                background: white;
            }

            .logo {
                font-size: 25px;
                font-weight: bold;
                color: #426747;
            }

            nav a {
                text-decoration: none;
                color: #344536;
                margin-left: 25px;
                font-size: 14px;
            }

            .hero {
                min-height: 430px;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                text-align: center;
                padding: 60px 20px;
                background: linear-gradient(135deg, #e8efe3, #f5eadb);
            }

            .hero h1 {
                font-size: 48px;
                margin-bottom: 20px;
                color: #35583c;
            }

            .hero p {
                font-size: 18px;
                max-width: 550px;
                line-height: 1.7;
                color: #647463;
            }

            .hero button {
                margin-top: 30px;
                padding: 14px 30px;
                border: none;
                border-radius: 30px;
                background: #426747;
                color: white;
                font-size: 15px;
                cursor: pointer;
            }

            .products {
                padding: 65px 8%;
                text-align: center;
            }

            .products h2 {
                font-size: 30px;
                margin-bottom: 12px;
            }

            .subtitle {
                color: #849083;
                margin-bottom: 35px;
            }

            .product-container {
                display: flex;
                justify-content: center;
                flex-wrap: wrap;
                gap: 25px;
            }

            .card {
                background: white;
                width: 250px;
                padding: 30px 20px;
                border-radius: 16px;
                box-shadow: 0 5px 20px rgba(0,0,0,0.06);
                transition: transform 0.3s;
            }

            .card:hover {
                transform: translateY(-8px);
            }

            .product-icon {
                font-size: 55px;
                margin-bottom: 20px;
            }

            .card h3 {
                margin-bottom: 12px;
                color: #426747;
            }

            .card p {
                color: #849083;
                font-size: 14px;
                line-height: 1.6;
            }

            .price {
                display: block;
                margin-top: 18px;
                font-size: 19px;
                font-weight: bold;
                color: #bd8852;
            }

            footer {
                text-align: center;
                padding: 25px;
                background: #344f39;
                color: white;
                font-size: 14px;
            }

            @media (max-width: 600px) {
                header {
                    flex-direction: column;
                    gap: 15px;
                }

                nav a {
                    margin: 0 8px;
                }

                .hero h1 {
                    font-size: 34px;
                }
            }
        </style>
    </head>

    <body>

        <header>
            <div class="logo">NatureShop 🌿</div>

            <nav>
                <a href="/">Home</a>
                <a href="#products">Products</a>
                <a href="#about">About Us</a>
            </nav>
        </header>

        <section class="hero" id="about">
            <h1>Discover Natural Beauty</h1>

            <p>
                Take care of yourself with our handmade natural cosmetics.
                Pure ingredients, authentic products and beauty inspired by nature.
            </p>

            <button onclick="document.getElementById('products').scrollIntoView({behavior:'smooth'})">
                Explore Our Products
            </button>
        </section>

        <section class="products" id="products">

            <h2>Our Natural Collection</h2>

            <p class="subtitle">
                Simple ingredients. Natural beauty. Better care.
            </p>

            <div class="product-container">

                <div class="card">
                    <div class="product-icon">🧼</div>
                    <h3>Natural Soap</h3>
                    <p>Handmade soap with natural ingredients for gentle skin care.</p>
                    <span class="price">12 TND</span>
                </div>

                <div class="card">
                    <div class="product-icon">🌸</div>
                    <h3>Essential Oils</h3>
                    <p>Pure aromatic oils inspired by nature and relaxation.</p>
                    <span class="price">25 TND</span>
                </div>

                <div class="card">
                    <div class="product-icon">🌿</div>
                    <h3>Natural Cream</h3>
                    <p>A nourishing cream designed for everyday skin care.</p>
                    <span class="price">18 TND</span>
                </div>

            </div>
        </section>

        <footer>
            © 2026 NatureShop — Natural Beauty, Naturally.
        </footer>

    </body>
    </html>
    """


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
