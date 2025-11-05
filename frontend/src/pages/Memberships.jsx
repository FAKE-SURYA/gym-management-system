import React, { useState, useEffect } from 'react'
import Navbar from '../components/common/Navbar'
import membershipService from '../services/membershipService'
import LoadingSpinner from '../components/common/LoadingSpinner'

const Memberships = () => {
  const [memberships, setMemberships] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchMemberships()
  }, [])

  const fetchMemberships = async () => {
    try {
      const data = await membershipService.getAllMemberships()
      setMemberships(data)
    } catch (error) {
      console.error('Error fetching memberships:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) return <LoadingSpinner />

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      
      <div className="p-6">
        <h1 className="text-3xl font-bold text-gray-800 mb-8">Memberships</h1>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {memberships.map((membership) => (
            <div key={membership.id} className="bg-white p-6 rounded-lg shadow-md">
              <h3 className="font-semibold text-lg mb-2">Member ID: {membership.member_id}</h3>
              <p className="text-gray-600 mb-2">Plan: {membership.plan_id}</p>
              <p className="text-sm text-gray-500">
                {membership.start_date} to {membership.end_date}
              </p>
              <div className="mt-4">
                <span className={`px-3 py-1 rounded-full text-sm font-semibold ${
                  membership.status === 'active' 
                    ? 'bg-green-100 text-green-800' 
                    : 'bg-red-100 text-red-800'
                }`}>
                  {membership.status}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

export default Memberships
