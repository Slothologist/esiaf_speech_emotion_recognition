#!/usr/bin/env python


import pyesiaf
import rospy
from moveit_ros_planning_interface._moveit_roscpp_initializer import roscpp_init
from esiaf_ros.msg import RecordingTimeStamps, AugmentedAudio, EmotionInfo

# config
import yaml
import sys

def msg_from_string(msg, data):
    msg.deserialize(data)

nodename = 'esiaf_emotion_recognizer'

# initialize rosnode
rospy.init_node(nodename)
roscpp_init(nodename, [])

# read config
rospy.loginfo('Loading config...')
argv = sys.argv
if len(argv) < 2:
    rospy.logerr('Need path to configfile as first parameter!')
    exit('1')
path_to_config = argv[1]
data = yaml.safe_load(open(path_to_config))

rospy.loginfo('Creating emotion recognizer instance...')

#wrapper = Wrapper(nodename=nodename)

emotion_publisher = rospy.Publisher(nodename + '/' + 'EmotionInfo', EmotionInfo, queue_size=10)

rospy.loginfo('Creating esiaf handler...')
handler = pyesiaf.Esiaf_Handler('emotion_recognizer', pyesiaf.NodeDesignation.EmotionInfo, sys.argv)

rospy.loginfo('Setting up esiaf...')
esiaf_format = pyesiaf.EsiafAudioFormat()
esiaf_format.rate = pyesiaf.Rate.RATE_16000
esiaf_format.bitrate = pyesiaf.Bitrate.BIT_INT_16_SIGNED
esiaf_format.endian = pyesiaf.Endian.LittleEndian
esiaf_format.channels = 1

esiaf_audio_info = pyesiaf.EsiafAudioTopicInfo()
esiaf_audio_info.topic = data['esiaf_input_topic']
esiaf_audio_info.allowedFormat = esiaf_format

rospy.loginfo('adding input topic...')


def input_callback(audio, timeStamps):
    # deserialize inputs
    _recording_timestamps = RecordingTimeStamps()
    msg_from_string(_recording_timestamps, timeStamps)

    # voice vector call
    emotion, probability = 0, 0

    # assemble output
    output = EmotionInfo()
    output.duration = _recording_timestamps
    output.voiceId = emotion
    output.probability = probability

    # publish output
    emotion_publisher.publish(output)



handler.add_input_topic(esiaf_audio_info, input_callback)
rospy.loginfo('input topic added')
handler.start_esiaf()

rospy.loginfo('Emotion recognizer ready!')
rospy.spin()

handler.quit_esiaf()
