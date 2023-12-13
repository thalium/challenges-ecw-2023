const fs           = require("fs");
const EventEmitter = require("events");
const canvas       = require("canvas");

const GAMEBOY_SCREEN_WIDTH  = 160;
const GAMEBOY_SCREEN_HEIGHT = 144;
const FRAME_BUFFER_SIZE     = GAMEBOY_SCREEN_HEIGHT * GAMEBOY_SCREEN_WIDTH;

const WASMBOY_IMPORTS = {
    index: {
        consoleLog: console.log,
        consoleLogTimeout: console.log
    },
    env: {
        abort: () => {
            console.error('AssemblyScript Import Object Aborted!');
        }
    }
};

class Gameboy {
    /**
     * Construct a gameboy instance
     * @param {string} ROMPath The ".gb" file path
     */
    constructor(ROMPath) {
        this.ROMPath = ROMPath;

        this.wasmInstance    = null;
        this.wasmboyMemory   = null;

        this.lastFrameData = new Uint8Array(FRAME_BUFFER_SIZE);
        this.frameData     = new Uint8Array(FRAME_BUFFER_SIZE);

        this.interval = null;

        this.isStarted   = false;
        this.isPlaying   = false;
        this.isResetting = false;

        this.consoleEvents = new EventEmitter();
    }

    on(what, cb) {
        // Special case for late frameUpdate events listeners
        if(what === "frameUpdate" && this.isStarted && this.isPlaying && this.lastFrameData !== null) {
            cb(this.lastFrameData);
        }

        return this.consoleEvents.on(what, cb);
    }
    
    /**
     * Starts the console core and load the ROM
     * To play a game. You need to call 'loadROM' an then 'play'
     */
    async start() {
        // Check if the console isn't already started
        if(this.isStarted) {
            console.log("[o] Trying to start the console while it is already started. Ignoring...");
            return;
        }
        
        // Instantiate WASM core
        let instantiatedWasm = await WebAssembly.instantiate(fs.readFileSync("./core-0-5-0.wasm"), WASMBOY_IMPORTS);
        this.wasmInstance  = instantiatedWasm.instance;
        this.wasmboyMemory = new Uint8Array(instantiatedWasm.instance.exports.memory.buffer);

        // Load ROM
        const rom = new Uint8Array(fs.readFileSync(this.ROMPath));
        for(let i = 0; i < rom.length; i++) {
            this.wasmboyMemory[this.wasmInstance.exports.CARTRIDGE_ROM_LOCATION.value + i] = rom[i];
        }

        this.isStarted = true;
        
        console.log("[*] Console started");
    }
    
    /**
     * Stops the console
     */
    stop() {
        this.pause();

        this.wasmInstance  = null;
        this.wasmboyMemory = null;

        this.isStarted = false;
        console.log("[*] Console stopped");
    }

    /**
     * Pause the console rendering
     */
    pause() {
        // Check if the console is currently started
        if(!this.isStarted) {
            console.log("[o] Attempting to pause while the console is not started. Ignoring...");
            return;
        }

        // Check if the console is currently playing
        if(!this.isPlaying) {
            console.log("[o] Attempting to pause the console while it is not playing. Ignoring...");
            return;
        }

        // Stops the rendering loop
        clearInterval(this.interval);
        this.interval  = null;
        
        console.log("[*] Console paused");
        this.isPlaying = false;
        this.consoleEvents.emit("pause");
    }

