// QR生成器核心功能
class QRGenerator {
    constructor() {
        this.generatedQRs = [];
        this.currentQR = null;
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadHistory();
    }

    setupEventListeners() {
        // 类型切换事件
        document.getElementById('qr-type-select')?.addEventListener('change', (e) => {
            this.onTypeChange(e.target.value);
        });

        // 生成按钮事件
        document.getElementById('generate-qr-btn')?.addEventListener('click', () => {
            this.generateQR();
        });

        // 下载按钮事件
        document.getElementById('download-qr-btn')?.addEventListener('click', () => {
            this.downloadQR();
        });

        // 批量生成按钮事件
        document.getElementById('batch-generate-btn')?.addEventListener('click', () => {
            this.showBatchDialog();
        });
    }

    onTypeChange(type) {
        // 显示/隐藏相应的输入字段
        const allInputs = document.querySelectorAll('.qr-input-group');
        allInputs.forEach(input => input.classList.add('hidden'));

        const targetInput = document.getElementById(`${type}-inputs`);
        if (targetInput) {
            targetInput.classList.remove('hidden');
        }

        // 清空其他类型的输入
        this.clearOtherInputs(type);
    }

    clearOtherInputs(currentType) {
        const types = ['text', 'url', 'wifi', 'email', 'phone', 'sms', 'contact'];
        types.forEach(type => {
            if (type !== currentType) {
                const inputs = document.querySelectorAll(`#${type}-inputs input, #${type}-inputs textarea`);
                inputs.forEach(input => input.value = '');
            }
        });
    }

