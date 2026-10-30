# Flem Dogs Aquarium

A customized edition of [Aquarium by akaloic](https://github.com/akaloic/aquarium), based on commit `440f55f2dd6a0bf798f316e4fd79b5a90b552e54`. Original MIT / Apache-2.0 licenses and author credits are preserved. See README-UPSTREAM.md for the original documentation.

## Windows download

Open [Windows preview downloads](https://github.com/jcoghlan14/flem-dogs-aquarium/releases). Once a build finishes successfully, download **Flem-Dogs-Aquarium-Windows.zip** from the release’s Assets section. Extract it completely, then open **Start Aquarium.cmd**. Keep the assets folder beside the EXE. No Rust installation is needed. If no preview is listed yet, the first build is still pending.

Windows x64 is the initial target. A graphics driver supporting the Bevy/wgpu renderer is required; actual rendering and interaction still need testing on a Windows PC. This is an unsigned community build. Do not disable Windows security protections to run it; report any warning first.

- Move the pointer near fish to scatter them.
- Left click inside the tank to drop food.
- Scroll to zoom; right drag to rotate; Esc to quit.
- **Start Full Screen.cmd** opens the aquarium on the main display.
- **Start Low Power.cmd** uses a lower rendering setting.

This Windows package is an interactive application, not a Windows desktop wallpaper or screensaver. The Mac-only --wallpaper option is rejected on other systems rather than silently creating a noninteractive window.

## Build yourself on Windows

Install Rust stable and Microsoft C++ build tools. In Git Bash, run `bash scripts/fetch_assets.sh`, then `cargo build --release --locked`. Run `target/release/aquarium.exe --windowed`. Internet is needed for build dependencies and the initial CC0 asset download; the packaged app runs offline.

## GitHub build

Upload this source tree to your own repository. Open Actions → Windows package → Run workflow. The workflow includes required assets, licenses and launchers in the ZIP. It never includes this Mac's logs, caches or personal paths. A completed build establishes compilation, not hardware compatibility; test the ZIP on Windows before calling it a verified release.
