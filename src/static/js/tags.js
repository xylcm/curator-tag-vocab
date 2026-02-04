const API = {
    stats: '/tagging/tags/api/stats',
    tags: '/tagging/tags/api/tags',
    tag: (id) => `/tagging/tags/api/tags/${id}`,
    categories: '/tagging/tags/api/categories',
    categoriesConfig: '/tagging/tags/api/categories/config',
    exportProtobuf: '/tagging/tags/api/export/protobuf',
    exportCsv: '/tagging/tags/api/export/csv'
};

let tags = [];
let currentPage = 1;
let totalPages = 1;
let editingTagId = null;
let categoriesData = [];

async function loadCategoriesConfig() {
    try {
        const res = await fetch(API.categoriesConfig);
        const data = await res.json();
        categoriesData = data.categories || [];
    } catch (err) {
        console.error('Failed to load categories config:', err);
        categoriesData = [];
    }
}

async function loadCategories() {
    try {
        const res = await fetch(API.categories);
        const data = await res.json();
        const categorySelect = document.getElementById('category-select');
        const currentValue = categorySelect.value;
        
        categorySelect.innerHTML = '<option value="">All Categories</option>';
        
        data.categories.forEach(category => {
            const option = document.createElement('option');
            option.value = category;
            option.textContent = category;
            categorySelect.appendChild(option);
        });
        
        if (currentValue && data.categories.includes(currentValue)) {
            categorySelect.value = currentValue;
        }
    } catch (err) {
        console.error('Failed to load categories:', err);
    }
}

async function loadStats() {
    try {
        const deleted = document.getElementById('deleted-select').value;
        const res = await fetch(`${API.stats}?deleted=${deleted}`);
        const data = await res.json();
        
        document.getElementById('stat-total').textContent = data.total;
        document.getElementById('stat-available').textContent = data.available;
        document.getElementById('stat-unavailable').textContent = data.unavailable;
        document.getElementById('stat-deleted').textContent = data.deleted;
    } catch (err) {
        console.error('Failed to load stats:', err);
    }
}

async function loadTags(page = 1) {
    const filter = document.getElementById('filter-select').value;
    const deleted = document.getElementById('deleted-select').value;
    const category = document.getElementById('category-select').value;
    const search = document.getElementById('search-input').value.trim();
    const sort = document.getElementById('sort-select').value;
    const order = document.getElementById('order-select').value;
    const container = document.getElementById('tags-container');
    
    container.innerHTML = '<div class="loading">正在加载标签...</div>';
    
    try {
        let url = `${API.tags}?page=${page}&limit=100&sort=${sort}&order=${order}&deleted=${deleted}`;
        if (filter !== 'all') {
            url += `&available=${filter}`;
        }
        if (category) {
            url += `&category=${encodeURIComponent(category)}`;
        }
        if (search) {
            url += `&search=${encodeURIComponent(search)}`;
        }
        
        const res = await fetch(url);
        const data = await res.json();
        tags = data.tags;
        
        currentPage = data.page;
        totalPages = data.total_pages;
        
        renderTags();
        updatePagination();
        await loadStats();
    } catch (err) {
        console.error('Failed to load tags:', err);
        container.innerHTML = '<div class="empty"><h2>加载失败</h2><p>请检查服务器连接</p></div>';
    }
}

function updatePagination() {
    const pagination = document.getElementById('pagination');
    const prevBtn = document.getElementById('prev-btn');
    const nextBtn = document.getElementById('next-btn');
    const pageInfo = document.getElementById('page-info');
    
    if (totalPages <= 1) {
        pagination.style.display = 'none';
        return;
    }
    
    pagination.style.display = 'flex';
    pageInfo.textContent = `第 ${currentPage} 页，共 ${totalPages} 页`;
    
    prevBtn.disabled = currentPage <= 1;
    nextBtn.disabled = currentPage >= totalPages;
}

function renderTags() {
    const container = document.getElementById('tags-container');
    
    if (tags.length === 0) {
        container.innerHTML = '<div class="empty"><h2>没有标签</h2><p>请添加新标签或选择其他过滤条件</p></div>';
        return;
    }
    
    const grid = document.createElement('div');
    grid.className = 'tags-grid';
    container.innerHTML = '';
    container.appendChild(grid);
    
    let index = 0;
    const chunkSize = 20;
    
    function renderChunk() {
        const end = Math.min(index + chunkSize, tags.length);
        const fragment = document.createDocumentFragment();
        
        for (; index < end; index++) {
            const card = createTagCard(tags[index]);
            fragment.appendChild(card);
        }
        
        grid.appendChild(fragment);
        
        if (index < tags.length) {
            requestAnimationFrame(renderChunk);
        }
    }
    
    renderChunk();
}

