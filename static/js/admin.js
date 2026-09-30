document.getElementById('product-form')?.addEventListener('submit', async (event) => {
  event.preventDefault();

  const payload = {
    id: `manual-${Date.now()}`,
    name: document.getElementById('product-name').value,
    type: document.getElementById('product-type').value,
    price: Number(document.getElementById('product-price').value),
    channel: document.getElementById('product-channel').value,
    audience: document.getElementById('product-audience').value,
    tagline: document.getElementById('product-tagline').value,
    category: 'general',
    cover: 'https://images.unsplash.com/photo-1512820790803-83ca734da794?auto=format&fit=crop&w=800&q=80',
    inventory: 100,
    rating: 4.8,
    goal: 'conversion',
    currency: 'USD',
  };

  const response = await fetch('/api/admin/product', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });

  const result = await response.json();
  alert(result.success ? 'Product saved successfully' : 'Error saving product');
  event.target.reset();
});

document.getElementById('campaign-form')?.addEventListener('submit', async (event) => {
  event.preventDefault();

  const payload = {
    name: document.getElementById('campaign-name').value,
    channel: document.getElementById('campaign-channel').value,
    objective: document.getElementById('campaign-objective').value,
    keywords: (document.getElementById('campaign-keywords').value || '')
      .split(',')
      .map((item) => item.trim())
      .filter(Boolean),
    creative: document.getElementById('campaign-creative').value,
    budget: Number(document.getElementById('campaign-budget').value || 0),
    status: 'draft',
  };

  const response = await fetch('/api/admin/campaign', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });

  const result = await response.json();
  alert(result.success ? 'Campaign saved successfully' : 'Error saving campaign');
  event.target.reset();
});

document.getElementById('generate-copy-btn')?.addEventListener('click', async () => {
  const productName = document.getElementById('copy-product-name').value || 'The Growth Blueprint';
  const audience = document.getElementById('copy-audience').value || 'new readers';
  const channel = document.getElementById('copy-channel').value || 'Amazon';

  const response = await fetch('/api/ai-copy', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ product_name: productName, audience, channel }),
  });

  const result = await response.json();
  const box = document.getElementById('generated-copy');

  box.innerHTML = `
    <h4>${result.creative.headline}</h4>
    <p>${result.creative.body}</p>
    <strong>CTA: ${result.creative.cta}</strong>
  `;
});
