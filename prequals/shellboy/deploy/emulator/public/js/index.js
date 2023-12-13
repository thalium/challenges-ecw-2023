const GAMEBOY_CAMERA_WIDTH  = 160;
const GAMEBOY_CAMERA_HEIGHT = 144;

// Translate keyboard input to gameboy joypad state
const KEY_TO_STATE = {
    "ArrowRight":   0x01, // Right
    "ArrowLeft":    0x02, // Left
    "ArrowUp":      0x04, // Up
    "ArrowDown":    0x08, // Down
    "a":            0x10, // A
    "b":            0x20, // B
    "o":            0x40, // Select
    "p":            0x80, // Start
    "r":            0x100 // Reset
};

var inputState = 0;

/**
 * Connect to GB emulator using websocket
 * @param {WebSocket} ws The websocket to use 
 * @returns 
 */
async function connectToServer(ws) {
    return new Promise((resolve, reject) => {
        const timer = setInterval(() => {
            if(ws.readyState === 1) {
                clearInterval(timer)
                resolve();
            }
        }, 10);
    });
}

/**
 * Convert received frame message to an image
 * @param {*} blob The compressed message received
 * @returns The image
 */
async function blobToImageData(blob) {
    // Decompress received data
    let data = new Zlib.Inflate(new Uint8Array(await blob.arrayBuffer())).decompress();

    // Create an array containing the image pixel colors
    // Received data is an array of Uint8 (there is only 1 color component, no RGB)
    var array = new Uint32Array(GAMEBOY_CAMERA_WIDTH*GAMEBOY_CAMERA_HEIGHT);
    for(var i=0; i < array.length; i++) array[i] = ~data[i] << 24;
    
    // Converte Uint32 array to an image data
    var iData = new ImageData(new Uint8ClampedArray(array.buffer), GAMEBOY_CAMERA_WIDTH, GAMEBOY_CAMERA_HEIGHT);
    return iData;
}

const ws = new WebSocket('ws://' + window.location.host + "/ws");

document.addEventListener('DOMContentLoaded', (event) => {
    (async function() {
        const canvas = document.getElementById("screen");
        const ctx = canvas.getContext("2d");
        ctx.webkitImageSmoothingEnabled = false;
        ctx.mozImageSmoothingEnabled = false;
        ctx.imageSmoothingEnabled = false;

        // Register a callback before connection (otherwise we will
        // miss the first frame)
        ws.onmessage = (message) => {
            // Convert message to image and displays it
            blobToImageData(message.data).then((res) => {
                ctx.putImageData(res, 0, 0);
            });
        };

        // Connect to the emulator server
        await connectToServer(ws);

        // Add event listener for joypad input (key released)
        document.addEventListener("keydown", (event) => {
            if(event.key in KEY_TO_STATE && !event.repeat) {
                inputState |= KEY_TO_STATE[event.key];
                fetch("/setState?state=" + inputState).then(response => {}).catch(err => {});
            }
        });

        // Add event listener for joypad input (key pressed)
        document.addEventListener("keyup", (event) => {
            if(event.key in KEY_TO_STATE) {
                inputState &= ~KEY_TO_STATE[event.key];
                fetch("/setState?state=" + inputState).then(response => {}).catch(err => {});
            }
        });
    })();
});

function joypad(key) {
    fetch("/setState?state=" + KEY_TO_STATE[key]).then(response => {
        fetch("/setState?state=0").then(response => {

        }).catch(err => {});
    }).catch(err => {});
}