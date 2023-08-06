from auditok import ADSFactory, AudioEnergyValidator, StreamTokenizer, player_for, dataset
from auditok.io import PyAudioSource, BufferAudioSource, StdinAudioSource, player_for
import operator
import os
from collections import OrderedDict
from pydub import AudioSegment
import sys
from threading import Thread
import threading
import time
from queue import Queue, Empty
import vaisdemo.vais as vais
import logging
import site

for path in site.getsitepackages():
    python_root = os.path.dirname(sys.executable)
    # print("Setting path")
    os.environ["PATH"] += os.pathsep + python_root
    os.environ["PATH"] += os.pathsep + os.path.join(python_root, "Scripts")
    os.system("ffmpeg")

def file_to_audio_source(filename, filetype=None, **kwargs):

    lower_fname = filename.lower()
    rawdata = False

    if filetype is not None:
        filetype = filetype.lower()

    if filetype == "raw" or (filetype is None and lower_fname.endswith(".raw")):

        srate = kwargs.pop("sampling_rate", None)
        if srate is None:
            srate = kwargs.pop("sr", None)

        swidth = kwargs.pop("sample_width", None)
        if swidth is None:
            swidth = kwargs.pop("sw", None)

        ch = kwargs.pop("channels", None)
        if ch is None:
            ch = kwargs.pop("ch", None)

        if None in (swidth, srate, ch):
            raise Exception("All audio parameters are required for raw data")

        data = open(filename).read()
        rawdata = True

    use_channel = kwargs.pop("use_channel", None)
    if use_channel is None:
        use_channel = kwargs.pop("uc", None)

    if use_channel is None:
        use_channel = 1
    else:
        try:
            use_channel = int(use_channel)
        except ValueError:
            pass

    if not isinstance(use_channel, (int)) and not use_channel.lower() in ["left", "right", "mix"] :
        raise ValueError("channel must be an integer or one of 'left', 'right' or 'mix'")

    asegment = None

    if rawdata:
        asegment = AudioSegment(data, sample_width=swidth, frame_rate=srate, channels=ch)
    if filetype in("wave", "wav") or (filetype is None and lower_fname.endswith(".wav")):
        asegment = AudioSegment.from_wav(filename)
    elif filetype == "mp3" or (filetype is None and lower_fname.endswith(".mp3")):
        asegment = AudioSegment.from_mp3(filename)
    elif filetype == "ogg" or (filetype is None and lower_fname.endswith(".ogg")):
        asegment = AudioSegment.from_ogg(filename)
    elif filetype == "flv" or (filetype is None and lower_fname.endswith(".flv")):
        asegment = AudioSegment.from_flv(filename)
    else:
        asegment = AudioSegment.from_file(filename)

    if asegment.channels > 1:

        if isinstance(use_channel, int):
            if use_channel > asegment.channels:
                raise ValueError("Can not use channel '{0}', audio file has only {1} channels".format(use_channel, asegment.channels))
            else:
                asegment = asegment.split_to_mono()[use_channel - 1]
        else:
            ch_lower = use_channel.lower()

            if ch_lower == "mix":
                asegment = asegment.set_channels(1)

            elif use_channel.lower() == "left":
                asegment = asegment.split_to_mono()[0]

            elif use_channel.lower() == "right":
                asegment = asegment.split_to_mono()[1]

    if asegment.frame_rate < 16000:
        raise Exception("Audio frame_rate is %d which is below 16000" % (asegment.frame_rate))
    if asegment.frame_rate > 16000:
        # print("Downsampling from %d to 16000" % (asegment.frame_rate))
        asegment = asegment.set_frame_rate(16000)

    if asegment.sample_width != 2:
        # print("Convert sample with from %d to 2" % (asegment.sample_width))
        asegment = asegment.set_sample_width(2)

    audio_length = len(asegment) / float(60000)
    if audio_length > 4.5:
        # print("Audio length: ", audio_length)
        raise Exception("Audio too long")

    return BufferAudioSource(data_buffer = asegment._data,
                                 sampling_rate = asegment.frame_rate,
                                 sample_width = asegment.sample_width,
                                 channels = asegment.channels)


class Worker(Thread):

    def __init__(self, timeout=0.2):
        self.timeout = timeout
        self.logger = None
        if sys.executable.endswith("pythonw.exe"):
            sys.stdout = open(os.devnull, "w");
            sys.stderr = open(os.path.join(os.getenv("TEMP"), "stderr-"+os.path.basename(sys.argv[0])), "w")
        else:
            self.logger = logging.getLogger(__name__)

        self._inbox = Queue()
        self._stop_request = Queue()
        Thread.__init__(self)

    def debug_message(self, message):
        if self.logger:
            self.logger.debug(message)

    def _stop_requested(self):

        try:
            message = self._stop_request.get_nowait()
            if message == "stop":
                return True

        except Empty:
            return False

    def stop(self):
        self._stop_request.put("stop")
        if self.isAlive():
            self.join()

    def send(self, message):
        self._inbox.put(message)

    def _get_message(self):
        try:
            message = self._inbox.get(timeout=self.timeout)
            return message
        except Empty:
            return None

class TokenizerWorker(Worker):

    END_OF_PROCESSING = "END_OF_PROCESSING"

    def __init__(self, ads, tokenizer, analysis_window, observer):
        self.ads = ads
        self.tokenizer = tokenizer
        self.analysis_window = analysis_window
        self.observer = observer
        self._inbox = Queue()
        self.count = 0
        Worker.__init__(self)

    def run(self):

        def notify_observers(data, start, end):
            audio_data = b''.join(data)
            self.count += 1

            start_time = start * self.analysis_window
            end_time = (end+1) * self.analysis_window
            duration = (end - start + 1) * self.analysis_window

            # notify observers
            self.observer.notify({"id" : self.count,
                             "audio_data" : audio_data,
                             "start" : start,
                             "end" : end,
                             "start_time" : start_time,
                             "end_time" : end_time,
                             "duration" : duration}
                            )

        self.ads.open()
        self.tokenizer.tokenize(data_source=self, callback=notify_observers)
        self.observer.notify(TokenizerWorker.END_OF_PROCESSING)

    def read(self):
        if self._stop_requested():
            return None
        else:
            return self.ads.read()

