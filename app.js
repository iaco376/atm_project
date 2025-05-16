const serverUrl = 'http://localhost:5050';

const welcomeScreen = document.getElementById('welcomeScreen');
const loginScreen = document.getElementById('loginScreen');
const atmMenu = document.getElementById('atmMenu');
const adminMenu = document.getElementById('adminMenu');

const loginForm = document.getElementById('loginForm');
const loginError = document.getElementById('loginError');
const welcomeText = document.getElementById('welcomeText');
const outputMessage = document.getElementById('outputMessage');

const btnLogoutClient = document.getElementById('btnLogout');
const btnLogoutAdmin = document.getElementById('btnLogoutAdmin');

let currentUser = null;
let currentRole = null;

// La prima apăsare de tastă, trecem de la welcome la login
document.addEventListener('keydown', () => {
  welcomeScreen.style.display = 'none';
  loginScreen.style.display = 'block';
  document.removeEventListener('keydown', arguments.callee);
});

// Login
loginForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  loginError.textContent = '';
  outputMessage.textContent = '';

  const username = loginForm.username.value.trim().toLowerCase();
  const password = loginForm.password.value;

  if (!username || !password) {
    loginError.textContent = 'Completează username și parola.';
    return;
  }

  try {
    const response = await fetch(`${serverUrl}/login`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ username, password })
    });

    if (!response.ok) {
      loginError.textContent = 'Date de autentificare incorecte.';
      return;
    }

    const data = await response.json();

    if (data.success) {
      loginScreen.style.display = 'none';
      currentUser = username;
      currentRole = data.rol;
      welcomeText.textContent = `Bine ai venit, ${username}!`;
      outputMessage.textContent = '';

      if (currentRole === 'admin') {
        adminMenu.style.display = 'block';
        atmMenu.style.display = 'none';
      } else if (currentRole === 'client') {
        atmMenu.style.display = 'block';
        adminMenu.style.display = 'none';
      } else {
        loginError.textContent = 'Rol necunoscut.';
      }

    } else {
      loginError.textContent = 'Date de autentificare incorecte.';
    }

  } catch (error) {
    loginError.textContent = 'Eroare la autentificare.';
    console.error(error);
  }
});

// Logout Client
btnLogoutClient.onclick = () => {
  atmMenu.style.display = 'none';
  loginScreen.style.display = 'block';
  loginForm.reset();
  loginError.textContent = '';
  outputMessage.textContent = '';
  currentUser = null;
  currentRole = null;
  welcomeText.textContent = '';
};

// Logout Admin
btnLogoutAdmin.onclick = () => {
  adminMenu.style.display = 'none';
  loginScreen.style.display = 'block';
  loginForm.reset();
  loginError.textContent = '';
  outputMessage.textContent = '';
  currentUser = null;
  currentRole = null;
  welcomeText.textContent = '';
};

// ==== FUNCȚII CLIENT ====

async function verificareSold() {
  outputMessage.textContent = 'Se verifică soldul...';
  try {
    const res = await fetch(`${serverUrl}/client/verificare_sold`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ utilizator: currentUser })
    });
    const data = await res.json();
    if (res.ok) {
      outputMessage.textContent = `Sold curent: ${data.sold} lei`;
    } else {
      outputMessage.textContent = data.message || 'Eroare la verificare sold.';
    }
  } catch(e) {
    outputMessage.textContent = 'Eroare la comunicare cu serverul.';
  }
}

async function retragereBani() {
  const suma = prompt('Introdu suma pentru retragere:');
  if (!suma) return;
  outputMessage.textContent = 'Se procesează retragerea...';
  try {
    const res = await fetch(`${serverUrl}/client/retragere_bani`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ utilizator: currentUser, suma: parseFloat(suma) })
    });
    const data = await res.json();
    if (res.ok) {
      outputMessage.textContent = data.message;
    } else {
      outputMessage.textContent = data.message || 'Eroare la retragere.';
    }
  } catch(e) {
    outputMessage.textContent = 'Eroare la comunicare cu serverul.';
  }
}

async function depunereBani() {
  const suma = prompt('Introdu suma pentru depunere:');
  if (!suma) return;
  outputMessage.textContent = 'Se procesează depunerea...';
  try {
    const res = await fetch(`${serverUrl}/client/depunere_bani`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ utilizator: currentUser, suma: parseFloat(suma) })
    });
    const data = await res.json();
    if (res.ok) {
      outputMessage.textContent = data.message;
    } else {
      outputMessage.textContent = data.message || 'Eroare la depunere.';
    }
  } catch(e) {
    outputMessage.textContent = 'Eroare la comunicare cu serverul.';
  }
}

async function transferBani() {
  const destinatar = prompt('Introdu numele destinatarului:');
  if (!destinatar) return;
  const suma = prompt('Introdu suma pentru transfer:');
  if (!suma) return;
  outputMessage.textContent = 'Se procesează transferul...';
  try {
    const res = await fetch(`${serverUrl}/client/transfer_bani`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ utilizator: currentUser, destinatar, suma: parseFloat(suma) })
    });
    const data = await res.json();
    if (res.ok) {
      outputMessage.textContent = data.message;
    } else {
      outputMessage.textContent = data.message || 'Eroare la transfer.';
    }
  } catch(e) {
    outputMessage.textContent = 'Eroare la comunicare cu serverul.';
  }
}

