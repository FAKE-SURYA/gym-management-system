import React, { useState, useEffect } from 'react'
import Navbar from '../components/common/Navbar'
import api from '../services/api'
import LoadingSpinner from '../components/common/LoadingSpinner'

const Attendance = () => {
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState('')

  const handleCheckIn = async () => {
    setLoading(true)
    try {
      const response = await api.post('/attendance/check-in')
      setMessage(`✅ ${response.data.message}`)
      setTimeout(() => setMessage(''), 3000)
    } catch (error) {
      setMessage(`❌ ${error.response?.data?.detail || 'Check-in failed'}`)
      setTimeout(() => setMessage(''), 3000)
    } finally {
      setLoading(false)
    }
  }

  const handleCheckOut = async () => {
    setLoading(true)
    try {
      const response = await api.post('/attendance/check-out')
      setMessage(`✅ ${response.data.message}`)
      setTimeout(() => setMessage(''), 3000)
    } catch (error) {
      setMessage(`❌ ${error.response?.data?.detail || 'Check-out failed'}`)
      setTimeout(() => setMessage(''), 3000)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      
      <div className="p-6">
        <h1 className="text-3xl font-bold text-gray-800 mb-8">Attendance Tracking</h1>
        
        <div className="bg-white p-8 rounded-lg shadow-md max-w-md mx-auto">
          <div className="space-y-4">
            <button
              onClick={handleCheckIn}
              disabled={loading}
              className="w-full bg-green-600 hover:bg-green-700 text-white font-bold py-3 px-4 rounded-lg disabled:opacity-50"
            >
              {loading ? 'Processing...' : 'Check In'}
            </button>
            
            <button
              onClick={handleCheckOut}
              disabled={loading}
              className="w-full bg-red-600 hover:bg-red-700 text-white font-bold py-3 px-4 rounded-lg disabled:opacity-50"
            >
              {loading ? 'Processing...' : 'Check Out'}
            </button>
          </div>
          
          {message && (
            <div className="mt-6 p-4 bg-gray-100 rounded-lg text-center">
              {message}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default Attendance
