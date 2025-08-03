const { app, BrowserWindow } = require('electron');
const path = require('path');
const { spawn } = require('child_process');

let djangoProcess = null;

function createWindow() {
    const mainWindow = new BrowserWindow({
        width: 1200,
        height: 800,
        webPreferences: {
            preload: path.join(__dirname, 'preload.js'),
            contextIsolation: true,
        }
    });

    // Start Django server
    const djangoAppPath = path.join(__dirname, 'nool');
    djangoProcess = spawn('python', ['manage.py', 'runserver', '--noreload'], { cwd: djangoAppPath });

    djangoProcess.stdout.on('data', (data) => {
        console.log(`Django stdout: ${data}`);
    });

    djangoProcess.stderr.on('data', (data) => {
        console.error(`Django stderr: ${data}`);
    });

    // Load the Django app after a short delay to allow the server to start
    setTimeout(() => {
        mainWindow.loadURL('http://127.0.0.1:8000');
    }, 5000); // 5 seconds delay

    // Open the DevTools.
    // mainWindow.webContents.openDevTools();
}

app.whenReady().then(() => {
    createWindow();

    app.on('activate', function() {
        if (BrowserWindow.getAllWindows().length === 0) createWindow();
    });
});

app.on('window-all-closed', function() {
    if (process.platform !== 'darwin') {
        if (djangoProcess) {
            djangoProcess.kill();
        }
        app.quit();
    }
});