function createTagCard(tag) {
    const card = document.createElement('div');
    card.className = `tag-card ${tag.available ? 'available' : 'unavailable'}`;
    card.dataset.id = tag.id;
    
    const zhTranslation = tag.translations?.zh_CN || '';
    const enTranslation = tag.translations?.en || '';
    
    const categoryText = tag.category || '';
    const subCategoryText = tag.sub_category || '';
    const hasCategoryInfo = categoryText || subCategoryText;
    
    let categoryDisplay = '';
    if (categoryText && subCategoryText) {
        categoryDisplay = `${escapeHtml(categoryText)} › ${escapeHtml(subCategoryText)}`;
    } else if (categoryText) {
        categoryDisplay = escapeHtml(categoryText);
    } else if (subCategoryText) {
        categoryDisplay = escapeHtml(subCategoryText);
    } else {
        categoryDisplay = '';
    }
    
    // 生成分类下拉框选项
    let categoryOptions = '<option value="">选择分类</option>';
    categoriesData.forEach(cat => {
        if (cat.available) {
            const selected = cat.category === categoryText ? 'selected' : '';
            categoryOptions += `<option value="${escapeHtml(cat.category)}" ${selected}>${escapeHtml(cat.category)}</option>`;
        }
    });
    
    card.innerHTML = `
        <div class="tag-header">
            <div class="tag-name">${escapeHtml(tag.tag)}</div>
            <div class="tag-status">
                <span class="status-badge ${tag.available ? 'available' : 'unavailable'}">
                    ${tag.available ? '可用' : '不可用'}
                </span>
            </div>
        </div>
        
        <div class="tag-info-list">
            <div class="tag-info-item">
                <span class="tag-info-label">English:</span>
                <span class="tag-info-value ${!enTranslation ? 'empty' : ''}">${enTranslation || 'No translation'}</span>
            </div>
            <div class="tag-info-item">
                <span class="tag-info-label">Chinese:</span>
                <span class="tag-info-value ${!zhTranslation ? 'empty' : ''}">${zhTranslation || '暂无翻译'}</span>
            </div>
            <div class="tag-info-item">
                <span class="tag-info-label">Category:</span>
                <span class="tag-info-value ${!hasCategoryInfo ? 'empty' : ''}">${hasCategoryInfo ? categoryDisplay : '暂无分类'}</span>
            </div>
            ${tag.context ? `<div class="tag-info-item">
                <span class="tag-info-label">Context:</span>
                <span class="tag-info-value">${escapeHtml(tag.context)}</span>
            </div>` : ''}
        </div>
        
        <div class="tag-edit-section">
            <div class="tag-edit-field tag-edit-field-primary">
                <label class="tag-edit-label">Tag Name</label>
                <input type="text" class="tag-name-input-edit" value="${escapeHtml(tag.tag)}" placeholder="Enter tag name" data-field="tag">
            </div>
            
            <div class="tag-edit-field">
                <label class="tag-edit-label">English</label>
                <input type="text" class="tag-translation-en-input" placeholder="English translation" value="${escapeHtml(enTranslation)}" data-field="translation_en">
            </div>
            
            <div class="tag-edit-field">
                <label class="tag-edit-label">Chinese</label>
                <input type="text" class="tag-translation-zh-input" placeholder="中文翻译" value="${escapeHtml(zhTranslation)}" data-field="translation_zh">
            </div>
            
            <div class="tag-edit-field">
                <label class="tag-edit-label">Category</label>
                <select class="tag-category-select" data-field="category">
                    ${categoryOptions}
                </select>
            </div>
            
            <div class="tag-edit-field">
                <label class="tag-edit-label">Context</label>
                <input type="text" class="tag-definition-input" value="${escapeHtml(tag.context)}" placeholder="Context description" data-field="context">
            </div>
            
            <div class="edit-actions">
                <button class="btn btn-success btn-small" onclick="saveTag(${tag.id})">保存</button>
                <button class="btn btn-secondary btn-small" onclick="cancelEdit(${tag.id})">取消</button>
            </div>
        </div>
        
        <div class="tag-actions">
            <button class="btn btn-primary btn-small" onclick="editTag(${tag.id})">编辑</button>
            <button class="btn btn-${tag.available ? 'secondary' : 'success'} btn-small" onclick="toggleAvailable(${tag.id}, ${!tag.available})">
                ${tag.available ? '不可用' : '可用'}
            </button>
            <button class="btn btn-danger btn-small" onclick="deleteTag(${tag.id})">删除</button>
        </div>
    `;
    
    return card;
}

