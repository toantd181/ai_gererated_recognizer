import React, { useState, useEffect } from 'react';
import { Upload, Image, CheckCircle, XCircle, Loader, Sparkles, Camera, AlertCircle } from 'lucide-react';

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [serverStatus, setServerStatus] = useState('checking');

  const API_URL = 'http://localhost:5000';

  // Check server health on mount
  useEffect(() => {
    checkServerHealth();
  }, []);

  const checkServerHealth = async () => {
    try {
      const response = await fetch(`${API_URL}/health`);
      const data = await response.json();
      if (response.ok) {
        setServerStatus('connected');
        console.log('✓ Server connected:', data);
      } else {
        setServerStatus('error');
      }
    } catch (err) {
      setServerStatus('disconnected');
    }
  };

  const handleFileSelect = (e) => {
    const file = e.target.files[0];
    if (file) {
      // Check file size (16MB limit)
      if (file.size > 16 * 1024 * 1024) {
        setError('File size must be less than 16MB');
        return;
      }

      setSelectedFile(file);
      setPreview(URL.createObjectURL(file));
      setResult(null);
      setError(null);
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setError('Please select an image first');
      return;
    }

    if (serverStatus !== 'connected') {
      setError('Server is not connected. Please start the Flask backend first.');
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const response = await fetch(`${API_URL}/predict`, {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();

      if (response.ok && data.success) {
        setResult(data);
      } else {
        setError(data.error || 'Failed to process image');
      }
    } catch (err) {
      setError('Failed to connect to server. Make sure the Flask backend is running on http://localhost:5000');
      setServerStatus('disconnected');
    } finally {
      setLoading(false);
    }
  };

  const resetApp = () => {
    setSelectedFile(null);
    setPreview(null);
    setResult(null);
    setError(null);
  };

  const isAIGenerated = result && result.prediction === 'AI-Generated';

  return (
    <div style={{
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #f5f3ff 0%, #e0e7ff 50%, #fce7f3 100%)',
      padding: '2rem',
      fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
    }}>
      <div style={{ maxWidth: '56rem', margin: '0 auto' }}>
        {/* Header */}
        <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '1rem', marginBottom: '1rem' }}>
            <Camera size={48} color="#9333ea" />
            <Sparkles size={40} color="#ec4899" />
          </div>
          <h1 style={{ fontSize: '2.5rem', fontWeight: 'bold', color: '#1f2937', margin: '0 0 0.5rem 0' }}>
            AI Face Detector
          </h1>
          <p style={{ color: '#6b7280', fontSize: '1rem', margin: 0 }}>
            Detect if a face image is real or AI-generated using EfficientNet-B3
          </p>
          
          {/* Server Status Badge */}
          <div style={{ marginTop: '1rem', display: 'flex', justifyContent: 'center' }}>
            <div style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: '0.5rem',
              padding: '0.5rem 1rem',
              borderRadius: '9999px',
              fontSize: '0.875rem',
              fontWeight: '500',
              backgroundColor: serverStatus === 'connected' ? '#dcfce7' : 
                             serverStatus === 'disconnected' ? '#fee2e2' : '#fef3c7',
              color: serverStatus === 'connected' ? '#166534' : 
                     serverStatus === 'disconnected' ? '#991b1b' : '#92400e',
            }}>
              <div style={{
                width: '8px',
                height: '8px',
                borderRadius: '50%',
                backgroundColor: serverStatus === 'connected' ? '#22c55e' : 
                               serverStatus === 'disconnected' ? '#ef4444' : '#f59e0b',
              }} />
              {serverStatus === 'connected' && 'Server Connected'}
              {serverStatus === 'disconnected' && 'Server Disconnected'}
              {serverStatus === 'checking' && 'Checking Server...'}
            </div>
          </div>
        </div>

        {/* Main Card */}
        <div style={{ backgroundColor: 'white', borderRadius: '0.5rem', boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1)', padding: '2rem' }}>
          
          {/* Info Banner */}
          <div style={{
            padding: '1rem',
            backgroundColor: '#eff6ff',
            border: '1px solid #bfdbfe',
            borderRadius: '0.5rem',
            marginBottom: '1.5rem',
            display: 'flex',
            alignItems: 'flex-start',
            gap: '0.75rem',
          }}>
            <AlertCircle size={20} color="#2563eb" style={{ flexShrink: 0, marginTop: '0.125rem' }} />
            <div style={{ fontSize: '0.875rem', color: '#1e40af' }}>
              <strong>Tip:</strong> This model works best with face images. Upload a photo containing a face for optimal results. 
              The system will automatically detect and analyze the face.
            </div>
          </div>

          {/* Upload Section */}
          <div style={{ marginBottom: '1.5rem' }}>
            <label style={{ display: 'block', marginBottom: '1rem', cursor: 'pointer' }}>
              <div style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                width: '100%',
                height: '16rem',
                border: '2px dashed #d1d5db',
                borderRadius: '0.5rem',
                backgroundColor: '#f9fafb',
                transition: 'border-color 0.2s',
              }}
              onMouseEnter={(e) => e.currentTarget.style.borderColor = '#9333ea'}
              onMouseLeave={(e) => e.currentTarget.style.borderColor = '#d1d5db'}
              >
                {preview ? (
                  <img
                    src={preview}
                    alt="Preview"
                    style={{ maxHeight: '100%', maxWidth: '100%', objectFit: 'contain', borderRadius: '0.5rem' }}
                  />
                ) : (
                  <div style={{ textAlign: 'center' }}>
                    <Upload size={48} color="#9ca3af" style={{ margin: '0 auto 0.5rem' }} />
                    <p style={{ color: '#6b7280', margin: '0 0 0.25rem 0' }}>Click to upload face image</p>
                    <p style={{ color: '#9ca3af', fontSize: '0.875rem', margin: 0 }}>
                      PNG, JPG, JPEG (Max 16MB)
                    </p>
                  </div>
                )}
              </div>
              <input
                type="file"
                accept="image/png,image/jpeg,image/jpg"
                onChange={handleFileSelect}
                style={{ display: 'none' }}
              />
            </label>

            {/* Buttons */}
            <div style={{ display: 'flex', gap: '1rem' }}>
              <button
                onClick={handleUpload}
                disabled={!selectedFile || loading || serverStatus !== 'connected'}
                style={{
                  flex: 1,
                  background: (!selectedFile || loading || serverStatus !== 'connected') ? '#d1d5db' : 'linear-gradient(to right, #9333ea, #ec4899)',
                  color: 'white',
                  padding: '0.75rem 1.5rem',
                  borderRadius: '0.5rem',
                  border: 'none',
                  fontWeight: '600',
                  cursor: (!selectedFile || loading || serverStatus !== 'connected') ? 'not-allowed' : 'pointer',
                  fontSize: '1rem',
                  opacity: (!selectedFile || loading || serverStatus !== 'connected') ? 0.6 : 1,
                  transition: 'all 0.2s',
                }}
              >
                {loading ? (
                  <span style={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                    <Loader size={20} style={{ marginRight: '0.5rem', animation: 'spin 1s linear infinite' }} />
                    Analyzing Face...
                  </span>
                ) : (
                  'Detect AI Face'
                )}
              </button>
              
              <button
                onClick={resetApp}
                style={{
                  padding: '0.75rem 1.5rem',
                  border: '2px solid #d1d5db',
                  borderRadius: '0.5rem',
                  backgroundColor: 'white',
                  fontWeight: '600',
                  cursor: 'pointer',
                  fontSize: '1rem',
                  transition: 'all 0.2s',
                }}
                onMouseEnter={(e) => e.currentTarget.style.backgroundColor = '#f9fafb'}
                onMouseLeave={(e) => e.currentTarget.style.backgroundColor = 'white'}
              >
                Reset
              </button>
            </div>
          </div>

          {/* Error Message */}
          {error && (
            <div style={{
              padding: '1rem',
              backgroundColor: '#fef2f2',
              border: '1px solid #fecaca',
              borderRadius: '0.5rem',
              display: 'flex',
              alignItems: 'flex-start',
              marginBottom: '1.5rem',
            }}>
              <XCircle size={20} color="#ef4444" style={{ marginRight: '0.75rem', marginTop: '0.125rem', flexShrink: 0 }} />
              <div>
                <p style={{ color: '#991b1b', fontWeight: '600', margin: '0 0 0.25rem 0' }}>Error</p>
                <p style={{ color: '#dc2626', fontSize: '0.875rem', margin: 0 }}>{error}</p>
              </div>
            </div>
          )}

          {/* Results Section */}
          {result && result.success && result.prediction && (
            <div style={{
              padding: '1.5rem',
              border: '2px solid',
              borderRadius: '0.5rem',
              borderColor: isAIGenerated ? '#d8b4fe' : '#86efac',
              backgroundColor: isAIGenerated ? '#faf5ff' : '#f0fdf4',
            }}>
              <div style={{ display: 'flex', alignItems: 'center', marginBottom: '1rem' }}>
                {isAIGenerated ? (
                  <Sparkles size={24} color="#9333ea" style={{ marginRight: '0.5rem' }} />
                ) : (
                  <CheckCircle size={24} color="#22c55e" style={{ marginRight: '0.5rem' }} />
                )}
                <h3 style={{ fontSize: '1.25rem', fontWeight: 'bold', color: '#1f2937', margin: 0 }}>
                  Detection Result
                </h3>
              </div>

              <div style={{
                padding: '1.25rem',
                backgroundColor: 'white',
                borderRadius: '0.5rem',
                border: '2px solid',
                borderColor: isAIGenerated ? '#d8b4fe' : '#86efac',
                marginBottom: '1.5rem',
              }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '1rem' }}>
                  <div>
                    <p style={{ fontSize: '0.875rem', color: '#6b7280', margin: '0 0 0.5rem 0' }}>Classification</p>
                    <p style={{
                      fontSize: '2rem',
                      fontWeight: 'bold',
                      color: isAIGenerated ? '#9333ea' : '#22c55e',
                      display: 'flex',
                      alignItems: 'center',
                      gap: '0.5rem',
                      margin: 0,
                    }}>
                      {isAIGenerated ? (
                        <>
                          <Sparkles size={32} />
                          <span>AI Face</span>
                        </>
                      ) : (
                        <>
                          <Image size={32} />
                          <span>Real Face</span>
                        </>
                      )}
                    </p>
                  </div>
                  <div style={{ textAlign: 'right' }}>
                    <p style={{ fontSize: '0.875rem', color: '#6b7280', margin: '0 0 0.5rem 0' }}>Confidence</p>
                    <p style={{
                      fontSize: '2rem',
                      fontWeight: 'bold',
                      color: isAIGenerated ? '#9333ea' : '#22c55e',
                      margin: 0,
                    }}>
                      {result.percentage || '0%'}
                    </p>
                  </div>
                </div>

                <div style={{
                  width: '100%',
                  height: '0.75rem',
                  backgroundColor: '#e5e7eb',
                  borderRadius: '9999px',
                  overflow: 'hidden',
                }}>
                  <div style={{
                    height: '100%',
                    width: `${(result.confidence || 0) * 100}%`,
                    backgroundColor: isAIGenerated ? '#9333ea' : '#22c55e',
                    transition: 'width 0.5s',
                  }} />
                </div>
              </div>

              {result.details && (
                <div>
                  <p style={{ fontSize: '0.875rem', fontWeight: '600', color: '#374151', margin: '0 0 0.75rem 0' }}>
                    Detailed Probabilities:
                  </p>

                  <div style={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    padding: '0.75rem',
                    backgroundColor: 'white',
                    borderRadius: '0.5rem',
                    marginBottom: '0.75rem',
                  }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                      <Sparkles size={20} color="#9333ea" />
                      <span style={{ fontWeight: '500', color: '#374151' }}>AI-Generated Face</span>
                    </div>
                    <span style={{ fontSize: '0.875rem', fontWeight: '600', color: '#374151' }}>
                      {((result.details.ai_generated_probability || 0) * 100).toFixed(2)}%
                    </span>
                  </div>

                  <div style={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    padding: '0.75rem',
                    backgroundColor: 'white',
                    borderRadius: '0.5rem',
                  }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                      <Image size={20} color="#22c55e" />
                      <span style={{ fontWeight: '500', color: '#374151' }}>Real Face</span>
                    </div>
                    <span style={{ fontSize: '0.875rem', fontWeight: '600', color: '#374151' }}>
                      {((result.details.real_probability || 0) * 100).toFixed(2)}%
                    </span>
                  </div>
                </div>
              )}

              <div style={{
                marginTop: '1rem',
                padding: '0.75rem',
                backgroundColor: '#eff6ff',
                border: '1px solid #bfdbfe',
                borderRadius: '0.5rem',
                fontSize: '0.875rem',
                color: '#1e40af',
              }}>
                <p style={{ margin: 0 }}>
                  {isAIGenerated
                    ? '⚠️ This face appears to be AI-generated. It may not represent a real person.'
                    : '✓ This face appears to be from a real person and not AI-generated.'}
                </p>
              </div>
            </div>
          )}
        </div>

        {/* Footer */}
        <div style={{ marginTop: '2rem', textAlign: 'center', fontSize: '0.875rem', color: '#6b7280' }}>
          <p style={{ margin: '0.25rem 0' }}>Powered by EfficientNet-B3 with 90.24% validation accuracy</p>
          <p style={{ margin: '0.25rem 0' }}>
            Trained on 85,000+ real and AI-generated face images
          </p>
          <p style={{ margin: '0.25rem 0', fontSize: '0.8rem', fontStyle: 'italic' }}>
            Backend: Flask • Frontend: React • Face Detection: MTCNN
          </p>
        </div>
      </div>

      <style>{`
        @keyframes spin {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  );
}

export default App;