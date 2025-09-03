import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import json
from pathlib import Path
try:
    from .files_organizer import FilesOrganizer
    from .config_manager import ConfigManager
except ImportError:
    from files_organizer import FilesOrganizer
    from config_manager import ConfigManager


class SettingsWindow:
    def __init__(self, parent, config):
        self.parent = parent
        self.config = config.copy()
        self.window = tk.Toplevel(parent)
        self.window.title("Settings")
        self.window.geometry("600x500")
        self.window.transient(parent)
        self.window.grab_set()
        
        self.create_widgets()
        self.load_config()
    
    def create_widgets(self):
        notebook = ttk.Notebook(self.window)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Image tab
        image_frame = ttk.Frame(notebook)
        notebook.add(image_frame, text="Images")
        
        # Image Export
        ttk.Label(image_frame, text="Export Settings:", font=('TkDefaultFont', 9, 'bold')).grid(row=0, column=0, columnspan=2, sticky='w', pady=(0,5))
        self.export_enabled = tk.BooleanVar()
        ttk.Checkbutton(image_frame, text="Enable image exports", variable=self.export_enabled).grid(row=1, column=0, columnspan=2, sticky='w', pady=2)
        
        ttk.Label(image_frame, text="Max Width:").grid(row=2, column=0, sticky='w', pady=2)
        self.max_width = tk.StringVar()
        ttk.Entry(image_frame, textvariable=self.max_width, width=10).grid(row=2, column=1, sticky='w', padx=(5,0))
        
        ttk.Label(image_frame, text="Max Height:").grid(row=3, column=0, sticky='w', pady=2)
        self.max_height = tk.StringVar()
        ttk.Entry(image_frame, textvariable=self.max_height, width=10).grid(row=3, column=1, sticky='w', padx=(5,0))
        
        ttk.Label(image_frame, text="Quality (1-100):").grid(row=4, column=0, sticky='w', pady=2)
        self.quality = tk.StringVar()
        ttk.Entry(image_frame, textvariable=self.quality, width=10).grid(row=4, column=1, sticky='w', padx=(5,0))
        
        # Screenshot Detection
        ttk.Label(image_frame, text="Screenshot Patterns:", font=('TkDefaultFont', 9, 'bold')).grid(row=5, column=0, columnspan=2, sticky='w', pady=(10,5))
        self.screenshot_patterns = tk.StringVar()
        ttk.Entry(image_frame, textvariable=self.screenshot_patterns, width=40).grid(row=6, column=0, columnspan=2, sticky='w', pady=2)
        
        # Editing Software
        ttk.Label(image_frame, text="Editing Software:").grid(row=7, column=0, sticky='w', pady=(10,2))
        self.editing_software = tk.StringVar()
        ttk.Entry(image_frame, textvariable=self.editing_software, width=40).grid(row=7, column=1, sticky='w', padx=(5,0))
        
        # Social Media Image Rules
        ttk.Label(image_frame, text="Social Media Rules (pattern:ext):").grid(row=8, column=0, sticky='w', pady=(10,2))
        self.social_media_rules = scrolledtext.ScrolledText(image_frame, width=50, height=4)
        self.social_media_rules.grid(row=8, column=1, sticky='w', padx=(5,0))
        
        # Video tab
        video_frame = ttk.Frame(notebook)
        notebook.add(video_frame, text="Videos")
        
        ttk.Label(video_frame, text="Short Video Threshold (seconds):").grid(row=0, column=0, sticky='w', pady=5)
        self.short_threshold = tk.StringVar()
        ttk.Entry(video_frame, textvariable=self.short_threshold, width=10).grid(row=0, column=1, sticky='w', padx=(5,0))
        
        ttk.Label(video_frame, text="Motion Photo Patterns:").grid(row=1, column=0, sticky='w', pady=5)
        self.motion_patterns = tk.StringVar()
        ttk.Entry(video_frame, textvariable=self.motion_patterns, width=40).grid(row=1, column=1, sticky='w', padx=(5,0))
        
        # Audio tab
        audio_frame = ttk.Frame(notebook)
        notebook.add(audio_frame, text="Audio")
        
        # MusicBrainz
        ttk.Label(audio_frame, text="MusicBrainz Settings:", font=('TkDefaultFont', 9, 'bold')).grid(row=0, column=0, columnspan=2, sticky='w', pady=(0,5))
        self.musicbrainz_enabled = tk.BooleanVar()
        ttk.Checkbutton(audio_frame, text="Enable MusicBrainz enhancement", variable=self.musicbrainz_enabled).grid(row=1, column=0, columnspan=2, sticky='w', pady=2)
        
        ttk.Label(audio_frame, text="Rate Limit (seconds):").grid(row=2, column=0, sticky='w', pady=2)
        self.rate_limit = tk.StringVar()
        ttk.Entry(audio_frame, textvariable=self.rate_limit, width=10).grid(row=2, column=1, sticky='w', padx=(5,0))
        
        ttk.Label(audio_frame, text="AcoustID API Key:").grid(row=3, column=0, sticky='w', pady=2)
        self.acoustid_key = tk.StringVar()
        ttk.Entry(audio_frame, textvariable=self.acoustid_key, width=30, show='*').grid(row=3, column=1, sticky='w', padx=(5,0))
        
        # Audio Rules
        ttk.Label(audio_frame, text="Call Recording Rules (pattern:ext):").grid(row=4, column=0, sticky='w', pady=(10,2))
        self.call_rules = scrolledtext.ScrolledText(audio_frame, width=50, height=4)
        self.call_rules.grid(row=4, column=1, sticky='w', padx=(5,0))
        
        ttk.Label(audio_frame, text="Voice Recording Rules (pattern:ext):").grid(row=5, column=0, sticky='w', pady=2)
        self.voice_rules = scrolledtext.ScrolledText(audio_frame, width=50, height=4)
        self.voice_rules.grid(row=5, column=1, sticky='w', padx=(5,0))
        
        ttk.Label(audio_frame, text="Voice Message Rules (pattern:ext):").grid(row=6, column=0, sticky='w', pady=2)
        self.voice_message_rules = scrolledtext.ScrolledText(audio_frame, width=50, height=4)
        self.voice_message_rules.grid(row=6, column=1, sticky='w', padx=(5,0))
        
        # Documents tab
        doc_frame = ttk.Frame(notebook)
        notebook.add(doc_frame, text="Documents")
        
        ttk.Label(doc_frame, text="Word Extensions:").grid(row=0, column=0, sticky='w', pady=2)
        self.word_ext = tk.StringVar()
        ttk.Entry(doc_frame, textvariable=self.word_ext, width=30).grid(row=0, column=1, sticky='w', padx=(5,0))
        
        ttk.Label(doc_frame, text="Excel Extensions:").grid(row=1, column=0, sticky='w', pady=2)
        self.excel_ext = tk.StringVar()
        ttk.Entry(doc_frame, textvariable=self.excel_ext, width=30).grid(row=1, column=1, sticky='w', padx=(5,0))
        
        ttk.Label(doc_frame, text="PDF Extensions:").grid(row=2, column=0, sticky='w', pady=2)
        self.pdf_ext = tk.StringVar()
        ttk.Entry(doc_frame, textvariable=self.pdf_ext, width=30).grid(row=2, column=1, sticky='w', padx=(5,0))
        
        ttk.Label(doc_frame, text="PowerPoint Extensions:").grid(row=3, column=0, sticky='w', pady=2)
        self.powerpoint_ext = tk.StringVar()
        ttk.Entry(doc_frame, textvariable=self.powerpoint_ext, width=30).grid(row=3, column=1, sticky='w', padx=(5,0))
        
        ttk.Label(doc_frame, text="Text Extensions:").grid(row=4, column=0, sticky='w', pady=2)
        self.text_ext = tk.StringVar()
        ttk.Entry(doc_frame, textvariable=self.text_ext, width=30).grid(row=4, column=1, sticky='w', padx=(5,0))
        
        ttk.Label(doc_frame, text="Ebook Extensions:").grid(row=5, column=0, sticky='w', pady=2)
        self.ebook_ext = tk.StringVar()
        ttk.Entry(doc_frame, textvariable=self.ebook_ext, width=30).grid(row=5, column=1, sticky='w', padx=(5,0))
        
        # Skip Patterns tab
        skip_frame = ttk.Frame(notebook)
        notebook.add(skip_frame, text="Skip Patterns")
        
        self.skip_hidden = tk.BooleanVar()
        ttk.Checkbutton(skip_frame, text="Skip hidden files", variable=self.skip_hidden).grid(row=0, column=0, columnspan=2, sticky='w', pady=5)
        
        ttk.Label(skip_frame, text="Max file size (GB):").grid(row=1, column=0, sticky='w', pady=2)
        self.max_file_size = tk.StringVar()
        ttk.Entry(skip_frame, textvariable=self.max_file_size, width=10).grid(row=1, column=1, sticky='w', padx=(5,0))
        
        ttk.Label(skip_frame, text="System Files to Skip:").grid(row=2, column=0, sticky='w', pady=2)
        self.system_files = tk.StringVar()
        ttk.Entry(skip_frame, textvariable=self.system_files, width=40).grid(row=2, column=1, sticky='w', padx=(5,0))
        
        ttk.Label(skip_frame, text="Temp Extensions to Skip:").grid(row=3, column=0, sticky='w', pady=2)
        self.temp_extensions = tk.StringVar()
        ttk.Entry(skip_frame, textvariable=self.temp_extensions, width=40).grid(row=3, column=1, sticky='w', padx=(5,0))
        
        ttk.Label(skip_frame, text="Ignore Directories:").grid(row=4, column=0, sticky='w', pady=2)
        self.ignore_directories = tk.StringVar()
        ttk.Entry(skip_frame, textvariable=self.ignore_directories, width=40).grid(row=4, column=1, sticky='w', padx=(5,0))
        
        # Buttons
        button_frame = ttk.Frame(self.window)
        button_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Button(button_frame, text="Save", command=self.save_config).pack(side='right', padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.window.destroy).pack(side='right')
    
    def load_config(self):
        # Image settings
        image_config = self.config.get('image_export', {})
        self.export_enabled.set(image_config.get('enabled', True))
        self.max_width.set(str(image_config.get('max_width', 3840)))
        self.max_height.set(str(image_config.get('max_height', 2160)))
        self.quality.set(str(image_config.get('quality', 85)))
        
        # Screenshot patterns
        patterns = self.config.get('screenshot_patterns', [])
        self.screenshot_patterns.set(', '.join(patterns))
        
        # Editing software
        editing_sw = self.config.get('editing_software', [])
        self.editing_software.set(', '.join(editing_sw))
        
        # Video settings
        video_config = self.config.get('video_thresholds', {})
        self.short_threshold.set(str(video_config.get('short_video_threshold', 60)))
        
        motion_patterns = self.config.get('motion_photo_patterns', [])
        self.motion_patterns.set(', '.join(motion_patterns))
        
        # Audio settings
        mb_config = self.config.get('musicbrainz', {})
        self.musicbrainz_enabled.set(mb_config.get('enabled', True))
        self.rate_limit.set(str(mb_config.get('rate_limit', 1.0)))
        self.acoustid_key.set(mb_config.get('acoustid_api_key', ''))
        
        # Call and voice recording rules
        call_rules = self.config.get('call_recording_rules', [])
        call_text = '\n'.join([f"{rule['pattern']}:{rule['extension']}" for rule in call_rules])
        self.call_rules.delete(1.0, tk.END)
        self.call_rules.insert(1.0, call_text)
        
        voice_rules = self.config.get('voice_recording_rules', [])
        voice_text = '\n'.join([f"{rule['pattern']}:{rule['extension']}" for rule in voice_rules])
        self.voice_rules.delete(1.0, tk.END)
        self.voice_rules.insert(1.0, voice_text)
        
        # Voice message rules
        voice_msg_rules = self.config.get('voice_message_rules', [])
        voice_msg_text = '\n'.join([f"{rule['pattern']}:{rule['extension']}" for rule in voice_msg_rules])
        self.voice_message_rules.delete(1.0, tk.END)
        self.voice_message_rules.insert(1.0, voice_msg_text)
        
        # Social media image rules
        social_rules = self.config.get('social_media_image_rules', [])
        social_text = '\n'.join([f"{rule['pattern']}:{rule['extension']}" for rule in social_rules])
        self.social_media_rules.delete(1.0, tk.END)
        self.social_media_rules.insert(1.0, social_text)
        
        # Document settings
        doc_config = self.config.get('document_categories', {})
        self.word_ext.set(', '.join(doc_config.get('word', [])))
        self.excel_ext.set(', '.join(doc_config.get('excel', [])))
        self.pdf_ext.set(', '.join(doc_config.get('pdf', [])))
        self.powerpoint_ext.set(', '.join(doc_config.get('powerpoint', [])))
        self.text_ext.set(', '.join(doc_config.get('text', [])))
        self.ebook_ext.set(', '.join(doc_config.get('ebook', [])))
        
        # Skip patterns
        skip_config = self.config.get('skip_patterns', {})
        self.skip_hidden.set(skip_config.get('hidden_files', True))
        self.max_file_size.set(str(skip_config.get('max_file_size_gb', 50)))
        self.system_files.set(', '.join(skip_config.get('system_files', [])))
        self.temp_extensions.set(', '.join(skip_config.get('temp_extensions', [])))
        self.ignore_directories.set(', '.join(skip_config.get('ignore_directories', [])))
    
    def save_config(self):
        try:
            # Image settings
            self.config.setdefault('image_export', {})['enabled'] = self.export_enabled.get()
            self.config['image_export']['max_width'] = int(self.max_width.get())
            self.config['image_export']['max_height'] = int(self.max_height.get())
            self.config['image_export']['quality'] = int(self.quality.get())
            
            # Screenshot patterns
            patterns = [p.strip() for p in self.screenshot_patterns.get().split(',') if p.strip()]
            self.config['screenshot_patterns'] = patterns
            
            # Editing software
            editing_sw = [s.strip() for s in self.editing_software.get().split(',') if s.strip()]
            self.config['editing_software'] = editing_sw
            
            # Video settings
            self.config.setdefault('video_thresholds', {})['short_video_threshold'] = int(self.short_threshold.get())
            motion_patterns = [p.strip() for p in self.motion_patterns.get().split(',') if p.strip()]
            self.config['motion_photo_patterns'] = motion_patterns
            
            # Audio settings
            self.config.setdefault('musicbrainz', {})['enabled'] = self.musicbrainz_enabled.get()
            self.config['musicbrainz']['rate_limit'] = float(self.rate_limit.get())
            self.config['musicbrainz']['acoustid_api_key'] = self.acoustid_key.get()
            
            # Call and voice recording rules
            call_text = self.call_rules.get(1.0, tk.END).strip()
            call_rules = []
            for line in call_text.split('\n'):
                if ':' in line:
                    pattern, ext = line.split(':', 1)
                    call_rules.append({'pattern': pattern.strip(), 'extension': ext.strip()})
            self.config['call_recording_rules'] = call_rules
            
            voice_text = self.voice_rules.get(1.0, tk.END).strip()
            voice_rules = []
            for line in voice_text.split('\n'):
                if ':' in line:
                    pattern, ext = line.split(':', 1)
                    voice_rules.append({'pattern': pattern.strip(), 'extension': ext.strip()})
            self.config['voice_recording_rules'] = voice_rules
            
            # Voice message rules
            voice_msg_text = self.voice_message_rules.get(1.0, tk.END).strip()
            voice_msg_rules = []
            for line in voice_msg_text.split('\n'):
                if ':' in line:
                    pattern, ext = line.split(':', 1)
                    voice_msg_rules.append({'pattern': pattern.strip(), 'extension': ext.strip()})
            self.config['voice_message_rules'] = voice_msg_rules
            
            # Social media image rules
            social_text = self.social_media_rules.get(1.0, tk.END).strip()
            social_rules = []
            for line in social_text.split('\n'):
                if ':' in line:
                    pattern, ext = line.split(':', 1)
                    social_rules.append({'pattern': pattern.strip(), 'extension': ext.strip()})
            self.config['social_media_image_rules'] = social_rules
            
            # Document settings
            self.config.setdefault('document_categories', {})
            self.config['document_categories']['word'] = [e.strip() for e in self.word_ext.get().split(',') if e.strip()]
            self.config['document_categories']['excel'] = [e.strip() for e in self.excel_ext.get().split(',') if e.strip()]
            self.config['document_categories']['pdf'] = [e.strip() for e in self.pdf_ext.get().split(',') if e.strip()]
            self.config['document_categories']['powerpoint'] = [e.strip() for e in self.powerpoint_ext.get().split(',') if e.strip()]
            self.config['document_categories']['text'] = [e.strip() for e in self.text_ext.get().split(',') if e.strip()]
            self.config['document_categories']['ebook'] = [e.strip() for e in self.ebook_ext.get().split(',') if e.strip()]
            
            # Skip patterns
            self.config.setdefault('skip_patterns', {})['hidden_files'] = self.skip_hidden.get()
            self.config['skip_patterns']['max_file_size_gb'] = int(self.max_file_size.get())
            self.config['skip_patterns']['system_files'] = [f.strip() for f in self.system_files.get().split(',') if f.strip()]
            self.config['skip_patterns']['temp_extensions'] = [e.strip() for e in self.temp_extensions.get().split(',') if e.strip()]
            self.config['skip_patterns']['ignore_directories'] = [d.strip() for d in self.ignore_directories.get().split(',') if d.strip()]
            
            self.parent.config = self.config
            self.window.destroy()
            messagebox.showinfo("Settings", "Settings saved successfully!")
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid value: {e}")


class ZenSortGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("ZenSort - File Organizer")
        self.root.geometry("700x500")
        
        self.organizer = None
        self.organizing = False
        self.paused = False
        self.config = {}
        self.settings_file = Path.home() / '.zensort_gui_settings.json'
        self.log_lines = []
        self.max_log_lines = 100
        self.current_folder = ""
        self.last_source = ''
        self.last_dest = ''
        
        self.create_widgets()
        self.load_settings()
    
    def create_widgets(self):
        # Directory selection frame
        dir_frame = ttk.LabelFrame(self.root, text="Directories", padding=10)
        dir_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(dir_frame, text="Source:").grid(row=0, column=0, sticky='w', pady=5)
        self.source_var = tk.StringVar()
        ttk.Entry(dir_frame, textvariable=self.source_var, width=50).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(dir_frame, text="Browse", command=self.browse_source).grid(row=0, column=2, pady=5)
        
        ttk.Label(dir_frame, text="Destination:").grid(row=1, column=0, sticky='w', pady=5)
        self.dest_var = tk.StringVar()
        ttk.Entry(dir_frame, textvariable=self.dest_var, width=50).grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(dir_frame, text="Browse", command=self.browse_dest).grid(row=1, column=2, pady=5)
        
        # Control buttons frame
        control_frame = ttk.Frame(self.root)
        control_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(control_frame, text="Settings", command=self.open_settings).pack(side='left', padx=5)
        self.start_btn = ttk.Button(control_frame, text="Start", command=self.start_organization)
        self.start_btn.pack(side='left', padx=5)
        self.pause_btn = ttk.Button(control_frame, text="Pause", command=self.pause_organization, state='disabled')
        self.pause_btn.pack(side='left', padx=5)
        self.stop_btn = ttk.Button(control_frame, text="Stop", command=self.stop_organization, state='disabled')
        self.stop_btn.pack(side='left', padx=5)
        self.exit_btn = ttk.Button(control_frame, text="Exit", command=self.exit_application)
        self.exit_btn.pack(side='left', padx=5)
        
        # Status indicator
        self.status_var = tk.StringVar(value="Ready")
        self.status_label = ttk.Label(control_frame, textvariable=self.status_var, foreground='green')
        self.status_label.pack(side='right', padx=10)
        
        # Progress frame
        progress_frame = ttk.LabelFrame(self.root, text="Progress", padding=10)
        progress_frame.pack(fill='x', padx=10, pady=5)
        
        self.progress_var = tk.StringVar(value="Ready")
        ttk.Label(progress_frame, textvariable=self.progress_var).pack(anchor='w')
        
        self.progress_bar = ttk.Progressbar(progress_frame, mode='determinate')
        self.progress_bar.pack(fill='x', pady=5)
        
        # Log area
        log_frame = ttk.LabelFrame(self.root, text="Log", padding=10)
        log_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=15, font=('Consolas', 9))
        self.log_text.pack(fill='both', expand=True)
        self.log_text.tag_config('folder', foreground='blue', font=('Consolas', 9, 'bold'))
        self.log_text.tag_config('file', foreground='black')
        self.log_text.tag_config('success', foreground='green')
        self.log_text.tag_config('error', foreground='red')
        self.log_text.tag_config('warning', foreground='orange')
        self.log_text.tag_config('info', foreground='gray')
    
    def browse_source(self):
        # Use last source as initial directory if it exists
        initial_dir = self.last_source if self.last_source and Path(self.last_source).exists() else None
        directory = filedialog.askdirectory(title="Select Source Directory", initialdir=initial_dir)
        if directory:
            self.source_var.set(directory)
            self.last_source = directory
    
    def browse_dest(self):
        # Use last destination as initial directory if it exists
        initial_dir = self.last_dest if self.last_dest and Path(self.last_dest).exists() else None
        directory = filedialog.askdirectory(title="Select Destination Directory", initialdir=initial_dir)
        if directory:
            self.dest_var.set(directory)
            self.last_dest = directory
    
    def open_settings(self):
        if self.organizing:
            messagebox.showwarning("Warning", "Cannot change settings while organizing")
            return
        
        dest = self.dest_var.get().strip()
        if not dest:
            messagebox.showwarning("Warning", "Please select a destination directory first")
            return
        
        # Initialize config if destination doesn't have config file
        dest_path = Path(dest)
        config_file = dest_path / 'zensort_config.json'
        
        if not config_file.exists():
            try:
                from .config_manager import ConfigManager
            except ImportError:
                from config_manager import ConfigManager
            
            config_manager = ConfigManager(dest_path)
            self.config = config_manager.load_config()  # This will return defaults
            config_manager.save_config(self.config)  # Save defaults to file
        
        SettingsWindow(self.root, self.config)
    
    def start_organization(self):
        source = self.source_var.get().strip()
        dest = self.dest_var.get().strip()
        
        if not source or not dest:
            messagebox.showerror("Error", "Please select both source and destination directories")
            return
        
        source_path = Path(source)
        dest_path = Path(dest)
        
        if not source_path.exists():
            messagebox.showerror("Error", "Source directory does not exist")
            return
        
        if not source_path.is_dir():
            messagebox.showerror("Error", "Source path is not a directory")
            return
        
        # Check if destination is inside source
        try:
            dest_path.resolve().relative_to(source_path.resolve())
            messagebox.showerror("Error", "Destination cannot be inside source directory")
            return
        except ValueError:
            pass
        
        self.organizing = True
        self.paused = False
        self.update_button_states()
        self.set_status("Starting...", 'orange')
        self.clear_log()
        self.log("Starting organization...", 'info')
        
        # Save current directories
        self.save_settings()
        
        # Start organization in separate thread
        thread = threading.Thread(target=self.run_organization)
        thread.daemon = True
        thread.start()
    
    def pause_organization(self):
        if self.organizer and self.organizing:
            if self.paused:
                self.organizer.resume()
                self.paused = False
                self.pause_btn.config(text="Pause")
                self.set_status("Running...", 'green')
                self.log("Resumed organization", 'info')
            else:
                self.organizer.pause()
                self.paused = True
                self.pause_btn.config(text="Resume")
                self.set_status("Paused", 'orange')
                self.log("Paused organization", 'warning')
    
    def stop_organization(self):
        if self.organizer:
            self.organizer.stop()
            self.set_status("Stopping...", 'red')
            self.log("Stopping organization...", 'warning')
    
    def run_organization(self):
        try:
            source = self.source_var.get()
            dest = self.dest_var.get()
            
            self.organizer = FilesOrganizer(
                source_dir=source,
                dest_dir=dest
            )
            
            # Apply config if available
            if self.config:
                self.organizer.config.update(self.config)
            
            self.root.after(0, lambda: self.set_status("Running...", 'green'))
            success = self.organizer.organize(progress_callback=self.progress_callback)
            
            # Final statistics
            stats = self.organizer.get_stats()
            status_text = 'completed' if success else 'stopped'
            status_color = 'green' if success else 'orange'
            
            self.root.after(0, lambda: self.set_status(f"Organization {status_text}", status_color))
            self.root.after(0, lambda: self.log(f"\n=== Organization {status_text} ===", 'success' if success else 'warning'))
            self.root.after(0, lambda: self.log(
                f"=== FINAL RESULTS ===", 'success' if success else 'warning'
            ))
            self.root.after(0, lambda: self.log(
                f"Total: {stats['total']} | Processed: {stats['processed']} | "
                f"Skipped: {stats['skipped']} | Duplicates: {stats['duplicates']} | "
                f"Errors: {stats['errors']}", 'info'
            ))
            self.root.after(0, lambda: self.log(
                f"Log file saved in: {self.dest_var.get()}/logs/", 'info'
            ))
            
        except Exception as e:
            self.root.after(0, lambda: self.set_status("Error occurred", 'red'))
            self.root.after(0, lambda: self.log(f"Error: {e}", 'error'))
        finally:
            self.organizing = False
            self.paused = False
            self.root.after(0, self.update_button_states)
    
    def progress_callback(self, current, total, stats, file_action=None):
        if total > 0:
            percentage = (current / total) * 100
            self.root.after(0, lambda: self.progress_bar.config(value=percentage))
            self.root.after(0, lambda: self.progress_var.set(
                f"Progress: {current}/{total} ({percentage:.1f}%) | "
                f"Processed: {stats['processed']} | Skipped: {stats['skipped']} | "
                f"Duplicates: {stats['duplicates']} | Errors: {stats['errors']}"
            ))
            
            # Show file action if provided
            if file_action:
                action = file_action.split(' ', 1)[0]
                tag = 'success' if action == 'PROCESSED' else 'warning' if action in ['SKIPPED', 'DUPLICATE'] else 'error'
                self.root.after(0, lambda: self.log(file_action, tag))
    
    def log(self, message, tag='file'):
        def _log():
            # Maintain log history
            self.log_lines.append((message, tag))
            if len(self.log_lines) > self.max_log_lines:
                self.log_lines.pop(0)
                # Clear and rebuild log display
                self.log_text.delete(1.0, tk.END)
                for msg, msg_tag in self.log_lines:
                    self.log_text.insert(tk.END, msg + "\n", msg_tag)
            else:
                self.log_text.insert(tk.END, message + "\n", tag)
            
            self.log_text.see(tk.END)
        
        self.root.after(0, _log)
    
    def clear_log(self):
        self.log_lines.clear()
        self.log_text.delete(1.0, tk.END)
        self.progress_bar.config(value=0)
        self.progress_var.set("Ready")
    
    def set_status(self, status, color='black'):
        self.status_var.set(status)
        self.status_label.config(foreground=color)
    
    def update_button_states(self):
        if self.organizing:
            self.start_btn.config(state='disabled')
            self.pause_btn.config(state='normal')
            self.stop_btn.config(state='normal')
            self.exit_btn.config(state='disabled')
        else:
            self.start_btn.config(state='normal')
            self.pause_btn.config(state='disabled', text='Pause')
            self.stop_btn.config(state='disabled')
            self.exit_btn.config(state='normal')
    
    def exit_application(self):
        if self.organizing:
            if messagebox.askyesno("Exit", "Organization is in progress. Do you want to stop and exit?"):
                if self.organizer:
                    self.organizer.stop()
                self.root.quit()
        else:
            self.root.quit()
    
    def load_settings(self):
        try:
            if self.settings_file.exists():
                with open(self.settings_file, 'r') as f:
                    settings = json.load(f)
                    # Store last paths but don't auto-populate
                    self.last_source = settings.get('last_source', '')
                    self.last_dest = settings.get('last_destination', '')
                    self.config = settings.get('config', {})
            else:
                self.last_source = ''
                self.last_dest = ''
        except Exception:
            self.last_source = ''
            self.last_dest = ''
    
    def save_settings(self):
        try:
            # Load existing settings to preserve other values
            existing_settings = {}
            if self.settings_file.exists():
                with open(self.settings_file, 'r') as f:
                    existing_settings = json.load(f)
            
            # Update only source and destination
            existing_settings['last_source'] = self.last_source
            existing_settings['last_destination'] = self.last_dest
            existing_settings['config'] = self.config
            
            with open(self.settings_file, 'w') as f:
                json.dump(existing_settings, f)
        except Exception:
            pass
    
    def run(self):
        self.root.mainloop()


def main():
    app = ZenSortGUI()
    app.run()


if __name__ == '__main__':
    main()