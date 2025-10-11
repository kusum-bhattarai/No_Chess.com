import React, { useState } from 'react';
import { colors, buttonStyle, buttonHoverStyle } from '../styles';

const modalOverlayStyle = {
  position: 'fixed',
  top: 0,
  left: 0,
  width: '100%',
  height: '100%',
  backgroundColor: 'rgba(0, 0, 0, 0.5)', // Semi-transparent backdrop
  display: 'flex',
  justifyContent: 'center',
  alignItems: 'center',
  zIndex: 1000,
  animation: 'fadeIn 0.3s ease', // Fade-in animation
};

const modalContentStyle = {
  backgroundColor: colors.background,
  padding: '30px',
  borderRadius: '12px', // Rounded for cuteness
  boxShadow: '0 4px 20px rgba(0, 0, 0, 0.2)', // Soft shadow
  width: '400px',
  textAlign: 'center',
};

const titleStyle = {
  fontSize: '1.8rem',
  marginBottom: '20px',
  color: colors.primary,
};

const inputStyle = {
  marginBottom: '20px',
  padding: '10px',
  width: '100%',
  border: `1px solid ${colors.primary}`,
  borderRadius: '8px',
};

const errorStyle = {
  color: '#D87070', // Red from colors (evalNegative)
  marginBottom: '10px',
};

const loadingStyle = {
  color: colors.primary,
  marginBottom: '10px',
};

// Keyframe animation (add to global styles or here)
const fadeIn = `@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }`;

function PgnUploadModal({ onClose, onUpload }) {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setError(null);
  };

  const handleUpload = async () => {
    if (!file) {
      setError('Please select a PGN file.');
      return;
    }
    setLoading(true);
    const formData = new FormData();
    formData.append('pgn_file', file);

    try {
      const response = await onUpload(formData); // Call parent handler
      onClose(); // Close modal on success
      // Parent will handle navigation
    } catch (err) {
      setError('Upload failed: ' + (err.response?.data?.detail || err.message));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={modalOverlayStyle} onClick={onClose}>
      <style>{fadeIn}</style> {/* Inline keyframes */}
      <div style={modalContentStyle} onClick={(e) => e.stopPropagation()}> {/* Prevent close on content click */}
        <h2 style={titleStyle}>Upload PGN File</h2>
        <input type="file" accept=".pgn" style={inputStyle} onChange={handleFileChange} />
        {error && <p style={errorStyle}>{error}</p>}
        {loading && <p style={loadingStyle}>Uploading...</p>}
        <button
          style={buttonStyle}
          onMouseOver={(e) => Object.assign(e.target.style, buttonHoverStyle)}
          onMouseOut={(e) => Object.assign(e.target.style, buttonStyle)}
          onClick={handleUpload}
          disabled={loading}
        >
          Upload and Review
        </button>
      </div>
    </div>
  );
}

export default PgnUploadModal;