// ==== FUNCȚII ADMIN ====

async function creareCont() {
  const nume = prompt('Introdu numele noului cont:');
  if (!nume) return;
  const parola = prompt('Introdu parola:');
  if (!parola) return;
  const tip = prompt('Introdu tipul contului (client/admin):');
  if (!tip) return;
  const rol = tip.toLowerCase() === 'admin' ? 'admin' : 'client';
  const soldInitial = prompt('Introdu soldul inițial (număr):') || '0';

  outputMessage.textContent = 'Se creează contul...';
  try {
    const res = await fetch(`${serverUrl}/admin/creare_cont`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ nume, parola, tip, rol, sold_initial: parseFloat(soldInitial) })
    });
    const data = await res.json();
    if (res.ok) {
      outputMessage.textContent = data.message;
    } else {
      outputMessage.textContent = data.message || 'Eroare la creare cont.';
    }
  } catch(e) {
    outputMessage.textContent = 'Eroare la comunicare cu serverul.';
  }
}

async function inchidereCont() {
  const nume = prompt('Introdu numele contului de șters:');
  if (!nume) return;
  outputMessage.textContent = 'Se șterge contul...';
  try {
    const res = await fetch(`${serverUrl}/admin/inchidere_cont`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ nume })
    });
    const data = await res.json();
    if (res.ok) {
      outputMessage.textContent = data.message;
    } else {
      outputMessage.textContent = data.message || 'Eroare la ștergere cont.';
    }
  } catch(e) {
    outputMessage.textContent = 'Eroare la comunicare cu serverul.';
  }
}

async function listareConturi() {
  outputMessage.textContent = 'Se încarcă lista conturilor...';
  try {
    const res = await fetch(`${serverUrl}/admin/listare_conturi`);
    const data = await res.json();
    if (res.ok) {
      if (data.conturi && data.conturi.length > 0) {
        outputMessage.innerHTML = '<strong>Conturi existente:</strong><br>' +
          data.conturi.map(c => `${c.nume} - ${c.tip} - ${c.rol} - Sold: ${c.sold}`).join('<br>');
      } else {
        outputMessage.textContent = 'Nu există conturi.';
      }
    } else {
      outputMessage.textContent = 'Eroare la încărcarea conturilor.';
    }
  } catch(e) {
    outputMessage.textContent = 'Eroare la comunicare cu serverul.';
  }
}

async function conturiCurente() {
  outputMessage.textContent = 'Se încarcă conturile curente...';
  try {
    const res = await fetch(`${serverUrl}/admin/conturi_curente`);
    const data = await res.json();
    if (res.ok) {
      if (data.conturi_curente && data.conturi_curente.length > 0) {
        outputMessage.innerHTML = '<strong>Conturi curente:</strong><br>' +
          data.conturi_curente.map(c => `${c.nume} - Sold: ${c.sold}`).join('<br>');
      } else {
        outputMessage.textContent = 'Nu există conturi curente.';
      }
    } else {
      outputMessage.textContent = 'Eroare la încărcarea conturilor curente.';
    }
  } catch(e) {
    outputMessage.textContent = 'Eroare la comunicare cu serverul.';
  }
}

async function depoziteBancare() {
  outputMessage.textContent = 'Se încarcă depozitele bancare...';
  try {
    const res = await fetch(`${serverUrl}/admin/depozite_bancare`);
    const data = await res.json();
    if (res.ok) {
      if (data.depozite_bancare && data.depozite_bancare.length > 0) {
        outputMessage.innerHTML = '<strong>Depozite bancare:</strong><br>' +
          data.depozite_bancare.map(d => `${d.nume} - Sold: ${d.sold}`).join('<br>');
      } else {
        outputMessage.textContent = 'Nu există depozite bancare.';
      }
    } else {
      outputMessage.textContent = 'Eroare la încărcarea depozitelor.';
    }
  } catch(e) {
    outputMessage.textContent = 'Eroare la comunicare cu serverul.';
  }
}

// ==== LEGĂTURA BUTOANELOR CLIENT ====

document.getElementById('btnViewInfo').onclick = verificareSold;
document.getElementById('btnDeposit').onclick = depunereBani;
document.getElementById('btnWithdraw').onclick = retragereBani;
document.getElementById('btnTransfer').onclick = transferBani;
// 'btnTransactions' doar afișează alert momentan
document.getElementById('btnTransactions').onclick = () => alert('Istoric tranzacții (nu este implementat)');

// ==== LEGĂTURA BUTOANELOR ADMIN ====

document.getElementById('btnCreareCont').onclick = creareCont;
document.getElementById('btnListareConturi').onclick = listareConturi;
document.getElementById('btnInchidereCont').onclick = inchidereCont;
document.getElementById('btnDepozite').onclick = depoziteBancare;
document.getElementById('btnConturiCurente').onclick = conturiCurente;
