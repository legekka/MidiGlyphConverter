# MIDI to GLYPH converter
Using vanilla FL Studio 20, you can create custom glyphs for Nothing Phone (1), which can be exported as a MIDI file. The `converter.py` script will export it in the correct format to use it with [Glyph Control - Phone (1)](https://play.google.com/store/apps/details?id=tech.ozstudios.np1_glyph_control)


###  **Warning! This repo isn't really user friendly, so you have to do some research on your own f you get stuck. Root is also needed!**

Editor:
![FL Visualizer](https://legekka.fs.boltz.hu/lxukih.gif)

## Requirements
I recommend using a virtual environment, but it's not necessary. You can install the requirements with: 

```
pip install -r requirements.txt
```

## Usage
1. Open the provided FL studio file in `FL/Notification-1.flp`, when opening first, you will have to set the correct path for each `resources`. (Couldn't managed to store them in relative paths)
2. If you are not familiar with FL studio, I can't really help you, but you can find a lot of tutorials on YouTube. Basically you have to edit the values of the Automation Clips to control the LEDs in the animation. You can also play around with the knobs on the Control Surface
3. When you are done, export the project as a MIDI file. (File -> Export -> MIDI File), here are my settings:
![midi settings](https://legekka.fs.boltz.hu/025qwu.png)
4. Convert the MIDI file with the `converter.py` script. Here's how you can run it:
    ```
    python converter.py <input_file.mid> -r <resolution>
    ```
    The resolution is the duration of a single frame in milliseconds. (Default: 100)<br> 
    In theory you could use 15ms, but I don't recommend it, because my script isn't optimized for that. With my phone, I got the best results with 30/50ms, but you can play around with it. It gets slower with higher resolution because the Glyph Control app can't handle it.<br>
    You will get 3 files in the `output` folder. 

5. Now you'll have to create a new pattern in the **Glyph Control** app on your phone. I've just added some basic "Still" pattern, it will get replaced either way, so it doesn't matter.
![pattern-creation-1](https://legekka.fs.boltz.hu/bhnt45.png)
![pattern-creation-2](https://legekka.fs.boltz.hu/8a2yfb.png)

6. Now you should get your `FlutterSharedPreferences.xml`. I've provided one with the repo to know how it looks like, but you should use your own. It's located on your phone at `/data/data/tech.ozstudios.np1_glyph_control/shared_prefs/FlutterSharedPreferences.xml`. You can use `adb` to pull it from your phone.

7. To edit the file, you should replace the `||EDIT THIS||` part with the content of your output's TXT file.
    ```xml
    <?xml version='1.0' encoding='utf-8' standalone='yes' ?>
    <map>
        <string name="flutter.currentNotifPattern">patternio</string>
        <string name="flutter.My-New-Pattern ">||EDIT THIS||</string>
        <string name="flutter.journal">VGhpcyBpcyB0aGUgcHJlZml4IGZvciBhIGxpc3QurO0ABXNyABNqYXZhLnV0aWwuQXJyYXlMaXN0eIHSHZnHYZ0DAAFJAARzaXpleHAAAAACdwQAAAAC&#10;dAAJcGF0dGVybmlvdAAPTXktTmV3LVBhdHRlcm4geA==&#10;    </string>
        <string name="flutter.patternio">a_big_json</string>
    </map>
    ```
8. First **Force Stop** the app, then you can copy back the `FlutterSharedPreferences.xml` to your phone. (You can use `adb push` for that)
9. Start the app, and select your new pattern. It should work now!