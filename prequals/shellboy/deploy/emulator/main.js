const APP_PORT = 1337;

const express   = require("express");
const path      = require("path");
const WebSocket = require("ws");
const http      = require("http")
const zlib      = require("zlib");
const emulator  = require("./src/emulator.js");

/**
 * Setup the frontend endpoints
 * @param {*} front The frontend app
 * @param {*} gameboy The gameboy emulator
 */
function setupFrontend(front, gameboy) {

    // Define static contents
    front.use(express.static("public"));

    // Index page
    front.get("/", (req, rep) => {
        rep.sendFile(path.join(__dirname, "public", "index.html"));
    });
    
    // Send button state to the emulator
    front.get("/setState", (req, rep) => {
        if(!("state" in req.query) || req.query.state === '') {
            rep.send("'state' param is missing or empty");
            return;
        }
    
        let stateParam = req.query.state;
        let state = parseInt(stateParam);
    
        if(!isNaN(state)) {
            gameboy.setInputState(state).then((ret) => {
                if(ret) {
                    gameboy.on("frameExecuted", () => {
                        rep.send("OK");
                    })
                }
            }).catch(() => {
                rep.send("Error while handling input");
            })
        }
    });

    // Get the gameboy screen data
    front.get("/render", (req, rep) => {
        const file = gameboy.getRenderedImage();

        rep.writeHead(200, {
            'Content-Type': 'image/png',
            'Content-Length': file.length
        });

        rep.end(file);
    });
}

/**
 * Setup the websocket for console screen updating
 * @param {*} wss The websocket
 * @param {*} gameboy The gameboy emulator
 */
function setupWebsocket(wss, gameboy) {
    wss.on("connection", async (client) => {
        gameboy.on("frameUpdate", (frameData) => {
            client.send(zlib.deflateSync(frameData));
        });
    });
}

/**
 * Setup the gameboy emulator
 * @param {*} gameboy The gameboy emulator
 */
async function setupEmulator(gameboy) {
    await gameboy.start();
    gameboy.play();
}

async function main() {
    const front  = express();
    const server = http.createServer();
    const gameboy = new emulator.Gameboy("./shellboy.gb");
    const wss = new WebSocket.Server({ 
        server: server
    });

    await setupEmulator(gameboy);
    setupFrontend(front, gameboy);
    setupWebsocket(wss, gameboy);

    server.on("request", front);

    server.listen(APP_PORT, () => {
        console.log("[*] Server started");
    });
}

main();
