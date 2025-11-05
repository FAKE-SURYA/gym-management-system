import React, { useState, useEffect } from 'react'
import Navbar from '../components/common/Navbar'
import memberService from '../services/memberService'
import LoadingSpinner from '../components/common/LoadingSpinner'

const Members = () => {
  const [members, setMembers] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchMembers()
  }, [])

  const fetchMembers = async () => {
    try {
      const data = await memberService.getAllMembers()
      setMembers(data)
    } catch (error) {
      console.error('Error fetching members:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) return <LoadingSpinner />

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      
      <div className="p-6">
        <h1 className="text-3xl font-bold text-gray-800 mb-8">Members</h1>
        
        <div className="bg-white rounded-lg shadow-md overflow-hidden">
          <table className="w-full">
            <thead className="bg-gray-100 border-b">
              <tr>
                <th className="px-6 py-3 text-left text-sm font-semibold">ID</th>
                <th className="px-6 py-3 text-left text-sm font-semibold">Name</th>
                <th className="px-6 py-3 text-left text-sm font-semibold">Email</th>
                <th className="px-6 py-3 text-left text-sm font-semibold">Phone</th>
              </tr>
            </thead>
            <tbody>
              {members.map((member) => (
                <tr key={member.id} className="border-b hover:bg-gray-50">
                  <td className="px-6 py-3 text-sm">{member.id}</td>
                  <td className="px-6 py-3 text-sm font-medium">{member.full_name}</td>
                  <td className="px-6 py-3 text-sm">{member.email}</td>
                  <td className="px-6 py-3 text-sm">{member.phone}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}

export default Members
