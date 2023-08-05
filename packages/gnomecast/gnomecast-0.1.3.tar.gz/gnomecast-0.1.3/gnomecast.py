import codecs, contextlib, mimetypes, os, re, signal, socket, subprocess, tempfile, threading, time

DEPS_MET = True
try:
  import pychromecast
  import bottle
  import pycaption
except Exception as e:
  print(e)
  DEPS_MET = False
  
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib

__version__ = '0.1.3'

if DEPS_MET:
  pycaption.WebVTTWriter._encode = lambda self, s: s


CAST_PNG = os.path.join(os.path.dirname(os.path.abspath(__file__)),'gnomecast','cast.png')

def throttle(seconds=2):
  def decorator(f):
    timer = None
    lastest_args, latest_kwargs = None, None
    def run_f():
      nonlocal timer, lastest_args, latest_kwargs
      ret = f(*lastest_args, **latest_kwargs)
      timer = None
      return ret
    def wrapper(*args, **kwargs):
      nonlocal timer, lastest_args, latest_kwargs
      lastest_args, latest_kwargs = args, kwargs
      if timer == None:
        timer = threading.Timer(seconds, run_f)
        timer.start()
    return wrapper
  return decorator


class Transcoder(object):

  def __init__(self, cast, fn, done_callback):
    self.cast = cast
    self.source_fn = fn
    self.p = None

    try:
      subprocess.check_output(['ffmpeg', '-i', fn], stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
      output = e.output.decode().split('\n')
    container = fn.lower().split(".")[-1]
    video_codec = None
    transcode_audio = True
    for line in output:
      print(line)
      line = line.strip()
      if line.startswith('Stream') and 'Video' in line:
        video_codec = line.split()[3]
      elif line.startswith('Stream') and 'Audio' in line and ('aac (LC)' in line or 'aac (HE)' in line):
        transcode_audio = False

    print('Transcoder', fn, container, video_codec, transcode_audio)
    
    self.transcode_video = video_codec!='h264'
    self.transcode_audio = transcode_audio
    self.transcode = container!='mp4' or self.transcode_video or self.transcode_audio
    self.progress_bytes = 0
    self.progress_seconds = 0
    self.done_callback = done_callback
    print (self.transcode, self.transcode_video, self.transcode_audio)
    if self.transcode:
      self.done = False
      self.trans_fn = tempfile.mkstemp(suffix='.mp4', prefix='movie_caster_')[1]
      os.remove(self.trans_fn)
      #flags = '''-c:v libx264 -profile:v high -level 5 -crf 18 -maxrate 10M -bufsize 16M -pix_fmt yuv420p -x264opts bframes=3:cabac=1 -movflags faststart -c:a libfdk_aac -b:a 320k''' # -vf "scale=iw*sar:ih, scale='if(gt(iw,ih),min(1920,iw),-1)':'if(gt(iw,ih),-1,min(1080,ih))'"
      args = ['ffmpeg', '-threads', '4', '-i', self.source_fn, '-c:v', 'h264' if self.transcode_video else 'copy', '-c:a', 'mp3' if self.transcode_audio else 'copy', self.trans_fn] # '-movflags', 'faststart'
      #args = ['ffmpeg', '-i', self.source_fn, '-c:v', 'libvpx', '-b:v', '5M', '-c:a', 'libvorbis', '-deadline','realtime', self.trans_fn]
      #args = ['ffmpeg', '-i', self.source_fn] + flags.split() + [self.trans_fn]
      print(args)
      self.p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
      t = threading.Thread(target=self.monitor)
      t.daemon = True
      t.start()
    else:
      self.trans_fn = None
      self.done = True
      self.done_callback()
  
  @property
  def fn(self):
    return self.trans_fn if self.transcode else self.source_fn
    
  def wait_for_byte(self, offset, buffer=128*1024*1024):
    if self.done: return
    if self.source_fn.lower().split(".")[-1]=='mp4':
      while offset > self.progress_bytes + buffer:
        print('waiting for', offset, 'at', self.progress_bytes + buffer)
        time.sleep(2)
    else:
      while not self.done:
        print('waiting for transcode to finish')
        time.sleep(2)
    print('done waiting')
  
  def monitor(self):
    line = ''
    r = re.compile(r'=\s+')
    while True:
      char = self.p.stdout.read(1).decode()
      if char == '' and self.p.poll() != None:
        break
      if char != '':
        line += char
        if char == '\r':
          # frame=92578 fps=3937 q=-1.0 size= 1142542kB time=01:04:21.14 bitrate=2424.1kbits/s speed= 164x 
          print(line)
          line = r.sub('=', line)
          items = [s.split('=') for s in line.split()]
          d = dict([x for x in items if len(x)==2])
          self.progress_bytes = int(d.get('size','0kb')[:-2])*1024
          self.progress_seconds = parse_ffmpeg_time(d.get('time','00:00:00'))
          line = ''
    self.p.stdout.close()
    self.done = True
    self.done_callback()
  
  def destroy(self):
    self.cast.media_controller.stop()
    if self.p:
      self.p.terminate()
    if self.trans_fn and os.path.isfile(self.trans_fn):
      os.remove(self.trans_fn)


class Gnomecast(object):

  def __init__(self):
    self.ip = (([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")] or [[(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + [None])[0]
    with contextlib.closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
      s.bind((self.ip, 0))
      self.port = s.getsockname()[1]
    self.app = bottle.Bottle()
    self.cast = None
    self.last_known_player_state = None
    self.last_known_current_time = None
    self.last_time_current_time = None
    self.fn = None
    self.transcoder = None
    self.subtitles = None
    self.duration = None
    self.seeking = False

  def run(self):
    self.build_gui()
    threading.Thread(target=self.init_cast).start()
    t = threading.Thread(target=self.start_server)
    t.daemon = True
    t.start()
    t = threading.Thread(target=self.monitor_cast)
    t.daemon = True
    t.start()
    Gtk.main()
    
  def start_server(self):
    app = self.app

    @app.route('/subtitles.vtt')
    def subtitles():
      #response = bottle.static_file(self.subtitles_fn, root='/', mimetype='text/vtt')
      response = bottle.response
      response.headers['Access-Control-Allow-Origin'] = '*'
      response.headers['Access-Control-Allow-Methods'] = 'GET, HEAD'
      response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
      response.headers['Content-Type'] = 'text/vtt'
      return self.subtitles
    
    @app.get('/video.mp4')
    def video():
      print(list(bottle.request.headers.items()))
      print(self.transcoder.fn)
      ranges = list(bottle.parse_range_header(bottle.request.environ['HTTP_RANGE'], 1000000000000))
      print('ranges', ranges)
      offset, end = ranges[0]
      self.transcoder.wait_for_byte(offset)
      response = bottle.static_file(self.transcoder.fn, root='/')
      response.headers['Access-Control-Allow-Origin'] = '*'
      response.headers['Access-Control-Allow-Methods'] = 'GET, HEAD'
      response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
      return response

    #app.run(host=self.ip, port=self.port, server='paste', daemon=True)
    from paste import httpserver
    from paste.translogger import TransLogger
    handler = TransLogger(app, setup_console_handler=True)
    httpserver.serve(handler, host=self.ip, port=str(self.port), daemon_threads=True)

  def update_status(self):
    fn = os.path.basename(self.fn)
    if len(fn) > 60:
      fn = fn[:50] + '...' + fn[-10:]
    notes = [fn]
    if self.duration:
      notes.append(self.humanize_seconds(self.duration))
    else:
      notes.append('Loading...')
#    if self.last_known_player_state and self.last_known_player_state!='UNKNOWN':
#      notes.append('Cast: %s' % self.last_known_player_state)
    if self.transcoder and not self.transcoder.done:
      notes.append('Converting: %i%%' % (self.transcoder.progress_seconds*100 // self.duration))
    self.file_button.set_label('  -  '.join(notes))
    
  def monitor_cast(self):
    while True:
      time.sleep(1)
      if not self.cast: continue
      seeking = self.seeking
      cast = self.cast
      mc = cast.media_controller
      if mc.status.player_state != self.last_known_player_state:
        if mc.status.player_state=='PLAYING' and self.last_known_player_state=='BUFFERING' and seeking:
          self.seeking = False
        def f():
          self.update_media_button_states()
          self.update_status()
        self.last_known_player_state = mc.status.player_state
        GLib.idle_add(f)
      elif self.transcoder and not self.transcoder.done:
        def f():
          self.update_status()
        GLib.idle_add(f)
      if self.last_known_current_time != mc.status.current_time:
        self.last_known_current_time = mc.status.current_time
        self.last_time_current_time = time.time()
      if not seeking and mc.status.player_state=='PLAYING':
        GLib.idle_add(lambda: self.scrubber_adj.set_value(mc.status.current_time + time.time() - self.last_time_current_time))

  def init_cast(self):
    chromecasts = pychromecast.get_chromecasts()
    def f():
      self.cast_store.clear()
      self.cast_store.append([None, "Select a cast device..."])
      for cc in chromecasts:
        friendly_name = cc.device.friendly_name
        if cc.cast_type!='cast':
          friendly_name = '%s (%s)' % (friendly_name, cc.cast_type)
        self.cast_store.append([cc, friendly_name])
      self.cast_combo.set_active(0)
    GLib.idle_add(f)

  def update_media_button_states(self):
    mc = self.cast.media_controller if self.cast else None
    self.play_button.set_sensitive(bool(self.transcoder and self.cast and mc.status.player_state in ('BUFFERING','PLAYING','PAUSED','IDLE','UNKNOWN') and self.fn))
    self.stop_button.set_sensitive(bool(self.transcoder and self.cast and mc.status.player_state in ('BUFFERING','PLAYING','PAUSED')))
    self.rewind_button.set_sensitive(bool(self.transcoder and self.cast and mc.status.player_state in ('PLAYING','PAUSED')))
    self.forward_button.set_sensitive(bool(self.transcoder and self.cast and mc.status.player_state in ('PLAYING','PAUSED')))
    self.play_button.set_image(Gtk.Image(stock=Gtk.STOCK_MEDIA_PAUSE) if self.cast and mc.status.player_state=='PLAYING' else Gtk.Image(stock=Gtk.STOCK_MEDIA_PLAY))
    if self.transcoder and self.duration:
      self.scrubber_adj.set_upper(self.duration)
      self.scrubber.set_sensitive(True)
    else:
      self.scrubber.set_sensitive(False)


  def build_gui(self):
    self.win = win = Gtk.Window(title='GnomeCast')
    win.set_border_width(0)
    self.cast_store = cast_store = Gtk.ListStore(object, str)
    cast_store.append([None, "Searching local network - please wait..."])

    vbox_outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
    vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16)
    
    self.thumbnail_image = Gtk.Image()
    self.thumbnail_image.set_from_file(CAST_PNG)
    vbox_outer.pack_start(self.thumbnail_image, True, False, 0)
    alignment = Gtk.Alignment(xscale=1, yscale=1)
    alignment.add(vbox)
    alignment.set_padding(16, 20, 16, 16)
    vbox_outer.pack_start(alignment, False, False, 0)

    self.cast_combo = cast_combo = Gtk.ComboBox.new_with_model(cast_store)
    cast_combo.set_entry_text_column(1)
    renderer_text = Gtk.CellRendererText()
    cast_combo.pack_start(renderer_text, True)
    cast_combo.add_attribute(renderer_text, "text", 1)
    cast_combo.set_active(0)

    vbox.pack_start(cast_combo, False, False, 0)
    win.add(vbox_outer)

    self.file_button = button1 = Gtk.Button("Choose a video file...")
    button1.connect("clicked", self.on_file_clicked)
    vbox.pack_start(button1, False, False, 0)

    self.subtitle_store = subtitle_store = Gtk.ListStore(str, int, str)
    subtitle_store.append(["No subtitles.", -1, None])
    subtitle_store.append(["Add subtitle file...", -2, None])
    self.subtitle_combo = Gtk.ComboBox.new_with_model(subtitle_store)
    self.subtitle_combo.connect("changed", self.on_subtitle_combo_changed)
    self.subtitle_combo.set_entry_text_column(0)
    renderer_text = Gtk.CellRendererText()
    self.subtitle_combo.pack_start(renderer_text, True)
    self.subtitle_combo.add_attribute(renderer_text, "text", 0)
    self.subtitle_combo.set_active(0)
    vbox.pack_start(self.subtitle_combo, False, False, 0)
    
    self.scrubber_adj = Gtk.Adjustment(0, 0, 100, 15, 60, 0)
    self.scrubber = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL, adjustment=self.scrubber_adj)
    self.scrubber.set_digits(0)
    def f(scale, s):
      notes = [self.humanize_seconds(s)]
      if self.cast and self.cast.media_controller.status.player_state=='BUFFERING':
        notes.append('...')
      return ''.join(notes)
    self.scrubber.connect("format-value", f)
    self.scrubber.connect("change-value", self.scrubber_move_started)
    self.scrubber.connect("change-value", self.scrubber_moved)
    self.scrubber.set_sensitive(False)
    vbox.pack_start(self.scrubber, False, False, 0)

    hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=16)
    self.rewind_button = Gtk.Button(None, image=Gtk.Image(stock=Gtk.STOCK_MEDIA_REWIND))
    self.rewind_button.connect("clicked", self.rewind_clicked)
    self.rewind_button.set_sensitive(False)
    hbox.pack_start(self.rewind_button, True, False, 0)
    self.play_button = Gtk.Button(None, image=Gtk.Image(stock=Gtk.STOCK_MEDIA_PLAY))
    self.play_button.connect("clicked", self.play_clicked)
    self.play_button.set_sensitive(False)
    hbox.pack_start(self.play_button, True, False, 0)
    self.forward_button = Gtk.Button(None, image=Gtk.Image(stock=Gtk.STOCK_MEDIA_FORWARD))
    self.forward_button.connect("clicked", self.forward_clicked)
    self.forward_button.set_sensitive(False)
    hbox.pack_start(self.forward_button, True, False, 0)
    self.stop_button = Gtk.Button(None, image=Gtk.Image(stock=Gtk.STOCK_MEDIA_STOP))
    self.stop_button.connect("clicked", self.stop_clicked)
    self.stop_button.set_sensitive(False)
    hbox.pack_start(self.stop_button, True, False, 0)
    vbox.pack_start(hbox, False, False, 0)
    
    cast_combo.connect("changed", self.on_cast_combo_changed)

    win.connect("delete-event", self.quit)
    win.connect("key_press_event", self.on_key_press)
    win.show_all()

    GLib.unix_signal_add(GLib.PRIORITY_DEFAULT, signal.SIGINT, self.quit)

  def scrubber_move_started(self, scale, scroll_type, seconds):
    print('scrubber_move_started', seconds)
    self.seeking = True

  @throttle()
  def scrubber_moved(self, scale, scroll_type, seconds):
    print('scrubber_moved', seconds)
    self.seeking = True
    self.cast.media_controller.seek(seconds)

  def humanize_seconds(self, s):
    s = int(s)
    hours = s // (60*60)
    minutes = (s // 60) % 60
    seconds = s % 60
    if hours:
      return '%ih %im %is' % (hours, minutes, seconds)
    if minutes:
      return '%im %is' % (minutes, seconds)
    else:
      return '%is' % (seconds)
    

  def stop_clicked(self, widget):
    if not self.cast: return
    self.cast.media_controller.stop()
  
  def quit(self, a=0, b=0):
    if self.transcoder:
      self.transcoder.destroy()
    if self.cast:
      self.cast.media_controller.stop()
    Gtk.main_quit()

  def forward_clicked(self, widget):
    self.seek_delta(30)
    
  def rewind_clicked(self, widget):
    self.seek_delta(-10)
    
  def seek_delta(self, delta):
    seconds = self.cast.media_controller.status.current_time + time.time() - self.last_time_current_time + delta
    self.last_time_current_time = time.time()
    self.cast.media_controller.status.current_time = seconds
    self.scrubber_adj.set_value(seconds)
    self.seeking = True
    self.cast.media_controller.seek(seconds)
    
  def play_clicked(self, widget):
    if not self.cast:
      print('no cast selected')
      return
    cast = self.cast
    mc = cast.media_controller
    
    if mc.status.player_state=='PLAYING':
      mc.pause()
    elif mc.status.player_state=='PAUSED':
      mc.play()
    elif mc.status.player_state in ('IDLE','UNKNOWN'):
      cast.wait()
      mc = cast.media_controller
      kwargs = {}
      if self.subtitles:
        kwargs['subtitles'] = 'http://%s:%s/subtitles.vtt' % (self.ip, self.port)
      mc.play_media('http://%s:%s/video.mp4' % (self.ip, self.port), 'video/mp4', **kwargs)
#      mc.update_status()
      print(cast.status)
      print(mc.status)
#      mc.enable_subtitle(1)
      #mc.block_until_active()

  def on_file_clicked(self, widget):
      dialog = Gtk.FileChooserDialog("Please choose a video file...", self.win,
          Gtk.FileChooserAction.OPEN,
          (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
           Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

      filter_py = Gtk.FileFilter()
      filter_py.set_name("Videos")
      filter_py.add_mime_type("video/*")
      dialog.add_filter(filter_py)
        
      response = dialog.run()
      if response == Gtk.ResponseType.OK:
          print("Open clicked")
          print("File selected: " + dialog.get_filename())
          self.select_file(dialog.get_filename())
      elif response == Gtk.ResponseType.CANCEL:
          print("Cancel clicked")

      dialog.destroy()
      
  def on_new_subtitle_clicked(self):
      dialog = Gtk.FileChooserDialog("Please choose a subtitle file...", self.win,
          Gtk.FileChooserAction.OPEN,
          (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
           Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

      filter_py = Gtk.FileFilter()
      filter_py.set_name("Subtitles")
      filter_py.add_pattern("*.srt")
      filter_py.add_pattern("*.vtt")
      dialog.add_filter(filter_py)
        
      response = dialog.run()
      if response == Gtk.ResponseType.OK:
          print("Open clicked")
          print("File selected: " + dialog.get_filename())
          self.select_subtitles_file(dialog.get_filename())
      elif response == Gtk.ResponseType.CANCEL:
          print("Cancel clicked")
          self.subtitle_combo.set_active(0)

      dialog.destroy()
      
  def select_subtitles_file(self, fn):
    ext = fn.split('.')[-1]
    display_name = os.path.basename(fn)
    if ext=='vtt':
      with open(fn) as f:
        self.subtitles = f.read()
    else:
      with open(fn) as f:
        caps = f.read()
      if caps.startswith('\ufeff'): # BOM
        caps = caps[1:]
      converter = pycaption.CaptionConverter()
      converter.read(caps, pycaption.detect_format(caps)())
      self.subtitles = converter.write(pycaption.WebVTTWriter())
    pos = len(self.subtitle_store)
    self.subtitle_store.append([display_name, pos-2, self.subtitles])
    self.subtitle_combo.set_active(pos)
    
  def select_file(self, fn):
    self.file_button.set_label(os.path.basename(fn))
    self.thumbnail_image.set_from_file(CAST_PNG)
    self.fn = fn
    threading.Thread(target=self.gen_thumbnail).start()
    threading.Thread(target=self.update_transcoder).start()
  
  def update_transcoder(self):
    if self.transcoder: 
      self.transcoder.destroy()
      self.transcoder = None
    if self.cast and self.fn:
      self.transcoder = Transcoder(self.cast, self.fn, lambda: GLib.idle_add(self.update_status))
    GLib.idle_add(self.update_media_button_states)
        
  def gen_thumbnail(self):
    thumbnail_fn = tempfile.mkstemp(suffix='.jpg', prefix='moviecaster_thumbnail_')[1]
    os.remove(thumbnail_fn)
    subtitle_ids = []
    self.ffmpeg_desc = output = subprocess.check_output(['ffmpeg', '-y', '-i', self.fn, '-f', 'mjpeg', '-vframes', '1', '-ss', '27', '-vf', 'scale=800:-1', thumbnail_fn], stderr=subprocess.STDOUT)
    for line in output.decode().split('\n'):
      line = line.strip()
      if line.startswith('Duration:'):
        self.duration = parse_ffmpeg_time(line.split()[1].strip(','))
      if line.startswith('Stream') and 'Subtitle' in line:
        id = line.split()[1].strip('#').replace(':','.')
        id = id[:id.index('(')]
        subtitle_ids.append(id)
    print('subtitle_ids', subtitle_ids)
    def f():
      self.thumbnail_image.set_from_file(thumbnail_fn)
      os.remove(thumbnail_fn)
      self.update_status()
    GLib.idle_add(f)
    new_subtitles = []
    for subtitle_id in subtitle_ids:
      srt_fn = tempfile.mkstemp(suffix='.srt', prefix='moviecaster_')[1]
      output = subprocess.check_output(['ffmpeg', '-y', '-i', self.fn, '-vn', '-an', '-codec:s:%s' % subtitle_id, 'srt', srt_fn], stderr=subprocess.STDOUT)
      with open(srt_fn) as f:
        caps = f.read()
      print('caps', caps)
      converter = pycaption.CaptionConverter()
      converter.read(caps, pycaption.detect_format(caps)())
      subtitles = converter.write(pycaption.WebVTTWriter())
      new_subtitles.append((subtitle_id, subtitles))
    def f():
      pos = len(self.subtitle_store)
      for id, subs in new_subtitles:
        self.subtitle_store.append([id, pos-2, subs])
        pos += 1
    GLib.idle_add(f)
    os.remove(srt_fn)

  def on_key_press(self, widget, event, user_data=None):
    key = Gdk.keyval_name(event.keyval)
    ctrl = (event.state & Gdk.ModifierType.CONTROL_MASK)
    if key=='q' and ctrl:
      self.quit()
      return True
    return False

  def on_cast_combo_changed(self, combo):
      tree_iter = combo.get_active_iter()
      if tree_iter is not None:
          model = combo.get_model()
          cast, name = model[tree_iter][:2]
          print(cast)
          self.cast = cast
          self.last_known_player_state = None
          self.update_media_button_states()
          threading.Thread(target=self.update_transcoder).start()
      else:
          entry = combo.get_child()
          print('entry', entry)
#          print("Entered: %s" % entry.get_text())

  def on_subtitle_combo_changed(self, combo):
      tree_iter = combo.get_active_iter()
      if tree_iter is not None:
          model = combo.get_model()
          text, position, subs = model[tree_iter]
          print(text, position, subs)
          if position==-1: self.subtitles = None
          elif position==-2: self.on_new_subtitle_clicked()
          else: self.subtitles = subs
      else:
          entry = combo.get_child()
          print('entry', entry)

def parse_ffmpeg_time(time_s):
  hours, minutes, seconds = (float(s) for s in time_s.split(':'))
  return hours*60*60 + minutes*60 + seconds
  

if DEPS_MET and __name__=='__main__':
  caster = Gnomecast()
  caster.run()
  

