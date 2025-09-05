# FFmpeg Binaries

Place platform-specific FFmpeg binaries in this directory:

## Windows
- `ffmpeg-win64.exe` - For x64/amd64 systems
- `ffmpeg-win-arm64.exe` - For ARM64 systems

## Linux
- `ffmpeg-linux-x64` - For x86_64 systems  
- `ffmpeg-linux-arm64` - For aarch64 systems

## macOS
- `ffmpeg-macos-x64` - For Intel Macs
- `ffmpeg-macos-arm64` - For Apple Silicon Macs

## Download Sources
- **Windows**: https://www.gyan.dev/ffmpeg/builds/ (static builds)
- **Linux**: https://johnvansickle.com/ffmpeg/ (static builds)
- **macOS**: https://evermeet.cx/ffmpeg/ (static builds)

## Notes
- Use static builds (no dependencies)
- Ensure executable permissions on Linux/macOS
- Build script automatically detects architecture and bundles appropriate binary