function editTag(tagId) {
    if (editingTagId !== null && editingTagId !== tagId) {
        cancelEdit(editingTagId);
    }
    
    editingTagId = tagId;
    const card = document.querySelector(`[data-id="${tagId}"]`);
    
    const tagNameInputEdit = card.querySelector('.tag-name-input-edit');
    const tagTranslationZhInput = card.querySelector('.tag-translation-zh-input');
    const tagTranslationEnInput = card.querySelector('.tag-translation-en-input');
    const tagCategorySelect = card.querySelector('.tag-category-select');
    const tagDefinitionInput = card.querySelector('.tag-definition-input');
    
    const currentTag = tags.find(t => t.id === tagId);
    if (currentTag) {
        tagNameInputEdit.value = currentTag.tag || '';
        tagTranslationZhInput.value = currentTag.translations?.zh_CN || '';
        tagTranslationEnInput.value = currentTag.translations?.en || '';
        tagCategorySelect.value = currentTag.category || '';
        tagDefinitionInput.value = currentTag.context || '';
    }
    
    // 隐藏显示内容
    const tagInfoList = card.querySelector('.tag-info-list');
    const tagActions = card.querySelector('.tag-actions');
    if (tagInfoList) tagInfoList.style.display = 'none';
    if (tagActions) tagActions.style.display = 'none';
    
    // 添加编辑中的卡片样式
    card.classList.add('editing');
    
    // 显示编辑区域
    const editSection = card.querySelector('.tag-edit-section');
    if (editSection) editSection.classList.add('editing');
}

function cancelEdit(tagId) {
    editingTagId = null;
    const card = document.querySelector(`[data-id="${tagId}"]`);
    
    // 显示显示内容
    const tagInfoList = card.querySelector('.tag-info-list');
    const tagActions = card.querySelector('.tag-actions');
    if (tagInfoList) tagInfoList.style.display = 'flex';
    if (tagActions) tagActions.style.display = 'flex';
    
    // 移除编辑中的卡片样式
    card.classList.remove('editing');
    
    // 隐藏编辑区域
    const editSection = card.querySelector('.tag-edit-section');
    if (editSection) editSection.classList.remove('editing');
}

async function saveTag(tagId) {
    const card = document.querySelector(`[data-id="${tagId}"]`);
    
    const newName = card.querySelector('.tag-name-input-edit').value.trim();
    const newTranslationZh = card.querySelector('.tag-translation-zh-input').value.trim();
    const newTranslationEn = card.querySelector('.tag-translation-en-input').value.trim();
    const newCategory = card.querySelector('.tag-category-select').value;
    const newContext = card.querySelector('.tag-definition-input').value.trim();
    
    // 保留原有的 sub_category 值（如果存在）
    const currentTag = tags.find(t => t.id === tagId);
    const newSubCategory = currentTag?.sub_category || '';
    
    if (!newName) {
        showToast('标签名称不能为空', 'error');
        return;
    }
    
    try {
        const translations = {};
        if (newTranslationZh) translations.zh_CN = newTranslationZh;
        if (newTranslationEn) translations.en = newTranslationEn;
        
        const res = await fetch(API.tag(tagId), {
            method: 'PUT',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                tag: newName,
                context: newContext,
                category: newCategory,
                sub_category: newSubCategory,
                translations: translations
            })
        });
        
        const data = await res.json();
        
        if (data.success) {
            showToast('保存成功', 'success');
            editingTagId = null;
            
            const filter = document.getElementById('filter-select').value;
            const deleted = document.getElementById('deleted-select').value;
            const category = document.getElementById('category-select').value;
            const search = document.getElementById('search-input').value.trim();
            const sort = document.getElementById('sort-select').value;
            const order = document.getElementById('order-select').value;
            
            let url = `${API.tags}?page=${currentPage}&limit=100&sort=${sort}&order=${order}&deleted=${deleted}`;
            if (filter !== 'all') {
                url += `&available=${filter}`;
            }
            if (category) {
                url += `&category=${encodeURIComponent(category)}`;
            }
            if (search) {
                url += `&search=${encodeURIComponent(search)}`;
            }
            
            const tagsRes = await fetch(url);
            const tagsData = await tagsRes.json();
            tags = tagsData.tags;
            
            renderTags();
            await loadStats();
            await loadCategories();
        } else {
            showToast('保存失败', 'error');
        }
    } catch (err) {
        console.error('Failed to save tag:', err);
        showToast('保存失败：网络错误', 'error');
    }
}

