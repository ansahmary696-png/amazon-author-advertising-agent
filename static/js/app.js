const formatCurrency = (value) => `$${Number(value).toFixed(2)}`;

async function loadOverview() {
  const response = await fetch('/api/overview');
  const data = await response.json();
  const { metrics } = data;

  const campaignCount = document.getElementById('campaign-count');
  const avgPrice = document.getElementById('avg-price');
  const bestChannel = document.getElementById('best-channel');

  if (campaignCount) campaignCount.textContent = metrics.campaign_count ?? 0;
  if (avgPrice) avgPrice.textContent = formatCurrency(metrics.average_price ?? 0);
  if (bestChannel) bestChannel.textContent = metrics.best_channel ?? 'Amazon';
}

async function loadProducts() {
  const response = await fetch('/api/products');
  const products = await response.json();
  const grid = document.getElementById('product-grid');

  if (!grid) return;

  grid.innerHTML = products.map((product) => `
    <article class="product-card">
      <img src="${product.cover || 'https://images.unsplash.com/photo-1512820790803-83ca734da794?auto=format&fit=crop&w=800&q=80'}" alt="${product.name}" />
      <h3>${product.name}</h3>
      <p>${product.tagline || 'High-value product for growth-minded buyers.'}</p>
      <div class="product-meta">
        <span class="price-tag">${formatCurrency(product.price || 0)}</span>
        <span class="tag">${product.channel || 'Selar'}</span>
      </div>
    </article>
  `).join('');
}

async function loadCampaigns() {
  const response = await fetch('/api/campaigns');
  const campaigns = await response.json();
  const list = document.getElementById('campaign-list');

  if (!list) return;

  list.innerHTML = campaigns.map((campaign) => `
    <div class="product-card">
      <h3>${campaign.name}</h3>
      <p><strong>Channel:</strong> ${campaign.channel}</p>
      <p><strong>Goal:</strong> ${campaign.objective}</p>
      <p>${campaign.creative}</p>
      <div class="product-meta">
        <span class="tag">Budget: ${formatCurrency(campaign.budget || 0)}</span>
        <span class="tag">${(campaign.keywords || []).slice(0, 2).join(', ')}</span>
      </div>
    </div>
  `).join('');
}

async function renderDashboard() {
  const overview = await fetch('/api/overview').then((res) => res.json());
  const summaryCards = document.getElementById('summary-cards');

  if (!summaryCards) return;

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
  if (channelChart) {
    channelChart.innerHTML = (overview.channels || []).map((channel) => `
      <div class="bar-row">
        <span>${channel.name}</span>
        <div class="bar-track">
          <div class="bar-fill" style="width: ${channel.performance}%"></div>
        </div>
        <strong>${channel.performance}%</strong>
      </div>
    `).join('');
  }

  const list = document.getElementById('campaign-ideas');
  if (list) {
    list.innerHTML = [
      'Build a stronger Amazon brand positioning for better discoverability.',
      'Use Selar bundles to increase average order value and customer lifetime value.',
      'Retarget previous visitors with urgency-based, benefit-led offers at the right time.',
    ].map((idea) => `<li>${idea}</li>`).join('');
  }
}

(async function init() {
  await loadOverview();
  await loadProducts();
  await loadCampaigns();

  if (document.getElementById('summary-cards')) {
    await renderDashboard();
  }
})();
