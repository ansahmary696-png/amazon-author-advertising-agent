const formatCurrency = (value) => `$${Number(value).toFixed(2)}`;

async function loadOverview() {
  const response = await fetch('/api/overview');
  const data = await response.json();

  document.getElementById('campaign-count').textContent = data.metrics.campaign_count;
  document.getElementById('avg-price').textContent = formatCurrency(data.metrics.average_price);
  document.getElementById('best-channel').textContent = data.metrics.best_channel;
}

async function loadProducts() {
  const response = await fetch('/api/products');
  const products = await response.json();
  const grid = document.getElementById('product-grid');

  grid.innerHTML = products.map(product => `
    <article class="product-card">
      <img src="${product.cover}" alt="${product.name}" />
      <h3>${product.name}</h3>
      <p>${product.tagline}</p>
      <div class="product-meta">
        <span class="price-tag">${formatCurrency(product.price)}</span>
        <span class="tag">${product.channel}</span>
      </div>
    </article>
  `).join('');
}

async function loadCampaigns() {
  const response = await fetch('/api/campaigns');
  const campaigns = await response.json();
  const list = document.getElementById('campaign-list');

  list.innerHTML = campaigns.map(campaign => `
    <div class="product-card">
      <h3>${campaign.name}</h3>
      <p><strong>Channel:</strong> ${campaign.channel}</p>
      <p><strong>Goal:</strong> ${campaign.objective}</p>
      <p>${campaign.creative}</p>
      <div class="product-meta">
        <span class="tag">Budget: ${formatCurrency(campaign.budget)}</span>
        <span class="tag">${campaign.keywords.slice(0, 2).join(', ')}</span>
      </div>
    </div>
  `).join('');
}

async function renderDashboard() {
  const overview = await fetch('/api/overview').then((res) => res.json());
  const summaryCards = document.getElementById('summary-cards');

  const cards = [
    ['Total products', overview.metrics.total_products],
    ['Average price', formatCurrency(overview.metrics.average_price)],
    ['Campaign count', overview.metrics.campaign_count],
    ['Best channel', overview.metrics.best_channel],
  ];

  summaryCards.innerHTML = cards.map(([label, value]) => `
    <div class="summary-card">
      <span>${label}</span>
      <strong>${value}</strong>
    </div>
  `).join('');

  const channelChart = document.getElementById('channel-chart');
  channelChart.innerHTML = overview.channels.map((channel) => `
    <div class="bar-row">
      <span>${channel.name}</span>
      <div class="bar-track"><div class="bar-fill" style="width: ${channel.performance}%"></div></div>
      <strong>${channel.performance}%</strong>
    </div>
  `).join('');

  const list = document.getElementById('campaign-ideas');
  list.innerHTML = [
    'Build a stronger Amazon brand positioning for book discoverability.',
    'Use Selar bundles to increase average order value.',
    'Retarget visitors with conversion-led offers and urgency-driven messaging.',
  ].map((idea) => `<li>${idea}</li>`).join('');
}

(async function init() {
  await loadOverview();
  await loadProducts();
  await loadCampaigns();

  if (document.getElementById('summary-cards')) {
    await renderDashboard();
  }
})();

