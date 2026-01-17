async function fetchStatus() {
  const res = await fetch("/api/status");
  const s = await res.json();

  document.getElementById("doorStatus").textContent = s.door;
  document.getElementById("windowStatus").textContent = s.window;
  document.getElementById("laundryStatus").textContent = s.laundry;
  document.getElementById("fanStatus").textContent = s.fan;
  document.getElementById("buzzerStatus").textContent = s.buzzer;
  document.getElementById("ledStatus").textContent = s.led;

  document.getElementById("piMode").textContent = s.on_pi ? "Running on Raspberry Pi ✅" : "MOCK mode (not Pi) ⚠️";
}

function showToast(msg) {
  document.getElementById("toastMsg").textContent = msg;
  const toastEl = document.getElementById("toast");
  const t = bootstrap.Toast.getOrCreateInstance(toastEl, { delay: 1800 });
  t.show();
}

async function doAction(device, action) {
  try {
    const res = await fetch("/api/action", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ device, action })
    });

    const data = await res.json();
    if (!data.ok) {
      showToast("❌ " + (data.error || data.message || "Failed"));
      return;
    }
    showToast("✅ " + data.message);
    await fetchStatus();
  } catch (e) {
    showToast("❌ Network error");
  }
}

// initial load + poll
fetchStatus();
setInterval(fetchStatus, 1500);
