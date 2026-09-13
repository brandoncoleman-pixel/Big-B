# Big-B

## Reproducible Codespace

This repository includes a `.devcontainer` image with the Big-B desktop
software, Google Chrome, FreeRDP, PulseAudio, FFmpeg, TigerVNC, noVNC, and
the Python media-bridge dependency preinstalled. When creating a Codespace,
select the repository's **Big-B Desktop** dev container and let it finish
building. If this Codespace already existed before the `.devcontainer` files
were added or changed, run **Codespaces: Rebuild Container** first. After the
build completes, start the complete setup with:

```sh
./start
```

The image forwards noVNC on port `6080`, the media bridge on `6081`, and VNC
on `5901`. The Codespace image build is the only installation step.

## Media setup

Run `./start` to launch the VNC desktop and RDP session. The RDP connection
now enables:

- Playback audio through the local PulseAudio-compatible server.
- Microphone redirection for Google Chat.
- Optional webcam USB redirection with `RDP_USB_CAMERA`.

For media on the computer running noVNC, open the forwarded `6081` URL in that
browser and choose **Connect camera and microphone**. Keep that page open while
using Google Chat in the Chrome window inside the noVNC desktop. It requests the
local camera and microphone, sends microphone audio to the desktop's PulseAudio
source, publishes camera frames to its virtual V4L2 camera, plays remote desktop
speaker output locally, and provides the speaker volume slider. Opening port
`6081` directly now displays this page instead of a WebSocket error.

Control whether Google Chat can reach the bridge with `./port6081 on`,
`./port6081 off`, `./port6081 status`, or `./port6081 toggle`. `off` keeps the
bridge running but changes the forwarded port to private access. The same
control is available as the **Port access** button on the 6081 media page.
The page also has separate **Microphone**, **Camera**, and **Speaker** switches.
Turn on **Camera** to preview the local webcam, then use **Record camera** to
download a WebM recording. Camera recording is local to the browser; sending
camera frames into the noVNC Chrome still requires `/dev/video0`.

The startup output must say `Media bridge is listening on port 6081`,
`Virtual microphone source is available`, and `Virtual camera device is
available`. Camera frames from the 6081 page appear in Chrome as `Big-B Virtual
Camera`, and the microphone appears as `vnc_microphone`. If the virtual
camera warning remains, the host kernel must provide compatible `videodev` and
`v4l2loopback` modules; installing the userspace package alone is not enough.
Without `/dev/video0`, Google Chat video in the noVNC Chrome cannot update; the
microphone and speaker paths can still work. In this Codespace, loading the
kernel module is blocked, so use a webcam exposed to FreeRDP with
`RDP_USB_CAMERA` or `RDP_USB_AUTO=1` for Google Chat video.

Microphone audio uses short packets and a bounded bridge queue so PulseAudio
backpressure does not stall incoming voice data.
The microphone and remote-speaker PulseAudio sinks are separate, preventing
Google Chat playback from being fed back into the microphone recording.

For a separate FreeRDP session, camera forwarding requires the webcam to be
visible as a USB device to the FreeRDP host. Set its FreeRDP identifier before
starting, for example:

```sh
export RDP_USB_CAMERA='046d:0825#123456'
./start
```

To let FreeRDP discover eligible USB cameras automatically, use:

```sh
export RDP_USB_AUTO=1
./start
```

In Google Chat or another site, click the browser permission prompt and choose
`vnc_microphone` and `Big-B Virtual Camera` when using Chrome inside noVNC. The
RDP browser uses its own redirected devices, while the local noVNC browser uses
the devices granted to the media page.

For the RDP microphone path, connect the media page before joining the Google
Chat call. If the RDP session was already open before the virtual microphone
was created, restart the desktop with `./stop` followed by `./start` so
FreeRDP discovers `vnc_microphone`.

noVNC itself only transports the desktop video and input; it does not
transport speaker, camera, or microphone media channels.