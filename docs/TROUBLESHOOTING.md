# ZenSort Troubleshooting Guide

This guide helps you resolve common issues with ZenSort.

## Installation Issues

### Python Not Found
**Error**: `'python' is not recognized as an internal or external command`

**Solutions**:
1. Install Python 3.8+ from [python.org](https://python.org)
2. Add Python to your system PATH
3. Use `python3` instead of `python` on Linux/macOS
4. Restart your terminal/command prompt

### Permission Denied
**Error**: `Permission denied` when installing packages

**Solutions**:
1. Use virtual environment: `python -m venv venv`
2. Run as administrator (Windows) or use `sudo` (Linux/macOS)
3. Use `--user` flag: `pip install --user package_name`

### Missing Dependencies
**Error**: `ModuleNotFoundError: No module named 'PIL'`

**Solutions**:
1. Install requirements: `pip install -r requirements.txt`
2. Activate virtual environment first
3. Install missing package: `pip install Pillow`

## Runtime Errors

### Source Directory Issues

**"Source directory does not exist"**
- Check the path spelling and case sensitivity
- Ensure you have read permissions
- Use absolute paths instead of relative paths

**"Source path is not a directory"**
- Verify you selected a folder, not a file
- Check if the path points to a symbolic link

### Destination Directory Issues

**"Destination cannot be inside source directory"**
- Choose a destination outside the source folder
- Use a different drive: `C:\Photos` → `D:\Organized`
- Use parent directory: `/home/user/photos` → `/home/user/organized`

**"Permission denied writing to destination"**
- Check write permissions on destination folder
- Run as administrator if needed
- Ensure destination drive has enough space

### File Processing Errors

**"Error extracting EXIF"**
- Image file may be corrupted
- Unsupported image format
- Try with different images to isolate the issue

**"Error copying file"**
- Check available disk space
- Verify file isn't in use by another program
- Check file permissions

**"Database connection error"**
- Ensure destination directory is writable
- Close other instances of ZenSort
- Delete `zensort.db` file and restart

## Performance Issues

### Slow Processing
**Symptoms**: Very slow file processing, high CPU usage

**Solutions**:
1. **Disable MusicBrainz**: Set `"enabled": false` in musicbrainz config
2. **Disable image exports**: Set `"enabled": false` in image_export config
3. **Reduce batch size**: Lower the `batch_size` in processing config
4. **Close other applications**: Free up system resources
5. **Use SSD storage**: Process files on solid-state drives

### High Memory Usage
**Symptoms**: System becomes unresponsive, out of memory errors

**Solutions**:
1. **Process smaller directories**: Break large collections into chunks
2. **Restart ZenSort**: Clear memory between sessions
3. **Increase virtual memory**: Adjust system page file size
4. **Close other applications**: Free up RAM

### Network Issues (MusicBrainz)
**Symptoms**: "MusicBrainz search failed", slow audio processing

**Solutions**:
1. **Check internet connection**: Ensure stable connectivity
2. **Increase rate limit**: Set higher value in `rate_limit` config
3. **Disable MusicBrainz**: Process without metadata enhancement
4. **Use wired connection**: More stable than WiFi

## GUI Issues

### Window Not Responding
**Symptoms**: GUI freezes, buttons don't work

**Solutions**:
1. **Wait for processing**: Large operations take time
2. **Check task manager**: Verify ZenSort is still running
3. **Restart application**: Close and reopen ZenSort
4. **Use CLI instead**: Command line interface is more stable

### Settings Not Saving
**Symptoms**: Configuration changes don't persist

**Solutions**:
1. **Check permissions**: Ensure write access to config directory
2. **Close properly**: Don't force-quit the application
3. **Manual config**: Edit `zensort_config.json` directly

### Progress Not Updating
**Symptoms**: Progress bar stuck, no log updates

**Solutions**:
1. **Wait longer**: Large files take time to process
2. **Check logs**: Look for error messages
3. **Restart processing**: Stop and start again

## Configuration Issues

### Invalid JSON Syntax
**Error**: `JSONDecodeError: Expecting ',' delimiter`

**Solutions**:
1. **Validate JSON**: Use online JSON validator
2. **Check commas**: Ensure proper comma placement
3. **Check quotes**: Use double quotes, not single
4. **Reset config**: Delete config file to restore defaults

### Regex Pattern Errors
**Error**: `re.error: bad character range`

**Solutions**:
1. **Escape special characters**: Use `\\` for literal backslashes
2. **Test patterns**: Use online regex testers
3. **Use raw strings**: Prefix with `r"pattern"`

### File Extension Issues
**Symptoms**: Files not being categorized correctly

**Solutions**:
1. **Check case sensitivity**: Extensions should be lowercase
2. **No dots**: Don't include dots in extension lists
3. **Add missing extensions**: Update config with new file types

## Platform-Specific Issues

### Windows

**Antivirus Blocking**
- Add ZenSort to antivirus exclusions
- Temporarily disable real-time protection
- Use Windows Defender exclusions

**Long Path Names**
- Enable long path support in Windows 10/11
- Use shorter destination paths
- Move files closer to drive root

### macOS

**Gatekeeper Blocking**
- Right-click executable and select "Open"
- Go to System Preferences → Security & Privacy
- Allow the application to run

**Permission Issues**
- Grant Full Disk Access in System Preferences
- Use `chmod +x` to make scripts executable

### Linux

**Missing Libraries**
- Install tkinter: `sudo apt-get install python3-tk`
- Install audio libraries: `sudo apt-get install libavcodec-extra`
- Update package lists: `sudo apt-get update`

**Display Issues**
- Set display variable: `export DISPLAY=:0`
- Install X11 forwarding for SSH sessions

## Data Recovery

### Accidental File Movement
**Problem**: Files moved to wrong locations

**Solutions**:
1. **Check duplicates database**: Look in `zensort.db`
2. **Search by filename**: Use system search tools
3. **Check logs**: Review processing logs for file paths
4. **Manual restoration**: Move files back using file manager

### Corrupted Database
**Problem**: Duplicate detection not working

**Solutions**:
1. **Delete database**: Remove `zensort.db` file
2. **Restart ZenSort**: New database will be created
3. **Re-process files**: Run organization again

### Lost Configuration
**Problem**: Settings reset to defaults

**Solutions**:
1. **Check config location**: Look in destination directory
2. **Restore from backup**: Use previous config file
3. **Reconfigure manually**: Set up preferences again

## Getting Help

### Before Reporting Issues
1. **Check this guide**: Review troubleshooting steps
2. **Update ZenSort**: Use the latest version
3. **Test with small dataset**: Isolate the problem
4. **Check logs**: Note specific error messages

### Information to Include
When reporting issues, provide:
- Operating system and version
- Python version (`python --version`)
- ZenSort version
- Complete error messages
- Steps to reproduce the problem
- Sample files that cause issues (if safe to share)

### Where to Get Help
1. **GitHub Issues**: Report bugs and feature requests
2. **Documentation**: Check README and configuration guide
3. **Community Forums**: Ask questions and share solutions

## Prevention Tips

### Regular Maintenance
1. **Update regularly**: Keep ZenSort and dependencies current
2. **Monitor disk space**: Ensure adequate free space
3. **Backup configurations**: Save working config files
4. **Test changes**: Use small test directories first

### Best Practices
1. **Start small**: Test with a few files before processing thousands
2. **Backup important files**: Keep originals safe
3. **Use version control**: Track configuration changes
4. **Document customizations**: Note why you made specific changes

### Performance Optimization
1. **Use fast storage**: SSD drives for better performance
2. **Close unnecessary programs**: Free up system resources
3. **Process during off-hours**: Avoid peak usage times
4. **Monitor system resources**: Watch CPU, memory, and disk usage