class TokenSaverWorker(Worker):

    def __init__(self, api_key, timeout=0.2, callback=None, server_url="service.grpc.vais.vn:50051", **kwargs):
        self.kwargs = kwargs
        self.max_asr_thread = 4
        self.total_data = 0
        self.server_url = server_url
        self.api_key = api_key
        self.callback = callback
        self.asr_queue = Queue()
        self.data_queue = Queue()
        self.results = OrderedDict()
        self.stop_request = False
        Worker.__init__(self, timeout=timeout)

    def run_asr(self, s_time, e_time, audio_data):
        def on_result(text, is_final, **kwargs):
            if is_final:
                if text:
                    text = text.replace("<SPOKEN_NOISE>", "").strip()
                    if s_time not in self.results:
                        self.results[s_time] = [e_time, [text]]
                    else:
                        self.results[s_time][1].append(text)
        with vais.VaisService(self.api_key, record=False, server_url=self.server_url) as vais_engine:
            vais_engine.asr_callback = on_result
            vais_engine.asr(audio_data=audio_data)
        if s_time in self.results:
            self.results[s_time][1] = " ".join(self.results[s_time][1])

    def do_the_work(self):
        display_text = []
        try:
            while True:
                try:
                    s_time, e_time, audio_data = self.data_queue.get(timeout=1)
                    if s_time is None:
                        break
                except Empty:
                    continue
                if self._stop_requested() or self.stop_request:
                    self.debug_message({"status": "Got stop request"})
                    self.stop_request = True
                    break
                # self.debug_message({"status": "queue new asr session", "start_time": s_time})
                self.run_asr(s_time, e_time, audio_data)
                self.data_queue.task_done()
                if self.callback:
                    display_text = []
                    done_percentage = 100 * float(self.total_data - self.data_queue.qsize()) / self.total_data
                    for s, (e, text) in self.results.items():
                        if isinstance(text, list):
                            text = " ".join(text)
                        display_text.append("--> %s ..." %(text[:40]))
                    self.callback(done_percentage, "\n".join(display_text[-10:]))
        except Exception as e:
            self.debug_message({"status": e})
        self.asr_queue.task_done()

    def run(self):
        self.asr_queue = Queue()
        for i in range(self.max_asr_thread):
            t = Thread(target=self.do_the_work)
            t.daemon = True
            t.start()
            self.asr_queue.put(t)
        run_s_time = time.time()
        while True:
            if self._stop_requested():
                break

            message = self._get_message()
            if message is not None:
                if message == TokenizerWorker.END_OF_PROCESSING:
                    break

                audio_data = message.pop("audio_data", None)
                start_time = message.pop("start_time", None)
                end_time = message.pop("end_time", None)
                _id = message.pop("id", None)
                # self.debug_message({"status": "new segment %.2f %.2f" % (start_time, end_time)})
                self.data_queue.put((start_time, end_time, audio_data))

        for i in range(self.max_asr_thread):
            self.data_queue.put((None, None, None))
        self.asr_queue.join()
        run_e_time = time.time()
        self.callback(100, "Done! Spent %.2fs" % (run_e_time - run_s_time), is_finished=True)

    def notify(self, message):
        self.total_data += 1
        self.send(message)

def segment_audio(fname, api_key, energy_threshold=50, min_duration=0.2, max_duration=20, max_silence=0.3, callback=None,
        server_url="service.grpc.vais.vn:50051"):
    tokenizer_worker = None
    audio_segment = []
    observer = TokenSaverWorker(api_key, callback=callback, server_url=server_url)
    # try:
    analysis_window = 0.01
    asource = None
    try:
        asource = file_to_audio_source(fname)
    except Exception as e:
        callback(-1, "File audio không được hỗ trợ, hoặc độ dài quá 4 phút!", False)
        return None, None
    ads = ADSFactory.ads(audio_source=asource, block_dur=analysis_window, max_time=None, record=False)
    validator = AudioEnergyValidator(sample_width=asource.get_sample_width(), energy_threshold=energy_threshold)
    mode = 0
    analysis_window_per_second = 1. / analysis_window
    tokenizer = StreamTokenizer(validator=validator, min_length=min_duration * analysis_window_per_second,
                                    max_length=int(max_duration * analysis_window_per_second),
                                    max_continuous_silence=max_silence * analysis_window_per_second,
                                    mode = mode)
    tokenizer_worker = TokenizerWorker(ads, tokenizer, analysis_window, observer)
    return tokenizer_worker, observer

    # except KeyboardInterrupt:
        # if tokenizer_worker is not None:
            # tokenizer_worker.stop()
        # observer.stop()

    # f = open(fname_output, 'w', newline='')
    # import csv
    # fieldnames = ['start', 'end', 'text']
    # writer = csv.DictWriter(f, fieldnames=fieldnames)
    # writer.writeheader()
    # sorted_x = sorted(observer.results.items(), key=operator.itemgetter(0))
    # for start_time, (end_time, text) in sorted_x:
        # writer.writerow({'start': start_time, 'end': end_time, 'text': text})

if __name__ == "__main__":
    data = segment_audio("/home/truong-d/work/vais/vlsp18/wav/002192e360_4m.wav", "demo", "output.csv")