async function toggleAvailable(tagId, available) {
    try {
        const res = await fetch(API.tag(tagId), {
            method: 'PUT',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                available: available
            })
        });
        
        const data = await res.json();
        
        if (data.success) {
            showToast(`已标记为${available ? '可用' : '不可用'}`, 'success');
            
            const card = document.querySelector(`[data-id="${tagId}"]`);
            if (card) {
                if (available) {
                    card.classList.remove('unavailable');
                    card.classList.add('available');
                } else {
                    card.classList.remove('available');
                    card.classList.add('unavailable');
                }
                
                const statusBadge = card.querySelector('.status-badge');
                statusBadge.textContent = available ? '可用' : '不可用';
                statusBadge.classList.remove('available', 'unavailable');
                statusBadge.classList.add(available ? 'available' : 'unavailable');
                
                const actionButtons = card.querySelectorAll('.tag-actions .btn');
                const toggleBtn = actionButtons[1];
                if (toggleBtn) {
                    toggleBtn.textContent = available ? '不可用' : '可用';
                    toggleBtn.classList.remove('btn-secondary', 'btn-success');
                    toggleBtn.classList.add(available ? 'btn-secondary' : 'btn-success');
                    toggleBtn.onclick = () => toggleAvailable(tagId, !available);
                }
            }
            
            const tagIndex = tags.findIndex(t => t.id === tagId);
            if (tagIndex !== -1) {
                tags[tagIndex].available = available;
            }
            
            await loadStats();
        } else {
            showToast('操作失败', 'error');
        }
    } catch (err) {
        console.error('Failed to toggle available:', err);
        showToast('操作失败：网络错误', 'error');
    }
}

async function deleteTag(tagId) {
    try {
        const res = await fetch(API.tag(tagId), {
            method: 'DELETE'
        });
        
        const data = await res.json();
        
        if (data.success) {
            showToast('删除成功', 'success');
            
            const card = document.querySelector(`[data-id="${tagId}"]`);
            if (card) {
                card.style.transition = 'opacity 0.3s, transform 0.3s';
                card.style.opacity = '0';
                card.style.transform = 'scale(0.9)';
                
                setTimeout(() => {
                    card.remove();
                    tags = tags.filter(t => t.id !== tagId);
                }, 300);
            }
            
            await loadStats();
        } else {
            showToast('删除失败', 'error');
        }
    } catch (err) {
        console.error('Failed to delete tag:', err);
        showToast('删除失败：网络错误', 'error');
    }
}

function openAddModal() {
    document.getElementById('add-modal').classList.add('active');
    document.getElementById('new-tag-name').value = '';
    document.getElementById('new-tag-context').value = '';
    document.getElementById('new-tag-sub-category').value = '';
    document.getElementById('new-tag-translation-zh').value = '';
    document.getElementById('new-tag-translation-en').value = '';
    document.getElementById('new-tag-available').checked = true;
    
    // 填充分类下拉框
    const categorySelect = document.getElementById('new-tag-category');
    categorySelect.innerHTML = '<option value="">选择分类</option>';
    categoriesData.forEach(cat => {
        if (cat.available) {
            const option = document.createElement('option');
            option.value = cat.category;
            option.textContent = cat.category;
            categorySelect.appendChild(option);
        }
    });
}

function closeAddModal() {
    document.getElementById('add-modal').classList.remove('active');
}

