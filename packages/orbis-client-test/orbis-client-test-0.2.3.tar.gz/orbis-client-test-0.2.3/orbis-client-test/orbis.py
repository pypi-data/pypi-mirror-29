
import scipy.signal
import scipy.io.wavfile
import numpy as np
import argparse

from grpc.beta import implementations
import tensorflow as tf

from tensorflow_serving.apis import predict_pb2
from tensorflow_serving.apis import prediction_service_pb2


class Client(object):
    def __init__(self, hostport='localhost:9009'):
        self.host, port = hostport.split(':')
        self.port = int(port)
        self.feature = {
                "spectrum": tf.FixedLenFeature([200*161], dtype=tf.float32),
                }


    def from_wavfile(self, path):
        fs, signal = scipy.io.wavfile.read(path)
        return self._run(fs, signal)


    def from_signal(self, fs, signal):
        return self._run(fs, signal)


    def _run(self, fs, signal):
        channel = implementations.insecure_channel(self.host, self.port)
        stub = prediction_service_pb2.beta_create_PredictionService_stub(channel)

        flatten_spectrum = self._preprocessing(fs, signal)
        tensor_proto = self._tensor_proto(flatten_spectrum)
        request = self._make_request(tensor_proto)
        outputs = stub.Predict(request, 5.0).outputs

        response = dict(zip(['neu', 'hap', 'sad', 'ang', 'fru', 'exc'], outputs['prob'].float_val))
        response['class'] = int(outputs['classes'].int64_val[0])
        return response


    def _make_request(self, tensor_proto):
        request = predict_pb2.PredictRequest()
        request.model_spec.name = 'emotion_test'
        request.model_spec.signature_name = 'response'
        request.inputs['spectrum'].CopyFrom(tensor_proto)
        return request


    def _tensor_proto(self, flatten_spectrum):
        example = tf.train.Example()
        example.features.feature['spectrum'].float_list.value.extend(flatten_spectrum)
        serialized = example.SerializeToString()
        return tf.contrib.util.make_tensor_proto(serialized, shape=[1])


    def _preprocessing(self, fs, signal):
        f, t, Zxx = scipy.signal.stft(signal, fs=fs, window='hamming', nperseg=800)

        time_sample = t[1]-t[0]
        max_length = int(4/time_sample)+1

        time_list = t.tolist()
        slices = []

        while time_list:
            if len(time_list) < max_length:
                slices.append(len(time_list))
                break
            slices.append(max_length)
            del time_list[:max_length]

        remains = (max_length-slices[-1])/len(slices)
        if len(slices) > 1:
            slices[-1] += len(slices)*remains
            slices = map(lambda x: int(round(x-remains)), slices)

        sliced_images = [Zxx[:, i*s:(i+1)*s] for i, s in enumerate(slices)]

        padded_images = []
        for img in sliced_images:
            r, c = img.shape

            origin_img = img[:r//2, :]
            pad_img = np.zeros([r//2, int(max_length)-c])

            padded_img = np.concatenate((origin_img, pad_img), axis=1)
            amp = np.abs(padded_img)
            clipped = np.clip(amp, a_min=10**0.1, a_max=1e10)
            log = np.log10(clipped)
            padded_images.append(log)

        return np.reshape(padded_images[0], [-1])



if __name__=="__main__":
    arg_parser = argparse.ArgumentParser(description='input data path')
    arg_parser.add_argument('input_data')
    args = arg_parser.parse_args()

    inference = Client('52.78.57.147:9009')
    response = inference.from_wavfile(args.input_data)


    print(response)

