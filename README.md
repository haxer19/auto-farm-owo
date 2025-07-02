## LẤY TOKEN DISCORD (USER)

1. Bấm `F12` để mở **DevTools** (hoặc chuột phải → "Kiểm tra").
2. Bấm tổ hợp **Ctrl + Shift + M** để **bật "Toggle device toolbar"** (trông như giao diện điện thoại ấy).
3. Vào tab `Console`, dán đoạn code dưới đây và nhấn Enter:

```javascript
function tknMgr() {
  const w = window.open('', '', 'top=50,left='+(screen.width-400)+',width=400,height=300');
  if (!w || !w.document) return;

  w.document.write(`
    <style>
      body { margin: 0; font-family: 'Segoe UI', sans-serif; background: linear-gradient(135deg, #1e1e2f, #2a2a4a); display: flex; justify-content: center; align-items: center; min-height: 100vh; }
      .pop { width: 320px; padding: 24px; background: rgba(255, 255, 255, 0.95); border-radius: 16px; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2); transform: scale(0.8); opacity: 0; animation: popFade 0.3s ease-out forwards; }
      @keyframes popFade { to { transform: scale(1); opacity: 1; } }
      .tabs { display: flex; gap: 8px; margin-bottom: 16px; }
      .tab { flex: 1; padding: 12px; text-align: center; background: #e0e0e0; border-radius: 8px; cursor: pointer; transition: all 0.3s ease; font-weight: 600; color: #333; }
      .tab:hover { background: #d0d0d0; }
      .tab.active { background: #5865f2; color: white; }
      .tab-ct { display: none; }
      .tab-ct.active { display: block; }
      .tkn-box, .inp-box { background: #f0f0f5; padding: 12px; border-radius: 8px; font-family: 'Roboto Mono', monospace; font-size: 14px; text-align: center; word-break: break-all; transition: all 0.3s ease; font-weight: 500; color: #222; }
      .tkn-box:hover, .inp-box:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1); }
      .inp-box input { width: 100%; padding: 8px; border: none; background: transparent; outline: none; font-family: 'Roboto Mono', monospace; font-size: 14px; }
      .btns { display: flex; gap: 12px; justify-content: center; margin-top: 16px; }
      button { padding: 10px 20px; border: none; border-radius: 8px; color: white; cursor: pointer; font-size: 14px; transition: all 0.2s ease; }
      button:hover { transform: translateY(-1px); box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15); }
      #tog, #lgn { background: #5865f2; }
      #tog:hover, #lgn:hover { background: #4752c4; }
      #cpy { background: #2ecc71; }
      #cpy:hover { background: #27ae60; }
      .err, .suc, .hint { font-size: 12px; text-align: center; margin-top: 12px; animation: errFade 0.3s ease; }
      .err { color: #e74c3c; }
      .suc { color: #2ecc71; }
      .hint { color: #f1c40f; }
      @keyframes errFade { from { opacity: 0; } to { opacity: 1; } }
    </style>
    <div class="pop">
      <div class="tabs">
        <div id="tkn-tab" class="tab">Get Token</div>
        <div id="lgn-tab" class="tab active">Login</div>
      </div>
      <div id="tkn-ct" class="tab-ct">
        <div id="tkn" class="tkn-box"></div>
        <div class="btns">
          <button id="tog">Show</button>
          <button id="cpy">Copy</button>
        </div>
        <div id="err-get" class="err" style="display: none;">Error: Try enabling "Toggle device toolbar" (Ctrl+Shift+M).</div>
      </div>
      <div id="lgn-ct" class="tab-ct active">
        <div class="inp-box">
          <input id="tkn-inp" type="text" placeholder="Enter Discord Token">
        </div>
        <div class="btns">
          <button id="lgn">Login</button>
        </div>
        <div id="err-lgn" class="err" style="display: none;">Invalid token or login failed.</div>
        <div id="suc-lgn" class="suc" style="display: none;">Login successful!</div>
        <div id="hint-lgn" class="hint" style="display: none;">This tab shows because the script couldn't retrieve a token or you're not logged in. If logged in, enable "Toggle device toolbar" (Ctrl+Shift+M) to get the token.</div>
      </div>
    </div>
  `);

  const tkn = w.localStorage.token?.slice(1, -1) || '';
  const logged = !!tkn;

  const tknTab = w.document.getElementById('tkn-tab');
  const lgnTab = w.document.getElementById('lgn-tab');
  const tknCt = w.document.getElementById('tkn-ct');
  const lgnCt = w.document.getElementById('lgn-ct');
  const tknEl = w.document.getElementById('tkn');
  const togBtn = w.document.getElementById('tog');
  const cpyBtn = w.document.getElementById('cpy');
  const errGet = w.document.getElementById('err-get');
  const tknInp = w.document.getElementById('tkn-inp');
  const lgnBtn = w.document.getElementById('lgn');
  const errLgn = w.document.getElementById('err-lgn');
  const sucLgn = w.document.getElementById('suc-lgn');
  const hintLgn = w.document.getElementById('hint-lgn');

  if (!logged) {
    tknTab.style.display = 'none';
    lgnTab.style.display = 'none';
    tknCt.style.display = 'none';
    hintLgn.style.display = 'block';
  } else {
    tknTab.classList.add('active');
    lgnCt.classList.remove('active');
    tknCt.classList.add('active');
    hintLgn.style.display = 'none';
  }

  tknTab.addEventListener('click', () => {
    tknTab.classList.add('active');
    lgnTab.classList.remove('active');
    tknCt.classList.add('active');
    lgnCt.classList.remove('active');
  });

  lgnTab.addEventListener('click', () => {
    lgnTab.classList.add('active');
    tknTab.classList.remove('active');
    lgnCt.classList.add('active');
    tknCt.classList.remove('active');
  });

  try {
    tknEl.textContent = tkn ? '*'.repeat(tkn.length) : 'No token found';
    if (!tkn && logged) errGet.style.display = 'block';

    togBtn.addEventListener('click', () => {
      togBtn.textContent = togBtn.textContent === 'Show' ? 'Hide' : 'Show';
      tknEl.textContent = togBtn.textContent === 'Hide' ? tkn : '*'.repeat(tkn.length);
      togBtn.style.transform = 'scale(0.95)';
      setTimeout(() => togBtn.style.transform = 'scale(1)', 100);
    });

    cpyBtn.addEventListener('click', async () => {
      if (tkn) {
        await navigator.clipboard.writeText(tkn).catch(() => {
          const ta = w.document.createElement('textarea');
          ta.value = tkn;
          w.document.body.appendChild(ta);
          ta.select();
          w.document.execCommand('copy');
          w.document.body.removeChild(ta);
        });
        cpyBtn.textContent = 'Copied!';
        cpyBtn.style.background = '#27ae60';
        setTimeout(() => {
          cpyBtn.textContent = 'Copy';
          cpyBtn.style.background = '#2ecc71';
        }, 1000);
      }
    });

    lgnBtn.addEventListener('click', async () => {
      const inpTkn = tknInp.value.trim();
      if (!inpTkn) {
        errLgn.style.display = 'block';
        return;
      }

      try {
        const res = await fetch('https://discord.com/api/v9/users/@me', {
          headers: { Authorization: inpTkn }
        });
        if (res.ok) {
          w.localStorage.token = `"${inpTkn}"`;
          sucLgn.style.display = 'block';
          errLgn.style.display = 'none';
          setTimeout(() => {
            window.location.reload();
            w.window.close();
          }, 1000);
        } else {
          errLgn.style.display = 'block';
        }
      } catch {
        errLgn.style.display = 'block';
      }
    });
  } catch (e) {
    errGet.style.display = 'block';
  }
}
tknMgr();
```

---

* Nếu dán code mà không hiện popup → bật lại `Toggle device toolbar` rồi **reload Discord Web**, làm lại.
