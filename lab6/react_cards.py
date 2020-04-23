#!/usr/bin/env python3

import asyncio
import sys

import cv2
import numpy as np

sys.path.insert(0, '../lab5')
import imgclassification

import cozmo
from cozmo.util import degrees, distance_mm, speed_mmps


try:
    from PIL import ImageDraw, ImageFont
except ImportError:
    sys.exit('run `pip3 install --user Pillow numpy` to run this example')


async def run(robot: cozmo.robot.Robot):
    '''The run method runs once the Cozmo SDK is connected.'''

    try:
    
        # Move lift down and tilt the head up
        await robot.set_head_angle(degrees(10)).wait_for_completed()
        robot.move_lift(-3)

        img_clf = imgclassification.ImageClassifier()

        # load images
        (train_raw, train_labels) = img_clf.load_data_from_folder('../lab5/train/')  
        # convert images into features
        train_data = img_clf.extract_image_features(train_raw)
        # train model
        img_clf.train_classifier(train_data, train_labels)

        num_images = 20
        while True:
            data = np.empty([num_images, 240, 320, 3])
            for i in range(num_images): 
                # get camera image
                event = await robot.world.wait_for(cozmo.camera.EvtNewRawCameraImage, timeout=30)
                # add to data
                data[i] = np.asarray(event.image)
                
            # convert camera image into features
            live_data = img_clf.extract_image_features(data)

            # get label
            predicted_labels = img_clf.predict_labels(live_data)
            print("Predicc: ")
            print(predicted_labels)

            # say/ act on label
            # NOTE: one could increase num_images, and create an outer loop in
            # order to make sure X number of labels is consistent, but I found
            # this simpler version to work better 
            for x in range(num_images):
                if (predicted_labels[x] == "plane"):
                    await robot.say_text("plane", voice_pitch=-1.0, duration_scalar=0.5).wait_for_completed()
                    await robot.play_anim_trigger(cozmo.anim.Triggers.CubePounceWinRound).wait_for_completed()
                    await robot.set_head_angle(degrees(10)).wait_for_completed()
                    break
                elif (predicted_labels[x] == "drone"):
                    await robot.say_text("drone", voice_pitch=-1.0, duration_scalar=0.5).wait_for_completed()
                    await robot.play_anim_trigger(cozmo.anim.Triggers.CubePounceWinRound).wait_for_completed()
                    await robot.set_head_angle(degrees(10)).wait_for_completed()
                    break
                elif (predicted_labels[x] == "inspection"):
                    await robot.say_text("inspection", voice_pitch=-1.0, duration_scalar=0.5).wait_for_completed()
                    await robot.play_anim_trigger(cozmo.anim.Triggers.CubePounceWinRound).wait_for_completed()
                    await robot.set_head_angle(degrees(10)).wait_for_completed()
                    break


    except KeyboardInterrupt:
        print("")
        print("Exit requested by user")
    except cozmo.RobotBusy as e:
        print(e)

if __name__ == '__main__':
    cozmo.run_program(run, use_viewer = True, force_viewer_on_top = True)

