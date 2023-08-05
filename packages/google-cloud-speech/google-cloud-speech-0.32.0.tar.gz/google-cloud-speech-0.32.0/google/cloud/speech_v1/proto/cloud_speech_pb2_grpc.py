# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import google.cloud.speech_v1.proto.cloud_speech_pb2 as google_dot_cloud_dot_speech__v1_dot_proto_dot_cloud__speech__pb2
import google.longrunning.operations_pb2 as google_dot_longrunning_dot_operations__pb2


class SpeechStub(object):
  """Service that implements Google Cloud Speech API.
  """

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.Recognize = channel.unary_unary(
        '/google.cloud.speech.v1.Speech/Recognize',
        request_serializer=google_dot_cloud_dot_speech__v1_dot_proto_dot_cloud__speech__pb2.RecognizeRequest.SerializeToString,
        response_deserializer=google_dot_cloud_dot_speech__v1_dot_proto_dot_cloud__speech__pb2.RecognizeResponse.FromString,
        )
    self.LongRunningRecognize = channel.unary_unary(
        '/google.cloud.speech.v1.Speech/LongRunningRecognize',
        request_serializer=google_dot_cloud_dot_speech__v1_dot_proto_dot_cloud__speech__pb2.LongRunningRecognizeRequest.SerializeToString,
        response_deserializer=google_dot_longrunning_dot_operations__pb2.Operation.FromString,
        )
    self.StreamingRecognize = channel.stream_stream(
        '/google.cloud.speech.v1.Speech/StreamingRecognize',
        request_serializer=google_dot_cloud_dot_speech__v1_dot_proto_dot_cloud__speech__pb2.StreamingRecognizeRequest.SerializeToString,
        response_deserializer=google_dot_cloud_dot_speech__v1_dot_proto_dot_cloud__speech__pb2.StreamingRecognizeResponse.FromString,
        )


class SpeechServicer(object):
  """Service that implements Google Cloud Speech API.
  """

  def Recognize(self, request, context):
    """Performs synchronous speech recognition: receive results after all audio
    has been sent and processed.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def LongRunningRecognize(self, request, context):
    """Performs asynchronous speech recognition: receive results via the
    google.longrunning.Operations interface. Returns either an
    `Operation.error` or an `Operation.response` which contains
    a `LongRunningRecognizeResponse` message.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def StreamingRecognize(self, request_iterator, context):
    """Performs bidirectional streaming speech recognition: receive results while
    sending audio. This method is only available via the gRPC API (not REST).
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_SpeechServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'Recognize': grpc.unary_unary_rpc_method_handler(
          servicer.Recognize,
          request_deserializer=google_dot_cloud_dot_speech__v1_dot_proto_dot_cloud__speech__pb2.RecognizeRequest.FromString,
          response_serializer=google_dot_cloud_dot_speech__v1_dot_proto_dot_cloud__speech__pb2.RecognizeResponse.SerializeToString,
      ),
      'LongRunningRecognize': grpc.unary_unary_rpc_method_handler(
          servicer.LongRunningRecognize,
          request_deserializer=google_dot_cloud_dot_speech__v1_dot_proto_dot_cloud__speech__pb2.LongRunningRecognizeRequest.FromString,
          response_serializer=google_dot_longrunning_dot_operations__pb2.Operation.SerializeToString,
      ),
      'StreamingRecognize': grpc.stream_stream_rpc_method_handler(
          servicer.StreamingRecognize,
          request_deserializer=google_dot_cloud_dot_speech__v1_dot_proto_dot_cloud__speech__pb2.StreamingRecognizeRequest.FromString,
          response_serializer=google_dot_cloud_dot_speech__v1_dot_proto_dot_cloud__speech__pb2.StreamingRecognizeResponse.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'google.cloud.speech.v1.Speech', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
