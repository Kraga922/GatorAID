import React from 'react';

function VideoStream() {
  return (
    <div>
      <h1>Pose Detection Stream</h1>
      {/* The video feed will be displayed using the <img> element */}
      <img
        src="http://127.0.0.1:5000/video_feed"
        alt="Video Stream"
        style={{ width: '100%', height: 'auto' }}
      />
    </div>
  );
}

export default VideoStream;
