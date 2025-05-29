import React from 'react';

const spinnerStyle: React.CSSProperties = {
  border: '4px solid rgba(0, 0, 0, 0.1)',
  width: '36px',
  height: '36px',
  borderRadius: '50%',
  borderLeftColor: '#09f', // Or your app's primary color
  animation: 'spin 1s ease infinite',
};

// Keyframes need to be injected globally or via a styled-components approach for broader compatibility.
// For a simple component like this, injecting a <style> tag is a straightforward way if not using CSS-in-JS libs.
const keyframesStyle = `
  @keyframes spin {
    0% {
      transform: rotate(0deg);
    }
    100% {
      transform: rotate(360deg);
    }
  }
`;

export const LoadingSpinner: React.FC = () => {
  return (
    <>
      {/* eslint-disable-next-line react/no-danger */}
      <style dangerouslySetInnerHTML={{ __html: keyframesStyle }} />
      <div style={spinnerStyle} data-testid="loading-spinner" />
    </>
  );
};

export default LoadingSpinner;
