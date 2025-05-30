// frontend/src/components/common/Notification.tsx
import React, { useEffect, useState } from 'react';

export type NotificationType = 'success' | 'error' | 'info';

interface NotificationProps {
  message: string | null;
  type?: NotificationType;
  duration?: number; // Duration in milliseconds, 0 for persistent
  onClose?: () => void; // Callback when notification closes itself or is closed by user
}

export const Notification: React.FC<NotificationProps> = ({
  message,
  type = 'info',
  duration = 3000, // Default to 3 seconds
  onClose,
}) => {
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    if (message) {
      setIsVisible(true);
      if (duration > 0) {
        const timer = setTimeout(() => {
          // Call handleClose only if it's still visible and relevant
          // This check helps if message changes rapidly causing stale closures
          if (isVisible) { 
            handleClose();
          }
        }, duration);
        return () => clearTimeout(timer);
      }
    } else {
      setIsVisible(false);
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [message, duration, isVisible]); // Added isVisible to deps to handle rapid message changes correctly

  const handleClose = () => {
    setIsVisible(false);
    if (onClose) {
      onClose();
    }
  };

  if (!isVisible || !message) {
    return null;
  }

  const getBackgroundColor = () => {
    switch (type) {
      case 'success':
        return '#4CAF50'; // Green
      case 'error':
        return '#f44336'; // Red
      case 'info':
      default:
        return '#2196F3'; // Blue
    }
  };

  const baseStyle: React.CSSProperties = {
    position: 'fixed',
    top: '20px',
    right: '20px',
    padding: '15px 20px',
    color: 'white',
    backgroundColor: getBackgroundColor(),
    borderRadius: '5px',
    boxShadow: '0 2px 10px rgba(0,0,0,0.2)',
    zIndex: 1000,
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    minWidth: '250px',
    maxWidth: '90%',
  };

  const closeButtonStyle: React.CSSProperties = {
    marginLeft: '15px',
    color: 'white',
    backgroundColor: 'transparent',
    border: 'none',
    fontSize: '1.2em',
    cursor: 'pointer',
  };

  return (
    <div style={baseStyle} role="alert">
      <span>{message}</span>
      {/* Show close button only if onClose is provided and notification is persistent (duration === 0) 
          OR if duration > 0 to allow manual closing before timer.
          Let's always show if onClose is provided, for better UX.
      */}
      {onClose && (
        <button onClick={handleClose} style={closeButtonStyle} aria-label="Close notification">
          &times;
        </button>
      )}
    </div>
  );
};