    /**
     * Start the emulation
     */
    play() {
        // Check if the console is currently started
        if(!this.isStarted) {
            console.log("[o] Attempting to play while the console is not started. Ignoring...");
            return;
        }

        // Check if the console is currently playing
        if(this.isPlaying) {
            console.log("[o] Attempting to play while it is already playing. Ignoring...");
            return;
        }

        // Configure the console
        this.wasmInstance.exports.config(
            0, // enableBootRom
            1, // useGbcWhenAvailable
            0, // audioBatchProcessing
            0, // graphicsBatchProcessing
            0, // timersBatchProcessing
            0, // graphicsDisableScanlineRendering
            0, // audioAccumulateSamples
            1, // tileRendering
            1, // tileCaching
            0  // enableAudioDebugging
        );

        console.log("[*] Console playing");
        this.isPlaying = true;
        this.consoleEvents.emit("play");

        this.interval = setInterval(() => {
            // Execute frame and check for errors
            if(this.wasmInstance.exports.executeFrame() == 0) {

                // Copy the frame data
                for(let i = 0; i < FRAME_BUFFER_SIZE; i++) {
                    this.frameData[i] = this.wasmboyMemory[this.wasmInstance.exports.FRAME_LOCATION.value + i * 3];
                }

                // Compare the frame buffer with the previous buffer sent to the client
                // and only send new frames to the client.
                if(Buffer.compare(this.lastFrameData, this.frameData) != 0) {
                    
                    // Copy the frame data in the last (send) frame data
                    for(let i = 0; i < FRAME_BUFFER_SIZE; i++) {
                        this.lastFrameData[i] = this.frameData[i];
                    }

                    // Notify all frame update callbacks
                    this.consoleEvents.emit("frameUpdate", this.lastFrameData);
                }

                // Trigger only one time frameExecuted listeners
                this.consoleEvents.emit("frameExecuted");
                this.consoleEvents.removeAllListeners("frameExecuted");
            }
        }, 16); // 16 ms = 60 fps
    }

    /**
     * Get the console current image
     */
    getRenderedImage() {
        // Create a canvas the size of the gameboy screen
        let c   = canvas.createCanvas(GAMEBOY_SCREEN_WIDTH, GAMEBOY_SCREEN_HEIGHT);
        let ctx = c.getContext("2d", { pixelFormat: 'A8' });

        // Get pixels values (pixels are RGB) but why only wants 1 component for a grayscale image
        let frameData = new Uint8ClampedArray(FRAME_BUFFER_SIZE);
        for(let i = 0; i < FRAME_BUFFER_SIZE; i++) {
            frameData[i] = this.wasmboyMemory[this.wasmInstance.exports.FRAME_LOCATION.value + i * 3];
        }

        // Create the image data and add it to the canvas
        let iData = canvas.createImageData(frameData, GAMEBOY_SCREEN_WIDTH, GAMEBOY_SCREEN_HEIGHT);
        ctx.putImageData(iData, 0, 0);

        // Dump the canvas to a PNG image
        return Buffer.from(c.toDataURL("image/png").split(",")[1], "base64");
    }

    /**
     * Set the input state
     * @param {number} state The client input state
     */
    async setInputState(state) {
        // Check if the console is running
        if(!this.isStarted || !this.isPlaying) {
            console.log("[*] Ignoring input. Console is not started nor playing...");
            return false;
        }

        let self = this;

        if((state & 0x100) != 0 && !this.isResetting) {
            // Handle reset state
            this.isResetting = true;
            this.stop();
            await this.start();
            this.play();

            setTimeout(() => {
                self.isResetting = false;
            }, 1000);
        } else {
            // Handle normal states
            this.wasmInstance.exports.setJoypadState(
                ((state & 0x04) != 0) ? 1 : 0, // UP
                ((state & 0x01) != 0) ? 1 : 0, // RIGHT
                ((state & 0x08) != 0) ? 1 : 0, // DOWN
                ((state & 0x02) != 0) ? 1 : 0, // LEFT
                ((state & 0x10) != 0) ? 1 : 0, // A
                ((state & 0x20) != 0) ? 1 : 0, // B
                ((state & 0x40) != 0) ? 1 : 0, // SELECT
                ((state & 0x80) != 0) ? 1 : 0  // START
            );
        }

        return true
    }
}

module.exports = {
    Gameboy: Gameboy
};
