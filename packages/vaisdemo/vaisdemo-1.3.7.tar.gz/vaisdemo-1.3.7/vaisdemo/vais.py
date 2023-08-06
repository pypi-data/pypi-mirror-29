from __future__ import print_function
import uuid
import grpc
import json
import audioop
import shutil
import yaml
import vaisdemo.speech.v1.cloud_speech_pb2_grpc as cloud_speech_pb2_grpc
import vaisdemo.speech.v1.cloud_speech_pb2 as cloud_speech_pb2
import threading
import importlib
import vaisdemo.capture as capture
import wave

try:
    import pyaudio
except Exception as e:
    exit(1)

CHUNK = 640

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
RECORD_SECONDS = 15
lock = threading.Lock()

class VaisService():
    def __init__(self, api_key, resources_path=None, silence=False, mic_name=None, record=True, server_url="service.grpc.vais.vn:50051"):
        self.api_key = api_key
        self.record = record
        self.url = server_url
        self.channel = grpc.insecure_channel(self.url)
        self.channel.subscribe(callback=self.connectivity_callback, try_to_connect=True)
        self.stop = False
        self.stub = cloud_speech_pb2_grpc.SpeechStub(self.channel)
        self.volume = 0
        self.mic_name = mic_name
        if self.record:
            self.capture = capture.Capture({'sound': {'input_device': mic_name}}, "/tmp/audio")
        self.asr_callback = None
        self.encoder = None
        try:
            from speex import WBEncoder
            self.encoder = WBEncoder()
            self.encoder.quality = 10
            packet_size = self.encoder.frame_size
            CHUNK = packet_size
        except Exception as e:
            pass

    def state_callback(*args):
        pass

    def __enter__(self):
        if self.record:
            self.capture.setup(self.state_callback)
        return self

    def __exit__(self, *args):
        if self.record:
            self.capture.cleanup()
        try:
            shutil.rmtree("/tmp/audio")
        except Exception as e:
            pass

    def connectivity_callback(self, c):
        pass

    def get_speech(self):
        try:
            audio_stream = self.capture.silence_listener()
            for data in audio_stream:
                self.volume = audioop.max(data, 2)
                if self.encoder:
                    with lock:
                        data = self.encoder.encode(data)
                yield data
        except Exception as e:
            self.asr_callback(e.message, False)

    def load_audio(self, fname):
        fin = wave.open(fname)
        nframes = fin.getnframes()
        chunk_size = 640
        total_read = 0
        n_read = 0
        while total_read < nframes:
            n_read += 1
            nframe_left = nframes - total_read
            read_size = chunk_size
            if chunk_size > nframe_left:
                read_size = nframe_left

            data = fin.readframes(read_size)
            self.volume = audioop.max(data, 2)
            if self.encoder:
                with lock:
                    data = self.encoder.encode(data)
            total_read += read_size
            yield data

    def load_audio_bin(self, all_data):
        nframes = len(all_data)
        chunk_size = 640
        total_read = 0
        n_read = 0
        for s_idx in range(0, nframes, chunk_size):
            e_idx = s_idx + chunk_size
            data = all_data[s_idx:e_idx]
            data_length = len(data)
            if data_length == chunk_size:
                if self.encoder:
                    with lock:
                        data = self.encoder.encode(data)
                yield data

    def generate_messages(self, filename=None, audio_data=None):
        audio_encode = cloud_speech_pb2.RecognitionConfig.SPEEX_WITH_HEADER_BYTE
        if self.encoder is None:
            audio_encode = cloud_speech_pb2.RecognitionConfig.LINEAR16

        config = cloud_speech_pb2.RecognitionConfig(encoding=audio_encode, max_alternatives=3)
        streaming_config = cloud_speech_pb2.StreamingRecognitionConfig(config=config, single_utterance=False, interim_results=True)
        request = cloud_speech_pb2.StreamingRecognizeRequest(streaming_config=streaming_config)
        yield request
        speech_iter = None
        if (not filename) and (not audio_data):
            speech_iter = self.get_speech()
        elif not audio_data:
            speech_iter = self.load_audio(filename)
        else:
            speech_iter = self.load_audio_bin(audio_data)

        self.asr_callback("Ready!", False)
        for audio in speech_iter:
            request = cloud_speech_pb2.StreamingRecognizeRequest(audio_content=audio)
            yield request

    def asr(self, filename=None, audio_data=None):
        self.asr_callback("Connecting ...", False)
        metadata = [(b'api-key', self.api_key)]
        responses = self.stub.StreamingRecognize(self.generate_messages(filename=filename, audio_data=audio_data), metadata=metadata)
        for response in responses:
            if response.results:
                if response.results[0].alternatives:
                    if not response.results[0].is_final:
                        self.asr_callback(response.results[0].alternatives[0].transcript,
                                      response.results[0].is_final)
                    else:
                        output = []
                        confidence = []
                        for w in response.results[0].alternatives[0].words:
                            confidence.append(w.confidence)
                            output.append(w.word)
                            # if w.confidence < 0.6:
                                # output.append("[color=a06f1b]" + w.word + "[/color]")
                            # else:
                                # output.append(w.word)
                        self.asr_callback(response.results[0].alternatives[0].transcript,
                                      response.results[0].is_final, confidence=confidence, words=output)

                    # for alternative in response.results[0].alternatives:
                        # print("-->", alternative.transcript)
                        # for w in alternative.words:
                            # print("Word:", w.word, "Confidence:", w.confidence)
