# flask-crop
A flask application which will crop images from filesystem with size in name.
For example `$hostname/photos/test_150x150.jpg' is goint to find `photos/test.jpg` and will crop it to 150x150px, serve it and save it.
You need to set the `MEDIA_ROOT`.
