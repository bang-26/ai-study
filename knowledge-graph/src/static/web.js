'use strict';

// ===== DOM 引用 =====
const dialogArea = document.getElementById('dialog-area');
const input = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');

// ===== 状态 =====
let isProcessing = false;
const messageHistory = [];

// ===== Markdown 配置 =====
let marked;
if (typeof marked !== 'undefined') {
    marked.setOptions({
        breaks: false,
        gfm: true
    });
}

// ===== 初始化 =====
function init() {
    bindEvents();
    input.focus();
}

function bindEvents() {
    // 发送按钮
    sendBtn.addEventListener('click', sendMessage);

    // 回车发送
    input.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    // 自动调整高度
    input.addEventListener('input', () => {
        input.style.height = 'auto';
        input.style.height = Math.min(input.scrollHeight, 200) + 'px';
    });

    // Ctrl+L 清空对话
    document.addEventListener('keydown', (e) => {
        if ((e.ctrlKey || e.metaKey) && e.key === 'l') {
            e.preventDefault();
            clearChat();
        }
    });
}

// ===== 发送消息 =====
async function sendMessage() {
    const message = input.value.trim();
    if (!message || isProcessing) return;

    isProcessing = true;
    sendBtn.disabled = true;

    addMessage(message, true);
    input.value = '';
    input.style.height = 'auto';

    const loadingBubble = createLoadingBubble();
    dialogArea.appendChild(loadingBubble);
    scrollToBottom();

    let responseContent = null;

    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message })
        });

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }

        const data = await response.json();
        responseContent = data.message;
    } catch (error) {
        console.error('请求失败:', error);
        responseContent = '系统暂时无法响应，请稍后再试 😥';
    } finally {
        loadingBubble.remove();
        if (responseContent !== null) {
            addMessage(responseContent, false);
        }
        isProcessing = false;
        sendBtn.disabled = false;
        input.focus();
    }
}

// ===== 添加消息 =====
function addMessage(content, isUser) {
    const bubble = document.createElement('div');
    bubble.classList.add('message-bubble', isUser ? 'user-message' : 'bot-message', 'new-message');

    if (!isUser && typeof marked !== 'undefined' && typeof DOMPurify !== 'undefined') {
        const mdContainer = document.createElement('div');
        mdContainer.className = 'markdown-content';
        const dirty = marked.parse(content.toString());
        mdContainer.innerHTML = DOMPurify.sanitize(dirty, {
            ADD_TAGS: ['iframe'],
            ADD_ATTR: ['allowfullscreen']
        });
        bubble.appendChild(mdContainer);
    } else {
        bubble.textContent = content;
    }

    // 时间戳
    const timeSpan = document.createElement('span');
    timeSpan.className = 'message-time';
    timeSpan.textContent = formatTime(new Date());
    bubble.appendChild(timeSpan);

    // 动画结束后移除 class
    bubble.addEventListener('animationend', function handler() {
        this.classList.remove('new-message');
        this.removeEventListener('animationend', handler);
    });

    dialogArea.appendChild(bubble);
    scrollToBottom();

    // 记录历史
    messageHistory.push({ role: isUser ? 'user' : 'assistant', content, time: Date.now() });
}

// ===== 加载气泡 =====
function createLoadingBubble() {
    const bubble = document.createElement('div');
    bubble.classList.add('message-bubble', 'bot-message', 'new-message');

    const container = document.createElement('div');
    container.className = 'loading-container';

    const loader = document.createElement('div');
    loader.className = 'loader';

    container.appendChild(loader);
    container.appendChild(document.createTextNode('正在思索中...'));
    bubble.appendChild(container);

    return bubble;
}

// ===== 清空对话 =====
function clearChat() {
    if (messageHistory.length === 0) return;
    if (!confirm('确定清空当前对话吗？')) return;

    dialogArea.querySelectorAll('.message-bubble').forEach(el => el.remove());
    messageHistory.length = 0;

    // 恢复欢迎语
    const welcome = document.createElement('div');
    welcome.className = 'bot-message message-bubble';
    welcome.textContent = '您好！我是电商智能客服，请问有什么需要我帮忙的？';
    dialogArea.appendChild(welcome);
}

// ===== 工具函数 =====
function formatTime(date) {
    const h = String(date.getHours()).padStart(2, '0');
    const m = String(date.getMinutes()).padStart(2, '0');
    return `${h}:${m}`;
}

function scrollToBottom() {
    requestAnimationFrame(() => {
        window.scrollTo({
            top: document.body.scrollHeight,
            behavior: 'smooth'
        });
    });
}

// ===== 启动 =====
document.addEventListener('DOMContentLoaded', init);
