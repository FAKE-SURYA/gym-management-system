import React, { useState, useEffect } from 'react'
import Navbar from '../components/common/Navbar'
import api from '../services/api'
import LoadingSpinner from '../components/common/LoadingSpinner'

const Trainers = () => {
  const [trainers, setTrainers] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchTrainers()
  }, [])

  const fetchTrainers = async () => {
    try {
      const response = await api.get('/trainers/')
      setTrainers(response.data)
    } catch (error) {
      console.error('Error fetching trainers:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) return <LoadingSpinner />

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      
      <div className="p-6">
        <h1 className="text-3xl font-bold text-gray-800 mb-8">Trainers</h1>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {trainers.map((trainer) => (
            <div key={trainer.id} className="bg-white p-6 rounded-lg shadow-md">
              <h3 className="font-semibold text-lg">{trainer.full_name}</h3>
              <p className="text-gray-600">{trainer.email}</p>
              <p className="text-sm text-gray-500 mt-2">{trainer.phone}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

export default Trainers