    getQRData() {
        const type = document.getElementById('qr-type-select').value;
        
        switch (type) {
            case 'text':
                return document.getElementById('text-input').value;
            
            case 'url':
                let url = document.getElementById('url-input').value;
                if (url && !url.startsWith('http://') && !url.startsWith('https://')) {
                    url = 'https://' + url;
                }
                return url;
            
            case 'wifi':
                const ssid = document.getElementById('wifi-ssid').value;
                const password = document.getElementById('wifi-password').value;
                const security = document.getElementById('wifi-security').value;
                return `WIFI:T:${security};S:${ssid};P:${password};H:false;;`;
            
            case 'email':
                const to = document.getElementById('email-to').value;
                const subject = document.getElementById('email-subject').value;
                const body = document.getElementById('email-body').value;
                return `mailto:${to}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
            
            case 'phone':
                return `tel:${document.getElementById('phone-input').value}`;
            
            case 'sms':
                const phone = document.getElementById('sms-phone').value;
                const message = document.getElementById('sms-message').value;
                return `sms:${phone}:${message}`;
            
            case 'contact':
                const name = document.getElementById('contact-name').value;
                const contactPhone = document.getElementById('contact-phone').value;
                const email = document.getElementById('contact-email').value;
                const org = document.getElementById('contact-org').value;
                return `BEGIN:VCARD\nVERSION:3.0\nFN:${name}\nORG:${org}\nTEL:${contactPhone}\nEMAIL:${email}\nEND:VCARD`;
            
            default:
                return '';
        }
    }

    validateInput() {
        const type = document.getElementById('qr-type-select').value;
        const data = this.getQRData();
        
        if (!data || data.trim() === '') {
            this.showToast('请填写必要的信息', 'warning');
            return false;
        }

        // 特定类型的验证
        switch (type) {
            case 'url':
                try {
                    new URL(data);
                } catch {
                    this.showToast('请输入有效的网址', 'warning');
                    return false;
                }
                break;
            
            case 'email':
                const email = document.getElementById('email-to').value;
                if (!email || !email.includes('@')) {
                    this.showToast('请输入有效的邮箱地址', 'warning');
                    return false;
                }
                break;
            
            case 'wifi':
                if (!document.getElementById('wifi-ssid').value) {
                    this.showToast('请输入WiFi名称', 'warning');
                    return false;
                }
                break;
            
            case 'contact':
                if (!document.getElementById('contact-name').value) {
                    this.showToast('请输入联系人姓名', 'warning');
                    return false;
                }
                break;
        }

        return true;
    }

    async generateQR() {
        if (!this.validateInput()) {
            return;
        }

        const type = document.getElementById('qr-type-select').value;
        const data = this.getQRData();
        const size = document.getElementById('qr-size-select').value;

        try {
            const response = await fetch('/api/qr/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    data: data,
                    type: type,
                    size: parseInt(size)
                })
            });

            const result = await response.json();

            if (result.success) {
                this.currentQR = {
                    data: result.data,
                    filename: result.filename,
                    type: type,
                    content: data,
                    timestamp: new Date().toISOString()
                };

                this.displayQR(result.data);
                this.addToHistory(this.currentQR);
                this.showToast('QR码生成成功！', 'success');
            } else {
                this.showToast(result.error || '生成失败', 'error');
            }
        } catch (error) {
            console.error('生成QR码失败:', error);
            this.showToast('生成失败，请稍后重试', 'error');
        }
    }

    displayQR(base64Data) {
        const preview = document.getElementById('qr-preview');
        if (!preview) return;

        const img = document.createElement('img');
        img.src = 'data:image/png;base64,' + base64Data;
        img.alt = 'Generated QR Code';
        img.className = 'max-w-full h-auto mx-auto';

        preview.innerHTML = '';
        preview.appendChild(img);
        preview.classList.remove('hidden');
    }

    downloadQR() {
        if (!this.currentQR) {
            this.showToast('请先生成QR码', 'warning');
            return;
        }

        const link = document.createElement('a');
        link.download = this.currentQR.filename;
        link.href = 'data:image/png;base64,' + this.currentQR.data;
        link.click();

        this.showToast('QR码下载成功！', 'success');
    }

    addToHistory(qrData) {
        this.generatedQRs.unshift(qrData);
        
        // 限制历史记录数量
        if (this.generatedQRs.length > 20) {
            this.generatedQRs = this.generatedQRs.slice(0, 20);
        }

        this.saveHistory();
        this.renderHistory();
    }

    renderHistory() {
        const container = document.getElementById('qr-history');
        if (!container) return;

        container.innerHTML = this.generatedQRs.map((qr, index) => `
            <div class="history-item bg-white p-3 rounded-lg border border-gray-200 mb-2">
                <div class="flex items-center justify-between">
                    <div class="flex items-center space-x-3">
                        <img src="data:image/png;base64,${qr.data}" 
                             alt="QR Code" 
                             class="w-12 h-12 rounded">
                        <div>
                            <p class="text-sm font-medium text-gray-900">${this.getTypeName(qr.type)}</p>
                            <p class="text-xs text-gray-500">${new Date(qr.timestamp).toLocaleString()}</p>
                        </div>
                    </div>
                    <div class="flex space-x-2">
                        <button onclick="qrGenerator.downloadFromHistory(${index})" 
                                class="text-blue-600 hover:text-blue-800 text-sm">
                            <i class="fas fa-download"></i>
                        </button>
                        <button onclick="qrGenerator.deleteFromHistory(${index})" 
                                class="text-red-600 hover:text-red-800 text-sm">
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                </div>
            </div>
        `).join('');
    }

    getTypeName(type) {
        const names = {
            'text': '文本QR码',
            'url': '网址QR码',
            'wifi': 'WiFi配置QR码',
            'email': '邮件QR码',
            'phone': '电话QR码',
            'sms': '短信QR码',
            'contact': '联系人QR码'
        };
        return names[type] || 'QR码';
    }

    downloadFromHistory(index) {
        const qr = this.generatedQRs[index];
        if (!qr) return;

        const link = document.createElement('a');
        link.download = qr.filename;
        link.href = 'data:image/png;base64,' + qr.data;
        link.click();

        this.showToast('QR码下载成功！', 'success');
    }

    deleteFromHistory(index) {
        this.generatedQRs.splice(index, 1);
        this.saveHistory();
        this.renderHistory();
        this.showToast('已删除', 'success');
    }

    showBatchDialog() {
        // 显示批量生成对话框
        const dialog = document.getElementById('batch-dialog');
        if (dialog) {
            dialog.classList.remove('hidden');
        }
    }

    async batchGenerate() {
        const textarea = document.getElementById('batch-data');
        if (!textarea) return;

        const lines = textarea.value.split('\n').filter(line => line.trim());
        if (lines.length === 0) {
            this.showToast('请输入要批量生成的数据', 'warning');
            return;
        }

        const type = document.getElementById('batch-type').value;
        const results = [];

        for (let i = 0; i < lines.length; i++) {
            const line = lines[i].trim();
            if (!line) continue;

            try {
                const response = await fetch('/api/qr/generate', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        data: line,
                        type: type,
                        size: 512
                    })
                });

                const result = await response.json();
                if (result.success) {
                    results.push({
                        data: result.data,
                        filename: result.filename,
                        type: type,
                        content: line,
                        timestamp: new Date().toISOString()
                    });
                }
            } catch (error) {
                console.error(`生成第${i+1}个QR码失败:`, error);
            }
        }

        if (results.length > 0) {
            this.generatedQRs.unshift(...results);
            this.saveHistory();
            this.renderHistory();
            this.showToast(`批量生成完成！共生成${results.length}个QR码`, 'success');
        } else {
            this.showToast('批量生成失败', 'error');
        }

        // 关闭对话框
        const dialog = document.getElementById('batch-dialog');
        if (dialog) {
            dialog.classList.add('hidden');
        }
    }

    saveHistory() {
        localStorage.setItem('qr_generator_history', JSON.stringify(this.generatedQRs));
    }

    loadHistory() {
        const saved = localStorage.getItem('qr_generator_history');
        if (saved) {
            try {
                this.generatedQRs = JSON.parse(saved);
                this.renderHistory();
            } catch (error) {
                console.error('加载历史记录失败:', error);
            }
        }
    }

    showToast(message, type = 'info') {
        if (typeof showToast === 'function') {
            showToast(message, type);
        } else {
            console.log(`Toast [${type}]: ${message}`);
        }
    }
}

// 初始化QR生成器
let qrGenerator;
document.addEventListener('DOMContentLoaded', () => {
    qrGenerator = new QRGenerator();
});
