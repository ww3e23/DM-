// DM生成器核心功能
class DMGenerator {
    constructor() {
        this.products = [];
        this.campaigns = [];
        this.selectedCampaign = null;
        this.selectedProducts = [];
        this.settings = {
            showShop: true,
            showCampaign: true,
            showLogo: true,
            showContact: true,
            showNotes: true,
            showQR: true,
            layout: 'grid',
            theme: 'default'
        };
        this.init();
    }

    init() {
        this.loadDefaultData();
        this.setupEventListeners();
    }

    loadDefaultData() {
        // 加载默认商品数据
        this.products = [
            {
                id: 1,
                name: "精选商品A",
                price: 299,
                originalPrice: 399,
                description: "高品质商品，限时优惠",
                image: null
            },
            {
                id: 2,
                name: "精选商品B",
                price: 199,
                originalPrice: 299,
                description: "热销商品，数量有限",
                image: null
            }
        ];

        // 加载默认方案数据
        this.campaigns = [
            {
                id: 1,
                name: "春季促销",
                qrImage: null,
                qrUrl: "https://example.com/spring-sale"
            },
            {
                id: 2,
                name: "会员专享",
                qrImage: null,
                qrUrl: "https://example.com/vip"
            }
        ];
    }

    setupEventListeners() {
        // 商品表单提交
        document.getElementById('product-form')?.addEventListener('submit', (e) => {
            e.preventDefault();
            this.addProduct(new FormData(e.target));
        });

        // 方案表单提交
        document.getElementById('form-add-campaign')?.addEventListener('submit', (e) => {
            e.preventDefault();
            this.addCampaign(new FormData(e.target));
        });

        // 生成DM按钮
        document.getElementById('generate-dm-btn')?.addEventListener('click', () => {
            this.generateDM();
        });
    }

    addProduct(formData) {
        const product = {
            id: Date.now(),
            name: formData.get('name'),
            price: parseFloat(formData.get('price')),
            originalPrice: formData.get('originalPrice') ? parseFloat(formData.get('originalPrice')) : null,
            description: formData.get('desc'),
            image: null
        };

        this.products.push(product);
        this.renderProducts();
        this.showToast('商品添加成功！', 'success');
        
        // 清空表单
        document.getElementById('product-form').reset();
    }

    addCampaign(formData) {
        const campaign = {
            id: Date.now(),
            name: formData.get('campaignName'),
            qrImage: null,
            qrUrl: formData.get('qrUrl')
        };

        this.campaigns.push(campaign);
        this.renderCampaigns();
        this.showToast('方案添加成功！', 'success');
        
        // 清空表单
        document.getElementById('form-add-campaign').reset();
        document.getElementById('form-add-campaign').classList.add('hidden');
    }

    renderProducts() {
        const container = document.getElementById('product-list');
        if (!container) return;

        container.innerHTML = this.products.map(product => `
            <div class="product-item bg-white p-4 rounded-lg border border-gray-200">
                <div class="flex items-center justify-between mb-2">
                    <h4 class="font-semibold text-gray-900">${product.name}</h4>
                    <div class="flex items-center space-x-2">
                        <input type="checkbox" 
                               class="product-checkbox" 
                               data-product-id="${product.id}"
                               ${this.selectedProducts.includes(product.id) ? 'checked' : ''}>
                        <button onclick="dmGenerator.removeProduct(${product.id})" 
                                class="text-red-600 hover:text-red-800">
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                </div>
                <div class="text-sm text-gray-600 mb-2">
                    <span class="text-lg font-bold text-green-600">¥${product.price}</span>
                    ${product.originalPrice ? `<span class="text-gray-400 line-through ml-2">¥${product.originalPrice}</span>` : ''}
                </div>
                <p class="text-sm text-gray-500">${product.description || '暂无描述'}</p>
            </div>
        `).join('');

        // 绑定选择事件
        container.querySelectorAll('.product-checkbox').forEach(checkbox => {
            checkbox.addEventListener('change', (e) => {
                const productId = parseInt(e.target.dataset.productId);
                if (e.target.checked) {
                    if (!this.selectedProducts.includes(productId)) {
                        this.selectedProducts.push(productId);
                    }
                } else {
                    this.selectedProducts = this.selectedProducts.filter(id => id !== productId);
                }
                this.updateSelectedSummary();
            });
        });
    }

    renderCampaigns() {
        const container = document.getElementById('campaign-pill-list');
        if (!container) return;

        container.innerHTML = this.campaigns.map(campaign => `
            <button class="campaign-pill px-4 py-2 rounded-full border-2 transition-colors
                          ${this.selectedCampaign === campaign.id ? 'border-blue-500 bg-blue-50 text-blue-700' : 'border-gray-200 hover:border-gray-300'}"
                    onclick="dmGenerator.selectCampaign(${campaign.id})">
                ${campaign.name}
            </button>
        `).join('');
    }

