## LẤY TOKEN DISCORD (USER)

1. Bấm `F12` để mở **DevTools** (hoặc chuột phải → "Kiểm tra").
2. Bấm tổ hợp **Ctrl + Shift + M** để **bật "Toggle device toolbar"** (trông như giao diện điện thoại ấy).
3. Vào tab `Console`, dán đoạn code dưới đây và nhấn Enter:

```javascript
function getToken() {
    const popup = window.open('', '', 'top=50,left='+(screen.width-400)+',width=400,height=300');
    if (!popup || !popup.document) {
        return;
    }

    popup.document.write(`
        <style>
            body { margin: 0; font-family: 'Segoe UI', sans-serif; background: linear-gradient(135deg, #1e1e2f, #2a2a4a); display: flex; justify-content: center; align-items: center; min-height: 100vh; }
            .popup { width: 300px; padding: 24px; background: rgba(255, 255, 255, 0.95); border-radius: 16px; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2); transform: scale(0.8); opacity: 0; animation: popupFadeIn 0.3s ease-out forwards; }
            @keyframes popupFadeIn { to { transform: scale(1); opacity: 1; } }
            .token-container { background: #f0f0f5; padding: 12px; border-radius: 8px; font-family: 'Courier New', monospace; text-align: center; word-break: break-all; transition: all 0.3s ease; font-weight: bold; color: cyan; }
            .token-container:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1); }
            .buttons { display: flex; gap: 12px; justify-content: center; margin-top: 16px; }
            button { padding: 10px 20px; border: none; border-radius: 8px; color: white; cursor: pointer; font-size: 14px; transition: all 0.2s ease; }
            button:hover { transform: translateY(-1px); box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15); }
            #toggle { background: #5865f2; }
            #toggle:hover { background: #4752c4; }
            #copy { background: #2ecc71; }
            #copy:hover { background: #27ae60; }
            .error { color: #e74c3c; font-size: 12px; text-align: center; margin-top: 12px; animation: errorFadeIn 0.3s ease; }
            @keyframes errorFadeIn { from { opacity: 0; } to { opacity: 1; } }
        </style>
        <div class="popup">
            <div id="token" class="token-container"></div>
            <div class="buttons">
                <button id="toggle">Show</button>
                <button id="copy">Copy</button>
            </div>
            <div id="error" class="error" style="display: none;">Error: Try enabling "Toggle device toolbar" (Ctrl+Shift+M).</div>
        </div>
    `);

    try {
        window.dispatchEvent(new Event('beforeunload'));
        const token = popup.localStorage.token?.slice(1, -1) || '';
        const tokenEl = popup.document.getElementById('token');
        const toggleBtn = popup.document.getElementById('toggle');
        const copyBtn = popup.document.getElementById('copy');
        const errorEl = popup.document.getElementById('error');

        tokenEl.textContent = token ? '*'.repeat(token.length) : 'No token found';
        if (!token) errorEl.style.display = 'block';

        toggleBtn.addEventListener('click', () => {
            toggleBtn.textContent = toggleBtn.textContent === 'Show' ? 'Hide' : 'Show';
            tokenEl.textContent = toggleBtn.textContent === 'Hide' ? token : '*'.repeat(token.length);
            toggleBtn.style.transform = 'scale(0.95)';
            setTimeout(() => toggleBtn.style.transform = 'scale(1)', 100);
        });

        copyBtn.addEventListener('click', async () => {
            if (token) {
                await navigator.clipboard.writeText(token).catch(() => {
                    const textarea = popup.document.createElement('textarea');
                    textarea.value = token;
                    popup.document.body.appendChild(textarea);
                    textarea.select();
                    popup.document.execCommand('copy');
                    popup.document.body.removeChild(textarea);
                });
                copyBtn.textContent = 'Copied!';
                copyBtn.style.background = '#27ae60';
                setTimeout(() => {
                    copyBtn.textContent = 'Copy';
                    copyBtn.style.background = '#2ecc71';
                }, 1000);
            }
        });
    } catch (e) {
        popup.document.getElementById('error').style.display = 'block';
    }
}
getToken();
```

---

* Nếu dán code mà không hiện popup → bật lại `Toggle device toolbar` rồi **reload Discord Web**, làm lại.