import React, { useRef, useState, useEffect, useCallback } from "react";
import Webcam from "react-webcam";

const WebcamCapture = () => {
  const webcamRef = useRef(null);
  const [processedImgSrc, setProcessedImgSrc] = useState(null);

  const sendFrameToBackend = useCallback(async (imageSrc) => {
    try {
      const response = await fetch("http://localhost:5000/process_image", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ image: imageSrc }),
      });

      const data = await response.json();
      if (data.processed_image) {
        setProcessedImgSrc(`data:image/jpeg;base64,${data.processed_image}`);
      }
    } catch (error) {
      console.error("Error:", error);
    }
  }, []);

  const captureFrame = useCallback(() => {
    if (webcamRef.current) {
      const imageSrc = webcamRef.current.getScreenshot();
      if (imageSrc) {
        sendFrameToBackend(imageSrc);
      }
    }
  }, [sendFrameToBackend]);

  useEffect(() => {
    const interval = setInterval(() => {
      captureFrame(); // Capture a frame every 100ms (adjust this for performance)
    }, 100);
    return () => clearInterval(interval);
  }, [captureFrame]);

  return (
    <div>
      <Webcam
        audio={false}
        ref={webcamRef}
        screenshotFormat="image/jpeg"
        width={640}
        height={480}
      />
      <div>
        {processedImgSrc && (
          <img src={processedImgSrc} alt="Processed video stream" />
        )}
      </div>
    </div>
  );
};

export default WebcamCapture;
