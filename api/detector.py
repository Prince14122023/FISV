import cv2
import numpy as np

def analyze_fabric(frame):
    try:
        
        smooth = cv2.bilateralFilter(frame, 13, 90, 90)
        lab = cv2.cvtColor(smooth, cv2.COLOR_BGR2Lab)
        l_chan, a_chan, b_chan = cv2.split(lab)
        
        
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8)).apply(l_chan)


        edges = cv2.Canny(clahe, 90, 210) 
        mask = cv2.dilate(edges, np.ones((3,3), np.uint8))
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        status, defect_type, briefing, accuracy = "PASS", "OPTIMAL", "Surface integrity meets 100% industrial standards.", 100.0
        max_area = 0

        
        for cnt in contours:
            area = cv2.contourArea(cnt)
            
            if area > 150:
                x, y, w, h = cv2.boundingRect(cnt)
                
                if area > max_area:
                    max_area = area
                    status = "FAIL"
                    defect_type = "SURFACE ANOMALY"
                    accuracy = 65.0
                    
                    aspect = float(w)/h
                    roi_l = clahe[y:y+h, x:x+w]
                    mean_l = np.mean(roi_l)
                    mean_a = np.mean(a_chan[y:y+h, x:x+w])
                    mean_b = np.mean(b_chan[y:y+h, x:x+w])

                    
                    if mean_l < 85:
                        briefing = "CRITICAL: Structural matrix breach (Hole/Void) detected. Physical material integrity is compromised."
                    elif aspect < 0.2:
                        briefing = "WARNING: Vertical linear irregularity (Needle Line/Laddering) found. Yarn alignment failure detected."
                    elif aspect > 6.0:
                        briefing = "NOTICE: Horizontal insertion anomaly (Missing/Double Pick) identified in the weaving matrix."
                    elif mean_b > 152 or mean_a > 152 or mean_b < 108:
                        briefing = "ALERT: Chromatic inconsistency (Color Bleeding/Stain) detected. Unstable dye migration found."
                    elif area < 600:
                        briefing = "ANOMALY: Localized surface knot or abnormal yarn thickness (Slub) deviating from smooth baseline."
                    else:
                        briefing = "QUALITY FAIL: Non-standard texture pattern identified. Surface uniformity fails 100% scan protocol."

                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)

        return frame, status, defect_type, briefing, accuracy

    except Exception as e:
        return frame, "ERROR", "SYSTEM_FAULT", str(e), 0.0