    selectCampaign(campaignId) {
        this.selectedCampaign = campaignId;
        this.renderCampaigns();
        this.updateSelectedSummary();
    }

    removeProduct(productId) {
        this.products = this.products.filter(p => p.id !== productId);
        this.selectedProducts = this.selectedProducts.filter(id => id !== productId);
        this.renderProducts();
        this.updateSelectedSummary();
    }

    updateSelectedSummary() {
        const summary = document.getElementById('chosen-summary');
        if (!summary) return;

        const selectedProducts = this.products.filter(p => this.selectedProducts.includes(p.id));
        const campaign = this.campaigns.find(c => c.id === this.selectedCampaign);

        let summaryText = '';
        if (campaign) {
            summaryText += `方案: ${campaign.name}`;
        }
        if (selectedProducts.length > 0) {
            summaryText += ` | 商品: ${selectedProducts.length}个`;
        }

        summary.textContent = summaryText || '请选择方案和商品';
    }

    async generateDM() {
        if (!this.selectedCampaign) {
            this.showToast('请选择一个DM方案', 'warning');
            return;
        }

        if (this.selectedProducts.length === 0) {
            this.showToast('请至少选择一个商品', 'warning');
            return;
        }

        try {
            const campaign = this.campaigns.find(c => c.id === this.selectedCampaign);
            const selectedProducts = this.products.filter(p => this.selectedProducts.includes(p.id));

            const dmData = {
                campaign: campaign,
                products: selectedProducts,
                settings: this.settings,
                timestamp: new Date().toISOString()
            };

            // 调用后端API生成DM
            const response = await fetch('/api/dm/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(dmData)
            });

            const result = await response.json();

            if (result.success) {
                this.showToast('DM生成成功！', 'success');
                this.displayGeneratedDM(result.data);
            } else {
                this.showToast(result.error || '生成失败', 'error');
            }
        } catch (error) {
            console.error('生成DM失败:', error);
            this.showToast('生成失败，请稍后重试', 'error');
        }
    }

    displayGeneratedDM(dmData) {
        // 这里显示生成的DM预览
        const preview = document.getElementById('dm-preview');
        if (!preview) return;

        // 创建DM预览HTML
        const dmHTML = this.createDMPreview(dmData);
        preview.innerHTML = dmHTML;
        preview.classList.remove('hidden');
    }

    createDMPreview(data) {
        const campaign = data.campaign;
        const products = data.products;

        return `
            <div class="dm-preview bg-white border border-gray-200 rounded-lg p-6">
                <div class="dm-header text-center mb-6">
                    <h1 class="text-2xl font-bold text-gray-900 mb-2">${campaign.name}</h1>
                    <p class="text-gray-600">限时优惠，数量有限</p>
                </div>
                
                <div class="products-grid grid grid-cols-2 gap-4 mb-6">
                    ${products.map(product => `
                        <div class="product-card bg-gray-50 p-4 rounded-lg">
                            <div class="product-image bg-gray-200 h-32 rounded-lg mb-3 flex items-center justify-center">
                                <i class="fas fa-image text-gray-400 text-2xl"></i>
                            </div>
                            <h3 class="font-semibold text-gray-900 mb-2">${product.name}</h3>
                            <div class="price mb-2">
                                <span class="text-lg font-bold text-green-600">¥${product.price}</span>
                                ${product.originalPrice ? `<span class="text-gray-400 line-through ml-2">¥${product.originalPrice}</span>` : ''}
                            </div>
                            <p class="text-sm text-gray-600">${product.description || ''}</p>
                        </div>
                    `).join('')}
                </div>
                
                <div class="dm-footer text-center">
                    <p class="text-sm text-gray-600 mb-4">扫描二维码了解更多</p>
                    <div class="qr-code bg-gray-200 w-24 h-24 mx-auto rounded-lg flex items-center justify-center">
                        <i class="fas fa-qrcode text-gray-400 text-xl"></i>
                    </div>
                </div>
            </div>
        `;
    }

    showToast(message, type = 'info') {
        // 使用全局的showToast函数
        if (typeof showToast === 'function') {
            showToast(message, type);
        } else {
            console.log(`Toast [${type}]: ${message}`);
        }
    }
}

// 初始化DM生成器
let dmGenerator;
document.addEventListener('DOMContentLoaded', () => {
    dmGenerator = new DMGenerator();
});