async function saveNewTag() {
    const name = document.getElementById('new-tag-name').value.trim();
    const context = document.getElementById('new-tag-context').value.trim();
    const category = document.getElementById('new-tag-category').value;
    const subCategory = document.getElementById('new-tag-sub-category').value.trim();
    const translationZh = document.getElementById('new-tag-translation-zh').value.trim();
    const translationEn = document.getElementById('new-tag-translation-en').value.trim();
    const available = document.getElementById('new-tag-available').checked;
    
    if (!name) {
        showToast('标签名称不能为空', 'error');
        return;
    }
    
    try {
        const translations = {};
        if (translationZh) translations.zh_CN = translationZh;
        if (translationEn) translations.en = translationEn;
        
        const res = await fetch(API.tags, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                tag: name,
                context: context,
                category: category,
                sub_category: subCategory,
                translations: translations,
                available: available
            })
        });
        
        const data = await res.json();
        
        if (data.success) {
            showToast('添加成功', 'success');
            closeAddModal();
            await loadCategories();
            await loadTags(1);
        } else {
            showToast('添加失败', 'error');
        }
    } catch (err) {
        console.error('Failed to add tag:', err);
        showToast('添加失败：网络错误', 'error');
    }
}

function showToast(message, type = 'success') {
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.textContent = message;
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.remove();
    }, 3000);
}

async function exportProtobuf() {
    try {
        showToast('正在导出 Protobuf...', 'info');
        const response = await fetch(API.exportProtobuf);
        
        if (!response.ok) {
            throw new Error('Export failed');
        }
        
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        
        // 从响应头获取文件名
        const contentDisposition = response.headers.get('content-disposition');
        let filename = 'tags_vocabulary.pb';
        if (contentDisposition) {
            const matches = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/.exec(contentDisposition);
            if (matches != null && matches[1]) {
                filename = matches[1].replace(/['"]/g, '');
            }
        }
        
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        
        showToast('Protobuf 导出成功', 'success');
    } catch (err) {
        console.error('Failed to export protobuf:', err);
        showToast('导出失败：网络错误', 'error');
    }
}

async function exportCsv() {
    try {
        showToast('正在导出 CSV...', 'info');
        const response = await fetch(API.exportCsv);
        
        if (!response.ok) {
            throw new Error('Export failed');
        }
        
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        
        // 从响应头获取文件名
        const contentDisposition = response.headers.get('content-disposition');
        let filename = 'tags_vocabulary.csv';
        if (contentDisposition) {
            const matches = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/.exec(contentDisposition);
            if (matches != null && matches[1]) {
                filename = matches[1].replace(/['"]/g, '');
            }
        }
        
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        
        showToast('CSV 导出成功', 'success');
    } catch (err) {
        console.error('Failed to export CSV:', err);
        showToast('导出失败：网络错误', 'error');
    }
}

const escapeDiv = document.createElement('div');
function escapeHtml(text) {
    if (text === null || text === undefined) return '';
    escapeDiv.textContent = text;
    return escapeDiv.innerHTML;
}

// Event listeners
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('load-btn').onclick = () => loadTags(1);
    document.getElementById('add-btn').onclick = openAddModal;
    document.getElementById('export-protobuf-btn').onclick = exportProtobuf;
    document.getElementById('export-csv-btn').onclick = exportCsv;
    document.getElementById('deleted-select').onchange = () => {
        loadStats();
        loadTags(1);
    };
    document.getElementById('filter-select').onchange = () => loadTags(1);
    document.getElementById('category-select').onchange = () => loadTags(1);
    document.getElementById('sort-select').onchange = () => loadTags(1);
    document.getElementById('order-select').onchange = () => loadTags(1);
    document.getElementById('prev-btn').onclick = () => loadTags(currentPage - 1);
    document.getElementById('next-btn').onclick = () => loadTags(currentPage + 1);
    
    let searchTimeout;
    document.getElementById('search-input').oninput = function() {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(() => {
            loadTags(1);
        }, 500);
    };
    
    document.getElementById('search-input').onkeypress = function(e) {
        if (e.key === 'Enter') {
            clearTimeout(searchTimeout);
            loadTags(1);
        }
    };

    document.getElementById('add-modal').onclick = function(e) {
        if (e.target === this) {
            closeAddModal();
        }
    };

    // Initialize
    loadCategoriesConfig().then(() => {
        loadCategories();
        loadStats();
        loadTags(1);
    });
});
