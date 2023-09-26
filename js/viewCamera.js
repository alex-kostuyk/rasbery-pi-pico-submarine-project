async function startWebcam() {
    try {
        const devices = await navigator.mediaDevices.enumerateDevices();
        let cameraDevice = null;

        for (const device of devices) {
            if (device.kind === 'videoinput' && device.label === 'USB2.0 PC CAMERA') {
                cameraDevice = device;
                break;
            }
        }

        const constraints = cameraDevice
            ? { video: { deviceId: cameraDevice.deviceId } }
            : { video: true };

        const stream = await navigator.mediaDevices.getUserMedia(constraints);
        const webcamVideo = document.getElementById('webcam');
        webcamVideo.srcObject = stream;
    } catch (error) {
    alert('Error accessing the cam:', error);
    }
}

startWebcam();